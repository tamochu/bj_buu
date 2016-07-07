$is_battle = 2;  # ÊŞÄÙÌ×¸Ş2
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
#================================================
# í‘ˆ Created by Merino
#================================================
# $m{value} ‚É‚Í •ºm‚Ì”{—¦

$m{war_select_switch} = 0;

# ˆê‹R‘Å‚¿‚Ì‚Ì‘Šè‚Ì¾ØÌBˆê”Ôæ“ª‚¾‚¯‚ª’f‚è—p‚Ì¾ØÌ(‘Œ¸‰Â”\)
my @answers = ('’f‚é!', '–]‚Ş‚Æ‚±‚ë‚¾!', '•Ô‚è“¢‚¿‚É‚µ‚Ä‚­‚ê‚é!', '‚¢‚´Ÿ•‰!', '‚æ‚©‚ë‚¤!', '‚¢‚¢‚¾‚ë‚¤!', '‘Šè‚É‚È‚ë‚¤!', '‚©‚©‚Á‚Ä‚±‚¢!');

# wŒ`–¼(‘Œ¸•s‰ÂB–¼‘O‚Ì•ÏX‰Â”\)
my @war_forms = ('UŒ‚wŒ`','–hŒäwŒ`','“ËŒ‚wŒ`');

# V‹K‚Ìƒ{[ƒiƒXƒ^ƒCƒ€(í‘ˆŸ—˜”)ƒŠƒ~ƒbƒg
my $new_entry_war_c = 100;
=pod
# ƒ‰ƒ“ƒ_ƒ€ƒZƒŒƒNƒg—pƒRƒ}ƒ“ƒh‘Ş”ğ
my $m_cmd = $cmd;
if (!$m{war_select_switch} && $m_cmd >= 0 && $m_cmd <= 2) {
	while (1) {
		$m_cmd = int(rand(3));
		if ($m{rest_a} + $m{rest_b} + $m{rest_c} <= 0) {
			last;
		}
		if ($m_cmd eq '0' && $m{rest_a} > 0) {
			last;
		}
		if ($m_cmd eq '1' && $m{rest_b} > 0) {
			last;
		}
		if ($m_cmd eq '2' && $m{rest_c} > 0) {
			last;
		}
	}
}
=cut
#================================================
# —˜—pğŒ
#================================================
sub is_satisfy {
	if ($time < $w{reset_time}) {
		$mes .= 'IíŠúŠÔ‚È‚Ì‚Åí‘ˆ‚ğ’†~‚µ‚Ü‚·<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!defined $cs{strong}[$y{country}]) {
		$mes .= 'U‚ß‚Ä‚¢‚é‘‚ÍÁ–Å‚µ‚Ä‚µ‚Ü‚Á‚½‚Ì‚ÅAí‘ˆ‚ğ’†~‚µ‚Ü‚·<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub tp_100 {
	$mes .= "$c_y‚É’…‚«‚Ü‚µ‚½<br>";
	
	my $is_ambush = &_get_war_you_data; # ‘Ò‚¿•š‚¹‚³‚ê‚Ä‚½ê‡–ß‚è’l‚ ‚è
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};

	# ŒÀŠEÀ°İ”Œˆ’è
	$m{turn} = int( rand(6)+7 );
	if ($m{value} > 1) {
		$m{turn} += 3;
		$y{sol} = int($rank_sols[$y{rank}]);
	}
	else {
		$y{sol} = int($rank_sols[$y{rank}] * $m{value});
	}

	# •º‚ª‘«‚è‚È‚¢
	if ($y{sol} > $cs{soldier}[$y{country}]) {
		$mes .= "$c_y‚Í•º•s‘«‚Ì‚æ‚¤‚¾c<br>‹Ù‹}‚ÉŠñ‚¹W‚ß‚Ì‘–¯‚ª¢W‚³‚ê‚½<br>";
		$cs{strong}[$y{country}] -= int(rand(100)+100);
		$cs{strong}[$y{country}] = 1 if $cs{strong}[$y{country}] < 1;
		$y{sol_lv} = int( rand(10) + 45 );
		&write_cs;
	}
	else {
		$cs{soldier}[$y{country}] -= int($y{sol} / 3);
		$y{sol_lv} = 80;
		&write_cs;
	}

	# ‘Ò‚¿•š‚¹
	if (($pets[$m{pet}][2] ne 'no_ambush' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && $is_ambush) {
		$mes .= "$c_y‚Ì$y{name}—¦‚¢‚é$y{sol}‚Ì$units[$y{unit}][1]‚ª‘Ò‚¿•š‚¹‚µ‚Ä‚¢‚Ü‚µ‚½!<br>";
		if ($y{unit} eq '11') { # ˆÃE•”‘à
			my $v = int( $m{sol} * (rand(0.2)+0.2) );
			$m{sol} -= $v;
			$m{sol_lv} = int( rand(15) + 15 ); # 15 ` 29
			$mes .= "$units[$y{unit}][1]‚É‚æ‚éˆÃE‚ÅA$v‚Ì•º‚ª‚â‚ç‚ê‚Ü‚µ‚½!<br>";
		}
		elsif ($y{unit} eq '14') { # Œ¶‰e•”‘à
			$m{sol_lv} = int( rand(10) + 5 ); # 5 ` 14
			$mes .= "$units[$y{unit}][1]‚É‚æ‚éŒ¶p‚ÅA•ºm’B‚Í¬—‚µ‘å‚«‚­m‹C‚ª‰º‚ª‚è‚Ü‚µ‚½!<br>";
		}
		else {
			$m{sol_lv} = int( rand(15) + 10 ); # 10 ` 24
			$mes .= "‘Ò‚¿•š‚¹‚É‚æ‚è•ºm’B‚Í¬—‚µ‘å‚«‚­m‹C‚ª‰º‚ª‚è‚Ü‚µ‚½!<br>";
		}
		if ($pets[$y{pet}][2] eq 'no_single' && $w{world} ne '17') {
			$y{wea} = 'no_single';
			$y{sol_lv} = int( rand(10) + 5);
			$mes .= "$pets[$y{pet}][1]‚Ì—Í‚Åâ‘Î‚Éˆê‹R‘Å‚¿‚É‚Í‚È‚è‚Ü‚¹‚ñ‚ª•º‚Ìm‹C‚Í‰º‚ª‚Á‚Ä‚¢‚Ü‚·<br>";
		}
		&write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉU‚ß‚İ$y{name}‚Ì‘Ò‚¿•š‚¹‚É‚ ‚¢‚Ü‚µ‚½");
		
		&c_up('tam_c');

		my $yid = unpack 'H*', $y{name};
		if (-d "$userdir/$yid") {
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			if ($m{super_rank}){
				$rank_name = '';
				$rank_name .= 'š' for 1 .. $m{super_rank};
				$rank_name .= $m{rank_name};
			}
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}/$rank_name/$units[$m{unit}][1]/“—¦$m{lea}($date)<>";
			close $fh;
		}
	}
	else {
		$m{sol_lv} = 80;
		$mes .= "$c_y‚©‚ç$y{name}—¦‚¢‚é$y{sol}‚Ì•º‚ªo‚Ä‚«‚Ü‚µ‚½<br>";
	}

	# ‰‡ŒRŒnÍß¯Ä
	if ($w{world} ne '17') {
		&use_pet('war_begin');
	}
	# “¯–¿‚µ‚Ä‚¢‚é‘‚©‚ç‚Ì‰‡ŒR
	if ($union) {
		my $v = int( $m{sol} * (rand(0.1)+0.1) );
		$m{sol} += $v;
		$mes .= "‚È‚ñ‚ÆA$cs{name}[$union]‚©‚ç$v•º‚Ì‰‡ŒR‚ª‹ì‚¯‚Â‚¯‚½!<br>";
	}
=pod
	# ”z”v
	if ($m{war_select_switch}) {
		$m{rest_a} = 0;
		$m{rest_b} = 0;
		$m{rest_c} = 0;
		$y{rest_a} = 0;
		$y{rest_b} = 0;
		$y{rest_c} = 0;
		
		my $idx = 0;
		for my $cnt (1..$m{turn}) {
			unless ($units[$m{unit}][7][$idx]) {
				$idx = 0;
			}
			
			if ($units[$m{unit}][7][$idx] eq '1') {
				$m{rest_a}++;
			} elsif ($units[$m{unit}][7][$idx] eq '2') {
				$m{rest_b}++;
			} elsif ($units[$m{unit}][7][$idx] eq '3') {
				$m{rest_c}++;
			} else {
				if (rand(3) < 1) {
					$m{rest_a}++;
				} elsif (rand(2) < 1) {
					$m{rest_b}++;
				} else {
					$m{rest_c}++;
				}
			}
			$idx++;
		}
		$idx = 0;
		for my $cnt (1..$m{turn}) {
			unless ($units[$y{unit}][7][$idx]) {
				$idx = 0;
			}
			
			if ($units[$y{unit}][7][$idx] eq '1') {
				$y{rest_a}++;
			} elsif ($units[$y{unit}][7][$idx] eq '2') {
				$y{rest_b}++;
			} elsif ($units[$y{unit}][7][$idx] eq '3') {
				$y{rest_c}++;
			} else {
				if (rand(3) < 1) {
					$y{rest_a}++;
				} elsif (rand(2) < 1) {
					$y{rest_b}++;
				} else {
					$y{rest_c}++;
				}
			}
			$idx++;
		}
	} else {
		$m{rest_a} = $m{turn};
		$m{rest_b} = $m{turn};
		$m{rest_c} = $m{turn};
		$y{rest_a} = $m{turn};
		$y{rest_b} = $m{turn};
		$y{rest_c} = $m{turn};
	}
=cut
	if ($config_test) {
		$y{sol} /= 10;
	}
	
	$m{tp} += 10;
	&n_menu;
}

#================================================
sub tp_110 {
	$is_battle = 2;
	$m{act} += int(rand($m{turn})+$m{turn});
	
	$mes .= "¡‰ñ‚Ììí‚ÌŒÀŠEÀ°İ‚Í $m{turn} À°İ‚Å‚·<br>";
	$mes .= "$m{name}ŒR $m{sol}l VS $y{name}ŒR $y{sol}l<br>";
	$mes .= 'U‚ß‚ŞwŒ`‚ğ‘I‚ñ‚Å‚­‚¾‚³‚¢<br>';
#	$mes .= "©•ª $war_forms[0]:$m{rest_a}‰ñ $war_forms[1]:$m{rest_b}‰ñ $war_forms[2]:$m{rest_c}‰ñ<br>";
#	$mes .= "‘Šè $war_forms[0]:$y{rest_a}‰ñ $war_forms[1]:$y{rest_b}‰ñ $war_forms[2]:$y{rest_c}‰ñ<br>";
	&menu(@war_forms,'‘Ş‹p');
	
	$m{tp} += 10;
	&write_cs;
}

#================================================
sub tp_120 { &tp_190; } # tp120‚¾‚Æ‘Ş‹p‰Â
sub tp_130 { &tp_190; } # tp130‚¾‚Æˆê‹R‘Å‚¿‰Â
sub tp_140 { # ˆê‹R‘Å‚¿
	require './lib/war_battle.cgi';

	if ($m{hp} <= 0) {
		$mes .= "ˆê‹R‘Å‚¿‚É”s‚êwŠöŠ¯‚ğ¸‚Á‚½$m{name}‚Ì•”‘à‚ÍíˆÓ‚ğ‘r¸‚µA“GŒR‚©‚ç‚Ì’ÇŒ‚‚ğ‚¤‚¯‘S–Å‚µ‚Ü‚µ‚½c<br>";
		&write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉNUA$y{name}‚Æˆê‹R“¢‚¿‚ğ‰‰‚¶‚é‚ª”s–k‚µ•”‘à‚Í”s‘–‚µ‚½‚æ‚¤‚Å‚·");
		&war_lose;
	}
	elsif ($y{hp} <= 0) {
		$mes .= "“GŒR‚Í$y{name}‚Ì”s–k‚ÉíˆÓ‚ğ‘r¸‚µ‚Ü‚µ‚½I«‚ğŒ‡‚¢‚½•”‘à‚È‚Ç“G‚Å‚Í‚ ‚è‚Ü‚¹‚ñ<br>“GŒR‚ğ’ÇŒ‚‚µA‚©‚È‚è‚Ì”íŠQ‚ğ—^‚¦‚Ü‚µ‚½I<br>";
		&war_win(1);

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('single');
		}
	}
}

#================================================
# Ù°ÌßÒÆ­° À°İI—¹‚©Ÿ‚Â‚©•‰‚¯‚é‚©‚Ü‚Å
#================================================
sub loop_menu {
	$is_battle = 2;
	$mes .= "c‚è$m{turn} À°İ<br>";
	$mes .= "$m{name}ŒR $m{sol}l VS $y{name}ŒR $y{sol}l<br>";
	$mes .= 'U‚ß‚ŞwŒ`‚ğ‘I‚ñ‚Å‚­‚¾‚³‚¢<br>';
#	$mes .= "©•ª $war_forms[0]:$m{rest_a}‰ñ $war_forms[1]:$m{rest_b}‰ñ $war_forms[2]:$m{rest_c}‰ñ<br>";
#	$mes .= "‘Šè $war_forms[0]:$y{rest_a}‰ñ $war_forms[1]:$y{rest_b}‰ñ $war_forms[2]:$y{rest_c}‰ñ<br>";
	&menu(@war_forms);
}
=pod
sub _rest_check {
	if ($m{rest_a} + $m{rest_b} + $m{rest_c} > 0) {
		if ($m_cmd eq '0' && $m{rest_a} <= 0) {
			$mes .= 'c‚è‰ñ”‚ª‚ ‚è‚Ü‚¹‚ñ<br>';
			return 0;
		}
		if ($m_cmd eq '1' && $m{rest_b} <= 0) {
			$mes .= 'c‚è‰ñ”‚ª‚ ‚è‚Ü‚¹‚ñ<br>';
			return 0;
		}
		if ($m_cmd eq '2' && $m{rest_c} <= 0) {
			$mes .= 'c‚è‰ñ”‚ª‚ ‚è‚Ü‚¹‚ñ<br>';
			return 0;
		}
	}
	return 1;
}
=cut
sub tp_190 {
#	if ($m_cmd >= 0 && $m_cmd <= 2 && &_rest_check) {
	if ($cmd >= 0 && $cmd <= 2) {
		--$m{turn};
=pod
		if ($m_cmd eq '0') {
			$m{rest_a}--;
		}
		if ($m_cmd eq '1') {
			$m{rest_b}--;
		}
		if ($m_cmd eq '2') {
			$m{rest_c}--;
		}
=cut
		$mes .= "c‚è$m{turn}À°İ<br>";
		&_crash;
		
		if ($m{sol} <= 0 && $y{sol} <= 0) {
			$mes .= "—¼ŒR‚Æ‚à‚É‰ó–Å“I‘¹ŠQ‚ğó‚¯í“¬Œp‘±‚ª•s‰Â”\\‚Æ‚È‚è‚Ü‚µ‚½<br>$e2j{strong}‚Í—¼w‰c‚Æ‚à•Ï‰»‚È‚µ<br>";
			$m{value} < 1
				? &write_world_news("‰½Ò‚©‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚É‘j‚Ü‚êŒƒí‚Ì––A—¼ŒR‰ó–Å‚µ‚½‚æ‚¤‚Å‚·")
				: &write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚É‘j‚Ü‚êŒƒí‚Ì––A—¼ŒR‰ó–Å‚µ‚½‚æ‚¤‚Å‚·")
				;

			&war_draw;
		}
		elsif ($m{sol} <= 0) {
			$mes .= '‰ä‚ªŒR‚Í‘S–Å‚µ‚Ü‚µ‚½B“P‘Ş‚µ‚Ü‚·c<br>';
			$m{value} < 1
				? &write_world_news("‰½Ò‚©‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚Ì‘O‚É”s‘Ş‚µ‚½‚æ‚¤‚Å‚·")
				: &write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚Ì‘O‚É”s‘Ş‚µ‚½‚æ‚¤‚Å‚·")
				;

			&war_lose;
		}
		elsif ($y{sol} <= 0) {
			$mes .= '“G•”‘à‚ğŒ‚”j‚µ‚Ü‚µ‚½!!‰ä‚ªŒR‚ÌŸ—˜‚Å‚·!<br>';
			&war_win;
		}
		elsif ($m{turn} <= 0) {
			$mes .= "í“¬ŒÀŠEÀ°İ‚ğ’´‚¦‚Ä‚µ‚Ü‚Á‚½c‚±‚êˆÈã‚Íí‚¦‚Ü‚¹‚ñ<br>$e2j{strong}‚Í—¼w‰c‚Æ‚à•Ï‰»‚È‚µ<br>";
			$m{value} < 1
				? &write_world_news("‰½Ò‚©‚ª$c_y‚ÉNU‚µA$y{name}‚Ì•”‘à‚É‘j‚Ü‚êí“¬ŒÀŠE‚ğµ°ÊŞ°‚µ‚½‚æ‚¤‚Å‚·")
				: &write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉNU‚µA$y{name}‚Ì•”‘à‚É‘j‚Ü‚êí“¬ŒÀŠE‚ğµ°ÊŞ°‚µ‚½‚æ‚¤‚Å‚·")
				;

			&war_draw;
		}
		else {
			$mes .= 'U‚ß‚ŞwŒ`‚ğ‘I‚ñ‚Å‚­‚¾‚³‚¢<br>';
#			$mes .= "©•ª $war_forms[0]:$m{rest_a}‰ñ $war_forms[1]:$m{rest_b}‰ñ $war_forms[2]:$m{rest_c}‰ñ<br>";
#			$mes .= "‘Šè $war_forms[0]:$y{rest_a}‰ñ $war_forms[1]:$y{rest_b}‰ñ $war_forms[2]:$y{rest_c}‰ñ<br>";

			# ˆê‹R‘Å‚¿oŒ»Šm—§
			if ($y{wea} eq 'no_single') {
				&menu(@war_forms,'‘Ş‹p');
				$m{tp} = 120;
			}
			elsif ( ((($pets[$m{pet}][2] eq 'war_single' && $w{world} ne '17') && int(rand($m{turn}+3)) == 0) || int(rand($m{turn}+15)) == 0 || ($pets[$y{pet}][2] eq 'ambush_single' && $w{world} ne '17')) && $m{unit} ne '18') {
				&menu(@war_forms,'ˆê‹R‘Å‚¿');
				$m{tp} = 130;
			}
			elsif ($m{turn} < 4)  {
				&menu(@war_forms);
			}
			else {
				&menu(@war_forms,'‘Ş‹p');
				$m{tp} = 120;
			}
		}
	}
#	elsif ($m_cmd eq '3' && $m{tp} eq '120') {
	elsif ($cmd eq '3' && $m{tp} eq '120') {
		$m_mes = '‘SŒR‘Ş‹p!!';

		if ($m{turn} < 5) {
			$mes .= '“GŒR‚É“¦‘–‘Ş˜H‚ğÇ‚ª‚êA‚à‚Í‚â“P‘Ş‚Í•s‰Â”\\‚Å‚·<br>';
			$m{tp} = 190;
			&loop_menu;
		}
		# ‘Ş‹p‚Å‚«‚éŠm—§
		elsif ( int(rand($m{turn})) == 0) {
			$mes .= 'c”O‚Å‚·‚ªìí‚ğ’†~‚µ‘Ş‹p‚µ‚Ü‚·<br>';
			$m{value} < 1
				? &write_world_news("‰½Ò‚©‚ª$c_y‚ÉNU‚µA$y{name}‚Ì•”‘à‚ÆŒğíB—]‹V‚È‚­“P‘Ş‚µ‚½–Í—l")
				: &write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚ÉNU‚µA$y{name}‚Ì•”‘à‚ÆŒğíB—]‹V‚È‚­“P‘Ş‚µ‚½–Í—l")
				;

			&war_escape;
		}
		else {
			$mes .= '‘Ş‹p‚É¸”s‚µ‚Ü‚µ‚½<br>';
			$m{tp} = 190;
			&loop_menu;
		}
	}
#	elsif ($m_cmd eq '3' && $m{tp} eq '130') {
	elsif ($cmd eq '3' && $m{tp} eq '130') {
		$m_mes = "$y{name}‚Æˆê‹R‘Å‚¿Šè‚¢‚½‚¢!";

		my $v = int(rand(@answers));

		if ($v <= 0) {
			$y_mes = $answers[$v];
			$mes .= 'ˆê‹R‘Å‚¿‚ğ’f‚ç‚ê‚Ü‚µ‚½<br>';
			&loop_menu;
			$m{tp} = 190;
		}
		else {
			$y_mes = $answers[$v];
			
			$mes .= "$y{name}‚Éˆê‹R‘Å‚¿‚ğ\\‚µ‚İA‚±‚Ìí‚¢‚ÌŸ”s‚ğ‰Ë‚¯‚½ˆê‹R“¢‚¿‚ğs‚È‚¤–‚É!<br>";
			$m{tp} = 140;
			&n_menu;
		}
	}
	else {
		&loop_menu;
		$m{tp} = 190;
	}
}

#================================================
# wŒ`íŒ‹‰Ê
#================================================
=pod
sub _ai {
	my @y_cmds = (0, 1, 2);
	my $y_cmd;

	if ($m{rest_a} + $m{rest_b} <= 0){
		if ($y{rest_b} > 0) {
			@y_cmds = (1);
		} elsif ($y{rest_c} > 0) {
			@y_cmds = (2);
		}
	} elsif ($m{rest_b} + $m{rest_c} <= 0) {
		if ($y{rest_c} > 0) {
			@y_cmds = (2);
		} elsif ($y{rest_a} > 0) {
			@y_cmds = (0);
		}
	} elsif ($m{rest_c} + $m{rest_a} <= 0) {
		if ($y{rest_a} > 0) {
			@y_cmds = (0);
		} elsif ($y{rest_b} > 0) {
			@y_cmds = (1);
		}
	} elsif ($m{rest_a} <= 0 && $y{rest_a} + $y{rest_b} > 0) {
		@y_cmds = (0, 1);
	} elsif ($m{rest_b} <= 0 && $y{rest_b} + $y{rest_c} > 0) {
		@y_cmds = (1, 2);
	} elsif ($m{rest_c} <= 0 && $y{rest_c} + $y{rest_a} > 0) {
		@y_cmds = (0, 2);
	}

	while (1) {
		$y_cmd = $y_cmds[int(rand(@y_cmds))];
		if ($y{rest_a} + $y{rest_b} + $y{rest_c} <= 0) {
			last;
		}
		if ($y_cmd eq '0' && $y{rest_a} > 0) {
			last;
		}
		if ($y_cmd eq '1' && $y{rest_b} > 0) {
			last;
		}
		if ($y_cmd eq '2' && $y{rest_c} > 0) {
			last;
		}
	}
	return $y_cmd;
}
=cut
sub _crash {
=pod
	my $y_cmd = &_ai;
	if ($y_cmd eq '0') {
		$y{rest_a}--;
	}
	if ($y_cmd eq '1') {
		$y{rest_b}--;
	}
	if ($y_cmd eq '2') {
		$y{rest_c}--;
	}
	
	$m_mes = $war_forms[$m_cmd];
	$y_mes = $war_forms[$y_cmd];
=cut
	my $y_cmd = int(rand(3));

	$m_mes = $war_forms[$cmd];
	$y_mes = $war_forms[$y_cmd];

	my $result = 'lose';
#	if ($m_cmd eq '0') {
	if ($cmd eq '0') {
		$result = $y_cmd eq '1' ? 'win'
				: $y_cmd eq '2' ? 'lose'
				:				  'draw'
				;
	}
#	elsif ($m_cmd eq '1') {
	elsif ($cmd eq '1') {
		$result = $y_cmd eq '2' ? 'win'
				: $y_cmd eq '0' ? 'lose'
				:				  'draw'
				;
	}
#	elsif ($m_cmd eq '2') {
	elsif ($cmd eq '2') {
		$result = $y_cmd eq '0' ? 'win'
				: $y_cmd eq '1' ? 'lose'
				:				  'draw'
				;
	}
	
	my $m_lea = $m{lea};
	my $y_lea = $y{lea};
	my $m_min_wea;
	if($weas[$m{wea}][2] eq 'Œ•'){
		$m_min_wea = 1;
	}elsif($weas[$m{wea}][2] eq '‘„'){
		$m_min_wea = 6;
	}elsif($weas[$m{wea}][2] eq '•€'){
		$m_min_wea = 11;
	}elsif($weas[$m{wea}][2] eq '‰Š'){
		$m_min_wea = 16;
	}elsif($weas[$m{wea}][2] eq '•—'){
		$m_min_wea = 21;
	}elsif($weas[$m{wea}][2] eq '—‹'){
		$m_min_wea = 26;
	}elsif($m{wea} == 0){
		$m_min_wea = 0;
	}else{
		$m_min_wea = 33;
	}
	my $y_min_wea;
	if($weas[$y{wea}][2] eq 'Œ•'){
		$y_min_wea = 1;
	}elsif($weas[$y{wea}][2] eq '‘„'){
		$y_min_wea = 6;
	}elsif($weas[$y{wea}][2] eq '•€'){
		$y_min_wea = 11;
	}elsif($weas[$y{wea}][2] eq '‰Š'){
		$y_min_wea = 16;
	}elsif($weas[$y{wea}][2] eq '•—'){
		$y_min_wea = 21;
	}elsif($weas[$y{wea}][2] eq '—‹'){
		$y_min_wea = 26;
	}else{
		$y_min_wea = 33;
	}
	$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
	$m_wea_modify -= 100 unless $m{wea};
	$m_wea_modify = 100 if ($m{wea} == 14);
	$m_wea_modify = 0 if ($m{wea} == 31);
	$m_wea_modify = 100 if ($m{wea} == 32);
	$m_lea += $m_wea_modify;
	$m_lea =  0 if ($m_lea < 0);
	$y_wea_modify = $weas[$y{wea}][5] - $weas[$y_min_wea][5];
	$y_wea_modify -= 100 unless $y{wea};
	$y_wea_modify = 100 if ($y{wea} == 14);
	$y_wea_modify = 0 if ($y{wea} == 31);
	$y_wea_modify = 100 if ($y{wea} == 32);
	$y_lea += $y_wea_modify;
	$y_lea -= 100 unless $y{wea};
	$y_lea =  0 if ($y_lea < 0);
	
	my $m_attack = ($m{sol}*0.1 + $m_lea*2) * $m{sol_lv} * 0.01 * $units[$m{unit}][4] * $units[$y{unit}][5];
	my $y_attack = ($y{sol}*0.1 + $y_lea*2) * $y{sol_lv} * 0.01 * $units[$y{unit}][4] * $units[$m{unit}][5];

	if (&is_tokkou($m{unit}, $y{unit})) {
		$is_m_tokkou = 1;
		$m_attack *= 1.3;
		$y_attack *= 0.5;
	}
	if (&is_tokkou($y{unit}, $m{unit})) {
		$is_y_tokkou = 1;
		$m_attack *= 0.5;
		$y_attack *= 1.3;
	}
	$m_attack = $m_attack < 150 ? int( rand(50)+100 ) : int( $m_attack * (rand(0.3) +0.9) );
	$y_attack = $y_attack < 150 ? int( rand(50)+100 ) : int( $y_attack * (rand(0.3) +0.9) );
	
	if ($result eq 'win') {
		$m_attack = int($m_attack * 1.3);
		$y_attack = int($y_attack * 0.5);
		
		$m{sol_lv} += int(rand(5)+10);
		$y{sol_lv} -= int(rand(5)+10);

		$mes .= qq|›©ŒR”íŠQ$y_attack <font color="#FF0000">œ“GŒR”íŠQ$m_attack</font><br><br>|;
	}
	elsif ($result eq 'lose') {
		$m_attack = int($m_attack * 0.5);
		$y_attack = int($y_attack * 1.3);
		$m{sol_lv} -= int(rand(5)+10);
		$y{sol_lv} += int(rand(5)+10);
	
		$mes .= qq|<font color="#FF0000">›©ŒR”íŠQ$y_attack</font> œ“GŒR”íŠQ$m_attack<br><br>|;
	}
	else {
		$m{sol_lv} += int(rand(3)+5);
		$y{sol_lv} += int(rand(3)+5);
	
		$mes .= qq|›©ŒR”íŠQ$y_attack œ“GŒR”íŠQ$m_attack<br><br>|;
	}
	
	$m{sol} -= $y_attack;
	$y{sol} -= $m_attack;
	$m{sol} = 0 if $m{sol} < 0;
	$y{sol} = 0 if $y{sol} < 0;

	$m{sol_lv} = $m{sol_lv} < 10  ? int( rand(11) )
			   : $m{sol_lv} > 100 ? 100
			   :					$m{sol_lv}
			   ;
	$y{sol_lv} = $y{sol_lv} < 10  ? int( rand(11) )
			   : $y{sol_lv} > 100 ? 100
			   :					$y{sol_lv}
			   ;
}


#================================================
# ŠK‹‰‚Æ“—¦‚ª“¯‚¶‚­‚ç‚¢‚Ì‘Šè‚ğƒ‰ƒ“ƒ_ƒ€‚Å’T‚·BŒ©‚Â‚©‚ç‚È‚¢ê‡‚Í—pˆÓ‚³‚ê‚½NPC
#================================================
sub _get_war_you_data {
	my @lines = &get_country_members($y{country});
	
	my $war_mod = &get_modify('war');
	
	if (@lines >= 1) {
		my $retry = ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000      ? 0 # ¢ŠEî¨y“S•ÇzU‚ß‚½‘‚Ì‘—Í‚ª3000ˆÈ‰º‚Ìê‡‚Í‹­§NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # ¢ŠEî¨yˆÃ•zU‚ß‚½‘‚ªNPC‘‚È‚çÌßÚ²Ô°Ï¯Áİ¸Ş‚Í‚P‰ñ
				  : $w{world} eq $#world_states - 5 ? 3 # ¢ŠEî¨yÙ‘¬zÌßÚ²Ô°Ï¯Áİ¸Ş‚Í3‰ñ
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 15 && $w{world} ne '17') ? 	1
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && $w{world} ne '17') ? 	2
				  :																5 # ‚»‚Ì‘¼ÌßÚ²Ô°Ï¯Áİ¸Ş‚ğÅ‚‚T‰ñ‚Ù‚ÇØÄ×²‚·‚é
				  ;
		$retry = int($retry / $war_mod);
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # “¯‚¶l‚È‚çŸ
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp —]•ª‚È‰üsíœ
			
			my $y_id = unpack 'H*', $lines[$c];
			
			# ‚¢‚È‚¢ê‡‚ÍØ½Ä‚©‚çíœ
			unless (-f "$userdir/$y_id/user.cgi") {
				require "./lib/move_player.cgi";
				&move_player($lines[$c], $y{country},'del');
				next;
			}
			my %you_datas = &get_you_datas($y_id, 1);
			
			$y{name} = $you_datas{name};
			
			next if $you_datas{lib} eq 'prison'; # ˜S–‚Ìl‚Íœ‚­
			next if $you_datas{lib} eq 'war'; # í‘ˆ‚Éo‚Ä‚¢‚él‚Íœ‚­
			next if ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 20 && $w{world} ne '17'); # š20Ì§İÄÑ
			
			if ($m{win_c} < $new_entry_war_c) {
				if ( $m{rank} >= ($you_datas{rank} + int(rand(2)) ) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} elsif ($cs{disaster}[$y{country}] eq 'mismatch' && $cs{disaster_limit}[$y{country}] >= $time) {
				# wŠöŒn“¬—
				if ( $you_datas{rank} <= $m{rank}) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} else {
				# ‘Ò‚¿•š‚¹‚µ‚Ä‚¢‚él‚ª‚¢‚½‚ç
				if ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 1;
				}
				# ŠK‹‰‚Æ“—¦‚ª‹ß‚¢lB¶‚Ì”š‚ğ0‚É‚·‚ê‚Î‚æ‚è‹­‚³‚Ì‹ß‚¢‘Šè‘å‚«‚­‚·‚ê‚ÎFX‚È‘Šè
				elsif ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			}
		}
	}
	
	# ¼¬ÄŞ³ or NPC
	($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17') || int(rand(3 / $war_mod)) == 0 || ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7'))
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] ` [4] ‚Ì 5l([0]‹­‚¢ >>> [4]ã‚¢)
#================================================
sub _get_war_npc_data {
	&error("‘Šè‘($y{country})‚ÌNPCƒf[ƒ^‚ª‚ ‚è‚Ü‚¹‚ñ") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	my $war_mod = &get_modify('war');
	
	require "$datadir/npc_war_$y{country}.cgi";

	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2) * $war_mod)
		  : $m{lea} > 250 ? int((rand(2)+1) * $war_mod)
		  : $m{lea} > 120 ? int((rand(2)+2) * $war_mod)
		  :                 int((rand(2)+3) * $war_mod)
		  ;
	if($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17'){
		$v += int(rand($m{pet_c}*0.2));
	}

	# “ˆê‘‚Ìê‡‚ÍNPCã‘Ì
	my($c1, $c2) = split /,/, $w{win_countries};
	# ‘—Í’á‚¢ê‡‚Í‹­‚¢NPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country}) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		unless($k eq 'name' && $pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && rand(2) < 1){
			$y{$k} = $v;
		}
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';
	
	return 0;
}

#================================================
# ¼¬ÄŞ³
#================================================
sub _get_war_shadow_data {
	# ‘—Í’á‚¢ê‡‚Í1.5”{
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# “ˆê‘‚Ìê‡‚ÍNPCã‘Ì
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = '¼¬ÄŞ³‹Rm(NPC)';
	
	return 0;
}


#================================================
# •ºí‚ª“ÁU(—L—˜)‚©‚Ç‚¤‚©
#================================================
sub is_tokkou {
	my($m_unit, $y_unit) = @_;
	
	for my $tokkou (@{ $units[$m_unit][6] }) {
		return 1 if $tokkou eq $y_unit;
	}
	return 0;
}


#================================================
# _war_result.cgi‚Éˆ—Œ‹‰Ê‚ğ“n‚·
#================================================
sub war_win {
	my $is_single = shift;
	require "./lib/_war_result.cgi";
	&war_win($is_single);
}
sub war_lose {
	require "./lib/_war_result.cgi";
	&war_lose;
}
sub war_draw {
	require "./lib/_war_result.cgi";
	&war_draw;
}
sub war_escape {
	require "./lib/_war_result.cgi";
	&war_escape;
}


1; # íœ•s‰Â
