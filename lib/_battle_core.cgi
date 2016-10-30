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
if    ($guas[$y{gua}][2] =~ /–³|Œ•|•€|‘„/) { $y_df += $guas[$m{gua}][3]; }
elsif ($guas[$y{gua}][2] =~ /‰Š|•—|—‹/)    { $y_mdf+= $guas[$m{gua}][3]; }
# g—p‚·‚é‚Ì‚Í AT or MAT, DF or MDF ‚Ì‚Ç‚¿‚ç‚©
if    ($weas[$m{wea}][2] =~ /–³|Œ•|•€|‘„/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /‰Š|•—|—‹/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y_mdf; }
if    ($weas[$y{wea}][2] =~ /–³|Œ•|•€|‘„/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /‰Š|•—|—‹/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m_mdf; }

$m_ag -= $guas[$m{gua}][5];
$y_ag -= $guas[$y{gua}][5];
if($guas[$m{gua}][0] ne '7'){
	$m_ag -= $weas[$m{wea}][5];
}
$m_ag = int(rand(5)) if $m_ag < 1;
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea},$y{wea})){
		$m_at = int(1.5 *$m_at);
		$y_at = int(0.75*$y_at);
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
		if (&is_gua_valid($y{gua},$m{wea})){
			$m_at = int(0.5 *$m_at);
			$is_y_tokkou2 = 1;
		}
	} else {
		$m_at = int(0.3 *$m_at);
		$is_y_tokkou2 = 1;
	}
}
#else {
#	$m_at = int($m_at * 1.2) if $m{wea};
#}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})){
			$y_at = int(0.5 *$y_at);
			$is_m_tokkou2 = 1;
		}
	} else {
		$y_at = int(0.3 *$y_at);
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
		# –³‰ü‘¢‚Ìó‘Ô‚Æˆá‚Á‚ÄŒãU‚Å‚àæU‚Éæ‚ñ‚¶‚ÄŒø‰Ê‚ğ”­Šö‚·‚éˆ—‚ªÀ‘•‚³‚ê‚½
		# ‚µ‚½‚ª‚Á‚ÄAæUŒãU‚Æ‚¢‚¤‚Ç‚¿‚ç‚ğ—Dæ‚µ‚Äˆ—‚·‚é‚©ˆÈ‘O‚É—¼•û‚Å‚«‚é‚¾‚¯‚Ìˆ—‚ğs‚¤

		local $m_s = undef;
		local $pikorin;
		if (!$metal) { # ÒÀÙ‘Šè‚É‚Íí‚ÉUŒ‚‚Å•KE‹Z‚à‘M‚©‚È‚¢
			$m_s = $skills[ $m_skills[ $cmd - 1 ] ] if $cmd > 0 && $guas[$m{gua}][0] ne '21'; # 1ºÏİÄŞˆÈã‚ğ“ü—Í‚µ‚Ä‚¢‚Ä‹¶ím‚ÌŠZ‚¶‚á‚È‚­ÒÀÙ‘Šè‚¶‚á‚È‚¢‚È‚ç•KE‹Z
			$m_s = undef if defined($m_s) && ($weas[$m{wea}][2] ne $m_s->[2] || !&m_mp_check($m_s)); # •KE‹Z‚ğ‘I‘ğ‚µ‚Ä‚¢‚Ä‚à‘®«‚ªˆá‚Á‚½‚èMP‚ª‘«‚è‚È‚¢‚È‚çUŒ‚
	
			# ‹Z‘M‚¢‚Ä‚àƒtƒ‰ƒO‚ª—§‚½‚È‚¢–â‘è‘Îô ƒtƒ‰ƒO©‘Ì‚ÍæUŒãUŠÖŒW‚È‚¢‚Ì‚Å—\‚ß‘M‚«ˆ—‚ğÏ‚Ü‚¹‚Îƒtƒ‰ƒO—§‚Ä‚ç‚ê‚é
			$pikorin = &_learning if !defined($m_s); # UŒ‚‚Å‹Z‚ğ‘M‚¢‚½‚È‚ç‚Î 1 ‚ª•Ô‚èA‘M‚¢‚½‹Z‚Í $m_s ‚É“ü‚é
		}

		local $y_s = $skills[ $y_skills[ int(rand(6)) - 1 ] ] if $guas[$y{gua}][0] ne '21'; # ‹¶ím‚ÌŠZ‚¶‚á‚È‚¢‚È‚ç•KE‹Z
		$y_s = undef if defined($y_s) && ($weas[$y{wea}][2] ne $y_s->[2] || !&y_mp_check($y_s)); # •KE‹Z‚ğ‘I‘ğ‚µ‚Ä‚¢‚Ä‚à‘®«‚ªˆá‚Á‚½‚èMP‚ª‘«‚è‚È‚¢‚È‚çUŒ‚

=pod
		# UŒ‚ƒtƒ‰ƒO‚â–h‹ïƒtƒ‰ƒO‚à—\‚ß‚±‚±‚ÅÏ‚Ü‚¹‚Ä‚µ‚Ü‚¢‚½‚¢‚ªƒCƒW‚é•”•ª‚ª‘‚¦‚é‚Ì‚Å‚Æ‚è‚ ‚¦‚¸Œ»óˆÛ
		# ƒtƒ‰ƒO—Ş‚ğ‚Ü‚¸‘S•”ô‚¢o‚µ‚Ä‚©‚çˆ—‚·‚ê‚Î•Ï‚È‹““®‚µ‚È‚­‚È‚é
		# —á
		#   –³Œø‹Z‚ğÈºĞĞ‚Å”ğ‚¯‚ç‚ê‚é‚ÆMPÁ”ï‚¹‚¸‚É–³Œø‹Z‚ğ”­Šö‚Å‚«‚é
		#   ½Àİ‹Z‚ğÔÀÉ¶¶ŞĞ‚Å•Ô‚³‚ê‚Ä‚à‘Šè‚É½ÀİŒø‰Ê‚ğ—^‚¦‚é
		# í“¬‚Í $who ‚Å©•ª‚Æ‘Šè‚ğØ‚è‘Ö‚¦‚Ä‚é‚Ì‚Å‚»‚ê“¯—l $who ‚Åí“¬ƒtƒ‰ƒO‚àØ‚è‘Ö‚¦‚é
		local $who = 'm';
		&m_flag2; # ${"$who"."_is_guard"} ¨ $m_is_guard ‚È‚Çƒtƒ‰ƒO“ü‚é
		local $who = 'y';
		$y_flag2; # ${"$who"."_is_guard"} ¨ $y_is_guard ‚È‚Çƒtƒ‰ƒO“ü‚é
=cut

		# Ÿ”s”»’è‚É‚Â‚¢‚Ä‚Í–¢’…è
		# Šî–{“I‚ÉƒvƒŒƒCƒ„[•s—˜‚É‚È‚Á‚Ä‚¢‚é‚ªAæUŒãU‚Å•ª‚¯‚é‚Ì‚à—Ç‚¢‚Ì‚Å‚ÍH
		if ( rand($m_ag * 3) >= rand($y_ag * 3) ) { # ƒvƒŒƒCƒ„[æU
			my $v = &m_attack2;
			if ($y{hp} <= 0 && $m{hp} > 0) { # Ø½¸ÀŞÒ°¼Ş‚Å©•ª‚ªHP0‚É‚È‚Á‚Ä‚à“G‚ÌUŒ‚‚ÉˆÚ‚é«
				&win; # ÌßÚ²Ô°æU‚¾‚©‚ç‚Ü‚¸‚ÍŸ—˜”»’è‚¾‚Æv‚í‚ê‚é
			}
			else {
				&y_attack2;
				if    ($m{hp} <= 0) { &lose; } # ‚³‚ç‚ÉØ½¸ÀŞÒ°¼Ş‚Å‘Šè‚ªHP0‚É‚È‚Á‚Ä‚à‚·‚Å‚É©•ª‚ÍHP0‚È‚Ì‚Å•‰‚¯‚é
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; } # ÌßÚ²Ô°æU‚¾‚©‚çŸ—˜”»’èæ‚É‚µ‚½‚çH
					elsif ($y{hp} <= 0) { &win; }
				}
			}
		}
		else { # NPCæU
			&y_attack2;
			if ($m{hp} <= 0) { # Ø½¸ÀŞÒ°¼Ş‚Å“G‚ªHP0‚É‚È‚Á‚Ä‚à‚±‚Á‚¿‚ÌUŒ‚‚ÉˆÚ‚é«
				&lose; # NPCæU‚¾‚©‚ç‚Ü‚¸‚Í”s–k”»’è‚¾‚Æv‚í‚ê‚é
			}
			else {
				my $v = &m_attack2;
				if    ($m{hp} <= 0) { &lose;  } # ‚³‚ç‚ÉØ½¸ÀŞÒ°¼Ş‚Å‚±‚Á‚¿‚ªHP0‚É‚È‚é‚Æ•‰‚¯‚é
				elsif ($y{hp} <= 0) { &win; }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; }
					elsif ($y{hp} <= 0) { &win; }
				}
			}
		}
		$m{turn}++;
	}
	$m{mp} = 0 if $m{mp} < 0;
	$y{mp} = 0 if $y{mp} < 0;
}

#=================================================
# ©•ª‚ÌUŒ‚
#=================================================
sub m_attack2 {
	&y_flag2;

	if ($pikorin) { # ]—ˆÈºĞĞ‘Šè‚ÉUŒ‚‚µ‚Ä”ğ‚¯‚ç‚ê‚é‚Æ‹Z‚ğ‘M‚©‚È‚©‚Á‚½ ‘M‚­‚ª“–‚½‚ç‚È‚¢‚ÉC³
		$m_mes = "‘M‚¢‚½!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">™‘M‚«!!$m{name}‚Ì$m_s->[1]!!</font><br>|;
	}
	if ($gua_avoid) { # ‘Šè‚ÌÈºĞĞ”»’è
		$mes .= "$y{name}‚Í‚Ğ‚ç‚è‚Æg‚ğ‚©‚í‚µ‚½<br>";
		return;
	}

	local $who = 'm';
	my $hit_damage = $y{hp}; # —^‚¦‚½ƒ_ƒ[ƒW‚ğ‚Â

	if (defined($m_s)) { # •KE‹Z
		if ($pikorin) { # ]—ˆ’Ê‚è‘M‚¢‚½‹Z‚ÍMPÁ”ï‚à‚È‚¯‚ê‚Î–³Œø‹Z‚È‚Ç‚Ìƒtƒ‰ƒO–³‹
			&{ $m_s->[4] }($m_at);
		}
		else {
			$m{mp} -= $guas[$m{gua}][0] eq '6' ? int($m_s->[3] / 2) : $m_s->[3];
			$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
			$mes .= "$m{name}‚Ì$m_s->[1]!!<br>";
			if($is_guard){
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$y{hp} = $pre_yhp;
			} elsif ($gua_skill_mirror) {
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$m{hp} -= $pre_yhp - $y{hp};
				$mes .= "‚µ‚©‚µ$guas[$y{gua}][1]‚ª‹Z‚ğ”½Ë‚µ ".($pre_yhp - $y{hp})." ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½!!<br>";
				$y{hp} = $pre_yhp;
			} else {
				&{ $m_s->[4] }($m_at);
			}
		}
	}
	else { # UŒ‚
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}‚ÌUŒ‚!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0; # 999->249.75 && 0`248 1/249
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0; # 999->99.9 0`98 1/99 ‚È‚ñ‚Æ‚È‚­1/3‚®‚ç‚¢‚Å‰ïS‚Å‚à‚¦‚¦‚ñ‚Å‚È‚¢‚©
			}
			my $gua_mes;
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[$m{gua}][1]‚ª‹ì“®‚·‚é!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$m{gua}][1]‚ª–\\‘–‚·‚é!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "UŒ‚‚ğ•Ô‚³‚ê $v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "½Àİ‚Å“®‚¯‚È‚¢!<br>";
			}
			else {
				$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname‚Í‰ó‚ê‚Ä‚µ‚Ü‚Á‚½<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$hit_damage -= $y{hp};

	# ‘—“d•‚Íó‚¯‚½ƒ_ƒ[ƒW‚Å‰ñ•œ‚·‚é‚Æv‚Á‚Ä‚½‚¯‚Ç—^‚¦‚½ƒ_ƒ[ƒW‚Å‰ñ•œ‚·‚é •ª‚¯‚Ä‘‚¢‚Ä‚ ‚é‚±‚Æ‚©‚çd—l‚Æv‚í‚ê‚é
	# ¸ÜÊŞ×‚ÍÁ”ïMP”¼Œ¸‚¾‚©‚ç–³Œø‹Z˜A‘Å‚Å‚à‰¶Œbó‚¯‚ç‚ê‚é‚ªA‘—“d•‚Í—^‚¦‚½ƒ_ƒ[ƒW‚ÉˆË‘¶‚·‚é‚Ì‚Å¸ÜÊŞ×‚Ù‚Ç‰¶Œbó‚¯‚È‚¢‚Æv‚í‚ê‚é
	# ‚–£—Í‚ª¿°×İŒ‚‚Á‚Ä‰^‚ª—Ç‚¯‚ê‚Î¸ÜÊŞ×‚æ‚è‚àŒø—¦‚Í—Ç‚¢‚ªc20‚©‚ç18,15‚Æ‚©‚É‚·‚é‚Ì‚ÍH
	if ($guas[$m{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "‚ ‚½‚¦‚½ÀŞÒ°¼Ş‚©‚ç MP ‚ğ $v ‹zû‚µ‚Ü‚µ‚½<br>";
		$m{mp} += $v;
		$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ–h‚¬‚Ü‚µ‚½<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $y{hp} <= 0) {
		$mes .= "$guas[$y{gua}][1]‚ÉUŒ‚‚ª“–‚½‚èŠïÕ“I‚É’v–½‚ğ‚Ü‚Ì‚ª‚ê‚½<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$y{gua}][1]‚ªÀŞÒ°¼Ş‚ğ”¼Œ¸‚³‚¹‚Ü‚µ‚½<br>";
		$y{hp} += int($hit_damage / 2);
	}

}

#=================================================
# ‘Šè‚ÌUŒ‚
#=================================================
sub y_attack2 {
	&m_flag2;
	if ($metal) {
		$mes .= "$y{name}‚Í—lq‚ğŒ©‚Ä‚¢‚é";
		return;
	}
	if ($gua_avoid) { # ‘Šè‚ÌÈºĞĞ”»’è
		$mes .= "$m{name}‚Í‚Ğ‚ç‚è‚Æg‚ğ‚©‚í‚µ‚½<br>";
		return;
	}

	local $who = 'y';
	my $hit_damage = $m{hp}; # —^‚¦‚½ƒ_ƒ[ƒW‚ğ‚Â

	if (defined($y_s)) { # •KE‹Z
		$y{mp} -= $y_s->[3]; # NPC‘¤‚Å¸ÜÊŞ×‚Ì‚¨ç‚è‚ª‹@”\‚µ‚Ä‚È‚¢ ‹­‚·‚¬‚é‚©‚çH
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}‚Ì$y_s->[1]!!<br>";

		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
#			$mes .= "$guas[$m{gua}][1]‚ª‹Z‚ğ”½Ë‚·‚é!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$mes .= "‚µ‚©‚µ$guas[$m{gua}][1]‚ª‹Z‚ğ”½Ë‚µ ".($pre_mhp - $m{hp})." ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½!!<br>";
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else { # UŒ‚
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}‚ÌUŒ‚!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $gua_mes;
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes .= "<br>$guas[$y{gua}][1]‚ª‹ì“®‚·‚é!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$y{gua}][1]‚ª–\\‘–‚·‚é!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "UŒ‚‚ğ•Ô‚µ $v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "½Àİ‚Å“®‚¯‚È‚¢!<br>";
			}
			else {
				$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
				$m{hp} -= $v;
			}
		}
	}
	$hit_damage -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "‚ ‚½‚¦‚½ÀŞÒ°¼Ş‚©‚ç MP ‚ğ $v ‹zû‚µ‚Ü‚µ‚½<br>";
		$y{mp} += $v;
		$y{mp} = $y{max_mp} if $y{mp} > $y{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v ‚ÌÀŞÒ°¼Ş‚ğ–h‚¬‚Ü‚µ‚½<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $m{hp} <= 0) {
		$mes .= "$guas[$m{gua}][1]‚ÉUŒ‚‚ª“–‚½‚èŠïÕ“I‚É’v–½‚ğ‚Ü‚Ì‚ª‚ê‚½<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$m{gua}][1]‚ªÀŞÒ°¼Ş‚ğ”¼Œ¸‚³‚¹‚Ü‚µ‚½<br>";
		$m{hp} += int($hit_damage / 2);
	}
}

#=================================================
# ©•ª‚ÌUŒ‚Ì×¸Ş
#=================================================
sub m_flag2 {
	&init_battle_flags;
	return if ($guas[$m{gua}][0] eq '21') && !$pikorin; # ‹¶ím‚ÌŠZ‚ÍUŒ‚‹­§ ‘M‚¢‚Ä‚é‚È‚ç‹¶ím‚ÌŠZ‚Å‚à•KE‹Z

	&{ $m_s->[6] } if defined($m_s); # •KE‹Z

	# –h‹ï‚Ì“Áêƒtƒ‰ƒO
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}

#=================================================
# ‘Šè‚ÌUŒ‚Ì×¸Ş
#=================================================
sub y_flag2 {
	&init_battle_flags;
	return if $guas[$y{gua}][0] eq '21'; # ‹¶ím‚ÌŠZ‚ÍUŒ‚‹­§
	return if $metal;

	&{ $y_s->[6] } if defined($y_s); # •KE‹Z

	# –h‹ï‚Ì“Áêƒtƒ‰ƒO
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
}


#=================================================
# UŒ‚Ì×¸Ş‚Ì‰Šú‰»
#=================================================
sub init_battle_flags {
	$is_guard = 0; # HPƒ_ƒ[ƒW"•KE‹Z"‚Ì–³Œøƒtƒ‰ƒO
	$is_guard_s = 0; # ‚È‚ñ‚Ìƒtƒ‰ƒO‚©•ª‚©‚ç‚ñ
	$gua_relief = 0; # HPƒ_ƒ[ƒW‚ÌŒyŒ¸ƒtƒ‰ƒO
	$gua_remain = 0; # HP0‚Ì‰ñ”ğƒtƒ‰ƒO
	$gua_half_damage = 0; # HPƒ_ƒ[ƒW‚Ì”¼Œ¸ƒtƒ‰ƒO
	$gua_skill_mirror = 0; # "•KE‹Z"‚Ì”½Ëƒtƒ‰ƒO
	$gua_avoid = 0; # s“®‚Ì–³Œøƒtƒ‰ƒO
}

sub run_battle {
=pod
	if ($m{name} eq 'nanamie' || $m{name} eq '') {
		$m{mp} = 999;
		$m{ag} = 548;
		$y{mp} = 999;
		$m{act} = 0;
		$mes .= "m{wea} : $m{wea}, y{wea} : $y{wea}<br>";
		$mes .= "m{gua} : $m{gua}, y{gua} : $y{gua}<br>";
		$mes .= "skill_0 : $y_skills[0], skill_1 : $y_skills[1], skill_2 : $y_skills[2], skill_3 : $y_skills[3], skill_4 : $y_skills[4], skill_-1 : $y_skills[-1]<br><br>";
	}
=cut
	if ($cmd eq '') {
		$mes .= 'í“¬ºÏİÄŞ‚ğ‘I‘ğ‚µ‚Ä‚­‚¾‚³‚¢<br>';
	}
	elsif ($m{turn} >= 20) { # ‚È‚©‚È‚©Œˆ’…‚Â‚©‚È‚¢ê‡
		$mes .= 'í“¬ŒÀŠEÀ°İ‚ğ’´‚¦‚Ä‚µ‚Ü‚Á‚½c‚±‚êˆÈã‚Íí‚¦‚Ü‚¹‚ñ<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $y_rand = int(rand(6))-1;
		# ‹Z‚Í5‚Â‚¾‚¯‚ÇA5”Ô–Ú‚Ì‹Z‚ª‘I‚Î‚ê‚éŠm—¦‚ª‚‚¢(1/6, 1/6, 1/6, 1/6, 1/3)
		# ƒvƒŒƒCƒ„[‚ÌUŒ‚ƒRƒ}ƒ“ƒh•ª‚ÌƒYƒŒC³‚ğƒRƒsƒy‚µ‚½Œ‹‰ÊŠm—¦‚Ì•Î‚è‚ª¶‚¶‚é•s‹ï‡‚©‚Æv‚Á‚½‚ªA
		# ‹Z‚ğ5‚Â‚·‚×‚Ä–„‚ß‚Ä‚È‚¢ê‡‚É‚ÍUŒ‚‚É‚È‚éŠm—¦‚ğã‚°‚é‚æ‚¤‚É‚·‚éˆÓ}‚ª‚ ‚é‚Ì‚©‚à
		# ‚È‚Ì‚ÅA‹Z‚ª‘S•”–„‚Ü‚Á‚Ä‚é‚È‚ç‚Î1/5‚¸‚ÂA‹Z‚ª–„‚Ü‚Á‚Ä‚È‚¢‚È‚ç]—ˆ’Ê‚èUŒ‚‚ğ‚‚ß
		# ‚±‚ñ‚®‚ç‚¢‚Í— ‹Z“I‚È‚±‚Æ‚Æ‚µ‚ÄƒXƒ‹[‚Å‚à—Ç‚¢‚©‚àH
#		my $y_rand = @y_skills >= 5 ? int(rand(5)) : int(rand(6))-1 ; # (-1, 0, 1, 2, 3, 4) -1”Ô–Ú‚Ì—v‘f‚ÍƒPƒc‚È‚Ì‚Å 4 ‚Æ“¯‚¶
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&y_flag($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "y_flag<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		my $v = &m_attack;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "m_attack<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&m_flag;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_flag<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
			}
=cut
			&y_attack($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_attack<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
				$m{hp} = 1 if $m{hp} < 1;
			}
=cut
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		my $y_rand = int(rand(6))-1;
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&m_flag;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "m_flag<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
		}
=cut
		&y_attack($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$m{hp} = 1 if $m{hp} < 1;
			$mes .= "y_attack<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&y_flag($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_flag<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			my $v = &m_attack;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_attack<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# ©•ª‚ÌUŒ‚
#=================================================
sub m_attack {
	if ($gua_avoid) {
		$mes .= "$y{name}‚Í‚Ğ‚ç‚è‚Æg‚ğ‚©‚í‚µ‚½<br>";
		return;
	}
	
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	if ($guas[$m{gua}][0] eq '21') {
		$m_s = undef;
	}
	
	my $guard_pre_hp = $y{hp};
	
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚© # ƒƒ^ƒ‹‘Šè‚¶‚á‚È‚¢‚©
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s) && !$metal) {
		if($guas[$m{gua}][0] eq '6'){
			$m{mp} -= int($m_s->[3] / 2);
		}else{
			$m{mp} -= $m_s->[3];
		}
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}‚Ì$m_s->[1]!!<br>";
		local $who = 'm';
		if($is_guard){
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$y{hp} = $pre_yhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$y{gua}][1]‚ª‹Z‚ğ”½Ë‚·‚é!!<br>";
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$m{hp} -= $pre_yhp - $y{hp};
			$y{hp} = $pre_yhp;
		} else {
			&{ $m_s->[4] }($m_at);
		}
	}
	# ËßºØİ! K“¾‹Z5–¢– ‚©‚Â •ŠíÚÍŞÙ ‚©‚Â ‘Šè‚Ì‹­‚³•’ÊˆÈãª 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0 && !$metal) {
		local $who = 'm';
		&_pikorin;
	}
	else { # UŒ‚
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}‚ÌUŒ‚!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0;
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0;
			}
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$m{gua}][1]‚ª‹ì“®‚·‚é!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$mes .= "<br>$guas[$m{gua}][1]‚ª–\\‘–‚·‚é!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			
			if ($is_counter) {
				$mes .= "<br>UŒ‚‚ğ•Ô‚³‚ê $v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>½Àİ‚Å“®‚¯‚È‚¢!<br>";
			}
			else {
				$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wname‚Í‰ó‚ê‚Ä‚µ‚Ü‚Á‚½<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $y{hp};

	if ($guas[$m{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>ƒ_ƒ[ƒW‚ğMP".int($guard_pre_hp / 20)."‚Æ‚µ‚Ä‹zû‚µ‚½<br>";
		$m{mp} += int($guard_pre_hp / 20);
		if ($m{mp} > $m{max_mp}) {
			$m{mp} = $m{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ–h‚¬‚Ü‚µ‚½<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $y{hp} <= 0) {
		$mes .= "<br>Û¹¯ÄÍßİÀŞİÄ‚ÉUŒ‚‚ª“–‚½‚èŠïÕ“I‚É’v–½‚ğ‚Ü‚Ì‚ª‚ê‚½<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>ƒ_ƒ[ƒW‚ğ”¼Œ¸‚³‚¹‚½<br>";
		$y{hp} += int($guard_pre_hp / 2);
	}
	
}
#=================================================
# ‘Šè‚ÌUŒ‚
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	
	if ($guas[$y{gua}][0] eq '21') {
		$y_s = undef;
	}
	if ($metal) {
		$mes .= "$y{name}‚Í—lq‚ğŒ©‚Ä‚¢‚é";
		return;
	}
	
	if ($gua_avoid) {
		$mes .= "$m{name}‚Í‚Ğ‚ç‚è‚Æg‚ğ‚©‚í‚µ‚½<br>";
		return;
	}
	
	my $guard_pre_hp = $m{hp};
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚©
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}‚Ì$y_s->[1]!!<br>";

		local $who = 'y';
		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$m{gua}][1]‚ª‹Z‚ğ”½Ë‚·‚é!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else {
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}‚ÌUŒ‚!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$y{gua}][1]‚ª‹ì“®‚·‚é!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$mes .= "<br>$guas[$y{gua}][1]‚ª–\\‘–‚·‚é!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;

			if ($is_counter) {
				$mes .= "<br>UŒ‚‚ğ•Ô‚µ $v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>½Àİ‚Å“®‚¯‚È‚¢!<br>";
			}
			else {
				$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
				$m{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>ƒ_ƒ[ƒW‚ğMP‚Æ‚µ‚Ä‹zû‚µ‚½<br>";
		$y{mp} += int($guard_pre_hp / 20);
		if ($y{mp} > $y{max_mp}) {
			$y{mp} = $y{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ–h‚¬‚Ü‚µ‚½<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $m{hp} <= 0) {
		$mes .= "<br>$guas[$m{gua}][1]‚ÉUŒ‚‚ª“–‚½‚èŠïÕ“I‚É’v–½‚ğ‚Ü‚Ì‚ª‚ê‚½<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>ƒ_ƒ[ƒW‚ğ”¼Œ¸‚³‚¹‚½<br>";
		$m{hp} += int($guard_pre_hp / 2);
	}
}

#=================================================
# ©•ª‚ÌUŒ‚Ì×¸Ş
#=================================================
sub m_flag {
	if ($guas[$m{gua}][0] eq '21') {
		return;
	}
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚©
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s)) {
		&{ $m_s->[6] };
	}
	# –h‹ï‚Ì“Áêƒtƒ‰ƒO
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}
#=================================================
# ‘Šè‚ÌUŒ‚Ì×¸Ş
#=================================================
sub y_flag {
	if ($guas[$y{gua}][0] eq '21') {
		return;
	}
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	if ($metal) {
		return;
	}
	
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚©
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		&{ $y_s->[6] };
	}
	# –h‹ï‚Ì“Áêƒtƒ‰ƒO
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
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
			$m_s = $skills[ $no ];
			return 1;
		}
		else { # —áŠOˆ—FŠo‚¦‚ç‚ê‚é‚à‚Ì‚ª‚È‚¢
			$m_mes = '‘M‚ß‚«‚»‚¤‚Å‘M‚¯‚È‚¢c';
		}
	}
	return 0;
}

sub _pikorin {
	# Šo‚¦‚ç‚ê‚é‘®«‚Ì‚à‚Ì‚ğ‘S‚Ä@lines‚É“ü‚ê‚é
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "‘M‚¢‚½!! $skills[$no][1]!";
		# Šo‚¦‚Ä‚¢‚È‚¢‹Z‚È‚ç’Ç‰Á
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">™‘M‚«!!$m{name}‚Ì$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # —áŠOˆ—FŠo‚¦‚ç‚ê‚é‚à‚Ì‚ª‚È‚¢
		$m_mes = '‘M‚ß‚«‚»‚¤‚Å‘M‚¯‚È‚¢c';
	}
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
		for my $i (1 .. $#m_skills+1) {
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
	return ($y{mp} >= $y_s->[3] || ($guas[$y{gua}][0] eq '6' && $y{mp} >= int($y_s->[3] / 2)));
}



1; # íœ•s‰Â
