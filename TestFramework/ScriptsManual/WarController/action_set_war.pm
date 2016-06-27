sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::WarController;
	
	my $warc = WarController->new();
	$warc->action_set_war($argvs->{value1}, $argvs->{value2}, $argvs->{value3});
}
1;
