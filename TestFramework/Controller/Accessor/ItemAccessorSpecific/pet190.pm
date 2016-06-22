package ItemAccessor;
use TestFramework::Controller::ControllerConst;

#引数は自身のプレイヤー名、対象プレイヤー、称号
*enact = sub{

	my ($player_name, $trick_name, $trick_shogo) = @_;
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

		if($m{tp} ne 700){
			die "\$m{tp} : expected : 700\nactual : $m{tp}\n";
		}
	
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		require "bj.cgi";

		if($m{tp} ne 710){
			die "\$m{tp} : expected : 710\nactual : $m{tp}\n";
		}

	};

	#対象プレイヤー選んでいたずら実行
	my $select_and_run= sub{
		
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
	
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		$ENV{QUERY_STRING} .= "&cmd=1".
				      "&trick_name=$trick_name".
				      "&trick_shogo=$trick_shogo";

		$mes = "";
		require "bj.cgi";


		if($m{lib} ne ""){
			die "\$m{lib} : expected : \"\"\nactual : $m{lib}\n";
		}

		#いたずらされた相手の称号チェック
		_read_user($trick_name);
		($m{shogo} eq $trick_shogo) or die "$trickname 's shogo\n expected : $trick_shogo\nactual : $m{shogo}\nmes = $mes\n";

	};


	Util::fork_sub($enter_bj);
	Util::fork_sub($select_and_run);
};

1;
