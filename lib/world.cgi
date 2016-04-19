sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
#require './lib/reset.cgi';
require './lib/_world_reset.cgi';
#================================================
# ¢ŠEî¨ Created by Merino
#================================================

#================================================
# ‘I‘ğ‰æ–Ê
#================================================
sub tp_100 {
	# “ˆêworld‚ÆŠúŒÀØ‚êreset‚Å‘Î‚É‚µ‚½‚©‚Á‚½‚ª“ˆêÒ‚Ì‰æ–Ê‚É‚à•\¦‚·‚é‚½‚ß’f”O
	# “Áêî¨‚É‚¨‚¯‚é“ˆê‚Ì•¶Œ¾‚Í _war_result.cgi ‚ğ‘‚«Š·‚¦‚é

	# Õ‚èî¨‚É“ˆê
#	if (&is_festival_world) {
#		if ($w{world} eq $#world_states-1) { # ¬—
#			$migrate_type = &festival_type('konran', 0);
#		}
#		elsif ($w{world} eq $#world_states-2) { # •s‹ä‘Õ“V
#			$migrate_type = &festival_type('kouhaku', 0);
#			$w{country} -= 2;
#		}
#		elsif ($w{world} eq $#world_states-3) { # O‘u
#			$migrate_type = &festival_type('sangokusi', 0);
#			$w{country} -= 3;
#		}
#		&player_migrate($migrate_type);
#	}

#	&reset;

	$mes .= "‚ ‚È‚½‚Í‚±‚Ì¢ŠE‚É‰½‚ğ‹‚ß‚Ü‚·‚©?<br>";
	&menu('ŠF‚ª–]‚Ş‚à‚Ì','Šó–]','â–]','•½˜a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	&show_desire;
	if (&is_special_world) { # “Áêî¨‚ÌŠJn
		if ($w{year} =~ /6$/) { # ˆÃ•E‰p—Y
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‚©‚«Á‚³‚ê‚Ü‚µ‚½</i>");
		}
		elsif ($year % 40 == 0) { # •s‹ä‘Õ“V
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í“ñ‚Â‚É•ª‚©‚ê‚Ü‚µ‚½</i>");
		}
		elsif ($year % 40 == 20) { # O‘u
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­•ª—ô‚µ‚½¢ŠE‚ğ“ˆê‚·‚×‚­O‘‚ª‘ä“ª‚µ‚Ü‚µ‚½</i>");
		}
		elsif ($year % 40 == 10) { # Ù‘¬
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­¢ŠE‚ª‹£‚¢‡‚¤‚±‚Æ‚É</i>");
		}
		else { # ¬—
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í¬—‚ÉŠ×‚è‚Ü‚µ‚½</i>");
		}
	}
	else (!$w{year} =~ /5$) { # “Áêî¨ˆÈŠO‚ÌŠJn
		my @new_worlds;
		if ($cmd eq '1') { # Šó–]
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') { # â–]
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') { # •½˜a
			@new_worlds = (0);
		}
		else {
			@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
		my @next_worlds = &unique_worlds(@new_worlds);
		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# “¯‚¶‚Ì‚¶‚á‚Â‚Ü‚ç‚È‚¢‚Ì‚Å
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>¢ŠE‚Í $world_states[$old_world] ‚Æ‚È‚è‚Üc‚¹‚ñ $world_states[$w{world}]‚Æ‚È‚è‚Ü‚µ‚½</i>");
		}
		else {
			if ($w{world} eq '0') { # •½˜a
#				Unrecognized character \x90; marked by <-- HERE after
				&write_world_news('<i>¢ŠE‚Í '.$world_states[$w{world}].' ‚É‚È‚è‚Ü‚µ‚½</i>');
			}
			elsif ($w{world} eq '18') { # E”°
				&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚µ‚½‚Ó‚¢‚ñ‚«(©‚È‚º‚©•ÏŠ·‚Å‚«‚È‚¢)‚É‚È‚è‚Ü‚µ‚½</i>");
			}
			else {
				&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
			}
		}
		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else { # “Áêî¨ˆÈŠO‚ÌŠJn

#	require './lib/reset.cgi';
#	&reset; # ‚±‚±‚Ü‚Å¡Šú“ˆê‚Ìˆ—

#	my $migrate_type = 0;
	# ¢ŠEî¨ ¬—“Ë“ü
#		&show_desire;
#	}
#	elsif ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		$migrate_type = &opening_festival;
#		&wt_c_reset;
#	}

#	unshift @old_worlds, $w{world};
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

#	my $migrate_type = 0;
	&opening_common;
#	elsif (&is_festival_world) { # Õ‚èî¨‚È‚ç‚Î
#		if ($w{world} eq $#world_states-1) { # ¬—
#			$migrate_type = &festival_type('konran', 1);
#		}
#		elsif ($w{world} eq $#world_states-2) { # •s‹ä‘Õ“V
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('kouhaku');
#		}
#		elsif ($w{world} eq $#world_states-3) { # O‘u
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('sangokusi');
#		}
#		elsif ($w{world} eq $#world_states-4) { # ‰p—Y
#			$w{game_lv} += 20;
#			for my $i (1 .. $w{country}) {
#				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#			}
#		}
#		elsif ($w{world} eq $#world_states-5) { # Ù‘¬
#			$migrate_type = &festival_type('sessoku', 1);
#		}
#	}

	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;

#	require "./lib/reset.cgi";
#	&player_migrate($migrate_type);
#	&player_migrate($migrate_type) if &is_festival_world;
}

# ƒvƒŒƒCƒ„[‚Ì–]‚İ‚ğ•\¦‚·‚é
sub show_desire {
	if ($cmd eq '1') { # Šó–]
		&mes_and_world_news("<b>¢ŠE‚ÉŠó–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
	}
	elsif ($cmd eq '2') { # â–]
		&mes_and_world_news("<b>¢ŠE‚Éâ–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
	}
	elsif ($cmd eq '3') { # •½˜a
		&mes_and_world_news("<b>¢ŠE‚É•½˜a‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
	}
	else {
		&mes_and_world_news('<b>¢ŠE‚É‚İ‚È‚ª–]‚Ş‚à‚Ì‚ğ–]‚İ‚Ü‚µ‚½</b>', 1);
	}
}

1; # íœ•s‰Â