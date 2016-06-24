sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::country_controller;
	
	my $cc = CountryController->new();
	my $setting = {
		year => $argvs->{value1},
		world => $argvs->{value2},
		country => $argvs->{value3}
	};
	$cc->admin_reset_countries($setting);
}
1;
