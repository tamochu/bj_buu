###########################################
#複数のクラスから呼ばれるユーティリティー
############################################

package Util;
#無名サブルーチンをフォークした先で実行する
sub fork_sub{

	use Socket;

	socketpair(PARENT, CHILD, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or die;
	select(PARENT);$|=1;
	select(CHILD);$|=1;
	select(STDOUT);	

	my $pid = fork;
	if ($pid ne 0) {
	    # 親プロセス
	    my $line = "";
	    close PARENT;
	    $line =  ($_ = <CHILD>);
	    close CHILD;
	    wait;
	    return $line;
	}
	elsif (defined $pid) {
	    my $sub_routine = shift;
	    # 子プロセス
	    close CHILD;
	    my $line = $sub_routine->();
	    print PARENT $line;
	    close PARENT;
	    exit;
	}

}


1;
