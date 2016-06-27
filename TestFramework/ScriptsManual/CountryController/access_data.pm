sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::CountryController;
	
	my $cc = CountryController->new();
	if($argvs->{value3} eq "get_value"){
		my $value = $cc->access_data($argvs->{value1}, $argvs->{value2});
		die "$argvs->{value2} = $value\n";
	}
	else{
		$cc->access_data($argvs->{value1}, $argvs->{value2}, $argvs->{value3});
	}

}
1;
