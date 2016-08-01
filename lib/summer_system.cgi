require './lib/jcode.pl';
#================================================
# ﾒｲﾝでよく使う処理
#================================================
sub read_summer { # Get %s
	return unless &on_summer;
	$mid   = $in{id} || unpack 'H*', $in{login_name};
	# ???
	# %s を summer.cgi に書き込む処理がどこにもなく常に空っぽが読み込まれる
	# system_game.cgi の write_user に write_summer 的な処理を追加した
	# %sと%mとで重複する可能性はあるが、そもそも $s{hoge} を参照していないので $m{hoge} に統一
#	%s = ();
	
	unless (-f "$userdir/$mid/summer.cgi") {
		open my $fh, "> $userdir/$mid/summer.cgi";
		close $fh;
	}
	open my $fh, "< $userdir/$mid/summer.cgi" or &error("そのような名前$in{login_name}のﾌﾟﾚｲﾔｰが存在しません");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$m{$k} = $v; # $s
	}
	$m{dummy} = 0; # $s
}
1; # 削除不可
