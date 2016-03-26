#=================================================
# ”Ä—p½Û¯Ä
#=================================================
# ’Ç‰Á/íœ/•ÏX/•À‚Ñ‘Ö‚¦‰Â
@slots = (
	#[0]No,	[1]½Û¯Ä–¼,		[2]—˜‰v—¦,	[3]“±“üƒRƒXƒg,[4]ˆ—(”z—ñ),[5]—˜‰v—¦‰Â•Ï
	[0,		'----',			0,			0,			[sub{}],0],

	[1,		'CR´³Şªİ¹ŞÛ¶·Ş', 0.01,		1000000,	[sub{&_slot(0.01);}], 0],
	[2,		'CR“Ø•¨Œê', 	-0.2,		1000,		[sub{&_slot(-0.2);}],0],
	[3,		'CRr‚ç‚µ‰®‚ÌÊÙ‚³‚ñ', 0.1,	2000000,	[sub{&_slot(0.1);}],0],
	[4,		'Jacks or Better', -0.2,	10000,		[sub{&_jacks_or_better1();}, sub{&_jacks_or_better2();}, sub{&_jacks_or_better3(9);}],0],
	[5,		'Nines or Better', -0.4,	1000,		[sub{&_jacks_or_better1();}, sub{&_jacks_or_better2();}, sub{&_jacks_or_better3(7);}],0],
	[6,		'Better than One pair', 0.2,2000000,	[sub{&_jacks_or_better1();}, sub{&_jacks_or_better2();}, sub{&_jacks_or_better3(13);}],0],
	[7,		'CRƒfƒ‰ƒbƒNƒX“Ø•¨Œê', 0,	1000000,	[sub{&_slot($y{ag});}],1],
);

#=================================================
# ”Ä—pŠÖ”
#=================================================
sub _get_coin {
	my $coin = shift;
	$m{coin} += $coin;
	
	my $shop_id = unpack 'H*', $y{name};
	my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
	my @lines = ();
	if (-f $this_pool_file) {
		open my $fh, "+< $this_pool_file" or &error("$this_pool_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		
		while (my $line = <$fh>){
			my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
			$pool -= $coin;
			$this_term_gain -= $coin;
			if ($pool < 0) {
				&c_up('storm_c');
				close $fh;
				unlink "$userdir/$shop_id/shop_casino.cgi";
				unlink $this_pool_file;
				&mes_and_world_news("<b>$y{name}‚ÌŒo‰c‚·‚éˆá–@ƒJƒWƒm‚ğŒo‰c”j’]‚Ì‚½‚ß•Â“X‚É’Ç‚¢‚İ‚Ü‚µ‚½</b>", 1, $name);
				&refresh;
				return;
			}
			push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
			last;
		}
		
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	} else {
		&refresh;
		return;
	}
}

sub _slot_run {
	my $shop_id = unpack 'H*', $y{name};
	my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
	my @lines = ();
	if (-f $this_pool_file) {
		open my $fh, "+< $this_pool_file" or &error("$this_pool_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		
		while (my $line = <$fh>){
			my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
			$slot_runs++;
			push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
			last;
		}
		
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	} else {
		&refresh;
		return;
	}
}

#=================================================
# ½Û¯Ä
#=================================================
sub _slot {
	my $profit = shift;
	my $bet = $y{wea};
	my $success_par = 1 - $profit;
	
	if ($cmd eq '0') {
		if ($m{coin} >= $bet) {
			my @m = ('‡','ô','õ','š','‚V');
			my @o = (10, 15,  20,  30,  50); # µ¯½Ş
			my @s = ();
			$s[$_] = int(rand(@m)) for (0 .. 2);
			$mes .= "[\$$bet½Û¯Ä]<br>";
			
			if ($success_par > 1) {
				if (rand(1) < ($success_par - 1) / 5.0) {
					$s[0] = $s[1] = $s[2] = 0;
				}
			} else {
				if (rand(1) > $success_par) {
					$s[0] = int(rand(@m - 1)) + 1;
					$s[2] = ($s[0] + int(rand(@m - 1)) + 1) % @m;
				}
			}
			$mes .= "<p>y$m[$s[0]]zy$m[$s[1]]zy$m[$s[2]]z</p>";
			&_get_coin(-1 * $bet);
			&_slot_run;
			if ($s[0] == $s[1] && $s[1] == $s[2]) {
				my $v = $bet * $o[$s[0]];
				&_get_coin($v);
				$mes .= "‚È‚ñ‚Æ!! $m[$s[0]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!<br>";
				$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!!<br>';
				$mes .= "***** º²İ $v –‡ GET !! *****<br>";
				&c_up('cas_c');
				&use_pet('casino');
			}
			else {
				$mes .= '<p>Ê½ŞÚ</p>';
				$m{act} += 1;
			}
			$mes .= '‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?';
			&menu('Play!', '‚â‚ß‚é');
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	else {
		&begin;
	}
}

#=================================================
# Jacks or Better
#=================================================
sub _h_to_vj {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 53;
		$i++;
	}
	return $v;
}
sub _v_to_hj {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 53) - 1;
		$v -= $v % 53;
		$v /= 53;
		$i++;
	}
	return @h;
}

sub _jacks_or_better1 {
	my $need_money = $y{wea};
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = ();

	if ($cmd eq '0') {
		if ($m{coin} >= $need_money) {
			my $ran = $m{cas_c} > 50000 ? 1000:6000 - ($m{cas_c} / 10);
			$m{stock} = int(rand($ran));
			@h = &_draw_new(@h);

			$m{value} = &_h_to_vj(@h);
			$mes .= "y ";
			for my $i (0..4){
				$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
			}
			$mes .= "z<br>";
			$mes .= "ŒğŠ·‚·‚éƒJ[ƒh‚ğ‘I‚ñ‚Å‚Ë";
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="checkbox" name="change_0" value="1">1–‡–Ú($suit[$h[0] / 13] $num[$h[0] % 13])‚ğŒğŠ·<br>|;
			$mes .= qq|<input type="checkbox" name="change_1" value="1">2–‡–Ú($suit[$h[1] / 13] $num[$h[1] % 13])‚ğŒğŠ·<br>|;
			$mes .= qq|<input type="checkbox" name="change_2" value="1">3–‡–Ú($suit[$h[2] / 13] $num[$h[2] % 13])‚ğŒğŠ·<br>|;
			$mes .= qq|<input type="checkbox" name="change_3" value="1">4–‡–Ú($suit[$h[3] / 13] $num[$h[3] % 13])‚ğŒğŠ·<br>|;
			$mes .= qq|<input type="checkbox" name="change_4" value="1">5–‡–Ú($suit[$h[4] / 13] $num[$h[4] % 13])‚ğŒğŠ·<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="ŒğŠ·" class="button1"></p></form>|;

			$y{cha} = 1;
			&_slot_run;
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	else {
		&begin;
	} 
}

sub _jacks_or_better2 {
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @sub_h = &_v_to_hj($m{value});
	my @h = ();
	my $i;

	for my $j (0..4){
		next if $in{"change_$j"};
		push @h, $sub_h[$j];
	}
	$m{value} = &_h_to_vj(@h);

	$i = 0;
	$mes .= "y ";
	until($h[$i] eq '') {
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
		$i++;
	}
	$mes .= "z<br>";
	$y{cha} = 2;
	&n_menu;
}

sub _jacks_or_better3 {
	my $min_pair = shift; # 9:Jacks or Better
	if ($min_pair < 0 || $min_pair > 13) {
		$min_pair = 9;
	}
	my $need_money = $y{wea};
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = &_v_to_hj($m{value});

	@h = &_draw_new(@h);
	$mes .= "y ";
	for my $i (0..4){
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
	}
	$mes .= "z<br>";
	$m{value} = &_h_to_vj(@h);

	&_check_hand_j($min_pair);

	if($m{stock} == 1000){
		$mes .= "Royal Straight Flash<br>";
	}elsif($m{stock} == 200){
		$mes .= "Straight Flash<br>";
	}elsif($m{stock} == 25){
		$mes .= "Four of a kind<br>";
	}elsif($m{stock} == 10){
		$mes .= "Full House<br>";
	}elsif($m{stock} == 7){
		$mes .= "Flash<br>";
	}elsif($m{stock} == 5){
		$mes .= "Straight<br>";
	}elsif($m{stock} == 4){
		$mes .= "Three of a kind<br>";
	}elsif($m{stock} == 3){
		$mes .= "Two pair<br>";
	}elsif($m{stock} == 1){
		my @pairs = ('----', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Sevens', 'Eights', 'Nines', 'Tens', 'Jacks', 'Queens', 'Kings', 'Aces');
		$mes .= $min_pair > 0 ? $pairs[$min_pair] . " or Better<br>" : 'One pair';
	}else{
		$mes .= "No pair<br>";
	}

	if ($m{stock} > 0) { 
		$m{stock} *= $need_money;
		$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
		$mes .= "º²İ $m{stock} –‡ Get!<br>";
		&_get_coin($m{stock});
		$m{stock} = $m{value} = 0;
		&menu('play','‚â‚ß‚é');
		&c_up('cas_c');
		&use_pet('casino');
	}
	else { # •‰‚¯
		&_get_coin(-1 * $need_money);
		$m{stock} = $m{value} = 0;
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 5;
	}
	$y{cha} = 0;
}

sub _draw_new{
	my $c;
	my $j;
	my @h;
	$j = 0;
	until($_[$j] eq ''){
		$h[$j] = $_[$j];
		$j++;
	}
	for my $i (0..4){
		next if $h[$i] ne '';
		while(1){
			$c = int(rand(52));
			my $go = 1;
			for $j(0..$i-1){
				$go = 0 if $h[$j] == $c;
			}
			last if $go == 1;
		}
		$h[$i] = $c;
	}
	if($m{stock} == 1){
		@h = (12,10,9,11,0);
	}
	if($m{stock} == 2){
		@h = (25,13,22,24,23);
	}
	if($m{stock} == 3){
		@h = (26,38,35,37,36);
	}
	if($m{stock} == 4){
		@h = (48,51,39,50,49);
	}
	if($m{stock} == 5){
		@h = (1,10,9,11,0);
	}
	if($m{stock} == 6){
		@h = (25,0,22,24,23);
	}
	if($m{stock} == 7){
		@h = (26,38,34,37,36);
	}
	if($m{stock} == 8){
		@h = (48,26,39,50,49);
	}
	$m{stock} = 0;
	$j = 1;
	while(1){
		last if $h[$j] eq '';
		if($h[$j-1] > $h[$j]){
			my $tem = $h[$j-1];
			$h[$j-1] = $h[$j];
			$h[$j] = $tem;
			$j = 1;
			next;
		}
		$j++;
	}

	return @h;
}

sub _check_hand_j{
	my $min_pair = shift;
	my @h = &_v_to_hj($m{value});
	my $is_straight = 0;
	my $is_royal = 0;
	my $is_flash = 0;
	my $is_four = 0;
	my $is_three = 0;
	my $pair_num = 0;
	my $pair_high = 0;
	my @subh = ();
	my @suith = ();
	my $i;

	for $i (0..4){
		$subh[$i] = $h[$i] % 13;
		$suith[$i] = ($h[$i] - $subh[$i]) / 13;
	}
	$i = 1;
	while(1){
		last if $subh[$i] eq '';
		if($subh[$i-1] > $subh[$i]){
			my $tem = $subh[$i-1];
			$subh[$i-1] = $subh[$i];
			$subh[$i] = $tem;
			$i = 1;
			next;
		}
		$i++;
	}
	if($subh[0]+1 == $subh[1]&& $subh[0]+2 == $subh[2] && $subh[0]+3 == $subh[3] && $subh[0]+4 == $subh[4]){
		$is_straight = 1;
	}
	if($subh[0] == 0 && $subh[1] == 9 && $subh[2] == 10 && $subh[3] == 11 && $subh[4] == 12){
		$is_royal = 1;
		$is_straight = 1;
	}
	if($suith[0] == $suith[1] && $suith[0] == $suith[2] && $suith[0] == $suith[3] && $suith[0] == $suith[4]){
		$is_flash = 1;
	}
	for $i (0..12){
		my $card = 0;
		for my $j (0..4){
			$card++ if $subh[$j] == $i;
		}
		if($card == 4){
			$is_four = 1;
		}elsif($card == 3){
			$is_three = 1;
		}elsif($card == 2){
			$pair_num++;
			$pair_high = $i;
		}
	}

	if($is_royal && $is_straight && $is_flash){
		$m{stock} = 1000;
	}elsif($is_straight && $is_flash){
		$m{stock} = 200;
	}elsif($is_four){
		$m{stock} = 25;
	}elsif($is_three && $pair_num == 1){
		$m{stock} = 10;
	}elsif($is_flash){
		$m{stock} = 7;
	}elsif($is_straight){
		$m{stock} = 5;
	}elsif($is_three){
		$m{stock} = 4;
	}elsif($pair_num == 2){
		$m{stock} = 3;
	}elsif($pair_num == 1 && ($pair_high > $min_pair || $pair_high == 0)){
		$m{stock} = 1;
	}else{
		$m{stock} = 0;
	}
}
1; # íœ•s‰Â
