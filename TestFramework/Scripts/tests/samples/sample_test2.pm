#サンプルその２
#混乱が正常に動作しているかチェックする
package sample_test2;

#コントローラーで使う定数
use TestFramework::Controller::ControllerConst;

#混乱が正常に動作しているかチェックするテスト
sub run{

	#サンプルその１のように自分で初期設定を行わずに
	#生成されたシチュエーション（log, user, html, data)をロードする
	#situation1では６カ国１年目平和、開戦状態
	#1の国には（s1c1m, s1c2f)、２の国には(s1c2m, s1c2f)のように男女二名ずつ在籍している
	require $ControllerConst::SituationLoader;
	SituationLoader::load_siuation("situation1");
	
	#混乱で移動しない設定が正常に動作しているかテストするために、まず世界設定を混乱直前の年度にする
	require $ControllerConst::world_controller;
	$wc = WorldController->new();
	$wc->access_data("year", 39);

	#統一が簡単になるようにゲームレベルも下げておく
	$wc->access_data("game_lv", 1);

	#更に

}
1;
