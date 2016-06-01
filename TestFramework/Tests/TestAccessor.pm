#アクセッサーの単体テスト

package TestCUI;

use feature 'say';
use lib qw(./TestFramework/Adapter/Accessor);
require "CountryAccessor.pm";
require "WorldAccessor.pm";
require "WarAccessor.pm";
require "PlayerAccessor.pm";

my $username_first_part = "test";
my $username_sufix = "3";
my $username = $username_first_part.$username_sufix;
my $user_id = unpack ('H*', $username);
my $passward = "test4a";
my $first_country = 1;
my $second_country = 2;
my $added_country_name = "test_country";

#test_ca();
test_pa();
#test_wa();
#test_wara();

#PlayerAccessorテスト
sub test_pa{
	
	print "***test_pa::start***\n\n";
	my $testname = "test_pa;:";


	
	my $pa = PlayerAccessor->new();
	my $ca = CountryAccessor->new();

	#$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");

	($ca->access_data($first_country, "capacity", 35) eq 35) ? _print_ok($testname."p1") : _print_error($testname."p1");

	($ca->access_data($second_country, "capacity", 25) eq 25) ? _print_ok($testname."p2") : _print_error($testname."p2");

	$pa->shikan_player($username, $first_country) ;
	($pa->access_data($username, "country") eq $first_country) ? _print_ok($testname."p3") : _print_error($testname."p3");

	$pa->shikan_player($username, $second_country) ;
	($pa->access_data($username, "country") eq $second_country) ? _print_ok($testname."p4") : _print_error($testname."p4");


	$pa->remove_player($username);
	(-d "./user/$user_id") ? _print_ok($testname."p5") : _print_error($testname."p5");


	print "\n***test_pa::end***\n\n";
}

#CountryAccessorテスト
sub test_ca{

	print "***test_ca::start***\n\n";
	my $ca = CountryAccessor->new();

	#access_data
	say "*** access_data test ***";
	say "capacity of country 1 = ", $ca->access_data(1, "capacity") ;
	say "set 35 to capacity of country 1 = ", $ca->access_data(1, "capacity", 35);
	say "capacity of country 1 = ", $ca->access_data(1, "capacity");

	#add_country
	say "*** add_country test***";
	say "num_country = ", $ca->get_num_country();
	my $added_country = $ca->add_country($added_country_name, "#000FFF");
	say "num_country = ", $ca->get_num_country();

	#remove_country 
	#say "*** remove_country test***";
	#$ca->remove_country($added_country);
	#say "num_country = ", $ca->get_num_country();
	print "\n***test_ca::end***\n\n";
}

#WorldAccesorテスト
sub test_wa{

	print "***test_wa::start***\n\n";
	my $wa = WorldAccessor->new();

	#国の数
	my $year = $wa->access_data("country", 6);
	my $year = $wa->access_data("year");
	say "year = ", $year; 
	$wa->access_data("year", 13);	
	say "year = ", $wa->access_data("year");
	$wa->access_data("year", 15);	
	
	#災害起こす
	#$wa->evoke_disaster();
	#$wa->evoke_disaster(1);
	print "***test_wa::end***\n\n";
}

#WarAccessorテスト
sub test_wara{

	print "***test_wara::start***\n\n";
	my $testname = "test_pa::";
	my $error_mes = "";
	my $pa = PlayerAccessor->new();
	my $wara = WarAccessor->new();
	my $ca = CountryAccessor->new();
	my $wa = WorldAccessor->new();

	#$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	$ca->access_data($first_country, "capacity", 25);
	#print $pa->shikan_player($username, $first_country);

	
	#set_war success
	print "*****enter set_war success*********\n";
	$wa->access_data("reset_time", "zero");
	$wara->set_war($username, $second_country,1);
	($pa->access_data($username, "lib") eq "war") ? _print_ok($testname."set_war success test : ".$mes) : _print_error($testname."set_war success test : ".$mes);


	#set_war fail
	#期待：既に直前にset_warしているから失敗
	print "*****enter set_war fail*********\n";
	eval{
		$wara->set_war($username, $second_country, 1);
	};
	if($@){
		_print_ok($testname."set_war fail test : ". $@);
	}
	else{
		_print_error($testname."set_war fail test");

	}
	
	#encount fail
	#期待：拘束中のはず
	print "*****enter encount fail*********\n";
	eval{
			$wara->encount($username);
	};
	if($@){
		_print_ok($testname."encount fail test".$@);
	}
	else{
		_print_error($testname."encount fail test");
	}

	
	#encount success
	$pa->access_data($username, "wt", 0);
	$mes = $wara->encount($username);
	($pa->access_data($username, "lib") eq "war") ? 
		_print_ok($testname."encount success test") : _print_error($testname."encount success test".$mes);

	#finish_war success
	my $sum_c_1 = $pa->access_data($username, "lose_c") 
		  + $pa->access_data($username, "win_c")
		  + $pa->access_data($username, "draw_c");
	$mes = $wara->finish_war($username);
	my $sum_c_2 = $pa->access_data($username, "lose_c") 
		  + $pa->access_data($username, "win_c")
		  + $pa->access_data($username, "draw_c");
	($sum_c_2 gt $sum_c_1) ? _print_ok($testname."wara4") : _print_error($testname."wara4".$mes);
	

	#finish_war failed
	
	print "***test_wara::end***\n\n";
}

#print eror
sub _print_error{
	my $point = shift;
	die $point;
}

#print ok
sub _print_ok{
	my $point = shift;
	say $point;
}
