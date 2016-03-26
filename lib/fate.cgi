my $this_file = "$userdir/$id/super.cgi";
#=================================================
# 英雄
#=================================================
# 冷却期間
$cooldown_time = 6 * 3600;
# トリガー
@triggers = (
#	[0]No	[1]名前			[2]type			[3]倍率	[4]選択可能	[5]発動率(%)
	[0,		'ﾏｲﾙｰﾑ',		'myroom',		0.1,	1,			100],
	[1,		'戦争勝利',		'war',			0.5,	1,			100],
	[2,		'軍事成功',		'military',		0.4,	1,			60],
	[3,		'偽計決裂',		'breakdown',	1,		0,			100],
	[4,		'外交成功',		'promise',		0.4,	1,			60],
	[5,		'宣戦布告',		'declaration',	0.8,	0,			80],
	[6,		'停戦条約',		'cessation',	0.6,	0,			80],
	[7,		'内政',			'domestic',		0.4,	1,			50],
	[8,		'戦闘勝利',		'battle',		0.3,	0,			20],
	[9,		'修行',			'training',		0.4,	0,			30],
	[10,	'討伐',			'hunting',		0.4,	0,			30],
	[11,	'闘技場',		'colosseum',	0.4,	0,			80],
	[12,	'一騎打ち',		'single',		1,		0,			100],
	[13,	'ｶｼﾞﾉ',			'casino',		0.2,	0,			1],
	[14,	'発言',			'voice',		0.2,	0,			10],
	[15,	'孵化',			'incubation',	0.3,	0,			100],
	[16,	'脱獄',			'prison',		0.5,	0,			100],
	[17,	'救出',			'rescue',		0.7,	0,			70],
	[18,	'闘技場優勝',	'colosseum_top',1,		0,			100],
	[19,	'ボス討伐',		'boss',			1,		0,			100],
	[20,	'暴発',			'random',		1,		0,			100],
);

# タイミング
@timings = (
#	[0]No	[1]名前							[2]条件		[3]倍率		[4]選択可能
	[0,		'任意',							sub{ return 1; },	0.1,	1],
	[1,		'滅亡時',						sub{ return $cs{is_die}[$m{country}]; },	0.5,	1],
	[2,		'国力トップ',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return 0; } } return 1; },	0.7,	0],
	[3,		'資源がすべて10000未満の時',	sub{ return ($cs{food}[$m{country}] < 10000 && $cs{money}[$m{country}] < 10000 && $cs{soldier}[$m{country}] < 10000); },	0.4,	1],
	[4,		'兵士が20000未満の時',			sub{ return $cs{soldier}[$m{country}] < 20000; },	0.6,	0],
	[5,		'兵士が999999の時',				sub{ return $cs{soldier}[$m{country}] >= 999999; },	0.8,	0],
	[6,		'代表の時',						sub{ return &is_daihyo; },	0.3,	1],
);

# その他デメリット
@demerits = (
#	[0]No	[1]名前				[2]デメリット		[3]倍率		[4]選択可能
	[0,		'基本拘束',			sub{ &wait; },	1,	1],
	[1,		'世代交代',			sub{ $m{lv} = 99; $m{exp} = 100; },	1,	0],
	[2,		'ステータスダウン',	sub{ @st = (qw/max_hp max_mp at df mat mdf ag cha lea/); $k = $st[int(rand(@st))]; $m{$k} -= int(rand(20)); $m{$k} = $m{$k} <= 0 ? int(rand(20)):$m{$k}},	0.6,	0],
	[3,		'階級ダウン',		sub{ $m{rank_exp} -= 100; },	1,	1],
	[4,		'所持金減少',		sub{ $m{money} -= 10000; },	0.7,	0],
	[5,		'ゴミクズ',			sub{ $m{shogo} = $shogos[1][0]; },	0.9,	0],
	[6,		'なし',				sub{ },		0.5,	0],
);

# 回数
@max_counts = (
#	[0]No	[1]回数	[2]倍率	[3]選択可能
	[0,		1,		1,		1],
	[1,		2,		0.4,		0],
	[2,		3,		0.2,		0],
);

# 効果
@effects = (
#	[0]No	[1]名前				[2]効果			[3]選択可能	[4]メッセージ
	[0,		'ﾌｪﾝﾘﾙ',			sub{
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
	},	1,	'各国の国力が減少した'],
	[1,		'ｾﾞｳｽ',				sub{
		$v = shift;
		$cs{strong}[$m{country}] += int((10000 + rand(10000)) * $v);
		&write_cs;
	},	1,	'自国の国力が増加した'],
	[2,		'ﾛﾌﾟﾄ（大地震）',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{soldier}[$i] -= int((rand(600000)+200000) * $v);
			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
		};
		&write_cs;
	},	0,	'全国の兵士が激減した'],
	[3,		'ﾛﾌﾟﾄ（自然災害）',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{food}[$i] -= int((rand(600000)+200000) * $v);
			$cs{food}[$i] = 0 if $cs{food}[$i] < 0;
		};
		&write_cs;
	},	0,	'全国の食糧が激減した'],
	[4,		'ﾛﾌﾟﾄ（経済破綻）',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			$cs{money}[$i] -= int((rand(600000)+200000) * $v);
			$cs{money}[$i] = 0 if $cs{money}[$i] < 0;
		};
		&write_cs;
	},	0,	'全国の資金が激減した'],
	[5,		'ｱﾙｶﾄﾗｽﾞ',				sub{
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
	 		
	 			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi が開けません");
	 			print $fh "$cs{$k}[$i]<>$i<>\n";
	 			close $fh;
	 		}
		};
		&write_cs;
	},	1,	'全国の代表が監禁された'],
	[6,		'ｱﾙｶﾄﾗｽﾞ(裏)',				sub{
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
		
			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi が開けません");
			print $fh "$name<>$c<>\n";
			close $fh;
		};
		&write_cs;
	},	0,	"$cs{name}[$c]の国民が監禁された"],
	[7,		'ｸｯｷｰ',				sub{
		$v = shift;
		$cs{food}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'自国の食糧が増加した'],
	[8,		'ｴﾋﾞｽ',				sub{
		$v = shift;
		$cs{money}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'自国の資金が増加した'],
	[9,		'ﾏﾙｽ',				sub{
		$v = shift;
		$cs{soldier}[$m{country}] += int((500000 + rand(2000000)) * $v);
		&write_cs;
	},	1,	'自国の兵士が増加した'],
	[10,	'ｳﾛﾎﾞﾛｽ',				sub{
		$v = shift;
		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 3600;
			$cs{extra}[$m{country}] = 1;
		}
		&write_cs;
	},	0,	'自国の奪国力が増加する'],
	[11,	'ｳﾛﾎﾞﾛｽ(軍事)',				sub{
		$v = shift;
		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 3600;
			$cs{extra}[$m{country}] = 2;
		}
		&write_cs;
	},	0,	'自国の軍事力が増加する'],
	[12,	'ｲｰｽﾀｰ',				sub{
		$v = shift;
		for my $i (1..$w{country}) {
			if ($cs{is_die}[$i]) {
				$cs{is_die}[$i] = 0;
				--$w{game_lv};
			}
		};
		&write_cs;
	},	1,	'全国が復興しました'],
	[13,	'ﾘｳﾞｧｲｱｻﾝ',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my $vv = int((20000 + rand(20000)) * $v);
		if ($cs{strong}[$c] < $vv) {
			$vv = $cs{strong}[$c];
		}
		$cs{strong}[$c] -= $vv;
		$cs{strong}[$m{country}] += int($vv / 3);
		&write_cs;
	},	0,	"$cs{name}[$c]の国力を奪った"],
	[13,	'ｴｸｽｶﾘﾊﾞｰ',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		$cs{strong}[$c] = 0;
		$cs{is_die}[$c] = 1;
		&write_cs;
	},	0,	"$cs{name}[$c]に聖剣を放った"],
);
#=================================================
# 登録メッセージ
#=================================================
sub regist_mes {
	$force = shift;
	$tm = qq|<hr>必殺技|;
	my $attack = &get_attack;
	my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack;
	&count_check($a_max_count, $a_count, $a_last_attack);
	$attack = &get_attack;
	if ($attack eq '' || $force) {
		$tm .= qq|<br><select name="trigger" class="menu1">|;
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
			$tm .= qq|<option value="$i">$max_counts[$i][1]回</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="effect" class="menu1">|;
		for my $i (0..$#effects) {
			next if !$effects[$i][3];
			$tm .= qq|<option value="$i">$effects[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><input type="text" name="voice" class="text_box_b"/>|;
		$tm .= qq|<br><input type="checkbox" name="random" value="1"/>適当|;
	} else {
		my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $random) = split /<>/, $attack;
		$tm .= qq|<br>$triggers[$trigger][1]|;
		$tm .= qq|<br>$timings[$timing][1]|;
		$tm .= qq|<br>$demerits[$demerit][1]|;
		$tm .= qq|<br>$max_counts[$max_count][1]回|;
		$tm .= qq|<br>$effects[$effect][1]|;
		$tm .= qq|<br>セリフ「$voice」|;
	}

	return $tm;
}
#=================================================
# 必殺技登録
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
	open my $fh, ">> $this_file" or &error("$this_fileに書き込めません");
	print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>0<>$time<>\n";
	close $fh;
	
	return 1;
}
#=================================================
# 必殺技取得
#=================================================
sub get_attack {
	if (-f "$this_file") {
		open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
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
# 必殺技削除
#=================================================
sub del_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
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
# 必殺技使用
#=================================================
sub use_count_up {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
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
# 必殺技回数チェック
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
# 必殺技発動
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
		&use_count_up;
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
	&mes_and_world_news("必殺技を開放しました。<br><b>$m{name}「$voice」</b><br>$e_mes", 1);
}
#=================================================
# 修正後所属人数
#=================================================
sub modified_member {
	my $count_country = shift;
	my $count = 0;
	my @members = &get_country_members($count_country);
	for my $member (@members) {
		$member =~ tr/\x0D\x0A//d; # = chomp 余分な改行削除
		my $member_id = unpack 'H*', $member;
		my %datas = &get_you_datas($member_id, 1);
		unless ($datas{sedai} == 1) {
			$count++;
		}
	}
	return $count;
}

1;