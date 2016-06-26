#TestFramework/Situations/situation1.pmで生成されるデータをロードする
package refresh_situation1;

&run;

sub run{
	use TestFramework::Controller::ControllerConst;
	
	require  $ControllerConst::situation_loader;

	#既存プレイヤー削除
	require $ControllerConst::controller_helper;
	require $ControllerConst::player_controller;
	my $pc = PlayerController->new();
	my @lines = ControllerHelper::get_all_users();
	for my $line (@lines){
		my @vars = split(/<>/, $line);
		$pc->remove_player($vars[1]);
	}

	SituationLoader::load_situation("situation1");
}
1;
