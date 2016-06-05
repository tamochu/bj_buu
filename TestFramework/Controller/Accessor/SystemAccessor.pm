#############################################
# サーバーの時間、ファイル操作などのアクセサ
#############################################

package SystemAccessor;
use lib qw(./TestFramework/lib);
use Test::MockTime qw( :all );
use File::Copy 'move';
use File::Copy::Recursive qw(fcopy dircopy);
use File::Path 'rmtree';

sub new {
	
	my $class = shift;
	my $self = {};

	return bless($self, $class);

}

#システムのtimeを進めたり戻したりするように見せかける
#単位は秒
sub change_time{
	my $self = shift;
	my $sec = shift;
	Test::MockTime::set_relative_time($sec);
}

#システムのtimeを指定した時刻に変更する
#単位は秒
sub set_time{
	my $self = shift;
	my $sec = shift; 
	Test::MockTime::set_absolute_time($sec);
}

#システムのtimeを指定した時刻で固定する
#単位は秒
sub fix_time{
	my $self = shift;
	my $sec = shift; 
	Test::MockTime::set_fixed_time($sec);

}

#システムのtimeを元に戻す
sub restore_time{
	my $self = shift;
	Test::MockTime::restore();
}


#ディレクトリの移動
sub move{

	my $self = shift;
	my $src_path = shift;
	my $dst_path = shift;

	if(-d $src_path){
		dircopy($src_path, $dst_path) or die $!;
		rmtree($src_path);
	}
	else{
		die("Couldn't identify $src_path");
	}

}

1;
