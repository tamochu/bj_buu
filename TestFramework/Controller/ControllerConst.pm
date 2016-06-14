##########################################
# Controllerで使われる定数
##########################################
package ControllerConst;


##########################################
#WarController
##########################################
#
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
