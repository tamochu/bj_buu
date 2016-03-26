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
        MahjongPlayerInfo = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';

    var MahjongPlayerInfo = {};

    MahjongPlayerInfo.game_ = null;
    MahjongPlayerInfo.setGame = function(game) {
        MahjongPlayerInfo.game_ = game;
    };
    // プレイヤー情報のクラス本体
    MahjongPlayerInfo.PlayerInfo = Class.create({
        // コンストラクタ
        initialize: function() {
            this.playerName = "player";
            this.point = 25000;
            this.position = 0;// 0:下 1:右 2:上 3:左
            this.infoLabel = new Label();
            this.infoLabel.font = "8px cursive";
        },
        
        // プレイヤーの位置を設定する関数。public
        setPosition: function(position) {
            this.position = position;
        },
        
        // プレイヤー名を設定する関数。public
        setPlayerName: function(playerName) {
            this.playerName = playerName;
        },
        
        // プレイヤー名のゲッター。public
        getPlayerName: function() {
            return this.playerName;
        },
        
        // 持ち点を設定する関数。public
        setPoint: function(point) {
            this.point = point;
        },
        
        // 持ち点を増減する関数。public
        pointAdd: function(point) {
            this.point += point;
        },
        
        // ﾌﾟﾚｲﾔｰ情報を表示させる関数。public
        show: function() {
            var entityWidth = MahjongPlayerInfo.game_.width * 0.23;
            var entityHeight = MahjongPlayerInfo.game_.height * 0.03;
            var posX = MahjongPlayerInfo.game_.width * 0.35;
            var posY = MahjongPlayerInfo.game_.height * 0.6;
            var rotate = 0;
            if (this.position === 1) {
                posX = MahjongPlayerInfo.game_.width * 0.49;
                posY = MahjongPlayerInfo.game_.height * 0.51;
                rotate = 270;
            } else if (this.position === 2) {
                posX = MahjongPlayerInfo.game_.width * 0.4;
                posY = MahjongPlayerInfo.game_.height * 0.37;
                rotate = 180;
            } else if (this.position === 3) {
                posX = MahjongPlayerInfo.game_.width * 0.25;
                posY = MahjongPlayerInfo.game_.height * 0.46;
                rotate = 90;
            }
            this.infoLabel.text = this.playerName + ":" + this.point;
            this.infoLabel.x = posX;
            this.infoLabel.y = posY;
            this.infoLabel.width = entityWidth;
            this.infoLabel.height = entityHeight;
            this.infoLabel.backgroundColor = 'white';
            this.infoLabel.rotation = rotate;
            MahjongPlayerInfo.game_.rootScene.addChild(this.infoLabel);
        }
    });
    
    // モジュールのエクスポート
    return MahjongPlayerInfo;
});
