package ItemAccessor;
use TestFramework::Controller::ControllerConst;

*enact = sub{

	my ($player_name,$monster_name, $win_mes, $lose_mes, $file_name) = @_;

	#画像ファイルが指定されていなければデフォルトアイコン
	unless(defined $file_name){
		$file_name = "default_icon";
	}

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
	
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		require "bj.cgi";
		if($m{tp} ne 110){
			die "\$m{tp} : expected : 110\nactual : $m{tp}\n";
		}

	};

	#パラメータとサブミットをシミュレーションしてモンスター作成
	my $submit = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_before_bj($player_name);
		$mes = "";
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		$ENV{QUERY_STRING} .= "&name=$monster_name"
				     ."&mes_win=$win_mes"
				     ."&mes_lose=$lose_mes"
				     ."&file_name=$file_name";

		require "bj.cgi";

		if($m{lib} ne ""){
			die "\$m{lib} : expected : \"\"\nactual : $m{lib}\n";
		}

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($submit);
};

1;
