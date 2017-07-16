#================================================
# ƒƒCƒ“‰æ–Ê Created by Merino
#================================================

# ‚¨“X‚Ì”„ã‹à‚ÌÅ‹à(0(Å‹à‚È‚µ)`0.99‚Ü‚Å)
my $shop_sale_tax = 0.5;
# ƒMƒ‹ƒhƒ}ƒXƒ^[‚ÌÅ‹à–Æœ—¦(0(Å‹à‚È‚µ)`0.99‚Ü‚Å)
my $guild_master_tax_rate = 1.0;
# Šˆ”­‚ÈƒMƒ‹ƒh‚ÌÅ‹à–Æœ—¦(0(Å‹à‚È‚µ)`1.0‚Ü‚Å)
my $guild_prior_tax_rate = 1.0;
# ‚»‚Ì‘¼‚ÌƒMƒ‹ƒh‚ÌÅ‹à–Æœ—¦(0(Å‹à‚È‚µ)`1.0‚Ü‚Å)
my $guild_ferior_tax_rate = 1.0;

# ÒÆ­° ’Ç‰Á/•ÏX/íœ/•À‚×‘Ö‚¦‰Â”\
my @menus = (
	['XV',		''],
	['¼®¯Ëßİ¸ŞÓ°Ù',	'shopping'],
	['—a‚©‚èŠ',	'depot'],
	['‘ŒÉ',	'depot_country'],
	['Ï²Ù°Ñ',		'myself'],
	['Cs',		'training'],
	['“¢”°',		'hunting'],
	['‘î•ñ',		'country'],
	['“à­',		'domestic'],
	['ŠOŒğ',		'promise'],
	['ŒR–',		'military'],
	['í‘ˆ',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['›z‰»', 'incubation'];
}
if (&on_summer) {
	push @menus, ['‰ÄÕ‚è', 'summer_festival'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# Ò²İ¼½ÃÑ
#================================================
sub main_system {
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '—‘m';
			push @menus, ['›z‰»', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# ÀÏºŞ¬’·
	elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "‚Á‚Ä‚¢‚½$eggs[$m{egg}][1]‚ªŒõ‚¾‚µ‚Ü‚µ‚½!<br>";
		
		# Ê½ŞÚ´¯¸Şê—pˆ—
		if ( $eggs[$m{egg}][1] eq 'Ê½ŞÚ´¯¸Ş' && rand(7) > 1 && $m{egg} != 53) {
			if (rand(6) > 1) {
				$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $eggs[$m{egg}][1]‚ªY‚Ü‚ê‚Ü‚µ‚½<br>";
			}
			else {
				$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚Í‹ó‚Á‚Û‚Å‚µ‚½c<br>";
				$m{egg} = 0;
			}
		}
		# À·µİ´¯¸Ş
		elsif ($eggs[$m{egg}][1] eq 'À·µİ´¯¸Ş') {
			$m{egg_c} = 0;
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '‚¨‚¢‚·[';
			$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $pets[$v][1] ‚ªY‚Ü‚ê‚Ü‚µ‚½<br>$pets[$v][1]ƒ$pet_mes<br><br>$pets[$v][1]‚Í—a‚©‚èŠ‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# ›z‰»‚ğƒƒMƒ“ƒO
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			if (rand(3) < 1) {
				$m{egg} = 0;
			} else {
				$mes .= "$eggs[$m{egg}][1]‚ª‚ğ‹ts‚µ‚½<br>";
			}
		}
		# ±ËŞØÃ¨´¯¸Şê—pˆ—(—j“ú‚É‚æ‚è•Ï‚í‚é)
		elsif ( $eggs[$m{egg}][1] eq '±ËŞØÃ¨´¯¸Ş' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '‚¨‚¢‚·[';
			$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $pets[$v][1] ‚ªY‚Ü‚ê‚Ü‚µ‚½<br>$pets[$v][1]ƒ$pet_mes<br><br>$pets[$v][1]‚Í—a‚©‚èŠ‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# ›z‰»‚ğƒƒMƒ“ƒO
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '‚¨‚¢‚·[';
			$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $pets[$v][1] ‚ªY‚Ü‚ê‚Ü‚µ‚½<br>$pets[$v][1]ƒ$pet_mes<br><br>$pets[$v][1]‚Í—a‚©‚èŠ‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# ›z‰»‚ğƒƒMƒ“ƒO
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('incubation');
		}
	}
	# µ°¸¼®İ‘ãA‚¨“X‚Ì”„ã‹àA‘—‹àŒn‚Ìó‚¯æ‚è
	elsif (-s "$userdir/$id/money.cgi") {
		if($m{guild_number}){
			open my $fhg1, "< $logdir/guild_shop1_sale.cgi";
			my $lineg1 = <$fhg1>;
			my($g1_sale_c, $g1_sale_money, $g1_update_t) = split /<>/, $lineg1;
			close $fhg1;
			
			open my $fhg2, "< $logdir/guild_shop2_sale.cgi";
			my $lineg2 = <$fhg2>;
			my($g2_sale_c, $g2_sale_money, $g2_update_t) = split /<>/, $lineg2;
			close $fhg2;
			if(($m{guild_number} == 1 && $g1_sale_c > $g2_sale_c) || ($m{guild_number} == 2 && $g2_sale_c > $g1_sale_c)){
				$shop_sale_tax *= $guild_prior_tax_rate;
			}else{
				$shop_sale_tax *= $guild_ferior_tax_rate;
			}
			
			open my $fhg, "< $logdir/bbs_akindo_$m{guild_number}_allmember.cgi";
			my $headline = <$fhg>;
			while (my $line = <$fhg>) {
				my($mname, $vote, $master) = split /<>/, $line;
				if ($master) {
					if($mname eq $m{name}){
						$shop_sale_tax *= $guild_master_tax_rate;
					}
					last;
				}
			}
			close $fhg;
		}
		
		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;
			
			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$name‚É $money G‚ğx•¥‚¢‚Ü‚µ‚½<br>";
				
				# ‹âsŒo‰cÒ‚ª‘‹àƒ}ƒCƒiƒX‚É‚È‚Á‚½ê‡‚Í‹âs‚Í“|Y
				if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
					unlink "$userdir/$id/shop_bank.cgi";
					unlink "$userdir/$id/shop_sale_bank.cgi";
					&mes_and_send_news("<b>Œo‰c‚·‚é‹âs‚ÍÔšŒo‰c‚Ì‚½‚ß“|Y‚µ‚Ü‚µ‚½</b>", 1);
				}
			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '¤l' || $pets[$m{pet}][2] eq 'tax_free') {
					$mes .= "$name‚©‚ç $money G‚Ì”„ã‹à‚ğó‚¯æ‚è‚Ü‚µ‚½<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$name‚©‚ç $money G‚Ì”„ã‹à‚ğó‚¯æ‚èA$v GÅ‹à‚Æ‚µ‚Äæ‚ç‚ê‚Ü‚µ‚½<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			elsif ($is_shop_sale eq '2') {
				$mes .= "$name‚©‚ç $money ‚ğó‚¯æ‚è‚Ü‚µ‚½<br>";
			}
			else {
				$m{money} += $money;
				$mes .= "$name‚©‚ç $money G‚ğó‚¯æ‚è‚Ü‚µ‚½<br>";
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/ex_c.cgi") {
		open my $fh, "+< $userdir/$id/ex_c.cgi" or &error("$userdir/$id/ex_c.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($c, $number) = split /<>/, $line;
			&c_up($c) for(1..$number);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/cataso_res.cgi") {
		if (!$m{cataso_ratio}) {
			$m{cataso_ratio} = 1500;
		}
		open my $fh, "+< $userdir/$id/cataso_res.cgi" or &error("$userdir/$id/cataso_res.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($compare, $value) = split /<>/, $line;
			my %c_data = &get_you_datas($compare, 1);
			if (!$c_data{cataso_ratio}) {
				$c_data{cataso_ratio} = 1500;
			}
			my $dr = int(16 + ($c_data{cataso_ratio} - $m{cataso_ratio}) * 0.04 + 0.5);
			if ($dr < 1) {
				$dr = 1;
			} elsif ($dr > 32) {
				$dr = 32;
			}
			$m{cataso_ratio} += int($dr * $value);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif ((-s "$userdir/$id/head_hunt.cgi") && $m{random_migrate} ne $w{year}) {
		open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($hname, $hcountry) = split /<>/, $line;
			$mes .= "$hname‚©‚ç $cs{name}[$hcountry] ‚Ö‚ÌŠ©—U‚ğó‚¯‚Ü‚µ‚½<br>";
			if ($m{shogo} eq $shogos[1][0]) {
				$m{shogo} = '';
				$m{shogo_t} = $shogos[1][0];
			}
		}
		$m{lib} = 'country_move';
		$m{tp} = 100;
		close $fh;
	}
	# ‘‚ÉŠ‘®‚µ‚Ä‚¢‚éê‡
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "“ú ‚Ì‘‚Ö‚ÌvŒ£‚ª”F‚ß‚ç‚êA$m{name}‚ÌŠK‹‰‚ª$rank_name‚É¸i‚µ‚Ü‚µ‚½<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				my $rank_name = &get_rank_name($m{rank}, $m{name});
				$mes .= "$m{name}‚ÌŠK‹‰‚ª$rank_name‚É~Ši‚µ‚Ü‚µ‚½<br>";
				if($m{super_rank}){
					$mes .= "‚µ‚©‚µ$m{rank_name}‚Í–¼—_E‚È‚Ì‚Å–¼Ì‚Í‚»‚Ì‚Ü‚Ü‚Å‚·<br>";
				}
			}
		}
		# ‹‹—^
		elsif ($m{country} && $time >= $m{next_salary}) {
			if($m{salary_switch} && $in{get_salary} ne '1'){
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
				$mes .= qq|<input type="submit" value="‹‹—¿‚ğó‚¯æ‚é" class="button1"></form>|;
			}else{
				$m{egg_c} += int(rand(50)+100) if $m{egg};
				&salary;
			}
		}
	}

	if($m{shogo_t} ne '' || $m{icon_t} ne ''){
		if($time >= $m{trick_time}){
			if($m{shogo_t} ne ''){
				$m{shogo} = $m{shogo_t} unless ($m{shogo} eq $shogos[1][0]);
				$m{shogo_t} = '';
			}
			if($m{icon_t} ne ''){
				if($m{icon} ne $default_icon){
					unlink "$icondir/$m{icon}" or &error("$m{icon}‚ª‘¶İ‚µ‚Ü‚¹‚ñ");
				}
				$m{icon} = $m{icon_t};
				$m{icon_t} = '';
			}
		}
	}
	if(-s "$userdir/$id/fx.cgi"){
		require './lib/fx_func.cgi';
		$mes .= &check_losscut;
	}

	$y{country} = 0 if $y{country} eq '';
#	$m{act} = 0 if $config_test;
	&run_tutorial_quest('tutorial_full_act_1') if $m{act} > 99;
}

#================================================
# ‹‹—^
#================================================
sub salary {
	# ‹‹—^Å
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );
	
	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;
	
	my $v = int( $salary_base * &tax ) + 1000;
	
	# ŒNå‚È‚ç‹‹—¿2.0”{A‘‚Ì‘ã•\Ò‚È‚ç‹‹—¿1.5”{
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$v *= 2.0;
	} elsif (&is_daihyo) {
		$v *= 1.5;
	}
	
	# “ˆê‘‚È‚çÎŞ°Å½
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# “¯–¿‚È‚µ‚Å“ˆê‚È‚ç2”{
		$v *= defined $c2 ? 1.75 : 2;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}
	
	# –Å–S
	$v *= 0.5 if $cs{is_die}[$m{country}];
	
	# ¤l‚È‚çÎŞ°Å½
	$v += 5000 if $jobs[$m{job}][1] eq '¤l';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_m‚©‚ç $v G‚Ì‹‹—^‚ª‚ ‚½‚¦‚ç‚ê‚Ü‚µ‚½<br>";
	&write_yran('sal', $v, 1) if $v > 0;
}


#================================================
# ¢‘ãŒğ‘ã/ÚÍŞÙ±¯Ìß
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};
	
	# ¢‘ãŒğ‘ã
	my $sedai_max = &seed_bonus('sedai_lv', 100);
	if ($m{lv} >= $sedai_max) {
		$m{lv} = 1;
		&c_up('sedai');
		
		# Œ‹¥‚µ‚Ä‚¢‚½ê‡
		if ($m{marriage}) {
			&mes_and_world_news("$m{marriage}‚Æ‚ÌŠÔ‚É‚Å‚«‚½$m{sedai}‘ã–Ú‚Ìq‹Ÿ‚ÉˆÓu‚ªˆø‚«Œp‚ª‚ê‚Ü‚µ‚½", 1);
			
			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}
			
			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));
			$m{super_rank} = 0;
			$m{rank_name} = '';
			
			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # Šo‚¦‚Ä‚¢‚é‹Z‚ğ•Û‘¶
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;
		
					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# Šo‚¦‚Ä‚¢‚È‚¢½·Ù‚È‚ç’Ç‰Á
						unless ($line =~ /,\Q$skill\E,/) {
							$is_rewrite = 1;
							$line .= "$skill,";
						}
					}
					if ($is_rewrite) {
						$line  = join ",", sort { $a <=> $b } split /,/, $line;
						$line .= ',';
						
						seek  $fh, 0, 0;
						truncate $fh, 0;
						print $fh $line;
					}
					close $fh;
				}
				
				if ($pets[$m{pet}][2] eq 'copy_pet' && $datas{pet}) {
					$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚Í$datas{name}‚ÌÍß¯Ä‚Ì$pets[$datas{pet}][1]‚ğºËß°‚µ‚Ü‚µ‚½<br>";
					$m{pet} = $datas{pet};
					&get_icon_pet;
				}
				
			}
		}
		# Œ‹¥‚µ‚Ä‚¢‚È‚¢‚Æ‚«
		else {
			if($m{job} ne '24'){
				&mes_and_world_news("$m{sedai}‘ã–Ú‚Ö‚ÆˆÓu‚ªˆø‚«Œp‚ª‚ê‚Ü‚µ‚½", 1);
			}else{
				&mes_and_world_news("$m{sedai}‘ã–Ú‚Ö‚ÆˆÓu‚ªˆø‚«Œp‚ª‚ê‚Ü‚µ‚½–‚–@­—$m{name}‚Ìƒ\\ƒEƒ‹ƒWƒFƒ€‚ª^‚Á•‚Éõ‚Ü‚Á‚½I", 1);
				open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiÌ§²Ù‚ª‚ ‚è‚Ü‚¹‚ñ");
				$line = <$bfh>;
				my $boss_name = (split /<>/, $line)[0];
				close $bfh;
				if($boss_name eq '•‰‚¯ƒCƒxƒ“ƒg'){
					$in{boss_at} = $m{at} + 500;
					$in{boss_df} = $m{df} + 500;
					$in{boss_mat} = $m{mat} + 500;
					$in{boss_mdf} = $m{mdf} + 500;
					$in{boss_ag} = $m{ag} + 500;
					$in{boss_cha} = $m{cha} + 500;
					open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiÌ§²Ù‚ª‚ ‚è‚Ü‚¹‚ñ");
					print $bfh "–‚—$m{name}<>0<>99999<>99999<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$m{wea}<>$m{skills}<>$m{mes_lose}<>$m{mes_win}<>$default_icon<>$m{wea_name}<>\n";
					close $bfh;
				}
			}
			
			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}
			
			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚Ì—Í‚É‚æ‚è½Ã°À½‚ª‚»‚Ì‚Ü‚Üˆø‚«Œp‚ª‚ê‚Ü‚µ‚½<br>";
				$mes .= "–ğ–Ú‚ğI‚¦‚½$pets[$m{pet}][1]š$m{pet_c}‚ÍAŒõ‚Ì’†‚Ö‚ÆÁ‚¦‚Ä‚¢‚Á‚½c<br>";
				&remove_pet;
			}
			else {
				&c_up('boch_c');
				my $down_par = $m{sedai} > 7 ? (rand(0.25)+0.6) : $m{sedai} * 0.05 + 0.35;
				if($m{job} eq '22' || $m{job} eq '23'){
					$down_par = (rand(0.5) + 0.45);
				}
				for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
					unless($m{job} eq '24' && ($k eq 'max_mp' || $k eq 'cha' || $k eq 'cha_org')){
						$m{$k} = int($m{$k} * $down_par);
					}
				}
				if($m{job} eq '24'){
					$m{job} = 0;
				}
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} -= int(rand(2));
				$m{super_rank} = 0;
				$m{rank_name} = '';
			}
		}
		if($m{master} && $m{master_c} && $m{sedai} >= 3){
			&graduate;
		}
		# ˆÈ‰º‹¤’Ê‚Ìˆ—
		$m{rank} = 1 if $m{rank} < 1;
	
		&use_pet('sedai');
		
		if ($m{skills}) { # Šo‚¦‚Ä‚¢‚é‹Z‚ğ•Û‘¶
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# Šo‚¦‚Ä‚¢‚È‚¢½·Ù‚È‚ç’Ç‰Á
				unless ($line =~ /,\Q$skill\E,/) {
					$is_rewrite = 1;
					$line .= "$skill,";
				}
			}
			if ($is_rewrite) {
				$line  = join ",", sort { $a <=> $b } split /,/, $line;
				$line .= ',';
				
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
			}
			close $fh;
		}
		if ($pets[$m{pet}][2] eq 'keep_seed') {
			$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚Ì—Í‚É‚æ‚èí‘°‚ª‚»‚Ì‚Ü‚Üˆø‚«Œp‚ª‚ê‚Ü‚µ‚½<br>";
			$mes .= "–ğ–Ú‚ğI‚¦‚½$pets[$m{pet}][1]š$m{pet_c}‚ÍAŒõ‚Ì’†‚Ö‚ÆÁ‚¦‚Ä‚¢‚Á‚½c<br>";
			&remove_pet;
			&seed_change('keep');
		} elsif ($pets[$m{pet}][2] eq 'change_seed') {
			$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚Ì—Í‚É‚æ‚èí‘°‚ª•Ï‚í‚é‚©‚à‚µ‚ê‚Ü‚¹‚ñ<br>";
			$mes .= "–ğ–Ú‚ğI‚¦‚½$pets[$m{pet}][1]š$m{pet_c}‚ÍAŒõ‚Ì’†‚Ö‚ÆÁ‚¦‚Ä‚¢‚Á‚½c<br>";
			&remove_pet;
			&seed_change('change');
		} else {
			&seed_change('');
		}
		$m{marriage} = '';
#		&refresh_new_commer;
	}
	# ƒŒƒxƒ‹ƒAƒbƒv
	else {
		$mes .= "Lv±¯Ìßô<br>";
		
		# HP ‚¾‚¯‚Í•K‚¸‚PˆÈãup‚·‚éd—l
		my $v = int( rand($jobs[$m{job}][2]) ) + 1;
		$m{max_hp} += $v;
		$mes .= "$e2j{max_hp}+$v ";

		my $count = 3;
		for my $k (qw/max_mp at df mat mdf ag lea cha/) {
			my $v = int( rand($jobs[$m{job}][$count]+1) );
			$m{$k} += $v;
			if ($k eq 'cha') {
				$m{cha_org} += $v;
			}
			$mes .= "$e2j{$k}+$v ";
			++$count;
		}
		
		&use_pet('lv_up');
		&run_tutorial_quest('tutorial_lv_20_1') if $m{lv} == 20;
	}
}

#================================================
# ’íq‘²‹Æ
#================================================
sub graduate {
	&send_item($m{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
	if(rand(7) > 1){
		&send_item($m{master}, 2, int(rand($#eggs)+1), 0, 0, 1);
	}else{
		require './lib/shopping_offertory_box.cgi';
		&send_god_item(5, $m{master});
	}

	&mes_and_world_news("$m{master}‚Ì’íq‚Æ‚µ‚Ä—§”h‚É¬’·‚µ‚Ü‚µ‚½", 1);
	&regist_you_data($m{master}, 'master', '');
	$m{master} = '';
	$m{master_c} = '';
}

1; # íœ•s‰Â
