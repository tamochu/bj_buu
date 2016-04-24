sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
require './lib/reset.cgi';
#require './lib/_world_reset.cgi';
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
	if (&is_special_world) { # “Áêî¨‚ÌŠJn
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # ‰p—Y
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í‰p—Y‚ª“`à‚ğì‚èo‚·‘ã‚É‚È‚è‚Ü‚µ‚½</i>");
		}
		elsif ($w{year} =~ /6$/) { # ˆÃ•
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‚©‚«Á‚³‚ê‚Ü‚µ‚½</i>");
		}
		elsif ($w{year} % 40 == 0) { # •s‹ä‘Õ“V
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í“ñ‚Â‚É•ª‚©‚ê‚Ü‚µ‚½</i>");
		}
		elsif ($w{year} % 40 == 20) { # O‘u
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­•ª—ô‚µ‚½¢ŠE‚ğ“ˆê‚·‚×‚­O‘‚ª‘ä“ª‚µ‚Ü‚µ‚½</i>");
		}
		elsif ($w{year} % 40 == 10) { # Ù‘¬
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚à‹ó‚µ‚­¢ŠE‚ª‹£‚¢‡‚¤‚±‚Æ‚É</i>");
		}
		else { # ¬—
			&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‹ó‚µ‚­¢ŠE‚Í¬—‚ÉŠ×‚è‚Ü‚µ‚½</i>");
		}
	}
	else { # “Áêî¨ˆÈŠO‚ÌŠJn
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

		($w{world}, $w{world_sub}) = &choice_unique_world(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);

#		my @next_worlds = &unique_worlds(@new_worlds);
#		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# “¯‚¶‚Ì‚¶‚á‚Â‚Ü‚ç‚È‚¢‚Ì‚Å
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>¢ŠE‚Í $world_states[$old_world] ‚Æ‚È‚è‚Üc‚¹‚ñ $world_states[$w{world}]‚Æ‚È‚è‚Ü‚µ‚½</i>");
		}
		&begin_common_world;
#		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else { # “Áêî¨ˆÈŠO‚ÌŠJn
	&add_world_log($w{world});
#	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
#	my $saved_w = 0;
#	$nline = "";
#	for my $old_w (@old_worlds){
#		next if $old_w =~ /[^0-9]/;
#		$nline .= "$old_w<>";
#		last if $saved_w > 15;
#		$saved_w++;
#	}
#	print $fh "$w{world}<>$nline\n";
#	close $fh;

#	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;
}

1; # íœ•s‰Â