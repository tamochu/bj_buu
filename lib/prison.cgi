sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
my $this_depot_file = "$userdir/$id/depot.cgi";
#=================================================
# ˜S– Created by Merino
#=================================================

#=================================================
# —˜—pğŒ
#=================================================
sub is_satisfy {
	if ($m{act} >= 100) {
		$mes .= "$m{name}‚Í­‚µ‹x‘§‚ğ‚Æ‚é‚±‚Æ‚É‚µ‚½<br>Ÿ‚És“®‚Å‚«‚é‚Ì‚Í $GWT•ªŒã‚Å‚·";
		$m{act} = 0;
		&wait;
		return 0;
	}
	return 1;
}

#=================================================
# ˜S–ÒÆ­°
#=================================================
sub tp_100 {
	if (-f "$userdir/$id/rescue_flag.cgi" # Ú½·­°Ì×¸Ş‚ª‚ ‚é‚©
		|| $time < $w{reset_time} # Ií’†
		|| !defined $cs{name}[$y{country}]) { # ‘íœ

			unlink "$userdir/$id/rescue_flag.cgi" or &error("$userdir/$id/rescue_flag.cgiíœ¸”s") if -f "$userdir/$id/rescue_flag.cgi";
			$mes .= "’‡ŠÔ‚É‹~o‚³‚ê‚Ü‚µ‚½<br>";
			
			&refresh;
			&n_menu;
			&escape;
	}
	else {
		$mes .= "$m{name}‚Í$c_y‚Ì$cs{prison_name}[$y{country}]‚É•Â‚¶‚ß‚ç‚ê‚Ü‚µ‚½<br>";
		$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
		&menu('•‚¯‚ğ‘Ò‚Â','’E‘–‚ğ‚İ‚é','Q•Ô‚é');
		$m{tp} += 10;
	}
}

sub tp_110 {
	# ’Eo
	if ($cmd eq '1') {
		$mes .= "$m{name}‚Í’E‘–‚ª‚Å‚«‚»‚¤‚©FX‚Æ‚µ‚Ä‚İ‚½<br>";
		if ( int(rand(4)) == 0 ) { # ¬Œ÷
			$mes .= "‚È‚ñ‚Æ‚©$cs{prison_name}[$y{country}]‚©‚ç’Eo‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚½!<br>";
			$m{tp} += 10;
		}
		elsif ( $m{cha} > rand(1000)+400 ) {
			$mes .= "ŠÅç‚ğ—U˜f‚µ‚Ä$cs{prison_name}[$y{country}]‚©‚ç’Eo‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚½!<br>";
			$m{tp} += 10;
		}
		else {
			$mes .= '‚Ç‚¤‚â‚ç–³—‚È‚æ‚¤‚¾c<br>';
			$m{act} += 10;
			$m{tp} = 100;
		}
		&n_menu;
	}
	# Q•Ô‚é
	elsif ($cmd eq '2') {
		$mes .= "Q•Ô‚é‚ÆŠK‹‰‚Æ‘ã•\\ÒÎß²İÄ‚ª‰º‚ª‚èAè‘±‚«‚É$GWT•ª‚©‚©‚è‚Ü‚·<br>";
		$mes .= "$c_m ‚ğ— Ø‚èA$c_y‚ÉQ•Ô‚è‚Ü‚·‚©?<br>";
		&menu('‚â‚ß‚é','Q•Ô‚é');
		$m{tp} = 200;
	}
	else {
		$m{tp} = 100;
		&tp_100;
	}
}

#=================================================
# ˜S–’Eo
#=================================================
sub tp_120 {
	$m{tp} += 10;
	$m{value} = int(rand(40))+40;
	$m{turn}  = int(rand(4)+4);
	$mes .= "$cs{prison_name}[$y{country}]‚©‚ç’Eo‚µ‚Ü‚µ‚½! <br>";
	$mes .= "$c_y’Eo‚Ü‚Åc‚èy$m{turn}À°İz“G•º‚Ì‹C”zy$m{value}%z<br>";
	$mes .= '‚Ç‚¿‚ç‚Éi‚İ‚Ü‚·‚©?<br>';
	&menu('¶','‰E');
	$m{value} += int( 10 - rand(21) ); # }10
	$m{value} = int(rand(30)) if $m{value} < 10;
}

#=================================================
# Ù°ÌßÒÆ­° •ß‚Ü‚é‚©’Eo‚·‚é‚Ü‚Å
#=================================================
sub loop_menu {
	$mes .= "$c_y’Eo‚Ü‚Åc‚èy$m{turn}À°İz“G•º‚Ì‹C”zy$m{value}%z<br>";
	$mes .= '‚Ç‚¿‚ç‚Éi‚İ‚Ü‚·‚©?<br>';
	int(rand(3)) == 0 ? &menu('¶','‰E') : &menu('¶','’¼i','‰E');
}
sub tp_130 {
	# Œ©‚Â‚©‚é
	if ( $m{value} > rand(110)+30 ) {
		$mes .= '“G•º‚ÉŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚Á‚½!!<br>';
		$m{tp} += 10;
		&n_menu;
	}
	# ’Eo¬Œ÷
	elsif (--$m{turn} <= 0) {
		if ($m{country} && $y{country}) {
			&c_up('esc_c');
			&use_pet('escape');
			&write_yran('esc', 1, 1);
		}
		&mes_and_world_news("–³–‚É$c_y‚©‚ç‚Ì©—Í’Eo‚É¬Œ÷‚µ‚Ü‚µ‚½!");
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('prison');
		}
		
		&refresh;
		&n_menu;
		&escape;
	}
	else {
		&loop_menu;
	}
	$m{value} += int( 10 - rand(21) ); # }10
	$m{value} = int(rand(30)) if $m{value} < 10;
}
# Œ©‚Â‚©‚Á‚½:“¦‚°Ø‚ê‚é or •ß‚Ü‚é
sub tp_140 {
	if ( rand(6) < 1 ) {
		$mes .= '‚È‚ñ‚Æ‚©“G•º‚ğU‚èØ‚è‚Ü‚µ‚½<br>';
		$m{tp} -= 10;
		&loop_menu;
	}
	else {
		$mes .= "“G•º‚ÉˆÍ‚Ü‚ê$cs{prison_name}[$y{country}]‚Ö‚Æ˜A‚ê–ß‚³‚ê‚Ü‚µ‚½<br>";
		$m{tp} = 100;
		$m{act} += 20;
		&n_menu;
	}
}


#=================================================
# Q•Ô‚é
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$mes .= "$e2j{ceo}‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
#		if ($m{name} eq $m{vote} || &is_daihyo) {
#			$mes .= "‘‚Ì‘ã•\\Ò‚â$e2j{ceo}‚É—§Œó•â‚µ‚Ä‚¢‚éê‡‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
#			$m{tp} = 100;
#			&n_menu;
#		}
		elsif ($m{shogo} eq $shogos[1][0]) {
			$mes .= "$shogos[1][0]‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($cs{member}[$y{country}] >= $cs{capacity}[$y{country}]) {
			$mes .= "$c_y‚Í’èˆõ‚ª‚¢‚Á‚Ï‚¢‚Å‚·<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5) {
			$mes .= "¡Šú‚ÍQ•Ô‚ê‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($m{random_migrate} eq $w{year}) {
			$mes .= "¡Šú‚ÍQ•Ô‚ê‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
		else {
			require './lib/move_player.cgi';
			&move_player($m{name}, $m{country}, $y{country});
			&escape;
			
			$m{shogo} = $shogos[1][0];

			$m{rank} -= $m{rank} > 10 ? 2 : 1;
			$m{rank} = 1 if $m{rank} < 1;
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "ŠK‹‰‚ª$rank_name‚É‚È‚è‚Ü‚µ‚½<br>";
			if($m{super_rank}){
				$mes .= "‚µ‚©‚µ$m{rank_name}‚Í–¼—_E‚È‚Ì‚Å–¼Ì‚Í‚»‚Ì‚Ü‚Ü‚Å‚·<br>";
			}

			&mes_and_world_news("$cs{name}[$y{country}]‚ÉQ•Ô‚è‚Ü‚µ‚½", 1);
			$m{country} = $y{country};
			$m{vote} = '';
			
			# ‘ã•\Îß²İÄDown
			for my $key (qw/war dom mil pro/) {
				$m{$key.'_c'} = int($m{$key.'_c'} * 0.4);
			}

			&refresh;
			&wait;
			&n_menu;
		}
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		$m{tp} = 100;
		&n_menu;
	}
}

#=================================================
# come by pet
#=================================================
sub tp_300 {
	if (int(rand(10)) + 10 <= $m{pet_c}) {
		$m{tp} = 320;
		&{'tp_' . $m{tp}};
		return;
	}
	$mes .= '‚Ç‚Ì‘‚Ì˜S–‚Ös‚«‚Ü‚·‚©?<br>';
	&menu('–³Š‘®',@countries,'‚â‚ß‚é');
	$m{tp} = 310;
}

sub tp_310 {
	if($cmd eq '' || $cmd == $m{country} || $cmd == $w{country} + 1){
		&refresh;
		&n_menu;
	}else{
		$y{country} = $cmd;
		&add_prisoner;
	}
}

sub tp_320 {
	$mes .= 'ƒoƒJƒ“ƒX‚ÉÍß¯Ä‚ğ˜A‚ê‚Äs‚¯‚Ü‚·B<br>';
	$layout = 2;
	my($count, $sub_mes) = &radio_my_pet_depot;

	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<p><input type="submit" value="ˆøo‚·" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="ˆøo‚·" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_330 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $add_line = '';
		my @lines = ();
		open my $fh, "+< $this_depot_file" or &error("$this_depot_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			++$count;
			if (!$new_line && $cmd eq $count) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				if($kind eq '3') {
					$new_line = $line;
					if($m{pet}) {
						$add_line = "$kind<>$m{pet}<>$m{pet_c}<>0<>\n";
						$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚ğ—a‚¯";
					}
				} else {
					$mes .= 'Íß¯ÄˆÈŠO‚Í˜A‚ê‚Ä‚¢‚¯‚Ü‚¹‚ñ<br>';
					push @lines, $line;
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line) {
			push @lines, $add_line if $add_line;
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my $s_mes;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			if ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚ğˆøo‚µ‚Ü‚µ‚½<br>";
			}
		}
		else {
			close $fh;
		}
	}
	$mes .= '‚Ç‚Ì‘‚Ì˜S–‚Ös‚«‚Ü‚·‚©?<br>';
	&menu('–³Š‘®',@countries,'‚â‚ß‚é');
	$m{tp} = 310;
}

sub radio_my_pet_depot {
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script">|;
	$sub_mes .= qq|<input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	open my $fh, "< $this_depot_file" or &error("$this_depot_file ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		next if ($kind ne '3');
		$sub_mes .= qq|<input type="radio" name="cmd" value="$count">|;
		$sub_mes .= qq|[‚Ø]$pets[$item_no][1]š$item_c$lock_mes<br>|;
	}
	close $fh;
	
	return $count, $sub_mes;
}
#=================================================
# ˜S–Ì§²Ù‚©‚ç©•ª‚Ì–¼‘O‚ğœ‚­
#=================================================
sub escape {
	if (-f "$logdir/$y{country}/prisoner.cgi") {
		my @lines = ();
		open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name,$country,$flag) = split /<>/, $line;
			push @lines, $line unless $name eq $m{name};
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}


1; # íœ•s‰Â
