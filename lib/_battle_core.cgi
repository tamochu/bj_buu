require "$datadir/skill.cgi";
$is_battle = 1; # ÊŞÄÙÌ×¸Ş1
#================================================
# í“¬ Created by Merino
#================================================

#ÈºĞĞ–â‘è
#@ÈºĞĞ‘Šè‚É‹Z‚ğ”ğ‚¯‚ç‚ê‚é‚Æ‚±‚Á‚¿‚Ìˆê•”‚Ì‹Z‚ÍMPÁ”ï‚È‚µ‚ÅŒø‰Ê‚ª”­Šö‚³‚ê‚é
#@‹t‚É¾ÙÊŞ‚È‚Ç‘Šè‚É“–‚½‚é‚±‚Æ‚ğ‘O’ñ‚Æ‚µ‚È‚¢‹Z‚ÍŒø‰Ê‚à”­Šö‚µ‚È‚¢
#@‚»‚à‚»‚àÈºĞĞ”ğ‚¯‚·‚¬‚È‹C‚à‚·‚é
#@”X‚Ì–â‘è‚ğŠÜ‚ßAUŒ‚Ì×¸Ş‚ğ‹¤—p‚µ‚Ä‚é‚Ì‚ª‚â‚è‚É‚­‚¢

# •Ší‚É‚æ‚é—D—ò
my %tokkous = (
# '‹­‚¢‘®«' => qr/ã‚¢‘®«/,
	'Œ•' => qr/•€/,
	'•€' => qr/‘„/,
	'‘„' => qr/Œ•/,
	'‰Š' => qr/•—|–³/,
	'•—' => qr/—‹|–³/,
	'—‹' => qr/‰Š|–³/,
	'–³' => qr/Œ•|•€|‘„/,
);

#================================================
# g‚¤’l‚ğ Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# ‰æ–Ê•\¦‚â½·Ù‚Åg‚¤‚Ì‚Å¸ŞÛ°ÊŞÙ•Ï”
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$m_mdf= $m{mdf};
$y_df = $y{df};
$y_mdf= $y{mdf};
$m_ag = $m{ag};
$y_ag = $y{ag};

if    ($guas[$m{gua}][2] =~ /–³|Œ•|•€|‘„/) { $m_df += $guas[$m{gua}][3]; }
elsif ($guas[$m{gua}][2] =~ /‰Š|•—|—‹/)    { $m_mdf+= $guas[$m{gua}][3]; }
if    ($guas[$y{gua}][2] =~ /–³|Œ•|•€|‘„/) { $y_df += $guas[$y{gua}][3]; }
elsif ($guas[$y{gua}][2] =~ /‰Š|•—|—‹/)    { $y_mdf+= $guas[$y{gua}][3]; }
# g—p‚·‚é‚Ì‚Í AT or MAT, DF or MDF ‚Ì‚Ç‚¿‚ç‚©
if    ($weas[$m{wea}][2] =~ /–³|Œ•|•€|‘„/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /‰Š|•—|—‹/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y_mdf; }
if    ($weas[$y{wea}][2] =~ /–³|Œ•|•€|‘„/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /‰Š|•—|—‹/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m_mdf; }

$m_ag -= $guas[$m{gua}][5];
$m_ag -= $weas[$m{wea}][5] if $guas[$m{gua}][0] ne '7';
$m_ag = int(rand(5)) if $m_ag < 1;

$y_ag -= $guas[$y{gua}][5];
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea}, $y{wea})) {
		$m_at = int(1.5 * $m_at);
		$y_at = int(0.75 * $y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}
# •Ší‚Æ–h‹ï‚Ì‘Š«İ’è(UŒ‚—Í)
# ‘fèvs–h‹ï‚ ‚è 0.3”{ ‘fèvs–h‹ï‚È‚µ 1.0”{
# •Šívs–h‹ï‚È‚µ 1.0”{ •Šívs–h‹ï‘®«ˆá‚¢ 1.0”{ •Šívs–h‹ï‘®«“¯‚¶ 0.5”{
# ‘fè‚Å–h‹ï‚¿‰£‚Á‚½‚ç‰º•ûC³“¯—lA•Ší‚Å–h‹ï‚È‚µ‰£‚Á‚½‚çã•ûC³‚Æ‚©‚Í‚µ‚È‚¢‚ÌH ‘fè•s—˜‚Å‘Š‘Î“I‚É•Ší‚¿—L—˜‚Æ‚àŒ¾‚¦‚é‚¯‚Ç
if ($y{gua}) {
	if ($m{wea}) {
		if (&is_gua_valid($y{gua},$m{wea})) {
			$m_at = int(0.5 * $m_at);
			$is_y_tokkou2 = 1;
		}
	}
	else {
		$m_at = int(0.3 * $m_at);
		$is_y_tokkou2 = 1;
	}
}
#else {
#	$m_at = int($m_at * 1.2) if $m{wea};
#}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})) {
			$y_at = int(0.5 * $y_at);
			$is_m_tokkou2 = 1;
		}
	} else {
		$y_at = int(0.3 * $y_at);
		$is_m_tokkou2 = 1;
	}
}
#else {
#	$y_at = int($y_at * 1.2) if $y{wea};
#}

#================================================
# Ò²İ“®ì
#================================================
&run_battle2;
#&run_battle;

&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# Àsˆ—
#================================================
sub run_battle2 {
	if ($cmd eq '') {
		$mes .= 'í“¬ºÏİÄŞ‚ğ‘I‘ğ‚µ‚Ä‚­‚¾‚³‚¢<br>';
	}
	elsif ($m{turn} >= 20) { # ‚È‚©‚È‚©Œˆ’…‚Â‚©‚È‚¢ê‡
		$mes .= 'í“¬ŒÀŠEÀ°İ‚ğ’´‚¦‚Ä‚µ‚Ü‚Á‚½c‚±‚êˆÈã‚Íí‚¦‚Ü‚¹‚ñ<br>';
		&lose;
	}
	else {
		# –³‰ü‘¢‚Æˆá‚Á‚Äƒ^[ƒ“‡‚ğ–³‹‚µ‚ÄŒø‰Ê‚ğ”­Šö‚·‚éˆ—‚ªÀ‘•‚³‚ê‚Ä‚¢‚é
		# æUEŒãU‚Ç‚¿‚ç‚ğ—Dæ‚µ‚Äˆ—‚·‚é‚©ˆÈ‘O‚É—¼•û‚Ìƒtƒ‰ƒOŠÇ—‚ğs‚¤

		# ‚Ü‚¸©•ª‚Æ‘Šè‚ÌUŒ‚E•KE‹Z”»’è $m_s ‚ª–¢’è‹`‚È‚ç©•ªA$y_s ‚ª–¢’è‹`‚È‚ç‘Šè‚ÍUŒ‚
		local $m_s = undef; # ÌßÚ²Ô°‚Ì‹Zƒf[ƒ^‚ª“ü‚é –¢’è‹`‚È‚çUŒ‚
		local $pikorin; # ÌßÚ²Ô°‚ª‹Z‚ğ‘M‚¢‚½‚© 1 ‘M‚¢‚½ 0 ‘M‚¢‚Ä‚È‚¢
		if (!$metal) { # ÒÀÙ‘Šè‚É‚Íí‚ÉUŒ‚‚Å•KE‹Z‚à‘M‚©‚È‚¢
			$m_s = $skills[ $m_skills[ $cmd - 1 ] ] if $cmd > 0 && $guas[$m{gua}][0] ne '21'; # 1ºÏİÄŞˆÈã‚ğ“ü—Í‚µ‚Ä‚¢‚Ä‹¶ím‚ÌŠZ‚¶‚á‚È‚­ÒÀÙ‘Šè‚¶‚á‚È‚¢‚È‚ç•KE‹Z
			$m_s = undef if defined($m_s) && ($weas[$m{wea}][2] ne $m_s->[2] || !&m_mp_check($m_s)); # •KE‹Z‚ğ‘I‘ğ‚µ‚Ä‚¢‚Ä‚à‘®«‚ªˆá‚Á‚½‚èMP‚ª‘«‚è‚È‚¢‚È‚çUŒ‚
			# ‹Z‘M‚¢‚Ä‚àƒtƒ‰ƒO‚ª—§‚½‚È‚¢–â‘è‘Îô ƒtƒ‰ƒO©‘Ì‚ÍæUŒãUŠÖŒW‚È‚¢‚Ì‚Å—\‚ß‘M‚«ˆ—‚ğÏ‚Ü‚¹‚Îƒtƒ‰ƒO—§‚Ä‚ç‚ê‚é
			$pikorin = &_learning if !defined($m_s); # UŒ‚‚Å‹Z‚ğ‘M‚¢‚½‚È‚ç‚Î 1 ‚ª•Ô‚èA‘M‚¢‚½‹Z‚Í $m_s ‚É“ü‚é
		}
		local $y_s = undef; # “G‚Ì‹Zƒf[ƒ^‚ª“ü‚é –¢’è‹`‚È‚çUŒ‚
		$y_s = $skills[ $y_skills[ int(rand(6)) - 1 ] ] if $guas[$y{gua}][0] ne '21'; # ‹¶ím‚ÌŠZ‚¶‚á‚È‚¢‚È‚ç•KE‹Z
		$y_s = undef if defined($y_s) && ($weas[$y{wea}][2] ne $y_s->[2] || !&y_mp_check($y_s) || $metal); # •KE‹Z‚ğ‘I‘ğ‚µ‚Ä‚¢‚Ä‚à‘®«‚ªˆá‚Á‚½‚èMP‚ª‘«‚è‚È‚¢‚Æ‚©ÒÀÙ‚È‚çUŒ‚

		# ƒtƒ‰ƒO‚ğ‚Ü‚¸‘S•”ô‚¢o‚µ‚Ä‚©‚çˆ—‚·‚ê‚Î•Ï‚È‹““®‚µ‚È‚­‚È‚é
		# —á
		#   –³Œø‹Z‚ğÈºĞĞ‚Å”ğ‚¯‚ç‚ê‚é‚ÆMPÁ”ï‚¹‚¸‚É–³Œø‹Z‚ğ”­Šö‚Å‚«‚é
		#   ½Àİ‹Z‚ğÔÀÉ¶¶ŞĞ‚Å•Ô‚³‚ê‚Ä‚à‘Šè‚É½ÀİŒø‰Ê‚ğ—^‚¦‚é
		# í“¬‚Í $who ‚Å©•ª‚Æ‘Šè‚ğØ‚è‘Ö‚¦‚Ä‚é‚Ì‚Å‚»‚ê“¯—l $who ‚Åƒtƒ‰ƒOŠÇ—‚àØ‚è‘Ö‚¦‚é

		local $who = '';
		$who = 'm';
		&get_battle_flags; # $m_is_guard, $m_is_stanch, ... ‚È‚Ç‚ª“ü‚é skill.cgi QÆ
		$who = 'y';
		&get_battle_flags; # $y_is_guard, $y_is_stanch, ... ‚È‚Ç‚ª“ü‚é skill.cgi QÆ

		# ‚±‚±‚Å–h‰qÒ‚Ì–³ŒøŒø‰Ê‚ğƒIƒt‚É‚·‚ê‚Î–³Œø‹ZMP–¢Á”ïƒoƒO‹N‚«‚È‚¢‚Í‚¸
		# ‚½‚¾A–³Œø‚Æ‚¢‚¤‚æ‚èÈºĞĞ‚Ì‚‘¬ˆÚ“®‚Å”ğ‚¯‚Ä‚éƒCƒƒW‚ª‹­‚·‚¬‚é(“–‚Ä‚é‹C‚Ì‚È‚¢•KE‹Z‚ğ”ğ‚¯‚Ä‚àˆÓ–¡‚È‚¢”ğ‚¯‚ç‚ê‚È‚¢‚İ‚½‚¢‚È)‚Ì‚ÆA
		# ’Pƒ‚É–³Œø‚ª‹­‚¢‚Ì‚ÅMP–¢Á”ïƒoƒOc‚Á‚Ä‚é‚®‚ç‚¢‚Å‚¿‚å‚¤‚Ç—Ç‚¢‹C‚µ‚©‚µ‚È‚¢
		# $m_is_guard = 0 if $m_is_guard && $y_gua_avoid;
		# $y_is_guard = 0 if $y_is_guard && $m_gua_avoid;

		# ‚±‚±‚ÅUŒ‚Ò‚Ì½ÀİŒø‰Ê‚ğƒIƒt‚É‚·‚ê‚Î½Àİ‹Z”½ËƒoƒO‹N‚«‚È‚¢‚Í‚¸
		# $m_is_stanch = 0 if $m_is_stanch && $y_gua_skill_mirror;
		# $y_is_stanch = 0 if $y_is_stanch && $m_gua_skill_mirror;

		# Šî–{“I‚ÉƒvƒŒƒCƒ„[•s—˜‚É‚È‚Á‚Ä‚¢‚é‚ªAæUŒãU‚Å•ª‚¯‚é‚Ì‚à—Ç‚¢‚Ì‚Å‚ÍH
		if ( rand($m_ag * 3) >= rand($y_ag * 3) ) { # ƒvƒŒƒCƒ„[æU
			$who = 'm';
			my $v = &attack;
			if ($y{hp} <= 0 && $m{hp} > 0) { # Ø½¸ÀŞÒ°¼Ş‚Å©•ª‚ªHP0‚É‚È‚Á‚Ä‚à“G‚ÌUŒ‚‚ÉˆÚ‚é«
				&win; # ÌßÚ²Ô°æU‚¾‚©‚ç‚Ü‚¸‚ÍŸ—˜”»’è‚¾‚Æv‚í‚ê‚é
			}
			else {
				$who = 'y';
				&attack;
				if    ($m{hp} <= 0) { &lose; } # ‚³‚ç‚ÉØ½¸ÀŞÒ°¼Ş‚Å‘Šè‚ªHP0‚É‚È‚Á‚Ä‚à‚·‚Å‚É©•ª‚ÍHP0‚È‚Ì‚Å•‰‚¯‚é
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; } # ÌßÚ²Ô°æU‚¾‚©‚çŸ—˜”»’èæ‚É‚µ‚½‚çH
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		else { # NPCæU
			$who = 'y';
			&attack;
			if ($m{hp} <= 0) { # Ø½¸ÀŞÒ°¼Ş‚Å“G‚ªHP0‚É‚È‚Á‚Ä‚à‚±‚Á‚¿‚ÌUŒ‚‚ÉˆÚ‚é«
				&lose; # NPCæU‚¾‚©‚ç‚Ü‚¸‚Í”s–k”»’è‚¾‚Æv‚í‚ê‚é
			}
			else {
				$who = 'm';
				my $v = &attack;
				if    ($m{hp} <= 0) { &lose; } # ‚³‚ç‚ÉØ½¸ÀŞÒ°¼Ş‚Å‚±‚Á‚¿‚ªHP0‚É‚È‚é‚Æ•‰‚¯‚é
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; }
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		$m{turn}++;
	}
	$m{mp} = 0 if $m{mp} < 0;
	$y{mp} = 0 if $y{mp} < 0;
}

#=================================================
# í“¬s“®
#=================================================
sub attack {
	my $temp_y = $who eq 'm' ? 'y' : 'm'; # UŒ‚‘¤‚ğu©•ªv‚Æ‚µ‚½ê‡‚Ìu‘Šèv‚ğİ’è
	my $temp_y_name = ${$temp_y}{name};
	my $skill = ${$who.'_s'} if defined(${$who.'_s'});

	if ($who eq 'm' && $pikorin) { # ]—ˆÈºĞĞ‘Šè‚ÉUŒ‚‚µ‚Ä”ğ‚¯‚ç‚ê‚é‚Æ‹Z‚ğ‘M‚©‚È‚©‚Á‚½ ‘M‚­‚ª“–‚½‚ç‚È‚¢‚ÉC³
		${$who.'_mes'} = "‘M‚¢‚½!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">™‘M‚«!!$m{name}‚Ì$m_s->[1]!!</font><br>|;
	}
	if ($who eq 'y' && $metal) {
		$mes .= "$y{name}‚Í—lq‚ğŒ©‚Ä‚¢‚é<br>";
		return;
	}
	if (${$temp_y.'_gua_avoid'}) { # ‘Šè‚ÌÈºĞĞ”»’è
		$mes .= "$temp_y_name‚Í‚Ğ‚ç‚è‚Æg‚ğ‚©‚í‚µ‚½<br>";
		return;
	}

	my $hit_damage = ${$temp_y}{hp}; # —^‚¦‚½ƒ_ƒ[ƒW‚ğ‚Â
	if (defined($skill)) { # •KE‹Z
		if ($who eq 'm' && $pikorin) { # ]—ˆ’Ê‚è‘M‚¢‚½‹Z‚ÍMPÁ”ï‚à‚È‚¯‚ê‚Î–³Œø‹Z‚È‚Ç‚Ìƒtƒ‰ƒO–³‹
			&{ $skill->[4] }($m_at);
		}
		else {
			# NPC‘¤‚Å¸ÜÊŞ×‚Ì‚¨ç‚è‚ª‹@”\‚µ‚Ä‚È‚¢ ‹­‚·‚¬‚é‚©‚çH
			${$who}{mp} -= $who eq 'm' && $guas[${$who}{gua}][0] eq '6' ? int($skill->[3] / 2) : $skill->[3];
			${$who.'_mes'} = $skill->[5] ? "$skill->[5]" : "$skill->[1]!" unless ${$who.'_mes'};
			$mes .= "${$who}{name}‚Ì$skill->[1]!!<br>";
			if (${$temp_y.'_is_guard'}) { # ‘Šè‚ª–³Œø‹Z
				&{ $skill->[4] }(${$who.'_at'});
				${$temp_y}{hp} = $hit_damage;
			}
			elsif (${$temp_y.'_gua_skill_mirror'}) { # ‘Šè‚ª”½Ë–h‹ï
				&{ $skill->[4] }(${$who.'_at'});
				${$who}{hp} -= $hit_damage - ${$temp_y}{hp};
				$mes .= "‚µ‚©‚µ$guas[${$temp_y}{gua}][1]‚ª‹Z‚ğ”½Ë‚µ ".($hit_damage - ${$temp_y}{hp})." ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½!!<br>";
				${$temp_y}{hp} = $hit_damage;
			}
			else {
				&{ $skill->[4] }(${$who.'_at'});
			}
		}
	}
	else { # UŒ‚
		my $sc = 1;
		if ($guas[${$who}{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		}
		elsif ($guas[${$who}{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "${$who}{name}‚ÌUŒ‚!!";
			my $kaishin_flag = ${$who}{hp} < ${$who}{max_hp} * 0.25 && int(rand(${$who}{hp})) == 0; # 999->249.75 && 0`248 1/249
			$kaishin_flag = int(rand(${$who}{hp} / 10)) == 0 if $guas[${$who}{gua}][0] eq '8'; # 999->99.9 0`98 1/99 ‚È‚ñ‚Æ‚È‚­1/3‚®‚ç‚¢‚Å‰ïS‚Å‚à‚¦‚¦‚ñ‚Å‚È‚¢‚©
			my $gua_mes;
			my $m_at_bf = ${$who.'_at'};
			if ($guas[${$who}{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[${$who}{gua}][1]‚ª‹ì“®‚·‚é!";
				${$who.'_at'} = int(${$who.'_at'} * 1.2);
			}
			elsif ($guas[${$who}{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[${$who}{gua}][1]‚ª–\\‘–‚·‚é!";
				${$who.'_at'} = int(${$who.'_at'} * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin(${$who.'_at'}) : &_attack_normal(${$who.'_at'}, ${$temp_y.'_df'});
			${$who.'_at'} = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if (${$temp_y.'_is_counter'}) {
				$mes .= "UŒ‚‚ğ•Ô‚³‚ê $v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
				${$who}{hp} -= $v;
			}
			elsif (${$temp_y.'_is_stanch'}) {
				$mes .= "½Àİ‚Å“®‚¯‚È‚¢!<br>";
			}
			else {
				$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ";
				$mes .= $who eq 'm' ? '‚ ‚½‚¦‚Ü‚µ‚½<br>' : '‚¤‚¯‚Ü‚µ‚½<br>';
				if ($who eq 'm' && $m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname‚Í‰ó‚ê‚Ä‚µ‚Ü‚Á‚½<br>" if $m{wea_c} == 0;
				}
				${$temp_y}{hp} -= $v;
			}
		}
	}
	$hit_damage -= ${$temp_y}{hp};

	# ‘—“d•‚Íó‚¯‚½ƒ_ƒ[ƒW‚Å‰ñ•œ‚·‚é‚Æv‚Á‚Ä‚½‚¯‚Ç—^‚¦‚½ƒ_ƒ[ƒW‚Å‰ñ•œ‚·‚é •ª‚¯‚Ä‘‚¢‚Ä‚ ‚é‚±‚Æ‚©‚çd—l‚Æv‚í‚ê‚é
	# ¸ÜÊŞ×‚ÍÁ”ïMP”¼Œ¸‚¾‚©‚ç–³Œø‹Z˜A‘Å‚Å‚à‰¶Œbó‚¯‚ç‚ê‚é‚ªA‘—“d•‚Í—^‚¦‚½ƒ_ƒ[ƒW‚ÉˆË‘¶‚·‚é‚Ì‚Å¸ÜÊŞ×‚Ù‚Ç‰¶Œbó‚¯‚È‚¢‚Æv‚í‚ê‚é
	# ‚–£—Í‚ª¿°×İŒ‚‚Á‚Ä‰^‚ª—Ç‚¯‚ê‚Î¸ÜÊŞ×‚æ‚è‚àŒø—¦‚Í—Ç‚¢‚ªc20‚©‚ç18,15‚Æ‚©‚É‚·‚é‚Ì‚ÍH
	if ($guas[${$who}{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "‚ ‚½‚¦‚½ÀŞÒ°¼Ş‚©‚ç MP ‚ğ $v ‹zû‚µ‚Ü‚µ‚½<br>";
		${$who}{mp} += $v;
		${$who}{mp} = ${$who}{max_mp} if ${$who}{mp} > ${$who}{max_mp};
	}

	if (${$temp_y.'_gua_relief'} && $hit_damage) {
		my $v = int($hit_damage / 10);
		$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ";
		$mes .= $who eq 'm' ? '–h‚ª‚ê‚Ü‚µ‚½<br>' : '–h‚¬‚Ü‚µ‚½<br>';
		${$temp_y}{hp} += $v;
	}
	elsif (${$temp_y.'_gua_remain'} && $hit_damage && ${$temp_y}{hp} <= 0) {
		$mes .= "$guas[${$temp_y}{gua}][1]‚ÉUŒ‚‚ª“–‚½‚èŠïÕ“I‚É’v–½‚ğ";
		$mes .= $who eq 'm' ? '‚Ü‚Ê‚ª‚ê‚ç‚ê‚½<br>' : '‚Ü‚Ê‚ª‚ê‚½<br>';
		${$temp_y}{hp} = 1;
	}
	elsif (${$temp_y.'_gua_half_damage'} && $hit_damage) {
		$mes .= "$guas[${$temp_y}{gua}][1]‚ªÀŞÒ°¼Ş‚ğ”¼Œ¸‚³‚¹‚Ü‚µ‚½<br>";
		${$temp_y}{hp} += int($hit_damage / 2);
	}
}

#=================================================
# UŒ‚E–hŒäÌ×¸Ş
#=================================================
sub get_battle_flags { # $who ‚ÅØ‚è‘Ö‚¦ $who = 'm' or $who = 'y'
	return if ($guas[${$who}{gua}][0] eq '21') && ($who ne 'm' || !$pikorin); # ‹¶ím‚ÌŠZ‚ÍUŒ‚‹­§ ‘M‚¢‚Ä‚é‚È‚ç‹¶ím‚ÌŠZ‚Å‚à•KE‹Z
	&{ ${$who.'_s'}->[6] } if defined(${$who.'_s'}); # •KE‹Z‚ÌÌ×¸Ş
	&{ $guas[ ${$who}{gua} ]->[6] } if ${$who}{gua}; # –h‹ï‚ÌÌ×¸Ş
}

#=================================================
# ‰ïSA’ÊíUŒ‚
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>‰ïS‚ÌˆêŒ‚!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# V‹ZK“¾(‚·‚Å‚ÉŠo‚¦‚Ä‚¢‚é‹Z‚Å‚à”­“®) K“¾‚Å1A–¢K“¾‚Å0
#=================================================
sub _learning {
	if (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		# Šo‚¦‚ç‚ê‚é‘®«‚Ì‚à‚Ì‚ğ‘S‚Ä@lines‚É“ü‚ê‚é
		my @lines = ();
		for my $i (1 .. $#skills) {
			push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
		}

		if (@lines) {
			my $no = $lines[int(rand(@lines))];
			# Šo‚¦‚Ä‚¢‚È‚¢‹Z‚È‚ç’Ç‰Á
			my $is_learning = 1;
			for my $m_skill (@m_skills) {
				if ($m_skill eq $no) {
					$is_learning = 0;
					last;
				}
			}
			$m{skills} .= "$no," if $is_learning;
			@m_skills = split /,/, $m{skills};
			$m_s = $skills[ $no ];
			return 1;
		}
		else { # —áŠOˆ—FŠo‚¦‚ç‚ê‚é‚à‚Ì‚ª‚È‚¢
			$m_mes = '‘M‚ß‚«‚»‚¤‚Å‘M‚¯‚È‚¢c';
		}
	}
	return 0;
}

#=================================================
# í“¬—pƒƒjƒ…[
#=================================================
sub battle_menu {
	if($is_smart){
		$menu_cmd .= qq|<table boder=0 cols=5 width=90 height=90>|;

		$menu_cmd .= qq|<tr><td><form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="submit" value="UŒ‚" class="button1s"><input type="hidden" name="cmd" value="0">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|</form>|;
		$menu_cmd .= qq|</td>|;

		for my $i (1 .. $#m_skills+1) {
			if($i % 5 == 0){
				$menu_cmd .= qq|<tr>|;
			}
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			my $mline;
			if(length($skills[ $m_skills[$i-1] ][1])>20){
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10,10). "\n" . substr($skills[ $m_skills[$i-1] ][1],20);
			}elsif(length($skills[ $m_skills[$i-1] ][1])>10) {
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10);
			}else{
				$mline = $skills[ $m_skills[$i-1] ][1];
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 5 == 4){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#m_skills % 5 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;
	}else{
		$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		$menu_cmd .= qq|<option value="0">UŒ‚</option>|;
		for my $i (1 .. $#m_skills+1) { # ºÏİÄŞˆÊ’u ”z—ñ—v‘fˆÊ’u‚Í -1
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
		}
		$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|<input type="submit" value="Œˆ ’è" class="button1"></form>|;
	}
}

#=================================================
# Ÿ—˜
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}‚ğ“|‚µ‚Ü‚µ‚½<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('battle');
	}

	$result = 'win';
}

#=================================================
# ”s–k
#=================================================
sub lose {
	if ($m{name} eq 'nanamie' || $m{name} eq 'QE') {
#		&win;
#		return;
	}

	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}‚Í‚â‚ç‚ê‚Ä‚µ‚Ü‚Á‚½c<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;

	$result = 'lose';
}

#=================================================
# •Ší‚É‚æ‚è“ÁU‚ª‚Â‚­‚©‚Ç‚¤‚©
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}

#=================================================
# –h‹ï‚ª—LŒø‚©‚Ç‚¤‚©
#=================================================
sub is_gua_valid {
	my($gua, $wea) = @_;
	return $guas[$gua][2] eq $weas[$wea][2];
}

#=================================================
# MP‚ª‚ ‚é‚©‚Ç‚¤‚©
#=================================================
sub m_mp_check {
	my $m_s = shift;
	return ($m{mp} >= $m_s->[3] || ($guas[$m{gua}][0] eq '6' && $m{mp} >= int($m_s->[3] / 2)));
}
sub y_mp_check {
	my $y_s = shift;
	return ($y{mp} >= $y_s->[3] || ($guas[$y{gua}][0] eq '6' && $y{mp} >= int($y_s->[3] / 2))); # í“¬s“®‚Å‚ÍŒø‚¢‚Ä‚È‚¢‚ª‚±‚Á‚¿‚Í¸ÜÊŞ×Œø‚¢‚Ä‚é
}

1; # íœ•s‰Â
