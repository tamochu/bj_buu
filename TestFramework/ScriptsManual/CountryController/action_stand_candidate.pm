sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::country_controller;
	
	my $cc = CountryController->new();
	$cc->action_stand_candidate($argvs->{value1});
}
1;