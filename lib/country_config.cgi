require './lib/move_player.cgi';
my $this_file = "$logdir/violator.cgi";
#=================================================
# 国設定 Created by Merino
#=================================================

# 各国設定の投資が有効な期間
my $valid_investment = 1;

# 君主の議決によりﾌﾟﾚｲﾔｰ削除権限(0:なし,1:あり)
my $is_ceo_delete = 1;

# 削除権限ありの場合。必要票
my @need_vote_violator = (2, 4, 5);

# 削除権限ありの場合。必要経過日数
my $non_new_commer_date = 30;
my $is_delete = $config_test ? 1 : $m{start_time} + $non_new_commer_date * 24 * 3600 < $time;

my @violate = ('島流し', '斬首', '永久追放');

# 削除権限ありの場合。君主の多重IPﾁｪｯｸ権限(0:なし,1:あり)
my $is_ceo_watch_multi = 1;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($cs{ceo}[$m{country}] ne $m{name}) {
		$mes .= "国の$e2j{ceo}でないと行うことができません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何か行いますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "流刑者を各国の$e2j{ceo}の投票により削除することができます<br>" if $is_ceo_delete;
		$mes .= "$c_mの名前、色、方針、会議室名や牢獄名を変更することができます<br>";
		$mes .= "$e2j{name}：$c_m<br>";
		$mes .= "国色：$cs{color}[$m{country}]<br>";
		$mes .= "会議室名：";
		$mes .= $cs{bbs_name}[$m{country}] eq '' ? "$cs{name}[$m{country}]作戦会議室" : $cs{bbs_name}[$m{country}];
		$mes .= "<br>牢獄名：$cs{prison_name}[$m{country}]";
	}
	my @menus = ('やめる', '国名/色を変更', '方針/ｼﾝﾎﾞﾙを変更','NPC名を変更','国庫の設定','各国設定','会議室名を変更','牢獄名を変更','安楽死');
	if ($is_ceo_delete) {
		push @menus, '流刑者議決';
		push @menus, '流刑者申\請';
		
		if ($is_ceo_watch_multi) {
			push @menus, '多重者ﾁｪｯｸ';
		}
	}
	&menu(@menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..11);

	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# 国名/色を変更
#================================================
sub tp_100 {
	$mes .= qq|$e2j{name}は全角7(半角14)文字まで。半角記号(,;"'&)、空白(ｽﾍﾟｰｽ)は使えません<br>|;
	#"
	$mes .= qq|国色は#から始まる16進数表\記<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{name}：<input type="text" name="name" value="$c_m" class="text_box1"><br>|;
	$mes .= qq|色：<input type="text" name="color" value="$cs{color}[$m{country}]" class="text_box1"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	my $is_rewrite = 0;
	if ($in{name} || $in{color}) {
		unless ($c_m eq $in{name}) {
			&error("$e2j{name}を記入してください") if $in{name} eq '';
			&error("$e2j{name}に不正な文字( ,;\"\'&<>\\\/ )が含まれています") if $in{name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("$e2j{name}に不正な空白が含まれています") if $in{name} =~ /　/ || $in{name} =~ /\s/;
			&error("$e2j{name}は全角7(半角14)文字までです") if length $in{name} > 14;
			for my $name (@{ $cs{name} }) {
				&error('その$e2j{name}はすでに使われています') if $in{name} eq $name;
			}
			
			$in{color} ||= $cs{color}[$m{country}];
			$mes .= "$e2j{name}を$in{name}に変更しました<br>";
			&write_world_news(qq|<b>$c_mの$e2j{ceo}$m{name}によって、$c_mを<font color="$in{color}">$in{name}</font>と$e2j{name}を改めました</b>|, 1);
			
			$cs{name}[$m{country}] = $in{name};
			$is_rewrite = 1;
		}
	
		unless ($cs{color}[$m{country}] eq $in{color}) {
			&error('色を半角英数字で記入してください') if $in{color} eq '' || $in{color} =~ /[^0-9a-zA-Z#]/;
			&error('色を#から始まる16進数の色で記入してください') if $in{color} !~ /#.{6}/;
			$mes .= "国色を$in{color}に変更しました<br>";
			$cs{color}[$m{country}] = $in{color};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#================================================
# 方針を変更
#================================================
sub tp_200 {
	my $line = &get_countries_mes($m{country});
	my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|方針[全角100(半角200)文字まで]<br>・改行は削除されます<br>|;
	$mes .= qq|<textarea name="country_mes" cols="60" rows="3" class="textarea1">$country_mes</textarea><br>|;

	$mes .= qq|ルール[全角100(半角200)文字まで]<br>・改行は削除されます<br>|;
	$mes .= qq|<textarea name="country_rule" cols="60" rows="3" class="textarea1">$country_rule</textarea><br>|;

	$mes .= qq|<hr>ｼﾝﾎﾞﾙ<br>|;

	# ｼﾝﾎﾞﾙ
	$mes .= qq|<input type="radio" name="country_mark" value="">なし<hr>|;
	if ($country_mark) {
		my $file_title = &get_goods_title($country_mark);
		$mes .= qq|<input type="radio" name="country_mark" value="$country_mark" checked><img src="$icondir/$country_mark">[現在のｼﾝﾎﾞﾙ]$file_title<hr>|;
	}
	opendir my $dh, "$userdir/$id/picture" or &error("$userdir/$id/picture ﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /^index.html$/;
		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="country_mark" value="$file_name"><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;">$file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	unless (defined $in{country_mes}) {
		$mes .= "やめました<br>";
		&begin;
		return;
	}
	
	&error("国の方針は全角100(半角200)文字までです") if length $in{country_mes} > 200;
	&error("国の方針は全角100(半角200)文字までです") if length $in{country_rule} > 200;
#	&error("貴様…何ヲシヨウトシテイルノカ…ワカッテイルノカ…？") if $w{world} eq $#world_states && $m{country} eq $w{country};
	
	my $is_rewrite = 0;
	my $country = 0;
	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($country eq $m{country}) {
			my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
			
			unless ($country_mes eq $in{country_mes}) {
				$is_rewrite = 1;
				$mes .= "国の方針を<hr>$in{country_mes}<hr>に変更しました<br>";
			}

			unless ($country_rule eq $in{country_rule}) {
				$is_rewrite = 1;
				$mes .= "刑法を<hr>$in{country_rule}<hr>に変更しました<br>";
			}
			
			# ｼﾝﾎﾞﾙあり→なし
			if ($country_mark && $in{country_mark} eq '') {
				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("ｼﾝﾎﾞﾙの書き換えに失敗しました");
				$mes .= qq|国のｼﾝﾎﾞﾙをなしに変更しました<br>|;
			}
			# ｼﾝﾎﾞﾙ変更
			elsif ($country_mark ne $in{country_mark}) {
				&error("同じﾀｲﾄﾙのｼﾝﾎﾞﾙがすでに使われています") if -f "$icondir/$in{country_mark}";
				&error("$non_titleの物をｼﾝﾎﾞﾙにすることはできません") if $in{country_mark} =~ /^_/;
				&error("選択した絵が存在しません") unless -f "$userdir/$id/picture/$in{country_mark}";

				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("ｼﾝﾎﾞﾙの書き換えに失敗しました") if -f "$icondir/$country_mark";
				rename "$userdir/$id/picture/$in{country_mark}", "$icondir/$in{country_mark}" or &error("ｼﾝﾎﾞﾙの書き換えに失敗しました");
				
				my $file_title = &get_goods_title($in{country_mark});
				$mes .= qq|国のｼﾝﾎﾞﾙを$file_title<img src="$icondir/$in{country_mark}">に変更しました<br>|;
			}
			
			if ($is_rewrite) {
				$line = "$in{country_mes}<>$in{country_mark}<>$in{country_rule}<>\n";
			}
			else {
				$mes .= "やめました<br>";
				last;
			}
		}
		push @lines, $line;
		++$country;
	}
	if ($country < $m{country}) { # バグで国の方針の数と国の数が合わない時
		$is_rewrite = 1;
		push @lines, "$in{country_mes}<><><>\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#================================================
# NPC名変更
#================================================
sub tp_300 {
	$mes .= "NPC名変更";
	$mes .= qq|<form method="$method" action="$script">|;

	require "$datadir/npc_war_$m{country}.cgi";
	for my $i (0..$#npcs) {
		$mes .= qq|<input type="text" name="npc_$i" value="$npcs[$i]{name}" class="text_box1" style="text-align:right"><br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	require "$datadir/npc_war_$m{country}.cgi";
	for my $i (0..$#npcs){
		&error("NPC名に不正な文字( ,;\"\'&<>\\\/ )が含まれています") if $in{"npc_$i"} =~ /[,;\"\'&<>\\\/]/;
		#"
		&error("NPC名に不正な空白が含まれています") if $in{"npc_$i"} =~ /　/ || $in{"npc_$i"} =~ /\s/;
		&error("NPC名は全角7(半角14)文字までです") if length $in{"npc_$i"} > 14;
		unless (defined $in{"npc_$i"}) {
			$mes .= "やめました<br>";
			&begin;
			return;
		}
	}
	
	my %npc_statuss = (
		max_hp => [999, 500, 250, 150, 100],
		max_mp => [999, 300, 100, 100, 50],
		at     => [700, 400, 200, 100, 50],
		df     => [500, 300, 200, 100, 50],
		mat    => [700, 400, 200, 100, 50],
		mdf    => [500, 300, 200, 100, 50],
		ag     => [800, 500, 200, 100, 50],
		cha    => [800, 500, 200, 100, 50],
		lea    => [500, 350, 150, 80,  40],
		rank   => [$#ranks, $#ranks-2, 8, 5, 3],
	);
	my @npc_weas = (
	#	[0]属性[1]武器No	[2]必殺技
		['無', [0],			[61..65],],
		['剣', [1 .. 5],	[1 .. 5],],
		['槍', [6 ..10],	[11..15],],
		['斧', [11..15],	[21..25],],
		['炎', [16..20],	[31..35],],
		['風', [21..25],	[41..45],],
		['雷', [26..30],	[51..55],],
	);
	
	my $line = qq|\@npcs = (\n|;
	
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$in{"npc_$i"}',\n|;
		
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
	
	open my $fh, "> $datadir/npc_war_$m{country}.cgi";
	print $fh $line;
	close $fh;

	&begin;
}

#================================================
# 国庫設定
#================================================
sub tp_400 {
	$mes .= "国庫設定";
	$mes .= qq|<form method="$method" action="$script">|;
	
	open my $fh, "< $logdir/$m{country}/depot.cgi" or &error("$logdir/$m{country}/depot.cgi が読み込めません");
	my $head_line = <$fh>;
	my($lv_s,$sedai_s,$message_s) = split /<>/, $head_line;
	close $fh;
	$mes .= qq|利用可能\レベル<input type="text" name="lv_s" value="$lv_s" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|利用可能\世代<input type="text" name="sedai_s" value="$sedai_s" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|メッセージ[全角100(半角200)文字まで]<br>・改行は削除されます<br>|;
	$mes .= qq|<textarea name="message_s" cols="60" rows="3" class="textarea1">$message_s</textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}

sub tp_410 {
	&error("国の方針は全角100(半角200)文字までです") if length $in{message_s} > 200;
	if (($in{lv_s} > 0 && $in{lv_s} < 99 && $in{lv_s} !~ /[^0-9]/) && ($in{sedai_s} > 0 && $in{sedai_s} < 99 && $in{sedai_s} !~ /[^0-9]/)) {
		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/depot.cgi" or &error("$logdir/$m{country}/depot.cgiが開けません");
		eval { flock $fh, 2; };
		my $head_line = <$fh>;
		push @lines, "$in{lv_s}<>$in{sedai_s}<>$in{message_s}<>\n";
		push @lines, $_ while <$fh>;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	&begin;
}

#================================================
# 各国設定
#================================================
sub tp_500 {
	if ($time > $w{reset_time}) {
		$mes .= "各国設定は終戦期間中のみ行えます<br>";
		&begin;
		return;
	}
	$mes .= "各国設定";
	$mes .= qq|<form method="$method" action="$script">|;
	my $point = 0;
	unless (-f "$logdir/$m{country}/additional_investment.cgi") {
		open my $fh, "> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi が読み込めません");
		close $fh;
	}
	open my $fh, "< $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi が読み込めません");
	while (my $line = <$fh>) {
		my($since,$name) = split /<>/, $line;
		if ($since + $valid_investment > $w{year}) {
			$point++;
		}
	}
	close $fh;
	$mes .= qq|振り分け可能\pt：$point pt<br>|;
	$mes .= qq|戦争<input type="text" name="war" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|内政<input type="text" name="dom" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|軍事<input type="text" name="mil" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|外交<input type="text" name="pro" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}

sub tp_510 {
	if ($in{war} < 0 || $in{dom} < 0 || $in{mil} < 0 || $in{pro} < 0) {
		$mes .= "0ポイント未満には設定できません";
		&begin;
		return;
	}
	my $point = 0;
	open my $fh, "< $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi が読み込めません");
	while (my $line = <$fh>) {
		my($since,$name) = split /<>/, $line;
		if ($since + $valid_investment > $w{year}) {
			$point++;
		}
	}
	close $fh;
	if ($point > 15) {
		$point = 15;
	}
	if ($in{war} + $in{dom} + $in{mil} + $in{pro} != 20) {
		$mes .= "合計20ポイントに設定してください";
		&begin;
		return;
	}
	if (cut_minus($in{war} - 5) + cut_minus($in{dom} - 5) + cut_minus($in{mil} - 5) + cut_minus($in{pro} - 5) > $point) {
		$mes .= "合計$pointポイント以内の変動に設定してください";
		&begin;
		return;
	}
	
	$cs{modify_war}[$m{country}] = $in{war} - 5;
	$cs{modify_dom}[$m{country}] = $in{dom} - 5;
	$cs{modify_mil}[$m{country}] = $in{mil} - 5;
	$cs{modify_pro}[$m{country}] = $in{pro} - 5;
	
	&write_cs;
	$mes .= "設定しました<br>";
	
	$mes .= "戦争：$cs{modify_war}[$m{country}]<br>内政：$cs{modify_dom}[$m{country}]<br>軍事：$cs{modify_mil}[$m{country}]<br>外交：$cs{modify_pro}[$m{country}]<br>";
	&begin;
}

sub cut_minus {
	$v = shift;
	if ($v < 0) {
		return 0;
	}
	return $v;
}

#================================================
# 会議室名変更
#================================================
sub tp_600 {
	my $bbs_name = $cs{bbs_name}[$m{country}] eq '' ? "$cs{name}[$m{country}]作戦会議室" : $cs{bbs_name}[$m{country}];

	$mes .= qq|会議室名は全角12(半角24)文字まで。半角記号(,;"'&)、空白(ｽﾍﾟｰｽ)は使えません<br>|;
	#"
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|会議室名：<input type="text" name="bbs_name" value="$bbs_name" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="default" value="1">ﾃﾞﾌｫﾙﾄにする<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_610 {
	my $is_rewrite = 0;
	if ($in{default} eq '1') {
		$cs{bbs_name}[$m{country}] = ''; # ﾃﾞﾌｫﾙﾄ

		$mes .= "会議室名をﾃﾞﾌｫﾙﾄに変更しました<br>";

		$is_rewrite = 1;
	}
	elsif ($in{bbs_name}) {
		unless ($cs{bbs_name}[$m{country}] eq $in{bbs_name}) {
			&error("会議室名を記入してください") if $in{bbs_name} eq '';
			&error("会議室名に不正な文字( ,;\"\'&<>\\\/ )が含まれています") if $in{bbs_name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("会議室名に不正な空白が含まれています") if $in{bbs_name} =~ /　/ || $in{bbs_name} =~ /\s/;
			&error("会議室名は全角12(半角24)文字までです") if length $in{bbs_name} > 24;

			$mes .= "会議室名を$in{bbs_name}に変更しました<br>";
			
			$cs{bbs_name}[$m{country}] = $in{bbs_name};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#================================================
# 牢獄名変更
#================================================
sub tp_700 {
	my $prison_name = $cs{prison_name}[$m{country}] ? $cs{prison_name}[$m{country}] : '牢獄';

	$mes .= qq|牢獄名は全角7(半角14)文字まで。半角記号(,;"'&)、空白(ｽﾍﾟｰｽ)は使えません<br>|;
	#"
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|会議室名：<input type="text" name="prison_name" value="$prison_name" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="default" value="1">ﾃﾞﾌｫﾙﾄにする<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_710 {
	my $is_rewrite = 0;
	if ($in{default} eq '1') {
		$cs{prison_name}[$m{country}] = '牢獄'; # ﾃﾞﾌｫﾙﾄ

		$mes .= "牢獄名をﾃﾞﾌｫﾙﾄに変更しました<br>";

		$is_rewrite = 1;
	}
	elsif ($in{prison_name}) {
		unless ($cs{prison_name}[$m{country}] eq $in{prison_name}) {
			&error("牢獄名を記入してください") if $in{prison_name} eq '';
			&error("牢獄名に不正な文字( ,;\"\'&<>\\\/ )が含まれています") if $in{prison_name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("牢獄名に不正な空白が含まれています") if $in{prison_name} =~ /　/ || $in{prison_name} =~ /\s/;
			&error("牢獄名は全角7(半角14)文字までです") if length $in{prison_name} > 14;

			$mes .= "牢獄名を$in{prison_name}に変更しました<br>";
			
			$cs{prison_name}[$m{country}] = $in{prison_name};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= 'やめました<br>';
	}

	&begin;
}

#================================================
# 安楽死
#================================================
sub tp_800 {
	my @lines = &get_country_members($m{country});
	$mes .= '以下のプレイヤーがキャラクター削除を望んでいます';
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table><tr><th></th><th>名前</th></tr>|;
	$mes .= qq|<tr><th><input type="radio" name="suicide" value="" checked/></th><th>いいえ</th></tr>|;
	for my $name (@lines) {
		$name =~ tr/\x0D\x0A//d;
		my %you_datas = &get_you_datas($name);
		if ($pets[$you_datas{pet}][2] eq 'life_down') {
			$mes .= qq|<tr><th><input type="radio" name="suicide" value="$you_datas{name}"/></th><th>$you_datas{name}</th></tr>|;
		}
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="安楽死" class="button_s"></form>|;

	$m{tp} += 10;
}
sub tp_810 {
	if ($in{suicide}) {
		my %you_datas = &get_you_datas($in{suicide});
		if ($pets[$you_datas{pet}][2] eq 'life_down') {
			$mes .= "$you_datas{name}さんを安楽死させました";
			&move_player($you_datas{name}, $you_datas{country}, 'del');
		}
	}
	&begin;
}

#================================================
# 流刑者議決
#================================================
sub tp_900 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "参入直後のﾌﾟﾚｲﾔｰには決議権がありません<br>";
		&begin;
		return;
	}

	$layout = 1;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="やめる" class="button1"></form>|;

	$mes .= "各国$e2j{ceo}の議決により荒らしや多重登録者などを流刑等することができます<br>";
	$mes .= "自己的な考えはNG。まずは各国代表\評議会で相談<br>";
	$mes .= "可決：流刑者を流刑<br>";
	$mes .= "否決：申\請した$e2j{ceo}が国から追放<br>";
	$mes .= '<hr>流刑者ﾘｽﾄ<br>';
	open my $fh, "< $this_file" or &error("$logdir/suspect.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$lv |= 0;
		
		$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$no">|;
		$mes .= qq|<font color="$cs{color}[$country]">$cs{name}[$country]</font>の$e2j{ceo}$nameが『$violator』を$violate[$lv]すべきと思っています<br>|;
		$mes .= qq|理由：$message<br>|;
		$mes .= qq|<input type="radio" name="answer" value="1">賛成 $yes_c票：$yess<br>|;
		$mes .= qq|<input type="radio" name="answer" value="2">反対 $no_c票：$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="投票" class="button_s"></form><hr>|;
	}
	close $fh;

	$m{tp} += 10;
}
sub tp_910 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "参入直後のﾌﾟﾚｲﾔｰには決議権がありません<br>";
		&begin;
		return;
	}
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		$mes .= 'やめました<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		$lv |= 0;
		
		if ($cmd eq $no) {
			# 申請したのが自分で反対なら申請を取消
			if ($m{name} eq $name && $in{answer} eq '2') {
				$mes .= "$violatorの$violate[$lv]者申\請を取消ました<br>";
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("自分の評議には投票することができません");
			}

			my $v_id = unpack 'H*', $violator;
			# 自動削除などで消えていた場合は除外
			if (!-f "$userdir/$v_id/user.cgi") {
				$mes .= "$violatorというﾌﾟﾚｲﾔｰが存在しません<br>";
				next;
			}

			# すでに自分がどちらかに入れていた場合のために、一回白紙にする
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{country} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{country} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($in{answer} eq '1') {
				$new_yess .= "$m{country},";
				$mes .= "$violatorの$violate[$lv]に賛成します<br>";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{country},";
				$mes .= "$violatorの$violate[$lv]に反対します<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_c = @yes_c;
			my $no_c  = @no_c;
			
			if ($yes_c >= $need_vote_violator[$lv]) {
				if($violator eq $admin_name){
					&write_world_news("<b>【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$datas{country}]の$violatorが$violate[$lv]になりました…と思ったか、バカめ</b>");
					$mes .= "賛成が$need_vote_violator票以上になったので$violatorは$violate[$lv]となります…と思ったの？バカなの？死ぬの？<br>";
					for my $n (@yes_c) {
						&regist_you_data($cs{ceo}[$n],'shogo','★反逆者');
						&regist_you_data($cs{ceo}[$n],'shogo_t','★反逆者');
						&regist_you_data($cs{ceo}[$n],'trick_time',$time + 30*24*3600);
					}
				}else{
					if ($lv > 0) {
						my %datas = &get_you_datas($v_id, 1);
						if ($lv > 1) {
							# 違反者リストに追加
							open my $fh2, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgiﾌｧｲﾙが開けません");
							open my $afh, "< $userdir/$v_id/access_log.cgi" or &error("$userdir/$v_id/access_log.cgiﾌｧｲﾙが開けません");
							while ($aline = <$afh>) {
								my ($aaddr, $ahost, $aagent)  = split /<>/, $aline;
								print $fh2 $aagent =~ /DoCoMo/ || $aagent =~ /KDDI|UP\.Browser/
									|| $aagent =~ /J-PHONE|Vodafone|SoftBank/ ? "$aagent\n" : "$aaddr\n";
							}
							close $afh;
							print $fh2 $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
								|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
							close $fh2;
						}
						&move_player($violator, $datas{country}, 'trash');
					} else {
						my %datas = &get_you_datas($v_id, 1);
						&move_player($violator, $datas{country}, 0);
						&regist_you_data($datas{name}, 'wt', 7 * 24 * 3600);
						&regist_you_data($datas{name}, 'country', 0);
						&regist_you_data($datas{name}, 'lib', '');
						&regist_you_data($datas{name}, 'tp', 0);
						&regist_you_data($datas{name},'silent_time',$time+7*24*3600);
						&regist_you_data($datas{name},'silent_kind',0);
					}
					&write_world_news("<b>【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$datas{country}]の$violatorが$violate[$lv]になりました<br>理由：$message</b>");
					$mes .= "賛成が$need_vote_violator票以上になったので$violatorは$violate[$lv]となります<br>";
				}
			}
			elsif ($no_c > $w{country} - $need_vote_violator[$lv]) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # 申請した人が消えていた場合
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$country]の$e2j{ceo}$nameが国外追放となりました</b>", 1, $name);
				$mes .= "反対が$need_vote_violator票以上になったので$nameが国外追放となります<br>";
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>$lv<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#================================================
# 流刑者申請
#================================================
sub tp_1000 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "参入直後のﾌﾟﾚｲﾔｰには申\請権がありません<br>";
		&begin;
		return;
	}
	$mes .= qq|自分が申\請したのを取消場合は、流刑者議決で反対に入れてください<br>|;
	$mes .= qq|<hr>流刑者申\請<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|名前：<input type="text" name="violator" value="$in{violator}" class="text_box1"><br>|;
	$mes .= qq|理由[全角40(半角80)文字まで]：<br><input type="text" name="message" class="text_box_b">|;
	for my $i (0..$#violate) {
		$mes .= qq|<input type="radio" name="lv" value="$i">$violate[$i]|;
	}
	$mes .= qq|<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="申\請する" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_1010 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "参入直後のﾌﾟﾚｲﾔｰには申\請権がありません<br>";
		&begin;
		return;
	}
	if ($in{violator} && $in{message}) {
		&error('文字数が長すぎます全角40(半角80)文字まで') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			push @lines, $_ while <$fh>;
			my($last_no) = (split /<>/, $lines[0])[0];
			++$last_no;
			push @lines, "$last_no<>$m{name}<>$m{country}<>$in{violator}<>$in{message}<>$m{country},<><>$in{lv}<>\n";
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			$mes .= "$in{violator}を$in{message}の理由で$violate[$in{lv}]者として申\請しました<br>";
		}
		else {
			$mes .= "$in{violator}というﾌﾟﾚｲﾔｰが存在しません<br>";
		}
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#================================================
# 多重者ﾁｪｯｸ
#================================================
sub tp_1100 {
	if (!$is_ceo_delete || !$is_ceo_watch_multi) {
		&begin;
		return;
	}

	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		open my $fh, "< $userdir/$id/user.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;
		
		my %p = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$p{$k} = $v;
		}
		($p{addr}, $p{host}, $p{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name shogo country addr host agent ldate/) {
			$line .= "$p{$k}<>";
		}
		push @lines, "$line\n";
	}
	closedir $dh;
	
	@lines = map { $_->[0] }
		sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] }
			map { [$_, split /<>/] } @lines;
	
	$layout = 1;
	$mes .= "IPｱﾄﾞﾚｽ、ﾎｽﾄ名、ﾌﾞﾗｳｻﾞが同じ人ﾘｽﾄ<br>";
	$mes .= "以下の状況によりﾘｽﾄに載ることがあるので、このﾘｽﾄに表示された人＝多重と関連付けるのは注意!!<br>";
	$mes .= "※管理権限を持っているﾌﾟﾚｲﾔｰは、他ﾌﾟﾚｲﾔｰでﾛｸﾞｲﾝすることができる<br>";
	$mes .= "※同じ地域や学校などの公共施設からﾛｸﾞｲﾝしている場合<br>";
	$mes .= "※携帯ﾌﾟﾚｲﾔｰの場合はもしかしたら被る可能\性があるので要確認!(携帯の判別はﾎｽﾄ名で確認)<br>";
	$mes .= "あからさまな多重以外は、とりあえず本人に確認してみること<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="violator" value="" checked>やめる|;
	$mes .= $is_mobile ? qq|<hr>名前/所属国/IPｱﾄﾞﾚｽ/ﾎｽﾄ名/ﾌﾞﾗｳｻﾞ/更新日<br>|
		: qq|<table class="table1"><tr><th>名前</th><th>所属国</th><th>IPｱﾄﾞﾚｽ</th><th>ﾎｽﾄ名</th><th>更新日<br></th></tr>|;
	
	my $b_line  = '';
	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $is_same = 0;
	for my $line (@lines) {
		my($sid, $sname, $sshogo, $scountry, $saddr, $shost, $sagent, $sldate) = split /<>/, $line;
		if ($saddr eq $b_addr && $shost eq $b_host && $sagent eq $b_agent
			|| ($sagent eq $b_agent && ($sagent =~ /DoCoMo/ || $sagent =~ /KDDI|UP\.Browser/ || $sagent =~ /J-PHONE|Vodafone|SoftBank/)) ) {

				unless ($is_same) {
					$is_same = 1;
					my($bid, $bname, $bshogo, $bcountry, $baddr, $bhost, $bagent, $bldate) = split /<>/, $b_line;
					$bname .= "[$bshogo]" if $bshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$bname">$bname/<font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]/$baddr/$bhost/$bldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$bname">$bname</td><td><font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font></td><td>$baddr</td><td>$bhost</td><td>$bldate<br></td></tr>|;
				}
					$sname .= "[$sshogo]" if $sshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$sname">$sname/<font color="$cs{color}[$scountry]">$cs{name}[$scountry]/$saddr/$shost/$sldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$sname">$sname</td><td><font color="$cs{color}[$scountry]">$cs{name}[$scountry]</font></td><td>$saddr</td><td>$shost</td><td>$sldate<br></td></tr>|;
		}
		else {
			$b_line  = $line;
			$b_addr  = $saddr;
			$b_host  = $shost;
			$b_agent = $sagent;
			$is_same = 0;
		}
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="流刑者申\請" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_1110 {
	if ($in{violator}) {
		$m{tp} = 900;
		&{ 'tp_'.$m{tp} };
	}
	else {
		&begin;
	}
}

1; # 削除不可
