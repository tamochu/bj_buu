require './lib/move_player.cgi';
my $this_file = "$logdir/$m{country}/violator.cgi";
#=================================================
# 国設定 Created by Merino
#=================================================

# 追放決定票(国代表者は5人)
my $need_vote_violator = 2;

# 一括送信に必要な費用
my $need_money = 3000;

# 追放拘束時間
my $violator_penalty = 3 * 24 * 3600;
# 国外退去拘束時間
my $deportation_penalty = 12 * 3600;

# 寄付額
my $investment_money = 1000000;

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
	elsif (!&is_daihyo) {
		$mes .= '国の代表\者でないと行うことができません<br>';
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
		$mes .= 'このｺﾏﾝﾄﾞは、国の代表\者のみ行うことができます<br>';
		$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="代表\評議会" class="button1"></form>|;
	}
	
	&menu('やめる', '代表\評議会', '国内一括送信', '税率調整', '追放者議決', '追放者申\請', '国代表\を辞任','国に寄付', '一斉表作成');
}
sub tp_1 {
	return if &is_ng_cmd(1..8);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}


#=================================================
# 評議会入り口
#=================================================
sub tp_100 {
	$mes .= qq|各国の代表\者のみ入室することができます<br>|;
	$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="代表\評議会" class="button1"></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	&begin;
}

#=================================================
# 一括送信
#=================================================
sub tp_200 {
	$mes .= "この国に所属するﾌﾟﾚｲﾔｰ全員に手紙を送ることができます<br>";
	$mes .= "１回の送信に $need_money Gかかります<br>";

	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="一括送信/やめる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	if ($in{comment}) {
		&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;

		if ($m{money} >= $need_money) {
			$in{comment} .= "<hr>【$cs{name}[$m{country}]全員に送信】";
			
			open my $fh_m, "< $logdir/$m{country}/member.cgi";
			while (my $line_m = <$fh_m>) {
				$line_m =~ tr/\x0D\x0A//d;
				
				my $y_id = unpack 'H*', $line_m;
				next unless -f "$userdir/$y_id/letter.cgi";
				
				my @lines = ();
				open my $fh, "+< $userdir/$y_id/letter.cgi" or &error('一括送信に失敗しました');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					push @lines, $line;
					last if @lines >= $max_log-1;
				}
				unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$in{comment}<>$m{icon}<>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				# 手紙があるよﾌﾗｸﾞをたてる
				my $letters = 0;
				if(-f "$userdir/$send_id/letter_flag.cgi"){
					open my $fh9, "< $userdir/$y_id/letter_flag.cgi";
					my $line = <$fh9>;
					($letters) = split /<>/, $line;
					close $fh9;
				}
				$letters++;
				
				open my $fh9, "> $userdir/$y_id/letter_flag.cgi";
				print $fh9 "$letters<>";
				close $fh9;
			}
			close $fh_m;
			
			$m{money} -= $need_money;
			$mes .= "$need_money G支払い、$cs{name}[$m{country}]全員に手紙を送信しました<br>";
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}


#=================================================
# 税率変更
#=================================================
sub tp_300 {
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{tax} [1%～99%]：<input type="text" name="tax" value="$cs{tax}[$m{country}]" class="text_box_s" style="text-align:right">%<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="変更する" class="button1"></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	if ($in{tax} && $cs{tax}[$m{country}] ne $in{tax}) {
		&error("$e2j{tax}を半角数字で記入してください") if $in{tax} eq '' || $in{tax} =~ /[^0-9]/;
		&error("$e2j{tax}は1% ～ 99%までです") if $in{tax} < 1 || $in{tax} > 99;

		$mes .= "$e2j{tax}を $in{tax} %に変更しました<br>";
		$cs{tax}[$m{country}] = $in{tax};
		&write_cs;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}


#=================================================
# 追放者議決
#=================================================
sub tp_400 {
	$layout = 1;

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="やめる" class="button1"></form>|;
	
	$mes .= "議決により荒らしや国の方針に従わない者を自国から追放することができます<br>";
	$mes .= "賛成が$need_vote_violator票以上：追放者を自国から追放<br>";
	$mes .= "反対が$need_vote_violator票以上：申\請した代表\者が国から追放<br>";
	$mes .= "<hr>追放者ﾘｽﾄ<br>";
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $w_span) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$no">|;
		$mes .= $w_span == 1 ? qq|$nameが『$violator』を追放すべきと思っています<br>|:qq|$nameが『$violator』を国外退去処分すべきと思っています<br>|;
		$mes .= qq|理由：$message<br>|;
		$mes .= qq|<input type="radio" name="answer" value="1" checked>賛成 $yes_c票：$yess<br>|;
		$mes .= qq|<input type="radio" name="answer" value="2">反対 $no_c票：$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="投票" class="button_s"></form><hr>|;
	}
	close $fh;

	$m{tp} += 10;
}
sub tp_410 {
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		$mes .= 'やめました<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $w_span) = split /<>/, $line;
		
		if ($cmd eq $no) {
			# 申請したのが自分で反対なら申請を取消
			if ($m{name} eq $name && $in{answer} eq '2') {
				$mes .= "$violatorの追放申\請を取消ました<br>";
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
			# 自国にいない場合は除外
			elsif ( !&is_my_country($violator) ) {
				$mes .= "$violatorというﾌﾟﾚｲﾔｰは$cs{name}[$m{country}]に所属しておりません<br>";
				next;
			}

			# すでに自分がどちらかに入れていた場合のために、一回白紙にする
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{name} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{name} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($in{answer} eq '1') {
				$new_yess .= "$m{name},";
				$mes .= "$violatorの追放に賛成します<br>";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{name},";
				$mes .= "$violatorの追放に反対します<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_cn = @yes_c;
			my $no_cn  = @no_c;
			my $penalty_time = $w_span == 1 ? $violator_penalty : $deportation_penalty;
			
			my $vote_disagree = 5 - $need_vote_violator;
			
			if ($yes_cn >= $need_vote_violator) {
				my %datas = &get_you_datas($v_id, 1);
				&move_player($violator, $datas{country}, 0);

				&regist_you_data($violator, 'wt', $penalty_time);
				&regist_you_data($violator, 'country', 0);
				&regist_you_data($violator, 'lib', '');
				&regist_you_data($violator, 'tp', 0);
				if($w_span == 2){
					# 代表ﾎﾟｲﾝﾄ半分
					for my $k (qw/war dom mil pro/) {
						my $kc = $k . "_c";
						&regist_you_data($violator, $kc, 0);
					}
				}

				&write_world_news("【議決】$cs{name}[$m{country}]の代表\者達の評議により、$violatorが国外追放となりました", 1, $violator);
				$mes .= "賛成が$need_vote_violator票以上になったので$violatorが追放されました<br>";
			}
			elsif ($no_cn >= $vote_disagree) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # 申請した人が消えていた場合
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', $penalty_time);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);
				if($w_span == 2){
					# 代表ﾎﾟｲﾝﾄ半分
					for my $k (qw/war dom mil pro/) {
						my $kc = $k . "_c";
						&regist_you_data($name, $kc, 0);
					}
				}

				&write_world_news("【議決】$cs{name}[$m{country}]の代表\者達の評議により、$nameが国外追放となりました", 1, $name);
				$mes .= "反対が$vote_desagree票以上になったので$nameが追放されました<br>";
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>\n";
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

#=================================================
# 追放者申請
#=================================================
sub tp_500 {
	$mes .= qq|自国の代表\者達の議決により自国のﾌﾟﾚｲﾔｰを追放することができます<br>|;
	$mes .= qq|自分が申\請したのを取消場合は、追放者議決で反対に入れてください<br>|;
	$mes .= qq|<hr>追放者申\請<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|名前：<input type="text" name="violator" class="text_box1"><br>|;
	$mes .= qq|理由[全角40(半角80)文字まで]：<br><input type="text" name="message" class="text_box_b">|;
	$mes .= qq|<br><input type="radio" name="w_span" value="1" checked>追放<br>|;
	$mes .= qq|<input type="radio" name="w_span" value="2">国外退去<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="申\請する" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_510 {
	if ($in{violator} && $in{message}) {
		&error('文字数が長すぎます全角40(半角80)文字まで') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
			if ( &is_my_country($in{violator}) ) {
				my @lines = ();
				open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
				eval { flock $fh, 2; };
				push @lines, $_ while <$fh>;
				my($last_no) = (split /<>/, $lines[0])[0];
				++$last_no;
				push @lines, "$last_no<>$m{name}<>$m{country}<>$in{violator}<>$in{message}<>$m{name},<><>$in{w_span}<>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				$mes .= "$in{violator}を$in{message}の理由で追放者として申\請しました<br>";
			}
			else {
				$mes .= "$cs{name}[$m{country}]に$in{violator}というﾌﾟﾚｲﾔｰが所属していません<br>";
			}
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


#=================================================
# 国の代表辞任
#=================================================
sub tp_600 {
	$mes .= "現在代表\となっている代表\ﾎﾟｲﾝﾄだけがﾘｾｯﾄされます<br>";
	$mes .= "$e2j{ceo}の辞任は$e2j投票から辞任してください<br>";
	$mes .= "国の代表\者を辞任しますか?<br>";
	&menu('やめる', '辞任する');

	$m{tp} += 10;
}
sub tp_610 {
	return if &is_ng_cmd(1);

	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$mes .= "$e2j{ceo}の辞任は$e2j{ceo}投票で行ってください<br>";
		&begin;
		return;
	}

	for my $k (qw/war pro dom mil/) {
		if ($cs{$k}[$m{country}] eq $m{name}) {
			$cs{$k}[$m{country}] = '';
			$cs{$k.'_c'}[$m{country}] = 0;
			&write_cs;
			
			$m{$k.'_c'} = 0;
			&mes_and_world_news("$e2j{$k}を辞任しました", 1);
			last;
		}
	}
	
	&begin;
}

#=================================================
# 国に寄付
#=================================================
sub tp_700 {
	$mes .= "国に $investment_money G寄付して国を強くします<br>";
	$mes .= "国に寄付しますか?<br>";
	&menu('やめる', '寄付する');

	$m{tp} += 10;
}
sub tp_710 {
	return if &is_ng_cmd(1);

	if ($m{money} < $investment_money) {
		$mes .= "お金が足りません<br>";
		&begin;
		return;
	}
	
	unless (-f "$logdir/$m{country}/additional_investment.cgi") {
		open my $fh, "> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi が読み込めません");
		close $fh;
	}
	open my $fh, ">> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi が読み込めません");
	print $fh "$w{year}<>$m{name}<>\n";
	close $fh;
	
	$m{money} -= $investment_money;
	
	&begin;
}

#=================================================
# 一斉表作成
#=================================================
sub wl {
	my ($hour, $min, $min2) = @_;
	$min += $min2;
	if ($min >= 60) {
		# 分が 60 以上なら時を増やして分を 60 未満に
		$hour += int($min / 60);
		$min = $min % 60;
	}
	return sprintf("%02d:%02d", $hour, $min);

}
sub tp_800 {
	$layout = 2;

	# 一斉表テンプレートの読み込み
	# ファイルがなければデフォルトテンプレート
	my @templates = ();
	my $p_id = unpack 'H*', $m{name};
	if (!(-e "$userdir/$p_id/isseihyo.cgi") || (-s "$userdir/$p_id/isseihyo.cgi") < 1) {
		push(@templates, "通常型(初期テンプレ)<>0;長期発<>15;通常発<>23;倍速発<>25;布告・停戦発<>45;一斉凸<>47;停戦着<>\n");
		open my $fh, "> $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ﾌｧｲﾙが読み込めません");
		print $fh $templates[0];
		close $fh;
	}
	else {
		open my $fh, "< $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ﾌｧｲﾙが読み込めません");
		while (my $l = <$fh>) {
			push(@templates, $l) if $l ne "\n";
		}
		close $fh;
	}

	my @wars_type = ();
	my @text = ();
	for my $i (0 .. $#templates) {
		my @line = split("<>", $templates[$i]);
		push(@wars_type, $line[0]); # テンプレの名前を取得
		$templates[$i] =~ s|<>|<>\n|g; # ユーザーが編集しやすいように改行
	}

	my ($min, $hour) = (localtime($time))[1 .. 2];
	my $now = sprintf("%02d:%02d", $hour, $min);

	# 分を将来で一番近い 5 か 0 に丸めたさらに20分後
	my $min_low = $min - int(($min * 0.1)) * 10;
	$min += $min_low < 5 ? 25 - $min_low : 30 - $min_low;
	if ($min >= 60) {
		# 分が 60 以上なら時を増やして分を 60 未満に
		$hour += int($min / 60);
		$min = $min % 60;
	}

	my $ttime = sprintf("%02d:%02d", $hour, $min);

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|開始時刻：<input type="text" name="time" value="$ttime" class="text_box_s"> 現在：$now<br><br>|;

	$mes .= qq|目標：<select name="target">|;
	for my $target (1 .. $w{country}) {
		$mes .= qq|<option value="$target" label="$cs{name}[$target]">$cs{name}[$target]</option>|;
	}
	$mes .= qq|</select><br><br>|;

	$mes .= qq|テンプレ：<select name="type">|;
	for my $type (0 .. $#wars_type) {
		$mes .= qq|<option value="$type" label="$wars_type[$type]">$wars_type[$type]</option>|;
	}
	$mes .= qq|</select><br><br>|;

	$mes .= qq|布告人員：<input type="text" name="hukoku" value="$m{name}" class="text_box_s"><br><br>|;
	$mes .= qq|停戦人員：<input type="text" name="teisen" value="" class="text_box_s"><br><br>|;

	$mes .= qq|ｺﾒﾝﾄ：<select name="text">|;
	$mes .= qq|<option value="" label="----">特になし</option>|;
	$mes .= qq|<option value="停戦役募集中" label="停戦役募集中">停戦役募集中</option>|;
	$mes .= qq|</select><br><br>|;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="作成する" class="button1"><br><br>|;
	$mes .= qq|<hr>各行末には必ず&lt;&gt;を書くこと<br>1行目が一斉表\の名称<br>セミコロンの左側に開始時刻を基準にしたn分後を指定、<br>セミコロンの右側にその時刻の行動を書く<br>|;

	for my $i (0 .. 4) {
		$mes .= qq|<textarea name="text_$i" rows="10" cols="25">$templates[$i]</textarea><br>|;
	}
	$mes .= qq|</form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_810 {
	if ($in{time}) {
		my @templates = ();
		my $p_id = unpack 'H*', $m{name};
		open my $fh, "> $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ﾌｧｲﾙが読み込めません");
		for my $i (0 .. 4) {
			$in{"text_$i"} =~ s|&lt;&gt;|<>|g;
			$in{"text_$i"} =~ s|&#59||g;
			print $fh qq/$in{"text_$i"}\n/;
			push(@templates, $in{"text_$i"});
		}
		close $fh;

		my ($hour, $min) = split(/:/, $in{time});
		my $sub_mes = "目標：$cs{name}[$in{target}]\n\n";
		my @line = split( /<>/, $templates[$in{type}] );
		for my $i (1 .. $#line) {
			my @array = split( /;/, $line[$i]);
			$sub_mes .= &wl($hour, $min, $array[0])." $array[1]\n";
		}
		$sub_mes .= "\n布告：$in{hukoku}\n";
		$sub_mes .= "停戦：$in{teisen}";
		$sub_mes .= "\n\n$in{text}" if $in{text};

		$mes .= qq|<textarea name="text_$i" rows="15" cols="35">$sub_mes</textarea><br>|;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#=================================================
# 追放しようとしている人は自国の人? 1(true) or 0(false)
#=================================================
sub is_my_country {
	my $name = shift;
	open my $fh, "< $logdir/$m{country}/member.cgi" or &error("$logdir/$m{country}/member.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		return 1 if $line eq $name;
	}
	close $fh;
	return 0;
}


1; # 削除不可
