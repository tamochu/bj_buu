#================================================
# ¤l‚Ì‹âs Created by Merino
#================================================

# ˆê‚Â‚Ì‹âs‚Å—˜—p‚Å‚«‚éÅ‘ål”
my $max_player_bank = 10;

# Å’á“ü‹àŠz
my $min_save_money = 10000;

# ‰Šú—a‹à§ŒÀ
my $default_max = 4999999;

#================================================
# ‹âs‚Ì–¼‘Oˆê——•\¦
#================================================
sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "Œ»İŒ_–ñ‚µ‚Ä‚¢‚é‹âsyŒo‰cÒ $m{bank}z<br>" if $m{bank};
	$mes .= "‚Ç‚±‚Ì‹âs‚És‚«‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= $m{bank} ? qq|<input type="radio" name="cmd" value="0">‚â‚ß‚é<br>|:qq|<input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>‹âs–¼</th><th>Œo‰cÒ</th><th>Ğ‰î•¶<br></th></tr>| unless $is_mobile;

	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		my $shop_id = unpack 'H*', $name;
		next unless -f "$userdir/$shop_id/shop_bank.cgi";

		if ($m{bank} eq $name){
			$is_find = 1;
			$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name" checked>$shop_name<br>|
				 : qq|<tr><td><input type="radio" name="cmd" value="$name" checked>$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
		}else {
			$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
				 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;		
		}
	}
	close $fh;
	$m{bank} = '' unless $is_find;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="‹âs‚É“ü‚é" class="button1"></p></form>|;
}

#================================================
# ‹âs“ü“X
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;
	
	# ‹âs‚ª‘¶İ‚µ‚È‚¢
	if (!$is_find || !-f "$userdir/$shop_id/shop_bank.cgi") {
		$mes .= "$m{stock}‚Æ‚¢‚¤‹âs‚Í•Â“X‚µ‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·<br>";
		&begin;
	}
	else {
		my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
		$mes .= "y$m{stock}zè”—¿$fee G / —˜—¦ $rishi % / —a‹àãŒÀ $max_dep G<br>";
		$mes .= "$y{name}u$shop_messagev<br>";
		
		&menu('‚â‚ß‚é', '‚²“ü‹à', '‚¨ˆøo‚µ');
		$m{tp} = 10;
	}
}

sub tp_10 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

sub bank_price {
	my $bank_file = shift;
	
	open my $fh, "< $bank_file" or &error("$bank_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $line;
	$max_pla = $max_player_bank unless $max_pla;	
	$max_dep = $default_max unless $max_dep;
	$rishi /= 10.0;
	return $fee, $rishi, $max_pla, $max_dep;
}



#================================================
# “ü‹à
#================================================
sub tp_100 {
	if ($m{bank} ne '' && $m{bank} ne $y{name}) {
		$mes .= "‘¼‚Ì‹âs‚ğ—˜—p‚·‚éê‡‚ÍAŒ»İ—˜—p‚µ‚Ä‚¢‚é‹âs‚©‚ç‘SŠzˆøo‚·•K—v‚ª‚ ‚è‚Ü‚·<br>";
		&begin;
		return;
	}
	my $shop_id = unpack 'H*', $y{name};
	
	my $count = 0;
	my $last_year = '';
	my $save_money = 0;
	open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
		++$count;
	}
	close $fh;
	
	my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
	if ($save_money > 0 || $count < $max_pla) {
		$mes .= qq|y$m{stock}zè”—¿$fee G / —˜—¦ $rishi% / —a‹àãŒÀ $max_dep G<br>|;
		$mes .= qq|$world_name—ï$last_year”N‚©‚ç $save_money G —a‚¯‚Ä‚¢‚Ü‚·<br>| if $save_money > 0;
		$mes .= qq|‚¢‚­‚ç“ü‹à‚µ‚Ü‚·‚©?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="text" name="save_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<p><input type="submit" value="“ü‹à" class="button1"></p></form>|;
		
		$m{tp} = 110;
		&n_menu;
	}
	else {
		$mes .= "$m{stock}‚Í’èˆõ‚ª‚¢‚Á‚Ï‚¢‚ÅA‚²—˜—p‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&begin;
	}
}
sub tp_110 {
	if ($in{save_money} <= 0 || $in{save_money} =~ /[^0-9]/) {
		$mes .= "‚â‚ß‚Ü‚µ‚½<br>";
		&begin;
		return;
	}
	elsif ($min_save_money > $in{save_money}) {
		$mes .= "“ü‹àŠz‚ÍÅ’á‚Å‚à $min_save_money GˆÈã•K—v‚Å‚·<br>";
		&tp_100;
		return;
	}

	my $shop_id = unpack 'H*', $y{name};
	my $save_money = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $head_line;
	$max_pla = $max_player_bank unless $max_pla;	
	$max_dep = $default_max unless $max_dep;

	# ‘SŠz
	if ($in{save_money} > $m{money}) {
		$in{save_money} = $m{money} - $fee;
		if ($m{name} ne $y{name} && $in{save_money} < $fee) {
			close $fh;
			$mes .= "è”—¿($fee G)‚ª‘«‚è‚Ü‚¹‚ñ<br>";
			&tp_100;
			return;
		}
	}
	elsif ($m{name} ne $y{name} && $m{money} - $in{save_money} < $fee) {
		close $fh;
		$mes .= "è”—¿($fee G)‚ª‘«‚è‚Ü‚¹‚ñ<br>";
		&tp_100;
		return;
	}
	
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($name eq $m{name}) {
			$save_money = $money;
		}
		else {
			push @lines, $line;
		}
	}
	
	if ($save_money + $in{save_money} > $max_dep) {
		$in{save_money} = $max_dep - $save_money;
		$save_money = $max_dep;
	}
	else {
		$save_money += $in{save_money};
	}
	$m{money} -= $in{save_money};

	if ($m{name} ne $y{name}) {
		$m{money} -= $fee;
		&send_money($y{name}, "y$m{stock}(è”—¿)z$m{name}", $fee);

		# ”„ã‹à‰ÁZ
		open my $fh2, "+< $userdir/$shop_id/shop_sale_bank.cgi" or &error("”„ãÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($sale_c, $sale_money,$update_t) = split /<>/, $line2;
		$sale_c++;
		$sale_money += $fee;
		seek  $fh2, 0, 0;
		truncate $fh2, 0;
		print $fh2 "$sale_c<>$sale_money<>$update_t<>";
		close $fh2;
		$mes .= "è”—¿ $fee G‚ğx•¥‚¢A";
	}

	push @lines, "$w{year}<>$m{name}<>$save_money<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "$in{save_money} G“ü‹à‚µ‚Ü‚µ‚½(—a‹àŠz $save_money G)<br>";
	$m{bank} = $y{name};
	&tp_1;
}

#================================================
# ‚¨ˆøo‚µˆ—
#================================================
sub tp_200 {
	my $shop_id = unpack 'H*', $y{name};
	
	my $last_year = 0;
	my $save_money = 0;
	open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
	}
	close $fh;
	
	if ($save_money == 0) {
		if($y{name} eq $m{bank}){
			$m{bank} = '';
		}
		$mes .= "$m{name}‚³‚ñ‚©‚ç‚Ì‚¨‹à‚Í—a‚©‚Á‚Ä‚¢‚Ü‚¹‚ñ<br>";
		&begin;
	}
	else {
		my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
		$mes .= qq|y$m{stock}zè”—¿$fee G / —˜—¦ $rishi% / —a‹àãŒÀ $max_dep G<br>|;
		$mes .= qq|$world_name—ï$last_year”N‚©‚ç $save_money G —a‚¯‚Ä‚¢‚Ü‚·<br>‚¢‚­‚çˆøo‚µ‚Ü‚·‚©?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="get_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="ˆøo‚µ" class="button1"></p></form>|;
		
		$m{tp} += 10;
		&n_menu;
	}
}
sub tp_210 {
	$cmd = $y{name};
	if ($in{get_money} <= 0 || $in{get_money} =~ /[^0-9]/) {
		$mes .= "‚â‚ß‚Ü‚µ‚½<br>";
		&tp_1;
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };

	my $head_line = <$fh>;
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $head_line;
	my $v;
	
	if ($m{name} ne $y{name} && $m{money} < $fee) {
		$mes .= "è”—¿($fee G)‚ª‘«‚è‚Ü‚¹‚ñ";
		&tp_1;
		return;
	}
	
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;

		if ($m{name} eq $name) {
			$is_rewrite = 1;
			
			$v = int( $money * ($w{year} - $year) * $rishi * 0.001);
			$in{get_money} = $money if $in{get_money} >= $money;
			$m{money} += int($in{get_money} + $v);
			$money -= $in{get_money};
			
			if ($m{name} ne $y{name}) {
				$m{money} -= $fee;
				&send_money($y{name}, "y$m{stock}(è”—¿)z$m{name}", $fee);
				$mes .= "è”—¿ $fee G ‚ğx•¥‚¢A" ;
			}

			$mes .= "$in{get_money} Gˆøo‚µ‚Ü‚µ‚½(—a‹àŠz $money G)<br>";
			
			if ($v > 0 && $m{name} ne $y{name}) {
				$mes .= "”N—˜‚Æ‚µ‚Ä $v Gˆøo‚µŠz‚ÉÌß×½‚³‚ê‚Ü‚µ‚½<br>";
			}
			
			if ($money <= 0) {
				$m{bank} = '';
				$mes .= "“ü‹à‹àŠz‚ª 0 GˆÈ‰º‚É‚È‚è‚Ü‚µ‚½‚Ì‚ÅA$m{stock}‚ÆŒ_–ñ‚ªI—¹‚µ‚Ü‚µ‚½<br>";
			}
			else {
				push @lines, "$w{year}<>$m{name}<>$money<>\n";
			}
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

	if ($v > 0 && $m{name} ne $y{name}) {
		&send_rishi($v);
	}
	&begin;
}

sub send_rishi {
	my $v = shift;
	my $y_id = unpack 'H*', $y{name};
	my %owner_datas = &get_you_datas($y_id, 1);
	my $same_bank = 0;
	
	if($owner_datas{bank} ne ''){
		my $shop_id = unpack 'H*', $owner_datas{bank};
	
		my $is_find = 0;
		open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
			if ($owner_datas{bank} eq $name) {
				$is_find = 1;
				last;
			}
		}
		close $fh;
	
		if (!$is_find || !-f "$userdir/$shop_id/shop_bank.cgi") {
			&send_money($y{name}, "y$m{stock}(”N—˜‘ã)z$m{name}", "-$v");
		}
		else {
			my @lines = ();
			open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $fh, 2; };

			my $head_line = <$fh>;
			push @lines, $head_line;
			while (my $line = <$fh>) {
				my($year, $name, $money) = split /<>/, $line;

				if ($y{name} eq $name) {
					if ($v >= $money){
						my $diff = $v - $money;
						&send_money($y{name}, "y$m{stock}(”N—˜‘ã)z$m{name}", "-$diff");
						$v = $money;
					}
					$money -= $v;
			
					if ($money <= 0) {
						&regist_you_data($y{name},'bank','');
					}
					else {
						push @lines, "$year<>$name<>$money<>\n";
					}
				}
				else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	else {
		&send_money($y{name}, "y$m{stock}(”N—˜‘ã)z$m{name}", "-$v");
	}
}

1; # íœ•s‰Â
