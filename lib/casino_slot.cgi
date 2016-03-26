#================================================
# ½Û¯ÄÀiƒvƒƒOƒŒƒbƒVƒuƒWƒƒƒbƒNƒ|ƒbƒgj
#================================================
require "$datadir/casino_bonus.cgi";

sub run {
	if ($in{mode} eq "play") {
	    $in{comment} = &play;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $jackpot) = &get_member;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="play">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="‰ñ‚·" class="button_s"><br>|;
	print qq|bet coin<select name="bet_value" class="select1">|;
	for my $i (1..3){
		print $m{c_value} == $i ? qq|<option value="$i" selected>$i bet| : qq|<option value="$i">$i bet|;
	}
	print qq|</select>|;
	print qq|</form><br>|;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="”­Œ¾" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|©“®ØÛ°ÄŞ<select name="reload_time" class="select1"><option value="0">‚È‚µ|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]•b| : qq|<option value="$i">$reload_times[$i]•b|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_cl:$member</font><br>|;
	print qq|¼Ş¬¯¸Îß¯Ä:$jackpot<br>|;

	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|ƒnƒ@ƒg|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ƒnƒ@ƒg|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bnameF$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($jackpot, $jceil) = split /<>/, $head_line;
	push @members, "$jackpot<>$jceil<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # “¯‚¶l‚È‚çŸ
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members - 1;

	return ($member_c, $member, $jackpot);
}

sub play {
	if ($m{coin} < 1000){
		$m{coin} = 0;
		&write_user;
		return ('º²İ‚ª‚ ‚è‚Ü‚¹‚ñ');
	}
	$m{c_value} = $in{bet_value};
	my @m = ('‚V');
	my @m_exval = ('‡','ô','õ','š','™','¢','¥','Ÿ','›','œ','~','¡','÷','£','','Š','‰','§','ó','ò');
	for my $val (@m_exval){
		push @m, $val for (0..5);
	}
	my @s = ();
	my $gflag = 0;
	my $rets = '';
	$s[$_] = int(rand(@m)) for (0 .. 8);
	if (&ceil_over) {
		$s[0] = 0;
		$s[1] = 0;
		$s[2] = 0;
	}
	$rets .= "<p>y$m[$s[3]]zy$m[$s[4]]zy$m[$s[5]]z</p>";
	$rets .= "<p>y$m[$s[0]]zy$m[$s[1]]zy$m[$s[2]]z</p>";
	$rets .= "<p>y$m[$s[6]]zy$m[$s[7]]zy$m[$s[8]]z</p>";
	$m{coin} -= 1000;
	if ($m[$s[0]] eq $m[$s[1]] && $m[$s[0]] eq $m[$s[2]]) {
		if ($s[0] != 0) { # jackpotˆÈŠO
			$m{coin} += 50000;
			$rets .= "‚È‚ñ‚Æ!! $m[$s[0]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!º²İ 50000 –‡Šl“¾";
		}else{
			$rets .= "Jackpot!!!";
			$rets .= &jackpot;
		}
		$gflag = 1;
	}

	if($m{c_value} >= 2){
		$m{coin} -= 1000;
		if ($m[$s[3]] eq $m[$s[4]] && $m[$s[3]] eq $m[$s[5]]) {
			if ($s[3] != 0) { # jackpotˆÈŠO
				$m{coin} += 50000;
				$rets .= "‚È‚ñ‚Æ!! $m[$s[3]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!º²İ 50000 –‡Šl“¾";
			}else{
				$rets .= "Jackpot!!!";
				$rets .= &jackpot;
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[7]] && $m[$s[6]] eq $m[$s[8]]) {
			if ($s[6] != 0) { # jackpotˆÈŠO
				$m{coin} += 50000;
				$rets .= "‚È‚ñ‚Æ!! $m[$s[6]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!º²İ 50000 –‡Šl“¾";
			}else{
				$rets .= "Jackpot!!!";
				$rets .= &jackpot;
			}
			$gflag = 1;
		}
	}
	
	if($m{c_value} == 3){
		$m{coin} -= 1000;
		if ($m[$s[3]] eq $m[$s[1]] && $m[$s[3]] eq $m[$s[8]]) {
			if ($s[3] != 0) { # jackpotˆÈŠO
				$m{coin} += 50000;
				$rets .= "‚È‚ñ‚Æ!! $m[$s[3]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!º²İ 50000 –‡Šl“¾";
			}else{
				$rets .= "Jackpot!!!";
				$rets .= &jackpot;
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[1]] && $m[$s[6]] eq $m[$s[5]]) {
			if ($s[6] != 0) { # jackpotˆÈŠO
				$m{coin} += 50000;
				$rets .= "‚È‚ñ‚Æ!! $m[$s[6]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!º²İ 50000 –‡Šl“¾";
			}else{
				$rets .= "Jackpot!!!";
				$rets .= &jackpot;
			}
			$gflag = 1;
		}
	}
	
	if($gflag == 0){
		&jackpot_add;
		$rets .= '<p>Ê½ŞÚ</p>';
	}
	&write_user;
	return ($rets);
}
sub jackpot{
	my $is_find = 0;
	my $l_is_in = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $prize = '';
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($jackpot, $jceil) = split /<>/, $head_line;
	$jceil = int(rand(100000000) + 3000000);
	push @members, "3000000<>$jceil<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # “¯‚¶l‚È‚çŸ
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	while($jackpot > 2500000){
		my $item_no = int(rand($#bonus+1));
		&send_item($m{name},$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
		if($bonus[$item_no][0] == 1){
			$prize .= "$weas[$bonus[$item_no][1]][1]";
		}elsif($bonus[$item_no][0] == 2){
			$prize .= "$eggs[$bonus[$item_no][1]][1]";
		}else{
			$prize .= "$pets[$bonus[$item_no][1]][1]";
		}

		$jackpot -= 1000000;
	}
	
	&mes_and_world_news("<b>¼Ş¬¯¸Îß¯Ä‚ğo‚µ‚Ü‚µ‚½</b>", 1);

	$m{coin} += $jackpot;
	return "º²İ $jackpot –‡ $prize ‚ğŠl“¾‚µ‚Ü‚µ‚½";
}

sub jackpot_add{
	my $is_find = 0;
	my $l_is_in = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($jackpot, $jceil) = split /<>/, $head_line;
	$jackpot += 50 * $m{c_value};
	push @members, "$jackpot<>$jceil<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # “¯‚¶l‚È‚çŸ
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	return "";
}

sub ceil_over{
	open my $fh, "< ${this_file}_member.cgi" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
	my $head_line = <$fh>;
	my($jackpot, $jceil) = split /<>/, $head_line;
	close $fh;
	
	return ($jackpot > $jceil);
}
1;#íœ•s‰Â
