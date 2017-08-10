#================================================
# Œg‘Ñ¹Ş°Ñ‰æ–Ê Created by Merino
#================================================

#================================================
# Ò²İ
#================================================
print qq|‘‹à $m{money} G<br>| if $m{lib} =~ /^shopping/ || $m{lib_r} =~ /^shopping/;
#if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
if ($m{lib_r} eq '' && ($mes && $m{wt} > 1) || (!$mes && $m{lib} eq '') ) {
#if (!$mes && ($is_battle ne 1 && $is_battle ne 2) ) {
	# ÅVî•ñ
	open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	print qq|<hr>|;
	print qq|ÅVî•ñ<br>$line|;
	# Á­°ÄØ±ÙÓ°ÄŞ‚Ì¸´½Äî•ñ
	if ($m{tutorial_switch}) {
		require './lib/tutorial.cgi';
		if ($m{country} == 0) { # ÈÊŞ×İ‚Å‚ÍdŠ¯Ã‘£ŒÅ’è
			print qq|<hr>Á­°ÄØ±Ù<br>|;
			print qq|u‘î•ñv¨udŠ¯v‚©‚ç‘‚ğ‘I‚Ô‚±‚Æ‚ÅdŠ¯‚Å‚«‚Ü‚·|;
		}
		elsif ($m{tutorial_quest_stamp_c} < $tutorial_quest_stamps) {
			print qq|<hr>¸´½Äî•ñ<br>|;
			my $quest = &show_quest;
			print qq|$quest$tutorial_mes|;
		}
	}
	print qq|<hr>|;
}
#print qq|<a name="menu">$menu_cmd</a><br>$mes<br>|;
print qq|$menu_cmd|;
print qq|<br>| unless $menu_cmd;
print qq|$mes$tutorial_mes| if $mes;

if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif ($m{lib} eq '' || $m{lib} eq 'prison') {
	&check_flag;
	&status_html;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
	&promise_table_html;
}
elsif ($m{wt} > 0) {
	&check_flag;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
	&promise_table_html;
}
elsif ($m{lib} =~ /(domestic|hunting|military|promise|training|war_form)/ && $m{tp} eq '1') {
	print qq|<hr>|;
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">Íß¯Ä:$pets[$m{pet}][1]š$m{pet_c}</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">Íß¯Ä:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)</font><br>|; }
	print qq|<font color="#99CC99">ÀÏºŞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
}
#================================================
# Ä¯ÌßÒÆ­°
#================================================
sub top_menu_html {
	print qq|<hr>|;
if (&is_sabakan) {
	my @country_menus = (
		[$script_index, "‚s ‚n ‚o", "disp_top"] ,
		["news.cgi", "‰ß‹‚Ì‰hŒõ", "disp_news"] ,
		["bbs_public.cgi", "Œf¦”Â", ""] ,
		["", "", ""] ,
		["chat_public.cgi", "Œğ—¬Lê", "disp_chat"] ,
		["chat_horyu.cgi", "‰ü‘¢ˆÄ“Š•[Š", ""] ,
		["bbs_ad.cgi", "é“`Œ¾”Â", "disp_ad"] ,
		["letter.cgi", "‚l‚™ ‚q‚‚‚", ""] ,
		["chat_prison.cgi", "˜S–", ""] ,
		["bbs_country.cgi", "ìí‰ï‹cº", ""] ,
		["bbs_union.cgi", "“¯–¿‰ï‹cº", ""] ,
		["bbs_vs_npc.cgi", "••ˆó‰ï‹cº", ""] ,
		["bbs_daihyo.cgi", "‘ã•\\•]‹c‰ï", "disp_daihyo"] ,
		["chat_casino.cgi", "‘Îl¶¼ŞÉ", ""] ,
		["chat_admin.cgi", "‰^‰c“¢˜_ê", ""],
		["", "", ""]
	);

	# 4x4 ‚ÌÄ¯ÌßÒÆ­°
	print qq|<div class="menu_table">|;
	for my $i (0 .. $#country_menus) {
		print qq|<div class="menu_parent_table">| if ($i) % 4 == 0;

		unless ( (($country_menus[$i][1] eq "“¯–¿‰ï‹cº") && !$union) ||
			(($country_menus[$i][1] eq "••ˆó‰ï‹cº") && ($w{world} != $#world_states) || ($m{country} == $w{country})) ||
			(($country_menus[$i][1] eq "‰^‰c“¢˜_ê") && !&is_sabakan) ) {

			if ($country_menus[$i][0]) {
				if ( !$country_menus[$i][2] || ($country_menus[$i][2] && $m{$country_menus[$i][2]}) ) {
					print qq|<div class="menu_child_table">|;
					print qq|<form method="$method" action="$country_menus[$i][0]" class="cmd_form">|;
					print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">| if $i;
					print qq|</form>|;
#					$button_count++;
					print "</div>";
				}
			}
		}

		print "</div>" if ($i+1) % 4 == 0;
	}
	print qq|</div>|;
}

=pod
	my $button_count = 0;
	print qq|<div>|;
	for my $i (0 .. $#country_menus) {
		# Ä¯ÌßÍß°¼Ş
		if ($i == 0) {
			if ($m{$country_menus[$i][2]}) {
				print qq|<form method="$method"  action="$country_menus[$i][0]" class="cmd_form">|;
				print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
				print qq|</form>|;
				$button_count++;
			}
		}
		elsif ($country_menus[$i][1] eq "“¯–¿‰ï‹cº") {
			if ($union) {
				print qq|<form method="$method" action="$country_menus[$i][0]" class="cmd_form">|;
				print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				print qq|</form>|;
				$button_count++;
			}
		}
		elsif ($country_menus[$i][1] eq "••ˆó‰ï‹cº") {
			if ( ($w{world} eq $#world_states) && ($m{country} ne $w{country}) ) {
				print qq|<form method="$method" action="$country_menus[$i][0]" class="cmd_form">|;
				print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				print qq|</form>|;
				$button_count++;
			}
		}
		elsif ($country_menus[$i][1] eq "‰^‰c“¢˜_ê") {
			if (&is_sabakan) {
				print qq|<form method="$method" action="$country_menus[$i][0]" class="cmd_form">|;
				print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				print qq|</form>|;
				$button_count++;
			}
		}
		# ‹­§‚©ŒÂlİ’è‚Å•\¦‚Éİ’è‚µ‚Ä‚¢‚éê‡‚É‚¾‚¯•\¦
		else {
			if ( !$country_menus[$i][2] || ($country_menus[$i][2] && $m{$country_menus[$i][2]}) ) {
				print qq|<form method="$method" action="$country_menus[$i][0]" class="cmd_form">|;
				print qq|<input type="submit" value="$country_menus[$i][1]" class="button2s">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				print qq|</form>|;
				$button_count++;
			}
		}
		if ($i < $#country_menus) {
			print qq|<br class="smart_br" />| if ($button_count) % 4 == 0;
			print qq|<br class="tablet_br" />| if ($button_count) % 7 == 0;
		}
	}
	# ‘Îl¶¼ŞÉ‚Ìl”
	if ($m{disp_casino}) {
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		print qq|<br>$a_line|;
	}
	print qq|</div>|;
=cut
=pod
	print qq|<form action="$script_index" class="cmd_form">|;
	print qq|<input type="submit" value="‚s ‚n ‚o" class="button2s">|;
	print qq|</form>|;

	unless ($m{disp_news} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="news.cgi">|;
		print qq|<input type="submit" value="‰ß‹‚Ì‰hŒõ" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}

	print qq|<form method="$method" action="bbs_public.cgi">|;
	print qq|<input type="submit" value="Œf ¦ ”Â" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;

	unless ($m{disp_chat} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="chat_public.cgi">|;
		print qq|<input type="submit" value="Œğ—¬Lê" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}

	print qq|<form method="$method" action="chat_horyu.cgi">|;
	print qq|<input type="submit" value="‰ü‘¢ˆÄ“Š•[Š" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;

	unless ($m{disp_ad} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="bbs_ad.cgi">|;
		print qq|<input type="submit" value="é“`Œ¾”Â" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}

	$country_menu .= qq|<tr><td><form method="$method" action="chat_prison.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="˜S–" class="button1s"></form></td>|;

	$country_menu .= qq|<td><form method="$method" action="bbs_country.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="ìí‰ï‹cº" class="button1s"></form></td>|;

	if ($union) {
		$country_menu .= qq|<td><form method="$method" action="bbs_union.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="“¯–¿‰ï‹cº" class="button1s"></form></td>|;
	}

	# ¢ŠEî¨ˆÃ•‚Ì‚İ
	if (($w{world} eq $#world_states) && $m{country} ne $w{country}) {
		$country_menu .= qq|<td><form method="$method" action="bbs_vs_npc.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="{ •• ˆó ‰ï ‹c {" class="button1s"></form></td>|;
	}

	$country_menu .= qq|<td><form method="$method" action="chat_casino.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="‘Îl¶¼ŞÉ" class="button1s"></form></td>|;
	
	unless ($m{disp_daihyo} eq '0'){
		$country_menu .= qq|<td><form method="$method" action="bbs_daihyo.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="‘ã•\\•]‹c‰ï" class="button1s"></form></td>|;
	}
	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		$country_menu .= qq|</tr><tr><td colspan=3>$a_line</td>|;
	}

	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="submit" value="‚l‚™ ‚q‚‚‚" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;

	if (&is_sabakan){
		$country_menu .= qq|<td>|;
		$country_menu .= qq|<form method="$method" action="chat_admin.cgi">|;
		$country_menu .= qq|<input type="submit" value="‰^‰c“¢˜_ê" class="button1s">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|</form>|;
		$country_menu .= qq|</td>|;
	}


			$menu_cmd .= qq|<form method="$method" action="$script" class="cmd_form">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button2s"><input type="hidden" name="cmd" value="$i">|;
#			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
#			print "$i ", ($i+1) % 4, " " , ($i+1) % 6, "<br>";

#			$menu_cmd .= qq|</div>| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
			$menu_cmd .= qq|<br class="smart_br" />| if ($i+1) % 4 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr" />| if ($i+1) % 4 == 0;
			$menu_cmd .= qq|<br class="tablet_br" />| if ($i+1) % 7 == 0;
=cut

	my $country_menu = '';
	$country_menu .= qq|<tr><td><form method="$method" action="chat_prison.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="˜S–" class="button1s"></form></td>|;
	$country_menu .= qq|<td><form method="$method" action="bbs_country.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="ìí‰ï‹cº" class="button1s"></form></td>|;

	# “¯–¿‘‚ª‚ ‚é‚È‚ç
	if ($union) {
		$country_menu .= qq|<td><form method="$method" action="bbs_union.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="“¯–¿‰ï‹cº" class="button1s"></form></td>|;
	}
	$country_menu .= qq|</tr>|;

	$country_menu .= qq|<tr>|;

	# ¢ŠEî¨ˆÃ•‚Ì‚İ
	if (($w{world} eq $#world_states) && $m{country} ne $w{country}) {
		$country_menu .= qq|<td><form method="$method" action="bbs_vs_npc.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="{ •• ˆó ‰ï ‹c {" class="button1s"></form></td>|;
	}

	# ƒMƒ‹ƒh‰Á–¿‚È‚ç
#	if ($m{akindo_guild}) {
#		$country_menu .= qq|<td><form method="$method" action="bbs_akindo.cgi">|;
#		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$country_menu .= qq|<input type="submit" value="ƒMƒ‹ƒh" class="button1s"></form></td>|;
#	}
	
	$country_menu .= qq|<td><form method="$method" action="chat_casino.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="‘Îl¶¼ŞÉ" class="button1s"></form></td>|;
	
	unless ($m{disp_daihyo} eq '0'){
		$country_menu .= qq|<td><form method="$method" action="bbs_daihyo.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="‘ã•\\•]‹c‰ï" class="button1s"></form></td>|;
	}
	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		$country_menu .= qq|</tr><tr><td colspan=3>$a_line</td>|;
	}

	if (&is_sabakan){
		$country_menu .= qq|<td>|;
		$country_menu .= qq|<form method="$method" action="chat_admin.cgi">|;
		$country_menu .= qq|<input type="submit" value="‰^‰c“¢˜_ê" class="button1s">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|</form>|;
		$country_menu .= qq|</td>|;
	}
	
	$country_menu .= qq|</tr>|;

	print qq|<table boder=0 cols=5 width=90 height=90>|;
	print qq|<tr>|;
	print qq|<td>|;
	print qq|<form action="$script_index">|;
	print qq|<input type="submit" value="‚s ‚n ‚o" class="button1s">|;
	print qq|</form>|;
	print qq|</td>|;
	unless ($m{disp_news} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="news.cgi">|;
		print qq|<input type="submit" value="‰ß‹‚Ì‰hŒõ" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="bbs_public.cgi">|;
	print qq|<input type="submit" value="Œf ¦ ”Â" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	print qq|</tr>|;
	print qq|<tr>|;
	unless ($m{disp_chat} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="chat_public.cgi">|;
		print qq|<input type="submit" value="Œğ—¬Lê" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="chat_horyu.cgi">|;
	print qq|<input type="submit" value="‰ü‘¢ˆÄ“Š•[Š" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	unless ($m{disp_ad} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="bbs_ad.cgi">|;
		print qq|<input type="submit" value="é“`Œ¾”Â" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="submit" value="‚l‚™ ‚q‚‚‚" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	print qq|</tr>|;
	print qq|$country_menu|;
	print qq|</table>|;

	print qq|<hr>|;
}

#================================================
# ½Ã°À½‰æ–Ê
#================================================
sub status_html {
	print qq|<hr><img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|<img src="$icondir/pet/$m{icon_pet}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon_pet} && $m{pet_icon_switch};
	print qq|$m{name}|;
	print qq|[$m{shogo}]| if $m{shogo};
	print qq|<br>|;
#	print qq|Ì† $m{shogo}<br>| if $m{shogo};
#	print $m{name}, "[$m{shogo}]<br>";

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
	if($m{country} && $m{wt} <= 0){
		my $next_rank = $m{rank} * $m{rank} * 10;
		my $nokori_time = $m{next_salary} - $time;
		$nokori_time = 0 if $nokori_time < 0;
		my $nokori_time_mes = sprintf("<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
		my $reset_rest = int($w{reset_time} - $time);
		my $gacha_time = $m{gacha_time} - $time;
		$gacha_time = 0 if $gacha_time < 0;
		my $gacha_time_mes = sprintf("<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		my $gacha_time2 = $m{gacha_time2} - $time;
		$gacha_time2 = 0 if $gacha_time2 < 0;
		my $gacha_time2_mes = sprintf("<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		my $offertory_time = $m{offertory_time} - $time;
		$offertory_time = 0 if $offertory_time < 0;
		my $offertory_time_mes = sprintf("<b>%d</b><b>%02d</b>•ª<b>%02d</b>•bŒã", $offertory_time / 3600, $offertory_time % 3600 / 60, $ofertory_time % 60);

#		print qq|<hr size="1">|;
		print qq|$units[$m{unit}][1] <b>$rank_sols[$m{rank}]</b>•º<br>|;
		my $rank_name = &get_rank_name($m{rank}, $m{name});
		if ($m{super_rank}){
			$rank_name = '';
			$rank_name .= 'š' for 1 .. $m{super_rank};
			$rank_name .= $m{rank_name};
		}
		print qq|$rank_name $e2j{rank_exp} [ <b>$m{rank_exp}</b> / <b>$next_rank</b> ]<br>|;
		print qq|“G‘[‘O‰ñF<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> ˜A‘±<b>$m{renzoku_c}</b>‰ñ]<br>| if $m{renzoku_c};
		print qq|<hr size="1">|;
		if ($m{disp_gacha_time}) {
#			print qq|c‚èŠÔ<br>\n|;
			print qq|<table class="table1s">|;
			print qq|<tr><th>‹‹—^</th><th>æÎ‘K</th></tr>\n|;
			print qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td><td><span id="offertory_time">$offertory_time_mes</span></td></tr>\n|;
			print qq|<tr><th>ƒKƒ`ƒƒ</th><th>ƒKƒ`ƒƒi‚j</th></tr>\n|;
			print qq|<tr><td><span id="gacha_time">$gacha_time_mes</span></td><td><span id="gacha_time2">$gacha_time2_mes</span></td></tr>\n|;
			print qq|</table>|;
		} else {
			print qq|‹‹—^‚Ü‚Åc‚è <span id="nokori_time">$nokori_time_mes</span>\n|;
		}
		print qq|<script type="text/javascript"><!--\n nokori_time($nokori_time, $reset_rest, $gacha_time, $gacha_time2, $offertory_time);\n// --></script>\n|;
		print qq|<br>|;
	}
	print qq|<b>$m{sedai}</b>¢‘ã–Ú $sexes[$m{sex}]<br>|;
	print qq|Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>|;
	print qq|”æ˜J“x <b>$m{act}</b>%<br>|;
	print qq|ŒoŒ±’l [<b>$m{exp}</b>/<b>100</b>]<br>|;
#	print qq|Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>|;
	print qq|‘‹à <b>$m{money}</b> G<br>|;
	print qq|ŒMÍ<b>$m{medal}</b>ŒÂ<br>|;
	print qq|º²İ <b>$m{coin}</b>–‡<br>|;
	print qq|•ó¸¼Şy$m{lot}z<br>|;
	print qq|<font color="#CC9999">$e2j{hp} [<b>$m{hp}</b>/<b>$m{max_hp}</b>]</font><br>|;
	print qq|<font color="#CC99CC">$e2j{mp} [<b>$m{mp}</b>/<b>$m{max_mp}</b>]</font><br>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<font color="#9999CC">•Ší:[$weas[$m{wea}][2]]$wnameš<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>| if $m{wea};
	print qq|<font color="#9999CC">–h‹ï:[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>| if $m{gua};
	my $icon_pet_lv = " Lv.<b>$m{icon_pet_lv}</b>" if $m{icon_pet} && $m{pet_icon_switch};
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">Íß¯Ä:$pets[$m{pet}][1]š$m{pet_c}$icon_pet_lv</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">Íß¯Ä:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)$icon_pet_lv</font><br>|; }
	print qq|<font color="#99CC99">ÀÏºŞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print qq|<font color="#CCCC99">’  :$m{insect_name}</font><br>| if $m{insect_name};
#	print qq|<hr>|;
}

#================================================
# è†A‰×•¨Áª¯¸
#================================================
sub check_flag {
	if (-f "$userdir/$id/temp_mes.cgi") {
		open my $fh, "< $userdir/$id/temp_mes.cgi";
		my $line = <$fh>;
		close $fh;
		print qq|<hr><font color="#FF0000">$line</font><br>|;
	}
	if ($m{tutorial_switch}) {
		print qq|<hr><font color="#FF0000">Á­°ÄØ±ÙÓ°ÄŞ</font><br>|;
	}
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
	my $is_breeder_find = 0;
	for my $bi (0 .. 2) {
		if (-f "$userdir/$id/shopping_breeder_$bi.cgi") {
			if ((stat "$userdir/$in{id}/shopping_breeder_$bi.cgi")[9] < $time) {
				$is_breeder_find = 1;
			}
		}
	}
	print qq|<font color="#FF66CC">ˆç‚Ä‰®‚Ì—‘‚ª›z‰»‚µ‚Ä‚¢‚Ü‚·</font><br>| if $is_breeder_find;
}

#================================================
# í“¬‰æ–Ê
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';

	my $m_hp_par = $m{max_hp} <= 0 ? 0 :
				$m{hp} > $m{max_hp} ? 100 : int($m{hp} / $m{max_hp} * 100);
	my $y_hp_par = $y{max_hp} <= 0 ? 0 :
				$y{hp} > $y{max_hp} ? 100 :int($y{hp} / $y{max_hp} * 100);
	my $m_mp_par = $m{max_mp} <= 0 ? 0 :
				$m{mp} > $m{max_mp} ? 100 : int($m{mp} / $m{max_mp} * 100);
	my $y_mp_par = $y{max_mp} <= 0 ? 0 :
				$y{mp} > $y{max_mp} ? 100 : int($y{mp} / $y{max_mp} * 100);
	my $fuka = !$m{egg} ? 0 :
				int($m{egg_c} / $eggs[$m{egg}][2] * 100) > 100 ? 100 : int($m{egg_c} / $eggs[$m{egg}][2] * 100);
	my $exp = $m{exp} > 100 ? 100 : $m{exp};

	$m_mes = qq|¢$m_mes£| if $m_mes;
	$y_mes = qq|¢$y_mes£| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">š</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">š</font>' : '';
	my $m_tokkou2 = $is_m_tokkou2 ? '<font color="#FFFF00">š</font>' : '';
	my $y_tokkou2 = $is_y_tokkou2 ? '<font color="#FFFF00">š</font>' : '';

	print qq|$m_icon $m{name} $m_mes<br>|;
	print qq|<table border="0">|;
	print qq|<tr><td>$e2j{max_hp}F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_hp_par%"></div></td><td> (<b>$m{hp}</b>/<b>$m{max_hp}</b>)<br></td></tr>|;
	print qq|<tr><td>$e2j{max_mp}F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m_mp_par%"></div></td><td> (<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br></td></tr>|;
	print qq|<tr><td colspan="3">UŒ‚—Í [ <b>$m_at</b> ] / –hŒä—Í [ <b>$m_df</b> ] / ‘f‘‚³[ <b>$m_ag</b> ]<br></td></tr>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<tr><td colspan="3">$m_tokkou•ŠíF[$weas[$m{wea}][2]] $wnameš$m{wea_lv} ($m{wea_c})<br></td></tr>| if $m{wea};
	print qq|<tr><td colspan="3">$m_tokkou2–h‹ïF[$guas[$m{gua}][2]] $guas[$m{gua}][1]<br></td></tr>| if $m{gua};
	print qq|<tr><td colspan="3">Íß¯ÄF$pets[$m{pet}][1]š$m{pet_c}<br></td></tr>| if $pets[$m{pet}][2] eq 'battle';
	print qq|<tr><td>$e2j{exp}F</td><td><div class="bar4"><img src="$htmldir/space.gif" style="width: $exp%"></div></td><td> (<b>$m{exp}</b>/<b>100</b>)<br></td></tr>|;
	print qq|<tr><td>$eggs[$m{egg}][1]F</td><td><div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div></td><td> (<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)<br></td></tr>|;
	print qq|<tr><td>”æ˜J“xF</td><td><div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $m{act}%"></div></td><td> (<b>$m{act}</b>/<b>100</b>)<br></td></tr>|;
	print qq|</table>@ VS<br>|;
	
	print qq|$y_icon $y{name} $y_mes<br>|;
	print qq|<table border="0">|;
	print qq|<tr><td>$e2j{max_hp}F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_hp_par%"></div></td><td> (<b>$y{hp}</b>/<b>$y{max_hp}</b>)<br></td></tr>|;
	print qq|<tr><td>$e2j{max_mp}F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y_mp_par%"></div></td><td> (<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br></td></tr>|;
	print qq|<tr><td colspan="3">UŒ‚—Í [ <b>$y_at</b> ] / –hŒä—Í [ <b>$y_df</b> ] / ‘f‘‚³[ <b>$y_ag</b> ]<br></td></tr>|;
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	print qq|<tr><td colspan="3">$y_tokkou•ŠíF[$weas[$y{wea}][2]] $ywname<br></td></tr>| if $y{wea};
	print qq|<tr><td colspan="3">$y_tokkou2–h‹ïF[$guas[$y{gua}][2]] $guas[$y{gua}][1]<br></td></tr>| if $y{gua};
	print qq|</table>|;
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
	print qq|$m_tokkou$units[$m{unit}][1]/<b>$m{sol}</b>•º/m‹C[<b>$m{sol_lv}</b>%]/“—¦[<b>$m_lea</b>]<br>|;
	print qq|<hr>|;
	print qq|$y_icon<font color="$cs{color}[$y{country}]">$y{name}$y_mes</font><br>|;
	print qq|$y_tokkou$units[$y{unit}][1]/<b>$y{sol}</b>•º/m‹C[<b>$y{sol_lv}</b>%]/“—¦[<b>$y_lea</b>]<br>|;
}

#================================================
# ©‘/“¯–¿‘‚Ìî•ñ
#================================================
sub my_country_info {
	print qq|<hr>| if $m{country};
	print qq|<div class="c_infos">|;

	print qq|<div class="c_info">|;
	print qq|<span style="color: $cs{color}[$m{country}];">$c_m</span>|;
	print qq|<div class="c_info1p">|;
	print qq|<div class="c_info1c">$e2j{strong}:$cs{strong}[$m{country}]</div>|;
	print qq|<div class="c_info1c">$e2j{tax}:$cs{tax}[$m{country}]%</div>|;
	print qq|<div class="c_info1c">$e2j{state}:$country_states[ $cs{state}[$m{country}] ]</div>|;
	print qq|</div>|;
	print qq|<div class="c_info2p">|;
	print qq|<div class="c_info2c">$e2j{food}:$cs{food}[$m{country}]</div>|;
	print qq|<div class="c_info2c">$e2j{money}:$cs{money}[$m{country}]</div>|;
	print qq|<div class="c_info2c">$e2j{soldier}:$cs{soldier}[$m{country}]</div>|;
	print qq|</div>|;
	print qq|</div>|;

	if ($union) {
#		print qq|<br>|;
		print qq|<div class="u_info">|;
		print qq|<span style="color: $cs{color}[$union];">$cs{name}[$union]</span>|;
		print qq|<div class="c_info1p">|;
		print qq|<div class="c_info1c">$e2j{strong}:$cs{strong}[$union]</div>|;
		print qq|<div class="c_info1c">$e2j{tax}:$cs{tax}[$union]%</div>|;
		print qq|<div class="c_info1c">$e2j{state}:$country_states[ $cs{state}[$union] ]</div>|;
		print qq|</div>|;
		print qq|<div class="c_info2p">|;
		print qq|<div class="c_info2c">$e2j{food}:$cs{food}[$union]</div>|;
		print qq|<div class="c_info2c">$e2j{money}:$cs{money}[$union]</div>|;
		print qq|<div class="c_info2c">$e2j{soldier}:$cs{soldier}[$union]</div>|;
		print qq|</div>|;
		print qq|</div>|;
	}
	print qq|</div>|;

=pod
	print qq|<hr>|;
	print qq|<dl>$c_m|;
	print qq|<dt>$e2j{strong}</dt><dd>$cs{strong}[$m{country}]</dd>|;
	print qq|<dt>$e2j{tax}</dt><dd>$cs{tax}[$m{country}]%</dd>|;
	print qq|<dt>$e2j{state}</dt><dd>$country_states[ $cs{state}[$m{country}] ]</dd>|;
	print qq|<dt>$e2j{food}</dt><dd>$cs{food}[$m{country}]</dd>|;
	print qq|<dt>$e2j{money}</dt><dd>$cs{money}[$m{country}]</dd>|;
	print qq|<dt>$e2j{soldier}</dt><dd>$cs{soldier}[$m{country}]</dd>|;
	print qq|</dl>|;

	print qq|<hr><table class="table1s">|;
	print qq|<tr><th colspan="3" style="color: #333; background-color: $cs{color}[$m{country}]; text-align: center;">$c_m</th></tr>\n|;
	print qq|<tr><th>$e2j{strong}</th><th>$e2j{tax}</th><th>$e2j{state}</th></tr>\n|;
	print qq|<tr><td align="right">$cs{strong}[$m{country}]</td><td align="right">$cs{tax}[$m{country}]%</td><td align="center">$country_states[ $cs{state}[$m{country}] ]</td></tr>\n|;
	print qq|<tr><th>$e2j{food}</th><th>$e2j{money}</th><th>$e2j{soldier}</th></tr>\n|;
	print qq|<tr><td align="right">$cs{food}[$m{country}]</td><td align="right">$cs{money}[$m{country}]</td><td align="right">$cs{soldier}[$m{country}]</td></tr>\n|;
	print qq|</table>|;

	if ($union) {
		print qq|<br>|;
		print qq|<table class="table1s">|;
		print qq|<tr><th colspan="3" style="color: #333; background-color: $cs{color}[$union]; text-align: center;">$cs{name}[$union]</th></tr>\n|;
		print qq|<tr><th>$e2j{strong}</th><th>$e2j{tax}</th><th>$e2j{state}</th></tr>\n|;
		print qq|<tr><td align="right">$cs{strong}[$union]</td><td align="right">$cs{tax}[$union]%</td><td align="center">$country_states[ $cs{state}[$union] ]</td></tr>\n|;
		print qq|<tr><th>$e2j{food}</th><th>$e2j{money}</th><th>$e2j{soldier}</th></tr>\n|;
		print qq|<tr><td align="right">$cs{food}[$union]</td><td align="right">$cs{money}[$union]</td><td align="right">$cs{soldier}[$union]</td></tr>\n|;
		print qq|</table>|;
	}
	print qq|<br>|;
=cut
=pod
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
=cut
}

#================================================
# Še‘‘—Í‚Ìî•ñ
#================================================
sub countries_info {
	my($c1, $c2) = split /,/, $w{win_countries};
#	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:320;">|;
	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:100%;">|;
	print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">$e2j{name}</th>|;
#	print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{name}</th>|;
	print qq|<td style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;
	
	unless ($w{world} eq '10') {
		print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">$e2j{strong}</th>|;
#		print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{strong}</th>|;
		for my $i (1 .. $w{country}) {
			my $status = $cs{strong}[$i];
			if ($cs{is_die}[$i] == 1) {
				$status = "–Å –S";
			}
			elsif ($cs{is_die}[$i] == 2) {
				$status = "½ ‘";
			}
			elsif ($cs{is_die}[$i] == 3) {
				$status = "•ö ‰ó";
			}
			print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$status</td>|;
#			print qq|<td align="center" style="border: 1px solid #999; background: #333;">$status</td>|;
#			print $cs{is_die}[$i] ? qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">–Å –S</td>| : qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$cs{strong}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|<tr><th style="border: 2px solid #999; background: #336;">é•Ç</th>|;
	print qq|<td align="center" style="border: 1px solid #999; background: #333;word-break:break-all;">$cs{barrier}[$_]%</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	for my $k (qw/ceo war dom pro mil/) {
		print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="center" style="border: 1px solid #999; background: #333;word-break:break-all;">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}
	print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">l”</th>|;
	print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$cs{member}[$_]/$cs{capacity}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table><br>|;

	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . 'ŠÔ' : int($limit_hour / 24) . '“ú';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>ŠÔ<b>%02d</b>•ª<b>%02d</b>•bŒã", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<hr><font color="#FF0000">œ</font>| : qq|<font color="#00FF00">œ</font>|;
	print qq|ÌßÚ²’† $w{playing}/$max_playingl<br>|;
	print qq|“ˆêŠúŒÀ c‚è$limit_day<br>|;
	if ($reset_rest > 0){
		print qq|IíŠúŠÔyc‚è$reset_time_mesz<br>|;
	}
	print qq|“ïˆÕ“x Lv.$w{game_lv}<br>“ˆê$e2j{strong} $touitu_strong<br>| unless $w{world} eq '10';
	print $c2 ? qq|“ˆê‘ <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>“¯–¿<br>|
		: $c1 ? qq|“ˆê‘ <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><br>|
		:       ''
		;
	print qq|¢ŠEî¨ <a href="world_summaries.cgi?id=$id&pass=$pass&world=$w{world}" class="clickable_name">$world_states[$w{world}]</a><br>|;
	print qq|$world_name—ï$w{year}”N<br>|;
}

#================================================
# —FD“x/ó‘Ô(table”Å)
#================================================
sub promise_table_html {
	my @promise_js = (
		'<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">|</td>',
		'<td align="center" style="background-color: #090">“¯–¿</td>',
		'<td align="center" style="background-color: #C00">Œğí’†</td>',
	);
	
#	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:320;"><tr><td style="border: 1px solid #999; background: #333; white-space: nowrap;">ó‘Ô/—FD“x</td>|;
	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:100%;"><tr><td style="border: 1px solid #999; background: #333; white-space: nowrap;">ó‘Ô/—FD“x</td>|;
	print qq|<td style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for 1 .. $w{country};
	print qq|</tr>|;
	
	for my $i (1 .. $w{country}) {
		print qq|<tr><td style="color: #333; background-color: $cs{color}[$i]">$cs{name}[$i]</td>|;
		for my $j (1 .. $w{country}) {
			if ($i eq $j) {
				print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">@</td>|;
			}
			elsif ($i > $j) {
				my $p_c_c = "p_${j}_${i}";
				print $promise_js[ $w{$p_c_c} ];
			}
			else {
				my $f_c_c = "f_${i}_${j}";
				print qq|<td align="right" style="border: 1px solid #999; background: #333; white-space: nowrap;">$w{$f_c_c}%</td>|;
			}
		}
		print qq|</tr>|;
	}
	print qq|</table>|;
}

sub countries_infos_table {
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
		$ret_str .= "<br>" if $i % 7 == 6;
	}
#	$ret_str .= "</p>";
	return $ret_str;
}

sub show_world_news {
	open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	print "<hr>$line";
}

1; # íœ•s‰Â
