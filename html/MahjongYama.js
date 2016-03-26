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
        MahjongYama = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';

    var MahjongYama = {};
    
    MahjongYama.game_ = null;
    MahjongYama.setGame = function(game) {
        MahjongYama.game_ = game;
    };
    // ゲーム終了時に残る山牌数
    MahjongYama.restPais = 14;
    // 山のクラスの本体
    MahjongYama.Yama = Class.create({
        // コンストラクタ
        initialize: function() {
            this.restNum = 122;
            this.kanNum = 1;
            this.dora = [];
            this.ura = MahjongPai.Pai();
            this.ura.setFrame('u0');
            this.label = new Label("×" + this.getRest());
            this.label.color = '#FFF';
        },
        
        // カンの数を返す関数。public
        getKanNum: function() {
            return this.kanNum;
        },
        
        // 山を読み込む関数。public
        setJson: function(data) {
            this.restNum = data.RestNum;
            this.kanNum = data.KanNum;
            this.dora = data.Dora;
        },
        
        // 残りツモ数を返す関数。public
        getRest: function() {
            return this.restNum;
        },
        
        // ドラを現す文字列の配列を返す関数。public
        getDoraStrs: function() {
            return this.dora;
        },
        // 山の情報を表示する関数。public
        show: function() {
            var posX = MahjongYama.game_.width * 0.38;
            var posY = MahjongYama.game_.height * 0.38;
            this.ura.x = posX;
            this.ura.y = posY;
            this.label.x = posX + MahjongPai.sizeX * 1.5;
            this.label.y = posY + MahjongPai.sizeY / 2;
            this.label.text = "×" + this.getRest();
            MahjongYama.game_.rootScene.addChild(this.ura);
            MahjongYama.game_.rootScene.addChild(this.label);
            
            posY += MahjongPai.sizeY;
            for (var i = 0; i < this.dora.length; i++){
                var dora = MahjongPai.Pai();
                dora.setFrame(this.dora[i]);
                dora.x = posX + i * MahjongPai.sizeX;
                dora.y = posY;
                MahjongYama.game_.rootScene.addChild(dora);
            }
        }
    });
    
    return MahjongYama;
});