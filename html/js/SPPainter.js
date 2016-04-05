var id, pass;
var image_size;
var painter;

var Painter = function(canvas) {

  this.foreCanvas = canvas;

  if (this.foreCanvas) {
    this.foreContext = this.foreCanvas.getContext("2d");
    this.foreContext.lineJoin = "round";
    this.foreContext.lineCap = "round";
    this.foreContext.width = canvas.width;
    this.foreContext.height = canvas.height;
    this.color = {"r": 0, "g": 0, "b": 0};
    this.binImage = null;

    this.backCanvas = $('<canvas></canvas>').get(0);
    this.backCanvas.width = this.foreCanvas.width;
    this.backCanvas.height = this.foreCanvas.height;
    this.backContext = this.backCanvas.getContext("2d");

    this.iconCanvas = $('<canvas></canvas>').get(0);
    this.iconCanvas.width = $("#image_width").val();
    this.iconCanvas.height = $("#image_height").val();
    this.iconContext = this.iconCanvas.getContext("2d");

    this.undoImage = null;
    this.redoImage = null;

    this.changeType("pen");
    this.changeColor("#000000");
    this.changeBackColor("#ffffff");
    this.changeWeight(12);
    this.changeAlpha(0);

    this.button = ["pen", "dropper", "paint", "line", "fillrect", "rect", "fillarc", "arc", "cutrect"];
  }
};

function getPageX(event) {
  return typeof event.originalEvent.changedTouches !== "undefined" ? event.originalEvent.changedTouches[0].pageX : event.pageX;
}
function getPageY(event) {
  return typeof event.originalEvent.changedTouches !== "undefined" ? event.originalEvent.changedTouches[0].pageY : event.pageY;
}

$(function() {
  id = $("#id").val();
  pass = $("#pass").val();
  if (id == null || pass == null) {
    alert("そのような名前のﾌﾟﾚｲﾔｰが存在しません");
    document.location = "index.cgi";
// インデックスに移動
  }
  image_size = parseInt($("#image_size").val(), 10);

  painter = new Painter($("#cv").get(0));

  $("#cv").bind({
    "touchstart mousedown": function(event) {
      event.preventDefault();
      painter.drawStart(event);
    },
    "touchmove mousemove": function(event) {
      event.preventDefault();
      painter.draw(event);
    },
    "touchend mouseup": function(event) {
      painter.drawEnd(event);
    }
  });

  for (var i = 0; i < painter.button.length; i++) {
    $("#" + painter.button[i]).on("click", function() {
      $(this).blur();
      painter.changeType($(this).val());
    });
  }

  var action = function(event, id, value) {
    $("#_" + id).text(value);
    painter.color[id] = value;
    var r = ("0" + parseInt(painter.color["r"]).toString(16)).substr(-2);
    var g = ("0" + parseInt(painter.color["g"]).toString(16)).substr(-2);
    var b = ("0" + parseInt(painter.color["b"]).toString(16)).substr(-2);
    painter.changeColor("#" + r + g + b);
    $("#color").val("#" + r + g + b);
  };
  var vars = ["r", "g", "b"];
  for (var i = 0; i < vars.length; i++) {
    $("#" + vars[i]).on("change", function(event) {
      action(event, $(this).attr("id"), $(this).val())
    });
  }

  $("#color").on("change", function() {
    var vars = ["r", "g", "b"];
    painter.changeColor($(this).val());
    for (var i = 0; i < vars.length; i++) {
      var c = parseInt(this.value.substr((i*2)+1,2), 16);
      $("#" + vars[i]).val(c);
      $("#_"+vars[i]).text(c);
    }
  });

  $("#weight").on("change", function() {
    $("#_weight").text($(this).val());
    painter.changeWeight($(this).val());
  });

  $("#alpha").on("change", function() {
    $("#_alpha").text(parseInt($(this).val / 10, 10));
    painter.changeAlpha($(this).val());
  });

  $("#backcolor").on("change", function() {
    painter.changeBackColor($(this).val())
  });

  $("#undo").on("click", function() {
    $(this).blur();
    painter.undo();
  });

  $("#redo").on("click", function() {
    $(this).blur();
    painter.redo();
  });

  $("#convert").on("click", function() {
    $(this).blur();
    painter.mixtureImage(true, 0, 0, painter.foreCanvas.width, painter.foreCanvas.height);
  });

  $("#clear").on("click", function() {
    $(this).blur();
    if (confirm("本当に消しますか？")) {
      painter.saveundo();
      painter.clear();
      painter.saveredo();
    }
  });

  $("#file").on("change", function() {
    var file = $(this).prop('files')[0];
    
    if (!file.type.match('image.*')) {
      $(this).val('');
      return;
    }
    if (navigator.userAgent.indexOf('iPhone') > 0 || navigator.userAgent.indexOf('iPad') > 0 || navigator.userAgent.indexOf('iPod') > 0) {
      var UrlObject = window.URL || window.webkitURL;
      var blobUrl = UrlObject.createObjectURL(file);

      var tmpImage = new Image();
      tmpImage.src = blobUrl;
      tmpImage.onload = function() {
        painter.foreContext.drawImage(this, 0, 0, painter.foreCanvas.width, painter.foreCanvas.height);
        painter.mixtureImage(true, 0, 0, painter.foreCanvas.width, painter.foreCanvas.height);
      };
      tmpImage.onerror = function(e) {
        alert("imgError:" + e);
      };
    } else {
      var reader = new FileReader();
      reader.onload = function() {
        var img_src = $('<img>').attr('src', reader.result);
        painter.foreContext.drawImage(img_src.get(0), 0, 0, painter.foreCanvas.width, painter.foreCanvas.height);
        painter.mixtureImage(true, 0, 0, painter.foreCanvas.width, painter.foreCanvas.height);
      };
      reader.readAsDataURL(file);
    }
  });

  $("#send").on("click", function() {
    if (id == null || pass == null) {
      alert("そのような名前のﾌﾟﾚｲﾔｰが存在しません");
      return;
    }
    if (painter.binImage.byteLength > 0 && painter.binImage.byteLength <= image_size) {
      var filename = "_temp";

      var data = new FormData();
      var blob = new Blob([painter.binImage], {type: "image/"+$("#ext").text()});
      data.append("id", id);
      data.append("pass", pass);
      data.append("file", blob, filename+"."+$("#ext").text());

      var xhr = new XMLHttpRequest;

      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
          if (xhr.status == 200 || xhr.status == 304) {
            var result = xhr.responseText; // responseXML もあり
            if (result.length > 0) {
              alert(result);
            }
            else {
              document.location = "bj.cgi?id="+id+"&pass="+pass;
            }
          } else {
            alert('Failed. HttpStatus: '+xhr.statusText);
          }
        }
      };

      xhr.open("POST", $("#url_save").val(), false);
      xhr.send(data);

    }
  });
});

Painter.prototype.switchButton = function(id1, id2) {
  $("#" + id1).removeClass("on");
  $("#" + id1).addClass("off");
  $("#" + id2).addClass("on");
  $("#" + id2).removeClass("off");
};

Painter.prototype.clear = function() {
  this.foreContext.beginPath();
  this.foreContext.clearRect(0, 0, this.foreCanvas.width, this.foreCanvas.height);
};

Painter.prototype.undo = function() {
  this.foreContext.putImageData(this.undoImage, 0, 0);
};

Painter.prototype.saveundo = function() {
  delete this.undoImage;
  this.undoImage = this.foreContext.getImageData(0, 0, this.foreCanvas.width, this.foreCanvas.height);
};

Painter.prototype.redo = function() {
  this.foreContext.putImageData(this.redoImage, 0, 0);
};

Painter.prototype.saveredo = function() {
  delete this.redoImage;
  this.redoImage = this.foreContext.getImageData(0, 0, this.foreCanvas.width, this.foreCanvas.height);
};

Painter.prototype.mixtureImage = function(png, x, y, width, height) {
  var ext = png ? "image/png" : "image/jpeg";
  var foreImage = $("<img>");
  var backImage = $("<img>");

  backImage.attr("src", painter.backCanvas.toDataURL(ext));
  backImage.on("load", function() {
    painter.iconContext.drawImage(this, 0, 0, painter.iconCanvas.width, painter.iconCanvas.height);

    foreImage.attr("src", painter.foreCanvas.toDataURL(ext));
    foreImage.on("load", function() {
      delete backImage;
      x = x < 0 ? 0 : x;
      y = y < 0 ? 0 : y;
      width = width > painter.foreCanvas.width ? painter.foreCanvas.width : width;
      height = height > painter.foreCanvas.height ? painter.foreCanvas.height : height;

      painter.iconContext.drawImage(this, parseInt(x, 10), parseInt(y, 10), parseInt(width, 10), parseInt(height, 10), 0, 0, painter.iconCanvas.width, painter.iconCanvas.height);

      var image = painter.iconCanvas.toDataURL(ext);
      var base64data = image.split(',')[1];
      var tmpBinImage = b64utils.decode(base64data);

      if (png) {
        if (tmpBinImage.byteLength > image_size) {
          delete foreImage;
          painter.mixtureImage(false, x, y, width, height);
        }
        else {
          $("#newImg").attr("src", image);
          $("#ext").text("png");
          $("#size").text(tmpBinImage.byteLength);
          painter.binImage = tmpBinImage;
          delete foreImage;
          $("#_send").addClass("enable");
        }
      }
      else {
        if (tmpBinImage.byteLength > image_size) {
          delete foreImage;
          alert("画像ファイルが" + image_size + "Byteを超えています");
        }
        else {
          $("#newImg").attr("src", image);
          $("#ext").text("jpeg");
          $("#size").text(tmpBinImage.byteLength);
          painter.binImage = tmpBinImage;
          delete foreImage;
          $("#_send").addClass("enable");
        }
      }
    });
  });
};

Painter.prototype.dropColor = function(x, y) {
  x = x < 0 ? 0 : x;
  y = y < 0 ? 0 : y;

  var foreImage = this.foreContext.getImageData(x, y, 1, 1);
  var vars = ["r", "g", "b"];
  var rgb = [];
  for (var i = 0; i < vars.length; i++) {
    rgb[i] = foreImage.data[i];
    $("#" + vars[i]).val(rgb[i]);
    $("#_" + vars[i]).text(rgb[i]);
  }

  var cc = "#"+("0"+rgb[0].toString(16)).substr(-2)+("0"+rgb[1].toString(16)).substr(-2)+("0"+rgb[2].toString(16)).substr(-2);
  this.changeColor(cc);
  this.changeType("pen");
  $("#color").val(cc);
};

Painter.prototype.paintFill = function(x, y) {
  var alphas = [255, 228, 203, 177, 152, 126, 101, 75, 49, 24, 0];

  var cfa = new CanvasFillAlgorithm(this.foreCanvas);

  var r = parseInt(this.foreContext.fillStyle.substr(1,2), 16);
  var g = parseInt(this.foreContext.fillStyle.substr(3,2), 16);
  var b = parseInt(this.foreContext.fillStyle.substr(5,2), 16);
  var a = alphas[parseInt(10-this.foreContext.globalAlpha*10)];
  var c = ((r<<24) | (g<<16) | (b<<8) | a) >>> 0;

  cfa.paint(x, y, c);
};

Painter.prototype.changeType = function(type) {
  if (this.drawType) { this.switchButton(this.drawType, type); }
  this.drawType = type;
};

Painter.prototype.changeColor = function(color) {
  this.foreContext.strokeStyle = color;
  this.foreContext.fillStyle = color;
};

Painter.prototype.changeWeight = function(weight) {
  this.foreContext.lineWidth = weight;
  this.foreContext.strokeWidth = weight;
};

Painter.prototype.changeAlpha = function(alpha) {
  this.alpha = 1 - (alpha / 10);
  this.foreContext.globalAlpha = this.alpha;
};

Painter.prototype.changeBackColor = function(color) {
  this.backContext.strokeStyle = color;
  this.backContext.fillStyle = color;
  this.backContext.fillRect(0, 0, this.backCanvas.width, this.backCanvas.height);
};

Painter.prototype.drawStart = function(event) {
  this.drawFlag = true;
  this.saveundo();
  
  var rect = event.target.getBoundingClientRect();
  this.startx = getPageX(event)
  this.startx -= rect.left;
  this.startx -= $(window).scrollLeft();
  this.starty = getPageY(event);
  this.starty -= rect.top;
  this.starty -= $(window).scrollTop();

  switch (this.drawType) {
  case "paint":
  case "dropper":
    this.endx = this.startx;
    this.endy = this.starty;
    break;
  case "fillarc":
  case "arc":
    this.foreContext.beginPath();
    break;
  case "pen":
  case "line":
    this.foreContext.beginPath();
    this.foreContext.moveTo(this.startx, this.starty);
    break;
  }
};

Painter.prototype.draw = function(event) {
  if (!this.drawFlag) { return false; }

  var rect = event.target.getBoundingClientRect();
  this.endx =  getPageX(event);
  this.endx -= rect.left;
  this.endx -= $(window).scrollLeft();
  this.endy = getPageY(event);
  this.endy -= rect.top;
  this.endy -= $(window).scrollTop();

  if (this.drawType == "pen") {
    this.foreContext.lineTo(this.endx, this.endy);
    this.foreContext.stroke();
  }
  else {
    this.foreContext.globalAlpha = 0.1;
    var posx = Math.min(this.startx, this.endx);
    var posy = Math.min(this.starty, this.endy);
    var width = Math.max(this.startx, this.endx) - posx;
    var height = Math.max(this.starty, this.endy) - posy;
    if (this.drawType == "fillarc" || this.drawType == "arc") {
      this.clear();
      this.undo();
      this.foreContext.arc(this.startx, this.starty, Math.max(width, height) / 2, 0, Math.PI * 2, false);
      if (this.drawType == "fillarc") {
        this.foreContext.fill();
      } else {
        this.foreContext.stroke();
      }
    } else {
      this.undo();
    }
    switch (this.drawType) {
    case "line":
      this.foreContext.beginPath();
      this.foreContext.moveTo(this.startx, this.starty);
      this.foreContext.lineTo(this.endx, this.endy);
      this.foreContext.stroke();
      break;
    case "fillrect":
      this.foreContext.fillRect(posx, posy, width, height);
      break;
    case "cutrect":
      this.foreContext.globalAlpha = 0.2;
      var size = Math.max(width, height);
      this.foreContext.fillRect(this.startx - size / 2, this.starty - size  / 2, size, size);
      break;
    case "rect":
      this.foreContext.strokeRect(posx, posy, width, height);
      break;
    }
  }
};

Painter.prototype.drawEnd = function(event) {
  this.undo();
  if (this.drawType == "pen") {
    this.foreContext.stroke();
  }
  else {
    this.foreContext.globalAlpha = this.alpha;
    var posx = Math.min(this.startx, this.endx);
    var posy = Math.min(this.starty, this.endy);
    var width = Math.max(this.startx, this.endx) - posx;
    var height = Math.max(this.starty, this.endy) - posy;
    if (this.drawType == "fillarc" || this.drawType == "arc") {
      this.foreContext.arc(this.startx, this.starty, Math.max(width, height) / 2, 0, Math.PI * 2, false);
      if (this.drawType == "fillarc") {
        this.foreContext.fill();
      } else {
        this.foreContext.stroke();
      }
    }
    
    switch (this.drawType) {
    case "line":
      this.foreContext.lineTo(this.endx, this.endy);
      this.foreContext.stroke();
      break;
    case "fillrect":
      this.foreContext.fillRect(posx, posy, width, height);
      break;
    case "cutrect":
      var size = Math.max(width, height);
      this.mixtureImage(true, this.startx - size / 2, this.starty - size / 2, size, size);
      break;
    case "dropper":
      this.dropColor(this.endx, this.endy);
      break;
    case "paint":
        painter.paintFill(painter.endx, painter.endy);
      break;
    case "rect":
      this.foreContext.strokeRect(posx, posy, width, height);
      break;
    }
  }
  this.foreContext.closePath();

  this.drawFlag = false;
  this.saveredo();
};

function obj_dump(obj) {
  var text = "";
  var cnt = 0;
  for (var one in obj) {
    cnt++;
    if (cnt >= 5) {
      alert(text);
      text = "";
      cnt = 0;
    }
    text += one + "=" + obj[one] + "\n\n\n";
  }
  alert(text);
}
