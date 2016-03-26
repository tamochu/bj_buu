#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
my $this_script = 'cataso_ratio.cgi';
#=================================================
# ¶À~ÉŠÇ—
#=================================================

#=================================================
# ƒƒCƒ“ˆ—
#=================================================
&header2;
&decode;
&error('pass error' . $in{pass}) unless $in{pass} eq $cataso_pass;
&run;
&footer2;
exit;

#=================================================
# ˆ—
#=================================================
sub run {
	if ($in{target} ne '' && $in{compare} ne '' && $in{value} ne '' && $in{target} ne $in{compare}) {
		my $pid = unpack 'H*', $in{target};
		my $value = $in{value};
		if (-f "$userdir/$pid/user.cgi") {
			open my $fh, ">> $userdir/$pid/cataso_res.cgi";
			my $eid = unpack 'H*', $in{compare};
			print $fh "$eid<>$value<>\n";
			close $fh;
		}
	}
	if ($in{player_line}) {
		my @members = ();
		push @members, "header<>\n";
		
		open my $fh, "> $logdir/chat_casino_cataso_member.cgi" or &error('ÒÝÊÞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
		for my $name (split /<>/, $in{player_line}) {
			push @members, "$time<>$name<><>\n";
		}
		print $fh @members;
		close $fh;
	}
}

sub header2 {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	
print << "HTML";
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<title>result</title>
</head>
<body>
HTML
}

sub footer2 {
	print qq|</body></html>|;
}
