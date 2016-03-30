/*
this.addEventListener('message', function(e) {
  var jsonImage = e.data;
  var imageData = jsonImage.data;

  self.postMessage('Unknown command: ' + data.msg);
  };
}, false);
*/

//
// 元アルゴリズム: http://fussy.web.fc2.com/algo/algo3-2.htm
// JavaScript implementation - 2013 imaya
//

/**
 * @param {HTMLCanvasElement} canvas
 * @constructor
 */
CanvasFillAlgorithm = function(canvas) {
//CanvasFillAlgorithm = function(imageData) {
  /** @type {HTMLCanvasElement} */
  this.canvas = canvas;
  /** @type {CanvasRenderingContext2D} */
  this.ctx = canvas.getContext('2d');
  /** @type {ImageData} */
  this.imageData = this.ctx.getImageData(0, 0, canvas.width, canvas.height);
  /** @type {(CanvasPixelArray|Uint8ClampedArray)} */
  this.buffer = this.imageData.data;
  /** @type {Array.<Object>} */
  this.stack = [];
  /** @type {number} */
  this.colorDistance = 0.2;
  /** @type {number} */
  this.alphaDistance = 96;
};

/**
 * @param {number} distance
 */
CanvasFillAlgorithm.prototype.setColorDistance = function(distance) {
  this.colorDistance = distance;
};

/**
 * @param {number} distance
 */
CanvasFillAlgorithm.prototype.setAlphaDistance = function(distance) {
  this.alphaDistance = distance;
};

/** @type {number} @const */
CanvasFillAlgorithm.MaxDistance = Math.sqrt(255 * 255 * 3);

/**
 * @param {(CanvasPixelArray|Uint8ClampedArray)} buffer
 * @param {number} x
 * @param {number} y
 * @param {number} width
 * @return {number}
 */
CanvasFillAlgorithm.prototype.point = function(buffer, x, y, width) {
  /** @type {number} */
  var baseIndex = (width * y + x) * 4;

  return (
    (buffer[baseIndex    ] << 24) |
    (buffer[baseIndex + 1] << 16) |
    (buffer[baseIndex + 2] <<  8) |
    (buffer[baseIndex + 3]      )
  ) >>> 0;
};

/**
 * @param {(CanvasPixelArray|Uint8ClampedArray)} buffer
 * @param {number} x
 * @param {number} y
 * @param {number} width
 * @param {number} color
 */
CanvasFillAlgorithm.prototype.setColor = function(buffer, x, y, width, color) {
  /** @type {number} */
  var baseIndex = (width * y + x) * 4;

  buffer[baseIndex    ] = (color >> 24) & 0xff;
  buffer[baseIndex + 1] = (color >> 16) & 0xff;
  buffer[baseIndex + 2] = (color >>  8) & 0xff;
  buffer[baseIndex + 3] = (color      ) & 0xff;
};

/**
 * @param {number} color1
 * @param {number} color2
 * @return {boolean}
 */
CanvasFillAlgorithm.prototype.equalsColors = function(color1, color2) {
  /**
   * @param {number} color1
   * @param {number} color2
   * @return {number}
   */
  function colorDistance(color1, color2) {
    return Math.sqrt(
      Math.pow(((color1 >> 24) & 0xff) - ((color2 >> 24) & 0xff), 2) +
      Math.pow(((color1 >> 16) & 0xff) - ((color2 >> 16) & 0xff), 2) +
      Math.pow(((color1 >>  8) & 0xff) - ((color2 >>  8) & 0xff), 2)
    ) / CanvasFillAlgorithm.MaxDistance;
  }

  /**
   * @param {number} color1
   * @param {number} color2
   * @return {number}
   */
  function alphaDistance(color1, color2) {
    /** @type {number} */
    var sub = (color1 & 0xff) - (color2 & 0xff);

    return sub < 0 ? -sub : sub;
  }

  return ((color1 & 0xff) === 0 && (color2 & 0xff) === 0) ? true : (
    colorDistance(color1, color2) <= this.colorDistance &&
    alphaDistance(color1, color2) <= this.alphaDistance
  );
};

/**
 * @param {number} xLeft
 * @param {number} xRight
 * @param {number} y
 * @param {number} yParent
 * @param {number} color
 */
CanvasFillAlgorithm.prototype.scanLine = function(xLeft, xRight, y, yParent, color) {
  /** @type {(CanvasPixelArray|Uint8ClampedArray)} */
  var buffer = this.buffer;
  /** @type {number} */
  var width = this.imageData.width;
  /** @type {Array.<Object>} */
  var stack = this.stack;
  /** @type {Object} */
  var data;

  while (xLeft <= xRight) {
    // 非領域色を飛ばす
    for (; xLeft < xRight; xLeft++) {
      if (this.equalsColors(this.point(buffer, xLeft, y, width), color)) {
        break;
      }
    }

    // 既に塗ってあったら飛ばす
    if (!this.equalsColors(this.point(buffer, xLeft, y, width), color)) {
      break;
    }

    data = {};
    data.xLeft = xLeft;

    // 領域色を飛ばす
    for (; xLeft <= xRight ; xLeft++) {
      if (!this.equalsColors(this.point(buffer, xLeft, y, width), color)) {
        break;
      }
    }

    data.xRight = xLeft - 1;
    data.y = y;
    data.yParent = yParent;

    stack.push(data);
  }
};

/**
 * @param {number} x
 * @param {number} y
 * @param {number} paintColor
 */
CanvasFillAlgorithm.prototype.paint = function(x, y, paintColor) {
  /** @type {(CanvasPixelArray|Uint8ClampedArray)} */
  var buffer = this.buffer;
  /** @type {number} */
  var width = this.imageData.width;
  /** @type {number} */
  var height = this.imageData.height;
  /** @type {Array.<Object>} */
  var stack = this.stack;
  /** @type {number} */
  var xLeft;
  /** @type {number} */
  var xRight;
  /** @type {number} */
  var yParent;
  /** @type {number} */
  var targetColor = this.point(buffer, x, y, width);
  /** @type {number} */
  var nextLeft;
  /** @type {number} */
  var nextRight;
  /** @type {Object} */
  var seed;
  /** @type {number} */
  var i;

//    alert(targetColor);
//    alert(paintColor);

  // 領域色と描画色が等しければ処理不要
  if (this.equalsColors(targetColor, paintColor)) {
    return;
  }

  seed = {};
  seed.xLeft = seed.xRight  = x;
  seed.y     = seed.yParent = y;
  stack.push(seed);

  do {
    seed = stack.pop();

    xLeft = seed.xLeft;
    xRight = seed.xRight;
    y = seed.y;
    yParent = seed.yParent;

    nextLeft  = xLeft  - 1;
    nextRight = xRight + 1;

    // seed
    if (!this.equalsColors(this.point(buffer, xLeft, y, width), targetColor)) {
      continue;
    }

    // search right
    while (xRight < width) {
      if (!this.equalsColors(this.point(buffer, xRight + 1, y, width), targetColor)) {
        break;
      }
      xRight++;
    }

    // search left
    while (xLeft > 0) {
      if (!this.equalsColors(this.point(buffer, xLeft - 1, y, width), targetColor)) {
        break;
      }
      xLeft--;
    }

    // draw left to right
    for (i = xLeft; i <= xRight; ++i) {
      this.setColor(buffer, i, y, width, paintColor);
    }

    // search up
    if (y - 1 >= 0) {
      if (y - 1 === yParent) {
        this.scanLine(xLeft, nextLeft,  y - 1, y, targetColor);
        this.scanLine(nextRight, xRight, y - 1, y, targetColor);
      } else {
        this.scanLine(xLeft, xRight, y - 1, y, targetColor);
      }
    }

    // search down
    if (y + 1 < height) {
      if (y + 1 === yParent) {
        this.scanLine(xLeft, nextLeft,  y + 1, y, targetColor);
        this.scanLine(nextRight, xRight, y + 1, y, targetColor);
      } else {
        this.scanLine(xLeft, xRight, y + 1, y, targetColor);
      }
    }
  } while (stack.length > 0);

//  return this.imageData;
  this.ctx.putImageData(this.imageData, 0, 0);
};
