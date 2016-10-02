$mes .= qq|ŒMÍ $m{medal}ŒÂ<br>| if $is_mobile;
#=================================================
# •”‘à•ÏX Created by Merino
#=================================================

# ŒMÍ1ŒÂ‚Ì‹àŠz
my $exchange_money = 3000;

# š30•Ší‚Ì‰¿’l
my $exchange_medal = $m{wea} == 0 ? 0:
					$m{wea} <= 30 ? (($m{wea} - 1) % 5 + 1) * 5:
					($m{wea} % 5 + 5) * 5;

# ˆø‚«Š·‚¦•i
my @prizes = (
# í—Ş 1=•Ší,2=—‘,3=Íß¯Ä 
#	[0]í—Ş,[1]No,[2]ŒMÍ
	[0,	0,	0,	],
	[2,	24,	2,	], # ÌŞ×¯ÄŞ´¯¸Ş
	[2,	51,	3,	], # ËŞ·ŞÅ°´¯¸Ş
	[1,	12,	5,	], # ÄÏÎ°¸
	[1,	17,	5,	], # ´ÙÌ§²±°
	[1,	27,	5,	], # ´Ù»İÀŞ°
	[3,	126,	15,	], # ½Ø°Ìß¼°Ìß
	[2,	21,	15,	], # Ú¼ŞªİÄŞ´¯¸Ş
	[3,	184,	18,	], # Úİ¼Ş
	[2,	33,	20,	], # ³ªÎßİ´¯¸Ş
	[2,	27,	25,	], # ÊßİÄŞ×´¯¸Ş
	[2,	3,	30,	], # ÄŞØ°Ñ´¯¸Ş
	[2,	45,	80,	], # ´İÄŞ´¯¸Ş
	[2,	37,	90,	], # ºŞ¯ÄŞ´¯¸Ş
	[2,	46,	99,	], # ÊŞÂ´¯¸Ş
);

# “Á•ÊğŒ‚Å¸×½Áªİ¼Ş‚Å‚«‚é‚à‚Ì
my %plus_needs = (
# •”‘àNo => ğŒ•¶,					ifğŒ									# ğŒ¸Ø±Œã‚Ìˆ—
	7  => ['ÀŞ°¸Î°½‚ğ¶æÑ',			sub{ $pets[$m{pet}][2] eq 'speed_up' },	sub{ $mes.="$pets[$m{pet}][1]š$m{pet_c}‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; &remove_pet; } ],
	8  => ['ÄŞ×ºŞİŒn‚ÌÍß¯Ä‚ğ¶æÑ',	sub{ $pets[$m{pet}][1] =~ /ÄŞ×ºŞİ/ },	sub{ $mes.="$pets[$m{pet}][1]š$m{pet_c}‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; &remove_pet; } ],
	11 => ['E‹Æ‚ª”EÒ',			sub{ $jobs[$m{job}][1] eq '”EÒ' },		sub{} ],
	12 => ["$eggs[23][1]‚ğ¶æÑ",	sub{ $m{egg} eq '23'},					sub{ $mes.="$eggs[$m{egg}][1]‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; $m{egg} = 0; $m{egg_c} = 0; } ],
	15 => ['E‹Æ‚ª–‚•¨g‚¢',		sub{ $jobs[$m{job}][1] eq '–‚•¨g‚¢' },	sub{} ],
	16 => ['¸ÛÉ½‚ğ¶æÑ+“à­n—û“x‚ªŒv5000ˆÈã',			sub{ ($pets[$m{pet}][0] eq '42' && $m{nou_c}+$m{sho_c}+$m{hei_c}>=5000) },	sub{$mes.="$pets[$m{pet}][1]š$m{pet_c}‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; &remove_pet;} ],
	17 => ['ºŞ°½Ä‚ğ¶æÑ+’DŒR–3ín—û“x‚ªŒv10000ˆÈã',			sub{ ($pets[$m{pet}][2] eq 'no_ambush' && $m{gou_c}+$m{cho_c}+$m{sen_c}>=10000) },	sub{$mes.="$pets[$m{pet}][1]š$m{pet_c}‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; &remove_pet;} ],
	18 => ['Û·‚ğ¶æÑ+í‘ˆŸ—˜”500ˆÈã',			sub{ ($pets[$m{pet}][0] eq '12' && $m{win_c}>=500) },	sub{$mes.="$pets[$m{pet}][1]š$m{pet_c}‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; &remove_pet;} ],
);


#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚ ‚è‚Ü‚·‚©?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "‚±‚±‚Å‚Í$m{name}‚Ì‚Á‚Ä‚¢‚éŒMÍ‚É‰‚¶‚Ä•”‘à‚ğ¸×½Áªİ¼Ş‚µ‚½‚è‚Å‚«‚Ü‚·<br>";
		$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
	}
	&menu('‚â‚ß‚é','‚¨‹à‚ª—~‚µ‚¢','±²ÃÑ‚ª—~‚µ‚¢','•”‘à‚ğ•Ï‚¦‚½‚¢','–¼—_E‚É‚È‚é','©•ª‚¾‚¯‚Ì•Ší‚ª—~‚µ‚¢','ŒMÍ‚ª—~‚µ‚¢');
}
sub tp_1 {
	return if &is_ng_cmd(1..6);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ŒMÍ¨‚¨‹à
#=================================================
sub tp_100 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "ŒMÍ1ŒÂ‚É‚Â‚« $exchange_money G‚ÉŠ·‚¦‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
	$mes .= "‰½ŒÂ‚ÌŒMÍ‚ğŒ£ã‚µ‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="medal" value="0" class="text_box1" style="text-align:right">ŒÂ|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="Œ£ã‚·‚é" class="button1"></p></form>|;
}
sub tp_110 {
	if ($in{medal} && $in{medal} !~ /[^0-9]/) {
		if ($in{medal} > $m{medal}) {
			$mes .= "$in{medal}ŒÂ‚àŒMÍ‚ğ‚Á‚Ä‚¢‚Ü‚¹‚ñ<br>";
		}
		else {
			my $v = $in{medal} * $exchange_money;
			$m{money} += $v;
			$m{medal} -= $in{medal};
			
			$mes .= "ŒMÍ$in{medal}ŒÂ‚ğŒ£ã‚µ‚Ä $v G‚ğ‚à‚ç‚¢‚Ü‚µ‚½<br>";
		}
	}
	&begin;
}

#=================================================
# ŒMÍ¨±²ÃÑ
#=================================================
sub tp_200 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "‚Ç‚ê‚ÆŒğŠ·‚µ‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1" cellpadding="3"><tr><th>–¼‘O</th><th>ŒMÍ<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i">|;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[—‘]$eggs[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '3' ? qq|[ƒy]$pets[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[$guas[ $prizes[$i][1] ][2]]$guas[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]ŒÂ<br></td></tr>|;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>~<input type="text" name="loop" value="1" class="text_box1" style="text-align:right"></p>|;
	$mes .= qq|<p><input type="submit" value="ŒğŠ·‚·‚é" class="button1"></p></form>|;
}
sub tp_210 {
	if ($cmd && defined $prizes[$cmd]) {
		if ($in{loop} && $in{loop} !~ /[^0-9]/) {
			for my $loop (1..$in{loop}) {
				if ($m{medal} >= $prizes[$cmd][2]) {
					$m{medal} -= $prizes[$cmd][2];
					
					$mes .= "ŒMÍ$prizes[$cmd][2]ŒÂ‚ğŒ£ã‚µ‚Ä";

					if ($prizes[$cmd][0] eq '1') {
						$mes .= "$weas[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], $weas[ $prizes[$cmd][1] ][4], 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '2') {
						$mes .= "$eggs[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '3') {
						$mes .= "$pets[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '4') {
						$mes .= "$guas[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
				}
				else {
					$mes .= 'ŒMÍ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
				}
			}
		}
	}
	&begin;
}

#=================================================
# ŒMÍ¨•”‘à{‚¨‹à
#=================================================
sub tp_300 {
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "¸×½Áªİ¼Ş‚Å—]‚Á‚½ŒMÍ‚Í‚¨‹à‚ÉŠ·‹à‚µ‚Ü‚·<br>";
	$mes .= "‚Ç‚Ì•”‘à‚É¸×½Áªİ¼Ş‚µ‚Ü‚·‚©?<hr>";
	$mes .= "¡‚Ì•”‘à‚©‚ç‚Å¸×½Áªİ¼Ş‚Å‚«‚é‚Ì‚ÍˆÈ‰º‚Å‚·<br>";
	
	$mes .= "$units[0][1] ğŒF‚È‚µ<br>";
	my @menus = ('‚â‚ß‚é', $units[0][1]);
	if ($config_test) {
		for my $i (1 .. $#units) {
			$mes .= "$units[$i][1] ğŒF‚È‚µ<br>";
			push @menus, $units[$i][1];
		}
	}
	else {
		for my $i (1 .. $#units) {
			if ($i eq $units[$m{unit}][2]) {
				$mes .= "$units[$i][1] ğŒF‚È‚µ<br>";
				push @menus, $units[$i][1];
			}
			elsif ($m{unit} eq $units[$i][2]) {
				$mes .= "$units[$i][1] ğŒF$units[ $units[$i][2] ][1]/ŒMÍ$units[$i][3]ŒÂ/";
				$mes .= $plus_needs{$i}[0] if defined $plus_needs{$i};
				$mes .= "<br>";
				
				push @menus, $units[$i][1];
			}
			else {
				push @menus, '';
			}
		}
	}
	
	&menu(@menus);
}
sub tp_310 {
	if ($cmd) {
		--$cmd;

		if ($cmd) {
			if ($config_test) {
				$m{unit} = $cmd;
				$mes .= "$units[$m{unit}][1]‚É¸×½Áªİ¼Ş‚µ‚Ü‚µ‚½<br>";
				&begin;
				return;
			}

			# ¸×½ÀŞ³İ
			unless ($cmd eq $units[$m{unit}][2]) {
				# “ÁêğŒ
				if (defined $plus_needs{$cmd}) {
					if (&{ $plus_needs{$cmd}[1] } && $units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
						&{ $plus_needs{$cmd}[2] };
						$m{medal} -= $units[$cmd][3];
					}
					else {
						$mes .= "¸×½Áªİ¼Ş‚Å‚«‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
						&begin;
						return;
					}
				}
				elsif ($units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
					$m{medal} -= $units[$cmd][3];
				}
				else {
					$mes .= "¸×½Áªİ¼Ş‚Å‚«‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
					&begin;
					return;
				}
			}
		}
		
		$m{unit} = $cmd;
		$mes .= "$units[$m{unit}][1]‚É¸×½Áªİ¼Ş‚µ‚Ü‚µ‚½<br>";

		if ($m{medal} > 0) {
			my $v = $m{medal} * $exchange_money;
			$m{money} += $v;
			$mes .= "c‚è‚ÌŒMÍ$m{medal}ŒÂ‚ğŒ£ã‚µ‚Ä $v G‚ğ‚à‚ç‚¢‚Ü‚µ‚½<br>";
			$m{medal} = 0;
		}
	}
	&begin;
}

#=================================================
# –¼—_E
#=================================================
sub tp_400 {
	if ($m{rank_exp} <= 6210 || $m{rank} != $#ranks) { # (13*13*10) + (14*14*10) + (16*16*10) ‚©‚Â Å‚ŠK‹‰
		$mes .= "–¼—_ŠK‹‰‚É‚È‚ê‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
		&begin;
		return;
	}

	$layout = 1;
	$m{tp} += 10;
	$mes .= "1¢‘ãŒÀ‚è‚Ì–¼—_E‚ÉA‚«‚Ü‚·<br>";
	$mes .= "vŒ£’l2560‚ÅŠK‹‰–¼‚ğ©—R‚É•Ï‚¦‚ç‚ê‚Ü‚·<br>";
	$mes .= "–¼—_E‚É‚È‚è‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="s_rank" value="" class="text_box1" style="text-align:right">ŠK‹‰–¼|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="–¼—_E‚É‚È‚é" class="button1"></p></form>|;
}
sub tp_410 {
	&error("ŠK‹‰–¼‚ª’·‚·‚¬‚Ü‚·‘SŠp5(”¼Šp10)•¶š‚Ü‚Å‚Å‚·") if length $in{s_rank} > 10;
	if ($in{s_rank}) {
		$m{rank_exp} -= 2560;
		$m{super_rank} += 1;
		$in{s_rank} =~ s/š/™/g;
		$m{rank_name} = $in{s_rank};

		$mes .= "–¼—_Euš$m{rank_name}v‚É‚È‚è‚Ü‚µ‚½<br>";
	}
	&begin;
}

#=================================================
# •ó‹ï
#=================================================
sub tp_500 {
	$m{tp} += 10;
	$mes .= "¸ÛÑÊ°Â‚Æˆø‚«Š·‚¦‚É©•ª‚Ì•Ší‚ğŒ©‚Â‚¯‚Ü‚·<br>";
	&menu('‚â‚ß‚é','¸ÛÑÊ°Â‚ğ•ù‚°‚é');
}
sub tp_510 {
	if ($cmd eq '1' && $m{wea} eq '32' && $m{wea_lv} >= 30) {
		$mes .= "Íß¯Ä‚ğ‘—‚è‚Ü‚µ‚½<br>";
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		&send_item($m{name}, 3, 191, 0, 0, 1);
	}else{
		$mes .= "š30‚Ì¸ÛÑÊ°Â‚ÆŒğŠ·‚Å‚«‚Ü‚·<br>";
	}
	&begin;
}

#=================================================
# •Ší¨ŒMÍ
#=================================================
sub tp_600 {
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "‚²ˆ¤—p‚Ì•Ší‚ğŒMÍ $exchange_medal ŒÂ‚ÉŠ·‚¦‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
	$mes .= "”„‚è•¥‚¢‚Ü‚·‚©?<br>";
	
	&menu('‚â‚ß‚é','”„‚è•¥‚¤');
}
sub tp_610 {
	if ($cmd eq '1') {
		if ($m{wea_lv} ne '30') {
			$mes .= "V•i‚Å‚ÍŒMÍ‚É•Ï‚¦‚ç‚ê‚Ü‚¹‚ñ<br>";
		}
		else {
			$m{wea} = 0;
			$m{wea_c} = 0;
			$m{wea_lv} = 0;
			if($m{wea_name}){
				$m{wea_name} = "";
				$exchange_medal += 0;
			}
			$m{medal} += $exchange_medal;
			
			$mes .= "ˆ¤—p‚Ì•Ší‚ğ¿‚É“ü‚êAŒMÍ‚ğ $exchange_medal ŒÂ‚à‚ç‚¢‚Ü‚µ‚½<br>";
		}
	}
	&begin;
}


1; # íœ•s‰Â
