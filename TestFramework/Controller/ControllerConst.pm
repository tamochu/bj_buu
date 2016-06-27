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
our $PlayerAccessor = "$accessor_dir/PlayerAccessor.pm";
our $PlayerController = "$controller_dir/PlayerController.pm";
our $CountryAccessor = "$accessor_dir/CountryAccessor.pm";
our $CountryController= "$controller_dir/CountryController.pm";
our $WorldAccessor = "$accessor_dir/WorldAccessor.pm";
our $WorldController = "$controller_dir/WorldController.pm";
our $SystemAccessor = "$accessor_dir/SystemAccessor.pm";
our $SystemControler = "$controller_dir/SystemController.pm";
our $WarAccessor = "$accessor_dir/WarAccessor.pm";
our $WarController = "$controller_dir/WarController.pm";
our $ItemAccessor = "$accessor_dir/ItemAccessor.pm";
our $ItemController = "$controller_dir/ItemController.pm";
our $SimulationLoader = "$controller_dir/SituationLoader.pm";
our $ControllerHelper = "$controller_dir/ControllerHelper.pm";

#bjのcgiをrequireする際のラッパー
our $bj_wrapper = "$accessor_dir/BJWrapper.pm";

#アクセッサーで使うユーティリティ
our $accessor_util = "$accessor_dir/Util.pm";

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
