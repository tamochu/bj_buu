package TestAccessor;
require "./TestFramework/Controller/ControllerConst.pm";
require $ControllerConst::item_accessor;
require $ControllerConst::country_accessor;
require $ControllerConst::world_accessor;
require $ControllerConst::player_accessor;
	
my $username_prefix = "test";
my $username_sufix = 2;
my $username = $username_prefix.$username_sufix;
my $passward = "test4a";
my $first_country = 1;
my $second_country = 2;
my ($pa, $ca, $wa, $ia);

#&setup;
#&test_128();
#&test_129();
#&test_177();
#&test_128_177();
#&run;

sub setup{

	$pa = PlayerAccessor->new();
	$ca = CountryAccessor->new();
	$wa = WorldAccessor->new();

	$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	$ca->access_data($first_country, "capacity", 25);
	print $pa->shikan_player($username, $first_country);
}

sub run{

	$ia = ItemAccessor->new();
	my $new_wepon = [1, 1, 15, 4];
	my $new_egg = [2, 10, 10, 0];
	my $new_pet = [3, 61, 1, 0];
	my $new_gar = [4, 1, 0, 0];

	$ia->give_item($username, $new_wepon->[0], $new_wepon->[1], $new_wepon->[2], $new_wepon->[3]);
	$ia->give_item($username, $new_egg->[0], $new_egg->[1], $new_egg->[2], $new_egg->[3]);
	$ia->give_item($username, $new_pet->[0], $new_pet->[1], $new_pet->[2], $new_pet->[3]);
	$ia->give_item($username, $new_gar->[0], $new_gar->[1], $new_gar->[2], $new_gar->[3]);

	my $wep_index = $ia->get_item_index($username, $new_wepon->[0], $new_wepon->[1], $new_wepon->[2], $new_wepon->[3]);
	my $egg_index = $ia->get_item_index($username, $new_egg->[0], $new_egg->[1], $new_egg->[2], $new_egg->[3]);
	my $pet_index = $ia->get_item_index($username, $new_pet->[0], $new_pet->[1], $new_pet->[2], $new_pet->[3]);
	my $gar_index = $ia->get_item_index($username, $new_gar->[0], $new_gar->[1], $new_gar->[2], $new_gar->[3]);

	die("index does not match : expected 0: actual $wep_index") if($wep_index ne 0);
	die("index does not match : expected 1: actual $egg_index") if($egg_index ne 1);
	die("index does not match : expected 2: actual $pet_index") if($pet_index ne 2);
	die("index does not match : expected 3: actual $gar_index") if($gar_index ne 3);

	$ia->action_draw_item($username, 0);
	$ia->action_draw_item($username, 0);
	$ia->action_draw_item($username, 0);
	$ia->action_draw_item($username, 0);
	$ia->action_draw_item($username, $pet_index);
	
	unless( ($pa->access_data($username, "wea") eq $new_wepon->[1])
		and ($pa->access_data($username, "wea_c") eq $new_wepon->[2])
		and ($pa->access_data($username, "wea_lv") eq $new_wepon->[3])
		and ($pa->access_data($username, "egg") eq $new_egg->[1])
		and ($pa->access_data($username, "egg_c") eq $new_egg->[2])
		and ($pa->access_data($username, "pet") eq $new_pet->[1])
		and ($pa->access_data($username, "pet_c") eq $new_pet->[2])
		and ($pa->access_data($username, "gua") eq $new_gar->[1])){
	
		die("action_draw_item didn't work properly");
	}

	#ｱﾏﾂﾐ使用
	my $pet_effect = $ia->use_pet($username);
	die("use_pet didn't work : pet_effect expected 0 : acutual $pet_effect") if ($pet_effect ne 0);

	print "***test_ia end***\n\n";

}

sub test_128{

	$ia = ItemAccessor->new();
	my $pet = [3, 128, 0, 0];
	$ia->give_item($username, $pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	my $index = $ia->get_item_index($username,
		$pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	$ia->action_draw_item($username, $index);
	my $pet_effect = $ia->use_pet($username);
	$ia->enact_pet($username, "monster_name", "winyeah", "lose");
}

sub test_129{

	$ia = ItemAccessor->new();
	my $pet = [3, 129, 0, 0];
	$ia->give_item($username, $pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	my $index = $ia->get_item_index($username,
		$pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	$ia->action_draw_item($username, $index);
	my $pet_effect = $ia->use_pet($username);
	$ia->enact_pet($username, "monster129", "winyeah", "lose");
}

sub test_177{

	$ia = ItemAccessor->new();
	my $pet = [3, 177, 0, 0];
	$ia->give_item($username, $pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	my $index = $ia->get_item_index($username,
		$pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	$ia->action_draw_item($username, $index);
	my $pet_effect = $ia->use_pet($username);
	$ia->enact_pet($username, $second_country);
}

sub test_128_177{

	$ia = ItemAccessor->new();
	my $pet = [3, 128, 0, 0];
	$ia->give_item($username, $pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	my $index = $ia->get_item_index($username,
		$pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	$ia->action_draw_item($username, $index);
	my $pet_effect = $ia->use_pet($username);
	$ia->enact_pet($username, "monster128177", "winyeah", "lose");

	#直後に二つ目のペット使用
	my $pet = [3, 177, 0, 0];
	$ia->give_item($username, $pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	my $index = $ia->get_item_index($username,
		$pet->[0], $pet->[1], $pet->[2], $pet->[3]);
	$ia->action_draw_item($username, $index);
	my $pet_effect = $ia->use_pet($username);
	$ia->enact_pet($username, $second_country);

}

1;
