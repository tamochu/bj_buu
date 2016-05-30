################################
#サーバーのシステムにアクセスする
################################

package SystemAccessAdapter;

use lib qw(./Accessor);
require SystemAccessor;

sub new {
	my $class = shift;
	my $self = {};
	return bless ($self, $class);
}

#systemのlocaltimeを変更する
sub change_systime{
	
	my $self = shift;
	my $diff = shift;

}
