####################################
# プレイヤーデータのアクセサ
# access_data以外の関数はプレイヤーの操作を疑似的に再現する
####################################

use warnings;
use CGI::Carp;
#use strict;

package PlayerAccessor;

require './TestFramework/Controller/Accessor/Util.cgi';

#BJWrapper.cgiのファイル名
my $bj_wrapper = './TestFramework/Controller/Accessor/BJWrapper.cgi';

sub new{
	my $class = shift;
	my $self = {};

	return bless $self, $class;
}

#./user/user.cgiのデータを直接読み書きする
sub access_data{


	my $self = shift;
	my $user_name = shift;
	my $key = shift;
	my $new_value = shift;

	my $sub_routine = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($user_name);


		#新しい値が設定されていれば設定、なければ取得
		if (defined($new_value)){
		
			#y_の形のkeyなら%yに設定
			if ($key =~ /^y_(.+)$/){
				$y{$1} = $new_value;
			}
			else{
				$m{$key} = $new_value;
			}
	
			&write_user;
			_read_user($user_name);

		}

		if ($key =~ /^y_(.+)$/){
			return $y{$1};
		}
		else{
			return $m{$key};
		}
	};

	return Util::fork_sub($sub_routine);

}

#プレイヤーを作成する(new_entry.cgi経由)
sub create_player{

	my $self = shift;
	my ($name, $pass, $sex, $address) = @_;


	#new_entry.cgiからプレイヤー作成
	my $create = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();

		#同じ名前のプレイヤーが既にいるとnew_entry.cgiからは例外を吐かないのでここで判定
		my $dir = unpack('H*', $name);
		if(-d "$userdir/$dir"){
			die("PlayerAccessor::creat_player failed: $name already exists\n");
		}

		$ENV{REQUEST_METHOD} = "";	
		$ENV{REMOTE_ADDR} = $address;	
		$ENV{QUERY_STRING} = "mode=new_entry&name=$name&pass=$pass&sex=$sex";
		require 'new_entry.cgi';
	};

	#login.cgiを一度呼ばないと直後の処理でエラーが出る
	my $login = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		$ENV{REQUEST_METHOD} = "";	
		$ENV{QUERY_STRING} = "login_name=$name&pass=$pass";
		require 'login.cgi';
	};

	#bj.cgiを開きリフレッシュを呼ぶ
	my $back_bj = sub{

		require $bj_wrapper;
		package BJWrapper;
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base; 
		require "bj.cgi";
	};

	
	Util::fork_sub($create);
	Util::fork_sub($login);
	Util::fork_sub($back_bj);
	
}

#プレイヤーを削除する(.lib/move_player.cgi経由)
sub remove_player{

	my $self = shift;
	my $name = shift;

	my $sub_routine = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);

		require './lib/move_player.cgi';

		&read_cs;

		move_player($name, $m{country}, "del");
	};

	return Util::fork_sub($sub_routine);

}

#プレイヤーに士官させる
sub shikan_player{

	my $self = shift;
	my ($name, $to_country) = @_;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{

		require $bj_wrapper;
		package BJWrapper;
		_make_env_base($name);

	};
	my $env_base = Util::fork_sub($make_env);

	#国情報を開く
	my $enter_bj = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);
		_is_bound($name);

		$mes = "";
		#国情報
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=7"; 
		require "bj.cgi";
		_read_user($name);
		die ("in enter_bj false m{lib} : $m{lib}, mes = $mes\n") if ($m{lib} ne "country");

	};

	#国情報から国選択画面へ
	my $country_info = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);

		#士官
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=2"; 
		require "bj.cgi";
		_read_user($name);
		die ("in country_info false m{lib} :  $m{lib}, mes = $mes\n") if ($m{lib} ne "country_move");

	};

	#国選択画面から国を選択
	my $select_country = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);

		#国を選択
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$to_country"; 
		require "bj.cgi";
		_read_user($name);
		die ("failed to select country : m{tp} = $m{tp} mes = $mes\n") if ($m{tp} ne 300);

	};

	#士官
	my $shikan = sub{

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);

		#士官
		$ENV{REQUEST_METHOD} = "";	
		$ENV{QUERY_STRING} = $env_base."&cmd=1"; 
		require "bj.cgi";
		_read_user($name);
		
		#チェック。放浪時はm{country}は0
		&read_cs;
		my $num_country = $w{country};
		if($to_country eq ($num_country+1)){
			$to_country = 0;
		}
		die ("failed to shikan : m{country} = $m{country} mes = $mes\n") if ($m{country} ne $to_country);

	};

	#bj.cgiを開く
	my $back_bj = sub{
		require $bj_wrapper;
		package BJWrapper;

		$ENV{REQUEST_METHOD} = "";	
		$ENV{QUERY_STRING} = $env_base; 
		require "bj.cgi";

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($country_info);
	Util::fork_sub($select_country);
	Util::fork_sub($shikan);
	Util::fork_sub($back_bj);

}


#bj.cgiを開く
sub open_bj{

	my $self = shift;
	my $name = shift;

	$enter_bj = sub {

		require $bj_wrapper;
		package BJWrapper;

		_load_config();
		_read_user($name);

		require "bj.cgi";
	};

	Util::fork_sub($enter_bj);
}
1;
