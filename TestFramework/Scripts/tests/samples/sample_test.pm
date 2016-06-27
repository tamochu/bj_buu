#サンプルそのいち
#平和情勢で統一する様子をシミュレートする
package sample_test;

#テスト本体は必ずサブルーティンrunの中に書くこと
&run;

sub run{

	#コントローラーなどの定数
	use TestFramework::Controller::ControllerConst;

	#テストはコントローラーを操作することで行う
	#まず必要なコントローラーのインスタンスを生成する
	#国の作成や削除、おまかせ国データ作成などを行うCountryControllerを生成する
	require "./TestFramework/Controller/CountryController.cgi";
	my $cc = CountryController->new();
	
	#おまかせ国データ作成で国をリセットする
	#引数にパラメータを与えることも出来るが今回は引数なしのデフォルト（６カ国一年目平和）
	#関数の接頭辞にadminが付いている時はadmin.cgi経由の操作を表す
	$cc->admin_reset_countries();
	
	#次にプレイヤーを作成する
	#PlayerControllerはプレイヤーの作成や削除、士官等を行う
	require "./TestFramework/Controller/PlayerController.cgi";
	my $pc = PlayerController->new();
	my $player_name = "test2";
	my $player_passward = "test1a";
	$pc->create_player($player_name, $player_passward, 1);
	
	#士官させる前に、念のため士官上限を引き上げておく
	#いくつかのコントローラはaccess_dataという関数を持ち、それぞれデータの値を読み書きする
	#CountryControllerの場合、countries.cgiの最初の引数で指定された国のデータにアクセスしている
	#三つ目の引数が空なら読み込み、指定されていれば書き込む
	$cc->access_data(1, "capacity", 30);
	
	#士官させる
	#接頭辞がactionの関数はプレイヤーの操作をシミュレートしている
	#action_shikan_playerの場合、国情報→士官→国選択→はい、の流れを再現している
	$pc->action_shikan_player($player_name, 1);
	
	#戦争に出てみる
	#今はおまかせ国データ作成を呼んだ直後なので終戦期間のはず
	#当然戦争に出る関数を呼べば例外をスローするので、まず終戦期間を終わらせる
	#システムの時刻を偽装して時間を進める方法もあるが、テストの目的ではないため今回は直接reset_timeを書き換える
	require "./TestFramework/Controller/WorldController.cgi";
	my $wc = WorldController->new();
	$wc->access_data("reset_time", 0);

	
	#国2を相手に少数で戦争に出る
	#物資が足りないと戦争に出られず例外になるので、念のため物資を足しておく
	#内政をして時間を進める方法もあるが今回は直接書き換える
	$cc->access_data("food", 100000);
	$cc->access_data("money", 100000);
	$cc->access_data("soldier", 100000);

	#戦争に出る
	#戦争はWarControllerから操作する
	#接頭辞がactionなのでメニューから戦争→規模選択→相手国選択→出発を再現している
	require "./TestFramework/Controller/WarController.cgi";
	my $warc = WarController->new();
	$warc->action_set_war($player_name, 2, ControllerConst::WAR_SMALL);
	
	#作成したばかりのキャラなので勝利数的に少数しか出られない
	#長期で出れば失敗する
	#$warc->set_war($player_name, 2, ControllerConst::WAR_LARGE);
	
	#着弾する前に待機時間を処理する
	#システムの時間を偽装する方法もあるが今回はm{wt}を書き換える
	$pc->access_data($player_name, "wt", 0);
	$warc->action_encount($player_name);

	#一回戦闘する
	#じゃんけんは固定
	$warc->action_step_war($player_name);

	#決着がつくまで戦闘する
	$warc->action_complete_war($player_name);

	#テストの終了条件である、平和で統一がちゃんと行われるかをテストする
	#統一Lvを１に下げて戦争に勝利し、年度が進むことを確認して条件達成とする
	$wc->access_data("game_lv", 1);
	my $last_year = $wc->access_data("year");

	#戦争に出る
	$warc->action_set_war($player_name, 2, ControllerConst::WAR_SMALL);
	$pc->access_data($player_name, "wt", 0);
	$warc->action_encount($player_name);
	#action_win_warは対戦相手の兵力を０に、自分の兵力を10000にして戦闘を行い勝利する
	$warc->action_win_war($player_name);

	#統一処理がされたはずなので年度が進んでいるはず
	#このチェックは本来もっと色々なデータに関して厳密に行った方がバグを発見しやすい（後でヘルパー書く）
	my $current_year = $wc->access_data("year");
	unless($current_year eq ($last_year+1)){
		#テストが失敗したことはdieで例外を投げて知らせる
		#テストの失敗個所として出力されるので何が失敗したか分かりやすく書いたほうがいい
		die "something wrong: \$current_year is expected ", $last_year+1, "actual $current_year";
	}

	#テストの後の後処理があればここで書いても良い
	#特に無ければテスト終了
}

#テストはrequireで読み込まれるので、1も忘れずに
1;
	
	
	
