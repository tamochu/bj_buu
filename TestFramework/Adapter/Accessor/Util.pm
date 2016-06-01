###########################################
#複数のクラスから呼ばれるユーティリティー
############################################

package Util;
require './Jcode.pm';

#無名サブルーチンをフォークした先で実行する
sub fork_sub{

	use Socket;
	use IO::Handle;

	socketpair(PARENT, CHILD, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or die;
	select(PARENT);$|=1;
	select(CHILD);$|=1;
	CHILD->autoflush(1);
	PARENT->autoflush(1);
	select(STDOUT);	

	#ソケットに改行文字が含まれているとprintした時に通信がそこで終わってしまうので
	#改行を文字に置き換えて通信した後に戻すためのマーク
	my $mark = "replacement_for_cl";

	# 親プロセス
	if (my $pid = fork) {
	    my $line = "";
	    close PARENT;
	    chomp($line = <CHILD>);
	    close CHILD;

	    #改行を元に戻す
	    $line =~ s/$mark/\n/;

	    if($line =~ /^exception/){
		    die "$line";
	    }

	    waitpid($pid,0);
	    return $line;
	}
	#子プロセス
	elsif (defined $pid) {
	    my $sub_routine = shift;
	    close CHILD;

	    #サブルーチン実行
	    my $line = "";
	    my $message ="";

	    eval{
		    $message = $sub_routine->();
	    };

	    if($@){
		$line .= "exception was thrown in the forked process\n";
		$line .= $@; 
		$line =~ s/\n/$mark/;
	    }

	    $line .= $message;
	    #親にソケット通信でメッセージ送信
	    print PARENT $line;
	    close PARENT;
	    exit;
	}

}

1;
