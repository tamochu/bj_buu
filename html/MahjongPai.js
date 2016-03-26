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
        MahjongPai = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';

    var MahjongPai = {};

    MahjongPai.game_ = null;
    MahjongPai.setGame = function(game) {
        MahjongPai.game_ = game;
    };
    // 牌の大きさ。画像を変える場合はこちらも変えてください。
    MahjongPai.sizeXBase = 50;
    MahjongPai.sizeYBase = 74;
    // 拡大率
    MahjongPai.scale = 0.6;
    // 表示される牌の大きさ
    MahjongPai.sizeX = parseInt(MahjongPai.sizeXBase * MahjongPai.scale, 10);
    MahjongPai.sizeY = parseInt(MahjongPai.sizeYBase * MahjongPai.scale, 10);
    // 牌のイメージスプライト0番目が裏、ついでマンズ、ソウズ、ピンズ、字牌となります
    MahjongPai.image_ = "http://jsrun.it/assets/m/h/9/C/mh9CL.png";
    // 牌のクラスの本体
    MahjongPai.Pai = Class.create(Sprite, {
        // コンストラクタ。Spriteを継承しています。
        initialize: function() {
            Sprite.call(this, MahjongPai.sizeXBase, MahjongPai.sizeYBase);
            this.str = 'u0'; // m1～9,s1～9,p1～9,z1～7
            this.frame = 0;
            this.image = MahjongPai.game_.assets[MahjongPai.image_];
            this.scaleX = MahjongPai.scale;
            this.scaleY = MahjongPai.scale;
            this.id = -1;
            // 裏表示する際のフラグ
            this.uraFlag = false;
        },
        
        // 牌を指定する関数。public
        setFrame: function(str) {
            this.str = str;
            if (this.uraFlag) {
                this.frame = 0;
            } else {
                this.frame = MahjongPai.strToNum(str) + 1;
            }
        },
        
        // タッチしたときにゲームにイベントを返すようにする関数。public
        setId: function(id) {
            this.id = id;
            this.clearEventListener('touchstart');
            this.addEventListener('touchstart', function() {
                var e = new enchant.Event("select" + this.id);
                MahjongPai.game_.dispatchEvent(e);
            });
        },
        
        // 裏表示にするかどうかを設定する関数。引数にbooleanを渡す。public
        setUra: function(ura) {
            this.uraFlag = ura;
            this.setFrame(this.str);
        },
        
        // 牌の種類を簡単に取得するための関数。返り値は牌の種類を表す文字。public
        getType: function() {
            return this.str.substr(0, 1);
        },
        
        // 牌の種類を簡単に取得するための関数。返り値は牌の種類を表す数。public
        getNum: function() {
            return parseInt(this.str.substr(1, 1), 10);
        },
        
        // 牌の種類を簡単に取得するための関数。字牌かどうかを返す。public
        isTsu: function() {
            return (this.getType() === 'z');
        },
        
        // 牌の種類を簡単に取得するための関数。一九牌かどうかを返す。public
        isIku: function() {
            return (!this.isTsu() && (this.getNum() === 1 || this.getNum() === 9));
        },
        
        // 牌の種類を簡単に取得するための関数。一九字牌かどうかを返す。public
        isYaochu: function() {
            return (this.isTsu() || this.isIku());
        }
    });
    
    // 文字列をヒストグラムなどに使う数に変換する関数。public
    MahjongPai.strToNum = function(str) {
        var type = str.substr(0, 1);
        var num = parseInt(str.substr(1), 10);
        if (type === "m" && num >= 1 && num <= 9) {
            return (num - 1);
        } else if (type === "s" && num >= 1 && num <= 9) {
            return (num + 8);
        } else if (type === "p" && num >= 1 && num <= 9) {
            return (num + 17);
        } else if (type === "z" && num >= 1 && num <= 7) {
            return (num + 26);
        } else {
            return -1;
        }
    };
    
    // ヒストグラムなどに使う数を文字列に変換する関数。public
    MahjongPai.numToStr = function(num) {
        var type = parseInt(num / 9, 10);
        num = (num % 9) + 1;
        if (type === 0) {
            type = 'm';
        } else if (type === 1) {
            type = 's';
        } else if (type === 2) {
            type = 'p';
        } else if (type === 3) {
            type = 'z';
        } else {
            return 'u0';
        }
        return (type + num);
    };
    
    // ドラ表示牌からドラの文字列を返す関数。public
    MahjongPai.getDoraNextStr = function(pai) {
        var type = pai.getType();
        var num = pai.getNum() + 1;
        if (type === 'z') {
            if (num === 5) {
                num = 1;
            }else if (num === 8) {
                num = 5;
            }
        } else {
            if (num === 10) {
                num = 1;
            }
        }
        return (type + num);
    };
    
    // モジュールのエクスポート
    return MahjongPai;
});
