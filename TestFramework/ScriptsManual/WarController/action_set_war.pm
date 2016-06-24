sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::war_controller;
	
	my $warc = WarController->new();
	$warc->action_set_war($argvs->{value1}, $argvs->{value2}, $argvs->{value3});
}
1;
