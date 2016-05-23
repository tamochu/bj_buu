my $this_file = "$logdir/colosseum/champ_$m{stock}.cgi";
#================================================
# “¬‹Zê Created by Merino
#=================================================
# $m{stock} ‚ªØ°¸Ş $m{value} ‚ª ×³İÄŞ”

# ‚±‚Ì‰ñ”ˆÈã–h‰q‚·‚é‚Æ©“®ˆø‘Ş
my $limit_defence_c = 50;

# Î”è‚É‹L˜^
my $legend_defence_c = 25;

# ×³İÄŞÀ²ÄÙ
my @round_titles = ('‰í','€ŒˆŸ','ŒˆŸí');

# i‰ïÒ‚Ì¾ØÌ(1+2‚Ì‘g‚İ‡‚í‚¹)
my @coms_1 = ('‚È‚©‚È‚©‚Ì','‘å‹t“]‚Ì','½Ëß°ÃŞ¨°‚È','‘f°‚ç‚µ‚¢','Œ©‚²‚½‚¦‚Ì‚ ‚é','‹S‹C”—‚é','·ŞØ·ŞØ‚Ì','ˆê•û“I‚È','Œ©–‚È','Œ|p“I‚È','¸Ú²¼Ş°‚È','‘å”——Í‚Ì','‚æ‚­‚í‚©‚ç‚È‚¢');
my @coms_2 = ('‡','Ÿ•‰','í‚¢','UŒ‚','U–h','‹­‚³','‹Z','‹C”—','ÍÀÚ','“®‚«','ˆêŒ‚');

# Ø°¸Ş(’Ç‰Á‚µ‚½ê‡w./log/colosseum/x‚Éwchamp_?.cgixÌ§²Ù‚ğ’Ç‰Á‚·‚é‚±‚Æ)
my @menus = (
#	[0]–¼‘O,[1]‹­‚³§ŒÀ,[2]–h‰q‹à,[3]oê‹à,[4]Íß¯Ä§ŒÀ
	['ËßÖËßÖØ°¸Ş',	800,	1000,	1000, 1],
	['ËŞ·ŞÅ°Ø°¸Ş',	1500,	1000,	1000, 1],
	['ÍŞÃ×İØ°¸Ş',	3000,	2000,	2000, 1],
	['Ï¼Ş¼¬İØ°¸Ş',	0,		2000,	2000, 1],
	['¿Ù¼Ş¬°Ø°¸Ş',	0,		2000,	2000, 1],
	['Á¬İËßµİØ°¸Ş',	0,		3000,	3000, 1],
	['µÃŞİØ°¸Ş',	0,		3000,	3000, 0],
);

my %plus_needs = (
	'Ï¼Ş¼¬İØ°¸Ş'	=> ['•Ší‚Ì‘•”õ‘®«‚ªw•—A—‹A‰Šx‚Ì‚İ',		sub{ $weas[$m{wea}][2] =~ /•—|—‹|‰Š/ }],
	'¿Ù¼Ş¬°Ø°¸Ş'	=> ['•Ší‚Ì‘•”õ‘®«‚ªwŒ•A‘„A•€x‚Ì‚İ',		sub{ $weas[$m{wea}][2] =~ /Œ•|‘„|•€/ }],
);

#================================================
# —˜—pğŒ
#================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "“¬‹Zê‚ÉQ‰Á‚·‚é‚Ì‚É$e2j{hp}‚ª­‚È‚·‚¬‚Ü‚·<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ”æ˜J‚µ‚Ä‚¢‚éê‡‚Ís‚¦‚È‚¢
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	$m{tp} = 1 if $m{tp} > 1;
	$m{turn} = 0;
	my $m_st = &m_st;
	$mes .= "$m{name}‚Ì‹­‚³[ $m_st ]<br>";
	$mes .= "‚±‚±‚Í‹­Ò‚ªW‚Ü‚é“¬‹Zê‚Å‚·<br>Oí˜A‘±‚ÅŸ‚¿i‚Ş‚ÆÁ¬İËßµİ‚É‚È‚èÜ‹à‚ªo‚Ü‚·<br>";
	$mes .= "Á¬İËßµİ‚É‚È‚èA–h‰q‚·‚é‚±‚Æ‚Å‚à‚Ü‚½Ü‹à‚ª‚à‚ç‚¦‚Ü‚·<br>";
	$mes .= "<hr>‚Ç‚ÌØ°¸Ş‚É’§í‚µ‚Ü‚·‚©?<br>";
	for my $i (0 .. $#menus) {
		$mes .= $menus[$i][1] ? "$menus[$i][0]F‹­‚³$menus[$i][1]‚Ü‚Å<br>"
			  : "$menus[$i][0]F‹­‚³–³§ŒÀ<br>";
	}
	
	&menu('‚â‚ß‚é',map{ $_->[0] } @menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	
	--$cmd;
	$m{tp} = 100;
	$m{stock} = $cmd;
	$mes .= "$menus[$m{stock}][0] ‚Éoê‚·‚é‚É‚ÍA$menus[$m{stock}][3] G‚©‚©‚è‚Ü‚·<br>";
	$mes .= "’§í‚µ‚Ü‚·‚©?<br>";
	
	&champ_statuses($m{stock});
	
	&menu('‚â‚ß‚é','’§í‚·‚é');
}


#================================================
# oê¾¯Ä
#================================================
sub tp_100 {
	if ($cmd eq '1') {
		if ($menus[$m{stock}][1] <= 0 || &m_st <= $menus[$m{stock}][1]) {
			if (&is_champ) {
				$mes.="$m{name}‘Iè‚Í–h‰qÒ‚Å‚·‚Ì‚Å’§í‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
				&begin;
			}
			elsif ($m{money} >= $menus[$m{stock}][3]) {
				if (!defined $plus_needs{$menus[$m{stock}][0]} || &{ $plus_needs{$menus[$m{stock}][0]}[1] }) {
					$m{money} -= $menus[$m{stock}][3];
					$m{tp} = 110;
					$m{value} = 0;
					$mes .= "$menus[$m{stock}][0] ‚Éoê‚µ‚Ü‚·!<br>";
					&n_menu;
				}
				else {
					$mes .= "$menus[$m{stock}][0]‚Éoê‚Å‚«‚éğŒ‚Í $plus_needs{$menus[$m{stock}][0]}[0] ‚Å‚·<br>";
					&begin;
				}
			}
			else {
				$mes .= '‚¨‹à‚ª‘«‚è‚Ü‚¹‚ñ<br>';
				&begin;
			}
		}
		else {
			$mes .= "$menus[$m{stock}][0]‚Éoê‚Å‚«‚é‚Ì‚Í‹­‚³‚ª$menus[$m{stock}][1]ˆÈ‰º‚Ì‘Iè‚¾‚¯‚Å‚·<br>";
			&begin;
		}
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		&begin;
	}
}


#================================================
# —DŸ or ‡ŠJn‚Ì±Å³İ½
#================================================
sub tp_110 {
	open my $fh, "< $this_file" or &error("$this_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my @lines = <$fh>;
	close $fh;
	
	# –h‰qÒ”‚É‚æ‚è×³İÄŞ”’²®
	if ($m{value} <= 0) {
		$m{value} = @lines == 0 ? 3 # –h‰qÒ‚ª‚¢‚È‚¢‚Ì‚Å‚¢‚«‚È‚è—DŸ
				  : @lines == 1 ? 2 # ŒˆŸ‚©‚ç
				  : @lines == 2 ? 1 # €ŒˆŸ‚©‚ç
				  :               0 # ‰í‚©‚ç
				  ;
	}
	my $battles = @lines > 2 ? 0:@lines - 3;
	
	if ($m{value} > 2) { # —DŸ
		&c_up('col_c') for (1..$m{value});

		--$m{value};
		
		# –h‰qÒ‘‚«Š·‚¦ˆ—
		&_rewrite_champ;
		
		my $v = $menus[$m{stock}][2] * 10;
		$m{money} += $v;
		$mes.="$menus[$m{stock}][0]‚ÉV‚½‚È—DŸÒ‚ª’a¶‚µ‚Ü‚µ‚½!<br>";
		$mes.="$m{name}‘Iè‚Å‚·!$m{name}u$m{mes_win}v<br>";
		$mes.="Ü‹à‚Ì $v G‚ª‘—‚ç‚ê‚Ü‚·!<br>";
		$mes.="‚»‚ê‚Å‚ÍÄ‚Ñ$m{name}‘Iè‚É”è‚ğ!<br>";
		if ($menus[$m{stock}][4]) {
			$m{egg_c} += int(rand(20)+30) if $m{egg};
		} else {
			$m{egg_c} += int(rand(10)+5) if $m{egg};
		}
		$m{act} += 10;
		&write_colosseum_news(qq| <i>$menus[$m{stock}][0] VÁ¬İËßµİ <font color="$cs{color}[$m{country}]">$m{name}</font> ’a¶</i>|, 1);
		&send_twitter("$menus[$m{stock}][0] VÁ¬İËßµİ $m{name} ’a¶");
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('colosseum_top');
		}
		
		&refresh;
		&n_menu;
	}
	else {
		# ‘ŠèÃŞ°Àæ“¾
		($y{name},$y{country},$y{max_hp},$y{max_mp},$y{at},$y{df},$y{mat},$y{mdf},$y{ag},$y{cha},$y{wea},$y{skills},$y{mes_win},$y{mes_lose},$y{icon},$y{defence_c},$y{wea_name},$y{gua}) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $lines[$battles + $m{value}];
		$y{hp}  = $y{max_hp};
		$y{mp}  = $y{max_mp};
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
		
		$mes .= $coms_1[int(rand(@coms_1))].$coms_2[int(rand(@coms_2))]."‚Å‚µ‚½‚Ë!‚»‚ê‚Å‚Íˆø‚«‘±‚«<br>" if $m{value} > 0;
		$mes .= "$menus[$m{stock}][0] $round_titles[$m{value}]<br>";
		$mes .= "$m{name} VS $y{name}<br>";
		$mes .= "‡n‚ß!<br>";
		&n_menu;
		$m{tp} = 120;
	}
}

#================================================
# í“¬ˆ—
#================================================
sub tp_120 {
	if($menus[$m{stock}][4]) {
		require './lib/colosseum_battle.cgi';
	} else {
		require './lib/battle.cgi';
	}

	if ($m{hp} <= 0) {
		&col_lose;
	}
	elsif ($y{hp} <= 0) {
		&col_win;
	}
}

#================================================
# •‰‚¯
#================================================
sub col_lose {
	$m{act} += $m{value} * 5 + 5;
	$mes .= 'c”O‚Å‚µ‚½B‚Ü‚½’§í‚µ‚É—ˆ‚Ä‚¾‚³‚¢<br>';
	&_defence_c_up;
	&refresh;
	&n_menu;
}
#================================================
# Ÿ‚¿
#================================================
sub col_win {
	my $v = int( rand(10)+ 5 );
	$v = &use_pet('colosseum', $v);
	$m{exp} += $v;
	$m{egg_c} += int(rand(2)+1) if $m{egg};

	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] › ’§íÒ<font color="$cs{color}[$m{country}]">$m{name}</font> VS –h‰qÒ<font color="$cs{color}[$y{country}]">$y{name}</font> ~|);
	&send_twitter("$menus[$m{stock}][0]$round_titles[$m{value}] › ’§íÒ$m{name} VS –h‰qÒ$y{name} ~");
	
	$m{tp} = 110;
	++$m{value}; # ×³İÄŞ¶³İÄ±¯Ìß

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('colosseum');
	}

	&n_menu;
}

#================================================
# –h‰q”¶³İÄ±¯Ìß
#================================================
sub _defence_c_up {
	my $count = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my @temp_lines = <$fh>;
	my $count_sub = @temp_lines;
	while (my $line = shift @temp_lines) {
		if ($count == $count_sub - 3 + $m{value}) {
			my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $line;
			++$defence_c;
			
			&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] ~ ’§íÒ<font color="$cs{color}[$m{country}]">$m{name}</font> VS –h‰qÒ<font color="$cs{color}[$y{country}]">$y{name}</font> › –h‰q$defence_c|);
			&send_twitter("$menus[$m{stock}][0]$round_titles[$m{value}] ~ ’§íÒ$m{name} VS –h‰qÒ$y{name} › –h‰q$defence_c");

			# ‹K’è”ˆÈã‚¾‚Æ©“®ˆø‘Ş•Î”è
			if ($defence_c >= $limit_defence_c) {
				&_send_money_and_col_c_up($name, $defence_c);
				&write_colosseum_news(qq| <i><font color="$cs{color}[$country]">$name</font>‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½</i>|);
				&write_legend("champ_$m{stock}", "$cs{name}[$country]‚Ì$name‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚·", 1, $name);
				&send_twitter("$name‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½");
			}
			else {
				push @lines, "$name<>$country<>$max_hp<>$max_mp<>$at<>$df<>$mat<>$mdf<>$ag<>$cha<>$wea<>$skills<>$mes_win<>$mes_lose<>$icon<>$defence_c<>$wea_name<>$gua<>\n";
			}
		}
		else {
			push @lines, $line;
		}
		++$count;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# VÁ¬İËßµİ’a¶B
#================================================
sub _rewrite_champ {
	my $line = '';
	open my $fh, "+< $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my @lines = <$fh>;
	push @lines, "$m{name}<>$m{country}<>$m{max_hp}<>$m{max_mp}<>$m{at}<>$m{df}<>$m{mat}<>$m{mdf}<>$m{ag}<>$m{cha}<>$m{wea}<>$m{skills}<>$m{mes_win}<>$m{mes_lose}<>$m{icon}<>0<>$m{wea_name}<>$m{gua}<>\n";
	while(@lines > 3){
		$line = shift @lines;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($line) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = split /<>/, $line;

		# Î”è‚É‘‚«‚İ
		if ($defence_c >= $legend_defence_c) {
			&write_legend("champ_$m{stock}", "$cs{name}[$country]‚Ì$name‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚·", 1, $name);
			&write_colosseum_news(qq| <i><font color="$cs{color}[$country]">$name</font>‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½</i>|);
			&send_twitter("$name‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½");
		}
		else {
			&write_colosseum_news(qq| <b><font color="$cs{color}[$country]">$name</font>‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½</b>|, 1, $name);
			&send_twitter("$name‚ª$menus[$m{stock}][0]‚Å$defence_c‰ñ‚Ì–h‰q‚ğ‰Ê‚½‚µ–h‰qÒ‚ğˆø‘Ş‚µ‚Ü‚µ‚½");
		}
		
		&_send_money_and_col_c_up($name, $defence_c);
	}
}

#================================================
# ˆø‘ŞÒ‚É‚¨‹à‘—‹à‚Æ“¬‹Zên—û“x‚ğã‚°‚é
#================================================
sub _send_money_and_col_c_up {
	my($name, $defence_c) = @_;

	my $y_id = unpack 'H*', $name;
	if (-f "$userdir/$y_id/user.cgi") {
		&send_money($name, $menus[$m{stock}][0], $defence_c * $menus[$m{stock}][2]);

		my %datas = &get_you_datas($y_id, 1);
		$datas{col_c} += $defence_c;
		&regist_you_data($name, 'col_c', $datas{col_c});
	}
}


#================================================
# ©•ª‚ª–h‰qÒ‚©‚Ç‚¤‚©
#================================================
sub is_champ {
	open my $fh, "< $logdir/colosseum/champ_$m{stock}.cgi" or &error("$logdir/colosseum/champ_$m{stock}.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my $name = (split/<>/,$line)[0];
		return 1 if $name eq $m{name};
	}
	close $fh;
	return 0;
}

#================================================
# –h‰qÒ‚ÌƒXƒe[ƒ^ƒX•\¦
#================================================
sub champ_statuses {
	my $champ_stage = shift;
	
	open my $fh, "$logdir/colosseum/champ_$champ_stage.cgi" or &error("$logdir/colosseum/champ_$champ_stage.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my @lines = <$fh>;
	close $fh;
	
	$mes .= "<hr>–h‰qÒ<br>";
	my $count = @lines;
	for my $line (@lines) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $line;
		
		my $round_c = @round_titles - $count;
		my $wname = $wea_name ? $wea_name : $weas[$wea][1];
		$mes .= "$round_titles[$round_c]:$name(–h‰q$defence_c)/$wname/$guas[$gua][1]/$e2j{hp}$max_hp/$e2j{mp}$max_mp/$e2j{at}$at/$e2j{df}$df/$e2j{mat}$mat/$e2j{mdf}$mdf/$e2j{ag}$ag<br>";
		--$count;
	}
}


1; # íœ•s‰Â
