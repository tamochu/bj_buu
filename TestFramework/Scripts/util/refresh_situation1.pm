#TestFramework/Situations/situation1.pmで生成されるデータを更新する
package refresh_situation1;

&run;

sub run{
	use TestFramework::Controller::ControllerConst;
	require "$ControllerConst::situation_save_dir/situation1.pm";
	&situation1::refresh();
}
1;
