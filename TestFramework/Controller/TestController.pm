#コントローラーのテスト

package TestAccessor;
use lib qw(./TestFramework/lib);
use Test::MockTime qw( :all );
use feature 'say';
use lib qw(./TestFramework/Controller/);
require SystemController;


#時刻の誤差
my $time_margin = 1;

test_sc();

#SystemControllerテスト
sub test_sc{
	my $sc = SystemController->new();
	
	#ディレクトリセーブテスト
	#my $to_save_dir = "./log";
	#$sc->save_dir($to_save_dir);
	#$sc->restore();


	#時刻偽装のテスト
	my $current_time = 0;
	my $margined_time = undef;

	$sc->set_time(0);
	$current_time = time;
	$margined_time = 0 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt 0)){
		_print_error("set_time test : current_time expected 0 <= ct <= $margined_time: actual $current_time");
	}

	$sc->set_time(0);
	$sc->advance_time(10);
	$current_time = time;
	$margined_time = 10 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt 10)){
		_print_error("set_time advance_time test : current_time  expected 10 <= ct <= $margined_time: actual $current_time");
	}	
	
	$sc->fix_time(0);
	sleep 1;
	$current_time = time;
	if($current_time ne 0){
		_print_error("fix_time : current_time expected 0 : actual $current_time");
	}


	$sc->advance_time(10);
	sleep 1;
	$current_time = time;
	if($current_time ne 10){
		_print_error("fix_time advance : current_time expected 10 : actual $current_time");
	}


	$sc->restore_time();
	my $natural_time = time;
	$sc->advance_time(10);
	$current_time = time;
	$margined_time = $natural_time + 10 + $time_margin;
	if (($current_time gt $margined_time) or ($current_time lt ($natural_time + 10))){
		_print_error("fix_time advance : current_time expected $natural_time+10 <= $margined_time : actual $current_time");
	}


}

#print eror
sub _print_error{
	my $point = shift;
	die $point;
}
1;
