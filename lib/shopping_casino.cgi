$mes .= qq|º²İ $m{coin} –‡<br>| if ($is_mobile || $is_smart);
#================================================
# ¶¼ŞÉ Created by Merino
#================================================
# @mcmark @ocozz ‚ÌˆÓ–¡
$base_bet = 10;

#=================================================
# —˜—pğŒ
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]‚Ì•û‚Ío“ü‚è‹Ö~‚Å‚·<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ”æ˜J‚µ‚Ä‚¢‚éê‡‚Ís‚¦‚È‚¢
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚â‚Á‚¿‚á‚¤?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "‚¢‚ç‚Á‚µ‚á`‚¢ô¼Ş¬İ¼Ş¬İ—V‚ñ‚Å‚¢‚Á‚Ä‚Ë<br>";
	}
	
#	&menu('‚â‚ß‚é','$1½Û¯Ä','$10½Û¯Ä','$100½Û¯Ä','Ê²Û³','ÄŞ¯ÍßÙ','ÌŞ×¯¸¼Ş¬¯¸','Îß°¶°','Ë¯Ä±İÄŞÌŞÛ°','Ê²Û³2');
	&menu('‚â‚ß‚é','$1½Û¯Ä','$10½Û¯Ä','$100½Û¯Ä','$1000½Û¯Ä','Ê²Û³','ÄŞ¯ÍßÙ','ÌŞ×¯¸¼Ş¬¯¸','Îß°¶°','€”õ’†','Ê²Û³2','— ÄŞ¯ÍßÙ','Û²ÔÙÎß°¶°');
}

sub tp_1 {
	return if &is_ng_cmd(1..12);
	
	$m{tp} = $cmd * 100;
	&menu('Play!', '‚â‚ß‚é');
	$m{stock} = 0;
	$m{value} = '';

	if    ($cmd eq '1') { $mes .= '‚±‚±‚Í$1½Û¯Ä‚Å‚·<br>'; }
	elsif ($cmd eq '2') { $mes .= '‚±‚±‚Í$10½Û¯Ä‚Å‚·<br>'; }
	elsif ($cmd eq '3') { $mes .= '‚±‚±‚Í$100½Û¯Ä‚Å‚·<br>'; }
	elsif ($cmd eq '4') { $mes .= '‚±‚±‚Í$1000½Û¯Ä‚Å‚·<br>'; }
	elsif ($cmd eq '5') {
		$mes .= 'Ê²Û³‚Ö‚æ‚¤‚±‚»!<br>';
		$mes .= '‘O‚Ì¶°ÄŞ‚æ‚è‘å‚«‚¢‚©¬‚³‚¢‚©‚ğ“–‚Ä‚é¹Ş°Ñ‚Å‚·<br>';
		$mes .= '“¯‚¶¶°ÄŞ‚Ìê‡‚Í•‰‚¯‚Å‚·‚Ì‚Å’ˆÓ‚µ‚Ä‚­‚¾‚³‚¢‚Ë<br>';
		$mes .= 'ˆê‰ñ10º²İ‚Å‚·<br>';
	}
	elsif ($cmd eq '6') { # ÄŞ¯ÍßÙ
		$mes .= 'ÄŞ¯ÍßÙ‚Ö‚æ‚¤‚±‚»!<br>';
		$mes .= '3–‡‚Ì¶°ÄŞ‚Ì’†‚©‚çAÃŞ¨°×°‚ªˆø‚¢‚½¶°ÄŞ‚Æ“¯‚¶¶°ÄŞ‚ğˆø‚¯‚ÎŸ‚¿‚Å‚·<br>';
		$mes .= 'ˆê‰ñ10º²İ‚Å‚·<br>';
	}
	elsif ($cmd eq '7') { # ÌŞ×¯¸¼Ş¬¯¸
		$mes .= 'ÌŞ×¯¸¼Ş¬¯¸‚Ö‚æ‚¤‚±‚»!<br>';
		$mes .= '21‚ğ’´‚¦‚¸ÃŞ¨°×°‚æ‚è‘å‚«‚¢”‚É‚È‚ê‚ÎŸ‚¿‚Å‚·<br>';
		$mes .= 'ˆê‰ñÅ‘å10000º²İ‚Å‚·<br>';
	}
	elsif ($cmd eq '8') { # Îß°¶°
		$mes .= 'Îß°¶°‚Ö‚æ‚¤‚±‚»!<br>';
	}
#	elsif ($cmd eq '9') { # Ë¯Ä±İÄŞÌŞÛ°
#		$mes .= '¡€”õ’†‚¾‚æ<br>';
#		$mes .= '‚²‚ß‚ñ‚Ë<br>';
#	}
	elsif ($cmd eq '10') { # Ê²Û³2
		$mes .= 'Ê²Û³2‚Ö‚æ‚¤‚±‚»!<br>';
		$mes .= '‘O‚Ì¶°ÄŞ‚æ‚è‘å‚«‚¢‚©¬‚³‚¢‚©‚ğ“–‚Ä‚é¹Ş°Ñ‚Å‚·<br>';
		$mes .= '“¯‚¶¶°ÄŞ‚Í‚Å‚Ü‚¹‚ñ<br>';
		$mes .= 'ˆê‰ñ10º²İ‚Å‚·<br>';
	}
	elsif ($cmd eq '11') { # — ÄŞ¯ÍßÙ
		$mes .= '— ÄŞ¯ÍßÙ‚Ö‚æ‚¤‚±‚»!<br>';
		$mes .= 'ÃŞ¨°×°‚É“¯‚¶¶°ÄŞ‚ğ“–‚Ä‚ç‚ê‚È‚¢‚æ‚¤‚É‚·‚é¹Ş°Ñ‚Å‚·<br>';
		$mes .= 'ˆê‰ñ100º²İ‚Å‚·<br>';
	}
	elsif ($cmd eq '12') { # Îß°¶°
		$mes .= 'Û²ÔÙÎß°¶°‚Ö‚æ‚¤‚±‚»!<br>';
	}
	else {
		&refresh;
		&n_menu;
	}
}


#=================================================
# ½Û¯Ä
#=================================================
sub tp_100 { &_slot(1) }
sub tp_200 { &_slot(10) }
sub tp_300 { &_slot(100) }
sub tp_400 { &_slot(1000) }
sub _slot {
	my $bet = shift;
	
	if ($cmd eq '0') {
		if ($m{coin} >= $bet) {
			my @m = ('‡','ô','õ','š','‚V');
			my @o = (5,10, 15,  20,  30,  50); # µ¯½Ş ˆê”Ô¶‚ÍÁªØ°‚ª2‚Â‚»‚ë‚¢‚Ì‚Æ‚«
			my @s = ();
			$s[$_] = int(rand(@m)) for (0 .. 2);
			$mes .= "[\$$bet½Û¯Ä]<br>";
			$mes .= "<p>y$m[$s[0]]zy$m[$s[1]]zy$m[$s[2]]z</p>";
			$m{coin} -= $bet;
			
			if ($s[0] == $s[1]) { # 1‚Â–Ú‚Æ2‚Â–Ú
				if ($s[1] == $s[2]) { # 2‚Â–Ú‚Æ3‚Â–Ú
					my $v = $bet * $o[$s[0]+1]; # +1 = ÁªØ°2‚»‚ë‚¢
					$m{coin} += $v;
					$mes .= "‚È‚ñ‚Æ!! $m[$s[0]] ‚ª3‚Â‚»‚ë‚¢‚Ü‚µ‚½!!<br>";
					$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!!<br>';
					$mes .= "***** º²İ $v –‡ GET !! *****<br>";
					&c_up('cas_c');
					&use_pet('casino');
					&casino_win_common;
				}
				elsif ($s[0] == 0) { # ÁªØ°‚Ì‚İ1‚Â–Ú‚Æ2‚Â–Ú‚ª‚»‚ë‚¦‚Î‚æ‚¢
					my $v = $bet * $o[0];
					$m{coin} += $v;
					$mes .= 'ÁªØ°‚ª2‚Â‚»‚ë‚¢‚Ü‚µ‚½ô<br>';
					$mes .= "º²İ $v –‡Upô<br>";
					&c_up('cas_c');
					&use_pet('casino');
					&casino_win_common;
				}
				else {
					$mes .= '<p>Ê½ŞÚ</p>';
					$m{act} += 1;
				}
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
# Ê²Û³
#=================================================
sub tp_500 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # ’á‚¢‡
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "y$m[$m{value}]z<br>Ÿ‚Ì¶°ÄŞ‚Í High? or Low?";
			&menu('High!(‚‚¢)','Low!(’á‚¢)');
			
			$m{tp} = 510;
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ‚ª‚ ‚éê‡‚ÍŸ‚¿->‚â‚ß‚é‚Ì‘I‘ğ
		$mes .= "º²İ $m{stock} –‡‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_510 {
	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # ’á‚¢‡
	
	$m{value} = int(rand(@m));
	$mes .= "y$m[$stock_old]z-> y$m[$m{value}]z<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # ‚‚¢‘I‘ğ‚Å‚‚¢
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # ’á‚¢‘I‘ğ‚Å’á‚¢
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
			$mes .= "$m{stock}º²İ Get!<br>";
			$mes .= 'è‚É“ü‚ê‚½º²İ‚ğ‚»‚Ì‚Ü‚ÜŸ‚Ö‚Æ“q‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>';
			&menu('’§í‚·‚é','‚â‚ß‚é');

			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # •‰‚¯
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 6;
	}
	$m{tp} = 500;
}


#=================================================
# ÄŞ¯ÍßÙ
#=================================================
sub tp_600 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('š','Ÿ','£');
			$m{value} = int(rand(@m));
			$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy$m[$m{value}]z<br>";
			$mes .= '<p>y zy zy z</p><p>‚Ç‚Ì¶°ÄŞ‚ğ‘I‚Ñ‚Ü‚·‚©?</p>';
	
			&menu('¶','^‚ñ’†','‰E');
			$m{tp} = 610;
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ‚ª‚ ‚éê‡‚ÍŸ‚¿->‚â‚ß‚é‚Ì‘I‘ğ
		$mes .= "º²İ $m{stock} –‡‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_610 {
	my @m = ('š','Ÿ','£');
	my @s = (0,1,2);
	my $a = int(rand(@m));
	
	$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy$m[$m{value}]z<br>";
	$mes .= "<p>y$m[$s[$a]]zy$m[$s[$a-1]]zy$m[$s[$a-2]]z</p>";
	
	if (   ($cmd eq '0' && $m[$m{value}] eq $m[$s[$a]])       # ¶‘I‘ğ
		|| ($cmd eq '1' && $m[$m{value}] eq $m[$s[$a-1]])     # ^‚ñ’†‘I‘ğ
		|| ($cmd eq '2' && $m[$m{value}] eq $m[$s[$a-2]]) ) { # ‰E‘I‘ğ
		
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 6;
			$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
			$mes .= "º²İ $m{stock} –‡ Get!<br>";
			$mes .= 'è‚É“ü‚ê‚½º²İ‚ğ‚»‚Ì‚Ü‚ÜŸ‚Ö‚Æ“q‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>';
			&menu('’§í‚·‚é','‚â‚ß‚é');
			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # •‰‚¯
		$m{coin} -= 10;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 5;
	}
	$m{tp} = 600;
}

#=================================================
# ÌŞ×¯¸¼Ş¬¯¸@–¢À‘•F²İ¼­×İ½
#=================================================

sub h_to_v {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 14;
		$i++;
	}
	return $v;
}
sub v_to_h {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 14) - 1;
		$v -= $v % 14;
		$v /= 14;
		$i++;
	}
	return @h;
}

sub sph_to_v {
	my $i = 0;
	my $v = 0;
	my $k = 1;
	until ($_[$i] eq ''){
		$v += ($_[$i] + 1) * $k;
		$k *= 25;
		$i++;
	}
	return $v;
}
sub spv_to_h {
	my $v = $_[0];
	my $i = 0;
	my @h = ();
	until ($v <= 0){
		$h[$i] = ($v % 25) - 1;
		$v -= $v % 25;
		$v /= 25;
		$i++;
	}
	return @h;
}
#=================================================
# èDˆ—
#=================================================
sub tp_700 {
	if($cmd eq '0') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		if ($m{coin} > 0){
			$mes .= $m{stock} ? qq|ÍŞ¯Ä<input type="text" name="bet_money" value="$m{stock}" class="text_box1" style="text-align:right">–‡<br>|:
				qq|ÍŞ¯Ä<input type="text" name="bet_money" value="10" class="text_box1" style="text-align:right">–‡<br>|;
		}
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="“q‚¯‚é" class="button1"></p></form>|;
		$m{tp} = 705;
	}
	else{
	&begin;
	}
}

sub tp_705{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @handicap_p = (0,0,0,1,2,3,4,5,6,7,8,9,10,11,12);
	my @handicap_d = (0,1,2,3,3,3,4,4,4,5,5,5,6,7,8,9,10,11,12);
	my $n = 1;
	my @h = ();
	if($in{bet_money} > 0 && $in{bet_money} !~ /[^0-9]/){
		$m{stock} = $in{bet_money} > 10000 ? 10000:$in{bet_money};

		if ($m{coin} >= $m{stock}) {
			$h[0] = $handicap_d[int(rand(@handicap_d))];
			$h[1] = $handicap_p[int(rand(@handicap_p))];
			$h[2] = int(rand(@m));
			$mes .= "º²İ $m{stock} –‡“q‚¯‚Ü‚µ‚½<br>";
			$mes .= "ÃŞ¨°×°‚Ì±¯Ìß¶°ÄŞy$m[$h[0]]z<br>";
			$m{value} = &h_to_v(@h);
			$mes .= "y ";
			until($h[$n] eq ''){
				$mes .= "$m[$h[$n]] ";
				$n++;
			}
			$mes .= "z<br>‚Ç‚¤‚·‚é?";
			$m{tp} = 710;
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			push(@amenus,'Split(•ª‚¯‚é)') if($m{coin} >= $m{stock} * 2 && $h[1] == $h[2]);
			&menu(@amenus);
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

sub tp_710{&draw;}

sub draw{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my $pcount = 0;
	my $ace = 0; #Aˆ—
	my $n = 0; #ÌßÚ²Ô°‚Ì–‡”
	my @h = &v_to_h($m{value});

	$mes .= "ÃŞ¨°×°‚Ì±¯Ìß¶°ÄŞy$m[$h[0]]z<br>";

	if($cmd eq '0') {
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";

		if($pcount > 21){ # ÊŞ°½Ä
			$m{coin} -= $m{stock};
			$m{value} = '';
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
			&menu('Play!','‚â‚ß‚é');
			$m{act} += 6;
			$m{tp} = 700;
		}else {
			$mes .= "‚Ç‚¤‚·‚é?";
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 710;
		}
	}
	elsif($cmd eq '1'){
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";
		$mes .= '<p>‚±‚Ìè‚ÅŸ•‰</p>';
		$m{tp} = 720;
		&n_menu;
	}
	elsif($cmd eq '2'){
		$m{coin} -= $m{stock} / 2;
		$m{act} += 6;
		$m{value} = '';
		$mes .= '<p>~‚è‚Ü‚µ‚½B‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{tp} = 700;
	}
	elsif($cmd eq '3'){
		$m{stock} *= 2;
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";

		$m{tp} = 720;
		if($pcount > 21){ # ÊŞ°½Ä
			$m{coin} -= $m{stock};
			$m{value} = '';
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
			&menu('Play!','‚â‚ß‚é');
			$m{act} += 6;
			$m{tp} = 700;
		}else{
			&n_menu;
		}
	}elsif($cmd eq '4' && @h == 3) {
		$m{stock} *= 2;
		$mes .= "Split‚µ‚Ü‚µ‚½";
		$h[2] = int(rand(@m));
		$mes .= "y$m[$h[1]] $m[$h[2]]z<br>";
		if($h[1] != 0){
			$mes .= "y$m[$h[1]] z<br>";
			$m{value} = &h_to_v(@h);
			$m{tp} = 750;
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
		}else {
			$mes .= "y$m[$h[1]]z<br>";
			$m{value} = &h_to_v(@h);
			$m{tp} = 765;
			&n_menu;
		}
	}else {
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";
		$mes .= "‚Ç‚¤‚·‚é?";
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
		$m{tp} = 710;
	}
}


sub tp_720{
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my $pcount = 0;
	my $dcount = 0;
	my $cards = 1; #ÃŞ¨°×°‚Ì–‡”
	my $bj = 1; #“q‚¯‹à‹y‚ÑÌŞ×¯¸¼Ş¬¯¸ˆ—
	my $ace = 0; #Aˆ—
	my $n = 0; #ÌßÚ²Ô°‚Ì–‡”
	my @h = ();
	my $ran = 0;

	#standÃŞ¨°×°‚ÌèŒˆ’è,Ÿ—˜”»’è
	$ace = 0;
	@h = &v_to_h($m{value});
	$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy$m[$h[0]] ";
	if($h[0] == 0){
		$ace++;
		$dcount += 11;
	}
	elsif ($h[0] > 9){
		$dcount += 10;
	}
	else {
		$dcount += $h[0] + 1;
	}
	until($dcount > 16){ #17ˆÈã‚É‚È‚é‚Ü‚Åˆø‚­
		$ran = int(rand(@m));
		$mes .= "$m[$ran] ";
		if($ran == 0){
			$ace++;
			$dcount += 11;
		}
		elsif ($ran > 9){
			$dcount += 10;
		}
		else {
			$dcount += $ran + 1;
		}
		while($dcount > 21 && $ace > 0) {
			$dcount -= 10;
			$ace--;
		}

		$cards++;
	}
	$mes .= "z<br>";

	$n = 1;
	$ace = 0;
	until($h[$n] eq ''){
		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}
		$n++;
	}
	while($pcount > 21 && $ace > 0) {
		$pcount -= 10;
		$ace--;
	}

	$bj += 2 if $pcount == 21 && $n == 3;
	$bj += 3 if $dcount == 21 && $cards == 2;

	if($bj == 1){ #‚Ç‚¿‚ç‚àÌŞ×¯¸¼Ş¬¯¸‚Å‚È‚¢‚Æ‚«
		$mes .= "ÌßÚ²Ô°y$pcountz ÃŞ¨°×°y$dcountz<br>";
	}
	elsif($bj == 3){ #ÌßÚ²Ô°‚Ì‚İÌŞ×¯¸¼Ş¬¯¸‚Ì
		$mes .= "ÌßÚ²Ô°yBlackjackz<br>";
	}
	elsif($bj == 4){ #ÃŞ¨°×°‚ªÌŞ×¯¸¼Ş¬¯¸‚Ì
		$mes .= "ÃŞ¨°×°yBlackjackz<br>";
	}
	else { #‚Ç‚¿‚ç‚àÌŞ×¯¸¼Ş¬¯¸‚Ì
		$mes .= "ÌßÚ²Ô°yBlackjackz ÃŞ¨°×°yBlackjackz<br>";
	}


	if ($dcount > 21 || $bj == 3 || $pcount > $dcount){ #Ÿ‚¿
		$m{stock} *= $bj;
		$m{value} = '';
		$m{coin} += $m{stock};
		$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
		$mes .= "$m{stock}º²İ Get!<br>";
		$mes .= '<p>‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('’§í‚·‚é','‚â‚ß‚é');
		&c_up('cas_c');
		&use_pet('casino');
		&casino_win_common;
	}
	elsif(($pcount == $dcount && $bj != 4)) {
		$m{value} = '';
		$mes .= '<p>‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
	}
	else { # •‰‚¯
		$m{coin} -= $m{stock};
		$m{value} = '';
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 4;
	}
	$m{tp} = 700;
}

sub tp_750{&split;}#Splitê—p•ªŠò

sub split {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my $pcount = 0;
	my $ace = 0; #Aˆ—
	my $n = 0; #ÌßÚ²Ô°‚Ì–‡”
	my @h = &v_to_h($m{value});

	$mes .= "ÃŞ¨°×°‚Ì±¯Ìß¶°ÄŞy$m[$h[0]]z<br>";

	if($cmd eq '0') {
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z<br>";

		if($pcount > 21){ # ÊŞ°½Ä
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B</p>';
			@h = ($h[0],23,$h[1],int(rand(@m)));
			$mes .= "y$m[$h[2]] $m[$h[3]]z<br>";
			$m{value} = &sph_to_v(@h);
			$m{tp} = 760;
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
		}else {
			$mes .= "y$m[$h[1]] z<br>";
			$mes .= "‚Ç‚¤‚·‚é?";
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 750;
		}
	}
	elsif($cmd eq '1'){
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z<br>";
		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$pcount++ if $n == 3 && $pcount == 21;
		$mes .= '<p>second hand</p>';
		@h = ($h[0],$pcount,$h[1],int(rand(@m)));
		$mes .= "y$m[$h[2]] $m[$h[3]]z<br>";
		$m{value} = &sph_to_v(@h);
		$m{tp} = 760;
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	}
	elsif($cmd eq '2'){
		$mes .= '<p>~‚è‚Ü‚µ‚½B</p>';
		@h = ($h[0],0,$h[1],int(rand(@m)));
		$mes .= "y$m[$h[2]] $m[$h[3]]z<br>";
		$m{value} = &sph_to_v(@h);
		$m{act} += 6;
		$m{tp} = 760;
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	}
	elsif($cmd eq '3'){
		$n = 1;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ
		$m{value} = &h_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";

		if($pcount > 21){ # ÊŞ°½Ä
			$pcount = 23;
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B</p>';
		}
		@h = ($h[0],$pcount,0,$h[1],int(rand(@m)));
		$mes .= "y$m[$h[3]] $m[$h[4]]z<br>";
		$m{value} = &sph_to_v(@h);
		$m{tp} = 760;
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
	}else {
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";
		$mes .= "‚Ç‚¤‚·‚é?";
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
		$m{tp} = 750;
	}
}

sub tp_760 {&split_2;}

sub split_2 {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my $pcount = 0;
	my $ace = 0; #Aˆ—
	my $n = 0; #ÌßÚ²Ô°‚Ì–‡”
	my $nsub;
	my @h = &spv_to_h($m{value});

	$mes .= "ÃŞ¨°×°‚Ì±¯Ìß¶°ÄŞy$m[$h[0]]z<br>";

	if($cmd eq '0') {
		$n = 2;
		$n++ if $h[$n] == 0;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ
		$m{value} = &sph_to_v(@h);

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 2;
		$n++ if $h[$n] == 0;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";
		if($pcount > 21){ # ÊŞ°½Ä
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B</p>';
			@h = $h[2] == 0 ? ($h[0],$h[1],0,23):($h[0],$h[1],23);
			$m{value} = &sph_to_v(@h);
			$m{tp} = 770;
			&n_menu;
		}else {
			$mes .= "‚Ç‚¤‚·‚é?";
			my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
			push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
			&menu(@amenus);
			$m{tp} = 760;
		}
	}
	elsif($cmd eq '1'){
		$n = 2;
		$n++ if $h[$n] == 0;
		$nsub = $n;
		$mes .= "y";
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z<br>";
		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$pcount++ if $n - $nsub == 2 && $pcount == 21;
		@h = $h[2] == 0 ? ($h[0],$h[1],0,$pcount):($h[0],$h[1],$pcount);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	}
	elsif($cmd eq '2'){
		$mes .= '<p>~‚è‚Ü‚µ‚½B</p>';
		@h = $h[2] == 0 ? ($h[0],$h[1],0,0):($h[0],$h[1],0);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	}
	elsif($cmd eq '3'){
		$n = 2;
		$n++ if $h[$n] == 0;
		until($h[$n] eq ''){
			if($h[$n] == 0){
				$ace++;
				$pcount += 11;
			}
			elsif ($h[$n] > 9){
				$pcount += 10;
			}
			else {
				$pcount += $h[$n] + 1;
			}
			$n++;
		}
		$h[$n] = int(rand(@m)); #V‚µ‚­ˆø‚¢‚½¶°ÄŞ

		if($h[$n] == 0){
			$ace++;
			$pcount += 11;
		}
		elsif ($h[$n] > 9){
			$pcount += 10;
		}
		else {
			$pcount += $h[$n] + 1;
		}

		while($pcount > 21 && $ace > 0) {
			$pcount -= 10;
			$ace--;
		}
		$n = 2;
		$n++ if $h[$n] == 0;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";

		if($pcount > 21){ # ÊŞ°½Ä
			$mes .= '<p>ÊŞ°½Ä‚Å‚·B</p>';
			$pcount = 23;
		}

		@h = $h[2] == 0 ? ($h[0],$h[1],0,$pcount,0):($h[0],$h[1],$pcount,0);
		$m{value} = &sph_to_v(@h);
		$m{tp} = 770;
		&n_menu();
	}else {
		$n = 1;
		$mes .= "y";
		until($h[$n] eq ''){
			$mes .= "$m[$h[$n]] ";
			$n++;
		}
		$mes .= "z";
		$mes .= "‚Ç‚¤‚·‚é?";
		my @amenus = ('hit(‚à‚¤ˆê–‡)!','stand(Ÿ•‰)!','Surrender(~‚è‚é)');
		push(@amenus,'Double down(ÅŒã‚Ìˆê–‡)') if($m{coin} >= $m{stock} * 2);
		&menu(@amenus);
		$m{tp} = 760;
	}
}

sub tp_765 {#Ace Splitê—p
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @h = &v_to_h($m{value});

	if($h[2] > 8){
		$h[1] = 22;
	}else {
		$h[1] = 12 + $h[2];
	}

	@h = ($h[0],$h[1],0,int(rand(@m)));
	$mes .= "ÃŞ¨°×°‚Ì±¯Ìß¶°ÄŞy$m[$h[0]]z<br>";
	$mes .= "y$m[$h[2]] $m[$h[3]]z<br>";
	if($h[3] > 8){
		$h[2] = 22;
	}else {
		$h[2] = 12 + $h[3];
	}
	@h = ($h[0],$h[1],$h[2]);
	$m{value} = &sph_to_v(@h);
	$m{tp} = 770;
	&n_menu();
}

sub tp_770 {
	my @m = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my $pcount = 0;
	my $dcount = 0;
	my $cards = 1; #ÃŞ¨°×°‚Ì–‡”
	my $bj = 1; #“q‚¯‹à‹y‚ÑÌŞ×¯¸¼Ş¬¯¸ˆ—
	my $ace = 0; #Aˆ—
	my $n; #ÌßÚ²Ô°‚Ì–‡”
	my $nsub;
	my @h = ();
	my $ran = 0;
	my $is_dd = 0;
	my $is_dd2 = 0;
	my $pwin = 0;
	my $get_coin = 0;

	#standÃŞ¨°×°‚ÌèŒˆ’è,Ÿ—˜”»’è
	$ace = 0;
	@h = &spv_to_h($m{value});
	$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy$m[$h[0]] ";
	if($h[0] == 0){
		$ace++;
		$dcount += 11;
	}
	elsif ($h[0] > 9){
		$dcount += 10;
	}
	else {
		$dcount += $h[0] + 1;
	}
	until($dcount > 16){ #17ˆÈã‚É‚È‚é‚Ü‚Åˆø‚­
		$ran = int(rand(@m));
		$mes .= "$m[$ran] ";
		if($ran == 0){
			$ace++;
			$dcount += 11;
		}
		elsif ($ran > 9){
			$dcount += 10;
		}
		else {
			$dcount += $ran + 1;
		}
		while($dcount > 21 && $ace > 0) {
			$dcount -= 10;
			$ace--;
		}

		$cards++;
	}
	$mes .= "z<br>";
	$dcount = 23 if $dcount > 21;
	$h[0] = $dcount;

	$h[0]++ if $h[0] == 21 && $cards == 2;

	$mes .= "ÃŞ¨°×°y";
	$mes .= $h[0] > 22 ? "ÊŞ°½Ä":
	$h[0] == 22 ? "Blackjack":
	$h[0];
	$mes .= "z<br>";
	$mes .= "ÌßÚ²Ô°y";
	$mes .= $h[1] > 22 ? "ÊŞ°½Ä":
	$h[1] == 22 ? "Blackjack":
	$h[1] == 0 ? "Surrender":
	$h[1];
	$mes .= "z<br>";
	$is_dd++ if($h[2] == 0 && $h[3] ne '');
	$is_dd2++ if(($h[3] ne '' && $h[3] == 0 && $is_dd == 0)||($h[4] == 0 && $is_dd == 1));
	my $second_hand = $is_dd == 1 ? $h[3]:$h[2];
	$mes .= "ÌßÚ²Ô°y";
	$mes .= $second_hand > 22 ? "ÊŞ°½Ä":
	$second_hand == 22 ? "Blackjack":
	$second_hand == 0 ? "Surrender":
	$second_hand;
	$mes .= "z<br>";

	$get_coin = $m{coin};

	if($h[0] == 22) {
		if($h[1] == 22){
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
			if ($h[1] == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
		if($second_hand == 22){
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
			if ($second_hand == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
	}
	else {
		if ($h[1] == 23){
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
		}
		elsif ($h[1] > 0 && ($h[0] > 22 || $h[1] == 22 || $h[0] < $h[1])){ #Ÿ‚¿
			$m{coin} += $m{stock} / 2;
			$m{coin} += $m{stock} / 2 if $is_dd == 1;
			$m{coin} += $m{stock} if $h[1] == 22;
			$pwin++;
		}
		elsif($h[0] == $h[1]) {
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd == 1;
			if ($h[1] == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
		if ($second_hand > 22){
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
		}
		elsif ($second_hand > 0 && ($h[0] > 22 || $second_hand == 22 || $h[0] < $second_hand)){ #Ÿ‚¿
			$m{coin} += $m{stock} / 2;
			$m{coin} += $m{stock} / 2 if $is_dd2 == 1;
			$m{coin} += $m{stock} if $second_hand == 22;
			$pwin++;
		}
		elsif($h[0] == $second_hand) {
			$pwin++;
		}
		else {
			$m{coin} -= $m{stock} / 2;
			$m{coin} -= $m{stock} / 2 if $is_dd2 == 1;
			if ($second_hand == 0){
				$m{coin} += $m{stock} / 4;
				$pwin++;
			}
		}
	}
	$get_coin = $m{coin} - $get_coin;
	if ($pwin > 0 && $get_coin >= 0){ #Ÿ‚¿
		$m{value} = '';
		$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
		$mes .= "$get_coinº²İ Get!<br>";
		$mes .= '<p>‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('’§í‚·‚é','‚â‚ß‚é');
		&c_up('cas_c') for (1..$pwin);
		&use_pet('casino') for (1..$pwin);
		&casino_win_common;
	}
	else { # •‰‚¯
		$m{value} = '';
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 6;
	}
	$m{tp} = 700;
}

#=================================================
# Jacks or Better
#=================================================
sub h_to_vj {
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
sub v_to_hj {
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

#=================================================
# èDˆ—
#=================================================
sub tp_800 {
	if ($cmd eq '0'){
		$mes .= "‚Ç‚Ì‘ä‚ÅƒvƒŒƒC‚µ‚Ü‚·‚©H<br>";
		&menu("‚â‚ß‚é","1ƒvƒŒƒC10º²İ","1ƒvƒŒƒC100º²İ","1ƒvƒŒƒC1000º²İ");
		$m{tp} += 10;
	}
	else {
		&begin;
	}
}

sub tp_810 {
	my @bet_money = (10,100,1000);
	if($cmd eq '1' || $cmd eq '2' || $cmd eq '3'){
		$mes .= "1ƒvƒŒƒC$bet_money[$cmd-1]º²İ‚Ì‘ä‚Å—V‚Ñ‚Ü‚·<br>";
		$m{tp} += $cmd;
		&menu("Go","‚â‚ß‚é");
	}else {
		&begin;
	}
}

sub tp_811 {&deal_first(10);}

sub tp_821{&change_card();}

sub tp_831{&deal_second(10);}

sub tp_812 {&deal_first(100);}

sub tp_822{&change_card();}

sub tp_832{&deal_second(100);}

sub tp_813 {&deal_first(1000);}

sub tp_823{&change_card();}

sub tp_833{&deal_second(1000);}

sub deal_first{
	my $need_money = shift;
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = ();

	if ($cmd eq '0') {
		if ($m{coin} >= $need_money) {
			my $ran = $m{cas_c} > 50000 ? 1000:6000 - ($m{cas_c} / 10);
			$m{stock} = int(rand($ran));
			@h = &draw_new(@h);

			$m{value} = &h_to_vj(@h);
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

			$m{tp} += 10;
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

sub draw_new{
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

sub change_card{
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @sub_h = &v_to_hj($m{value});
	my @h = ();
	my $i;

	for my $j (0..4){
		next if $in{"change_$j"};
		push @h, $sub_h[$j];
	}
	$m{value} = &h_to_vj(@h);

	$i = 0;
	$mes .= "y ";
	until($h[$i] eq '') {
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
		$i++;
	}
	$mes .= "z<br>";
	$m{tp} += 10;
	&n_menu;
}

sub deal_second{
	my $need_money = shift;
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
	my @h = &v_to_hj($m{value});

	@h = &draw_new(@h);
	$mes .= "y ";
	for my $i (0..4){
		$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
	}
	$mes .= "z<br>";
	$m{value} = &h_to_vj(@h);

	&check_hand();

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
		$mes .= "Jack or Better<br>";
	}else{
		$mes .= "No pair<br>";
	}

	if ($m{stock} > 0) { 
		$m{stock} *= $need_money;
		$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
		$mes .= "º²İ $m{stock} –‡ Get!<br>";
		$m{coin} += $m{stock};
		$m{stock} = $m{value} = 0;
		&menu('play','‚â‚ß‚é');
		&c_up('cas_c');
		&use_pet('casino');
		&casino_win_common;
	}
	else { # •‰‚¯
		$m{coin} -= $need_money;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 5;
	}
	$m{tp} -= 20;
}

sub check_hand{
	my @h = &v_to_hj($m{value});
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
	}elsif($pair_num == 1 && ($pair_high > 9 || $pair_high == 0)){
		$m{stock} = 1;
	}else{
		$m{stock} = 0;
	}
}

#=================================================
# hit and blow(”p~)
#=================================================
sub tp_900 {
	&begin;
}

#=================================================
# Ê²Û³2
#=================================================
sub tp_1000 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # ’á‚¢‡
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "y$m[$m{value}]z<br>Ÿ‚Ì¶°ÄŞ‚Í High? or Low?";
			&menu('High!(‚‚¢)','Low!(’á‚¢)');
			
			$m{tp} = 1010;
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ‚ª‚ ‚éê‡‚ÍŸ‚¿->‚â‚ß‚é‚Ì‘I‘ğ
		$mes .= "º²İ $m{stock} –‡‚ğè‚É“ü‚ê‚Ü‚µ‚½!<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_1010 {
	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # ’á‚¢‡
	my @n;
	push @n, int(rand($#m - $stock_old)) + $stock_old+1 unless $stock_old == $#m;
	push @n, int(rand($stock_old)) unless $stock_old == 0;
	
	$m{value} = $n[int(rand(@n))];
	$mes .= "y$m[$stock_old]z-> y$m[$m{value}]z<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # ‚‚¢‘I‘ğ‚Å‚‚¢
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # ’á‚¢‘I‘ğ‚Å’á‚¢
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
			$mes .= "$m{stock}º²İ Get!<br>";
			$mes .= 'è‚É“ü‚ê‚½º²İ‚ğ‚»‚Ì‚Ü‚ÜŸ‚Ö‚Æ“q‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>';
			&menu('’§í‚·‚é','‚â‚ß‚é');

			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # •‰‚¯
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 6;
	}
	$m{tp} = 1000;
}

#=================================================
# — ÄŞ¯ÍßÙ
#=================================================
sub tp_1100 {
	if ($cmd eq '0') {
		if ($m{coin} >= 100) {
			my @m = ('š','Ÿ','£','œ');
			$m{value} = int(rand(@m));
			$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy z<br>";
			$mes .= '<p>yšzyŸzy£zyœz</p><p>‚Ç‚Ì¶°ÄŞ‚ğ‘I‚Ñ‚Ü‚·‚©?</p>';
	
			&menu('š','Ÿ','£','œ');
			$m{tp} = 1110;
		}
		else {
			$mes .= 'º²İ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ‚ª‚ ‚éê‡‚ÍŸ‚¿->‚â‚ß‚é‚Ì‘I‘ğ
		$mes .= "º²İ $m{stock} –‡‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
		$m{coin} += $m{stock};
		&casino_win_common;
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_1110 {
	my @m = ('š','Ÿ','£','œ');
	my $a = int(rand(@m));
	
	$mes .= "ÃŞ¨°×°‚Ì¶°ÄŞy$m[$a]z<br>";
	$mes .= "‹M•û‚Ì¶°ÄŞy$m[$cmd]z</p>";
	
	if ($cmd != $a) {
		$m{stock} = 100 if $m{stock} == 0;
		$m{stock} = int(1.5 * $m{stock});
		$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
		$mes .= "º²İ $m{stock} –‡ Get!<br>";
		$mes .= 'è‚É“ü‚ê‚½º²İ‚ğ‚»‚Ì‚Ü‚ÜŸ‚Ö‚Æ“q‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>';
		&menu('’§í‚·‚é','‚â‚ß‚é');
		&c_up('cas_c');
		&use_pet('casino');
	}
	else { # •‰‚¯
		$m{coin} -= 100;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 7;
	}
	$m{tp} = 1100;
}

#=================================================
# Û²ÔÙÎß°¶°
#=================================================
sub tp_1200 {
	if($cmd eq '0') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		if ($m{coin} > 0){
			$mes .= $m{stock} ? qq|ÍŞ¯Ä<input type="text" name="bet_money" value="$m{stock}" class="text_box1" style="text-align:right">–‡<br>|:
				qq|ÍŞ¯Ä<input type="text" name="bet_money" value="10" class="text_box1" style="text-align:right">–‡<br>|;
		}
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="“q‚¯‚é" class="button1"></p></form>|;
		$m{tp} += 10;
	}
	else{
		&begin;
	}
}

sub tp_1210 {
	if($in{bet_money} > 0 && $in{bet_money} !~ /[^0-9]/){
		$m{stock} = $in{bet_money} > 500 ? 500:$in{bet_money};
		if ($m{coin} >= $m{stock}) {
			my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
			my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
			my @h = ();
			@h = &draw_r_card(@h);
			@h = &draw_r_card(@h);
			$m{value} = &h_to_vj(@h);
			$mes .= "y ";
			for my $i (0..1){
				$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
			}
			$mes .= "z<br>";
			$mes .= "Ÿ‚Ì¶°ÄŞ‚ğˆø‚­H	<br>";
			$m{tp} += 10;
			&menu('draw','double up','‚â‚ß‚é');
		}
	}
	else {
		&begin;
	}
}

sub tp_1220 {
	if($cmd eq '2'){
		$m{coin} -= $m{stock};
		$m{stock} = $m{value} = 0;
		$mes .= '<p>‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
		&menu('Play!','‚â‚ß‚é');
		$m{act} += 1;
		$m{tp} -= 20;
	
	}else{
		if($cmd eq '1' && $m{coin} > $m{stock}*2){
			$m{stock} *= 2;
		}
		my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # ’á‚¢‡
		my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9826','&#9827','&#9825');
		my @h = &v_to_hj($m{value});
		@h = &draw_r_card(@h);
		$m{value} = &h_to_vj(@h);
		$mes .= "y ";
		for my $i (0..$#h){
			$mes .= "$suit[$h[$i] / 13] $num[$h[$i] % 13]  ";
		}
		$mes .= "z<br>";
		if(@h < 5){
			$mes .= "Ÿ‚Ì¶°ÄŞ‚ğˆø‚­H	<br>";
			&menu('draw','double up','‚â‚ß‚é');	
		}else {
			my $bet = $m{stock};
			my $base = $m{stock};
			&check_hand();
			
			if($m{stock} == 1000){
				$mes .= "Royal Straight Flash<br>";
				$bet *= 100;
			}elsif($m{stock} == 200){
				$mes .= "Straight Flash<br>";
				$bet *= 0;
			}elsif($m{stock} == 25){
				$mes .= "Four of a kind<br>";
				$bet *= 50;
			}elsif($m{stock} == 10){
				$mes .= "Full House<br>";
				$bet *= 10;
			}elsif($m{stock} == 7){
				$mes .= "Flash<br>";
				$bet *= 0;
			}elsif($m{stock} == 5){
				$mes .= "Straight<br>";
				$bet *= 5;
			}elsif($m{stock} == 4){
				$mes .= "Three of a kind<br>";
				$bet *= 1;
				$bet = int($bet);
			}elsif($m{stock} == 3){
				$mes .= "Two pair<br>";
				$bet *= 0;
			}elsif($m{stock} == 1){
				$mes .= "One pair<br>";
				$bet *= -1;
			}else{
				$mes .= "One pair<br>";
				$bet *= -1;
			}
			
			if ($bet >= 0) { 
				$mes .= '‚¨‚ß‚Å‚Æ‚¤‚²‚´‚¢‚Ü‚·!<br>';
				$mes .= "º²İ $bet –‡ Get!<br>";
				$m{coin} += $bet;
				$m{value} = 0;
				$m{stock} = $base;
				&menu('play','‚â‚ß‚é');
				&c_up('cas_c');
				&use_pet('casino');
				&casino_win_common;
			}
			else { # •‰‚¯
				$m{coin} += $bet;
				$m{value} = 0;
				$m{stock} = $base;
				$mes .= '<p>c”O‚Å‚µ‚½‚ËB‚à‚¤ˆê“x‚â‚è‚Ü‚·‚©?</p>';
				&menu('Play!','‚â‚ß‚é');
				$m{act} += 8;
			}
			$m{tp} -= 20;
		}
	}
}

sub draw_r_card{
	my @r_cards = (0, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 35, 36, 37, 38, 39, 48, 49, 50, 51);
	my $c;
	my $j;
	my @h;
	$j = 0;
	until($_[$j] eq ''){
		$h[$j] = $_[$j];
		$j++;
	}
	while(1){
		$c = $r_cards[int(rand(@r_cards))];
		my $go = 1;
		for $i(0..$j-1){
			$go = 0 if $h[$i] == $c;
		}
		last if $go == 1;
	}
	$h[$j] = $c;

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


sub casino_win_common {
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('casino');
	}
}
1; # íœ•s‰Â
