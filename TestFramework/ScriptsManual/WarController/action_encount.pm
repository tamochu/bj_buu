sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::WarController;
	
	my $warc = WarController->new();
	$warc->action_encount($argvs->{value1});
}
1;
