my $this_file = "$userdir/$id/super.cgi";
#=================================================
# ‰p—Y
#=================================================
# —â‹pŠúŠÔ
$coolhour = 6;
$cooldown_time = 60;#$coolhour * 3600;#6 * 3600;
# ƒgƒŠƒK[
@triggers = (
#	[0]No	[1]–¼‘O			[2]type			[3]”{—¦	[4]‘I‘ğ‰Â”\	[5]”­“®—¦(%)
	[0,		'Ï²Ù°Ñ',		'myroom',		0.1,	1,			100],
	[1,		'í‘ˆŸ—˜',		'war',			0.5,	1,			100],
	[2,		'ŒR–¬Œ÷',		'military',		0.4,	1,			60],
	[3,		'‹UŒvŒˆ—ô',		'breakdown',	1,		0,			100],
	[4,		'ŠOŒğ¬Œ÷',		'promise',		0.4,	1,			60],
	[5,		'éí•z',		'declaration',	0.8,	0,			80],
	[6,		'’âíğ–ñ',		'cessation',	0.6,	0,			80],
	[7,		'“à­',			'domestic',		0.4,	1,			50],
	[8,		'í“¬Ÿ—˜',		'battle',		0.3,	0,			20],
	[9,		'Cs',			'training',		0.4,	0,			30],
	[10,	'“¢”°',			'hunting',		0.4,	0,			30],
	[11,	'“¬‹Zê',		'colosseum',	0.4,	0,			80],
	[12,	'ˆê‹R‘Å‚¿',		'single',		1,		0,			100],
	[13,	'¶¼ŞÉ',			'casino',		0.2,	0,			1],
	[14,	'”­Œ¾',			'voice',		0.2,	0,			10],
	[15,	'›z‰»',			'incubation',	0.3,	0,			100],
	[16,	'’E–',			'prison',		0.5,	0,			100],
	[17,	'‹~o',			'rescue',		0.7,	0,			70],
	[18,	'“¬‹Zê—DŸ',	'colosseum_top',1,		0,			100],
	[19,	'ƒ{ƒX“¢”°',		'boss',			1,		0,			100],
	[20,	'–\”­',			'random',		1,		0,			100],
);

# ƒ^ƒCƒ~ƒ“ƒO
@timings = (
#	[0]No	[1]–¼‘O							[2]ğŒ		[3]”{—¦		[4]‘I‘ğ‰Â”\
	[0,		'”CˆÓ',							sub{ return 1; },	0.1,	1],
	[1,		'–Å–S',						sub{ return $cs{is_die}[$m{country}]; },	0.5,	1],
	[2,		'‘—Íƒgƒbƒv',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return 0; } } return 1; },	0.7,	0],
	[3,		'‘Œ¹‚ª‚·‚×‚Ä10000–¢–‚Ì',	sub{ return ($cs{food}[$m{country}] < 10000 && $cs{money}[$m{country}] < 10000 && $cs{soldier}[$m{country}] < 10000); },	0.4,	1],
	[4,		'•ºm‚ª20000–¢–‚Ì',			sub{ return $cs{soldier}[$m{country}] < 20000; },	0.6,	0],
	[5,		'•ºm‚ª999999‚Ì',				sub{ return $cs{soldier}[$m{country}] >= 999999; },	0.8,	0],
	[6,		'‘ã•\‚Ì',						sub{ return &is_daihyo; },	0.3,	1],
);

# ‚»‚Ì‘¼ƒfƒƒŠƒbƒg
@demerits = (
#	[0]No	[1]–¼‘O				[2]ƒfƒƒŠƒbƒg		[3]”{—¦		[4]‘I‘ğ‰Â”\
	[0,		'Šî–{S‘©',			sub{ &wait; },	1,	1],
	[1,		'¢‘ãŒğ‘ã',			sub{ $m{lv} = 99; $m{exp} = 100; },	1,	0],
	[2,		'ƒXƒe[ƒ^ƒXƒ_ƒEƒ“',	sub{ @st = (qw/max_hp max_mp at df mat mdf ag cha lea/); $k = $st[int(rand(@st))]; $m{$k} -= int(rand(20)); $m{$k} = $m{$k} <= 0 ? int(rand(20)):$m{$k}},	0.6,	0],
	[3,		'ŠK‹‰ƒ_ƒEƒ“',		sub{ $m{rank_exp} -= 100; },	1,	1],
	[4,		'Š‹àŒ¸­',		sub{ $m{money} -= 10000; },	0.7,	0],
	[5,		'ƒSƒ~ƒNƒY',			sub{ $m{shogo} = $shogos[1][0]; },	0.9,	0],
	[6,		'‚È‚µ',				sub{ },		0.5,	0],
);

# ‰ñ”
@max_counts = (
#	[0]No	[1]‰ñ”	[2]”{—¦	[3]‘I‘ğ‰Â”\
	[0,		1,		1,		1],
	[1,		2,		0.4,		0],
	[2,		3,		0.2,		0],
);

# Œø‰Ê
@effects = (
#	[0]No	[1]–¼‘O				[2]Œø‰Ê			[3]‘I‘ğ‰Â”\	[4]ƒƒbƒZ[ƒW
	[0,		'ÌªİØÙ',			sub{
		$v = shift;
		$c = &get_most_strong_country;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{strong}[$i] -= int((rand(16000)+2000) * $v);
			$cs{strong}[$i] -= int((rand(16000)+2000) * $v) if ($i eq $c);
			if ($cs{strong}[$i] < 0) {
				$cs{strong}[$i] = int(rand(10)) * 100;
			}
		};
		&write_cs;
	},	1,	'Še‘‚Ì‘—Í‚ªŒ¸­‚µ‚½'],
	[1,		'¾Ş³½',				sub{
		$v = shift;
		$cs{strong}[$m{country}] += int((10000 + rand(10000)) * $v);
		&write_cs;
	},	1,	'©‘‚Ì‘—Í‚ª‘‰Á‚µ‚½'],
	[2,		'ÛÌßÄi‘å’nkj',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{soldier}[$i] -= int((rand(600000)+200000) * $v);
			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
		};
		&write_cs;
	},	0,	'‘S‘‚Ì•ºm‚ªŒƒŒ¸‚µ‚½'],
	[3,		'ÛÌßÄi©‘RĞŠQj',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{food}[$i] -= int((rand(600000)+200000) * $v);
			$cs{food}[$i] = 0 if $cs{food}[$i] < 0;
		};
		&write_cs;
	},	0,	'‘S‘‚ÌH—Æ‚ªŒƒŒ¸‚µ‚½'],
	[4,		'ÛÌßÄiŒoÏ”j’]j',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{money}[$i] -= int((rand(600000)+200000) * $v);
			$cs{money}[$i] = 0 if $cs{money}[$i] < 0;
		};
		&write_cs;
	},	0,	'‘S‘‚Ì‘‹à‚ªŒƒŒ¸‚µ‚½'],
	[5,		'±Ù¶Ä×½Ş',				sub{
		$v = shift;
		my @ks = (qw/war dom pro mil ceo/);
		for my $k (@ks) {
		 	for my $i (1 .. $w{country}) {
	 			next if $cs{$k}[$i] eq '';
	 			next if $i eq $m{country};
	 			next if rand(0.1) > $v;
	 		
	 			&regist_you_data($cs{$k}[$i], 'lib', 'prison');
	 			&regist_you_data($cs{$k}[$i], 'tp', 100);
	 			&regist_you_data($cs{$k}[$i], 'y_country',  $m{country});
	 			&regist_you_data($cs{$k}[$i], 'wt', $GWT * 60);
	 			&regist_you_data($cs{$k}[$i], 'act', 0);
	 		
	 			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	 			print $fh "$cs{$k}[$i]<>$i<>\n";
	 			close $fh;
	 		}
		};
		&write_cs;
	},	1,	'‘S‘‚Ì‘ã•\‚ªŠÄ‹Ö‚³‚ê‚½'],
	[6,		'±Ù¶Ä×½Ş(— )',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my @names = &get_country_members($c);
	 	for my $name (@names) {
			$name =~ tr/\x0D\x0A//d;
		
			&regist_you_data($name, 'lib', 'prison');
			&regist_you_data($name, 'tp', 100);
			&regist_you_data($name, 'y_country',  $m{country});
			&regist_you_data($name, 'wt', $GWT * 60);
			&regist_you_data($name, 'act', 0);
		
			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
			print $fh "$name<>$c<>\n";
			close $fh;
		};
		&write_cs;
	},	0,	"$cs{name}[$c]‚Ì‘–¯‚ªŠÄ‹Ö‚³‚ê‚½"],
	[7,		'¸¯·°',				sub{
		$v = shift;
		$cs{food}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'©‘‚ÌH—Æ‚ª‘‰Á‚µ‚½'],
	[8,		'´ËŞ½',				sub{
		$v = shift;
		$cs{money}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'©‘‚Ì‘‹à‚ª‘‰Á‚µ‚½'],
	[9,		'ÏÙ½',				sub{
		$v = shift;
		$cs{soldier}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'©‘‚Ì•ºm‚ª‘‰Á‚µ‚½'],
	[10,	'³ÛÎŞÛ½',				sub{
		$v = shift;
		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 3600;
			$cs{extra}[$m{country}] = 1;
		}
		&write_cs;
	},	0,	'©‘‚Ì’D‘—Í‚ª‘‰Á‚·‚é'],
	[11,	'³ÛÎŞÛ½(ŒR–)',				sub{
		$v = shift;
		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 3600;
			$cs{extra}[$m{country}] = 2;
		}
		&write_cs;
	},	0,	'©‘‚ÌŒR–—Í‚ª‘‰Á‚·‚é'],
	[12,	'²°½À°',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			if ($cs{is_die}[$i]) {
				$cs{is_die}[$i] = 0 if $cs{is_die}[$i] < 2;
				--$w{game_lv};
			}
		};
		&write_cs;
	},	1,	'‘S‘‚ª•œ‹»‚µ‚Ü‚µ‚½'],
	[13,	'Ø³Ş§²±»İ',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my $vv = int((20000 + rand(20000)) * $v);
		if ($cs{strong}[$c] < $vv) {
			$vv = $cs{strong}[$c];
		}
		$cs{strong}[$c] -= $vv;
		$cs{strong}[$m{country}] += int($vv / 3);
		&write_cs;
	},	0,	"$cs{name}[$c]‚Ì‘—Í‚ğ’D‚Á‚½"],
	[13,	'´¸½¶ØÊŞ°',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		$cs{strong}[$c] = 0;
		$cs{is_die}[$c] = 1 if $cs{is_die}[$i] < 2;
		&write_cs;
	},	0,	"$cs{name}[$c]‚É¹Œ•‚ğ•ú‚Á‚½"],
);
#=================================================
# “o˜^ƒƒbƒZ[ƒW
#=================================================
sub regist_mes {
	$force = shift;
	$tm = qq|y•KE‹Zz|;
	my $attack = &get_attack;
	my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack;
	my $is_count = &count_check($a_max_count, $a_count, $a_last_attack);
	$attack = &get_attack;# HHH
	if ($attack eq '' || $force) {
		$tm .= qq|<form method="$method" action="$script">|;

		$tm .= qq|<select name="trigger" class="menu1">|;
		for my $i (0..$#triggers) {
			next if !$triggers[$i][4];
			$tm .= qq|<option value="$i">$triggers[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="timing" class="menu1">|;
		for my $i (0..$#timings) {
			next if !$timings[$i][4];
			$tm .= qq|<option value="$i">$timings[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="demerit" class="menu1">|;
		for my $i (0..$#demerits) {
			next if !$demerits[$i][4];
			$tm .= qq|<option value="$i">$demerits[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="max_count" class="menu1">|;
		for my $i (0..$#max_counts) {
			next if !$max_counts[$i][3];
			$tm .= qq|<option value="$i">$max_counts[$i][1]‰ñ</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="effect" class="menu1">|;
		for my $i (0..$#effects) {
			next if !$effects[$i][3];
			$tm .= qq|<option value="$i">$effects[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><input type="text" name="voice" class="text_box_b"/>|;
		$tm .= qq|<br><br><input type="checkbox" name="random" value="1"/>“K“–|;
		$tm .= qq|<input type="hidden" name="regist_attack"/>|;
		$tm .= qq|<input type="hidden" name="mode" value="regist_attack">|;
		$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$tm .= qq|<input type="submit" value="•KE‹Z‚ğİ’è‚·‚é" class="button1"></form>|;

	} else {
		my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $random, $last_attack) = split /<>/, $attack;
		unless ($is_count) {
	#		my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack_set;
	
			unless ($is_mobile) {
				$tm .= qq|<table class="table1" cellpadding="3">|;
				$tm .= qq|<tr><th>s“®</th><td>$triggers[$trigger][1]</td></tr>|;
				$tm .= qq|<tr><th>ğŒ</th><td>$timings[$timing][1]</td></tr>|;
				$tm .= qq|<tr><th>ƒfƒƒŠƒbƒg</th><td>$demerits[$demerit][1]</td></tr>|;
				$tm .= qq|<tr><th>‰ñ”</th><td>$max_counts[$max_count][1]‰ñ</td></tr>|;
				$tm .= qq|<tr><th>Œø‰Ê</th><td>$effects[$effect][1]</td></tr>|;
				$tm .= qq|<tr><th>¾ØÌ</th><td>u$voicev</td></tr>|;
				$tm .= qq|</table>|;
			}
			else {
				$tm .= qq|<br>$triggers[$trigger][1]|;
				$tm .= qq|<br>$timings[$timing][1]|;
				$tm .= qq|<br>$demerits[$demerit][1]|;
				$tm .= qq|<br>$max_counts[$max_count][1]‰ñ|;
				$tm .= qq|<br>$effects[$effect][1]|;
				$tm .= qq|<br>ƒZƒŠƒtu$voicev|;
			}

#			$tm .= qq|<br>Ÿ‚Ì•KE‹Z”­“®‚Ü‚Å <font color="#FF0000"><b>‚n‚jI</b></font>|;

			$tm .= qq|<br><form method="$method" action="$script">|;
			$tm .= qq|<input type="hidden" name="mode" value="use_attack">|;
			$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$tm .= qq|<input type="checkbox" name="luxury" value="1">‹ó‘Å‚¿|;
			$tm .= qq|<input type="submit" value="•KE‹Z‚ğg—p‚·‚é" class="button1"></form>|;
		}
		else {
			my $nokori_time = ($last_attack + $cooldown_time) - $time;
			my $nokori_time_mes = '';
			$nokori_time_mes = sprintf("–ñ<b>%d</b><b>%02d</b>•ªŒã", $nokori_time / 3600, $nokori_time % 3600 / 60);
			$tm .= qq|<br>•KE‹Z‚ÌÄİ’è‚Ü‚Å $nokori_time_mes|;
		}
	}

	return $tm;
}
#=================================================
# •KE‹Z“o˜^
#=================================================
sub regist_attack {
	my ($trigger, $timing, $demerit, $max_count, $effect, $voice, $random) = @_;
	my $attack = &get_attack;

	if ($attack ne '') {
		&del_attack;
		return 0;
	}
	if ($random) {
		my @triggers_s = ();
		for my $i (0..$#triggers) {
			if ($triggers[$i][4]) {
				push @triggers_s, $i;
			}
		}
		if (rand(10) < 1) {
			$trigger = int(rand(@triggers));
		} else {
			$trigger = $triggers_s[int(rand(@triggers_s))];
		}
		
		my @timings_s = ();
		for my $i (0..$#timings) {
			if ($timings[$i][4]) {
				push @timings_s, $i;
			}
		}
		if (rand(10) < 1) {
			$timing = int(rand(@timings));
		} else {
			$timing = $timings_s[int(rand(@timings_s))];
		}
		
		my @demerits_s = ();
		for my $i (0..$#demerits) {
			if ($demerits[$i][4]) {
				push @demerits_s, $i;
			}
		}
		if (rand(10) < 1) {
			$demerit = int(rand(@demerits));
		} else {
			$demerit = $demerits_s[int(rand(@demerits_s))];
		}
		
		my @max_counts_s = ();
		for my $i (0..$#max_counts) {
			if ($max_counts[$i][3]) {
				push @max_counts_s, $i;
			}
		}
		if (rand(10) < 1) {
			$max_count = int(rand(@max_counts));
		} else {
			$max_count = $max_counts_s[int(rand(@max_counts_s))];
		}
		
		my @effects_s = ();
		for my $i (0..$#effects) {
			if ($effects[$i][3]) {
				push @effects_s, $i;
			}
		}
		if (rand(10) < 1) {
			$effect = int(rand(@effects));
		} else {
			$effect = $effects_s[int(rand(@effects_s))];
		}
	} else {
		if (!$triggers[$trigger][4]) {
			return 0;
		}
		if (!$timings[$timing][4]) {
			return 0;
		}
		if (!$demerits[$demerit][4]) {
			return 0;
		}
		if (!$max_counts[$max_count][3]) {
			return 0;
		}
		if (!$effects[$effect][3]) {
			return 0;
		}
	}
	open my $fh, ">> $this_file" or &error("$this_file‚É‘‚«‚ß‚Ü‚¹‚ñ");
	print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>0<>$time<>\n";
	close $fh;
	
	return 1;
}
#=================================================
# •KE‹Zæ“¾
#=================================================
sub get_attack {
	if (-f "$this_file") {
		open my $fh, "< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				close $fh;
				return $line;
			}
		}
		close $fh;
	}
	return '';
}
#=================================================
# •KE‹Zíœ
#=================================================
sub del_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				next;
			}
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# •KE‹Z‰ğœ
#=================================================
sub cancel_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>0<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# •KE‹Zg—p
#=================================================
sub use_count_up {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# •KE‹Z‰ñ”ƒ`ƒFƒbƒN
#=================================================
sub count_check {
	my ($max_count, $count, $last_attack) = @_;
	if ($max_counts[$max_count][1] > $count) {
		return 0;
	} elsif ($last_attack + $cooldown_time < $time) {
		&del_attack;
		return 1;
	} else {
		return 1;
	}
}
#=================================================
# •KE‹Z”­“®
#=================================================
sub super_attack {
	my $key = shift;
	unless ($m{country}) {
		return;
	}
	if ($time < $w{reset_time}) {
		return;
	}
	my $attack = &get_attack;
	if ($attack eq '') {
		return;
	}
	my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $attack;
	if ($key eq 'luxury') {
		&cancel_attack;
	}
	if ($key ne $triggers[$trigger][2] || rand(100) > $triggers[$trigger][5]) {
		return;
	}
	$attackable = &{$timings[$timing][2]};
	if (!$attackable) {
		return;
	}
	if (&count_check($max_count, $count, $last_attack)) {
		return;
	}
	
	&{$demerits[$demerit][2]};
	my $mem = &modified_member($m{country});
	$effects[$effect][2]->($triggers[$trigger][3]
							* $timings[$timing][3]
							* $demerits[$demerit][3]
							* $max_counts[$max_count][2]
							* (1 + ($cs{capacity}[$m{country}] - $mem) * 0.1));
	$e_mes = $effects[$effect][4];
	&use_count_up;
	&mes_and_world_news("•KE‹Z‚ğŠJ•ú‚µ‚Ü‚µ‚½B<br><b>$m{name}u$voicev</b><br>$e_mes", 1);
}
#=================================================
# C³ŒãŠ‘®l”
#=================================================
sub modified_member {
	my $count_country = shift;
	my $count = 0;
	my @members = &get_country_members($count_country);
	for my $member (@members) {
		$member =~ tr/\x0D\x0A//d; # = chomp —]•ª‚È‰üsíœ
		my $member_id = unpack 'H*', $member;
		my %datas = &get_you_datas($member_id, 1);
		unless ($datas{sedai} == 1) {
			$count++;
		}
	}
	return $count;
}

1;