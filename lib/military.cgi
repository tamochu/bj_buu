#=================================================
# ŒR– Created by Merino
#=================================================

#=================================================
# —˜—pğŒ
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '‘‚É‘®‚µ‚Ä‚È‚¢‚Æs‚¤‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>dŠ¯‚·‚é‚É‚Íu‘î•ñv¨udŠ¯v‚©‚çs‚Á‚Ä‚İ‚½‚¢‘‚ğ‘I‚ñ‚Å‚­‚¾‚³‚¢<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ”æ˜J‚µ‚Ä‚¢‚éê‡‚Ís‚¦‚È‚¢
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= 'IíŠúŠÔ’†‚Íí‘ˆ‚ÆŒR–‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
		if ($m{value} eq 'military_ambush'){
			open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $fh, 2; };
			seek  $fh, 0, 0;
			truncate $fh, 0;
			close $fh;
		}
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "‘¼‚É‰½‚©s‚¢‚Ü‚·‚©?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= 'ŒR–‚ğs‚¢‚Ü‚·<br>‚Ç‚ê‚ğs‚¢‚Ü‚·‚©?<br>';
	}
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		&menu('‚â‚ß‚é','H—¿‚ğ‹­’D','‘‹à‚ğ’D‚¤','•ºm‚ğô”]','“à•”’ã@','‹UŒv','‘Ò‚¿•š‚¹','H—¿‚ğ‹­’D(’·Šú)','‘‹à‚ğ’D‚¤(’·Šú)','•ºm‚ğô”](’·Šú)');
	}else{
		&menu('‚â‚ß‚é','H—¿‚ğ‹­’D','‘‹à‚ğ’D‚¤','•ºm‚ğô”]','“à•”’ã@','‹UŒv','‘Ò‚¿•š‚¹');
	}
}
sub tp_1 {
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		return if &is_ng_cmd(1..9);
	}else{
		return if &is_ng_cmd(1..6);
	}
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '6') {
		$mes .= "“G‘‚©‚ç‚ÌŒR–sˆ×‚ğŒ©’£‚Á‚½‚èA“G‘‚©‚ç‚ÌiŒR‚ğ‘Ò‚¿•š‚¹‚µ‚ÄŠh—‚³‚¹‚Ü‚·($GWT•ª`)<br>";
		$mes .= "‚Ç‚¿‚ç‚Ì‘Ò‚¿•š‚¹‚ğ‚µ‚Ü‚·‚©?<br>";
		&menu('‚â‚ß‚é', 'ŒR–sˆ×‚ğŒ©’£‚é', 'iŒR‚ğ‘Ò‚¿•š‚¹');
	}
	else { # 1-5 7-9
		if    ($cmd eq '1') { $mes .= "‘Šè‘‚É”E‚Ñ‚İH—¿‚ğ’D‚¢‚Ü‚·<br>"; }
		elsif ($cmd eq '2') { $mes .= "‘Šè‘‚Ì‘‹àÙ°Ä‚ğŠh—‚µ‚¨‹à‚ğ—¬o‚³‚¹‚Ü‚·<br>"; }
		elsif ($cmd eq '3') { $mes .= "‘Šè‘‚Ì•ºm‚ğô”]‚µA©‘‚Ì•ºm‚É‚µ‚Ü‚·<br>"; }
		elsif ($cmd eq '4') { $mes .= "‘Šè‘‚Ì“à•”‚Ìó‘Ô‚ğ‘Fõ‚µ‚És‚«‚Ü‚·<br>"; }
		elsif ($cmd eq '5') { $mes .= "‘Šè‘‚Éˆ«‚¢‰\\‚ğ—¬‚µ—FD“x‚ğ‰º‚°‚Ü‚·<br>"; }
		elsif ($cmd eq '7') { $mes .= "‘Šè‘‚É”E‚Ñ‚İ‘å–Ú‚ÉH—¿‚ğ’D‚¢‚Ü‚·<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '8') { $mes .= "‘Šè‘‚Ì‘‹àÙ°Ä‚ğŠh—‚µ‘å–Ú‚É‚¨‹à‚ğ—¬o‚³‚¹‚Ü‚·<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '9') { $mes .= "‘Šè‘‚Ì•ºm‚ğ‘å–Ú‚Éô”]‚µA©‘‚Ì•ºm‚É‚µ‚Ü‚·<br>"; $GWT *= 2.5; }
		$mes .= "‚Ç‚Ì‘‚ÉŒü‚©‚¢‚Ü‚·‚©?($GWT•ª)<br>";
		&menu('‚â‚ß‚é', @countries);
	}
}

#=================================================
# ‘Ò‚¿•š‚¹
#=================================================
sub tp_600 {
	if ($cmd eq '1') {
		$mes .= "“G‘‚©‚ç‚ÌŒR–sˆ×‚ª‚È‚¢‚©©‘‚ğ„‰ñ‚µŠÄ‹‚µ‚Ü‚·<br>";
		$mes .= "‘Ò‚¿•š‚¹‚Ì—LŒøŠÔ‚ÍÅ‚‚Å$max_ambush_hourŠÔ‚Ü‚Å‚Å‚·<br>";
		$mes .= "Ÿ‚És“®‚Å‚«‚é‚Ì‚Í$GWT•ªŒã‚Å‚·<br>";
		$m{tp} += 10;
		$m{value} = 'military_ambush';
		
		# í‘ˆ‚Æ“¯‚¶d‘g‚İ‚Å‚à‚¢‚¢‚¯‚ÇA‘Šè‚Ì½Ã°À½‚ª•K—v‚È‚¢‚Ì‚ÆAÌ§²Ùµ°Ìßİ‚P‰ñ‚Å‚·‚Ş‚Ì‚ÅB
		open my $fh, ">> $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		print $fh "$time<>$m{name}<>\n";
		close $fh;

		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
	elsif ($cmd eq '2') {
		$mes .= "“G‘‚©‚ç‚ÌiŒR‚ğ‘Ò‚¿•š‚¹‚µ‚Ü‚·<br>";
		$mes .= "‘Ò‚¿•š‚¹‚Ì—LŒøŠÔ‚ÍÅ‚‚Å$max_ambush_hourŠÔ‚Å‚·<br>";
		$mes .= "Ÿ‚És“®‚Å‚«‚é‚Ì‚Í$GWT•ªŒã‚Å‚·<br>";
		$m{value} = 'ambush';
		$m{tp} += 10;

		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
	else {
		&begin;
	}
}
sub tp_610 {
	$m{turn} = 1;
	$mes .= "‘Ò‚¿•š‚¹‚ğI—¹‚µ‚Ü‚µ‚½<br>";
	
	# ‘Ò‚¿•š‚¹‚É‚Ğ‚Á‚©‚©‚Á‚½”
	if (-s "$userdir/$id/ambush.cgi") {
		open my $fh, "+< $userdir/$id/ambush.cgi" or &error("$userdir/$id/ambush.cgiƒtƒ@ƒCƒ‹‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		eval { flock $fh, 2 };
		my $line = <$fh>;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		
		my @lines = split /<>/, $line;
		$mes .= join ",<br>", @lines;
		$mes .= "<br>‚ğ‘Ò‚¿•š‚¹‚ÅŒ‚‘Ş‚µ‚Ü‚µ‚½!<br>";
		$m{turn} = @lines;
	}

	# ŒR–‘Ò‚¿•š‚¹‚ÌA„‰ñƒtƒ@ƒCƒ‹‚©‚ç©•ª‚ğœ‚­ˆ—
	if ($m{value} ne 'ambush') {
		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($pat_time,$name) = split /<>/, $line;
			next if $name eq $m{name};
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		&run_tutorial_quest('tutorial_mil_ambush_1');
	}elsif (-s "$userdir/$id/war.cgi") {
		open my $fh, "+< $userdir/$id/war.cgi" or &error("$userdir/$id/war.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $result) = split /<>/, $line;
			
			if ($result eq '0') {
				$mes .= "$name‚ğŒ‚‘Ş‚µ‚Ü‚µ‚½<br>";
			}
			elsif ($result eq '1') {
				$mes .= "$name‚É”s–k‚µ‚Ü‚µ‚½<br>";
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}

	&special_money($m{turn} * 500) if $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');
	&c_up('mat_c') for 1 .. $m{turn};
	&military_master_c_up('mat_c');
	&use_pet('mat') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '32');
	&tp_1000;
}

#=================================================
# ŒR–¾¯Ä
#=================================================
sub tp_100 { &exe1("H—¿‚ğ‹­’D‚µ‚É") }
sub tp_200 { &exe1("‘‹àÙ°Ä‚ğŠh—‚µ‚É") }
sub tp_300 { &exe1("•ºm‚ğô”]‚µ‚É") }
sub tp_400 { &exe1("“à•”î¨‚ğ’ã@‚µ‚É") }
sub tp_500 { &exe1("‹UŒv‚ğ‚µ‚É") }
sub tp_700 { &exe1("H—¿‚ğ‘å–Ú‚É‹­’D‚µ‚É") }
sub tp_800 { &exe1("‘‹àÙ°Ä‚ğ‘å–Ú‚ÉŠh—‚µ‚É") }
sub tp_900 { &exe1("•ºm‚ğ‘å–Ú‚Éô”]‚µ‚É") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});
	
	if ($m{country} eq $cmd) {
		$mes .= '©‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '“¯–¿‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '–Å–S‚µ‚Ä‚¢‚é‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;

		# ¢ŠEî¨u–À‘–v
		if (($w{world} eq '15' || ($w{world} eq '19' && $w{world_sub} eq '15'))) {
			$y{country} = int(rand($w{country}))+1;
			if ($cs{is_die}[&get_most_strong_country]){
				my $loop = 0;
				while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
					if($loop > 30) {
						$y{country} = &get_most_strong_country;
					}
					$y{country} = int(rand($w{country}))+1;
					$loop++;
				}
			}else {
				$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
			}
		}

		$GWT *= 2.5 if $m{tp} >= 710 && $m{tp} <= 910;	
		$mes .= "$_[0]$cs{name}[$y{country}]‚ÉŒü‚©‚¢‚Ü‚µ‚½<br>";
		$mes .= "$GWT•ªŒã‚É“’…‚·‚é—\\’è‚Å‚·<br>";

		$m{renzoku_c} = $y{country} eq $m{renzoku} ? $m{renzoku_c} + 1 : 1;
		$m{renzoku} = $y{country};

		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
}

#=================================================
# ŒR–ˆ—
#=================================================
sub tp_110 { &form1('H—¿‚ğ’D‚¤') }
sub tp_210 { &form1('’³•ñ‚ğs‚¤') }
sub tp_310 { &form1('ô”]‚ğs‚¤') }
sub tp_410 { &form1('î¨‚ğ’T‚é') }
sub tp_510 { &form1('ˆ«‚¢‰\\‚ğ—¬‚·') }
sub tp_710 { &form1('H—¿‚ğ’D‚¤(’·Šú)') }
sub tp_810 { &form1('’³•ñ‚ğs‚¤(’·Šú)') }
sub tp_910 { &form1('ô”]‚ğs‚¤(’·Šú)') }
sub form1 {
	$mes .= "$c_y‚É“’…‚µ‚Ü‚µ‚½<br>";
	$m{tp} += 10;
	$m{value} = int(rand(20))+5;#$config_test ? 0 : int(rand(20))+5;
	$m{value} += int(rand(10)+1);#$config_test ? 0 : int(rand(10)+1); # ƒQ[ƒ€ƒoƒ‰ƒ“ƒX‚ğl‚¦‚Ä‰Šú’lÌŞ°½Ä‚Í‚»‚Ì‚Ü‚Ü
	$m{value} += 30 if $y{country} && ($pets[$m{pet}][2] ne 'no_ambush' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && &is_patrol($_[0]);
	if ($m{pet} == -1) { # Õ°Ú²‚Ì–„‚ß‚İˆ—
		$m{pet_c}--;
		if ($m{pet_c} <= 0) {
			$m{pet} = 0;
			$m{pet_c} = 0;
		}
	}

	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "“G•º‚Ì‹C”zy $m{value}% z<br>";
	$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
	&menu($_[0],'ˆø‚«‚ ‚°‚é');
#	$m{value} += int(rand(10)+1); merino ‚ÌÁ‚µ–Y‚êH
}

#=================================================
# Ù°ÌßºÏİÄŞ ¸”s‚·‚é‚©‚â‚ß‚È‚¢ŒÀ‚è‘±‚­(tpŒÅ’è)
#=================================================
sub loop_menu {
	$mes .= "“G•º‚Ì‹C”zy $m{value}% z<br>";
	$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?';
	&menu('‘±‚¯‚é', '‚â‚ß‚é');
}
sub tp_120 { &exe2 }
sub tp_220 { &exe2 }
sub tp_320 { &exe2 }
sub tp_420 { &exe2 }
sub tp_520 { &exe2 }
sub tp_720 { &exe2 }
sub tp_820 { &exe2 }
sub tp_920 { &exe2 }
sub exe2 {
	if ($cmd eq '0') { # Às
		if ( $m{value} > rand(110)+35 ) { # ¸”s ’Pƒ‚Érand(100)‚É‚·‚é‚Æ30%‚­‚ç‚¢‚ÅŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚¤‚Ì‚Å rand(110)+30‚É•ÏX
			$mes .= "“G•º‚ÉŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚Á‚½!!<br>";
			$m{tp} = 1900;
			&n_menu;
		}
		else { # ¬Œ÷
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			if($m{tp} == 420 && $m{turn} < 7){
				my $tei_sp = rand($m{tei_c} / 500);
				$m{value} += $tei_sp > 5 ? int(rand(5)+1): int(rand(10-$tei_sp)+1);
			} else {
				$m{value} += int( $m{unit} eq '17' ? (rand(10)+1)*(0.7+rand(0.3)) : rand(10)+1 ); # ‰B–§‚Íã¸‹C”z’l0.7`0.9
			}
			&loop_menu;
			$m{tp} -= 10;
		}
	}
	elsif ($cmd eq '1') { # ‘Ş‹p
		$mes .= 'ˆø‚«ã‚°‚é‚±‚Æ‚É‚µ‚Ü‚·<br>';
		if ($m{turn} <= 0) { # ‰½‚à‚µ‚È‚¢‚Åˆø‚«ã‚°
			&refresh;
			&n_menu;
		}
		elsif ($m{tp} eq '420') { # “à•”’ã@
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
		}
		else {
			my $tmp_tp = $m{tp};
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 1000;
			if ($tmp_tp eq '120' || $tmp_tp eq '220' || $tmp_tp eq '320' ||
				$tmp_tp eq '720' || $tmp_tp eq '820' || $tmp_tp eq '920') {
				&run_tutorial_quest('tutorial_mil_1');
			}
			&n_menu;
		}
	}
	else {
		&loop_menu;
	}
}

#=================================================
# ¬Œ÷
#=================================================
sub get_mil_success {
	my $v = int( ($m{"$_[0]_c"} + $m{$_[1]}) * $m{turn} * rand($_[3]) );
	$v  = int(rand(500)+$_[2]-500) if $v > $_[2];
	$v *= 2 if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
	$v *= 2 if $cs{extra}[$m{country}] eq '2' && $cs{extra_limit}[$m{country}] >= $time;
	$m{stock} += $v;
	return $v;
}
sub get_mil_message {
	if ($m{stock} > $cs{$_[0]}[$y{country}]) {
		$mes .= "$c_y‚Ì$_[3]";
		$m{stock} = $cs{$_[0]}[$y{country}];
	} else {
		$mes .= "$_[2]";
	}
	$mes .= "<br>[ ˜A‘±$m{turn}‰ñ¬Œ÷ Ä°ÀÙ$_[1] $m{stock} ]<br>";
}
sub tp_130 { # ‹­’D¬Œ÷
	my $v = &get_mil_success('gou', 'at', 3000, 4);
	&get_mil_message('food', '‹­’D', "$v‚ÌH—¿‹­’D‚É¬Œ÷‚µ‚Ü‚µ‚½!", "H—¿‚ªs‚«‚Ü‚µ‚½!");
}
sub tp_230 { # ’³•ñ¬Œ÷
	my $v = &get_mil_success('cho', 'mat', 3000, 4);
	&get_mil_message('money', '’³•ñ', "$v‚Ì‘‹à—¬o‚É¬Œ÷‚µ‚Ü‚µ‚½!", "$e2j{money}‚ªs‚«‚Ü‚µ‚½!");
}
sub tp_330 { # ô”]¬Œ÷
	my $v = &get_mil_success('sen', 'cha', 2500, 4);
	&get_mil_message('soldier', 'ô”]', "$vl‚Ì•ºmô”]‚É¬Œ÷‚µ‚Ü‚µ‚½!", "•ºm‚ª‚à‚¤‚¢‚Ü‚¹‚ñ!");
}
sub tp_430{ # ’ã@
	$mes .= $m{turn} eq '1' ? "$e2j{food}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} eq '2' ? "$e2j{money}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} eq '3' ? "$e2j{soldier}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} eq '4' ? "$e2j{tax}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} eq '5' ? "$e2j{state}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} eq '6' ? "$e2j{strong}‚Ìî•ñ‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>"
		  : $m{turn} >   7  ? "‰ï‹cº‚Ì‰ï˜b‚ğ•·‚«‚Ü‚µ‚½!<br>"
		  :                   "é“à•”‚Ö‚ÆŒü‚©‚Á‚Ä‚İ‚Ü‚·<br>"
		  ;
}
sub tp_530{ # ‹UŒv
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = 10 if $v > 10;
	$mes .= "‰R‚Ìî•ñ‚ğ—¬‚·‚Ì‚É¬Œ÷‚µ‚Ü‚µ‚½!<br>[ ˜A‘±$m{turn}‰ñ¬Œ÷ Ä°ÀÙ‹UŒv $v% ]<br>";
}
sub tp_730 { # ‹­’D¬Œ÷
	my $v = &get_mil_success('gou', 'at', 4500, 6);
	&get_mil_message('food', '‹­’D', "$v‚ÌH—¿‹­’D‚É¬Œ÷‚µ‚Ü‚µ‚½!", "H—¿‚ªs‚«‚Ü‚µ‚½!");
}
sub tp_830 { # ’³•ñ¬Œ÷
	my $v = &get_mil_success('cho', 'mat', 4500, 6);
	&get_mil_message('money', '’³•ñ', "$v‚Ì‘‹à—¬o‚É¬Œ÷‚µ‚Ü‚µ‚½!", "$e2j{money}‚ªs‚«‚Ü‚µ‚½!");
}
sub tp_930 { # ô”]¬Œ÷
	my $v = &get_mil_success('sen', 'cha', 4000, 6);
	&get_mil_message('soldier', 'ô”]', "$vl‚Ì•ºmô”]‚É¬Œ÷‚µ‚Ü‚µ‚½!", "•ºm‚ª‚à‚¤‚¢‚Ü‚¹‚ñ!");
}

#=================================================
# ˆø‚«ã‚°
#=================================================
sub tp_140 { # ‹­’D
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_y‚ÉŠïPUŒ‚‚ğÀ{B$v‚Ì•º—Æ‚ğ‹­’D‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½");
}
sub tp_240 { # ’³•ñ
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_y‚Ì‘‹à’²’BÙ°Ä‚ğŠh—‚µA$v‚Ì$e2j{money}‚ğ—¬o‚³‚¹‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½");
}
sub tp_340 { # ô”]
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_y‚Ì$v‚Ì•º‚ğô”]‚·‚é‚±‚Æ‚É¬Œ÷!$c_m‚Ì•º‚Éæ‚è‚İ‚Ü‚µ‚½");
}
sub tp_740 { # ‹­’D
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_y‚ÉŠïPUŒ‚‚ğÀ{B$v‚Ì•º—Æ‚ğ‹­’D‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½");
}
sub tp_840 { # ’³•ñ
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_y‚Ì‘‹à’²’BÙ°Ä‚ğŠh—‚µA$v‚Ì$e2j{money}‚ğ—¬o‚³‚¹‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½");
}
sub tp_940 { # ô”]
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_y‚Ì$v‚Ì•º‚ğô”]‚·‚é‚±‚Æ‚É¬Œ÷!$c_m‚Ì•º‚Éæ‚è‚İ‚Ü‚µ‚½");
}
sub exe3 {
	my $k = shift;
	my $l = shift;

	&c_up("${l}_c") for 1 .. $m{turn};
	&military_master_c_up("${l}_c");
	$m{stock} = &use_pet($l, $m{stock}) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '33');
	$m{stock} = &seed_bonus($l, $m{stock});

	# ôm‚Í’DŒR–—Í1.1”{
	$m{stock} = int($m{stock} * 1.1) if  $cs{mil}[$m{country}] eq $m{name};
	# ŒNå‚Í’DŒR–—Í1.05”{A–\ŒN‚È‚ç‚Î1.2”{
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$m{stock} = int($m{stock} * $ceo_value);
	}
#	$m{stock} = int($m{stock} * 1.05) if  $cs{ceo}[$m{country}] eq $m{name};
	$m{stock} = int($m{stock} * 1.1) if  $m{unit} eq '17';
	$m{stock} = int($m{stock} * 0.3) if  $m{unit} eq '18';
	
	# Še‘İ’è
	$m{stock} = int($m{stock} * &get_modify('mil'));
	# b‰»
	$m{stock} = &seed_bonus('red_moon', $m{stock});
	
	my $v = $m{stock} > $cs{$k}[$y{country}] ? int($cs{$k}[$y{country}]) : int($m{stock});
	$cs{$k}[$y{country}] -= $v;
	$cs{$k}[$m{country}] += $v;
	
	&write_cs;

	&special_money(int($v * 0.1)) if $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');
	&write_yran($l, $v, 0,
					"${l}_t", $v, 1) if $v > 0;
	return $v;
}

# ----------------------------
sub tp_440 { # ’ã@
	$mes .= "y$c_y‚Ìî•ñz<br>";
	$mes .= "$e2j{food}F$cs{food}[$y{country}] <br>"       if $m{turn} >= 1;
	$mes .= "$e2j{money}F$cs{money}[$y{country}] <br>"     if $m{turn} >= 2;
	$mes .= "$e2j{soldier}F$cs{soldier}[$y{country}] <br>" if $m{turn} >= 3;
	$mes .= "$e2j{tax}F$cs{tax}[$y{country}]% <br>"        if $m{turn} >= 4;
	$mes .= "$e2j{state}F$country_states[ $cs{state}[$y{country}] ]<br>" if $m{turn} >= 5;
	$mes .= "$e2j{strong}F$cs{strong}[$y{country}] <br>"   if $m{turn} >= 6;
	$mes .= "ã‹L‚Ìî•ñ‚ğ$c_m‚Ì‰ï‹cº‚É•ñ‚µ‚Ü‚·‚©?<br>";
	&menu('‚â‚ß‚é','•ñ‚·‚é');
	$m{tp} += 10;
}	
sub tp_450 {
	&c_up('tei_c') for 1 .. $m{turn};
	&military_master_c_up('tei_c');
	&use_pet('tei') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '36');
	&special_money($m{turn} * 500) if $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');

	my $lcomment = "<br>";
	my $need_count = 7;
	if ($m{turn} > $need_count) {
		$m{turn} += $m{turn} - $need_count if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
		&write_yran('tei', $m{turn}-$need_count, 1);
		$mes .= "$c_y‚Ì‰ï‹cº‚Ìî•ñ‚ğ‚¢‚­‚Â‚©“‚İ•·‚«‚Å‚«‚½<br>";
		
		my $count = $need_count;
		my @bbs_logs = ();
		open my $fh, "< $logdir/$y{country}/bbs.cgi" or &error("BBSƒƒO‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
			$mes .= "$bcomment<br>";
			$lcomment .= "$bcomment<br>";
			last if ++$count > $m{turn};
		}
		close $fh;
	}

	# BBS‚É’Ç‹L
	if ($cmd eq '1') {
		my $w_name = $m{name};
		$w_name = '–¼–³‚µ' if $w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16');
		my $comment = "y$c_yz";
		$comment .= "$e2j{food}F$cs{food}[$y{country}]/"       if $m{turn} >= 1;
		$comment .= "$e2j{money}F$cs{money}[$y{country}]/"     if $m{turn} >= 2;
		$comment .= "$e2j{soldier}F$cs{soldier}[$y{country}]/" if $m{turn} >= 3;
		$comment .= "$e2j{tax}F$cs{tax}[$y{country}]%/"        if $m{turn} >= 4;
		$comment .= "$e2j{state}F$country_states[ $cs{state}[$y{country}] ]/" if $m{turn} >= 5;
		$comment .= "$e2j{strong}F$cs{strong}[$y{country}]/"   if $m{turn} >= 6;
		$comment .= '<br>‰ï˜b‚ğ—§‚¿•·‚«‚µ‚Ü‚µ‚½' if $m{turn} > 7;
		my $comment2 = '';
		$comment2 .= $lcomment if $m{turn} > $need_count;

		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/bbs.cgi" or &error("$logdir/$m{country}/bbs.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		push @lines, $_ while <$fh>;
		pop @lines if @lines > 50;
		unshift @lines, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment<>$m{icon}<>$m{icon_pet}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if($comment2){
			unless (-f "$logdir/$m{country}/bbs_log_$y{country}.cgi") {
				open my $fh2, "> $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
				close $fh2;
			}
			
			my @lines2 = ();
			open my $fh2, "+< $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $fh2, 2; };
			push @lines2, $_ while <$fh2>;
			if(@lines2 > 50){
				pop @lines2;
			}
			unshift @lines2, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment2<>$m{icon}<>\n";
			seek  $fh2, 0, 0;
			truncate $fh2, 0;
			print $fh2 @lines2;
			close $fh2;
		}

		$mes .= "$c_m‚Ì‰ï‹cº‚É•ñ‚µ‚Ü‚µ‚½<br>";
	}
	else {
		$mes .= "$m{name}‚Ì‹¹‚Ì“à‚É”é‚ß‚Ä‚¨‚­‚±‚Æ‚É‚µ‚Ü‚µ‚½<br>";
	}

	$m{tp} = 1000;
	&n_menu;
}

# ----------------------------
sub tp_540 { # ‹UŒv
	&c_up('gik_c') for 1 .. $m{turn};
	&military_master_c_up('gik_c');
	&use_pet('gik') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '37');
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = 10 if $v > 10;
	$v = &seed_bonus('gik', $v);
	&write_yran('gik', $v, 1) if $v > 0;
	for my $i (1 .. $w{country}) {
		next if $y{country} eq $i;
		
		my $u  = &union($y{country}, $i);
		$w{"f_$u"} -= $v;
		
		if ($w{"f_$u"} < rand(10)) {
			if ($w{"p_$u"} eq '1' && $w{world} ne '6') {
				$w{"p_$u"} = 0;
				&mes_and_world_news("<b>‹UŒv‚É‚æ‚è$c_y‚Æ$cs{name}[$i]‚Æ‚Ì“¯–¿‚ğŒˆ—ô‚³‚¹‚Ü‚µ‚½</b>");
				require './lib/shopping_offertory_box.cgi';
				&get_god_item(1);
				if ($w{world} eq $#world_states-4) {
					require './lib/fate.cgi';
					&super_attack('breakdown');
				}
			}
			
			$w{"f_$u"} = int(rand(10));
		}
	}
	
	&special_money($m{turn} * 500) if $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');
	$mes .= "$c_y‚Æ‘¼‘‚Ì—FD“x‚ğ$v%‰º‚°‚é‚Ì‚É¬Œ÷‚µ‚Ü‚µ‚½<br>";
	$m{tp} = 1000;

	&run_tutorial_quest('tutorial_gikei_1');

	&n_menu;
	&write_cs;
}

#=================================================
# ¸”s
#=================================================
sub tp_1900 {
	$m{act} += $m{turn};

	# ˜A‘±‚Å“¯‚¶‘‚¾‚Æ‚Šm—¦‚ÅÀ²°Î
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( (($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2 || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		&write_world_news("$c_m‚Ì$m{name}‚ªŒR–”C–±‚É¸”s‚µ$c_y‚Ì˜S–‚É—H•Â‚³‚ê‚Ü‚µ‚½");
		&add_prisoner;
	}
	else { # ‘Ş‹p¬Œ÷
		$mes .= "‚È‚ñ‚Æ‚©“G•º‚ğU‚èØ‚é‚±‚Æ‚ª‚Å‚«‚Ü‚µ‚½<br>";
		&n_menu;
	}
	my $v = int( (rand(4)+1) );
	$m{exp} += $v;
	$m{rank_exp}-= int(rand(6)+5);
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	$mes .= "”C–±‚É¸”s‚µ‚½‚½‚ßA$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
}

#=================================================
# ¬Œ÷
#=================================================
sub tp_1000 {
	$m{act} += $m{turn};

	my $v = int( (rand(3)+3) * $m{turn} );
	$v = &use_pet('military', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '161');
	$m{exp} += $v;
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	$m{egg_c} += int(rand($m{turn})+$m{turn}) if $m{egg};

	if ($m{turn} >= 5) {
		$mes .= "”C–±‚É‘å¬Œ÷!$m{name}‚É‘Î‚·‚é•]‰¿‚ª‘å‚«‚­ã‚ª‚è‚Ü‚µ‚½<br>";
		$m{rank_exp} += $m{turn} * 3;
	}
	else {
		$mes .= "”C–±‚É¬Œ÷!$m{name}‚É‘Î‚·‚é•]‰¿‚ªã‚ª‚è‚Ü‚µ‚½<br>";
		$m{rank_exp} += int($m{turn} * 1.5);
	}
	
	&daihyo_c_up('mil_c'); # ‘ã•\n—û“x
	if ( $w{world} eq $#world_states) {
		require './lib/vs_npc.cgi';
#		if (rand(12) < $npc_mil || ($cs{strong}[$w{country}] < 50000 && rand(4) < $npc_mil) ){ 		
		if (rand(12) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(4) < 1) ) {
		   &npc_military;
		}
	}

	&after_success_action('military');

	&write_cs;
	&refresh;
	&n_menu;
}


#=================================================
# ŒR–‘Ò‚¿•š‚¹‚ÌŒ©’£‚è‚ª‚¢‚éH
#=================================================
sub is_patrol {
	my $military_kind = shift;
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/patrol.cgi" or &error("$logdir/$y{country}/patrol.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pat_time,$name) = split /<>/, $line;
		next if $time > $pat_time + $max_ambush_hour * 3600;
		next if ++$sames{$name} > 1;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# Š‘®l”‚É‘Î‚µ‚Ä‚Ç‚ê‚­‚ç‚¢„‰ñ‚µ‚Ä‚¢‚é‚©
	my $p = $w{world} eq $#world_states && $y{country} eq $w{country} ? 80 : 30;
	if (@lines > 0 && (@lines / ($cs{member}[$y{country}]+1) * 100) >= rand($p) ) {
		my $a = @lines;
		my $line = $lines[rand(@lines)];
		my($pat_time,$name) = split /<>/, $line;
		&mes_and_world_news("$c_y‚ÉŒR–sˆ×‚ğÀsB„‰ñ‚µ‚Ä‚¢‚½$name‚ÌŠÄ‹‚Ì–Ú‚ªŒõ‚è‚Ü‚µ‚½");
		
		my $yid = unpack 'H*', $name;
		if (-d "$userdir/$yid") {
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}$military_kind($date)<>";
			close $fh;
		}

		return 1;
	}
	return 0;
}

sub military_master_c_up {
	# ‚Ü‚¸–³ğŒ‚É +1 ‚µ‚»‚±‚©‚ç4ÎßÁ–ˆ‚É‚³‚ç‚É +1
	if ($m{master_c} eq $_[0]) { &c_up($_[0]) for 0 .. (int($m{turn} / 4)); }
}

sub special_money {
	$m{money} += $_[0];
	$mes .= "¡‚Ü‚Å‚ÌŒ÷Ñ‚ª”F‚ß‚ç‚ê $_[0] G‚ÌŒ÷˜J‹à‚ª‚ ‚½‚¦‚ç‚ê‚½<br>";
}

1; # íœ•s‰Â
