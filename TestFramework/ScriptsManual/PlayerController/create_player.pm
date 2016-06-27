sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::PlayerController;
	
	my $pc = PlayerController->new();
	$pc->create_player($argvs->{value1}, $argvs->{value2},
		           $argvs->{value3}, $argvs->{value4});

}
1;
