package test_item_controller;
require "./TestFramework/Controller/ControllerConst.pm";
require $ControllerConst::item_controller;
require $ControllerConst::country_controller;
require $ControllerConst::world_controller;
require $ControllerConst::player_controller;
	
my $username_prefix = "test";
my $username_sufix = 2;
my $username = $username_prefix.$username_sufix;
my $username2= $username_prefix.($username_sufix + 20);
my $passward = "test4a";
my $first_country = 1;
my $second_country = 2;
my $pc = PlayerController->new();
my $cc = CountryController->new();
my $ic = ItemController->new();
my $wc = WorldController->new();

&setup;
#&run;

sub setup{
	
	#$cc->admin_reset_countries();
	$pc->create_player($username, $passward, 1);
	$pc->create_player($username2, $passward, 2);
	$cc->access_data($first_country, "capacity", 30);
	$cc->access_data($second_country, "capacity", 30);
	$wc->access_data("reset_time", 0);
	$pc->action_shikan_player($username, $first_country);
	$pc->action_shikan_player($username2, $second_country);
	
}

sub run{
	
	my $losstime= {type=>3, no=>152, c=>0, lv=>0};
	$ic->give_item($username, $losstime);

	#消費ペットの代表としてロスタイムを使用
	print STDERR "*** use losstime ***\n";
	my $last_limit = $wc->access_data("limit_time");
	my $index = $ic->get_item_index($username, $losstime);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);

	#ﾛｽﾀｲﾑ使用成功
	my $current_limit= $wc->access_data("limit_time");
	($current_limit gt $last_limit) or die "loss time didn't work\n";
	($pc->access_data($username, "pet") eq 0) or die "losstime should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} should be void\n";

	#以下action_step_petを網羅
	
	#128-130
	open (MH, "< ./log/monster/beginner.cgi") or die "failed to open beginner.cgi";
	my $monster_count = 0;
	while (my $line = <MH>){
		$monster_count++;
	}
	close MH;

	my $pet = {type=>3, no=>128, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, "pet128", "win128", "lose128");

	open (MH, "< ./log/monster/beginner.cgi") or die "failed to open beginner.cgi";
	my $new_monster_count = 0;
	while (my $line = <MH>){
		$new_monster_count++;
	}
	close MH;

	($new_monster_count eq ($monster_count + 1)) or die "monster was not be added";
	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ", $pc->access_data($username, "lib");

	#175
=pod
	$pet = {type=>3, no=>175, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, "pet128", "win128", "lose128");

	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");
=cut

	#176
	$pet = {type=>3, no=>176, c=>0, lv=>0};
	$pc->access_data($username2, "shogo", "test");
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, $username2); 
	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");
	$pc->access_data($username2, "shogo", "test");
	$pc->access_data($username2, "shogo_t", "");

	#177
	$pet = {type=>3, no=>177, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, $second_country); 
	($pc->access_data($username, "lib") eq "prison") or die "m{lib} is\nexpected : prison\nactual : ",$pc->access_data($username, "lib");
	$pc->refresh_player($username);

	#185
	my $money = $pc->access_data($username2, "money");
	$pet = {type=>3, no=>185, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, $username2); 
	my $new_money = $pc->access_data($username2, "money");
	($new_money ne $money) or die "money didn't change\n";
	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");

	#186
	
	#188
	
	#189
	
	#190
	my $ariyosi = {type=>3, no=>190, c=>0, lv=>0};
	$ic->give_item($username, $ariyosi);
	$index = $ic->get_item_index($username, $ariyosi);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, $username2, "test_shogo");
	my $new_shogo = $pc->access_data($username2, "shogo");
	($new_shogo eq "test_shogo") or die "$username2's shogo is \nexpected : test_shogo\nactual : $new_shogo\n";
	($pc->access_data($username, "pet") eq 0) or die "ariyosi should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");

	#191
	$pet = {type=>3, no=>191, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, "newwea", 1); 
	($pc->access_data($username, "wea_name") eq "newwea") or die "new weapon wasn't created\n";
	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");


	#198
	$pet = {type=>3, no=>198, c=>0, lv=>0};
	$ic->give_item($username, $pet);
	$index = $ic->get_item_index($username, $pet);
	$ic->action_draw_item($username, $index);
	$ic->action_use_pet($username);
	$ic->action_step_pet($username, $username2, "ttail"); 
	($pc->access_data($username2, "silent_tail") eq "ttail") or die "tail wasn't added";
	($pc->access_data($username, "pet") eq 0) or die "pet should have been used";
	($pc->access_data($username, "lib") eq "") or die "m{lib} is\nexpected : \"\"\nactual : ",$pc->access_data($username, "lib");

	#201

}
1;
