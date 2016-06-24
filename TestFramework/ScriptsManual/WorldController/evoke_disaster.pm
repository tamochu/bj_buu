sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::world_controller;
	
	my $wc = WorldController->new();
	$wc->evoke_disaster($argvs->{value1});

}
1;
