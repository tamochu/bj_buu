#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# index Created by Merino
#================================================

&header2;
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
	open my $fh, "+< $logdir/login.cgi" or &error('ﾛｸﾞｲﾝﾘｽﾄが開けません');
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

sub header2 {
	print "Content-type: text/html; charset=Shift_JIS\n";
	if ($gzip ne '' && $ENV{HTTP_ACCEPT_ENCODING} =~ /gzip/){  
		if ($ENV{HTTP_ACCEPT_ENCODING} =~ /x-gzip/) {
			print "Content-encoding: x-gzip\n\n";
		}
		else{
			print "Content-encoding: gzip\n\n";
		}
		open STDOUT, "| $gzip -1 -c";
	}
	else {
		print "\n";
	}
	
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	print qq|<meta name="robots" content="none">|;
	unless ($is_mobile) {
		print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
		print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">|;
		print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/bj.js?$jstime"></script>\n|;
		&load_RWD;
#		if ($is_smart) {
#			print qq|<meta name="viewport" content="width=device-width">|;
#			print qq|<meta name="viewport" content="width=device-width, maximum-scale=1.5, minimum-scale=0.5,user-scalable=yes,initial-scale=0.9" />|;
#			print qq|<link rel="stylesheet" media="screen and (max-width: 480px)" href="$htmldir/smart.css" />|;
#			print qq|<link rel="stylesheet" media="screen and (min-width: 481px)" href="$htmldir/tablet.css" />|;
#			print qq|<link rel="stylesheet" media="screen and (min-width: 481px) and (max-width: 720px)" href="$htmldir/tablet.css?$jstime" />|;
#		}
	} else {
		# ガラケーで外部CSSの読み込みはNG
		# HTMLファイルを読み込んだ後にCSSファイルを読み込むため、
		# 素のHTMLが表示された後にCSSが適用され画面がチラつくなどの問題がある
		print qq|<style type="text/css"><!-- a.clickable_name {color: inherit; text-decoration: none;} --></style>|;
	}
#	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
	print qq|</head><body $body><h1><a name="top">$title</a></h1>|;
}
