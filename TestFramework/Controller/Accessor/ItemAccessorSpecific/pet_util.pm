###########################################
# ペット固有の処理で使われる共通処理
###########################################

package pet_util;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::accessor_util;

#ペットが事前にマイルームで使われているか
sub is_ready{

	my ($player_name, $pet_no, $lib, $tp) = @_;
		
	die "$ControllerConst::accessor_util\n";
	my $check_ready = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_read_user($player_name);
		#ペットがセットされている
		unless($m{pet} eq $pet_no){
			die "\$m{pet} : expected : $pet_no\nactual :  $m{pet}\n";
		}

		#libチェック
		unless($m{lib} eq $lib){
			die "\$m{lib} : expected $lib\nactual : $m{lib}\n";
		}
		
		#tpチェック
		unless($m{lib} eq $tp){
			die "\$m{tp} : expected $tp\nactual : $m{tp}\n";
		}
		
	};
	Util::fork_sub($check_ready);
}
1;
