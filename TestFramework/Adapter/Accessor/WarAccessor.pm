####################################
# 戦争関連のアクセサ
####################################

use warnings;
#use strict;

package WarAccessor;
require './TestFramework/Adapter/Accessor/Util.pm';
use CGI::Carp;

#main.cgiのメニュー上の戦争のコマンド番号
my $menu_cmd_war = 11;

sub new{
	my $class = shift;
	my $self = {};
	return bless $self, $class;
}

#playerに進軍させる(far_form.cgi経由)
sub set_war{
	
	my $self = shift;
	my ($player_name, $target_country, $mode) = @_;
	my $player_id = unpack('H*', $player_name);
	my $pass = _get_pass($player_name);
	my $env_base = "id=$player_name&pass=$pass";


	#bj.cgi開く
	my $enter_bj = sub{

		_before_bj($player_name);
		_is_bound($player_name);

		&write_user;
		$ENV{QUERY_STRING} = $env_base;
		require "bj.cgi";
		
	};

	#メニューから戦争を選択する
	my $open_menu = sub{

		_before_bj($player_name);
		$m{tp} = 1;
		&write_user;

		$ENV{QUERY_STRING} = $env_base."&cmd=$menu_cmd_war";
		require "bj.cgi";
		_read_user($player_name);
		die "failed to set war : $mes" if ($m{lib} ne "war_form");
	};

	#規模を選択する
	my $select_war_mode = sub{

		_before_bj($player_name);
		$ENV{QUERY_STRING} = $env_base."&cmd=$mode";
		require "bj.cgi";
		die "failed to set war : $mes" if ($m{tp} ne 100);
		
	};

	#国を選択して出撃
	my $depart = sub{

		_before_bj($player_name);
		$ENV{QUERY_STRING} = $env_base."cmd=$target_country";
		require "bj.cgi";
		die "failed to set war : $mes" if ($m{lib} ne "war");

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
	
	$sub_routine = sub{

		_before_bj($player_name);
		#拘束中ならこの画面には入らない
		_is_bound($player_name);
		

		require './lib/war.cgi';

		#war.cgiの利用条件
		unless(&is_satisfy){
			croak $mes;
		}

		&tp_100;
		&write_user;
		&write_cs;
		return $mes;

	};

	return Util::fork_sub($sub_routine);
}

#戦闘して勝利、敗北、引き分け、撤退を呼ぶ(war.cgi経由)
#要encount()
sub finish_war{

	my $self = shift;
	my $player_name = shift;

	my $sub_routine = sub {

		_before_bj($player_name);
		_is_bound($player_name);

		require './lib/war.cgi';

		#war.cgiの利用条件
		unless(&is_satisfy){
			die $mes;
		}

		#じゃんけんは全て１のまま戦闘開始
		$cmd = 1;
		while($m{tp}){


			$mes = "";
			#撤退なしの戦闘
			&tp_190;
			
			&write_user;	
			_read_user();
		}


		return $mes;

	};

	return Util::fork_sub($sub_routine);
	
}

#戦闘過程をスキップして結果を呼び出す(_war_result.cgi経由)
#要encount()
sub finish_war_skip_battle{

	my $self = shift;
	my ($name, $result, $is_single) = @_;

	my $sub_routine = sub{

		_before_bj($player_name);

		require './lib/_war_result.cgi';

		#war_result.cgiの利用条件
		unless(&is_satisfy){
			croak $mes;
		}

		#過程をスキップして結末へ
		if($result eq 0){
			#引き分け
			&war_draw;
			
		}
		elsif($result eq 1){
			#負け
			&war_lose;
		}
		elsif($result eq 2){
			#退却
			&war_escape;

		}
		elsif($result eq 3){
			#勝ち
			&war_win($is_single);
		}
		else{
			croak "error: argument \$result needs to be within the range of 0 to 3";
		}

		&write_user;
		return $mes;

	};

	return Util::fork_sub($sub_routine);

}

#bj.cgiのbefore_bj偽装
sub _before_bj{

	my $user_name = shift;
	_load_config();
	_read_user($user_name);
	&read_cs;
}

#forkしたプロセスからbjのCGIをrequireする
sub _load_config{

	require "config.cgi";
	require "config_game.cgi";
}

#ユーザー名から%m,%yにデータ読み込み
sub _read_user{

	my $user_name = shift;

	my $id = unpack ('H*', $user_name);


	#%m %yへユーザーデータ読み込み
	$in{id} = $id;
	$in{pass} = _get_pass($user_name);
	&read_user;
}

#pass検索
sub _get_pass{

	my $user_name = shift;
	my $user_id = unpack('H*', $user_name);

	_load_config();

	open my $fh, "< $userdir/$user_id/user.cgi" or croak("couldn't open ", $userdir, "/", $user_id, "/user.cgi");
	my $line = <$fh>;	
	close $fh;

	my $pass;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if($k eq "pass") {
			$pass = $v;	
			last;
		}
	}

	return $pass;
}

#拘束判定
sub _is_bound{

	my $user_name = shift;
	_load_config();
	_read_user($user_name);

	#拘束中	
	if($m{wt} > 0){
		die "is bound : m{wt} > 0"; 
	}

	#lib処理中
	if($m{lib}){
		die "is in the middle of processing $m{lib}";
	}
}

1;
