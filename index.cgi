#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# index Created by Merino
#================================================

&header;
&read_cs;

$is_mobile ? require './lib/template_mobile_index.cgi' :
	$is_smart ? require './lib/template_smart_index.cgi' :
	require './lib/template_pc_index.cgi';
&index(&get_login_member);

&footer;
exit;

#================================================
sub get_login_member {
	my @lines = ();
	my %cs_c  = ();
	my %sames = ();
	my $list  = '';
	open my $fh, "+< $logdir/login.cgi" or &error('Û¸Þ²ÝØ½Ä‚ªŠJ‚¯‚Ü‚¹‚ñ');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($ltime, $name, $country, $shogo, $message, $icon) = split /<>/, $line;
		next if $time > $ltime + $login_min * 60;
		next if ++$sames{$name} > 1;
		
		if ($is_mobile || $is_smart) {
			$list .= qq|<font color="$cs{color}[$country]">$name</font>,|;
		}
		else {
			my $yid = unpack 'H*', $name;
			$icon  = $icon ? qq|<img src="$icondir/$icon" style="width: 25px;">| : '';
			$name .= $shogo ? "[$shogo][$cs{name}[$country]]" : "[$cs{name}[$country]]";
			$list .= qq|<div style="color: $cs{color}[$country]; border-bottom: 1px solid $cs{color}[$country];"><a href="profile.cgi?id=$yid&country=$country" style="color: $cs{color}[$country]; text-decoration: none;">$icon$name</a>/$message</div>\n|;
		}
		
		$cs_c{$country}++;
		$cs_c{all}++;
		push @lines, $line;
	}
	seek $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	return ($list, %cs_c);
}


