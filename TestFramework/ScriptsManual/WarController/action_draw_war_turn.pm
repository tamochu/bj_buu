sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::WarController;
	
	my $warc = WarController->new();
	$warc->action_draw_war_turn($argvs->{value1});
}
1;
