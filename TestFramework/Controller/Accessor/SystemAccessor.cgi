#############################################
# サーバーの時間、ファイル操作などのアクセサ
#############################################

package SystemAccessor;
use lib qw(./TestFramework/lib);
use Test::MockTime qw( :all );
use File::Copy qw(copy);
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


#ファイル/ディレクトリの移動
#移動先に同名フォルダがあれば削除してから移動
sub move_data{

	my $self = shift;
	my $src_path = shift;
	my $dst_path = shift;


	unless((defined $src_path) or (defined $dst_path)){
		die("SystemAccessor::move_data needs src_path and dst_path");
	}

	#ディレクトリの場合
	if(-d $src_path){
		if(-d $dst_path){
			rmtree($dst_path);
		}
		dircopy($src_path, $dst_path) or die $!;

		#退避元を削除する
		unless(rmtree($src_path)){
			die ("failed to rmtree($src_path)\n");
		}
	}
	#ファイルの場合
	elsif(-f $src_path){
		if(-f $dst_path){
			unless(unlink $dst_path){
				die("failed to delete $dst_path\n");
			}
		}
		copy($src_path, $dst_path) or die $!;

		#退避元を削除する
		unless(unlink $src_path){
			die("failed to delete $src_path\n");
		};

	}
	else{
		die("Couldn't identify $src_path\n");
	}

}

#ディレクトリ/ファイルのコピー
#コピー先に同名ディレクトリ/ファイルがあれば削除してからコピーする
sub copy_data{

	my $self = shift;
	my $src_path = shift;
	my $dst_path = shift;

	#ディレクトリの場合
	if(-d $src_path){
		if(-d $dst_path){
			rmtree($dst_path);
		}
		dircopy($src_path, $dst_path) or die $!;
	}
	#ファイルの場合
	elsif(-f $src_path){
		if(-f $dst_path){
			unless(unlink $dst_path){
				die("failed to delete $dst_path\n");
			}
		}
		copy($src_path, $dst_path);
	}
	else{
		die("Couldn't identify $src_path\n");
	}

}


1;
