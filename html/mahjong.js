enchant();

$(function() {
    var game = new Core(MahjongGame.sizeX, MahjongGame.sizeY);
    MahjongGame.setGame(game);
    var mahjong = MahjongGame.Game();
    mahjong.start();
});