####################################
# 戦争関連のアクセサ
####################################

use warnings;
use CGI::Carp;
#use strict;

package WarAccessor;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::accessor_util;

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
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);
	
	#bj.cgiから戦争を選ぶ
	my $enter_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_is_bound($player_name);

		$m{lib} = "main";
		$m{tp} = 1;
		&write_user;
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$menu_cmd_war";
		require "bj.cgi";
		_read_user($player_name);
		die ("in enter_bj failed to set war : m{lib} = $m{lib} mes = $mes\n") if ($m{lib} ne "war_form");

	};

	#規模選択
	my $select_mode = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_read_user($player_name);
		$mes = "";

		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$mode";
		require "bj.cgi";
		_read_user($player_name);
		die ("in select_mode failed to set war : m{tp} = $m{tp} mes = $mes\n") if ($m{tp} ne 100);
	};

	#相手国を選び出発
	my $select_country= sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$mes = "";
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$target_country";
		require "bj.cgi";
		_read_user($player_name);
		die ("in select_country failed to set war : m{lib} = $m{lib} mes = $mes\n") if ($m{lib} ne "war");
	};

	#国を選択して出撃
	my $depart = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$target_country";
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to set war : m{lib} = $m{lib} mes = $mes\n") if ($m{lib} ne "war");

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($select_mode);
	Util::fork_sub($select_country);

}

#進軍を着弾させる(war.cgi経由)
#要set_war()
sub encount{
	
	my $self = shift;
	my $player_name = shift;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);

	my $enter_bj= sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		$mes = "";
		
		require "bj.cgi";

		_read_user($player_name);
		die ("in enter_bj failed to encount : m{tp} = $m{tp}, mes = $mes\n") if ($m{tp} ne 110);

	};

	#限界ターンなどの提示画面を開く
	my $open_turn = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$mes = "";
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		require "bj.cgi";
		_read_user($player_name);
		die ("in open_turn failed to encount : $mes\n") if ($m{tp} ne 120);

	};

	Util::fork_sub($enter_bj);
	Util::fork_sub($open_turn);

}

#戦闘する
sub step_war{

	my $self = shift;
	my $player_name = shift;
	
	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);

	#陣形を選んで交戦
	my $select_formation = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_read_user($player_name);

		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$cmd_formation";
		require "bj.cgi";
		_read_user($player_name);
		die ("failed to step_war : m{tp} = $m{tp}\n") unless (($m{tp} eq 120) or ($m{tp} eq 130) or ($m{tp} eq 0) or ($m{lib} eq "world"));

	};

	Util::fork_sub($select_formation);

}


#統一後の選択肢を選ぶ
sub action_after_toitsu{

	my $self = shift;
	my ($player_name, $cmd) = @_;
	
	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);

	#bj.cgiを開く
	my $open_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_read_user($player_name);

		($m{lib} eq "world") or die "open_bj failed : m{lib} = $m{lib}\n";
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;
		require "bj.cgi";

	};

	#統一後の選択をする
	my $select_after_toitsu= sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_read_user($player_name);


		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$cmd";
		require "bj.cgi";
		_read_user($player_name);
		die ("select_after_toitsu failed : m{lib} = $m{lib}\n") unless ($m{lib} eq "");
	};

	Util::fork_sub($open_bj);
	Util::fork_sub($select_after_toitsu);

}


1;
