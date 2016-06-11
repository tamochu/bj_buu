#####################################
# 世界をコントロールする
#####################################


#use strict;
use warnings;

package WorldController;
require "./TestFramework/Controller/Accessor/WorldAccessor.pm";

sub new{

	my $class = shift;
	my $self = {};

	#世界データのアクセサ
	$self->{WORLD_ACCESSOR_INTERFACE} = WorldAccessor->new(); 

	bless ($self, $class);

	return $self;
}
#######################################
# テストから呼び出される関数
#######################################

#./log/countries.cgiの世界情報に直接アクセスして
#$w{}のデータを読み書きする
sub access_data{

	my $self = shift;
	$self->{WORLD_ACCESSOR_INTERFACE}->access_data(@_);
}

#災害を起こす
sub evoke_disaster{

	my $self = shift;
	my $more_switch= shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	#災害を起こす
	eval{
		$self->{WORLD_ACCESSOR_INTERFACE}->evoke_disaster($more_switch);
	};
	if($@){
		die ("$error_info : failed to evoke disaster\n");
	}

}

1;
