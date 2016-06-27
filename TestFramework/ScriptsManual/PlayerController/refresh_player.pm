sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::PlayerController;
	
	my $pc = PlayerController->new();
	$pc->refresh_player($argvs->{value1});

}
1;
