sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::player_controller;
	
	my $pc = PlayerController->new();
	$pc->action_shikan_player($argvs->{value1}, $argvs->{value2});

}
1;
