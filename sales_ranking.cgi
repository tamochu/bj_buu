#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# ”„ã×İ·İ¸Ş Created by Merino
#=================================================

# •\¦‚·‚é‚à‚Ì(./log/‚É‚ ‚é‚à‚Ì)@’Ç‰Á/•ÏX/íœ/•À‚×‘Ö‚¦‰Â”\
my @files = (
#	['À²ÄÙ',		'Û¸ŞÌ§²Ù–¼(shop_list_xxxx©‚Ì•”•ª)'],
	['¤l‚Ì‚¨“X',	'',			'ŒÂ'],
	['”ü‚Ì‰æ”ŒŠÙ',	'picture',	'–‡'],
	['ÌŞ¯¸Ï°¹¯Ä',	'book',		'û'],
	['¤l‚Ì‹âs',	'bank',		'‰ñ'],
);

# Å’áŒÀ•K—v‚È”„ã”(¤l‚Ì‚¨“X‚Ì‚İ)
my $min_sale_c = 5;


#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @files;
my $type = $files[$in{no}][1] ? "_$files[$in{no}][1]" : '';
my $flag_file = "$logdir/sales_ranking${type}_cycle_flag.cgi";
my $this_file = "$logdir/shop_list${type}.cgi";

&update_sales_ranking if -M $flag_file > $sales_ranking_cycle_day;
&run;
&footer;
exit;

#=================================================
# ×İ·İ¸Ş‰æ–Ê
#=================================================
sub run {
	my $flag_time = (stat $flag_file)[9];
	my($min, $hour, $mday, $month) = ( localtime( $flag_time + $sales_ranking_cycle_day * 24 * 3600) )[1..4];
	++$month;

	print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="casino_ranking.cgi">ˆá–@¶¼ŞÉ</a> / |;
	print qq|<h1>$files[$in{no}][0]”„ã×İ·İ¸Ş</h1>|;
	print qq|<div class="mes"><ul><li>×İ·İ¸Ş‚ÆŠe‚¨“X‚Ì”„ã‹à‚Æ”„ã”‚ÍA$sales_ranking_cycle_day“ú‚²‚Æ‚ÉØ¾¯Ä‚³‚êXV‚³‚ê‚Ü‚·|;

	if ($files[$in{no}][1] eq 'bank') {
		print "<li>XV‚ÌÀ²Ğİ¸Ş‚Åè‘±‰ñ”‚ª 0 ‰ñ‚Ì‹âs‚Í“|Y‚Æ‚È‚è‚Ü‚·";
		print "<li>XV‚ÌÀ²Ğİ¸Ş‚Å‘—a‹àŠz‚ª 100–œ G–¢–‚Ì‹âs‚Í“|Y‚Æ‚È‚è‚Ü‚·";
		print qq|<li>Ÿ‚ÌXVŠÔF$monthŒ$mday“ú$hour$min•ª</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>‡ˆÊ</th><th>—˜‰v</th><th>è‘±‚«</th><th>‹âs–¼</th><th>Œo‰cÒ</th><th>Ò¯¾°¼Ş</th></tr>| unless $is_mobile;
	}
	else {
		if ($files[$in{no}][1] eq '') {
			print qq|<li>XV‚ÌÀ²Ğİ¸Ş‚Å”„ã”‚ª $min_sale_cŒÂ–¢–‚Ì‚¨“X‚Í•Â“X‚Æ‚È‚è‚Ü‚·|;
		}
		else {
			print qq|<li>XV‚ÌÀ²Ğİ¸Ş‚Å”„ã‹à‚ª 0 G‚Ì‚¨“X‚Í•Â“X‚Æ‚È‚è‚Ü‚·|;
		}
		print qq|<li>Ÿ‚ÌXVŠÔF$monthŒ$mday“ú$hour$min•ª</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>‡ˆÊ</th><th>”„ã‹à</th><th>”„ã”</th><th>“X–¼</th><th>“X’·</th><th>Ò¯¾°¼Ş</th></tr>| unless $is_mobile;
	}
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while ($line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		print $is_mobile     ? qq|<hr><b>$rank</b>ˆÊ/$sale_money G/$sale_c$files[$in{no}][2]/$shop_name/$name/$message/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$rankˆÊ</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$rankˆÊ</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# ”„ã×İ·İ¸Ş‚ğXV
#=================================================
sub update_sales_ranking  {
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		$display = '' if $display ne '1';
		# ÊŞ¸Ş‚Å‚¨“X‚ª“ñ‚Â‚É‚È‚Á‚Ä‚¢‚é‚à‚Ì‚ğœ‚­
		next if ++$sames{$name} > 1;

		my $id = unpack 'H*', $name;
		next unless -f "$userdir/$id/shop${type}.cgi";
		
		open my $fh2, "+< $userdir/$id/shop_sale${type}.cgi";
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($m_sale_c, $m_sale_money, $m_update_t) = split /<>/, $line2;
		
		# ¤l‚Ì‹âsA‘—a‹àÁª¯¸
		if ($files[$in{no}][1] eq 'bank' && &is_the_end("$userdir/$id/shop${type}.cgi") ) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$name‚ÌŒo‰c‚·‚é$shop_name‚Í‘—a‹àŠz‚ª100–œ–¢–‚Ì‚½‚ß“|Y‚µ‚Ü‚µ‚½</b>", 1, $name);
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		# ”„ã‹à‚ª 0G ‚È‚çíœ
		elsif ($m_sale_money <= 0 && $m_update_t < $time - 24 * 3600 && !($files[$in{no}][1] eq '' && $guild_number)) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			
			if ($files[$in{no}][1] eq 'bank') {
				&write_send_news("<b>$name‚ÌŒo‰c‚·‚é$shop_name‚ÍŒo‰c”j’]‚Ì‚½‚ß“|Y‚µ‚Ü‚µ‚½</b>", 1, $name);
			}
			else {
				&write_send_news("<b>$name‚ÌŒo‰c‚·‚é$shop_name‚ÍŒo‰c”j’]‚Ì‚½‚ß•Â“X‚µ‚Ü‚µ‚½</b>", 1, $name);
			}
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		# ¤l‚Ì‚¨“X‚ÍÅ’áŒÀ•K—v‚È”„ã”‚àƒ`ƒFƒbƒN
		elsif ($files[$in{no}][1] eq '' && $m_sale_c < $min_sale_c && $m_update_t < $time - 24 * 3600) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$name‚ÌŒo‰c‚·‚é$shop_name‚ÍŒo‰c”j’]‚Ì‚½‚ß•Â“X‚µ‚Ü‚µ‚½</b>", 1, $name);
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		else {
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			
			push @lines, "$shop_name<>$name<>$message<>$m_sale_c<>$m_sale_money<>$display<>$guild_number<>\n";
		}
	}
	@lines = map{ $_->[0] } sort { $b->[4] <=> $a->[4] } map { [$_, split /<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# XVüŠúÌ×¸ŞÌ§²Ù‚ğXV
	open my $fh9, "> $flag_file";
	close $fh9;
}

sub is_the_end {
	my $bank_file = shift;
	
	my $sum_money = 0;
	open my $fh, "< $bank_file" or &error("$bank_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		$sum_money += $money;
	}
	close $fh;
	
	return $sum_money < 1000000 ? 1 : 0;
}



