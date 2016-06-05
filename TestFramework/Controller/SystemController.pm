###############################################################################
# システム時刻の偽装やファイルの保存、復元など
# システム時刻の偽装に関する関数はtime,localtimeなどの返り値を偽装し、単位は秒
###############################################################################

package SystemController;
use File::Path qw(make_path);

require "./TestFramework/Controller/Accessor/SystemAccessor.pm";


sub new {

	my $class = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";


	#callしたファイル名＋行数で退避ディレクトリを生成
	$caller_filename =~ s/\.//g;
	my $savedir = ".".$caller_filename.$caller_num_line;

	$self = {};

	#システムのアクセサ
	$self->{SYSTEM_ACCESSOR} = SystemAccessor->new();

	#データのセーブロード
	$self->{SAVE_DIR} = $savedir; #ファイル/ディレクトリの退避ディレクトリ
	$self->{SAVED_PATH} = []; #セーブされたファイルまたはディレクトリの元のパス/移動後のパス

	#システム時刻の偽装の状態
	use constant TIME_NATURAL => 0;
	use constant TIME_CHANGED => 1;
	use constant TIME_FIXED => 2;
	
	$self->{TIME_TYPE} = TIME_NATURAL;



	return bless ($self, $class);

}

sub DESTROY{

	my $self = shift;

	#退避していたデータを復元
	$self->restore();

	#セーブフォルダ削除
	rmdir $self->{SAVE_DIR};

	#システム自国を元に戻す
	$self->restore_time();

}

#systemのtimeを固定にする
sub fix_time{

	my $self = shift;
	my $sec = shift;
#	$self->{SYSTEM_ACCESSOR}->restore_time();
	$self->{SYSTEM_ACCESSOR}->fix_time($sec);
	$self->{TIME_TYPE} = TIME_FIXED;
}

#システムの時刻を再設定する
sub set_time{

	my $self = shift;
	my $time = shift;
	$self->{SYSTEM_ACCESSOR}->set_time($time);
	$self->{TIME_TYPE} = TIME_CHANGED;


}

#systemのtimeを引数で指定された秒前進させる
#状態がTIME_CHANGEDでもTIME_FIXでも、TIME_NATURALでも作用する
sub advance_time{
	
	my $self = shift;
	my $diff = shift; 
	
	if($self->{TIME_TYPE} eq TIME_NATURAL){
		$self->{TIME_TPYE} = TIME_CHANGED;
		$self->{SYSTEM_ACCESSOR}->change_time($diff);

	}
	elsif($self->{TIME_TYPE} eq TIME_CHANGED){
		my $current_time = time;
		$current_time += $diff;
		$self->{SYSTEM_ACCESSOR}->set_time($current_time);
	}
	elsif($self->{TIME_TYPE} eq TIME_FIXED){

		#timeは固定された時刻を返す
		my $current_time = time;
		$current_time = $current_time + $diff;
		$self->{SYSTEM_ACCESSOR}->fix_time($current_time);
	}
}

#systemのtimeを通常のものに戻す
sub restore_time{
	
	my $self = shift;
	$self->{SYSTEM_ACCESSOR}->restore_time();
	$self->{TIME_TYPE} = TIME_NATURAL;
}

#ディレクトリを退避
sub save_dir{

	my $self = shift;
	my $src_path = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	(-e $src_path) or die ("$error_info : $src_path does not exist");

	#カレントはcurrentに変換
	my $save_path = $src_path;
	$save_path =~ s/\.//;
	print "***save_path = $save_path***\n";
	print "***self->{SAVE_DIR} = $self->{SAVE_DIR}***\n";

	#保存先
	my $dst_path = $self->{SAVE_DIR}.$save_path;

	my $set = [ $src_path, $dst_path ];
	push(@{$self->{SAVED_PATH}}, $set);

	print "***set = $set->[0], $set->[1]***\n";
	print "***$self->{SAVED_PATH}->[0]->[0]***\n";
	print "***src = $src_path***\n***dst = $dst_path***\n";
	print "***self->{SAVE_DIR} = $self->{SAVE_DIR}***\n";
	unless ($self->{SYSTEM_ACCESSOR}->move($src_path, $dst_path)){
		die ("$error_info : failed to save $src_path");
	}
	
}


#ファイル/フォルダの復元
sub restore{

	my $self = shift;
	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	for my $set (@{$self->{SAVED_PATH}}){
		print "set =  $set->[1]  to $set->[0]\n";
		unless($self->{SYSTEM_ACCESSOR}->move($set->[1], $set->[0])){
			die ("$error_info : failed to restore $set->[1] to $set->[0]");
		}
	}

	#再初期化
	$self->{SAVED_PATH} = [];
}
1;
