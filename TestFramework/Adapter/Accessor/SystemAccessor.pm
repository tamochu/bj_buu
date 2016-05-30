#############################################
# サーバーの時間、ファイル操作などのアクセサ
#############################################

package SystemAccessor;

sub new {
	
	my $class = shift;
	my $self = shift;

	return bless($self, $class);

}

#システムのlocaltimeを偽装
sub change_localtime{
}
	my $self = shift;

#ファイルの保存
sub save_file{
	my $self = shift;
}

#ファイルの復元
sub load_file{
}
	my $self = shift;
