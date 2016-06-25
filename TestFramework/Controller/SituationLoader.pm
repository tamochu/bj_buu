#use strict;
use warnings;

package SituationLoader;
use TestFramework::Controller::ControllerConst;
sub save_situation{

	my $situation_name = shift;
	require $ControllerConst::system_accessor;
	my $sa = SystemAccessor->new();
	my @dirs = ["log", "user", "html", "data"];

	for $dir (@dirs){
		$sa->move_data($dir, $ControllerConst::situation_save_dir."/"$situation_name."/".$dir);
	}

}

sub load_situation{

	my $situation_name = shift;
	require $ControllerConst::system_accessor;
	my $sa = SystemAccessor->new();
	my @dirs = ["log", "user", "html", "data"];

	for $dir (@dirs){
		$sa->move_data($ControllerConst::situation_save_dir."/"$situation_name."/".$dir, $dir);
	}

}
1;
