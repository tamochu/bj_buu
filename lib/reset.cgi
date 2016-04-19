use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_world_reset.cgi';
require './lib/_festival_world.cgi';
#================================================
# ‘Ø¾¯Ä Created by Merino
#================================================

# “ˆê“ïˆÕ“xF[“ï‚µ‚¢ 60 ` 40 ŠÈ’P]
my $game_lv = $config_test ? int(rand(6) + 5) : int( rand(11) + 40 );

# “ˆêŠúŒÀ(“ú)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# Šú“ú‚ª‰ß‚¬‚½ê‡
#================================================
sub time_limit {
	# Õ‚èî¨‚ÉŠúŒÀØ‚ê
	if (&is_special_world) {
		if ($w{world} eq $#world_states-5) { # Ù‘¬
			my $strongest_country = 0;
			my $max_value = 0;
			for my $i (1 .. $w{country}) {
				if ($cs{strong}[$i] > $max_value) {
					$strongest_country = $i;
					$max_value = $cs{strong}[$i];
				}
			}
			&write_world_news("<b>$world_name‘å—¤‚ğ‘S“y‚É‚í‚½‚é‘—Í‹£‘ˆ‚Í$cs{name}[$strongest_country]‚ÌŸ—˜‚É‚È‚è‚Ü‚µ‚½</b>");
			&write_legend('touitu', "$world_name‘å—¤‚ğ‘S“y‚É‚í‚½‚é‘—Í‹£‘ˆ‚Í$cs{name}[$strongest_country]‚ÌŸ—˜‚É‚È‚è‚Ü‚µ‚½");
			$w{win_countries} = $strongest_country;
		}
		else {
			&write_world_news("<b>$world_name‘å—¤‚ğ“ˆê‚·‚éÒ‚ÍŒ»‚ê‚Ü‚¹‚ñ‚Å‚µ‚½</b>");
			&write_legend('touitu', "$world_name‘å—¤‚ğ“ˆê‚·‚éÒ‚ÍŒ»‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
		}
		$w{world} = int(rand($#world_states-5));
		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#		&player_migrate($migrate_type);
	}
	else { # ’Êíî¨‚ÅŠúŒÀØ‚ê
		&write_world_news("<b>$world_name‘å—¤‚ğ“ˆê‚·‚éÒ‚ÍŒ»‚ê‚Ü‚¹‚ñ‚Å‚µ‚½</b>");
		&write_legend('touitu', "$world_name‘å—¤‚ğ“ˆê‚·‚éÒ‚ÍŒ»‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
		$w{win_countries} = '';

		# “Áêî¨‘OŠú‚Å‚Í‚È‚¢‚È‚ç
		unless ($w{year} =~ /5$/ || $w{year} =~ /9$/) {
			my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
			my @next_worlds = &unique_worlds(@new_worlds);
			$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
		}
#			my $year = $w{year} + 1;
#			if ($year =~ /06$/ || $year =~ /26$/ || $year =~ /46$/ || $year =~ /66$/ || $year =~ /86$/) { # ‰p—Y
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-4] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($w{year} =~ /5$/) { # ˆÃ•
##				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 0) { # •s‹ä‘Õ“V
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-2] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 20) { # O‘u
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-3] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 10) { # Ù‘¬
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-5] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			else { # ¬—
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-1] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#		}
#		else {
#			unless ($w{year} =~ /5$/ || $w{year} =~ /6$/) {
#			}
#			if ($w{year} =~ /6$/) { # ˆÃ•I—¹‚È‚ç
#				$w{world} = int(rand($#world_states-5));
#			}
#			else {
#				my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
#				my @next_worlds = &unique_worlds(@new_worlds);
#				$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#			}

#			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#		}
	}

	&reset; # ‚±‚±‚Ü‚Å¡ŠúŠúŒÀØ‚ê‚Ìˆ—

	if ($w{world} eq '0') {# •½˜a
		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚É‚È‚è‚Ü‚µ‚½</i>");
	}
	elsif ($w{world} eq '18') {# E”°
		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚µ‚½‚Ó‚¢‚ñ‚«(©‚È‚º‚©•ÏŠ·‚Å‚«‚È‚¢)‚É‚È‚è‚Ü‚µ‚½</i>");
	}
	else {
		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
	}

#			my $year = $w{year} + 1;
#			if ($year =~ /06$/ || $year =~ /26$/ || $year =~ /46$/ || $year =~ /66$/ || $year =~ /86$/) { # ‰p—Y
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-4] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($w{year} =~ /5$/) { # ˆÃ•
##				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 0) { # •s‹ä‘Õ“V
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-2] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 20) { # O‘u
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-3] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			elsif ($year % 40 == 10) { # Ù‘¬
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-5] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#			else { # ¬—
#				&write_world_news("<i>¢ŠE‚Í $world_states[$#world_states-1] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#			}
#		}
#		else {
#			unless ($w{year} =~ /5$/ || $w{year} =~ /6$/) {
#			}
#			if ($w{year} =~ /6$/) { # ˆÃ•I—¹‚È‚ç
#				$w{world} = int(rand($#world_states-5));
#			}
#			else {
#				my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
#				my @next_worlds = &unique_worlds(@new_worlds);
#				$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#			}

#			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#		}
#	}

#	my $migrate_type = 0;
#	# ¢ŠEî¨ ¬—“Ë“ü
#	if ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		$migrate_type = &opening_festival;
#		&wt_c_reset;
#	}

#	unshift @old_worlds, $w{world};

#	elsif ($w{world} eq $#world_states) { # ˆÃ•‚È‚ç‚Î
#		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#	}
#	elsif ($w{world} eq $#world_states-4) { # ‰p—Y
#		$w{game_lv} += 20;
#		for my $i (1 .. $w{country}) {
#			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#		}
#	}

	$w{game_lv} = 0;

	&write_cs;
#	&player_migrate($migrate_type) if &is_festival_world;
}

#================================================
# ‘ÃŞ°ÀØ¾¯Äˆ—
# “ˆê‚ÆŠúŒÀØ‚ê‚ÅŒÄ‚Î‚ê‚é‚Ì‚Å’ŠÛ“I‚Æ‚·‚é
# ‚»‚µ‚Ä‚»‚ê‚¼‚ê‚Ìê‡•ª‚¯‚ğŠO•”‚Å‚â‚é
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});

	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
	}

	# I—¹ˆ—
	if (&is_special_world) { # “Áêî¨I—¹
		if ($w{year} =~ /6$/) { # ˆÃ•E‰p—YI—¹
			unless ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # ˆÃ•I—¹
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# ‰p—YI—¹ˆ—‚Í“Á‚É‚È‚µ
		}
		else { # Õ‚èî¨I—¹
			require './lib/_festival_world.cgi';
			my $migrate_type = &ending_festival;
			&player_migrate($migrate_type);
		}
#		$w{world} = int(rand($#world_states-5));
	}

	# ¢ŠEî¨ ˆÃ•‰ğœ
#	if ($w{year} =~ /6$/) {
#		$w{world} = int(rand($#world_states-5));
#		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
#			$w{world} = int(rand($#world_states-5));
#		} else {
#			require './lib/vs_npc.cgi';
#			&delete_npc_country;
#			$w{world} = int(rand($#world_states-5));
#		}
		# “ˆê¨reset‚Åƒ‰ƒ“ƒ_ƒ€î¨¨ƒ†[ƒU[‚ªî¨Œˆ’è
		# ƒ†[ƒU[‚ªî¨‚ğ‘I‚Î‚È‚¢ŒÀ‚èˆÃ•‚ª‘±‚­‚Ì‚Åd•û‚È‚¢‚©H
#		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
#	}
#	# ¢ŠEî¨ ¬—‰ğœ
#	if ($w{year} =~ /0$/) {
#		if($w{year} % 40 == 0){#•s‹ä‘Õ“V
#			$migrate_type = &festival_type('kouhaku', 0);
#			$w{country} -= 2;
#		}elsif($w{year} % 40 == 20){# O‘u
#			$migrate_type = &festival_type('sangokusi', 0);
#			$w{country} -= 3;
#		}elsif($w{year} % 40 == 10){# Ù‘¬
#			$migrate_type = &festival_type('sessoku', 0);
#		}else {#¬—
#			$migrate_type = &festival_type('konran', 0);
#		}
#		$w{world} = int(rand($#world_states-5));
#		# ‚Æ‚è‚ ‚¦‚¸ƒ†[ƒU[‚ªî¨‚ğ‘I‚Ô—]’n‚ª‚È‚¢Ù‘¬‚¾‚¯•\¦
#		# ‚¨‚»‚ç‚­“ˆêŠúŒÀØ‚ê‚Å‚±‚±‚ğ’Ê‚Á‚Ä‚¢‚é‚È‚ç‘¼‚ÌÕ‚èî¨‚Å‚à•\¦‚µ‚È‚¢‚Æ¡“x‚Í‰½‚à•\¦‚³‚ê‚È‚¢
#		# í‘ˆ‚Å“ˆê‚µ‚½‚Ì‚©ŠúŒÀØ‚ê‚È‚Ì‚©—v”»’f
#		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>") if $w{year} % 40 == 10;
#	}
	# dŠ¯‚Å‚«‚él”
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);
	
	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
#	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{limit_time} = $config_test ? $time: $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;
	if($w{year} % 40 == 10){
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $config_test ? $time: $time + 3600 * 36;
		$w{game_lv} = 99;
	}
	
	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# “ˆê‘‚Ìê‡‚ÍNPCã‘Ì
		if($w{year} % 40 == 10){
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		} else {
			$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
			$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		}
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			if ($cs{ceo}[$i]) {
				my $n_id = unpack 'H*', $cs{ceo}[$i];
				open my $fh, ">> $userdir/$n_id/ex_c.cgi";
				print $fh "ceo_c<>1<>\n";
				close $fh;
			}
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
		
		if ($w{year} % $reset_daihyo_cycle_year == 0) {
			for my $k (qw/war dom pro mil/) {
				my $kc = $k . "_c";
				next if $cs{$k}[$i] eq '';
				my $trick_id = unpack 'H*', $cs{$k}[$i];
				my %datas = &get_you_datas($trick_id, 1);
				&regist_you_data($cs{$k}[$i], $kc, int($datas{$kc} * 0.5));
				
				$cs{$k}[$i] = '';
				$cs{$kc}[$i] = 0;
				
			}
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>Še‘‚Ì$e2j{ceo}‚Ì”CŠú‚ª–—¹‚Æ‚È‚è‚Ü‚µ‚½</b>");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>Še‘‚Ì‘ã•\\Ò‚Ì”CŠú‚ª–—¹‚Æ‚È‚è‚Ü‚µ‚½</b>");
	}

	# “Áêî¨ŠJnˆ—
	if (&is_special_world) { # “Áêî¨ŠJn
		if ($w{year} =~ /6$/) { # ˆÃ•E‰p—YŠJn
			if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # ‰p—YŠJn
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
			else { # ˆÃ•ŠJn
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
		}
		else { # Õ‚èî¨ŠJn
			require './lib/_festival_world.cgi';
			my $migrate_type = &opening_festival;
#			if ($w{year} % 40 == 0){ # •s‹ä‘Õ“V
#				$migrate_type = &festival_type('kouhaku', 1);
#				$w{world} = $#world_states-2;
#			} elsif ($w{year} % 40 == 20) { # O‘u
#				$migrate_type = &festival_type('sangokusi', 1);
#				$w{world} = $#world_states-3;
#			} elsif ($w{year} % 40 == 10) { # Ù‘¬
#				$migrate_type = &festival_type('sessoku', 1);
#				$w{world} = $#world_states-5;
#			} else { # ¬—
#				$migrate_type = &festival_type('konran', 1);
#				$w{world} = $#world_states-1;
#			}
			&wt_c_reset;
#			if ($w{world} eq $#world_states-1) { # ¬—
#			}
#			elsif ($w{world} eq $#world_states-2) { # •s‹ä‘Õ“V
#				$migrate_type = &festival_type('kouhaku', 0);
#				$w{country} -= 2;
#			}
#			elsif ($w{world} eq $#world_states-3) { # O‘u
#				$w{country} -= 3;
#			}
#			elsif ($w{world} eq $#world_states-5) { # Ù‘¬
#			}
			&player_migrate($migrate_type);
		}
#		$w{world} = int(rand($#world_states-5));
	}
	else {
		if ($w{world} eq '0') { # •½˜a
			$w{reset_time} += 3600 * 12;
		}
		elsif ($w{world} eq '6') { # Œ‹‘©
			my @win_cs = ();
			for my $i (1 .. $w{country}) {
				push @win_cs, [$i, $cs{win_c}[$i]];
			}
			@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;

			# Šï”‚Ìê‡‚Íˆê”Ô‘‚Íœ‚­
			shift @win_cs if @win_cs % 2 == 1;
			
			my $half_c = int(@win_cs*0.5-1);
			for my $i (0 .. $half_c) {
				my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
				$w{'p_'.$c_c} = 1;
			}
		}
		elsif ($w{world} eq '18') { # E”°
			$w{reset_time} = $time;
			for my $i (1 .. $w{country}) {
				$cs{food}[$i]     = int(rand(300)) * 1000;
				$cs{money}[$i]    = int(rand(300)) * 1000;
				$cs{soldier}[$i]  = int(rand(300)) * 1000;
			}
		}
		$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	}

	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

	# ¢ŠEî¨ ˆÃ•“Ë“ü
#	if ($w{year} =~ /6$/) {
#		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # ‰p—Y
#			$w{world} = $#world_states-4;
#			$w{game_lv} += 20;
#			for my $i (1 .. $w{country}) {
#				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#			}
#		} else {
#			require './lib/vs_npc.cgi';
#			&add_npc_country;
#		}
#	}
#	# ¢ŠEî¨ ¬—“Ë“ü
#	if ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		if ($w{year} % 40 == 0){ # •s‹ä‘Õ“V
#			$w{world} = $#world_states-2;
#		} elsif ($w{year} % 40 == 20) { # O‘u
#			$w{world} = $#world_states-3;
#		} elsif ($w{year} % 40 == 10) { # Ù‘¬
#			$w{world} = $#world_states-5;
#		} else { # ¬—
#			$w{world} = $#world_states-1;
#		}
#		&wt_c_reset;
#	}
	
	# 1000”NƒfƒtƒHƒ‹ƒg
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
#	return $migrate_type;
}

1; # íœ•s‰Â