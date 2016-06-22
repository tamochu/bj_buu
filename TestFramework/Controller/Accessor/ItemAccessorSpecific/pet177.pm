package ItemAccessor;
use TestFramework::Controller::ControllerConst;
require "$ControllerConst::accessor_util";

#引数はプレイヤー名、対象の国（０を指定すると
#オプションでペットを連れていく選択肢が出た時の判断、連れていくペットのdepot内のindex
*enact = sub{

	my ($player_name, $target_country, $vacation, $item_index) = @_;


	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);

	};
	my $env_base = Util::fork_sub($make_env);

	#bj.cgiを開き牢獄の選択画面を開く
	my $enter_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
		
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		require "bj.cgi";

		if($m{tp} eq 310){
			return 0;
		}
		elsif($m{tp} eq 330){
			return 1;
		}
		else{
			die "\$m{tp} : expected : 310 or 330\nactual : $m{tp}\n";
		}

	};

	#連れていくぺットを選べる場合
	my $choose_pet = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
		
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		#連れていくペットを選択
		if($vacation){
			$ENV{QUERY_STRING} .= "&cmd=$item_index";
		}
		else{
			$ENV{QUERY_STRING} .= "&cmd=0";
		}
		
		require "bj.cgi";
	};

	#牢獄へ行く
	my $go_prison = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
		
		if($m{tp} ne 310){
			die "\$m{tp} : expected : 310\nactual : $m{tp}\n";
		}

		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		$ENV{QUERY_STRING} .= "&cmd=$target_country";
		print STDERR "env_base = $env_base\n";

		require "bj.cgi";
	};

	my $is_vacation = Util::fork_sub($enter_bj);

	if($is_vacation){
		Util::fork_sub($choose_pet);
	}

	Util::fork_sub($go_prison);
};

1;
