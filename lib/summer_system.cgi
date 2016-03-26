require './lib/jcode.pl';
#================================================
# Ò²İ‚Å‚æ‚­g‚¤ˆ—
#================================================
sub read_summer { # Get %s
	$mid   = $in{id} || unpack 'H*', $in{login_name};
	%s = ();
	
	unless (-f "$userdir/$mid/summer.cgi") {
		open my $fh, "> $userdir/$mid/summer.cgi";
		close $fh;
	}
	open my $fh, "< $userdir/$mid/summer.cgi" or &error("‚»‚Ì‚æ‚¤‚È–¼‘O$in{login_name}‚ÌÌßÚ²Ô°‚ª‘¶İ‚µ‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$s{$k} = $v;
	}
	$s{dummy} = 1;
}
1; # íœ•s‰Â
