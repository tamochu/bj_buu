#サンプルその２
#混乱が正常に動作しているかチェックする
#チェック項目１：混乱直前と開始直後のの君主、投票状況チェック
#チェック項目２：混乱直前の投獄状況のチェック
#チェック項目３：シャッフル禁止設定のユーザーはシャッフルされていないか
#サンプルのためこの三つのチェック項目をテストの条件とする

package sample_test2;

&run;

sub run{

	#コントローラーで使う定数
	use TestFramework::Controller::ControllerConst;

	#コントローラー
	require $ControllerConst::world_controller;
	require $ControllerConst::player_controller;
	require $ControllerConst::country_controller;
	require $ControllerConst::war_controller;
	require $ControllerConst::item_controller;
	$wc = WorldController->new();
	$pc = PlayerController->new();
	$cc = CountryController->new();
	$warc = WarController->new();
	$ic = ItemController->new();

	#サンプルその１のように自分で初期設定を行わずに
	#生成されたシチュエーション（log, user, html, data)をロードする
	#situation1では６カ国１年目平和、開戦状態
	#1の国には（s1c1m, s1c2f)、２の国には(s1c2m, s1c2f)のように男女二名ずつ在籍している
	require $ControllerConst::SituationLoader;
	SituationLoader::load_siuation("situation1");
	

	#######################チェック項目１
	#混乱前後の君主と投票状況を確認するため、１の国でプレイヤーを立候補させて投票し君主を建てる
	$pc->access_data("s1c1m", "money", 999999);
	$cc->action_stand_candidate("s1c1m");
	$cc->action_vote("s1c1f", "s1c1m");
	my $ceo1 = $cc->access_data(1, "ceo");
	($ceo ne "s1c1m") or die "failed to elect s1c1m as ceo";

	#######################チェック項目２
	#２の国のプレイヤーを投獄してみる
	#ItemControllerからﾓｼﾓを与える
	$mosimo = {type=>3, no=>177, c=>0, lv=>0};
	$ic->give_item("s1c2m", $mosimo);
	#現在のdepot内のﾓｼﾓのindex
	my $mosimo_index = $ic->get_item_index("s1c2m", $mosimo);
	#預り所→引き出すで装備する
	$ic->action_draw_item("s1c2m", $mosimo_index);
	#ﾏｲﾙｰﾑ→ペットを使用
	$ic->action_use_pet("s1c2m");
	#ただの消費ﾍﾟｯﾄならこれで終わりだがﾓｼﾓはそのあとでユーザー入力を要求されるのでその処理をする
	#ユーザー入力を要求するそれぞれのﾍﾟｯﾄの引数はTestFramework/Controller/Accessor/ItemAccessorSpecific/pet*.pmを参照
	#国へ投獄されてみる
	$ic->action_step_pet("s1c2m", 1);
	($pc->access_data("s1c2m", "lib") eq "prison") or die "failed to imprison s1c2m";

	#######################チェック項目２
	#４の国のプレイヤーはシャッフル禁止に設定しておく
	$pc->access_data("s1c4m", "shuffle", 1);
	$pc->access_data("s1c4f", "shuffle", 1);

	#混乱開始処理を呼ぶために混乱前年度に年度を変更しゲームレベルを変更して、3の国のプレイヤーに勝利させて統一させる
	#念のため統一熟練も調べる
	$wc->access_data("year", 39);
	$wc->access_data("game_lv", 1);
	$wc->access_data("reset_time", 0);
	my $old_tou_c = $pc->access_data("s1c3m", "tou_c");
	$warc->action_set_war("s1c3m",1);
	$pc->access_data("s1c3m", "wt", 0);
	$warc->action_encount("s1c3m");
	$warc->action_win_war("s1c3m");
	$warc->action_after_war("s1c3m", 1);
	my $new_tou_c = $pc->access_data("s1c3m", "tou_c");
	($new_tou_c eq ($old_tou_c + 1)) or die "tou_c didn't change";

	######################混乱開始直後の状況をチェックする
	#君主は解任されているか
	for my $i (1 .. 6){
		($cc->access_data(1, "ceo") eq "") or die "ceo exists in country $i\n";
	}

	#投票は解除されているか
	for my $player ($Situation1::situation1_players){
		($pc->access_data($player->{name}, "vote") eq "") or die "$player->{name}'s vote is not void\n";
	}

	#シャッフル禁止プレイヤーは元の国にいるか
	($pc->access_data("s1c4m", "country") eq 4) or die "s1c4m moved\n";
	($pc->access_data("s1c4f", "country") eq 4) or die "s1c4f moved\n";

	#投獄されたプレイヤーは復帰しているか
	($pc->access_data("s1c2m", "lib") eq "") or die "s1c2m is still in prison";

	#この後混乱中に君主を建ててから統一するなどして混乱後の君主投票状況をチェックする
	#サンプルとしては冗長なのでこれでテスト終了とする

}
1;
