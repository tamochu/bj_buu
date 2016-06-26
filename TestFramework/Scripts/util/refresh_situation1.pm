#TestFramework/Situations/situation1.pmで生成されるデータを更新する
package refresh_situation1;

&run;

sub run{
	use TestFramework::Controller::ControllerConst;
	require "$ControllerConst::situation_save_dir/situation1.pm";

	#既存プレイヤー削除
	require $ControllerConst::controller_helper;
	require $ControllerConst::player_controller;
	my $pc = PlayerController->new();
	my @lines = ControllerHelper::get_all_users();
	for my $line (@lines){
		my @vars = split(/<>/, $line);
		$pc->remove_player($vars[1]);
	}

	&situation1::refresh();
}
1;
