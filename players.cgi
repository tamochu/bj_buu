#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# ÌßÚ²Ô°ˆê——ÐÆ(Œg‘Ñ—p) Created by Merino
#================================================

&decode;
&header;
&read_cs;
&run;
&footer;
exit;

#================================================
sub run {
	$in{country} ||= 0;
	$in{country} = int($in{country});
	$in{country} = 0 if $in{country} > $w{country};

	print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	for my $i (0 .. $w{country}) {
		print $i eq $in{country} 
			? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / |
			: qq|<a href="?country=$i"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |
			;
	}
	print qq|<hr><h1><a href="$htmldir/$in{country}_chart.html">$cs{name}[$in{country}]</a>‚Ì—EŽm’B</h1><hr><ul>|;
	
	open my $fh, "< $logdir/$in{country}/member.cgi" or &error("$logdir/$in{country}/member.cgiÌ§²Ù‚ª“Ç‚Ýž‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my $id = unpack 'H*', $line;
		print qq|<li><a href="profile.cgi?id=$id&country=$in{country}">$line</a></li>|;
	}
	close $fh;
	print qq|</ul>|;
}
