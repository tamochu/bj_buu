#TestFramework/Situations/situation1.pmで生成されるデータを更新する
package refresh_situation1;

sub run{
	use TestFramework::Controller::ControllerConst;
	require "$situation_save_dir/situation1";
	&situation1::refresh();
}
1;
