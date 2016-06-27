sub run{

	my $argvs = shift;
	require "./TestFramework/Controller/ControllerConst.pm";
	require $ControllerConst::PlayerController;
	
	my $pc = PlayerController->new();
	if($argvs->{value3} ne "get_value"){
		$pc->access_data($argvs->{value1}, $argvs->{value2}, $argvs->{value3});
	}
	else{
		my $value = $pc->access_data($argvs->{value1}, $argvs->{value2});
		die "$argvs->{value2} = $value\n"; 
	}

}
1;
