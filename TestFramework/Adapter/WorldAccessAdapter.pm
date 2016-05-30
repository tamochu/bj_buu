#use strict;
use warnings;

package WorldAccessAdapter;

use lib qw(./Accessor);
require WorldAccessor;

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

#./log/countries.cgiの世界情報に直接アクセスして取得/変更
sub access_data{
}
