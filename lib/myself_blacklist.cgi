#================================================
# ﾌﾟﾛﾌｨｰﾙ設定 Created by Merino
#================================================

#================================================
sub begin {
	$layout = 2;

	unless (-f "$userdir/$id/blacklist.cgi") {
		open my $fh, "> $userdir/$id/blacklist.cgi" or &error("$userdir/$id/blacklist.cgiﾌｧｲﾙが開けません");
		close $fh;
	}
	open my $fh, "< $userdir/$id/blacklist.cgi" or &error("$userdir/$id/blacklist.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($blackname) = split /<>/, $line;
		$mes .= qq|<form>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="hidden" name="mode" value="delete">|;
		$mes .= qq|<input type="hidden" name="delname" value="$blackname">|;
		$mes .= qq|<p>$blackname<input type="submit" value="削除する" class="button1"></p></form><br>|;
	}
	close $fh;

	$mes .= qq|<form>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="mode" value="add">|;
	$mes .= qq|<input type="text" name="addname">|;
	$mes .= qq|<p><input type="submit" value="追加する" class="button1"></p></form>|;
	&n_menu;
}

sub tp_1 {
	if ($in{mode} eq 'add') {
		my $addid = unpack 'H*', $in{addname};
		if (-f "$userdir/$addid/user.cgi") {
			open my $fh, ">> $userdir/$id/blacklist.cgi" or &error("$userdir/$id/blacklist.cgiﾌｧｲﾙが開けません");
			print $fh "$in{addname}<>\n";
			close $fh;
		}
		&begin;
	} elsif ($in{mode} eq 'delete') {
		my @lines = ();
		open my $fh, "+< $userdir/$id/blacklist.cgi" or &error("$userdir/$id/blacklist.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($blackname) = split /<>/, $line;
			if ($blackname eq $in{delname}) {
				next;
			}
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		&begin;
	} else {
		$mes .= 'やめました<br>';
		&refresh;
	}
	&n_menu;
}


1; # 削除不可
