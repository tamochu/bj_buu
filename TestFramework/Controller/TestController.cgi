#コントローラーのテスト

package TestController;
use lib qw(./TestFramework/lib);
use Test::MockTime qw( :all );
use File::Path;
use feature 'say';
use lib qw(./TestFramework/Controller/);
require SystemController;
require WarController;
require PlayerController;
require WorldController;
require CountryController;


#時刻の誤差
my $time_margin = 1;

#国と人
my $username_first_part = "test";
my $username_sufix = 12; 
my $username_sufix2 = $username_sufix + 2;
my $username_sufix3 = $username_sufix + 4;
my $username = $username_first_part.$username_sufix;
my $username2 = $username_first_part.$username_sufix2;
my $user_id = unpack ('H*', $username);
my $user_id2 = unpack ('H*', $username2);
my $passward = "test4a";
my $first_country = 2;
my $second_country = 3;
my $third_country;
my $added_country_name = "test_country";

###############
#テスト切り替え
###############

#test_sc();
test_pc();
#test_cc();
#test_wac();
#test_wc();
#taihi();

sub taihi{
	my $cc = CountryController->new();
	$cc->access_data($first_country, "capacity", 30);
}

#WarControllerテスト
sub test_wac{

	my $wc = WorldController->new();
	my $pc = PlayerController->new();
	my $cc = CountryController->new();
	my $wac = WarController->new();

	$pc->create_player($username, $passward,1);
	$pc->access_data($username, "money", 4000000);
	$cc->access_data($first_country, "capacity", 30);
	$pc->action_shikan_player($username, $first_country);
	$pc->access_data($username, "renzoku_c", 0);
	$pc->access_data($username, "act", 0);
	$wc->access_data("reset_time", 0);
	$cc->access_data($first_country, "food", 100000);
	$cc->access_data($first_country, "money", 100000);
	$cc->access_data($first_country, "soldier", 100000);

	#小規模戦争進軍成功
	$wac->action_set_war($username, $second_country, 1);

	#戦闘成功
	$pc->access_data($username, "wt", 0);
	$wac->action_encount($username);
	$wac->action_complete_war($username);

	#戦争の勝利成功
	$pc->access_data($username, "renzoku_c", 0);
	$pc->access_data($username, "act", 0);
	$wac->action_set_war($username, $second_country, 1);
	$pc->access_data($username, "wt", 0);
	$wac->action_encount($username);
	$wac->action_win_war($username);

	#戦争の敗北成功
	$pc->access_data($username, "renzoku_c", 0);
	$pc->access_data($username, "act", 0);
	$wac->action_set_war($username, $second_country, 1);
	$pc->access_data($username, "wt", 0);
	$wac->action_encount($username);
	$wac->action_lose_war($username);

	#ターン切れドロー成功
	$pc->access_data($username, "renzoku_c", 0);
	$pc->access_data($username, "act", 0);
	$wac->action_set_war($username, $second_country, 1);
	$pc->access_data($username, "wt", 0);
	$wac->action_encount($username);
	$wac->action_draw_war_turn($username);
	
	#両軍壊滅ドロー成功
	$pc->access_data($username, "renzoku_c", 0);
	$pc->access_data($username, "act", 0);
	$wac->action_set_war($username, $second_country, 1);
	$pc->access_data($username, "wt", 0);
	$wac->action_encount($username);
	$wac->action_draw_war_kaimetu($username);

	#進軍失敗
	#長期戦争には階級が足りない
	eval{
		$wac->action_set_war($username, $second_country, WarController::LARGE);
	};
	unless($@){
		die("test_wc action_set_war fail : beyond position");
	}

	#進軍失敗
	#物資が足りない
	eval{
		$cc->access_data($first_country, "food", 0);
		$wac->action_set_war($username, $second_country, WarController::SMALL);
	};
	unless($@){
		die("test_wc action_set_war fail : suply shortage");
	}


	#進軍失敗
	#同盟国である
	
	#着弾失敗
	#戦争に出ていない
	eval{
		$wac->action_encount($username);
	};
	unless($@){
		die("test_wc action_encount fail : encount before departure");
	}


	
}

#PlayerControllerテスト
sub test_pc{

	my $pc = PlayerController->new();
	my $cc = CountryController->new();
	my $wc = WorldController->new();
	
	############################
	#プレイヤー生成成功テスト
	############################
	print "***test_pc p1***\n";
	eval{
		print "***test_pc p1-1***\n";
		$pc->create_player($username, $passward,1, "1.1.1.$username_sufix");
		print "***test_pc p1-2***\n";
		$pc->create_player($username2, $passward,1);
	};
	if($@){
		die("test_pc create_player success test\n", $@);
	}

	############################
	#プレイヤー生成失敗テスト
	############################
	eval{
		#不十分な引数
		print "***test_pc p2***\n";
		$pa->create_player("name", "pass");
	};
	unless($@){
		die("test_pc create_player fail test : invalid arguments");
	}

	eval{
		#同じプレイヤー名
		print "***test_pc p3***\n";
		$pc->create_player($username, $passward,1, "1.1.1.$username_sufix3");
	};
	unless($@){
		die("test_pc create_player fail test : same name player exists"); 
	}

	eval{
		#重複IP
		print "***test_pc p4***\n";
		$pc->create_player($username."a", $passward,1, "1.1.1.$username_sufix");
	};
	unless($@){
		die("test_pc create_player fail test : same ip"); 
	}

	############################
	#士官　成功
	############################

	print "***test_pc p4***\n";
	eval{
		#国番号１に士官
		print "***test_pc p4-1***\n";
		$pc->access_data($username, "money", 1000000);
		$wc->access_data($first_country, "capacity", 30);
		$pc->action_shikan_player($username, $first_country);

		#ネバランに士官
		print "***test_pc p4-2***\n";
		$pc->access_data($username, "wt", 0);
		$pc->action_shikan_player($username, $first_country);

		#国番号２に士官
		print "***test_pc p4-3***\n";
		$pc->access_data($username, "wt", 0);
		$wc->access_data($second_country, "capacity", 30);
		$pc->action_shikan_player($username, $second_country);

		#国番号２から国番号１に士官
		print "***test_pc p4-4***\n";
		$pc->access_data($username, "wt", 0);
		$wc->access_data($first_country, "capacity", 30);
		$pc->action_shikan_player($username, $first_country);

	};
	if($@){
		die("test_pc action_shikan_player success test", $@);
	}
	
	############################
	#プレイヤー士官失敗テスト
	############################
	eval{
		#拘束中に士官
		print "***test_pc p5***\n";
		$pa->access_data($username2, "wt", 100);
		$pa->action_shikan_player($username2, $second_country);
	};
	unless($@){
		die("test_pc create_player fail test : is bound");
	}
	$pa->access_data($username2, "wt", 0);
	$pa->access_data($username2, "tp", 0);
	$pa->access_data($username2, "turn", 0);
	$pa->access_data($username2, "lib", "");

	eval{
		#lib処理中に士官
		print "***test_pc p6***\n";
		$pa->access_data($username2, "wt", 0);
		$pa->access_data($username2, "lib", "yay");
		$pa->action_shikan_player($username2, $second_country);
	};
	unless($@){
		die("test_pc create_player fail test : is processing another lib");
	}
	$pa->access_data($username2, "wt", 0);
	$pa->access_data($username2, "tp", 0);
	$pa->access_data($username2, "turn", 0);
	$pa->access_data($username2, "lib", "");

	eval{
		#存在しない国に士官
		print "***test_pc p7***\n";
		$pa->access_data($username2, "wt", 0);
		my $num_country = $wa->access_data("country");
		$pa->action_shikan_player($username2, $num_country+1);
	};
	unless($@){
		die("test_pc create_player fail test : invalid country number");
	}
	$pa->access_data($username2, "wt", 0);
	$pa->access_data($username2, "tp", 0);
	$pa->access_data($username2, "turn", 0);
	$pa->access_data($username2, "lib", "");

	eval{
		#お金が足りない
		print "***test_pc p8***\n";
		$pa->access_data($username2, "wt", 0);
		$pa->access_data($username2, "money", 0);
		$pa->action_shikan_player($username2, $num_country+1);
	};
	unless($@){
		die("test_pc create_player fail test : no money");
	}
	$pa->access_data($username2, "wt", 0);
	$pa->access_data($username2, "tp", 0);
	$pa->access_data($username2, "turn", 0);
	$pa->access_data($username2, "lib", "");

	############################
	#プレイヤー削除成功テスト
	############################
	eval{
		print "***test_pc p9***\n";
		$pa->remove_player($username2);
	};
	if($@){
		die("test_pc remove_player success test", $@);
	}

	############################
	#プレイヤー削除失敗テスト
	############################
	eval{
		#存在しないプレイヤー
		print "***test_pc p10***\n";
		$pa->remove_player("invalid_name");
	};
	unless($@){
		die("test_pc create_player fail test : invalid name");
	}

	#後片付け
	$pa->remove_player($username);

}


#WorldControllerテスト
sub test_wc{

	my $wc = WorldController->new();
	my $cc = CountryController->new();

	#年度変更テスト
	my $old_year = $wc->access_data("year");
	say "***in test_wc old_year = $old_year***";
	$wc->access_data("year", $old_year+1);
	my $new_year = $wc->access_data("year");
	say "***in test_wc new_year= $new_year***";
	if($new_year ne ($old_year+1)){
		die("test_wc access success test");
	}

	#災害発生テスト
	#状態の和と物資の和
	my $sum_state = 0;
	my $sum_suply = 0;
	for my $i (1 .. $wc->access_data("country")){
		$sum_state += $cc->access_data($i, "state");
		$sum_suply += $cc->access_data($i, "food");
		$sum_suply += $cc->access_data($i, "money");
		$sum_suply += $cc->access_data($i, "soldier");
	}

	$wc->evoke_disaster();

	my $new_sum_state = 0;
	my $new_sum_suply = 0;
	for my $i (1 .. $wc->access_data("country")){
		$new_sum_state += $cc->access_data($i, "state");
		$new_sum_suply += $cc->access_data($i, "food");
		$new_sum_suply += $cc->access_data($i, "money");
		$new_sum_suply += $cc->access_data($i, "soldier");
	}

	if(($sum_state eq $new_sum_state) and ($sum_suply eq $new_sum_suply)){
		die("test_wc evoke_disaster success: $sum_state, $new_sum_state, $sum_suply, $new_sum_suply");
	}

}

#CountryControllerテスト
sub test_cc{
	my $cc = CountryController->new();
	my $wc = WorldController->new();

	#おまかせ国データ作成でﾘｾｯﾄ
	my $setting = { country => 3 };
	$cc->admin_reset_countries($setting);
	my $num_country = $wc->access_data("country");
	if($num_country ne 3){
		die ("test_cc admin_reset_countries success\n\$num_country expected : 3, actual : $num_country \n");
	}

	#国追加成功
	$cc->admin_add_country();
	print "***in TC w{country} = ",$wc->access_data("country"), "***\n";
	if($wc->access_data("country") ne 4){
		die ("test_cc admin_add_country success\n");
	}

	
}


#SystemControllerテスト
sub test_sc{


	my $sc = SystemController->new();
	#時刻偽装のテスト
	my $current_time = 0;
	my $margined_time = undef;

	$sc->set_time(0);
	$current_time = time;
	$margined_time = 0 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt 0)){
		die("set_time test : current_time expected 0 <= ct <= $margined_time: actual $current_time");
	}

	$sc->set_time(0);
	$sc->advance_time(10);
	$current_time = time;
	$margined_time = 10 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt 10)){
		die("set_time advance_time test : current_time  expected 10 <= ct <= $margined_time: actual $current_time");
	}	
	
	$sc->fix_time(0);
	sleep 1;
	$current_time = time;
	if($current_time ne 0){
		die("fix_time : current_time expected 0 : actual $current_time");
	}


	$sc->advance_time(10);
	sleep 1;
	$current_time = time;
	if($current_time ne 10){
		die("fix_time advance : current_time expected 10 : actual $current_time");
	}


	$sc->restore_time();
	my $natural_time = time;
	$sc->advance_time(10);
	$current_time = time;
	$margined_time = $natural_time + 10 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt ($natural_time + 10))){
		die("fix_time advance : current_time expected $natural_time+10 <= $margined_time : actual $current_time");
	}


}

1;
