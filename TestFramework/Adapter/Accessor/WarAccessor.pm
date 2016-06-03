####################################
# 戦争関連のアクセサ
####################################

use warnings;
use CGI::Carp;
#use strict;

package WarAccessor;
require './TestFramework/Adapter/Accessor/Util.pm';

#BJWrapper.pmのファイル名
my $bj_wapper = './TestFramework/Adapter/Accessor/BJWrapper.pm';

#main.cgiのメニュー上の戦争のコマンド番号
my $menu_cmd_war = 11;

#陣形じゃんけんで固定で出される陣形
my $cmd_formation = 1;

sub new{
	my $class = shift;
	my $self = {};
	return bless $self, $class;
}

#playerに進軍させる(far_form.cgi経由)
sub set_war{
	
	my $self = shift;
	my ($player_name, $target_country, $mode) = @_;



	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env_base = sub{
		require $bj_wapper;
		return BJWrapper::_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env_base);
	
	#bj.cgiを開く
	my $enter_bj = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		_is_bound($player_name);

		&write_user;
		$ENV{QUERY_STRING} = $env_base;
		require "bj.cgi";
	

	};

	#bj.cgiを開きメニューから戦争を選択する
	my $open_menu = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		$mes = "";
		$m{tp} = 1;
		&write_user;

		$ENV{QUERY_STRING} = $env_base."&cmd=$menu_cmd_war";
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to set war : m{lib} = $m{lib} mes = $mes") if ($m{lib} ne "war_form");
	};

	#規模を選択する
	my $select_war_mode = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		$mes = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$mode";
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to set war : m{tp} = $m{tp} mes = $mes") if ($m{tp} ne 100);
		
	};

	#国を選択して出撃
	my $depart = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{QUERY_STRING} = $env_base."&cmd=$target_country";
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to set war : m{lib} = $m{lib} mes = $mes") if ($m{lib} ne "war");

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($open_menu);
	Util::fork_sub($select_war_mode);
	Util::fork_sub($depart);

}

#進軍を着弾させる(war.cgi経由)
#要set_war()
sub encount{
	
	my $self = shift;
	my $player_name = shift;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env_base = sub{
		require $bj_wapper;
		return BJWrapper::_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env_base);

	my $enter_bj= sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{QUERY_STRING} = $env_base;
		$mes = "";
		
		require "bj.cgi";

		_read_user($player_name);
		die ("failed to encount : m{tp} = $m{tp}, mes = $mes") if ($m{tp} ne 110);

	};

	#限界ターンなどの提示画面を開く
	my $open_turn = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		$mes = "";
		$ENV{QUERY_STRING} = $env_base;
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to encount : $mes") if ($m{tp} ne 120);

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($open_turn);

}

#戦闘する
sub step_war{

	my $self = shift;
	my $player_name = shift;
	
	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env_base = sub{
		require $bj_wapper;
		return BJWrapper::_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env_base);
	
	#陣形を選んで交戦
	my $select_formation = sub{

		require $bj_wapper;
		package BJWrapper;

		_before_bj($player_name);
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to encount : m{tp} = $m{tp}") unless (($m{tp} eq 120) or ($m{tp} eq 130) or ($m{tp} eq 0));

	};

	Util::fork_sub($select_formation);

}




1;
