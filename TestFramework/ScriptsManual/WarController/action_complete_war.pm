sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::WarController;
	
	my $warc = WarController->new();
	$warc->action_complete_war($argvs->{value1});

}
1;
