package TestCUI;

use feature 'say';
use lib qw(./TestFramework/Adapter/Accessor);
require "PlayerAccessor.pm";
require "CountryAccessor.pm";
require "WorldAccessor.pm";

my $username_first_part = "test";
my $username_sufix = "15";
my $username = $username_first_part.$username_sufix;
my $passward = "test4a";

my $added_country_name = "test_country";
#test_ca();
#test_pa();
test_wa();

#PlayerAccessorテスト
sub test_pa{
	my $first_country = 1;
	my $second_country = 2;
	
	my $pa = PlayerAccessor->new();
	$pa->create_player($username, $passward, 1, "1.1.1.$username_sufix");
	my $ca = CountryAccessor->new();
	say "access_data($first_country, capacity, 25) = " ,$ca->access_data($first_country, "capacity", 35);
	say "access_data($second_country, capacity, 25) = " ,$ca->access_data($second_country, "capacity", 35);
	say "line\n";
	
	say "shikan_player=" , $pa->shikan_player($username, $first_country) ;
	say "access_data(test, country) = " , $pa->access_data($username, "country") ;
	say "shikan_player=" , $pa->shikan_player($username, $second_country) ;
	say "access_data(test, country) = " , $pa->access_data($username, "country") ;
	$pa->remove_player($username);
}

#CountryAccessorテスト
sub test_ca{

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
}

#WorldAccesorテスト
sub test_wa{
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
}
