#=================================================
# í‘ˆoŒ‚€”õ Created by Merino
#=================================================

# S‘©ŠÔ
$GWT = int($GWT * 1.5);

my @needs = $m{unit} ne '18' ? (0.5, 1.0, 2.0) : (0.75, 1.5, 3.0);

# iŒRí—Ş
my @war_marchs = (
#	[0]–¼‘O,[1]iŒRŠÔ•ºm‚Ì”{—¦,[2]Œo”ï‚Ì”{—¦,[3]•K—vğŒ
	['­”¸‰s',	0.5,	$needs[0],	sub{ $pets[$m{pet}][2] ne 'speed_down' }],
	['’Êíí‘ˆ',	1.0,	$needs[1],	sub{ $m{win_c} >= 1  }],
	['’·Šú‰“ª',	1.5,	$needs[2],	sub{ $m{unit} ne '11' && $m{win_c} >= 10 && $m{win_c} > $m{lose_c} }]
);
if($m{value} < 0 || $m{value} >= @war_marchs){$m{value} = $#war_marchs;}
my $need_costs = $rank_sols[$m{rank}] * $war_marchs[$m{value}][2];
if($m{unit} eq '16'){$need_costs *= 0.75;}

#=================================================
# —˜—pğŒ
#================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '‘‚É‘®‚µ‚Ä‚È‚¢‚Æs‚¤‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ”æ˜J‚µ‚Ä‚¢‚éê‡‚Ís‚¦‚È‚¢
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= 'IíŠúŠÔ’†‚Íí‘ˆ‚ÆŒR–‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ( $cs{is_die}[$m{country}] && ($w{world} eq '9' || $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13'))) ) {
		$mes .= "¢ŠEî¨‚ª$world_states[$w{world}]‚ÅA©‘‚ª–Å–S‚µ‚Ä‚¢‚é‚Ì‚Åí‘ˆ‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$m{tp} = 1;
		$mes .= '‚Ç‚Ì‚æ‚¤‚ÉU‚ß‚İ‚Ü‚·‚©?<hr>';
	}
	else {
		$mes .= "‘¼‘‚ÖU‚ß‚İ$e2j{strong}‚ğ’D‚¢‚Ü‚·<br>";
		$mes .= "‚Ç‚Ì‚æ‚¤‚ÉU‚ß‚İ‚Ü‚·‚©?<hr>";
	}

	my @menus = ('‚â‚ß‚é');
	for my $war_march (@war_marchs) {
		if (&{ $war_march->[3] }) {
			my $need_fm  = $rank_sols[$m{rank}] * $war_march->[2];
			my $need_GWT = &_unit_march($GWT * $war_march->[1]);
			$mes .= "$war_march->[0] [Á”ï•º—ÆF$need_fm Á”ï—\\ZF$need_fm ŠÔF$need_GWT•ª]<br>";
			push @menus, $war_march->[0];
		}
		else {
			push @menus, '';
		}
	}

	&menu(@menus);
}

#================================================
# ‘‘I‘ğ
#================================================
sub tp_1 {
	return if &is_ng_cmd(1..$#war_marchs+1);
	--$cmd;

	# ˆÃE•”‘à‚Í’·Šú‰“ª‹Ö~
	if ($m{unit} eq '11' && $cmd eq '2') {
		$mes .= "$units[$m{unit}][1]‚Í$war_marchs[$cmd][0]‚ÅiŒR‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif (!&{$war_marchs[$cmd][3]}) {
		$mes .= "$war_marchs[$cmd][0]‚ÅiŒR‚·‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif (defined $war_marchs[$cmd]) {
		$m{value} = $cmd;
		$mes .= "$war_marchs[$cmd][0]‚ÅiŒR‚µ‚Ü‚·<br>";
		$mes .= '‚Ç‚Ì‘‚ÉU‚ß‚İ‚Ü‚·‚©?<br>';
		
		&menu('‚â‚ß‚é', @countries);
		$m{tp} = 100;
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		&begin;
	}
}

#================================================
# í‘ˆ¾¯Ä
#================================================
sub tp_100 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{country} eq $cmd) {
		$mes .= '©‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '–Å‚ñ‚Å‚¢‚é‘‚ÍU‚ß‚ß‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '“¯–¿‘‚ÉU‚ß‚Ş‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($need_costs > $cs{food}[$m{country}]) {
		$mes .= "iŒR‚·‚é‚Ì‚É•K—v‚È$e2j{food}‚ª‘«‚è‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif ($need_costs > $cs{money}[$m{country}]) {
		$mes .= "iŒR‚·‚é‚Ì‚É•K—v‚È$e2j{money}‚ª‘«‚è‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif ($rank_sols[$m{rank}] * $war_marchs[$m{value}][1] > $cs{soldier}[$m{country}]) {
		$mes .= "$e2j{soldier}‚ª‘«‚è‚Ü‚¹‚ñ<br>©‘‚ğç‚é•ºm‚ª‚¢‚È‚­‚È‚Á‚Ä‚µ‚Ü‚¢‚Ü‚·<br>";
		&begin;
	}
	# iŒR
	elsif ($cmd && defined $war_marchs[$m{value}]) {
		$m{lib} = 'war';
		$m{tp}  = 100;
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
		} elsif ($w{world} eq $#world_states - 5) {
			$y{country} = int(rand($w{country}))+1;
			my $loop = 0;
			while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
				if($loop > 30) {
					$y{country} = &get_most_strong_country;
				}
				$y{country} = int(rand($w{country}))+1;
				$loop++;
			}
		}
		
		my $v = int( $rank_sols[$m{rank}] * $war_marchs[$m{value}][1] );

		$cs{soldier}[$m{country}] -= $v;
		$cs{food}[$m{country}]    -= int($need_costs);
		$cs{money}[$m{country}]   -= int($need_costs);
		
		$m{sol} = int( $v + int($m{cha} * 0.005) * 500 ); # cha200’´‚¦‚²‚Æ‚É+500
		$m{sol} += 500 if($m{cha} == 999); # cha999‚Å+500
		$m{value} = $war_marchs[$m{value}][1];

		$GWT = &_unit_march($GWT * $m{value});

		$mes .= "$v‚Ì•º‚ğ—¦‚¢‚Ä$cs{name}[$y{country}]‚ÉiŒR‚ğŠJn‚µ‚Ü‚·<br>";
		$mes .= "$GWT•ªŒã‚É“’…‚·‚é—\\’è‚Å‚·<br>";

		if ($y{country} eq $m{renzoku}) {
			++$m{renzoku_c};
		}
		else {
			$m{renzoku} = $y{country};
			$m{renzoku_c} = 1;
		}

		&before_action('icon_pet_exp', $GWT);
		&wait;
		&write_cs;
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		&begin;
	}
}

#================================================
# •”‘à‚É‚æ‚èiŒRŠÔ‚Ì‘Œ¸(‹É’[‚É’·‚·‚¬E’Z‚·‚¬‚Í¹Ş°ÑÊŞ×İ½•ö‰ó‚·‚é‚Ì‚ÅŠÔ§ŒÀ)
#================================================
sub _unit_march {
	my $need_GWT = shift;
	# d•ºBÅ‚iŒRŠÔ90•ª
	if ($m{unit} eq '1' && ($pets[$m{pet}][2] ne 'speed_up' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && $need_GWT * 1.5 < 90) {
		$need_GWT = $need_GWT * 1.5;
	}
	# “V”n,”ò—³BÅ’áiŒRŠÔ20•ª
	elsif ( ($m{unit} eq '7' || $m{unit} eq '8' || ($pets[$m{pet}][2] eq 'speed_up' && $w{world} ne '17')) && $need_GWT * 0.5 > 20 && $m{unit} ne '18') {
		$need_GWT = $need_GWT * 0.5;
	}
	if ($pets[$m{pet}][2] eq 'speed_down' && $w{world} ne '17') {
		$need_GWT *= $m{unit} eq '7' || $m{unit} eq '8' ? 4 : 2;
		$m{value} *= 3 unless $m{unit} eq '18';
	}
	
	if ($m{pet} eq '193'
#	&& $w{world} ne '7' && $w{world} ne $#world_states	
	) {
		$need_GWT -= 10;
	}
	return int($need_GWT);
}


1; # íœ•s‰Â
