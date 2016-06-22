package ItemAccessor;
use TestFramework::Controller::ControllerConst;

#引数は自身のプレイヤー名、武器の名前、武器の属性
*enact = sub{

	my ($player_name, $weapon_name, $type) = @_;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);

	};
	my $env_base = Util::fork_sub($make_env);

	#bj.cgiを開き設定画面を出す
	my $enter_bj = sub{
		
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
		_read_user($player_name);

		if($m{tp} ne 800){
			die "\$m{tp} : expected : 600\nactual : $m{tp}\n";
		}
	
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		require "bj.cgi";

		if($m{tp} ne 810){
			die "\$m{tp} : expected : 810\nactual : $m{tp}\n";
		}

	};

	#いたずら実行
	my $select_and_run= sub{
		
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
	
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		$ENV{QUERY_STRING} .= "&cmd=1".
				      "&type=$type".
				      "&weapon_name=$weapon_name";

		$mes = "";
		require "bj.cgi";


		if($m{lib} ne ""){
			die "\$m{lib} : expected : \"\"\nactual : $m{lib}\n";
		}

	};


	Util::fork_sub($enter_bj);
	Util::fork_sub($select_and_run);
};

1;
