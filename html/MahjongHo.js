enchant();

(function(definition){// 定義する関数を引数にとる
    // ロードされた文脈に応じてエクスポート方法を変える

    // CommonJS
    if (typeof exports === "object") {
        module.exports = definition();

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
        define(definition);

    // <script>
    } else {
        MahjongHo = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';

    var MahjongHo = {};

    MahjongHo.game_ = null;
    MahjongHo.setGame = function(game) {
        MahjongHo.game_ = game;
    };
    // 河のクラス本体
    MahjongHo.Ho = Class.create({
        // コンストラクタ
        initialize: function() {
            this.ho = [];
            this.reachAt = null;
            this.position = 0;// 0:下 1:右 2:上 3:左
            this.eaten = [];
        },
        
        // どこに表示する河か設定する関数。public
        setPosition: function(position) {
            this.position = position;
        },
        
        // 河に牌を追加する関数。引数は文字列なので注意。public
        addHo: function(str) {
            var pai = MahjongPai.Pai();
            pai.setFrame(str);
            this.ho.push(pai);
        },
        
        // 立直をする関数。public
        reach: function() {
            if (this.reachAt === null) {
                if (this.ho.length > 0) {
                    this.reachAt = this.ho.length - 1;
                    this.refresh();
                }
            }
        },
        
        // 鳴かれたときに呼ぶ関数。public
        eat: function() {
            if (this.ho.length > 0) {
                this.eaten.push(this.ho.length - 1);
                this.refresh();
            }
        },
        
        // 再描画フラグを立てる関数。
        refresh: function() {
            this.show();
        },
        
        // setAllで読み込める形で河の情報を文字列化する関数。public
        toString: function() {
            var retStr = "";
            for (var i = 0; i < this.ho.length; i++) {
                retStr += this.ho[i].str;
                if (i === this.reachAt) {
                    retStr += "r";
                }
                if (jQuery.inArray(i, this.eaten) === -1) {
                    retStr += "e";
                }
            }
            return retStr;
        },
        
        // 河を表示させる関数。public
        show: function() {
            this.showCore(false);
        },
        
        // 表示の内部関数。
        showCore: function(addFlag) {
            var beginPosX = 145;
            var beginPosY = 340;
            var directXX = 1;
            var directXY = 0;
            var directYX = 0;
            var directYY = 1;
            var rotate = 0;
            if (this.position === 1) {
                beginPosX = 345;
                beginPosY = 345;
                directXX = 0;
                directXY = -1;
                directYX = 1;
                directYY = 0;
                rotate = 270;
            } else if (this.position === 2) {
                beginPosX = 355;
                beginPosY = 145;
                directXX = -1;
                directXY = 0;
                directYX = 0;
                directYY = -1;
                rotate = 180;
            } else if (this.position === 3) {
                beginPosX = 145;
                beginPosY = 135;
                directXX = 0;
                directXY = 1;
                directYX = -1;
                directYY = 0;
                rotate = 90;
            }
            var posX = beginPosX;
            var posY = beginPosY;
            var index = 0;
            var sleepPai = false;
            for (var i = 0; i < this.ho.length; i++) {
                if (i === this.reachAt) {
                    sleepPai = true;
                }
                if (jQuery.inArray(i, this.eaten) == -1) {
                    var pai = this.ho[i];
                    if (sleepPai) {
                        pai.x = posX + directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 + directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        pai.y = posY + directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 + directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        pai.rotation = rotate + 90;
                        posX += directXX * MahjongPai.sizeY;
                        posY += directXY * MahjongPai.sizeY;
                        sleepPai = false;
                    } else {
                        pai.x = posX;
                        pai.y = posY;
                        pai.rotation = rotate;
                        posX += directXX * MahjongPai.sizeX;
                        posY += directXY * MahjongPai.sizeX;
                    }
                    if (!addFlag || i === this.ho.length - 1) {
                        MahjongHo.game_.rootScene.addChild(pai);
                    }
                    index++;
                    if (index % 6 === 0 && index < 18) {
                        var row = index / 6;
                        posX = beginPosX + directYX * row * MahjongPai.sizeY;
                        posY = beginPosY + directYY * row * MahjongPai.sizeY;
                    }
                }
            }
        },
        
        // 文字列から河情報を読み込む関数。public
        setAll: function(str) {
            this.ho = [];
            this.reachAt = null;
            this.eaten = [];
            var split_str = str.split('');
            var i = 0;
            while (i < split_str.length) {
                var c = split_str[i];
                if (c === 'm' || c === 's' || c === 'p' || c === 'z') {
                    var num = split_str[i + 1];
                    this.addHo(c + num);
                    i++;
                } else if (c === 'r') {
                    this.reach();
                } else if (c === 'e') {
                    this.eat();
                }
                i++;
            }
        }
    });
    
    // モジュールのエクスポート
    return MahjongHo;
});
