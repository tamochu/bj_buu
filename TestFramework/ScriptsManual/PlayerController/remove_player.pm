sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::PlayerController;
	
	my $pc = PlayerController->new();
	$pc->remove_player($argvs->{value1});

}
1;
