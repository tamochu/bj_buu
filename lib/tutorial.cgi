#================================================
# Á­°ÄØ±Ù
#================================================

# Á­°ÄØ±ÙÓ°ÄŞ‚ÌŠJn
sub start_tutorial {
	$m{tutorial_switch} = 1;
	&read_tutorial;
}

# Á­°ÄØ±ÙÓ°ÄŞ‚ÌI—¹
sub stop_tutorial {
	$m{tutorial_switch} = 0;
}

# Ò²İ‰æ–Ê‚É•\¦‚³‚ê‚éÒ¯¾°¼Ş
sub show_tutorial_message {
	my $message = shift;
	$mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ¸´½Ä’B¬‚É•\¦‚³‚ê‚éÒ¯¾°¼Ş
sub success_quest_mes {
	my $message = shift;
	$tutorial_mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ¸´½Ä’B¬ˆ—
sub success_quest_result {
	my $k = shift;
	unless ( ($tutorial_quests{$k}[3] eq 'egg_c' && $m{egg} eq '0') || ($tutorial_quests{$k}[3] eq 'wea_lv' && (!$m{wea} || $m{wea_lv} >= 30)) ) {
		$m{$tutorial_quests{$k}[3]} += $tutorial_quests{$k}[2];
	}

	if ($tutorial_quests{$k}[3] eq 'egg_c') {
		return " $tutorial_quests{$k}[2] ‚Ì›z‰»’l‚ğ–á‚¢‚Ü‚µ‚½";
	}
	elsif ($tutorial_quests{$k}[3] eq 'wea_lv') {
		return "•Ší‚ğ’b‚¦‚Ä‚à‚ç‚¢‚Ü‚µ‚½";
	}
	elsif ($tutorial_quests{$k}[3] eq 'money') {
		return " $tutorial_quests{$k}[2] G‚ª“Í‚«‚Ü‚µ‚½";
	}
	elsif ($tutorial_quests{$k}[3] eq 'coin') {
		return " $tutorial_quests{$k}[2] º²İ–á‚¢‚Ü‚µ‚½";
	}
	elsif ($tutorial_quests{$k}[3] eq 'rank_exp') {
		return " $tutorial_quests{$k}[2] ‚ÌvŒ£’l‚ğ–á‚¢‚Ü‚µ‚½";
	}
	elsif ($tutorial_quests{$k}[3] eq 'medal') {
		return " $tutorial_quests{$k}[2] ‚ÌŒMÍ‚ª‘—‚ç‚ê‚Ü‚µ‚½";
	}
}

# ¸´½ÄÃŞ°À
%tutorial_quests = (
	#key								=>	[[0]No,	[1]‰ñ”,	[2]•ñVˆ—,																					[3]¸´½Ä•¶,									[4]•ñV,			[5]à–¾•¶
#	tutorial_to_country_1		=>	[0,		1,			sub{ my $i = 25; $m{egg_c} += $i if $m{egg}; return " $i ‚Ì›z‰»’l‚ğ–á‚¢‚Ü‚µ‚½"; },		'ÈÊŞ°×İÄŞ‚©‚ç‘‚ÖdŠ¯‚µ‚Ä‚İ‚æ‚¤',	'›z‰»’l+25',	'‘‚ÉŠ‘®‚·‚é‚±‚Æ‚Å‹‹—¿‚ª–á‚¦‚½‚è“ˆêí‚ÉQ‰Á‚µ‚½‚è‚Å‚«‚Ü‚·'],
	tutorial_bbsc_write_1		=>	[0,		1,			25 ,		'egg_c',		'ÈÊŞ×İˆÈŠO‚Ììí‰ï‹cº‚Åˆ¥A‚µ‚Ä‚İ‚æ‚¤',	'›z‰»’l+25',		'ìí‚ğ—û‚Á‚½‚èG’k‚µ‚½‚è¿–â‚Å‚«‚Ü‚·'],
	tutorial_junk_shop_wea_1	=>	[1,		1,			3000,		'money',		'¼Ş¬İ¸¼®¯Ìß‚Å•Ší‚ğ”ƒ‚Á‚Ä‚İ‚æ‚¤',			'‘‹à+3000',		'‘•”õ‚·‚é‚Æí“¬Eí‘ˆ‚ÌUŒ‚—Í‚ªã‚ª‚è‚Ü‚·'],
	tutorial_junk_shop_gua_1	=>	[2,		1,			3000,		'money',		'¼Ş¬İ¸¼®¯Ìß‚Å–h‹ï‚ğ”ƒ‚Á‚Ä‚İ‚æ‚¤',			'‘‹à+3000',		'‘•”õ‚·‚é‚Æí“¬‚Ì–hŒä—Í‚ªã‚ª‚èA“ÁêŒø‰Ê‚ª•t‚«‚Ü‚·'],
	tutorial_junk_shop_sell_1	=>	[3,		1,			3000,		'money',		'¼Ş¬İ¸¼®¯Ìß‚É‰½‚©‚ğ”„‚Á‚Ä‚İ‚æ‚¤',			'‘‹à+3000',		'”„‚Á‚½‚à‚Ì‚Í¼Ş¬İ¸¼®¯Ìß‚É•À‚ÑA’N‚©‚ª”ƒ‚Á‚Ä‚­‚ê‚Ü‚·'],
	tutorial_5000_gacha_1		=>	[4,		1,			5,			'rank_exp',	'5000¶ŞÁ¬‚ğ‰ñ‚µ‚Ä‚İ‚æ‚¤',						'vŒ£’l+5',			'24ŠÔ‚É1‰ñ‰ñ‚¹‚é‚Ì‚Å–ˆ“ú‰ñ‚µ‚Ü‚µ‚å‚¤'],
	tutorial_bank_1				=>	[5,		1,			10,		'coin',		'‹âs‚É‚¨‹à‚ğ—a‚¯‚Ä‚İ‚æ‚¤',					'º²İ+10',			'–ˆ”N—˜q‚ª–á‚¦‚½‚èA“¢”°‚Å•‰‚¯‚Ä‚àˆÀS‚Å‚·'],
	tutorial_hunting_1			=>	[6,		1,			10,		'coin',		'“¢”°‚ğ‚µ‚Ä‚İ‚æ‚¤',				'º²İ+10',			'“¢”°‚Å‚Í‚¨‹à‚ª–á‚¦A—‘‚ğE‚Á‚½‚è‚·‚é‚±‚Æ‚à‚ ‚è‚Ü‚·'],
	tutorial_highlow_1			=>	[7,		1,			1,			'wea_lv',	'¶¼ŞÉ‚ÅÊ²Û³‚ğ‚µ‚Ä‚İ‚æ‚¤',						'•ŠíÚÍŞÙ+1',		'’™‚ß‚½º²İ‚Í–ğ—§‚Â±²ÃÑ‚ÆŒğŠ·‚Å‚«‚Ü‚·'],
	tutorial_training_1			=>	[8,		1,			5000,		'money',		'Cs‚ğ‚µ‚Ä‚İ‚æ‚¤',								'‘‹à+5000',		'Ô‚¢‘Šè‚Æí‚¤‚Æ‹Z‚ğ‘M‚«‚â‚·‚¢‚Å‚·'],
	tutorial_hospital_1			=>	[9,		1,			10000,	'money',		'•\š•a‰@‚Å¡–ü‚µ‚Ä–á‚¨‚¤',					'Š‹à+10000',	'HPEMP‚Ì©“®‰ñ•œ‚ğ‘Ò‚Ä‚È‚¢ê‡‚Í•a‰@‚Å‰ñ•œ‚Å‚«‚Ü‚·'],
	tutorial_breeder_1			=>	[10,		1,			20,		'coin',		'ˆç‚Ä‰®‚É—‘‚ğ—a‚¯‚Ä‚İ‚æ‚¤',					'º²İ+20',			'—a‚¯‚½—‘‚Í10•ª–ˆ‚É›z‰»’l‚ª +1 ‚³‚ê‚Ü‚·'],
	tutorial_full_act_1			=>	[11,		1,			25,		'egg_c',		'”æ˜J“x‚ğ 100 %ˆÈã‚É‚µ‚Ä‚İ‚æ‚¤',			'›z‰»’l+25',		'”æ˜J‚ª 100 %‚ğ’´‚¦‚é‚Æ“à­ˆÈŠO‚Ìs“®‚ª§ŒÀ‚³‚ê‚Ü‚·'],
	tutorial_dom_1					=>	[12,		1,			10000,	'money',		'“à­‚ğ‚µ‚Ä‚İ‚æ‚¤',								'Š‹à+10000',	'—­‚Ü‚Á‚½”æ˜J‚ğ‰ñ•œ‚µ‚Â‚Â•¨‘‚ğ‘‚â‚·‚±‚Æ‚ª‚Å‚«‚Ü‚·'],
	tutorial_mil_1					=>	[13,		1,			5,			'rank_exp',	'’DŒR–‚ğ‚µ‚Ä‚İ‚æ‚¤',							'vŒ£’l+5',			'•¨‘‚ğ’D‚¤‚±‚Æ‚Å“G‘‚ğ–WŠQ‚µ‚È‚ª‚ç•¨‘‚ğ‘‚â‚¹‚Ü‚·'],
	tutorial_gikei_1				=>	[14,		1,			10,		'coin',		'‹UŒv‚ğ‚µ‚Ä‚İ‚æ‚¤',								'º²İ+10',			'“G‘‚Ì“¯–¿‚ğ–³Œø‚É‚µ‚½‚èAŒğí‚³‚¹‚â‚·‚­‚È‚è‚Ü‚·'],
	tutorial_promise1_1			=>	[15,		1,			10000,	'money',		'—FDğ–ñ‚ğŒ‹‚ñ‚Å‚İ‚æ‚¤',						'Š‹à+10000',	'“¯–¿‚ğˆÛ‚µ‚½‚èAŒğí‚ğ–h‚®‚±‚Æ‚ª‚Å‚«‚Ü‚·'],
	tutorial_mil_ambush_1		=>	[16,		1,			10,		'coin',		'ŒR–‘Ò‚¿•š‚¹‚ğ‚µ‚Ä‚İ‚æ‚¤',					'º²İ+10',			'Œø‰Ê‚ª’·‚­‘±‚­‚Ì‚ÅQ‚é‘O‚È‚Ç‚ÉdŠ|‚¯‚Ä‚¨‚«‚Ü‚µ‚å‚¤'],
	tutorial_promise2_1			=>	[17,		1,			30000,	'money',		'’âíğ–ñ‚ğŒ‹‚ñ‚Å‚İ‚æ‚¤',						'Š‹à+30000',	'Œğíó‘Ô‚ğ‰ğœ‚·‚é‚±‚Æ‚Åˆê•û“I‚ÉU‚ß‚ç‚ê‚é‚Æ‚¢‚¤ó‹µ‚ğ–h‚°‚Ü‚·'],
	tutorial_ceo_1					=>	[18,		1,			1,			'medal',		'ŒNå‚É—§Œó•â‚µ‚Ä‚İ‚æ‚¤',						'ŒMÍ+1',			'ŒNå‚É‚È‚é‚Æê—pºÏİÄŞ‚ª‰ğ•ú‚³‚ê‚½‚èAŠeís“®‚É•â³‚ª•t‚«‚Ü‚·'],
	tutorial_job_change_1		=>	[19,		1,			20000,	'money',		'<a href="http://www43.atwiki.jp/bjkurobutasaba/pages/695.html">E‹Æ</a>‚ğ•Ï‚¦‚Ä‚İ‚æ‚¤',			'Š‹à+20000',		'ŒRt‚â—x‚èq‚ªˆê”Ê“I‚È‚æ‚¤‚Å‚·'],
	tutorial_lv_20_1				=>	[20,		1,			30000,	'money',		'ÚÍŞÙ‚ğ 20 ‚É‚µ‚æ‚¤',							'Š‹à+30000',	'Lv.20‚É‚È‚é‚ÆŒ‹¥‚Å‚«‚é‚æ‚¤‚É‚È‚è‚Ü‚·'],
	tutorial_mariage_1			=>	[21,		1,			30,		'coin',		'Œ‹¥‘Š’kŠ‚É“o˜^‚µ‚Ä‚İ‚æ‚¤',					'vŒ£’l+30',		'Œ‹¥‚·‚é‚Æ“]¶‚ÌƒXƒeŒ¸­‚ğ—}‚¦‚½‚èA‘Šè‚Ì‹Z‚ğK“¾‚Å‚«‚Ü‚·'],
);

# ½ÀİÌß”
# ¸´½ÄÃŞ°À‚ÉŠÜ‚ß‚é‚Æ¸´½Ä”‚ª•Ï“®‚µ‚½‚É‘‚«Š·‚¦‚È‚¢‚Æ‚¾‚©‚ç•ª‚¯‚Ä©“®‰»
$tutorial_quest_stamps = keys(%tutorial_quests);

# ½ÀİÌßÃŞ°À
@tutorial_stamps = (
	#[0]No,	[1]”,	[2]•ñVˆ—,																							[3]•ñV
	[0,		3,			sub{ &send_item($m{name}, 2, 51, 0, 0, 1); return "ËŞ·ŞÅ°´¯¸Ş‚ğ–á‚¢‚Ü‚µ‚½"; },	'ËŞ·ŞÅ°´¯¸Ş'],
	[1,		6,			sub{ my $i = 5000; $m{money} += $i; return " $i G‚ª“Í‚«‚Ü‚µ‚½"; },					'‘‹à+5000'],
	[2,		9,			sub{ &send_item($m{name}, 2, 25, 0, 0, 1); return "¸Ø½ÀÙ´¯¸Ş‚ğ–á‚¢‚Ü‚µ‚½"; },		'¸Ø½ÀÙ´¯¸Ş'],
	[3,		12,		sub{ &send_item($m{name}, 2, 1, 0, 0, 1); return "×İÀŞÑ´¯¸Ş‚ğ–á‚¢‚Ü‚µ‚½"; },		'×İÀŞÑ´¯¸Ş'],
	[4,		16,		sub{ my $i = 10000; $m{coin} += $i; return " $i º²İ–á‚¢‚Ü‚µ‚½"; },					'º²İ+10000'],
	[5,		19,		sub{ &send_item($m{name}, 2, 19, 0, 0, 1); return "½°Êß°´¯¸Ş‚ğ–á‚¢‚Ü‚µ‚½"; },		'½°Êß°´¯¸Ş'],
	[6,		22,		sub{ &send_item($m{name}, 2, 33, 0, 0, 1); return "³ªÎßİ´¯¸Ş‚ğ–á‚¢‚Ü‚µ‚½"; },		'³ªÎßİ´¯¸Ş'],
);

=pod
# ¸´½Ä’B¬‚ÉŠÖ‚·‚és“®‚Ì¬Œ÷‚ÉŒÄ‚Ño‚·‚Æ”»’è‚â’B¬ˆ—‚È‚Ç‚ğ‚â‚Á‚Ä‚­‚ê‚é
# ˆø”‚É‚Í¸´½Ä·°‚ğ”z—ñ‚Å“n‚·
sub run_tutorial_quest {
	my @ks = @_;

	for my $k (@ks) {
		++$m{$k};
		if ($m{$k} eq $tutorial_quests{$k}[1]) {
			my $str = "•ñV‚Æ‚µ‚Ä" . &{$tutorial_quests{$k}[2]};
			&success_quest_mes("¸´½Äu$tutorial_quests{$k}[3]v‚ğ’B¬‚µ‚Ü‚µ‚½I<br>$str<br><br>$tutorial_quests{$k}[5]");
			++$m{tutorial_quest_stamp_c};
		}
	}

	# ½ÀİÌßºİÌßØ°Ä
	if ($m{tutorial_quest_stamp_c} eq $tutorial_quest_stamps) {
		&success_quest_mes("‚·‚×‚Ä‚Ì½ÀİÌß‚ğW‚ß‚Ü‚µ‚½I");
	}
}
=cut

# Õ°»Ş°‚ÌÁ­°ÄØ±ÙÃŞ°À‚Ì“Ç‚İ‚İ
sub read_tutorial {
	&write_tutorial unless -f "$userdir/$id/tutorial.cgi"; # ‰Šú‰»

	open my $fh, "< $userdir/$id/tutorial.cgi" or &error("‚»‚Ì‚æ‚¤‚È–¼‘O$in{login_name}‚ÌÌßÚ²Ô°‚ª‘¶İ‚µ‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$m{$k} = $v; # $s
	}
}

# Õ°»Ş°‚ÌÁ­°ÄØ±ÙÃŞ°À‚Ì‘‚«‚İ
sub write_tutorial {
	my $line = "tutorial_quest_stamp_c;$m{tutorial_quest_stamp_c}<>"; # ½ÀİÌß‚Í¸´½ÄÃŞ°À‚É“à•ï‚³‚ê‚Ä‚È‚¢‚Ì‚Å—\‚ß’è‹`

	foreach my $k (keys(%tutorial_quests)) {
		$line .= "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/tutorial.cgi";
	print $fh "$line\n";
	close $fh;
}

# ¸´½Ä‚Ì’B¬ó‘Ô‚Ì•\¦
sub show_stamps {
	&read_tutorial unless $m{tutorial_switch}; # Á­°ÄØ±ÙÓ°ÄŞØ‚Á‚Ä‚Ä‚à½ÀİÌß’ ‚ÍŒ©‚ê‚é‚æ‚¤‚É

	$layout = 2;
	my $comp_par = int($m{tutorial_quest_stamp_c} / $tutorial_quest_stamps * 100);
	$mes .= "½ÀİÌß’  sºİÌß—¦ $comp_par%t<br>";

 	$mes .= $is_mobile ? '<hr>”Ô† / ’B¬ / ¸´½Ä / •ñV'
 		:qq|<table class="table1" cellpadding="3"><tr><th>”Ô†</th><th>’B¬</th><th>¸´½Ä</th><th>•ñV</th></tr>|;

	my @list = (); # ¸´½ÄÃŞ°À‚ªÊ¯¼­‚Å‡•s“¯‚È‚½‚ßA•\¦—p‚É¿°Ä‚·‚é
	$#list = $tutorial_quest_stamps - 1;
	foreach my $k (keys(%tutorial_quests)) {
		my ($no, $result, $quest, $str, $sub_str) = ($tutorial_quests{$k}[0]+1, '', '', '', '');
		if ($m{$k} >= $tutorial_quests{$k}[1]) {
			$result = '›';
			$quest = "<s>$tutorial_quests{$k}[4]</s>";
			$sub_str = $is_mobile ? "<br>$tutorial_quests{$k}[6]"
				: qq|<tr><td colspan="4">$tutorial_quests{$k}[6]</td></tr>|;
		}
		else {
			$result = '~';
			$quest = "$tutorial_quests{$k}[4]";
		}
	 	$str = $is_mobile ? qq|<hr>$no / $result / $quest / $tutorial_quests{$k}[5]|
	 		: qq|<tr><td align="right">$no</td><td align="center">$result</td><td>$quest</td><td>$tutorial_quests{$k}[5]</td></tr>|;
		splice(@list, $tutorial_quests{$k}[0], 1, $str.$sub_str);
	}

	for my $i (0 .. $#list) {
		$mes .= "$list[$i]";
	}

 	$mes .= qq|</table>| unless $is_mobile;

	$mes .= "<p>½ÀİÌß•ñV</p>";
 	$mes .= $is_mobile ? '<hr>”Ô† / ’B¬ / ½ÀİÌß” / •ñV'
 		:qq|<table class="table1" cellpadding="3"><tr><th>”Ô†</th><th>’B¬</th><th>½ÀİÌß”</th><th>•ñV</th></tr>|;

	my $no = 0;
	if ($is_mobile) {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '›' : '~';
		 	$mes .= "<hr>$result / $tutorial_stamps[$i][1] / $tutorial_stamps[$i][3]";
		}
	}
	else {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '›' : '~';
		 	$mes .= qq|<tr><td align="right">$no</td><td align="center">$result</td><td align="right">$tutorial_stamps[$i][1]</td><td>$tutorial_stamps[$i][3]</td></tr>|;
		}
	}

 	$mes .= qq|</table>| unless $is_mobile;
}

# –¢’B¬‚È˜”Õ‚Ì¸´½Ä‚ğ•\¦
sub show_quest {
	my $str = '';
	my $min = $tutorial_quest_stamps;
	foreach my $k (keys(%tutorial_quests)) {
		if ($m{$k} < $tutorial_quests{$k}[1] && $tutorial_quests{$k}[0] < $min) {
			$min = $tutorial_quests{$k}[0];
			$str = $tutorial_quests{$k}[4];
		}
	}

	return $str;
}

1; # íœ•s‰Â
