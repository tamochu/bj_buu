##########################################
# Controllerで使われる定数
##########################################
package ControllerConst;

#ディレクトリパス
our $testframework_root = "./TestFramework";
our $controller_dir = "$testframework_root/Controller";
our $accessor_dir = "$controller_dir/Accessor";
our $item_accessor_specific = "$accessor_dir/ItemAccessorSpecific";
our $situation_save_dir = "$testframework_root/Situations";
our $user_dir = "user";

#モジュールのパス
our $player_accessor = "$accessor_dir/PlayerAccessor.cgi";
our $player_controller = "$controller_dir/PlayerController.cgi";
our $country_accessor = "$accessor_dir/CountryAccessor.cgi";
our $country_controller = "$controller_dir/CountryController.cgi";
our $world_accessor = "$accessor_dir/WorldAccessor.cgi";
our $world_controller = "$controller_dir/WorldController.cgi";
our $system_accessor = "$accessor_dir/SystemAccessor.cgi";
our $system_controller = "$controller_dir/SystemController.cgi";
our $war_accessor = "$accessor_dir/WarAccessor.cgi";
our $war_controller = "$controller_dir/WarController.cgi";
our $item_accessor = "$accessor_dir/ItemAccessor.cgi";
our $item_controller = "$controller_dir/ItemController.cgi";
our $situation_loader = "$controller_dir/SituationLoader.pm";
our $controller_helper = "$controller_dir/ControllerHelper.pm";

#bjのcgiをrequireする際のラッパー
our $bj_wrapper = "$accessor_dir/BJWrapper.cgi";

#アクセッサーで使うユーティリティ
our $accessor_util = "$accessor_dir/Util.cgi";

##########################################
# WarController
##########################################

#set_war():戦争の規模
use constant WAR_SMALL => 1;
use constant WAR_MEDIUM => 2;
use constant WAR_LARGE => 3;

#action_complete_war:最大ターン
use constant WAR_MAX_TURN => 50;

#action_complete_war:結果
use constant WAR_RESULT_WIN => 1;
use constant WAR_RESULT_LOSE => 2;
use constant WAR_RESULT_DRAW => 3;
use constant WAR_RESULT_PRISONED => 4;



1;
