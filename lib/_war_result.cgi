use File::Copy::Recursive qw(rcopy);
use File::Path;
#=================================================
# í‘ˆŒ‹‰Ê Created by Merino
#=================================================
# war.cgi‚É‚ ‚Á‚Ä‚à‚¢‚¢‚¯‚Ç‚²‚¿‚á‚²‚¿‚á‚É‚È‚è‚»‚¤‚È‚Ì‚Å•ª—£

# ‹~ol”
my $max_rescue = 1;

#=================================================
# ˆø‚«•ª‚¯
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	
	my $is_rewrite = 0;
	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
	if ($y{sol} > 0) {
		$cs{soldier}[$y{country}] += int($y{sol} / 3);
		$is_rewrite = 1;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# •‰‚¯
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "•”‘à‘S–Å‚Æ‚¢‚¤•s–¼—_‚È”s–k‚Ìˆ×A$m{name}‚É‘Î‚·‚é•]‰¿‚ª’˜‚µ‚­‰º‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";

	if($m{master_c} eq 'lose_c'){
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(21)+50) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "‚µ‚©‚µ“a–ğ‚ğ—§”h‚É–±‚ß‚½ˆ×A$m{name}‚É‘Î‚·‚é•]‰¿‚ªã‚ª‚è‚Ü‚µ‚½<br>";
		$mes .= "‚³‚ç‚É$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	}
	
	$cs{soldier}[$y{country}] += int($y{sol} / 3) if $y{sol} > 0;
	&down_friendship;

	# ˜A‘±‚Å“¯‚¶‘‚¾‚Æ‚Šm—¦‚ÅÀ²°Î
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( ( ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 ) || ( ($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2  || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		my $mname = &name_link($m{name});
		&write_world_news("$c_m‚Ì$mname‚ª$c_y‚Ì˜S–‚É—H•Â‚³‚ê‚Ü‚µ‚½");
		&add_prisoner;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# ‘Ş‹p
#=================================================
sub war_escape {
	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );
	&write_yran('war', 1, 1);

	$cs{soldier}[$m{country}] += $m{sol};
	$cs{soldier}[$y{country}] += int($y{sol} / 3);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# Ÿ‚¿
#=================================================
sub war_win {
	my $is_single = shift;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('war');
		if ($is_single) {
			&super_attack('single');
		}
	}
	# ’D‘—ÍÍŞ°½:ŠK‹‰‚ª‚‚¢‚Ù‚ÇÌß×½B‰ºãAŠv–½‚Ì‚ÍŠK‹‰‚ª’á‚¢‚Ù‚ÇÌß×½
	my $v = ($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2')) ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# ’èˆõ‚ª­‚È‚¢•ªÌß×½‘½‚¢•ªÏ²Å½
#	if ($m{country}) {
#		$mem = &modified_member($m{country});
#	} else {
#		$mem = 0;
#	}
#	$v += ($cs{capacity}[$m{country}] - $mem) * 10 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 5 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));


	# ‘î¨‚É‚æ‚è’D‘—Í‘‰Á
	if (($w{world} eq '4' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '4' || $w{world_sub} eq '5')))) { # –\ŒNA¬“×
		$v *= 2.5;
	}
	elsif (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # Šv–½:ã‘—L—˜
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
		if ($m{sedai} < 5) {
			$v *= 3;
		}
		elsif ($m{sedai} < 10) {
			$v *= 2.5;
		}
	}
	elsif (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) { # ”’•º
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
			$v *= 1.2;	
	}
	else {
		$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
	}
	
	# Œğí’†‚È‚ç2”{
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	# Še‘İ’è
	$v *= &get_modify('war');
	
	# Q–d‚Í’D‘—Í1.1”{
	if ($cs{war}[$m{country}] eq $m{name}) {
		$v = int($v * 1.1) ;
	}
	# ŒNå‚Í’D‘—Í1.05”{A–\ŒN‚È‚ç‚Î1.2”{
	elsif ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$v = int($v * $ceo_value);
	}
#	#‘ã•\ƒ{[ƒiƒX
#	$v = int($v * 1.1) if $cs{war}[$m{country}] eq $m{name};    
#	$v = int($v * 1.05) if $cs{ceo}[$m{country}] eq $m{name};

	# b‰»
	$v = &seed_bonus('red_moon', $v);
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &seed_bonus('war_win', $v);
	$v = $m{value} * 100 if $m{pet} eq '193';
	if($m{unit} eq '18'){
		$v = $v * 1.5;
		$v = &use_pet('war_result', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) || $m{pet} eq '12');
	}else{
		$v = &use_pet('war_result', $v) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	}
	
	if ($cs{extra}[$m{country}] eq '1' && $cs{extra_limit}[$m{country}] >= $time) {
		$v = 999;
	}
	
	if ($w{world} eq $#world_states - 5) {
		$v = int($v / 10);
	}
	
	# ˆÃ•‘¤ƒJƒEƒ“ƒ^[‚ÌŠî–{’D‘—Íi­”‚â³ÛÎŞ—pj
	# “ˆêŠúŒÀØ‚ê‚»‚¤‚É‚È‚é‚Æ••ˆó‘¤‚ª—L—˜‚É‚È‚é‚Ì‚ÍA
	# “ˆêŠúŒÀØ‚ê‚½‚ÉˆÃ•¶‚«‚Ä‚Ä‚à•‰‚¯ˆµ‚¢‚¾‚µ‚Ç‚¤‚¹‚È‚ç‚¿‚á‚ñ‚Æ••ˆó‚µ‚ë‚Á‚Ä‚¢‚¤d—l‚©‚Æv‚í‚ê‚é
	$npc_v = int(rand(400)+600) if $w{world} eq $#world_states;

	# ’D‘—ÍãŒÀ
	if ($v !~ /^(\d)\1+$/) { # ¿ŞÛ–Ú(³ÛÎŞÛ½g—p‚È‚Ç)
		if ($m{value} < 1) { # ­”¸‰s
			$v = $v > 200 ? int(rand(50)+150) : int($v);
		}
		else { # ’ÊíE’·Šú
			if($m{unit} eq '18'){
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # “ˆêŠúŒÀc‚è‚P“ú
					$v = $v > 2000 ? int(rand(250)+1750) : int($v);
				}
				else {
					$v = $v > 1500  ? int(rand(200)+1300) : int($v);
					# ˆÃ•‘¤ƒJƒEƒ“ƒ^[‚Ì’D‘—Í
					$npc_v = int(rand(525)+975) if $w{world} eq $#world_states;
				}
			}else{
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # “ˆêŠúŒÀc‚è‚P“ú
					$v = $v > 1500 ? int(rand(250)+1250) : int($v);
				}
				else {
					$v = $v > 1000  ? int(rand(200)+800) : int($v);
					# ˆÃ•‘¤ƒJƒEƒ“ƒ^[‚Ì’D‘—Í
					$npc_v = int(rand(400)+600) if $w{world} eq $#world_states;
				}
			}
			# “ˆêŠúŒÀ‚ª‹ß‚Ã‚¢‚Ä‚«‚½‚çÌß×½
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# –Å–S‘‚Ìê‡”±‘¥
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	if ($cs{disaster}[$y{country}] eq 'paper' && $cs{disaster_limit}[$y{country}] >= $time) {
		$v += 100;
	}
	# ‘—Íƒf[ƒ^}
	$cs{strong}[$m{country}] += ($w{world} eq '13' || $w{world} eq $#world_states - 2 || $w{world} eq $#world_states - 3) ? int($v * 0.75):$v;
	$cs{strong}[$y{country}] -= $v unless ($w{world} eq $#world_states - 5);
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	&write_yran2(
		'strong', $v, 1,
		"strong_$y{country}", $v, 1,
		'win', 1, 1,
		'war', 1, 1
	);
#	&write_yran('strong', $v, 1);
#	&write_yran("strong_$y{country}", $v, 1);
#	&write_yran('win', 1, 1);
#	&write_yran('war', 1, 1);
	
	if ($w{world} eq $#world_states - 5) {
		$mes .= "$v‚Ì$e2j{strong}‚ğ“¾‚Ü‚µ‚½<br>";
	} else {
		$mes .= "$c_y‚©‚ç$v‚Ì$e2j{strong}‚ğ’D‚¢‚Ü‚µ‚½<br>";
	}
	
	my $mname = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$mname = '–¼–³‚µ';
	}
	if ($w{world} eq $#world_states - 5) {
		&write_world_news(qq|$c_m‚Ì$mname‚ª<font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ“¾‚é–‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|);
	} else {
		if ($is_single) {
			&write_world_news(qq|$c_m‚Ì$mname‚ª$c_y‚ÉNUA$y{name}‚Æˆê‹R“¢‚¿‚Ì––‚±‚ê‚ğ‰º‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤–‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|);
		}
		else {
			$m{value} < 1
				? &write_world_news(qq|‰½Ò‚©‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚ğŒ‚”j‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤‚±‚Æ‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|)
				: &write_world_news(qq|$c_m‚Ì$mname‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚ğŒ‚”j‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤‚±‚Æ‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|)
				;
		}
	}

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‘å‚«‚­ã‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$vv‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";

	if($m{master_c} eq 'win_c'){
		++$m{medal};
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(11)+20) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "‚»‚ÌŒ÷Ñ‚ğ‘å‚«‚­Œ–“`‚µ‚½ˆ×A$m{name}‚É‘Î‚·‚é•]‰¿‚ª‚³‚ç‚Éã‚ª‚è‚Ü‚µ‚½<br>";
		$mes .= "‚³‚ç‚É$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	}
	# Ú½·­°
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>1<>\n";
		close $fh;
	}

	&refresh;

	&daihyo_c_up('war_c'); # ‘ã•\n—û“x
	
	# ˆÃ•
	if ($w{world} eq $#world_states) {
		my $ahoalia = 1;
		for my $ac (1..$w{country} - 1) {
			if (!$cs{is_die}[$ac]) {
				$ahoalia = 0;
			}
		}
		if ($cs{strong}[$m{country}] >= $touitu_strong
			|| ($cs{strong}[$w{country}] <= 0
				&& $union ne $w{country})
			|| ($ahoalia && $m{country} eq $w{country})) {
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
		else{
			require './lib/vs_npc.cgi';
#			if( rand(4) < $npc_war  || ($cs{strong}[$w{country}] < 30000 && rand(3) < $npc_war) ) {
			if( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			    &npc_war;
			}
		}
	}
	# Ià
	elsif (($w{world} eq '13' || ($w{world} eq '19' && $w{world_sub} eq '13'))) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
	}
	# •s‹ä‘Õ“V
	elsif ($w{world} eq $#world_states - 2) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_touitu;
		}
	}
	# O‘u
	elsif ($w{world} eq $#world_states - 3) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
			$cs{strong}[$m{country}] += 3000;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
	}
	# Ù‘¬
	elsif ($w{world} eq $#world_states - 5) {
		my $cou = 0;
		my $max_value = 0;
		for my $i (1 .. $w{country}) {
			if ($cs{strong}[$i] > $max_value) {
				$cou = $i;
				$max_value = $cs{strong}[$i];
			}
		}
		$strongest_country = $cou;
		if ($y{country} eq $strongest_country) {
			if (rand(3) < 1) {
				my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 10  );
				&write_world_news("<b>Ø³Ş§²±»İ‚Ì‘å—’I$cs{name}[$m{country}]‚Í$cs{name}[$y{country}]‚Ì$e2j{$kkk}‚ğ $vvv ’D‚¢‚Ü‚µ‚½</b>");
			}
		} else {
			if (rand(3) < 1) {
				my $type = int(rand(12));
				if ($type == 0) {
					for my $i (1..$w{country}) {
						next if $i eq $m{country};
						$cs{strong}[$i] -= int(rand(40)+40);
					}
					&write_world_news("<b>Še‘‚Ì$e2j{strong}‚ª‰º‚ª‚è‚Ü‚µ‚½</b>");
				} elsif ($type <= 10) {
					if (rand(3) < 1) {
						$cs{food}[$m{country}] += 100000;
						&write_world_news("$c_m‚Ì$e2j{food}‚ª100000‘‰Á‚µ‚Ü‚µ‚½");
					} elsif (rand(2) < 1) {
						$cs{money}[$m{country}] += 100000;
						&write_world_news("$c_m‚Ì$e2j{money}‚ª100000‘‰Á‚µ‚Ü‚µ‚½");
					} else {
						$cs{soldier}[$m{country}] += 50000;
						&write_world_news("$c_m‚Ì$e2j{soldier}‚ª50000‘‰Á‚µ‚Ü‚µ‚½");
					}
				} else {
					for my $i (1..$w{country}) {
						for my $j ($i+1..$w{country}) {
							$w{"f_${i}_${j}"}=int(rand(20));
							$w{"p_${i}_${j}"}=2;
						}
					}
					&write_world_news("<b>¢ŠE’†‚ªŠJí‚Æ‚È‚è‚Ü‚µ‚½</b>");
				}
			}
		}
	}
	# “ˆê
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# –Å–S
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# •œ‹»
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '9' || ($w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13')))) ) {
		&_hukkou;
	}
	# “S•Ç
	elsif (($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>Ø³Ş§²±»İ‚Ì‘å—’I$cs{name}[$m{country}]‚Í$cs{name}[$y{country}]‚Ì$e2j{$kkk}‚ğ $vvv ’D‚¢‚Ü‚µ‚½</b>");
	}
	if($w{world} eq '19'){# “ä
		if($w{sub_time} < $time){
			$w{world_sub} = int(rand(@world_states-4));
			$w{sub_time} = $time + 6 * 3600;
		}
	}
	

	&write_cs;

	&n_menu;
}

#=================================================
# ˜S–‚É’‡ŠÔ‚ª‚¢‚é‚È‚ç‹~o
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country,$flag) = split /<>/, $line;
		if ($flag == 0 && $count < $max_rescue && ($country eq $m{country} || $union eq $country) && $country ne '0' ) {
			my $mname = $m{name};
			if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
				$mname = '–¼–³‚µ';
			}
			$mes .= "$c_y‚É•ß‚ç‚¦‚ç‚ê‚Ä‚¢‚½$name‚ğ‹~o‚µ‚Ü‚µ‚½<br>";
			$is_rescue = 1;
			&write_world_news("$c_m‚Ì$mname‚ª$c_y‚É•ß‚ç‚¦‚ç‚ê‚Ä‚¢‚½$name‚Ì‹~o‚É¬Œ÷‚µ‚Ü‚µ‚½");
			&write_yran('res', 1, 1);
			
			# Ú½·­°Ì×¸Şì¬
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgiÌ§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh2;
			}
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		&c_up('res_c');
		&use_pet('rescue');
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('rescue');
		}
	}
	close $fh;
}

#=================================================
# “ˆê
#=================================================
sub _touitu {
	&c_up('hero_c');
	&debug_log(\%w, 'touitsu_w');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];

	my $mname = &name_link($m{name});
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC‘‘¤‚ÌŸ—˜
			&mes_and_world_news("<em>ˆ«–‚’B‚Ì—¦æÒ‚Æ‚µ‚Ä$world_name‘å—¤‚ğx”z‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "[‚«ˆÅ‚æ‚è–ÚŠo‚ß‚½$cs{name}[$w{country}]‚Ì–ÒÒ’B‚ª$mname‚ğ•M“ª‚Æ‚µ$world_name‘å—¤‚ğx”z‚·‚é");
			&send_twitter("[‚«ˆÅ‚æ‚è–ÚŠo‚ß‚½$cs{name}[$w{country}]‚Ì–ÒÒ’B‚ª$m{name}‚ğ•M“ª‚Æ‚µ$world_name‘å—¤‚ğx”z‚·‚é");
			$is_npc_win = 1;
		}
		else {
			&mes_and_world_news("<em>–‚ŠE‚ğÄ‚Ñ••ˆó‚µA$world_name‘å—¤‚É‚Ğ‚Æ‚Æ‚«‚ÌˆÀ‚ç‚¬‚ª‚¨‚Æ‚¸‚ê‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m‚Ì$mname‚Æ‚»‚Ì’‡ŠÔ’B‚ª–‚ŠE‚ğÄ‚Ñ••ˆó‚µA$world_name‘å—¤‚É‚Ğ‚Æ‚Æ‚«‚ÌˆÀ‚ç‚¬‚ª‚¨‚Æ‚¸‚ê‚é");
			&send_twitter("$c_m‚Ì$m{name}‚Æ‚»‚Ì’‡ŠÔ’B‚ª–‚ŠE‚ğÄ‚Ñ••ˆó‚µA$world_name‘å—¤‚É‚Ğ‚Æ‚Æ‚«‚ÌˆÀ‚ç‚¬‚ª‚¨‚Æ‚¸‚ê‚é");
		}
	}
	elsif ($w{world} eq $#world_states-2) {
		&mes_and_world_news("<em>$world_name‘å—¤‚ğ“ñ•ª‚·‚éí‚¢‚Í$c_m‚Ì$mname‚Æ‚»‚Ì’‡ŠÔ’B‚ÌŸ—˜‚ÉI‚í‚Á‚½</em>",1);
		&write_legend('touitu', "$c_m‚Ì$mname‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		&send_twitter("$c_m‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		$w{win_countries} = $m{country};
	}
	elsif ($w{world} eq $#world_states-3) {
		&mes_and_world_news("<em>$world_name‘å—¤‚ğO•ª‚·‚éí‚¢‚Í$c_m‚Ì$mname‚Æ‚»‚Ì’‡ŠÔ’B‚ÌŸ—˜‚ÉI‚í‚Á‚½</em>",1);
		&write_legend('touitu', "$c_m‚Ì$mname‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		&send_twitter("$c_m‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		$w{win_countries} = $m{country};
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]“¯–¿‚Ì$mname‚ª$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]“¯–¿‚Ì$mname‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
			&send_twitter("$c_m$cs{name}[$union]“¯–¿‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		}
		else {
			&mes_and_world_news("<em>$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m‚Ì$mname‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
			&send_twitter("$c_m‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
}

#=================================================
# •œ‹»
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_m‚ğ•œ‹»‚³‚¹‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# –Å–S
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	$w{world_sub} = int(rand(@world_states-4));
	&mes_and_world_news("<b>$c_y‚ğ–Å‚Ú‚µ‚Ü‚µ‚½</b>", 1);

	# •¨‘Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# ‘ó‘Ô•Ï‰»
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# –Å–S‘‚©‚ç‘—Í‚ğ’Dæ‚µ‚½‚Ì”±‘¥
#=================================================
sub _penalty {
	# ĞŠQ
	if ( (($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12')) && rand(3) < 1) || rand(12) < 1 ) {
		&disaster( ($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12') )); # –ï”N or “ä(–ï”N)‚Ì‚İ’Ç‰ÁÍßÅÙÃ¨

=pod
		#1› 2~ 3› 4~ 5› 6› 7› 8~ 9› 10›
		if ($w{year} !~ /6$/ && $w{year} !~ /0$/ && $cs{strong}[$y{country}] < 5000) { # “Áêî¨‚Å‚È‚­‚©‚Â‘—Í5000–¢–iÉ±ÊŞØ±‚Ì½‘‰ñ”ğj‚Ì‚İ½‘”­“®
			# ½‘ó‘Ôæ“¾
			my $sleep_num = 0;
			for my $i (1 .. $w{country}) {
				$sleep_num++ if $cs{die}[$i] == 2;
			}
			unless ($sleep_num) { # ‚Ç‚±‚à½‘‚µ‚Ä‚È‚¢‚È‚ç½‘
				$cs{is_die}[$y{country}] = 2;
				$w{game_lv} -= int(rand(3)+4) unless $w{world} eq '15' || $w{world} eq '17'; # ”’•º‚Æ–À‘–‚Í“ˆê“ïˆÕ“x’á‚·‚¬‚é‚Ì‚Å‚»‚êˆÈã‰º‚°‚¸‘¼‚Ìî¨‚È‚ç‰º‚°‚é

				# ½‘‚µ‚Ä‚¢‚é‘‚É“¯–¿‚ª‚ ‚ê‚ÎØ‚é
				for my $i (1 .. $w{country}) {
					my $c_c = &union($y{country}, $i);
					$w{"p_$c_c"} = 0 if $w{"p_$c_c"} == 1;
				}
			}
		}
=cut
	}
}

#=================================================
# —FD“xDown
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	$w{'f_'.$c_c} -= ($m{pet_c} - 10) if ($m{pet} eq '193' && $m{pet_c} > 10);
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10 && $y{country} ne $union) {
		$w{'p_'.$c_c} = 2;
		my $mname = &name_link($m{name});
		&write_world_news("<b>$c_m‚Ì$mname‚ÌiŒR‚É‚æ‚è$c_y‚ÆŒğíó‘Ô‚É‚È‚è‚Ü‚µ‚½</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}

#=================================================
# C³ŒãŠ‘®l”
#=================================================
sub modified_member {
	my $i = shift;
	return $cs{member}[$i] - $cs{new_commer}[$i];
}



1; # íœ•s‰Â
