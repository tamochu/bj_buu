require "$datadir/skill.cgi";
$is_battle = 1; # ÊŞÄÙÌ×¸Ş1
#================================================
# í“¬ Created by Merino
#================================================

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
if ($y{gua}) {
	if ($m{wea}) {
		if (&is_gua_valid($y{gua},$m{wea})){
			$m_at = int(0.5 *$m_at);
		}
	} else {
		$m_at = int(0.3 *$m_at);
	}
}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})){
			$y_at = int(0.5 *$y_at);
		}
	} else {
		$y_at = int(0.3 *$y_at);
	}
}


#================================================
# Ò²İ“®ì
#================================================
&run_battle;
&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# Àsˆ—
#================================================
sub run_battle {
	if ($cmd eq '') {
		$mes .= 'í“¬ºÏİÄŞ‚ğ‘I‘ğ‚µ‚Ä‚­‚¾‚³‚¢<br>';
	}
	elsif ($m{turn} >= 20) { # ‚È‚©‚È‚©Œˆ’…‚Â‚©‚È‚¢ê‡
		$mes .= 'í“¬ŒÀŠEÀ°İ‚ğ’´‚¦‚Ä‚µ‚Ü‚Á‚½c‚±‚êˆÈã‚Íí‚¦‚Ü‚¹‚ñ<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $y_rand = int(rand(6))-1;
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&y_flag($y_rand);
		my $v = &m_attack;
		
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
			&y_attack($y_rand);
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
		&y_attack($y_rand);
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
			my $v = &m_attack;
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
		$mes .= "<br>ƒ_ƒ[ƒW‚ğMP‚Æ‚µ‚Ä‹zû‚µ‚½<br>";
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
# V‹ZK“¾(‚·‚Å‚ÉŠo‚¦‚Ä‚¢‚é‹Z‚Å‚à”­“®)
#=================================================
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
			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
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
			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
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
}

#=================================================
# ”s–k
#=================================================
sub lose {
	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}‚Í‚â‚ç‚ê‚Ä‚µ‚Ü‚Á‚½c<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;
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
