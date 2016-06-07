###############################################################################
# システム時刻の偽装など
# システム時刻の偽装に関する関数はtime,localtimeなどの返り値を偽装し、単位は秒
###############################################################################

package SystemController;
use File::Path qw(make_path rmtree);
use File::Copy qw(copy);
use File::Copy::Recursive qw(fcopy dircopy);
require "./TestFramework/Controller/Accessor/SystemAccessor.pm";


sub new {

	my $class = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";


	#callしたファイルのパス＋行数で退避ディレクトリを生成
	#cdからの相対ディレクトリなら先頭の./を削除、またファイルネーム中の.は全て削除する
	#最終的にはdirname/child_direnameの形に変換
	$caller_filename =~ s/^\.\///;
	$caller_filename =~ s/\.//g;

	my $savedir = "./".$caller_filename.$caller_num_line;
	$self = {};

	#システムのアクセサ
	$self->{SYSTEM_ACCESSOR} = SystemAccessor->new();

	#システム時刻の偽装の状態
	use constant TIME_NATURAL => 0;
	use constant TIME_CHANGED => 1;
	use constant TIME_FIXED => 2;
	$self->{TIME_TYPE} = TIME_NATURAL;

	return bless ($self, $class);

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

1;
