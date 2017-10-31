
#================================================
# いたずら
#================================================
#いたずらが元に戻る時間
my $trick_time = 24 * 60 * 60;

#================================================
sub begin {
	$mes .= "戻ります";
	&refresh;
	&n_menu;
}
sub tp_1  {
	$mes .= "戻ります";
	&refresh;
	&n_menu;
}

#================================================
# ｶﾞﾊｸ
#================================================
sub tp_100{
	$mes .= qq|<form method="$method" action="$script"><p>いたずら対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> やめる<hr>|;

	opendir my $dh, "$userdir/$id/picture" or &error('ﾏｲﾋﾟｸﾁｬが開けません');
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /\.html$/;

		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="icon" value="$file_name"><img src="$userdir/$id/picture/$file_name" $mobile_icon_size> $file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="このアイコンに変える" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110{
	if ($in{icon} eq '0'){
		$mes .= 'やめました<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq '') {
		$mes .= 'いたずら先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分にいたずらはできません<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{icon_t} eq ''){
		if ($in{icon} && -f "$userdir/$id/picture/$in{icon}") {
			&error("同じﾀｲﾄﾙのものがすでに使われています") if -f "$icondir/$in{icon}";
			rename "$userdir/$id/picture/$in{icon}", "$icondir/$in{icon}"  or &error("rename error");
			&regist_you_data($in{trick_name},'icon_t',$datas{icon});
			&regist_you_data($in{trick_name},'icon',$in{icon});
			&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);
			&remove_pet;
			&mes_and_world_news("$datas{name}のｱｲｺﾝにいたずらをしました");
		}
		else {
			$mes .= 'やめました<br>';
		}
	}
	&refresh;
	&n_menu;
}

#================================================
# ﾜﾛｽ
#================================================
sub tp_200{
	$mes .= qq|<form method="$method" action="$script"><p>いたずら対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>称号に（笑）をつける<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_210{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= 'いたずら先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分にいたずらはできません<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{shogo} && $datas{shogo_t} eq ''){
		my $t_shogo = $datas{shogo};
		$t_shogo .= '(笑)';
		&regist_you_data($in{trick_name},'shogo',$t_shogo);
		&regist_you_data($in{trick_name},'shogo_t',$datas{shogo});
		&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);

		&remove_pet;
		&mes_and_world_news("$datas{name}の称号を$datas{shogo}から$t_shogoに変えました");
	}
	&refresh;
	&n_menu;
}

#================================================
# ｻｷﾞ
#================================================
sub tp_300{
	$mes .= qq|<form method="$method" action="$script"><p>いたずら対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>所持金を増減させる<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_310{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= 'いたずら先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分にいたずらはできません<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	my $v = int(rand(6)+1) * 10000;
	$mes.="$pets[$m{pet}][1]★$m{pet_c}が$in{trick_name}のお金を $v G";
	if (rand(2) < 1 && $datas{money} > 10000) {
		$datas{money} -= $v;
		$datas{money} = 10000 if $datas{money} < 10000;
		&regist_you_data($in{trick_name},'money',$datas{money});
		$mes.="減らしました<br>";
	}
	else { 
		$datas{money} += $v;
		&regist_you_data($in{trick_name},'money',$datas{money});
		$mes.="増やしました<br>";
	}

	&remove_pet;
	&mes_and_world_news("$datas{name}の所持金にいたずらしました");
	&refresh;
	&n_menu;
}

#================================================
# ｻﾙｸﾞﾂﾜ
#================================================
sub tp_400{
	$mes .= qq|<form method="$method" action="$script"><p>拘束対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>発言できなくさせる<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_410{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '拘束先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分に拘束はできません<br>';
		&begin;
		return;
	}
	&regist_you_data($in{trick_name},'silent_time', $time + (60 * 20)); # 20分
	&regist_you_data($in{trick_name},'silent_kind', 0);
	&remove_pet if int(rand(3)) < 1;
	&mes_and_world_news("$in{trick_name}に猿轡をかけました");
	&refresh;
	&n_menu;
}

#================================================
# ﾍｯﾄﾞﾊﾝﾄ
#================================================
sub tp_500{
	$mes .= qq|<form method="$method" action="$script"><p>勧誘対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>自国に誘う<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="勧誘" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_510{
	return if &is_ng_cmd(1);
	if ($w{world} eq $#world_states || $w{world} eq $#world_states - 5) {
		$mes .= '今期は勧誘できません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq '') {
		$mes .= '勧誘先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分に勧誘はできません<br>';
		&begin;
		return;
	}

	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{country} eq $m{country}) {
		$mes .= '自国民を勧誘はできません<br>';
		&begin;
		return;
	}
	my $need_money = $datas{sedai} > 100 ? $rank_sols[$datas{rank}]+300000 : $rank_sols[$datas{rank}]+$datas{sedai}*3000;
	if ($m{money} < $need_money) {
		$mes .= 'お金が足りません<br>';
		&begin;
		return;
	}
	$m{money} -= $need_money;
	$mes .= "仲介料として$need_money G支払いました<br>";

	open my $fh, ">> $userdir/$trick_id/head_hunt.cgi";
	print $fh "$m{name}<>$m{country}<>\n";
	close $fh;
	&remove_pet;
	&refresh;
	&n_menu;
}

#================================================
# ﾒｶﾞﾎﾝ
#================================================
sub tp_600 {
	$mes .= qq|<form method="$method" action="$script"><p>発言内容：<input type="text" name="topic" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>叫ぶ<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="叫ぶ" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_610 {
	return if &is_ng_cmd(1);
	my $is_error = 0;
	if ($in{topic} =~ /[,;\"\'&<>]/) {
		$mes .= "発言内容に不正な文字( ,;\"\'&<> )が含まれています<br>$in{topic}<br>";
		$is_error = 1;
	}
	elsif (length($in{topic}) > 80) {
		$mes .= "発言内容は全角40(半角80)文字以内です<br>$in{topic}<br>";
		$is_error = 1;
	}
	if ($is_error) {
		&begin;
		return;
	}
	&remove_pet;
	$mes .= "$m{name}は";
	my $place = int(rand(1000));
	if ($place < 950) {
		$mes .= "広場で";
		&_write_news('world_news', "$m{name}は「$in{topic}」と叫んだ");
	}
	elsif ($place < 960) {
		$mes .= "物々交換の場で";
		&write_send_news("$m{name}は「$in{topic}」と叫んだ");
	}
	elsif ($place < 970) {
		$mes .= "日記置場で";
		&write_blog_news("$m{name}は「$in{topic}」と叫んだ");
	}
	elsif ($place < 980) {
		$mes .= "闘技場で";
		&write_colosseum_news("$m{name}は「$in{topic}」と叫んだ");
	}
	elsif ($place < 990) {
		$mes .= "絵の展示場で";
		&write_picture_news("$m{name}は「$in{topic}」と叫んだ");
	}
	elsif ($place < 999) {
		$mes .= "本屋で";
		&write_book_news("$m{name}は「$in{topic}」と叫んだ");
	}
	else {
		$mes .= "世界の中心で";
		&write_world_big_news("$m{name}は「$in{topic}」と叫んだ");
	}
	$mes .= "「$in{topic}」と叫んだ\n";

	&refresh;
	&n_menu;
}

#================================================
# ｱﾘﾖｼ
#================================================
sub tp_700{
	$mes .= qq|<form method="$method" action="$script"><p>いたずら対象：<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<br>称号：<input type="text" name="trick_shogo" class="text_box1"><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>称号をつける<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_710{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= 'いたずら先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分にいたずらはできません<br>';
		&begin;
		return;
	}
	if ($in{trick_shogo} eq '') {
		$mes .= '称号が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_shogo} eq $shogos[1][0]) {
		$mes .= '他人をゴミクズ呼ばわりとかいかんだろ･･･常識的に考えて･･･<br>';
		&begin;
		return;
	}
	$in{trick_shogo} =~ s/★/☆/g;
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{shogo_t} eq ''){
		&regist_you_data($in{trick_name},'shogo',$in{trick_shogo});
		&regist_you_data($in{trick_name},'shogo_t',$datas{shogo});
		&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);

		&remove_pet;
		&mes_and_world_news("$datas{name}に$in{trick_shogo}とあだ名をつけました");
	}
	&refresh;
	&n_menu;
}

#================================================
# ﾃﾝﾁﾄﾋﾄﾂ
#================================================
sub tp_800{
	$mes .= qq|<form method="$method" action="$script"><p>武器名：<input type="text" name="weapon_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>武器を手に入れる<br>|;
	$mes .= qq|属性|;
	$mes .= qq|<input type="radio" name="type" value="0" checked>選ばない|;
	$mes .= qq|<input type="radio" name="type" value="1" checked>剣|;
	$mes .= qq|<input type="radio" name="type" value="2" checked>槍|;
	$mes .= qq|<input type="radio" name="type" value="3" checked>斧|;
	$mes .= qq|<input type="radio" name="type" value="4" checked>火|;
	$mes .= qq|<input type="radio" name="type" value="5" checked>風|;
	$mes .= qq|<input type="radio" name="type" value="6" checked>雷<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="決定" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_810{
	return if &is_ng_cmd(1);
	if ($in{weapon_name} eq '') {
		$mes .= '武器名が記入されていません<br>';
		&begin;
		return;
	}
	if ($m{wea}) {
		# ｵﾘｼﾞﾅﾙ武器持った状態でﾃﾝﾁﾄﾋﾄﾂを使うとｵﾘｼﾞﾅﾙ武器の中身がｺﾋﾟｰされてしまう
		# ｺﾋﾟｰされることではなくｸﾛﾑﾊｰﾂになって戻ってこないことが問題
		if ($m{wea_name}) {
			&send_item($m{name}, 1, 32, 0, 0, 1); # ｸﾛﾑﾊｰﾂ
		}
		else {
			&send_item($m{name}, 1, $m{wea}, $m{wea_c}, $m{wea_lv}, 1);
		}
	}
	my $i;
	if ($in{type} >= 1 && $in{type} <= 6) {
		$i = ($in{type} - 1) * 5 + int(rand(5)) + 1
	}
	else {
		$i = int(rand($#weas)+1);
	}

	&remove_pet;
	$m{wea} = $i;

	# どうせ手放したらｸﾛﾊﾑ★0に戻るので★30になること自体はさほど問題にならなそう？
	# むしろ★0持ってる状態と★30持ってる状態でﾃﾝﾁﾄﾋﾄﾂ使った時に損をする側がでるから一律★30にしてしまっても良いかと
	# 代わりにオシャカデメリット
	$m{wea_c} = 0;
	$m{wea_lv} = 30;

	$m{wea_name} = "$in{weapon_name}";
	&mes_and_world_news("$in{weapon_name}を手に入れました");

	&refresh;
	&n_menu;
}

#================================================
# ｶｼﾗ
#================================================
sub tp_900 {
	$mes .= qq|<form method="$method" action="$script"><p>拘束対象：<input type="text" name="trick_name" class="text_box1"></p><br>|;
	$mes .= qq|<p>強制語尾：<input type="text" name="tail" value="ｶｼﾗ" class="text_box1"></p><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>語尾を強制させる<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_910 {
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '拘束先が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{tail} eq '') {
		$mes .= '語尾が記入されていません<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '自分に拘束はできません<br>';
		&begin;
		return;
	}
	if (length($in{tail}) > 80) {
		$mes .= '語尾は全角40(半角20)文字以内です<br>';
		&begin;
		return;
	}
	&regist_you_data($in{trick_name},'silent_time', $time+3600);
	&regist_you_data($in{trick_name},'silent_kind', 4);
	&regist_you_data($in{trick_name},'silent_tail', $in{tail});
	&remove_pet if rand(3) < 1;
	&mes_and_world_news("$in{trick_name}の語尾を強制しました");
	&refresh;
	&n_menu;
}

#================================================
# ﾎｰﾘｴ
#================================================
sub tp_1000{
	$mes .= qq|<form method="$method" action="$script"><p>偽装プレイヤー名：<input type="text" name="trick_name" class="text_box1"></p><br>|;
	$mes .= qq|<p>偽装国：<select name="trick_country" class="menu1">|;
	for my $i (1..$w{country}) {
		$mes .= qq|<option value="$i">$cs{name}[$i]</option>|;
	}
	$mes .= qq|</select></p><br>|;
	$mes .= qq|<p>ﾍﾟｯﾄ：<select name="trick_pet" class="menu1">|;
	for my $i (1..$#pets) {
		$mes .= qq|<option value="$i">$pets[$i][1]</option>|;
	}
	$mes .= qq|</select></p><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>ﾍﾟｯﾄを送ったふりをする<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="2">布告偽装<br>| if $m{country};
	$mes .= qq|<input type="radio" name="cmd" value="3">停戦偽装<br>| if $m{country};
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="いたずら" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_1010{
	if ($in{trick_name} eq '') {
		$mes .= 'いたずら名が記入されていません<br>';
		&begin;
		return;
	}
	if ($cmd eq '1') {
		&mes_and_send_news("$in{trick_name}に$pets[$in{trick_pet}][1]を送りました");
	}
	elsif ($cmd eq '2') {
		&write_world_news("<b>$cs{name}[$m{country}]の$in{trick_name}が</b><b>$cs{name}[$in{trick_country}]に宣戦布告をしました</b>");
	}
	elsif ($cmd eq '3') {
		&write_world_news("<b>$cs{name}[$m{country}]の$in{trick_name}が</b><b>$cs{name}[$in{trick_country}]と停戦条約を結びました</b>");
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
		return;
	}
	&remove_pet if rand(7) < 1;
	&refresh;
	&add_prisoner;
	&n_menu;
}

1; # 削除不可
