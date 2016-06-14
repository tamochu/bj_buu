#use strict;
use warnings;

package WarController;

require "./TestFramework/Controller/Accessor/WarAccessor.pm";
require "./TestFramework/Controller/Accessor/PlayerAccessor.pm";


sub new{
	my $class = shift;
	my $self = {};

	#戦争関連のアクセサ
	$self->{WAR_ACCESSOR_INTERFACE} = WarAccessor->new(); 
	$self->{PLAYER_ACCESSOR_INTERFACE} = PlayerAccessor->new();

	return bless $self, $class;
}

#進軍させる
#進軍するプレイヤー名、対象の国、進軍規模(定数)
use constant SMALL => 0;
use constant MEDIUM => 1;
use constant LARGE => 2;
sub action_set_war{

	my $self = shift;
	my ($player_name, $target_country, $mode) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $player_name) and (defined $target_country) and (defined $mode)){
		die ("$error_info : set_war needs player_name, target_country, and mode");
	}
	
	#進軍させる
	my $check = 0;
	eval{
		
		$self->{WAR_ACCESSOR_INTERFACE}->set_war($player_name, $target_country, $mode);
		if($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib")	eq "war"){
			$check = 1;
		}
	};
	if($@){
		die ("$error_info : set_war failed\n", $@);
	}

	#チェック
	unless($check){
		die ("$error_info : set_war failed\n", $@);
	}
	
}

#着弾する
sub action_encount{

	my $self = shift;
	my $player_name = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_encount needs player_name");
	}
	
	#着弾させる
	my $check = 0;
	eval{
		
		$self->{WAR_ACCESSOR_INTERFACE}->encount($player_name);
		if($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib")	eq "war"){
			$check = 1;
		}
	};
	if($@){
		die ("$error_info : action_encount failed\n", $@);
	}

	#チェック
	unless($check){
		die ("$error_info : action_encount failed\n", $@);
	}

}


#戦闘を行う
sub action_step_war{

	my $self = shift;
	my ($player_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_step_war needs player_name");
	}

	#戦闘させる
	my $check = 0;
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib");
		}

		#戦闘
		$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
	};
	if($@){
		die ("$error_info : set_war failed\n", $@);
	}

}


#無限ループ防止のための最大ターンの範囲で勝敗が付くまで戦争を行う
use constant MAX_TURN => 50;
#戻り値は勝敗結果の定数
use constant WIN => 1;
use constant LOSE => 2;
use constant DRAW => 3;
use constant PRISONED => 4;
sub action_complete_war{

	my $self = shift;
	my ($player_name) = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	my $ret = undef;

	unless (defined $player_name){
		die ("$error_info : action_complete_war needs player_name");
	}

	#戦闘させる
	my $check_sum_c = 0;
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib\n");
		}

		#戦闘前に戦績を記憶
		my $check_win_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "win_c");
		my $check_lose_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lose_c");
		my $check_draw_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c");

		#決着がつくまで戦闘
		for my $i (0 .. MAX_TURN){

			$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
			if($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") ne "war"){
				last;
			}

		};

		
		if($check_win_c lt $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "win_c")){
			return WarController::WIN;
		}
		elsif ($check_lose_c lt $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lose_c")){
			if($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") eq "prison"){
				return  WarController::PRISONED;
			}
			else{
				return  WarController::LOSE;
			}
		}
		elsif ($check_draw_c lt $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c")){
			return  WarController::DRAW;
		}
		else{
			die ("$error_info : failed to complete war: \n");
		}


	};
	if($@){
		die $@,"\n";
	}

}

#相手の兵力を０、自軍の兵力を１００００にして戦闘を行い勝利する
sub action_win_war{

	my $self = shift;
	my ($player_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_win_war needs player_name\n");
	}
	
	#戦闘させる
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib\n");
		}

		#事前に勝利数を記録
		my $win_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "win_c");

		#兵力設定
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "sol", 10000);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "y_sol", 0);

		#戦闘
		$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
		unless($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") eq ""){
			die ("$error_info : failed to win_war\n");
		}
		
		#チェック
		if(($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "win_c") - $win_c) ne 1){
			die ("$error_info : failed to win_war\n");
		}
		
	};
	if($@){
		die ("$error_info : win_war failed\n", $@);
	}

}

#自分の兵力を０、相手の兵力を１００００にして戦闘を行い敗北する
sub action_lose_war{

	my $self = shift;
	my ($player_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_lose_war needs player_name\n");
	}
	
	#戦闘させる
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib\n");
		}

		#事前に敗北数を記録
		my $lose_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lose_c");

		#兵力設定
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "sol", 0);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "y_sol", 10000);

		#戦闘
		$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
		unless($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") ne "war"){
			die ("$error_info : failed to lose_war\n");
		}
		
		#チェック
		if(($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lose_c") - $lose_c) ne 1){
			die ("$error_info : failed to lose_war\n");
		}
		
	};

	if($@){
		die ("$error_info : lose_war failed\n", $@);
	}


}

#ターンを０、相手と自分の兵力を１００００にして戦闘し引き分けにする
sub action_draw_war_turn{

	my $self = shift;
	my ($player_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_draw_war_turn needs player_name\n");
	}
	
	#戦闘させる
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib\n");
		}

		#事前に引き分け数を記録
		my $draw_c = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c");

		#兵力、ターンを設定
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "sol", 10000);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "y_sol", 10000);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "turn", 0);

		#戦闘
		$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
		unless($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") eq ""){
			die ("$error_info : failed to draw_war_turn\n");
		}
		
		#チェック
		if(($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c") - $draw_c) ne 1){
			die ("$error_info : failed to draw_war_turn\n");
		}
		
	};

	if($@){
		die ("$error_info : draw_war_turn failed\n", $@);
	}
	
}

#自分と相手の兵力を０にして両軍壊滅させる
sub action_draw_war_kaimetu{

	my $self = shift;
	my ($player_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name){
		die ("$error_info : action_draw_war_kaimetu needs player_name\n");
	}
	
	#戦闘させる
	eval{

		#進軍していなければエラー
		my $lib = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib");
		if($lib ne "war"){
			die ("$error_info : $player_name has not set to war. \$m{lib} = $lib\n");
		}

		#事前に引き分け数を記録
		my $draw_c= $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c");

		#兵力、ターンを設定
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "sol", 0);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "y_sol", 0);
		$self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "turn", 10);

		#戦闘
		$self->{WAR_ACCESSOR_INTERFACE}->step_war($player_name);
		unless($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "lib") eq ""){
			die ("$error_info : failed to draw_war_kaimetu\n");
		}
		
		#チェック
		if(($self->{PLAYER_ACCESSOR_INTERFACE}->access_data($player_name, "draw_c") - $draw_c) ne 1){
			die ("$error_info : failed to draw_war_kaimetu\n");
		}
		
	};

	if($@){
		die ("$error_info : draw_war_kaimetu failed\n", $@);
	}
}



