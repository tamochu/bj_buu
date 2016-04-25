my %action_weight = (
    dom => 0.8,
    pro  => 1.0,
    mil  => 1.0,
    war  => 1.1
);

#================================================
# 行動ログの書き込み
#================================================
sub write_action_log {
	my ($action_type, $wait_time) = @_;
	my $key = $action_type."_".$wait_time;
	my %action_log = ($key => 1);
	my $nline = "";
	my $fh;

	if (-e "$userdir/$id/action_log.cgi") {
		open $fh, "+< $userdir/$id/action_log.cgi" or &error("action_log.cgiが開けません");
		my $line = <$fh>;
		$line =~ tr/\x0D\x0A//d;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$action_log{$k} += $v;
		}
		for my $k (keys(%action_log)) {
			$nline .= "$k;$action_log{$k}<>";
		}

		seek $fh, 0, 0;
		truncate $fh, 0;
	}
	else {
		open $fh, "> $userdir/$id/action_log.cgi" or &error("action_log.cgiが開けません");
		$nline = "$key;1<>";
	}

	print $fh "$nline";
	close $fh;
}

#================================================
# 行動ログを国へ計上する
#================================================
sub add_action_log_country {
#	my ($action_type, $wait_time) = @_;
#	return 0 unless -e "$userdir/$id/action_log.cgi";

#	my @actions = ("dom_12", "dom_20", "dom_40");
	&read_user;
	my %action_log;
	my $line = "";
	my $nline = "";

	open my $fh1, "< $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
	$line = <$fh1>;
	$line =~ tr/\x0D\x0A//d;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} += $v;
	}
	close $fh1;

	open my $fh2, "< $userdir/$id/action_log.cgi" or &error("action_log.cgiが開けません");
	$line = <$fh2>;
	$line =~ tr/\x0D\x0A//d;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} += $v;
	}
	close $fh2;

	for my $k (keys(%action_log)) {
		$nline .= "$k;$action_log{$k}<>";
	}

	open my $fh1, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
	eval { flock $fh1, 2; };
	print $fh1 "$nline";
	close $fh1;

	open my $fh2, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
	print $fh2 "";
	close $fh2;
}

1;