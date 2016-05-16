#================================================
# PCｹﾞｰﾑ画面 Created by Merino
#================================================

#================================================
# ﾒｲﾝ
#================================================
if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif (!$main_screen) {
	&status_html;
}
&framework;

#================================================
# 全体の枠組み
#================================================
sub framework {
	my $country_menu = '';
	$country_menu .= qq|<form method="$method" action="chat_prison.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="牢獄" class="button1"></form>|;
	$country_menu .= qq|<form method="$method" action="bbs_country.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="作戦会議室" class="button1"></form>|;

	# 同盟国があるなら
	if ($union) {
		$country_menu .= qq|<form method="$method" action="bbs_union.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="同盟会議室" class="button1"></form>|;
	}

	# 世界情勢暗黒のみ
	if (($w{world} eq $#world_states) && $m{country} ne $w{country}) {
		$country_menu .= qq|<form method="$method" action="bbs_vs_npc.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="＋ 封 印 会 議 ＋" class="button1"></form>|;
	}

	# ギルド加盟なら
#	if ($m{akindo_guild}) {
#		$country_menu .= qq|<form method="$method" action="bbs_akindo.cgi">|;
#		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$country_menu .= qq|<input type="submit" value="ギルド" class="button1"></form>|;
#	}

	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		$country_menu .= $a_line;
	}
	$country_menu .= qq|<form method="$method" action="chat_casino.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="対人ｶｼﾞﾉ" class="button1"></form>|;
	
	unless ($m{disp_daihyo} eq '0'){
		$country_menu .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="代表\評議会" class="button1"></form>|;
	}

	print qq|<div align="center"><table border="0"><tr>|;
	if ($layout eq '2') { # 縦長
		print qq|<td valign="top">|;
		print qq|<table width="500" border="0" cellspacing="3" cellpadding="3" height="200" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>資金 $m{money} G<br>$mes</tt></td></tr></table></td>|;
	}
	else {
		print qq|<td valign="top">|;
		print qq|<table width="500" border="0" cellspacing="3" cellpadding="3" height="200" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$main_screen</tt></td></tr></table><br>|;
		&my_country_html if !$is_battle && $m{country};
	}
	print qq|</td><td width="160" valign="top" align="right">|;
	unless ($m{disp_top} eq '0'){
		print qq|<form action="$script_index"><input type="submit" value="Ｔ Ｏ Ｐ" class="button1"></form>|;
	}
	
	if (!$is_battle) { # 戦闘中非表示
		unless ($m{disp_news} eq '0'){
			print qq|<form method="$method" action="news.cgi">|;
			print qq|<input type="submit" value="過去の栄光" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|<form method="$method" action="bbs_public.cgi">|;
		print qq|<input type="submit" value="掲 示 板" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		unless ($m{disp_chat} eq '0'){
			print qq|<form method="$method" action="chat_public.cgi">|;
			print qq|<input type="submit" value="交流広場" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|<form method="$method" action="chat_horyu.cgi">|;
		print qq|<input type="submit" value="改造案投票所" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		unless ($m{disp_ad} eq '0'){
			print qq|<form method="$method" action="bbs_ad.cgi">|;
			print qq|<input type="submit" value="宣伝言板" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|$country_menu|;
		print qq|<form method="$method" action="letter.cgi">|;
		print qq|<input type="submit" value="Ｍｙ Ｒｏｏｍ" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		if (&is_sabakan){
			print qq|<form method="$method" action="chat_admin.cgi">|;
			print qq|<input type="submit" value="運営討論場" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
	}
	print qq|<p>$menu_cmd</p>| if $layout eq '2' && $menu_cmd;
	print qq|</td></tr><tr>|;

	if ($layout eq '1') { # 横長
		print qq|<td colspan="2" border="0" cellspacing="2" cellpadding="3" valign="top" width="100%">|;
		print qq|<table width="100%" height="100" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$mes</tt></td></tr></table></td>|;
	}
	elsif ($layout ne '2') { # 通常
		print qq|<td valign="top">|;
		if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
			# 最新情報
			open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiﾌｧｲﾙが読み込めません");
			my $line = <$fh>;
			close $fh;
			print qq|<table width="500" border="0" cellspacing="2" cellpadding="3" height="60" bgcolor="#CCCCCC"><tr>|;
			print qq|<td bgcolor="#000000" align="left" valign="top"><tt>◎最新情報◎<br>$line</tt></td>|;
			print qq|</tr></table>|;
		}
		elsif ($mes) { # ﾒｯｾｰｼﾞ
			print qq|<table width="500" border="0" cellspacing="2" cellpadding="3" height="100" bgcolor="#CCCCCC"><tr>|;
			print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$mes</tt></td>|;
			print qq|</tr></table>|;
		}
		
		print qq|</td><td valign="top" align="right">$menu_cmd</td>|;
	}
	print qq|</tr><tr><td colspan="2">|;

	if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
		# 国ﾃｰﾌﾞﾙ
		&countries_html;
		&world_info;
		&promise_table_html;
	}
	print qq|</td></tr></table></div>|;
}


#================================================
# ﾒｲﾝ画面
#================================================
sub status_html {
	my $head_mes = '';
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi";
		my $line = <$fh>;
		my($letters) = split /<>/, $line;
		close $fh;
		$head_mes .= qq|<font color="#FFCC66">手紙が $letters 件届いています</font><br>|;
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		$head_mes .= qq|<font color="#FFCC00">預かり所に荷物が届いています</font><br>|;
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		$head_mes .= qq|<font color="#FFCC99">ﾏｲﾙｰﾑに荷物が届いています</font><br>|;
	}
	
	my $country_info = '';
	if ($m{country}) {
		my $next_rank = $m{rank} * $m{rank} * 10;
		my $nokori_time = $m{next_salary} - $time;
		$nokori_time = 0 if $nokori_time < 0;
		my $nokori_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
		my $reset_rest = int($w{reset_time} - $time);
		my $gacha_time = $m{gacha_time} - $time;
		$gacha_time = 0 if $gacha_time < 0;
		my $gacha_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		my $gacha_time2 = $m{gacha_time2} - $time;
		$gacha_time2 = 0 if $gacha_time2 < 0;
		my $gacha_time2_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		my $offertory_time = $m{offertory_time} - $time;
		$offertory_time = 0 if $offertory_time < 0;
		my $offertory_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $offertory_time / 3600, $offertory_time % 3600 / 60, $ofertory_time % 60);

		$country_info .= qq|<hr size="1">|;
		$country_info .= qq|$units[$m{unit}][1] <b>$rank_sols[$m{rank}]</b>兵<br>|;
		$country_info .= qq|$e2j{rank_exp} [ <b>$m{rank_exp}</b> / <b>$next_rank</b> ]<br>|;
		$country_info .= qq|敵国[前回：<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> 連続<b>$m{renzoku_c}</b>回]<br>| if $m{renzoku_c};
		$country_info .= qq|<hr size="1">|;
#		$country_info .= qq|残り時間<br>\n|;
		$country_info .= qq|<table class="table1">|;
		if ($m{disp_gacha_time}) {
			$country_info .= qq|<tr><th>給与</th><th>賽銭</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td><td><span id="offertory_time">$offertory_time_mes</span></td></tr>\n|;
			$country_info .= qq|<tr><th>ガチャ</th><th>ガチャ（高）</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="gacha_time">$gacha_time_mes</span></td><td><span id="gacha_time2">$gacha_time2_mes</span></td></tr>\n|;
		} else {
			$country_info .= qq|<tr><th>給与</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td></tr>\n|;
		}
		$country_info .= qq|<script type="text/javascript"><!--\n nokori_time($nokori_time, $reset_rest, $gacha_time, $gacha_time2, $offertory_time);\n// --></script>\n|;
		$country_info .= qq|</table>|;
#		$country_info .= qq|<br>|;
	}
	
	my $name = $m{name};
	$name .= "[$m{shogo}]" if $m{shogo};
	my $marriage = '';
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		$marriage = qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	my $master = '';
	if ($m{master}){
		if($m{master_c}){
			$master = qq|師匠 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
		}else{
			$mid = unpack 'H*', $m{master};
			if (-f "$userdir/$mid/user.cgi") {
				$master = qq|弟子 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
			} else {
				$master = qq|弟子 <font color="#FF0000">$m{master} 死亡</font><br>|;
			}
		}
	}
	my $fuka = $m{egg} ? int($m{egg_c} / $eggs[$m{egg}][2] * 100) : 0;
	my $rank_name = &get_rank_name($m{rank}, $m{name});
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '★' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}

	$main_screen .= qq|<table width="100%" border="0"><tr><td width="60%" valign="top" align="left"><tt>$head_mes|;
	$main_screen .= qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| if $m{icon};
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	my $pet_c = $m{pet} ? "★$m{pet_c}":'';
	my $act_d = $m{act} > 100 ? 100 : $m{act}; 
	my $exp_d = $m{exp} > 100 ? 100 : $m{exp}; 
	$main_screen .=<<"EOM";

		$name<br>
		$marriage
		$master
		<font color="$cs{color}[$m{country}]">$c_m</font> $rank_name<br>
		$country_info
		<hr size="1">
		
		<font color="#9999CC">武器：[$weas[$m{wea}][2]]$wname★<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>
		<font color="#9999CC">防具：[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>
		<font color="#99CCCC">ﾍﾟｯﾄ：$pets[$m{pet}][1]$pet_c</font><br>
		<font color="#99CC99">ﾀﾏｺﾞ：$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>
		<div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div>
		<font color="#CCCC99">虫  ：$m{insect_name}</font><br>
		
	</tt></td><td valign="top" align="left"><tt>
		
		<b>$m{sedai}</b>世代目 $sexes[ $m{sex} ]<br>
		Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>
		<font color="#CC9999">$e2j{hp} [ <b>$m{hp}</b>/<b>$m{max_hp}</b> ]</font><br>
		<font color="#CC99CC">$e2j{mp} [ <b>$m{mp}</b>/<b>$m{max_mp}</b> ]</font><br>
		<hr size="1">
		疲労度 <b>$m{act}</b>%<br>
		<div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $act_d%"></div>
		<hr size="1">
		$e2j{exp} <b>$m{exp}</b>Exp<br>
		<div class="bar4"><img src="$htmldir/space.gif" style="width: $exp_d%"></div>

		<hr size="1">
		資金 <b>$m{money}</b>G<br>
		<hr size="1">
		勲　章　<b>$m{medal}</b>個<br>
		ｶｼﾞﾉｺｲﾝ <b>$m{coin}</b>枚<br>
		宝 ｸ ｼﾞ【$m{lot}】<br>
		
	</tt></td></tr></table>
EOM
}



#================================================
# 戦闘画面
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| : '';;
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" style="vertical-align: middle;">| : '';

	my $m_hp_par = $m{max_hp} <= 0 ? 0 : int($m{hp} / $m{max_hp} * 100);
	my $y_hp_par = $y{max_hp} <= 0 ? 0 : int($y{hp} / $y{max_hp} * 100);
	my $m_mp_par = $m{max_mp} <= 0 ? 0 : int($m{mp} / $m{max_mp} * 100);
	my $y_mp_par = $y{max_mp} <= 0 ? 0 : int($y{mp} / $y{max_mp} * 100);
	my $fuka = $m{egg} ? int($m{egg_c} / $eggs[$m{egg}][2] * 100) : 0;
	
	$m_mes = qq|<span style="color: #333; background-color: #FFF;">< $m_mes )</span>| if $m_mes;
	$y_mes = qq|<span style="color: #333; background-color: #FFF;">< $y_mes )</span>| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">★</font>' : '';

	$main_screen .= qq|$m_icon $m{name} $m_mes<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>$e2j{max_hp}：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_hp_par%"></div></td><td> (<b>$m{hp}</b>/<b>$m{max_hp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$e2j{max_mp}：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m_mp_par%"></div></td><td> (<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td colspan="3">攻撃力 [ <b>$m_at</b> ] / 防御力 [ <b>$m_df</b> ] / 素早さ[ <b>$m_ag</b> ]<br></td></tr>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	$main_screen .= qq|<tr><td colspan="3">$m_tokkou武器：[$weas[$m{wea}][2]] $wname★$m{wea_lv} ($m{wea_c})<br></td></tr>| if $m{wea};
	$main_screen .= qq|<tr><td colspan="3">防具：[$guas[$m{gua}][2]] $guas[$m{gua}][1]<br></td></tr>| if $m{gua};
	$main_screen .= qq|<tr><td colspan="3">ﾍﾟｯﾄ：$pets[$m{pet}][1]★$m{pet_c}<br></td></tr>| if $pets[$m{pet}][2] eq 'battle';
	my $act_d = $m{act} > 100 ? 100 : $m{act}; 
	my $exp_d = $m{exp} > 100 ? 100 : $m{exp}; 
	$main_screen .= qq|<tr><td>$e2j{exp}：</td><td><div class="bar4"><img src="$htmldir/space.gif" style="width: $exp_d%"></div></td><td> (<b>$m{exp}</b>/<b>100</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$eggs[$m{egg}][1]：</td><td><div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div></td><td> (<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>疲労度：</td><td><div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $act_d%"></div></td><td> (<b>$m{act}</b>/<b>100</b>)<br></td></tr>|;

	$main_screen .= qq|</table>　 VS<br>|;
	
	$main_screen .= qq|$y_icon $y{name} $y_mes<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>$e2j{max_hp}：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_hp_par%"></div></td><td> (<b>$y{hp}</b>/<b>$y{max_hp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$e2j{max_mp}：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y_mp_par%"></div></td><td> (<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td colspan="3">攻撃力 [ <b>$y_at</b> ] / 防御力 [ <b>$y_df</b> ] / 素早さ[ <b>$y_ag</b> ]<br></td></tr>|;
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	$main_screen .= qq|<tr><td colspan="3">$y_tokkou武器：[$weas[$y{wea}][2]] $ywname<br></td></tr>| if $y{wea};
	$main_screen .= qq|<tr><td colspan="3">防具：[$guas[$y{gua}][2]] $guas[$y{gua}][1]<br></td></tr>| if $y{gua};
	$main_screen .= qq|</table>|;
}

#================================================
# 戦争画面
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| : '';;
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" style="vertical-align: middle;">| : '';
	
	$war_march = 1 if $war_march <= 0;
	my $m_sol_par = $rank_sols[$m{rank}] * $war_march <= 0 ? 0 : int($m{sol} / ($rank_sols[$m{rank}] * $war_march) * 100);
	my $y_sol_par = $rank_sols[$y{rank}] * $war_march <= 0 ? 0 : int($y{sol} / ($rank_sols[$y{rank}] * $war_march) * 100);
	
	$m_mes = qq|<span style="color: #333; background-color: #FFF;">< $m_mes )</span>| if $m_mes;
	$y_mes = qq|<span style="color: #333; background-color: #FFF;">< $y_mes )</span>| if $y_mes;
	
	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	
	my $rank_name = &get_rank_name($m{rank}, $m{name});
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '★' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	$main_screen .= qq|$m_icon $m{name} [$rank_name] $m_mes<br>|;
	$main_screen .= qq|$m_tokkou$units[$m{unit}][1] 統率[<b>$m{lea}</b>] <br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>兵士：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_sol_par%"></div></td><td> (<b>$m{sol}</b>兵)<br></td></tr>|;
	$main_screen .= qq|<tr><td>士気：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m{sol_lv}%"></div></td><td> (<b>$m{sol_lv}</b>%)<br></td></tr>|;
	$main_screen .= qq|</table>|;
	$main_screen .= qq|　 VS　 残り$m{turn}ﾀｰﾝ<br>|;
	my $yrank_name = &get_rank_name($y{rank}, $y{name});
	$main_screen .= qq|$y_icon $y{name} [$yrank_name] $y_mes<br>|;
	$main_screen .= qq|$y_tokkou$units[$y{unit}][1] 統率[<b>$y{lea}</b>]<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>兵士：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_sol_par%"></div></td><td> (<b>$y{sol}</b>兵)<br></td></tr>|;
	$main_screen .= qq|<tr><td>士気：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y{sol_lv}%"></div></td><td> (<b>$y{sol_lv}</b>%)<br></td></tr>|;
	$main_screen .= qq|</table>|;
}


#================================================
# 国々の国力、代表者
#================================================
sub countries_html {
	my($c1, $c2) = split /,/, $w{win_countries};

	print qq|<table class="table1">|;
	print qq|<tr><th>$e2j{name}</th>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_];">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;
	
	unless ($w{world} eq '10') {
		print qq|<tr><th>$e2j{strong}</th>|;
		for my $i (1 .. $w{country}) {
			my $status = $cs{strong}[$i];
			if ($cs{is_die}[$i] == 1) {
				$status = "滅 亡";
			}
			elsif ($cs{is_die}[$i] == 2) {
				$status = "鎖 国";
			}
			elsif ($cs{is_die}[$i] == 3) {
				$status = "崩 壊";
			}
			print qq|<td align="center">$status</td>|;

#			print $cs{is_die}[$i] ? qq|<td align="center">滅 亡</td>| : qq|<td align="center">$cs{strong}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	for my $k (qw/ceo war dom pro mil/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="center">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}
	print qq|<tr><th>人数</th>|;
	print qq|<td align="center">$cs{member}[$_]/$cs{capacity}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;
	print qq|<tr><th>新規</th>|;
	print qq|<td align="center">$cs{new_commer}[$_]/$cs{capacity}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table><br>|;
}

#================================================
# 世界の情報
#================================================
sub world_info {
	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . '時間' : int($limit_hour / 24) . '日';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>時間<b>%02d</b>分<b>%02d</b>秒後", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<font color="#FF0000">●</font>| : qq|<font color="#00FF00">●</font>|;
	print qq|ﾌﾟﾚｲ中【$w{playing}/$max_playing人】/ |;
	print qq|世界情勢【<a href="world_summaries.cgi?id=$id&pass=$pass&world=$w{world}" class="clickable_name">$world_states[$w{world}]</a>】/ |;
	print qq|$world_name暦【$w{year}年】/ |;
	print qq|統一期限【残り$limit_day】<br>|;
	
	if ($reset_rest > 0){
		print qq|終戦期間【残り<span id="reset_time">$reset_time_mes</span>|;
		print qq|<noscript>$reset_time_mes</noscript>|;
		print qq|】<br>|;
	}
	print qq|難易度【Lv.$w{game_lv}】/ 統一$e2j{strong}【$touitu_strong】/ | unless $w{world} eq '10';
	print $c2 ? qq|統一国【<font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>同盟】|
		: $c1 ? qq|統一国【<font color="$cs{color}[$c1]">$cs{name}[$c1]</font>】|
		:       ''
		;
}


#================================================
# 友好度/状態(table版)
#================================================
sub promise_table_html {
	my @promise_js = (
		'<td align="center">−</td>',
		'<td align="center" style="background-color: #090">同盟</td>',
		'<td align="center" style="background-color: #C00">交戦中</td>',
	);
	
	print qq|<table class="table1s"><tr><td>状態/友好度</td>|;
	print qq|<td style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for 1 .. $w{country};
	print qq|</tr>|;
	
	for my $i (1 .. $w{country}) {
		print qq|<tr><td style="color: #333; background-color: $cs{color}[$i]">$cs{name}[$i]</td>|;
		for my $j (1 .. $w{country}) {
			if ($i eq $j) {
				print qq|<td align="center">　</td>|;
			}
			elsif ($i > $j) {
				my $p_c_c = "p_${j}_${i}";
				print $promise_js[ $w{$p_c_c} ];
			}
			else {
				my $f_c_c = "f_${i}_${j}";
				print qq|<td align="right">$w{$f_c_c}%</td>|;
			}
		}
		print qq|</tr>|;
	}
	print qq|</table><br>|;
}


#================================================
# 自国/同盟国の情報
#================================================
sub my_country_html {
	print <<"EOM";
		<table class="table1" width="500" cellpadding="3">
			<tr>
				<th>所属国</th>
				<th>$e2j{state}</th>
				<th>$e2j{tax}</th>
				<th>$e2j{strong}</th>
				<th>$e2j{food}</th>
				<th>$e2j{money}</th>
				<th>$e2j{soldier}</th>
			</tr><tr>
				<td style="color: #333; background-color: $cs{color}[$m{country}]; text-align: center;">$cs{name}[$m{country}]</td>
				<td align="center">$country_states[ $cs{state}[$m{country}] ]</td>
				<td align="right"><b>$cs{tax}[$m{country}]</b>%</td>
				<td align="right"><b>$cs{strong}[$m{country}]</b></td>
				<td align="right"><b>$cs{food}[$m{country}]</b></td>
				<td align="right"><b>$cs{money}[$m{country}]</b></td>
				<td align="right"><b>$cs{soldier}[$m{country}]</b></td>
			</tr>
		</table>
		<br>
EOM
	if ($union) {
		print <<"EOM";
		<table class="table1" width="500" cellpadding="3">
			<tr>
				<th>同盟国</th>
				<th>$e2j{state}</th>
				<th>$e2j{tax}</th>
				<th>$e2j{strong}</th>
				<th>$e2j{food}</th>
				<th>$e2j{money}</th>
				<th>$e2j{soldier}</th>
			</tr><tr>
				<td style="color: #333; background-color: $cs{color}[$union]; text-align: center;">$cs{name}[$union]</td>
				<td align="center">$country_states[ $cs{state}[$union] ]</td>
				<td align="right"><b>$cs{tax}[$union]</b>%</td>
				<td align="right"><b>$cs{strong}[$union]</b></td>
				<td align="right"><b>$cs{food}[$union]</b></td>
				<td align="right"><b>$cs{money}[$union]</b></td>
				<td align="right"><b>$cs{soldier}[$union]</b></td>
			</tr>
		</table>
		<br>
EOM
	}
}

#================================================
# ｶｼﾞﾉの人数
#================================================
sub all_member_n {
	my $ret_str = '';
	for my $i (0 .. $#files) {
		my $member_c  = 0;
		my %sames = ();
		my $tf_name = "$logdir/chat_casino$files[$i][2]_member.cgi";
	
		open my $fh, "< $tf_name" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		my $head_line = <$fh>;
		while (my $line = <$fh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
			if ($time - 60 > $mtime) {
				next;
			}
			next if $sames{$mname}++; # 同じ人なら次
			
			$member_c++;
		}
		close $fh;
		$ret_str .= substr($files[$i][0], 0, 2) . "/$member_c ";
		$ret_str .= "<br>" if $i % 4 == 3;
	}
	return $ret_str;
}


1; # 削除不可
