#サンプルそのいち
#_war_result.cgiを変更したという仮定で、平和で統一される様子をテストする

#まず必要なコントローラーをrequireして生成する
#コントローラーは独立したクラスなので、必要ないものはrequireしたり生成する必要はない
use lib qw(./TestFramework/Controller/);
#プレイヤーの作成や士官に使う
require PlayerController;
#年度や統一難易度の変更確認などに使う
require WorldController;
#国の国力などの変更確認に使う
require CountryController;
#戦争に使う
require WarController;
my $wc = WorldController->new();
my $cc = CountryController->new();
my $warc = WarController->new();
my $pc = PlayerController->new();

#今現在の国の状態が分からないので、テストの独立性を高めるためadmin_countryの機能で国を作り直す
#全てのデータはテスト後に（設定されてれば）復元される
#接頭辞がadmin_の関数はadmin.cgiを経由している
#admin_reset_countriesは引数を与えて国の数、年度、情勢などを設定できるが最初の説明なので
#空の引数でデフォルト（６カ国、１年目、平和）にする
print "***before reset contries***\n";
#$cc->admin_reset_countries();
print "***after  reset contries***\n";

#プレイヤーキャラを新しく登録させる
#引数は名前・パス・性別・IPアドレス
#ＩＰアドレスは省略すると内部でカウントした重複しないものを当てる。
print "***before create player***\n";
my $player_name = "korutopi";
my $pass	= "toilet";
$pc->create_player($player_name, $pass, 1);
print "***after create player***\n";

#重複したプレイヤー名、重複したIP、その他の原因でキャラが作れないときは例外を返す
#コントローラーの関数はその動作が失敗した時は内部でチェックをして例外を返す
#例外はテストを呼び出すTestInterfaceでキャッチされるが、失敗するかをチェックしたい時は自分でキャプチャーする
eval{
	#名前が重複している
	$pc->create_player($player_name, $pass, 1);
};
unless($@){
	#例外が投げられていなければ何かがおかしい
	#改めて例外をスローする
	#テストの例外は外側でキャッチされ、テスト結果の配列に追加される。
	die "pc->create_player should fail";
}

#プレイヤーキャラはネバランにいるので士官させる
#その前に、念のため国の士官上限を確保する
#まずは国の数を取得する
my $num_country = $wc->access_data("country");
#コントローラーのいくつかはaccess_dataという関数を持つ
#いずれもデータ（user.cgiやcountries.cgiなど）に直接アクセスして読み書きする
#今回はcountries.cgiにアクセスし、countryの値を取得した
#$wc->access_data("country", 10)のように数値を引数で渡すと書き換える
for my $i (1 .. $num_country){
	#CountryControllerのaccess_dataは国のindex, 属性名でcountries.cgiのデータにアクセスする
	#それぞれの国の士官上限を３０に書き換えておく
	$cc->access_data($i, "capacity", 30);
	#ついでに物資も再設定しとく
	$cc->access_data($i, "food", 100000);		
	$cc->access_data($i, "money", 100000);		
	$cc->access_data($i, "soldier", 100000);		
}
#国番号１の国に士官させる
$pc->action_shikan($player_name,1);

#2の国に少数で戦争に出てみる
#接頭辞がactionなのでプレイヤーの操作（戦争を選び、進軍規模を選び、相手国を選び出発する）を再現している
#デモのため失敗するはずのケースをいくつか見てみる
eval{
	#大規模で出る
	$warc->action_set_war($player_name, 2, WarController::LARGE);
};
unless($@){
	#新規登録したばかりのキャラは階級が足りない
	die "set_war should fail";
}

eval{
	$warc->action_set_war($player_name, 2, WarController::SMALL);
};
unless($@){
	#国を作り直したばかりで終戦期間のため失敗する
	die "set_war should fail";
}

#終戦期間を終わらせる
$wc->access_data("reset_time", 0);

#実際に出る
$wc->action_set_war($player_name, 2, WarController::SMALL);

#着弾する
#着弾ケースの失敗例を書くと多分戦争に出るところからやり直しになるので普通に成功させる
#action_encountをaction_set_warで出陣する前に呼べば当然例外をスローするし、拘束中でもスローする
#そのまえに拘束時間を０にする
$pc->access_data($player_name, "wt", 0);
$warc->action_encount($player_name);

#着弾中に他のaction_*の関数を呼べば例外を吐く（$m{lib}がwarだから)
#一回の戦闘では決着しないはずという前提で一回戦闘を行う。じゃんけんは固定
$warc->action_step_war($player_name);

#決着がつくまで戦闘を行う
#レンタル鯖で無限ループは怖いのでループ時は必ずカウンタを回すことを推奨
my $count = 0;
while(1){

	if($count > 50){
		die ("failed to finish war");
	}

	#他の方法もあるが今回はプレイヤーの勝利数、分け数、敗北数の和を比較して終了条件とする
	my $sum_c = $pc->access_data($player_name, "win_c")
	           +$pc->access_data($player_name, "lose_c")
	           +$pc->access_data($player_name, "draw_c");


	
	$warc->action_step_war($player_name);

	my $new_sum_c = $pc->access_data($player_name, "win_c")
	           +$pc->access_data($player_name, "lose_c")
	           +$pc->access_data($player_name, "draw_c");

	if($new_sum_c > $sum_c){
		last;
	}
	$count++;

}

#決着がつくまで戦闘を繰り返す関数もある
#戻り値で勝敗結果が返ってくるがここでは使わない
$warc->action_set_war($player_name, 3, WarController::SMALL);
$pc->access_data($player_name, "wt", 0);
$warc->action_encount($player_name);
$warc->action_complete_war($player_name);

#長くなるので他の機能はまたにしてテストを終了させる
#統一難易度をLv1まで下げて戦争に勝利し、年度が進めばテスト成功とする
#デモなので簡単な成功条件としているが、本来はもっとチェックしたほうが良い（あとでそういうヘルパー書く。多分）
my $last_year = $wc->access_data("year");
$wc->access_data("game_lv", 1);
$warc->action_set_war($player_name, 2, WarController::SMALL);
$pc->access_data($player_name, "wt", 0);
#戦闘中の兵数m{sol}とy{sol}を10000と0に書き換えて勝つ関数
#接頭辞actionなので戦闘自体はちゃんと行い勝利し、統一時の処理が行われる
$wac->action_win_war($player_name);
my $current_year = $wc->access_data("year");
unless($current_year > $last_year){
	die "no change in year";
}

#そのまま抜ければ成功テスト
#最後の１を忘れずに
1;
