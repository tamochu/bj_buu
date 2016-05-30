#use strict;
use warnings;

package PlayerAccessAdapter;

use lib qw(./Accessor);
require PlayerAccessor;

sub new{
	my $class = shift;
	my $self = PlayerAccessInterface->new();

	#国データのアクセサ
	$self->{COUNTRY_ACCESSOR_INTERFACE} = PlayerAccessor->new(); 

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
	$self->{COUNTRY_ACCESSOR_INTERFACE}->create_player(@_);
}

#player移籍
sub move_player{
	my $self = shift;
	$self->{COUNTRY_ACCESSOR_INTERFACE}->move_player(@_);

}

#player削除
sub remove_player{
	my $self = shift;
	my $name = shift;
	$self->{COUNTRY_ACCESSOR_INTERFACE}->move_player($name, 0, "del");
}

#playerにアイテムを与える
sub give_item{
}

#playerにアイテムを装備させる
sub set_item{
}

#playerに装備したペットを使用させる
sub use_item{
}


#playerを結婚させる
sub marriage{
}



1;

