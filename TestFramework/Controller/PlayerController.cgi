#use strict;
use warnings;

package PlayerController;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::player_accessor;

sub new{
	my $class = shift;
	my $self = PlayerAccessor->new();

	#プレイヤーデータのアクセサ
	$self->{PLAYER_ACCESSOR_INTERFACE} = PlayerAccessor->new(); 

	#プレイヤー生成時に使う偽装ipアドレスのカウンタ
	$self->{IP_ADDRESS_COUNT} = 0;

	bless ($self, $class);

	return $self;
}


######################################
# テストから呼び出される関数
#####################################

#user/id/user.cgiからデータを取得/設定
sub access_data{
	
	my $self = shift;
	$self->{PLAYER_ACCESSOR_INTERFACE}->access_data(@_);

}

#tp,wtを0に、libを空にした状態でbj.cgiを開く
sub refresh_player{

	my $self = shift;
	my $name = shift;

	$self->access_data($name, "wt", 0);
	$self->access_data($name, "lib", "");
	$self->access_data($name, "tp", 0);
	$self->{PLAYER_ACCESSOR_INTERFACE}->open_bj($name);

}

#player作成
sub create_player{

	my $self = shift;
	my ($name, $pass, $sex, $address) = @_;

	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $name) and (defined $pass) and (defined $sex)){
		die ("$error_info : PlayerAccessor::create_player needs at least name, pass, and sex\n");
	}

	#ipアドレスが設定されていれば使用、なければ偽装ipを使用
	unless(defined $address){
		$address = "10.1.1.$self->{IP_ADDRESS_COUNT}";
		$self->{IP_ADDRESS_COUNT}++;
	}
	my $new_name;
	eval{
		$self->{PLAYER_ACCESSOR_INTERFACE}->create_player($name, $pass, $sex, $address);
		$new_name = $self->{PLAYER_ACCESSOR_INTERFACE}->access_data($name, "name");
	};
	if($@){
		die("$error_info : create_player()\n", $@);
	}

	#チェック
	if($new_name ne $name){
		die("$error_info : create_player $name\n");
	}
}

#士官させる
sub action_shikan_player{

	my $self = shift;
	my ($name, $to_country) = @_;

	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $name) and (defined $to_country)){
		die ("$error_info : action_shikan_player needs at least name and to_country\n");
	}

	#士官させる
	my $new_country = undef;
	eval{
		$self->{PLAYER_ACCESSOR_INTERFACE}->shikan_player($name, $to_country);
		$new_country = $self->access_data($name, "country");
		
	};
	if($@){
		die ("$error_info : action_shikan_player\n", $@);	
	}

}

#player削除
sub remove_player{

	my $self = shift;
	my $name = shift;

	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $name){
		die ("$error_info : needs name\n");
	}

	#削除
	eval{
		$self->{PLAYER_ACCESSOR_INTERFACE}->remove_player($name);
	};
	if($@){
		die ("$error_info : remove_player failed\n", $@);
	}

	#チェック
	eval{
		$self->access_data($name, "name");
	};
	unless($@){
		die ("$error_info : remove_player failed\n");
	}
	$@ = "";
}



1;

