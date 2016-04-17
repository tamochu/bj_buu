sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
require './lib/world_reset.cgi';
#================================================
# ¢ŠEî¨ Created by Merino
#================================================

#================================================
# ‘I‘ğ‰æ–Ê
#================================================
sub tp_100 {
	$mes .= "‚ ‚È‚½‚Í‚±‚Ì¢ŠE‚É‰½‚ğ‹‚ß‚Ü‚·‚©?<br>";
	&menu('ŠF‚ª–]‚Ş‚à‚Ì','Šó–]','â–]','•½˜a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $wline;
	$wline = <$fh>;
	my @old_worlds = split /<>/, $wline;
	close $fh;
	my @next_worlds;
	my @new_worlds;
	
	if ($cmd eq '1') { # Šó–]
		&mes_and_world_news("<b>¢ŠE‚ÉŠó–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
	}
	elsif ($cmd eq '2') { # â–]
		&mes_and_world_news("<b>¢ŠE‚Éâ–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		@new_worlds = (8,9,10,11,12,13,14,15,16);
	}
	elsif ($cmd eq '3') { # •½˜a
		&mes_and_world_news("<b>¢ŠE‚É•½˜a‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		@new_worlds = (0);
	}
	else {
		&mes_and_world_news('<b>¢ŠE‚É‚İ‚È‚ª–]‚Ş‚à‚Ì‚ğ–]‚İ‚Ü‚µ‚½</b>', 1);
		@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
	}

	for my $new_v (@new_worlds){
		my $old_year = 0;
		my $old_flag = 0;
		for my $o (@old_worlds){
			last if $old_year > 10;
			if ($new_v == $o){
				$old_flag = 1;
				last;
			}
			$old_year++;
		}
		push @next_worlds, $new_v unless $old_flag;
	}

	$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
	$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

	# ‹­§ˆÃ•Šú
	if ($old_world eq $#world_states) {
		$w{world} = $#world_states;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‚©‚«Á‚³‚ê‚Ü‚µ‚½</i>");
	}
	# ‹­§ƒVƒƒƒbƒtƒ‹
	elsif ($old_world eq $#world_states-1) {
		$w{world} = $#world_states-1;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í¬—‚ÉŠ×‚è‚Ü‚µ‚½</i>");
	}
	# ‹­§g”’
	elsif ($old_world eq $#world_states-2) {
		$w{world} = $#world_states-2;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í“ñ‚Â‚É•ª‚©‚ê‚Ü‚µ‚½</i>");
	}
	# ‹­§O‘
	elsif ($old_world eq $#world_states-3) {
		$w{world} = $#world_states-3;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­•ª—ô‚µ‚½¢ŠE‚ğ“ˆê‚·‚×‚­O‘‚ª‘ä“ª‚µ‚Ü‚µ‚½</i>");
	}
	# ‹­§‰p—Y
	elsif ($old_world eq $#world_states-4) {
		$w{world} = $#world_states-4;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í‰p—Y‚ª“`à‚ğì‚èo‚·‘ã‚É‚È‚è‚Ü‚µ‚½</i>");
	}
	# ‹­§Ù‘¬
	elsif ($old_world eq $#world_states-5) {
		$w{world} = $#world_states-5;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­¢ŠE‚ª‹£‚¢‡‚¤‚±‚Æ‚É</i>");
	}
	# “¯‚¶‚Ì‚¶‚á‚Â‚Ü‚ç‚È‚¢‚Ì‚Å
	elsif ($w{world} eq $old_world) {
		$w{world} = int(rand(@world_states-3));
		++$w{world} if $w{world} eq $old_world;
		$w{world} = int(rand(10)) if $w{world} > $#world_states-3;
		&write_world_news("<i>¢ŠE‚Í $world_states[$old_world] ‚Æ‚È‚è‚Üc‚¹‚ñ $world_states[$w{world}]‚Æ‚È‚è‚Ü‚µ‚½</i>");
	}
	else {
		if ($w{world} eq '0') { # •½˜a
			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚É‚È‚è‚Ü‚µ‚½</i>");
		}elsif ($w{world} eq '18') { # E”°
			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚µ‚½‚Ó‚¢‚ñ‚«(©‚È‚º‚©•ÏŠ·‚Å‚«‚È‚¢)‚É‚È‚è‚Ü‚µ‚½</i>");
		}else{
			&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
		}
	}	
	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$nline\n";
	close $fh;
	
	my $migrate_type = 0;
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
	elsif ($w{world} eq $#world_states-4) { # ‰p—Y
		$w{game_lv} += 20;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states-2) { # •s‹ä‘Õ“V
		$w{game_lv} = 99;
		$w{country} += 2;
		my $max_c = int($w{player} / 2) + 3;
		for my $i ($w{country}-1..$w{country}){
			mkdir "$logdir/$i" or &error("$logdir/$i Ì«ÙÀŞ‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½") unless -d "$logdir/$i";
			for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				next if -f $output_file;
				open my $fh, "> $output_file" or &error("$output_file Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
				close $fh;
				chmod $chmod, $output_file;
			}
			for my $file_name (qw/leader member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				open my $fh, "> $output_file" or &error("$output_file Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
				close $fh;
				chmod $chmod, $output_file;
			}
			&add_npc_data($i);
			# create union file
			for my $j (1 .. $i-1) {
				my $file_name = "$logdir/union/${j}_${i}";
				$w{ "f_${j}_${i}" } = -99;
				$w{ "p_${j}_${i}" } = 2;
				next if -f "$file_name.cgi";
				open my $fh, "> $file_name.cgi" or &error("$file_name.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh;
				chmod $chmod, "$file_name.cgi";
				open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh2;
				chmod $chmod, "${file_name}_log.cgi";
				open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh3;
				chmod $chmod, "${file_name}_member.cgi";
			}
			unless (-f "$htmldir/$i.html") {
				open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh_h;
			}
			$cs{name}[$i]     = $i == $w{country} ? "‚½‚¯‚Ì‚±‚Ì—¢":"‚«‚Ì‚±‚ÌR";
			$cs{color}[$i]    = $i == $w{country} ? '#ff0000':'#ffffff';
			$cs{member}[$i]   = 0;
			$cs{win_c}[$i]    = 999;
			$cs{tax}[$i]      = 99;
			$cs{strong}[$i]   = 75000;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = $max_c;
			$cs{is_die}[$i]   = 0;
			my @lines = &get_countries_mes();
			if ($w{country} > @lines - 2) {
				open my $fh9, ">> $logdir/countries_mes.cgi";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				close $fh9;
			}
		}
		$migrate_type = 5;
		
		for my $i (1 .. $w{country}-2) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-2) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	elsif ($w{world} eq $#world_states-3) { # O‘u
		$w{game_lv} = 99;
		$w{country} += 3;
		my $max_c = int($w{player} / 3) + 3;
		for my $i ($w{country}-2..$w{country}){
			mkdir "$logdir/$i" or &error("$logdir/$i Ì«ÙÀŞ‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½") unless -d "$logdir/$i";
			for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				next if -f $output_file;
				open my $fh, "> $output_file" or &error("$output_file Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
				close $fh;
				chmod $chmod, $output_file;
			}
			for my $file_name (qw/leader member/) {
				my $output_file = "$logdir/$i/$file_name.cgi";
				open my $fh, "> $output_file" or &error("$output_file Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ‚Å‚µ‚½");
				close $fh;
				chmod $chmod, $output_file;
			}
			&add_npc_data($i);
			# create union file
			for my $j (1 .. $i-1) {
				my $file_name = "$logdir/union/${j}_${i}";
				$w{ "f_${j}_${i}" } = -99;
				$w{ "p_${j}_${i}" } = 2;
				next if -f "$file_name.cgi";
				open my $fh, "> $file_name.cgi" or &error("$file_name.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh;
				chmod $chmod, "$file_name.cgi";
				open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh2;
				chmod $chmod, "${file_name}_log.cgi";
				open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh3;
				chmod $chmod, "${file_name}_member.cgi";
			}
			unless (-f "$htmldir/$i.html") {
				open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html Ì§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
				close $fh_h;
			}
			$cs{name}[$i]     = $i == $w{country}-2 ? 'é°':
								$i == $w{country}-1 ? 'Œà':
													'å†';
			$cs{color}[$i]    = $i == $w{country}-2 ? '#4444ff':
								$i == $w{country}-1 ? '#ff4444':
													'#44ff44';
			$cs{member}[$i]   = 0;
			$cs{win_c}[$i]    = 999;
			$cs{tax}[$i]      = 99;
			$cs{strong}[$i]   = 50000;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = $max_c;
			$cs{is_die}[$i]   = 0;
			my @lines = &get_countries_mes();
			if ($w{country} > @lines - 3) {
				open my $fh9, ">> $logdir/countries_mes.cgi";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				print $fh9 "<>$default_icon<>\n";
				close $fh9;
			}
		}
		$migrate_type = 6;
		for my $i (1 .. $w{country}-3) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-2) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}elsif ($w{world} eq $#world_states-5) { # Ù‘¬
		$migrate_type = 4;
	}
	
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	
	&refresh;
	&n_menu;
	&write_cs;
	
	require "./lib/reset.cgi";
	&player_migrate($migrate_type);
}

sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]‘®«[1]•ŠíNo	[2]•KE‹Z
		['–³', [0],			[61..65],],
		['Œ•', [1 .. 5],	[1 .. 5],],
		['‘„', [6 ..10],	[11..15],],
		['•€', [11..15],	[21..25],],
		['‰Š', [16..20],	[31..35],],
		['•—', [21..25],	[41..45],],
		['—‹', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) ‹T‚Ì‰Æ’ëˆãŠw(NPC) pigure(NPC) ƒEƒFƒ‹(NPC) vipqiv(NPC) DT(NPC) ƒnƒ‹(NPC) ƒAƒVƒ…ƒŒƒC(NPC) ƒSƒ~ƒNƒY(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}

1; # íœ•s‰Â
