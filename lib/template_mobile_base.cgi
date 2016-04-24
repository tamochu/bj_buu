#================================================
# Œg‘Ñ¹Ş°Ñ‰æ–Ê Created by Merino
#================================================

#================================================
# Ò²İ
#================================================
print qq|‘‹à $m{money} G<br>| if $m{lib} =~ /^shopping/;
print qq|<a name="menu">$menu_cmd</a><br>$mes<br>|;

if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif ($m{lib} eq '') {
	&check_flag;
	&status_html;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}
elsif ($m{wt} > 0) {
	&check_flag;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
}


#================================================
# Ä¯ÌßÒÆ­°
#================================================
sub top_menu_html {
	print qq|<hr><a href="$script_index" accesskey="0">0.TOP</a>/| unless $m{disp_top} eq '0';
	print qq|<a href="./news.cgi?id=$id&pass=$pass" accesskey="1">1.‰ß‹‚Ì‰hŒõ</a>/| unless $m{disp_news} eq '0';
	print qq|<a href="./bbs_public.cgi?id=$id&pass=$pass" accesskey="2">2.Œf¦”Â</a>/|;
	print qq|<a href="./chat_public.cgi?id=$id&pass=$pass" accesskey="3">3.Œğ—¬Lê</a>/| unless $m{disp_chat} eq '0';
	print qq|<a href="./chat_horyu.cgi?id=$id&pass=$pass">‰ü‘¢ˆÄ“Š•[Š</a>/|;
	print qq|<a href="./bbs_ad.cgi?id=$id&pass=$pass" accesskey="4">4.é“`Œ¾”Â</a>/| unless $m{disp_ad} eq '0';
	print qq|<a href="./letter.cgi?id=$id&pass=$pass" accesskey="5">5.MyRoom</a>/|;
	print qq|<a href="./chat_prison.cgi?id=$id&pass=$pass" accesskey="7">7.˜S–</a>/|;
	print qq|<a href="./bbs_country.cgi?id=$id&pass=$pass" accesskey="8">8.ìí‰ï‹c</a>/|;
	print qq|<a href="./bbs_union.cgi?id=$id&pass=$pass" accesskey="9">9.“¯–¿‰ï‹c</a>/| if $union;
	print qq|<a href="./bbs_vs_npc.cgi?id=$id&pass=$pass" accesskey="6">6.+••ˆó‰ï‹c+</a>/| if ($w{world} eq $#world_states) && $m{country} ne $w{country};
#	print qq|<a href="./bbs_akindo.cgi?id=$id&pass=$pass" accesskey="*">*.ƒMƒ‹ƒh</a>/| if $m{akindo_guild};
	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		print $a_line;
		print qq|<a href="./chat_casino.cgi?id=$id&pass=$pass">‘Îl¶¼ŞÉ</a>/|;
	}
	print qq|<a href="./bbs_daihyo.cgi?id=$id&pass=$pass">‘ã•\\•]‹c‰ï</a>/| unless $m{disp_daihyo} eq '0';
	print qq|<a href="./chat_admin.cgi?id=$id&pass=$pass">‰^‰c“¢˜_ê</a>/| if (&is_sabakan);
}

#================================================
# ½Ã°À½‰æ–Ê
#================================================
sub status_html {
	print qq|<hr><img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|$m{name}<br>|;
	print qq|Ì† $m{shogo}<br>| if $m{shogo};
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|Œ‹¥‘Šè <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	if ($m{master}){
		if($m{master_c}){
			print qq|t  <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
		}else{
			$mid = unpack 'H*', $m{master};
			if (-f "$userdir/$mid/user.cgi") {
				$master = qq|’íq <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
			} else {
				$master = qq|’íq <font color="#FF0000">$m{master} €–S</font><br>|;
			}
		}
	}
	print qq|”æ˜J“x <b>$m{act}</b>%<br>|;
	print qq|Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>|;
	print qq|‘‹à <b>$m{money}</b> G<br>|;
	print qq|<font color="#CC9999">$e2j{hp} [<b>$m{hp}</b>/<b>$m{max_hp}</b>]</font><br>|;
	print qq|<font color="#CC99CC">$e2j{mp} [<b>$m{mp}</b>/<b>$m{max_mp}</b>]</font><br>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<font color="#9999CC">•Ší:[$weas[$m{wea}][2]]$wnameš<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>| if $m{wea};
	print qq|<font color="#9999CC">–h‹ï:[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>| if $m{gua};
	print qq|<font color="#99CCCC">Íß¯Ä:$pets[$m{pet}][1]š$m{pet_c}</font><br>| if $m{pet};
	print qq|<font color="#99CC99">ÀÏºŞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print qq|<font color="#CCCC99">’:$m{insect_name}</font><br>| if $m{insect_name};
}

#================================================
# è†A‰×•¨Áª¯¸
#================================================
sub check_flag {
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi";
		my $line = <$fh>;
		my($letters) = split /<>/, $line;
		close $fh;
		print qq|<hr><font color="#FFCC66">è†‚ª $letters Œ“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		print qq|<hr><font color="#FFCC00">—a‚©‚èŠ‚É‰×•¨‚ª“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		print qq|<font color="#FFCC99">Ï²Ù°Ñ‚É‰×•¨‚ª“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
	}
}

#================================================
# í“¬‰æ–Ê
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';
	
	$m_mes = qq|¢$m_mes£| if $m_mes;
	$y_mes = qq|¢$y_mes£| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">š</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">š</font>' : '';

	print "$m_icon$m{name}$m_mes<br>";
	print "$e2j{hp}(<b>$m{hp}</b>/<b>$m{max_hp}</b>)/$e2j{mp}(<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br>";
	print "UŒ‚[<b>$m_at</b>]/–hŒä[<b>$m_df</b>]/‘f‘[<b>$m_ag</b>]<br>";
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print "$m_tokkou•Ší:[$weas[$m{wea}][2]]$wnameš$m{wea_lv}($m{wea_c})<br>" if $m{wea};
	print "–h‹ï:[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>" if $m{gua};
	print "Íß¯Ä:$pets[$m{pet}][1]š$m{pet_c}<br>" if $pets[$m{pet}][2] eq 'battle';
	print "Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>";
	print "”æ˜J“x <b>$m{act}</b>%<br>";
	print qq|<font color="#99CC99">ÀÏºŞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print "<hr>";
	print "$y_icon$y{name}$y_mes<br>";
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	print "$e2j{hp}(<b>$y{hp}</b>/<b>$y{max_hp}</b>)/$e2j{mp}(<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br>";
	print "UŒ‚[<b>$y_at</b>]/–hŒä[<b>$y_df</b>]/‘f‘[<b>$y_ag</b>]<br>";
	print "$y_tokkou•Ší:[$weas[$y{wea}][2]]$ywname<br>" if $y{wea};
	print "–h‹ï:[$guas[$y{gua}][2]]$guas[$y{gua}][1]<br>" if $y{gua};
}

#================================================
# í‘ˆ‰æ–Ê
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';
	
	$m_mes = qq|¢$m_mes£| if $m_mes;
	$y_mes = qq|¢$y_mes£| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>š“ÁUš</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>š“ÁUš</b></font>' : '';
	
	print qq|$m_icon<font color="$cs{color}[$m{country}]">$m{name}$m_mes</font><br>|;
	print qq|$m_tokkou$units[$m{unit}][1]/<b>$m{sol}</b>•º/m‹C[<b>$m{sol_lv}</b>%]/“—¦[<b>$m{lea}</b>]<br>|;
	print qq|<hr>|;
	print qq|$y_icon<font color="$cs{color}[$y{country}]">$y{name}$y_mes</font><br>|;
	print qq|$y_tokkou$units[$y{unit}][1]/<b>$y{sol}</b>•º/m‹C[<b>$y{sol_lv}</b>%]/“—¦[<b>$y{lea}</b>]<br>|;
}

#================================================
# ©‘/“¯–¿‘‚Ìî•ñ
#================================================
sub my_country_info {
	my $next_rank = $m{rank} * $m{rank} * 10;
	my $nokori_time = $m{next_salary} - $time;
	$nokori_time = 0 if $nokori_time < 0;
	my $gacha_time = $m{gacha_time} - $time;
	$gacha_time = 0 if $gacha_time < 0;
	my $gacha_time2 = $m{gacha_time2} - $time;
	$gacha_time2 = 0 if $gacha_time2 < 0;
	my $offertory_time = $m{offertory_time} - $time;
	$offertory_time = 0 if $offertory_time < 0;

	my $rank_name = &get_rank_name($m{rank}, $m{name});
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= 'š' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	print qq|<hr>$rank_name $e2j{rank_exp} [<b>$m{rank_exp}/$next_rank</b>]<br>|;
	print qq|“G‘<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font>˜A‘±<b>$m{renzoku_c}</b>‰ñ<br>| if $m{renzoku_c};
	printf ("Ÿ‚Ì‹‹—^<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã<br>", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
	if ($m{disp_gacha_time}) {
		printf ("Ÿ‚ÌƒKƒ`ƒƒ<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã<br>", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		printf ("Ÿ‚ÌƒKƒ`ƒƒi‚‹‰j<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã<br>", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		printf ("Ÿ‚ÌæÎ‘K<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã<br>", $offertory_time / 3600, $offertory_time % 3600 / 60, $offertory_time % 60);
	}
	print qq|<hr><font color="$cs{color}[$m{country}]">$c_m</font><br>|;
	print qq|$e2j{strong}:$cs{strong}[$m{country}]<br>|;
	print qq|$e2j{tax}:$cs{tax}[$m{country}]%<br>|;
	print qq|$e2j{state}:$country_states[ $cs{state}[$m{country}] ]<br>|;
	print qq|$e2j{food}:$cs{food}[$m{country}]<br>|;
	print qq|$e2j{money}:$cs{money}[$m{country}]<br>|;
	print qq|$e2j{soldier}:$cs{soldier}[$m{country}]<br>|;

	if ($union) {
		print qq|<hr><font color="$cs{color}[$union]">$cs{name}[$union]</font><br>|;
		print qq|$e2j{strong}:$cs{strong}[$union]<br>|;
		print qq|$e2j{tax}:$cs{tax}[$union]%<br>|;
		print qq|$e2j{state}:$country_states[ $cs{state}[$union] ]<br>|;
		print qq|$e2j{food}:$cs{food}[$union]<br>|;
		print qq|$e2j{money}:$cs{money}[$union]<br>|;
		print qq|$e2j{soldier}:$cs{soldier}[$union]<br>|;
	}
}

#================================================
# Še‘‘—Í‚Ìî•ñ
#================================================
sub countries_info {
	print  "<hr>Še‘‚Ì$e2j{strong}<br>";
	for my $i (1 .. $w{country}) {
		print qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		my $status = $cs{strong}[$i];
		if ($cs{is_die}[$i] == 1) {
			$status = "–Å–S";
		}
		elsif ($cs{is_die}[$i] == 2) {
			$status = "••½";
		}
		elsif ($cs{is_die}[$i] == 3) {
			$status = "•ö‰ó";
		}
		print $w{world} eq '10' ? '' : $status;

#		print $w{world} eq '10' ? ''
#			: $cs{is_die}[$i]   ? "–Å–S"
#			:                     "$cs{strong}[$i]"
#			;
		
		if ($m{country} && $m{country} ne $i) {
			my $c_c = &union($m{country}, $i);
			print qq|[$w{'f_'.$c_c}%]|;
			if   ($w{'p_'.$c_c} eq '1') { print qq|<font color="#009900">“¯–¿</font>|; }
			elsif($w{'p_'.$c_c} eq '2') { print qq|<font color="#FF0000">Œğí</font>|; }
		}
		print "<br>";
	}

	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . 'ŠÔ' : int($limit_hour / 24) . '“ú';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>ŠÔ<b>%02d</b>•ª<b>%02d</b>•bŒã", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<hr><font color="#FF0000">œ</font>| : qq|<hr><font color="#00FF00">œ</font>|;
	print qq|ÌßÚ²’† $w{playing}/$max_playingl|;
	print qq|<hr>“ˆêŠúŒÀ c‚è$limit_day<br>|;
	if ($reset_rest > 0){
		print qq|IíŠúŠÔyc‚è$reset_time_mesz<br>|;
	}
	print qq|“ïˆÕ“x Lv.$w{game_lv}<br>“ˆê$e2j{strong} $touitu_strong<br>| unless $w{world} eq '10';
	print $c2 ? qq|“ˆê‘ <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>“¯–¿<br>|
		: $c1 ? qq|“ˆê‘ <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><br>|
		:       ''
		;
	print qq|¢ŠEî¨ <a href="world_summaries.cgi?id=$id&pass=$pass&world=$w{world}" style="color:inherit;text-decoration:none;">$world_states[$w{world}]</a><br>|;
	print qq|$world_name—ï$w{year}”N<br>|;
}

#================================================
# ¶¼ŞÉ‚Ìl”
#================================================
sub all_member_n {
	my $ret_str = '';
	for my $i (0 .. $#files) {
		my $member_c  = 0;
		my %sames = ();
		my $tf_name = "$logdir/chat_casino$files[$i][2]_member.cgi";
	
		open my $fh, "< $tf_name" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
		my $head_line = <$fh>;
		while (my $line = <$fh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
			if ($time - 60 > $mtime) {
				next;
			}
			next if $sames{$mname}++; # “¯‚¶l‚È‚çŸ
			
			$member_c++;
		}
		close $fh;
		$ret_str .= substr($files[$i][0], 0, 2) . "/$member_c ";
		$ret_str .= "<br>" if $i % 4 == 3;
	}
	return $ret_str;
}

1; # íœ•s‰Â
