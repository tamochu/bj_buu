sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::CountryController;
	
	my $cc = CountryController->new();
	$cc->action_vote($argvs->{value1}, $argvs->{value2});
}
1;
