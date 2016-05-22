#!/usr/local/bin/perl --
require './lib/system.cgi';
require './lib/move_player.cgi';
use File::Copy;
#================================================
# ÌßÚ²Ô°ˆê——HTMLì¬ + ŠúŒÀØ‚êÌßÚ²Ô°íœ
# & Cookie¾¯Ä(PC‚Ì‚İ) Created by Merino
#================================================

# ÌßÚ²Ô°ˆê——HTMLXVüŠú(“ú) 1“ú`
my $update_cycle_day = 1;

# Cookie•Û‘¶ŠúŠÔ(“ú)
my $limit_cookie_day = 30;


#================================================
&decode;
$in{is_cookie} ? &set_cookie($in{login_name},$in{pass},1) : &del_cookie unless $is_mobile;
require 'bj.cgi';

# “ˆêÒ‚ ‚ç‚í‚ê‚¸
if ($time > $w{limit_time}) {
	require './lib/reset.cgi';
	&time_limit;
}

#&summary_contribute;

# htmlÌ§²Ùì¬ & ŠúŒÀØ‚êÌßÚ²Ô°íœ
for my $i (0 .. $w{country}) {
	if (-M "./html/$i.html" >= $update_cycle_day) {
#	if (-M "./html/$i.html" >= 0) {
		&write_players_html($i);
		last;
	}
}

my $chart_time = (stat "./html/char_img.html")[9];
if($chart_time < $time - 3600){
	&chart_backup;
}

if (-M "./html/all.html" >= $update_cycle_day) {
#if (-M "./html/$i.html" >= 0) {
	&write_all_players_html;
	&backup_players;
}
&make_player_name_list;
#&refresh_new_commer;

exit;

#=================================================
# ¸¯·°¾¯Ä
#=================================================
sub set_cookie {
	my @cooks = @_;

	local($csec,$cmin,$chour,$cmday,$cmon,$cyear,$cwday) = gmtime(time + $limit_cookie_day * 24 * 60 * 60); # 24ŠÔ * 60•ª * 60•b
	local @mons = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	local @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	local $expirese_time = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$cwday],$cmday,$mons[$cmon],$cyear+1900,$chour,$cmin,$csec);

	for my $c (@cooks) {
		$c =~ s/(\W)/sprintf("%%%02X", unpack "C", $1)/eg;
		$cook .= "$c<>";
	}

	print "Set-Cookie: bj=$cook; expires=$expirese_time\n";
}

# ------------------
# ¸¯·°íœ
sub del_cookie {
	my $expires_time = 'Thu, 01-Jan-1970 00:00:00 GMT';
	print "Set-Cookie: bj=dummy; expires=$expires_time\n";
}


#=================================================
# ‘‚²‚Æ‚ÌhtmlÌ§²Ùì¬
#=================================================
# •\¦‚·‚é€–Ú‚ğ‘Œ¸‚·‚éê‡‚ÍA@rows ‚Æ 130s–Úü•Ó‚ğ•ÒW‚µ‚Ä‚Ë

sub write_players_html {
	my $country = shift;

	my @rows = (qw/–¼‘O «•Ê ŠK‹‰ •”‘à E‹Æ í‘° •Ší ÀÏºŞ Íß¯Ä ¢‘ã Lv HP MP AT DF MAT MDF AG LEA CHA ‚¨‹à º²İ XVŠÔ Ò¯¾°¼Ş ŠJn“ú/);

	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;

	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	open my $fh, "< $logdir/$country/member.cgi";
	while (my $player = <$fh>) {
		$player =~ tr/\x0D\x0A//d;
		
		# “¯‚¶–¼‘O‚Ìl‚ª•¡”‚¢‚éê‡
		next if ++$sames{$player} > 1;

		my $player_id = unpack 'H*', $player;

		# ‘¶İ‚µ‚È‚¢ê‡‚ÍØ½Ä‚©‚çíœ
		unless (-f "$userdir/$player_id/user.cgi") {
			&move_player($player, $country, 'del');
			next;
		}

		my %p = &get_you_datas($player_id, 1);
		
		# íœŠúŒÀ‚É‚È‚è©“®íœ
		if ($time > $p{ltime} + $auto_delete_day * 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			# ©“®íœ‰„–½Íß¯Ä‚ğ‘•”õ‚µ‚Ä‚¢‚é‚È‚ç©“®íœ“ú{24“ú‚Ííœ‚µ‚È‚¢
			if ($pets[$p{pet}][2] eq 'life_up') {
				if ($time > $p{ltime} + ($auto_delete_day + 30) * 3600 * 24) {
					&move_player($player, $country, 'del');
					next;
				}
			}
			else {
				&move_player($player, $country, 'del');
				next;
			}
		}
		# Á×Œ©‚¾‚¯‚Ìl(‚P¢‘ã–Ú‚ÌƒŒƒxƒ‹‚P)‚ğ‚T“ú–Ú‚Åíœ
		elsif ($p{lv} <= 1 && $p{sedai} <= 1 && $time > $p{ltime} + 3600 * 24 && $player ne $admin_name && !$p{delete_shield}) {
			&move_player($player, $country, 'del');
			next;
		}
		# ÊŞ¸Ş‚È‚Ç‚Åˆá‚¤‘‚Ìl‚ªŠ‘®‚µ‚Ä‚¢‚éê‡
		elsif ($p{country} ne $country) {
			&move_player($player, $country, $p{country});
			next;
		}
		
		my $name = $p{name};
		$name .= "[$p{shogo}]" if $p{shogo};
		
		my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..4];
		$start_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);

#		$html .= $count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
		my $rank_name = &get_rank_name($p{rank}, $p{name});
		$html .= qq|<tr>|;
		$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
		$html .= qq|<td>$sexes[$p{sex}]</td>|;
		$html .= qq|<td>$rank_name</td>|;
		$html .= qq|<td>$units[$p{unit}][1]</td>|;
		$html .= qq|<td>$jobs[$p{job}][1]</td>|;
		$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
		$html .= qq|<td>$weas[$p{wea}][1]</td>|;
		$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
		$html .= qq|<td>$pets[$p{pet}][1]</td>|;
		$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
		$html .= qq|<td>$p{ldate}</td>|;
		$html .= qq|<td>$p{mes}</td>|;
		$html .= qq|<td>$start_date</td>|;
		$html .= qq|</tr>\n|;
		
		# “Œv
		++$ranks{$p{rank}};
		++$weas{$weas[$p{wea}][2]};
		++$jobs{$p{job}};
		++$_seeds{$p{seed}};
		++$sexes{$p{sex}};
		++$units{$p{unit}};
		++$count;
	}
	close $fh;
	$html .= qq|</tbody></table>|;
	
	# Š‘®l”•â³
	$cs{member}[$country] = $count;

	if ($country eq '1') {
		$w{playing} = int($w{playing} * 0.9); # S‘©“ü‚ç‚¸—‚¿‚él‚ğl—¶‚µ‚Ä­‚µŒ¸‚ç‚·
	}

	&write_cs if $country > 0;

	# “ŒvHTML
	my $html_chart  = $w{world} eq $#world_states && $country eq $w{country} ? qq|<hr size="1"><h1>$cs{name}[$country] ‚Ìˆ«–‚’B</h1>| : qq|<hr size="1"><h1>$cs{name}[$country] ‚Ì—Em’B</h1>|;
	   $html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>Š‘®l”</th><td>$countl|;

	$html_chart .= qq|<br></td></tr><tr><th>«•Ê</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}l/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>ŠK‹‰</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>•”‘à</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>•Ší‘®«</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>E‹Æ</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>í‘°</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}
	
	$html_chart .= qq|<br></td></tr></table><br>|;
	
	# HTMLÌ§²Ùì¬
	open my $out, "> ./html/$country.html";
	print $out &header_players_html($country);
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;
	
	# Œg‘Ñ—p‚É“ŒvHTMLo—Í
	open my $out2, "> ./html/${country}_chart.html";
	print $out2 &header_chart_html($country);
	print $out2 $html_chart;
	print $out2 &footer_players_html;
	close $out2;
}

sub write_all_players_html {
	my @rows = (qw/–¼‘O «•Ê ŠK‹‰ •”‘à E‹Æ í‘° •Ší ÀÏºŞ Íß¯Ä ¢‘ã Lv HP MP AT DF MAT MDF AG LEA CHA ‚¨‹à º²İ XVŠÔ Ò¯¾°¼Ş ŠJn“ú/);
	
	my $html = '';
	$html .= qq|<table class="tablesorter"><thead><tr>|;
	$html .= qq|<th>$_</th>| for (@rows);
	$html .= qq|</tr></thead><tbody>|;
	
	my %sames = ();
	my %ranks = ();
	my %weas  = ();
	my %jobs  = ();
	my %_seeds  = ();
	my %sexes = ();
	my %units = ();
	my $count = 0;
	for my $country (0..$w{country}){
		open my $fh, "< $logdir/$country/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;

			# “¯‚¶–¼‘O‚Ìl‚ª•¡”‚¢‚éê‡
			next if ++$sames{$player} > 1;

			my $player_id = unpack 'H*', $player;


			my %p = &get_you_datas($player_id, 1);

			my $name = $p{name};
			$name .= "[$p{shogo}]" if $p{shogo};
		
			my($min,$hour,$mday,$mon,$year) = (localtime($p{start_time}))[1..4];
			$start_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);

			my $rank_name = &get_rank_name($p{rank}, $p{name});
			$html .= qq|<tr>|;
			$html .= qq|<td><a href="../profile.cgi?id=$player_id&country=$country">$name</a></td>|;
			$html .= qq|<td>$sexes[$p{sex}]</td>|;
			$html .= qq|<td>$rank_name</td>|;
			$html .= qq|<td>$units[$p{unit}][1]</td>|;
			$html .= qq|<td>$jobs[$p{job}][1]</td>|;
			$html .= qq|<td>$seeds{$p{seed}}[0]</td>|;
			$html .= qq|<td>$weas[$p{wea}][1]</td>|;
			$html .= qq|<td>$eggs[$p{egg}][1]</td>|;
			$html .= qq|<td>$pets[$p{pet}][1]</td>|;
			$html .= qq|<td align="right">$p{$_}</td>| for (qw/sedai lv max_hp max_mp at df mat mdf ag lea cha money coin/);
			$html .= qq|<td>$p{ldate}</td>|;
			$html .= qq|<td>$p{mes}</td>|;
			$html .= qq|<td>$start_date</td>|;
			$html .= qq|</tr>\n|;

			# “Œv
			++$ranks{$p{rank}};
			++$weas{$weas[$p{wea}][2]};
			++$jobs{$p{job}};
			++$_seeds{$p{seed}};
			++$sexes{$p{sex}};
			++$units{$p{unit}};
			++$count;
		}
		close $fh;
	}
	$html .= qq|</tbody></table>|;

	# “ŒvHTML
	my $html_chart  = qq|<hr size="1"><h1>‘S‘‚Ì—Em’B</h1>|;
	$html_chart .= qq|<table class="table1" cellpadding="2"><tr><th>Š‘®l”</th><td>$countl|;

	$html_chart .= qq|<br></td></tr><tr><th>«•Ê</th><td>|;
	for my $k (sort { $a <=> $b } keys %sexes) {
		$html_chart .= qq|$sexes[$k] $sexes{$k}l/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>ŠK‹‰</th><td>|;
	for my $k (sort { $a <=> $b } keys %ranks) {
		$html_chart .= qq|$ranks[$k] $ranks{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>•”‘à</th><td>|;
	for my $k (sort { $a <=> $b } keys %units) {
		$html_chart .= qq|$units[$k][1] $units{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>•Ší‘®«</th><td>|;
	for my $k (sort { $a cmp $b } keys %weas) {
		$html_chart .= qq|$k $weas{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>E‹Æ</th><td>|;
	for my $k (sort { $a <=> $b } keys %jobs) {
		$html_chart .= qq|$jobs[$k][1] $jobs{$k}/|;
	}
	$html_chart .= qq|<br></td></tr><tr><th>í‘°</th><td>|;
	for my $k (sort { $a <=> $b } keys %_seeds) {
		$html_chart .= qq|$seeds{$k}[0] $_seeds{$k}/|;
	}
	
	$html_chart .= qq|<br></td></tr></table><br>|;
	
	# HTMLÌ§²Ùì¬
	open my $out, "> ./html/all.html";
	print $out &header_all_players_html;
	print $out $html_chart;
	print $out $html;
	print $out &footer_players_html;
	close $out;

}

# ------------------
sub header_players_html {
	my $country = shift;

my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / $cs{name}[$country]</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>
<p>XV“ú $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= $i eq $country
			? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / |
			: qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |
			;
	}
	
	$html .= qq|<a href="all.html"><font color="#ffffff">‘SƒvƒŒƒCƒ„[</font></a> / |;
	
	if ($is_backup_countries) {
		$html .= $country eq 'chart' ? qq|‘—ÍÁ¬°Ä / | : qq|<a href="chart_img.html">‘—ÍÁ¬°Ä</a> / |;
	}
	
	return $html;
}

sub header_all_players_html {
my $html =<<"EOM";
<html>
<head>
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" type="text/css" href="bj.css">
<title>$title / ‘SƒvƒŒƒCƒ„[</title>
<link rel="stylesheet" type="text/css" href="themes/green/style.css">
<script type="text/javascript" src="jquery-latest.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript">
<!--
	\$(document).ready(function() {
		\$(".tablesorter").tablesorter({
		widgets: ['zebra']
		});
	});
-->
</script>
</head><body $body>
<form action="../$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>
<p>XV“ú $date</p>
EOM


	for my $i (0 .. $w{country}) {
		$html .= qq|<a href="$i.html"><font color="$cs{color}[$i]">$cs{name}[$i]</font></a> / |;
	}
	
	$html .= qq|<font color="#ffffff">‘SƒvƒŒƒCƒ„[</font> / |;
	
	if ($is_backup_countries) {
		$html .= qq|<a href="chart_img.html">‘—ÍÁ¬°Ä</a> / |;
	}
	
	return $html;
}
# ------------------
sub chart_backup {
	# ÊŞ¯¸±¯Ìßˆ—
	if ($is_backup_countries && -d "./backup" && -s "$logdir/countries.cgi" > 300) {
		my @lines = ();
		open my $fh_b, "< $logdir/countries.cgi";
		while (my $line = <$fh_b>) {
			push @lines, $line;
		}
		close $fh_b;
		
		my($mhour,$wday) = (localtime($time))[2,6];
		my $hour_file = "./backup/" . $wday . "_" . $mhour . ".cgi";
		open my $fh_b2, "> $hour_file";
		print $fh_b2 @lines;
		close $fh_b2;
		
		my $del_start = $wday + 1;
		my $del_end = $wday + 6;
		
		for my $d ($del_start..$del_end){
			my $del_d = $d > 6 ? $d - 7 : $d;
			for my $h (0..23){
				my $hour_file = "./backup/" . $del_d . "_" . $h . ".cgi";
				if(-f "$hour_file"){
					unlink $hour_file;
				}
			}
		}
		
		&create_world_chart;
	}
}

sub header_chart_html {
	my $country = shift;

	my $html = '';
	$html .= qq|<html><head>|;
	$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	$html .= qq|<title>$title / $cs{name}[$country]</title>|;
	$html .= qq|</head><body $body>|;
	$html .= qq|<form method="$method" action="../$script_index"><input type="submit" value="‚s‚n‚o"></form>|;
	$html .= qq|<form method="$method" action="../players.cgi"><input type="submit" value="–ß‚é"></form>|;
	$html .= qq|<p>XV“ú $date</p>|;
	$html .= qq|<hr size="1"><h1>$cs{name}[$country]</h1>|;
	
	return $html;
}
# ------------------
sub footer_players_html {
	my $html = '';
	$html .= qq|<br><div align="right" style="font-size:11px">|;
	$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">AmaŠy.net</a><br>|;  # ’˜ì•\¦:íœE”ñ•\¦ ‹Ö~!!
	$html .= qq|$copyright|;
	$html .= qq|</div></body></html>|;
	
	return $html;
}


# ÊŞ¯¸±¯Ìß‚æ‚èÃŞ°À‚ğæ“¾
sub create_world_chart {
	$touitu_strong = 0 if ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10')); # ¢ŠEî¨[[•£]
	
	# ÊŞ¯¸±¯ÌßÌ§²Ù‚ğŒÃ‚¢‚à‚Ì‡‚É¿°Ä
	my @lines = ();
	opendir my $dh, "backup";
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		
		my $file_time = (stat "./backup/$file_name")[9];
		push @lines, "$file_name<>$file_time<>\n";
	}
	closedir $dh;

	@lines = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ]} @lines;
	
	# ‘—Í‚ğæ“¾
	my $chxl_x = '';
	my @chds = ();
	my $count_day = 0;
	for my $line (@lines) {
		my($file_name, $file_time) = split /<>/, $line;
		
		my $i = 1;
		open my $fh, "< ./backup/$file_name";
		my $head_line = <$fh>;
		while (my $data_line = <$fh>) {
			if ($data_line =~ /<>is_die;1<>/) {
				$chds[$i] .= "0,";
			}
			else {
				my($strong)    = ($data_line =~ /<>strong;(\d+?)<>/);
				my $strong_par = $strong <= 0 || $touitu_strong <= 0 ? 0 : int($strong / $touitu_strong * 100);
				$strong_par = 100 if $strong_par > 100;
				$chds[$i] .= "$strong_par,";
			}
			++$i;
		}
		close $fh;
		
		my($mhour,$mday,$month) = (localtime($file_time))[2,3,4];
		++$month;
		$chxl_x .= "|$month/$mday $mhour:00";
		
		++$count_day;
	}
	my $chg_x = $count_day <= 2 ? 25 : int(50 / ($count_day-1) * 100) * 0.01;
	
	my $name = '';
	my $chco = '';
	my $chd = '';
	for my $i (1 .. $w{country}) {
		$chco .= "$cs{color}[$i],";
		chop $chds[$i]; # Œã”ö‚Ì,‚ğ‚Æ‚é
		$chd  .= "$chds[$i]|";
		
		$name .= qq|<font color="$cs{color}[$i]">¡y “ˆê <b>$cs{win_c}[$i]</b> z$cs{name}[$i]</font><br>|;
	}
	$chco =~ tr/#//d; # #‚ğœ‚­
	chop $chco; # Œã”ö‚Ì,‚ğ‚Æ‚é
	chop $chd;  # Œã”ö‚Ì|‚ğ‚Æ‚é
	
	my $one_tenth = int($touitu_strong * 0.1);
	my $count_scale = 0;
	my $scale = 0;
	my $chxl_y = '';
	for my $i (1 .. 15) {
		$chxl_y .= "|$scale";
		$scale += int($one_tenth * 0.01) * 100;
		++$count_scale;
		last if $scale >= $touitu_strong*0.95;
	}
	$chxl_y .= "|$touitu_strong";
	$chg_y = $count_scale <= 0 ? 25 : int(100 / $count_scale * 100) * 0.01;
	
	my $html = qq|<hr size="1"><h1>$world_name‘å—¤‘—ÍÁ¬°Ä</h1>|;
	$html .= qq{<img src="http://chart.apis.google.com/chart?cht=lc&chs=500x350&chco=$chco}
		  .  qq{&chd=t:$chd&chxt=x,y,r&chxl=0:$chxl_x|1:$chxl_y|2:|Die|Harf|Win}
		  .  qq{&chg=$chg_x,$chg_y&chtt=World+Force+Chart&chf=c,lg,110,003366,0.7,000000,0|bg,s,CCCCCC">};

	my $limit_day = int( ($w{limit_time} - $time) / (3600 * 24) );
	$html .= qq|<p>$name</p>|;
	$html .= qq|$world_name—ïy $w{year}”N z/ ¢ŠEî¨y $world_states[$w{world}] z/ “ˆêŠúŒÀy c‚è$limit_day“ú z/<br>|;
	$html .= qq|“ïˆÕ“xy Lv.$w{game_lv} z/ “ˆê$e2j{strong}y $touitu_strong z/ | unless ($w{world} eq '10' || ($w{world} eq '19' && $w{world_sub} eq '10'));

	my($c1, $c2) = split /,/, $w{win_countries};
	$html .= $c2 ? qq|“ˆê‘y <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>“¯–¿ z<br>|
		   : $c1 ? qq|“ˆê‘y <font color="$cs{color}[$c1]">$cs{name}[$c1]</font> z<br>|
		   :       qq|<br>|
		   ;
	
	# HTMLÌ§²Ùì¬
	open my $out, "> ./html/chart_img.html";
	print $out &header_players_html('chart');
	print $out $html;
	print $out &footer_players_html;
	close $out;
}



sub backup_players {
	mkdir "./snap_shot/snap_shot_$time";
	opendir my $dh, "$userdir" or &error("Õ°»Ş°ÃŞ¨Ú¸ÄØ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my $user_from = "$userdir/$pid/user.cgi";
		my $user_to = "./snap_shot/snap_shot_$time/user_$pid.cgi";
		
		copy($user_from, $user_to);
	}
	closedir $dh;
	
	my $countries_from = "$logdir/countries.cgi";
	my $countries_to = "./snap_shot/snap_shot_$time/countries.cgi";
	copy($countries_from, $countries_to);
	
	opendir my $rdh, "./snap_shot" or &error("ÊŞ¯¸±¯ÌßÃŞ¨Ú¸ÄØ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $backup_name = readdir $rdh) {
		if ($backup_name =~ /snap_shot_(\d+)/) {
			if ($1 < $time - 3 * 24 * 60 * 60) {
				rmtree(["./snap_shot/$backup_name"]);
			}
		}
	}
	closedir $rdh;
}
