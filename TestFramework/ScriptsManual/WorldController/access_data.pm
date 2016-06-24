sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::world_controller;
	
	my $wc = WorldController->new();
	if($argvs->{value2} eq "get_value"){
		my $value = $wc->access_data($argvs->{value1});
		die "$argvs->{value1} = $value\n";
	}
	else{
		$wc->access_data($argvs->{value1}, $argvs->{value2});
	}

}
1;
