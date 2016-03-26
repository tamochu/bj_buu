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
        MahjongPhyPai = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';

    var MahjongPhyPai = {};

    MahjongPhyPai.game_ = null;
    MahjongPhyPai.setGame = function(game) {
        MahjongPhyPai.game_ = game;
    };
    // 牌の大きさ。画像を変える場合はこちらも変えてください。
    MahjongPhyPai.sizeX = 30;
    MahjongPhyPai.sizeY = 46;
    // 牌のイメージスプライト0番目が裏、ついでマンズ、ソウズ、ピンズ、字牌となります
    MahjongPhyPai.image_ = "http://buu.pandora.nu/cgi-bin/bjtest/html/phyPai.png";
    // 牌のクラスの本体
    MahjongPhyPai.PhyPai = Class.create(PhyBoxSprite, {
        // コンストラクタ。Spriteを継承しています。
        initialize: function() {
            PhyBoxSprite.call(this, MahjongPhyPai.sizeX, MahjongPhyPai.sizeY, DYNAMIC_SPRITE, 1.0, 5.0, 0.2, true);
            this.str = 'u0'; // m1～9,s1～9,p1～9,z1～7
            this.frame = 0;
            this.image = MahjongPhyPai.game_.assets[MahjongPhyPai.image_];
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
                this.frame = MahjongPhyPai.strToNum(str) + 1;
            }
        },
        
        // IDのセッター。public
        setId: function(str, no) {
            this.setFrame(str);
            this.id = str + no;
            this.clearEventListener('pickup');
            this.addEventListener('pickup', function() {
                $.ajax({
                    type: 'POST',
                    url: 'chat_casino.cgi',
                    data: {
                        id: $("#id").val(),
                        pass: $("#pass").val(),
                        mode: 'tedumi',
                        arg: str + no
                    }
                });
            });
        },
        
        // クリックトリガー。public
        ontouchstart: function() {
            var e = new enchant.Event('pickup');
            this.dispatchEvent(e);
        },
        
        // 裏表示にするかどうかを設定する関数。引数にbooleanを渡す。public
        setUra: function(ura) {
            this.uraFlag = ura;
            this.setFrame(this.str);
        },
        
        // 裏返す関数。public
        reverse: function() {
            this.setUra(!this.uraFlag);
        },
    });    
    // 文字列をヒストグラムなどに使う数に変換する関数。public
    MahjongPhyPai.strToNum = function(str) {
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
    MahjongPhyPai.numToStr = function(num) {
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
    // モジュールのエクスポート
    return MahjongPhyPai;
});
