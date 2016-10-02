my $entry_file = $m{sex} eq '1' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
#my $this_file  = $m{sex} eq '2' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
my $this_file;
if (($m{sex} eq '2' && $pets[$m{pet}][2] ne 'marriage_y') || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b')){
   $this_file  = "$logdir/marriage_man.cgi";
   }
   else{
   $this_file = "$logdir/marriage_woman.cgi";
}
#================================================
# Œ‹¥‘Š’kŠ Created by Merino
#================================================

# Å‘å“o˜^”:ŒÃ‚¢l‚Í©“®íœ
my $max_marriage_list = 20;

# ÚÍŞÙ§ŒÀ:‚±‚ÌÚÍŞÙˆÈã‚Å‚È‚¢‚Æ—˜—p‚Å‚«‚È‚¢
my $need_lv = 20;

# “o˜^—¿,ÌßÛÎß°½Ş—¿
my $need_money = $m{sedai} > 20 ? int(40000+$m{lv}*1000) : int($m{sedai}*2000+$m{lv}*1000);


#================================================
# —˜—pğŒ
#================================================
sub is_satisfy {
	if ($m{lv} < $need_lv) { # Lv
		$mes .= "Œ‹¥‘Š’kŠ‚ÍALv.$need_lvˆÈã‚Ì•û‚Å‚È‚¢‚Æ“ü‚ê‚Ü‚¹‚ñ<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{marriage}) { # Šù¥
		$mes .= "•s—Ï‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{job} eq '24') { # –‚–@­—
		$mes .= "–‚–@­—‚Í‰i‰“‚Ì14Î‚Å‚·<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚ ‚è‚Ü‚·‚©?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '‚±‚±‚ÍŒ‹¥‘Š’kŠ‚Å‚²‚´‚¢‚Ü‚·<br>';
		$mes .= '–{“ú‚Í‚Ç‚Ì‚æ‚¤‚È‚²—pŒ‚Å‚µ‚å‚¤‚©?<br>';
	}
	
	&menu('‚â‚ß‚é','Êß°ÄÅ°‚ğ’T‚·','“o˜^‚·‚é','¥–ñ‚·‚é');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# Êß°ÄÅ°’T‚·
#================================================
sub tp_100 {
	$layout = 1;
	$mes .= '‚±‚¿‚ç‚ªA“o˜^ÒØ½Ä‚É‚È‚è‚Ü‚·<br>';
	$mes .= '‹C‚É‚È‚é•û‚ª‚¢‚Ü‚µ‚½‚ç±ÌßÛ°Á‚ğ‚µ‚Ä‚İ‚Ä‚Í‚¢‚©‚ª‚Å‚·‚©?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>Lv</th><th>ŠK‹‰</th><th>Ò¯¾°¼Ş<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		next if $name eq $m{name};
		my $rank_name = &get_rank_name($rank, $name);
		my $bname = &name_link($name);
		$bname .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/Lv$lv/ŠK‹‰$rank\name/$message<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="±ÌßÛ°Á‚·‚é" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
# ------------------
# ±ÌßÛ°Á
sub tp_110 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			last;
		}
	}
	close $fh;

	unless ($send_to) {
		$mes .= '“o˜^ÒØ½Ä‚É“o˜^‚³‚ê‚Ä‚¢‚È‚¢l‚É‚Í±ÌßÛ°Á‚Å‚«‚Ü‚¹‚ñ<br>';
		&begin;
		return;
	}

	$layout = 1;
	$mes .= "±ÌßÛ°Á(‘Šè‚ÉÒ¯¾°¼Ş‚ğ‘—‚é)‚Í–³—¿‚Å‚·<br>";
	$mes .= "ÌßÛÎß°½Ş‚ÍA¬Œ÷‚µ‚Ä‚à¸”s‚µ‚Ä‚à $need_money G‚©‚©‚è‚Ü‚·‚Ì‚ÅA<br>ÌßÛÎß°½Ş‚Íe–§‚ÈŠÖŒW‚É‚È‚Á‚Ä‚©‚ç‚É‚µ‚Ü‚µ‚å‚¤<br>";
	
	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$cmd">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|[$send_to]‚É±ÌßÛ°Á<br>|;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="submit" value="è†‚ğ‘—‚é/‚â‚ß‚é" class="button1">|;
	$mes .= qq|@ <input type="checkbox" name="is_proposal" value="1"> ÌßÛÎß°½Ş</form>|;
	$m{tp} += 10;
}
# ------------------
sub tp_120 {
	if (!$in{comment}) {
		$mes .= '–{•¶‚ª‚ ‚è‚Ü‚¹‚ñ<br>';
		&begin;
		return;
	}
	elsif ($in{is_proposal}) {
		if ( !&is_entry_marriage($m{name}) ) {
			$mes .= "ÌßÛÎß°½Ş‚·‚é‚É‚Í“o˜^‚·‚é•K—v‚ª‚ ‚è‚Ü‚·<br>";
			&begin;
			return;
		}
		elsif ($m{money} < $need_money) {
			$mes .= "ÌßÛÎß°½Ş‚·‚é‚É‚Í $need_money G•K—v‚Å‚·<br>";
			&begin;
			return;
		}
	}
	
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			if ($name eq $m{name}) { # «“]Š·‚É‚æ‚è
				$mes .= '©•ª‚É±ÌßÛ°Á‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
				$is_rewrite = 1;
			}
			elsif ( &is_unmarried($name) ) { # ‘¶İ‚·‚é + –¢¥‚È‚ç
				$in{comment} .= "<hr>yŒ‹¥‘Š’kŠF$m{name}—l‚©‚ç$name—lˆ¶z";
				$in{comment} .= "™ÌßÛÎß°½Ş™" if $in{is_proposal};
				&send_letter($name);
				$mes .= "$name‚É±ÌßÛ°Á‚Ìè†‚ğ‘—‚è‚Ü‚µ‚½<br>";
				
				# ÌßÛÎß°½Ş
				&proposal($name) if $in{is_proposal};
				
				push @lines, $line;
			}
			else {
				if (($m{sex} eq '2' && $pets[$m{pet}][2] eq 'marriage_y') || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b')){
					$is_rewrite = 0;
   				}
				else{
					$is_rewrite = 1;
				}
			}
		}
		else {
			push @lines, $line;
		}
	}
	# ‘¶İ‚µ‚È‚¢lA«“]Š·‚µ‚½lAŠù¥‚Ìl‚ª‚¢‚½‚ç‘‚«Š·‚¦
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	&begin;
}

# ------------------
# ÌßÛÎß°½Ş
sub proposal {
	my $name = shift;
	
	my $y_id = unpack 'H*', $name;
	my @lines = ();
	open my $fh, "+< $userdir/$y_id/proposal.cgi" or &error("$userdir/$y_id/proposal.cgiÌ§²Ù‚ªŠJ‚«‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pname) = (split /<>/, $line)[2];
		next if $pname eq $m{name};
		push @lines, $line
	}
	my($last_no) = (split /<>/, $lines[0])[0];
	++$last_no;
	unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	$mes .= "ÌßÛÎß°½Ş‘ã $need_money G‚ğx•¥‚¢A$name‚ÉÌßÛÎß°½Ş‚µ‚Ü‚µ‚½<br>";
	$m{money} -= $need_money;
}

#================================================
# “o˜^
#================================================
sub tp_200 {
	$layout = 2;
	my $sex_name   = $m{sex} eq '1' ? '’j«' : '—«';
	
	$mes .= qq|“o˜^‚·‚é‚É‚ÍA$need_money G‚©‚©‚è‚Ü‚·<br>|;
	$mes .= qq|<hr>Œ»İ“o˜^‚³‚ê‚Ä‚¢‚é$sex_nameØ½Ä<br>|;
	$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>Lv</th><th>ŠK‹‰</th><th>Ò¯¾°¼Ş<br></th></tr>| unless $is_mobile;

	open my $fh, "< $entry_file" or &error("$entry_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		my $rank_name = &get_rank_name($rank, $name);
		my $bname = &name_link($name);
		$bname .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr>$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/Lv$lv/ŠK‹‰$rank_name/$message<br>|
			 : qq|<tr><td>$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;

	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="submit" value="‘—M" class="button1">|;
	$mes .= qq|@ <input type="checkbox" name="cmd" value="1" checked>“o˜^‚·‚é</form>|;
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1);

	my $is_find = 0;
	my @lines = ();
	open my $fh, "+< $entry_file" or &error("$entry_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($name eq $m{name}) {
			$is_find = 1;
			last;
		}
		push @lines, $line;

		last if @lines >= $max_marriage_list+1;
	}
	if ($is_find) {
		close $fh;
		$mes .= "$m{name}—l‚Í‚·‚Å‚É‚²“o˜^Ï‚İ‚Å‚·<br>";
	}
	elsif ($m{money} < $need_money) {
		close $fh;
		$mes .= "“o˜^‚·‚é‚¨‹à‚ª‘«‚è‚Ü‚¹‚ñ<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		my $comment = $in{comment} . $m{mes};
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$comment<>$m{icon}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "“o˜^—¿ $need_money G‚ğx•¥‚¢‚Ü‚µ‚½<br>";
		$mes .= "$m{name}—l‚Å‚·‚ËB‚²“o˜^‚¢‚½‚µ‚Ü‚µ‚½<br>";
		$m{money} -= $need_money;
	}
	
	&begin;
}


#================================================
# ¥–ñ‚·‚é
#================================================
sub tp_300 {
	if($pets[$m{pet}][2] eq 'marriage' || (($pets[$m{pet}][2] eq 'marriage_y' || $pets[$m{pet}][2] eq 'marriage_b') && $m{pet_c} >= 5)) {
		$layout = 1;
		$mes .= '‚±‚¿‚ç‚ªA“o˜^ÒØ½Ä‚É‚È‚è‚Ü‚·<br>';
		$mes .= '´Û½‚Ì—Í‚É‚æ‚è‰i‰“‚Ìˆ¤‚ğ¾‚¢‚Ü‚·<br>';
		
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
		$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>Lv</th><th>ŠK‹‰</th><th>Ò¯¾°¼Ş<br></th></tr>| unless $is_mobile;

		open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			my $rank_name = &get_rank_name($rank, $name);
			my $bname = &name_link($name);
			$bname .= "[$shogo]" if $shogo;
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/Lv$lv/ŠK‹‰$rank_name/$message<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
		}
		close $fh;
		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="‰i‰“‚Ìˆ¤‚ğ¾‚¤" class="button1"></p></form>|;

		$m{tp} += 10;
	}
	elsif (-s "$userdir/$id/proposal.cgi") {
		$layout = 1;
		$mes .= 'ÌßÛÎß°½ŞÒˆê——<br>';
			
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
		$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>Lv</th><th>ŠK‹‰</th><th>Ò¯¾°¼Ş<br></th></tr>| unless $is_mobile;
		
		open my $fh, "< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi Ì§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			my $rank_name = &get_rank_name($rank, $name);
			my $bname = &name_link($name);
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$bname/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/Lv$lv/ŠK‹‰$rank_name/$message<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$no">$bname</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$rank_name</td><td>$message<br></td></tr>|;
		}
		close $fh;
		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="‰i‰“‚Ìˆ¤‚ğ¾‚¤" class="button1"></p></form>|;
		
		$m{tp} += 10;
	}
	else {
		$mes .= '‚Ü‚¾A’N‚©‚ç‚àÌßÛÎß°½Ş‚³‚ê‚Ä‚¢‚È‚¢‚æ‚¤‚Å‚·<br>';
		$mes .= '‘Ò‚Á‚Ä‚¢‚Ä‚àn‚Ü‚è‚Ü‚¹‚ñ<br>‚±‚¿‚ç‚©‚ç±ÌßÛ°Á‚µ‚Ä‚İ‚Ä‚Í‚¢‚©‚ª‚Å‚µ‚å‚¤?<br>';
		&begin;
	}
}
# Œ‹¥
sub tp_310 {
	if ($cmd && $pets[$m{pet}][2] eq 'marriage' || (($pets[$m{pet}][2] eq 'marriage_y' ||$pets[$m{pet}][2] eq 'marriage_b') && $m{pet_c} >= 5)) {
		my $is_rewrite = 0;
		my @lines = ();
		my $c;
		open my $tfh, "+< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $tfh, 2; };
		while (my $line = <$tfh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($cmd eq $no) {
				if ($name eq $m{name}) { # «“]Š·‚É‚æ‚è
					$mes .= '©•ª‚É±ÌßÛ°Á‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
					$is_rewrite = 1;
				}
				elsif ( &is_unmarried($name) ) {
					my @plines = ();
					open my $pfh, "+< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgiÌ§²Ù‚ªŠJ‚«‚Ü‚¹‚ñ");
					eval { flock $pfh, 2; };
					while (my $pline = <$pfh>) {
						my($pname) = (split /<>/, $pline)[2];
						next if $pname eq $name;
						push @plines, $pline
					}
					my($last_no) = (split /<>/, $plines[0])[0];
					++$last_no;
					unshift @plines, "$last_no<>$mdate<>$name<>$country<>$lv<>$rank<>$shogo<>$message<>$icon<>\n";
					seek  $pfh, 0, 0;
					truncate $pfh, 0;
					print $pfh @plines;
					close $pfh;
					$c = $last_no;
					push @lines, $line;
				}
				else {
					$is_rewrite = 1;
				}
			}
			else {
				push @lines, $line;
			}
		}
	# ‘¶İ‚µ‚È‚¢lA«“]Š·‚µ‚½lAŠù¥‚Ìl‚ª‚¢‚½‚ç‘‚«Š·‚¦
		if ($is_rewrite) {
			seek  $tfh, 0, 0;
			truncate $tfh, 0;
			print $tfh @lines;
		}
		close $tfh;
		if($c){
			$cmd = $c;
			&remove_pet if($pets[$m{pet}][2] eq 'marriage');
		}else {
			$cmd = 0;
		}
	}

	if ($cmd) {
		my $is_marriage = 0;
		open my $fh, "+< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi Ì§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($cmd eq $no) {
				if ( &is_unmarried($name) ) {
					$mes .= "$name‚ÆŒ‹¥‚·‚é‚±‚Æ‚ÉŒˆ‚ß‚Ü‚µ‚½!<br>";
					
					# ‘Šè‚ÌŒ‹¥€–Ú‚ğ•ÏX
					&regist_you_data($name, 'marriage', $m{name});
					
					$m{marriage} = $name;
					$is_marriage = 1;
					if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
						$m{job} = 0;
					}
					
					# ‘Šè‚Ìv‚¢oÌ§²Ù‚É‘‚«‚İ
					&write_memory("$m{name}‚ÆŒ‹¥‚µ‚Ü‚µ‚½™", $name);
					&write_memory("$name‚ÆŒ‹¥‚µ‚Ü‚µ‚½™");
					my %you_datas = &get_you_datas($name);
					my $v = int( ($rank_sols[$you_datas{rank}] + $rank_sols[$m{rank}]) * 0.5);
					if($m{sex} eq $you_datas{sex}) {
						&write_world_news(qq|<font color="#8a2be2">ƒ™:ß*'“¯«Œ‹¥'*ß:™„$m{name}‚Æ$name‚ªŒ‹¥‚µ‚Ü‚µ‚½</font>|);
						&send_twitter("ƒ™:ß*'“¯«Œ‹¥'*ß:™„$m{name}‚Æ$name‚ªŒ‹¥‚µ‚Ü‚µ‚½");
						if(int(rand(5)) == 0){
							&remove_pet;
						}elsif(int(rand(5)) == 0 && ($pets[$you_datas{pet}][2] eq 'marriage_y' || $pets[$you_datas{pet}][2] eq 'marriage_b')) {
							&regist_you_data($name, 'pet', 0);
						}
						$v *= 3;
					}else {
						&write_world_news(qq|<font color="#FF99FF">ƒ™:ß*'Œ‹¥'*ß:™„$m{name}‚Æ$name‚ªŒ‹¥‚µ‚Ü‚µ‚½</font>|);
						&send_twitter("ƒ™:ß*'Œ‹¥'*ß:™„$m{name}‚Æ$name‚ªŒ‹¥‚µ‚Ü‚µ‚½");
					}
					if($you_datas{job} eq '22' || $you_datas{job} eq '23' || $you_datas{job} eq '24'){
						&regist_you_data($name, 'job', 0);
					}
					
					&send_money($name,    'Œ‹¥j‚¢‹à', $v);
					&send_money($m{name}, 'Œ‹¥j‚¢‹à', $v);
					
					# “o˜^‚³‚ê‚Ä‚¢‚é–¼‘O‚ğíœ
					&delete_entry_marriage($m{name});
					&delete_entry_marriage($name);
					
					last;
				}
			}
			else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines unless $is_marriage; # Œ‹¥‚ğ‘I‘ğ‚µ‚½‚ªA‰½‚ç‚©‚Ì–â‘è‚ÅŒ‹¥‚Å‚«‚¸A‚»‚Ìl‚ğœ‚«ã‘‚«
		close $fh;
	}
	
	&begin;
}


#================================================
# –¢¥‚©‚Ç‚¤‚©
#================================================
sub is_unmarried {
	my $name = shift;
	my $y_id = unpack 'H*', $name;

	unless (-f "$userdir/$y_id/user.cgi") {
		$mes .= "c”O‚È‚±‚Æ‚É$name—l‚Í‚·‚Å‚É‘¼ŠE‚µ‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·c<br>";
		return 0;
	}
	
	my %you_datas = &get_you_datas($name);
	
	if ($m{sex} eq $you_datas{sex}) {
		if(($m{sex} eq '2' && $pets[$m{pet}][2] eq 'marriage_y' && ($m{pet} == $you_datas{pet} || $m{pet_c} >= 5)) || ($m{sex} eq '1' && $pets[$m{pet}][2] eq 'marriage_b' && ($m{pet} == $you_datas{pet} || $m{pet_c} >= 5))) {
			if ($you_datas{marriage} eq '') { # –¢¥
				return 1;
			}
			else {
				$mes .= "c”O‚È‚±‚Æ‚É$name—l‚Í‚·‚Å‚É‘¼‚Ìl‚ÆŒ‹¥‚µ‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·c<br>";
				return 0;
			}
		}else {
			$mes .= "c”O‚È‚±‚Æ‚É$name—l‚Í«•Ê‚ª•Ï‚í‚Á‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·c<br>";
			return 0;
		}
	}
	elsif ($you_datas{marriage} eq '') { # –¢¥
		return 1;
	}
	else {
		$mes .= "c”O‚È‚±‚Æ‚É$name—l‚Í‚·‚Å‚É‘¼‚Ìl‚ÆŒ‹¥‚µ‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·c<br>";
		return 0;
	}
}

#================================================
# “o˜^Ò‚©‚Ç‚¤‚©
#================================================
sub is_entry_marriage {
	my $entry_name = shift || $m{name};
	
	open my $fh, "< $entry_file" or &error("$entry_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[2];
		return 1 if $name eq $entry_name;
	}
	close $fh;
	
	return 0;
}

#================================================
# “o˜^íœ
#================================================
sub delete_entry_marriage {
	my $del_name = shift || $m{name};
	
	for my $file ($entry_file, $this_file) {
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $file" or &error("$fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($name eq $del_name) {
				$is_rewrite = 1;
			}
			else {
				push @lines, $line;
			}
		}
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;
	}
}


1; # íœ•s‰Â
