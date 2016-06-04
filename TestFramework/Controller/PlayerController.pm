#use strict;
use warnings;

package PlayerAccessAdapter;

use lib qw(./Accessor);
require PlayerAccessor;

sub new{
	my $class = shift;
	my $self = PlayerAccessInterface->new();

	#プレイヤーデータのアクセサ
	$self->{COUNTRY_ACCESSOR_INTERFACE} = PlayerAccessor->new(); 

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
	$self->{COUNTRY_ACCESSOR_INTERFACE}->access_data(@_);

}

#player作成
sub create_player{

	my $self = shift;
	my ($name, $pass, $sex, $address) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $name) and (defined $pass) and (defined $sex)){
		die ("$error_info : PlayerAccessor::create_player needs at least name, pass, and sex");
	}

	#ipアドレスが設定されていれば使用、なければ偽装ipを使用
	unless(defined $address){
		$address = "1.1.1.$self->{IP_ADDRESS_COUNT}";
		$self->{IP_ADDRESS_COUNT}++;
	}

	my $new_name = undef;
	eval{
		$self->{COUNTRY_ACCESSOR_INTERFACE}->create_player(@_);
		$new_name = $self->access_data($name, "name");
	};
	if($@){
		die("$error_info : failed to create player\n", $@);
	}

	#チェック
	if($new_name ne $name){
		die("$error_info : failed to create player $name");
	}
}

#士官させる
sub action_shikan_player{

	my $self = shift;
	my ($name, $to_country) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $name) and (defined $to_country)){
		die ("$error_info : needs at least name and to_country");
	}

	#士官させる
	my $new_country = undef;
	eval{
		$self->{COUNTRY_ACCESSOR_INTERFACE}->move_player($name, $to_country);
		$new_country = $self->access_data($name, "country");
		
	};
	if($@){
		die ("$error_info : failed to shikan\n", $@);	
	}

	#チェック
	if($new_country ne $to_country){
		die ("$error_info : failed to shikan. $name moved to country $new_country");
	}

}

#player削除
sub remove_player{

	my $self = shift;
	my $name = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $name){
		die ("$error_info : needs name");
	}

	#削除
	eval{
		$self->{COUNTRY_ACCESSOR_INTERFACE}->remove_player($name);
	};
	if($@){
		die ("$error_info : failed to remove_player");
	}

	#チェック
	eval{
		$self->access_data($name, "name");
	}
	unless($@){
		die ("$error_info : failed to remove_player");
	}
	$@ = "";
}



1;

