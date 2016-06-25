#TestFramework/Situations/situation1.pmで生成されるデータを更新する
package refresh_situation1;

&run;

sub run{
	use TestFramework::Controller::ControllerConst;
	
	require  $ControllerConst::situation_loader;
	SituationLoader::load_situation("situation1");
}
1;
