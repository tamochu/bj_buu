$mes .= qq|宝ｸｼﾞ【$m{lot}】<br>| if $is_mobile && $m{lot};
#================================================
# 宝くじ Created by Merino
#================================================

# 宝くじの値段
my $need_money = 1000;

# 何日おきに当選発表するか(日)
my $lot_cycle_day = 7;

my $lot_denominator = 100;

# 武器賞の賞品
my @wea_nos = (5,10,15,20,25,31,32);
my @wea_sub_nos = (4,9,14,19,24);

# ﾀﾏｺﾞ賞の賞品
my @egg_nos = (37,38,40);
my @egg_sub_nos = (3,35,36,39,41);

# ﾍﾟｯﾄ賞の賞品
my @pet_nos = (21,62,63,125,127,168,183);
my @pet_sub_nos = (7,8,17,18,64,151,184);


#================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($w{player} < 30) { # ﾌﾟﾚｲﾔｰが30人未満
		$mes .= '準備中だよ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	open my $fh, "+< $logdir/lot.cgi" or &error('宝くじﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my($lot_next_time, $round, $atari1,$no1,$no1_sub, $atari2,$no2,$no2_sub, $atari3,$no3,$no3_sub, $atari4,$no4,$no4_sub, $atari5,$no5,$no5_sub, $next_no1,$next_no2,$next_no3,$next_no4,$next_no5, $next_no1_sub,$next_no2_sub,$next_no3_sub,$next_no4_sub,$next_no5_sub) = split /<>/, $line;
	$round++;
	$round  = $round > 9 ? 1 : $round;
	
	# 当選発表時間
	if ($time > $lot_next_time) {
		# 宝くじの景品設定
		$no1 = $next_no1;
		$no2 = $next_no2;
		$no3 = $next_no3;
		$no4 = $next_no4;
		$no5 = $next_no5;
		$no1_sub = $next_no1_sub;
		$no2_sub = $next_no2_sub;
		$no3_sub = $next_no3_sub;
		$no4_sub = $next_no4_sub;
		$no5_sub = $next_no5_sub;
		$next_no1 = $wea_nos[int(rand(@wea_nos))];
		$next_no2 = $egg_nos[int(rand(@egg_nos))];
		$next_no3 = int(rand(21)+20) * 10000;
		$next_no4 = $pet_nos[int(rand(@pet_nos))];
		$next_no5 = int(rand(21)+20) * 10000;
		$next_no1_sub = $wea_sub_nos[int(rand(@wea_sub_nos))];
		$next_no2_sub = $egg_sub_nos[int(rand(@egg_sub_nos))];
		$next_no3_sub = int(rand(21)+20) * 1000;
		$next_no4_sub = $pet_sub_nos[int(rand(@pet_sub_nos))];
		$next_no5_sub = int(rand(21)+20) * 1000;
		
		$lot_next_time = int($time + 24 * 3600 * $lot_cycle_day);
		$atari1 = $round . sprintf("%03d", int(rand($lot_denominator)) );
		$atari2 = $round . sprintf("%03d", int(rand($lot_denominator)) );
		$atari3 = $round . sprintf("%03d", int(rand($lot_denominator)) );
		$atari4 = $round . sprintf("%03d", int(rand($lot_denominator)) );
		$atari5 = $round . sprintf("%03d", int(rand($lot_denominator)) );
		
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh "$lot_next_time<>$round<>$atari1<>$no1<>$no1_sub<>$atari2<>$no2<>$no2_sub<>$atari3<>$no3<>$no3_sub<>$atari4<>$no4<>$no4_sub<>$atari5<>$no5<>$no5_sub<>$next_no1<>$next_no2<>$next_no3<>$next_no4<>$next_no5<>$next_no1_sub<>$next_no2_sub<>$next_no3_sub<>$next_no4_sub<>$next_no5_sub<>";
		close $fh;
		
		&write_send_news(qq|<font color="#FFCC00">【宝くじ当選発表\】<br>武器賞【$atari1】$weas[$no1][1] (前後$weas[$no1_sub][1])<br>ﾀﾏｺﾞ賞【$atari2】$eggs[$no2][1] (前後$eggs[$no2_sub][1])<br>金貨賞【$atari3】$no3 G (前後$no3_sub G)<br>ﾍﾟｯﾄ賞【$atari4】$pets[$no4][1] (前後$pets[$no4_sub][1])<br>ｺｲﾝ賞【$atari5】$no5 ｺｲﾝ (前後$no5_sub ｺｲﾝ)</font>|);
	}
	close $fh;
	
	# 当選者が来たよ賞品を送るよ
	my $mylot = $m{lot};
	if ($atari1 eq $mylot) {
		$mes .= "おお!当選おめでと!賞品の $weas[$no1][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 1, $no1, $weas[$no1][4], 10, 1);
		&write_send_news(qq|$m{name}が武器賞に当選しました|);
		$m{lot} = '';
	} elsif ($atari1 == $mylot - 1 || $atari1 == $mylot + 1) {
		$mes .= "惜しかったね!副賞の $weas[$no1_sub][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 1, $no1_sub, $weas[$no1_sub][4], 10, 1);
		$m{lot} = '';
	}
	if ($atari2 eq $mylot) {
		$mes .= "おお!当選おめでと!賞品の $eggs[$no2][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 2, $no2, 0, 0, 1);
		&write_send_news(qq|$m{name}がﾀﾏｺﾞ賞に当選しました|);
		$m{lot} = '';
	} elsif ($atari2 == $mylot - 1 || $atari2 == $mylot + 1) {
		$mes .= "惜しかったね!副賞の $eggs[$no2_sub][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 2, $no2_sub, 0, 0, 1);
		$m{lot} = '';
	}
	if ($atari3 eq $mylot) {
		$mes .= "おお!当選おめでと!賞品の $no3 Gは送金しておいたよ<br>";
		&send_money($m{name}, '宝くじ屋', $no3);
		&write_send_news(qq|$m{name}が金貨賞に当選しました|);
		$m{lot} = '';
	} elsif ($atari3 == $mylot - 1 || $atari3 == $mylot + 1) {
		$mes .= "惜しかったね!副賞の $no3_sub Gは送金しておいたよ<br>";
		&send_money($m{name}, '宝くじ屋', $no3_sub);
		$m{lot} = '';
	}
	if ($atari4 eq $mylot) {
		$mes .= "おお!当選おめでと!賞品の $pets[$no4][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 3, $no4, 0, 0, 1);
		&write_send_news(qq|$m{name}がﾍﾟｯﾄ賞に当選しました|);
		$m{lot} = '';
	} elsif ($atari4 == $mylot - 1 || $atari4 == $mylot + 1) {
		$mes .= "惜しかったね!副賞の $pets[$no4_sub][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 3, $no4_sub, 0, 0, 1);
		$m{lot} = '';
	}
	if ($atari5 eq $mylot) {
		$mes .= "おお!当選おめでと!賞品の $no5 ｺｲﾝをあげるね<br>";
		$m{coin} += $no5;
		&write_send_news(qq|$m{name}がｺｲﾝ賞に当選しました|);
		$m{lot} = '';
	} elsif ($atari5 == $mylot - 1 || $atari5 == $mylot + 1) {
		$mes .= "惜しかったね!副賞の $no5_sub ｺｲﾝをあげるね<br>";
		$m{coin} += $no5_sub;
		$m{lot} = '';
	}
	
	my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
	++$lmonth;
	
	my $round_old = $round == 1 ? 9 : $round -1;
	$mes .= qq|<font color="#FFCC00">【第$round_old回の当選番号】<br>武器賞【$atari1：$weas[$no1][1] (前後$weas[$no1_sub][1])】<br>ﾀﾏｺﾞ賞【$atari2：$eggs[$no2][1] (前後$eggs[$no2_sub][1])】<br>金貨賞【$atari3：$no3 G (前後$no3_sub G)】<br>ﾍﾟｯﾄ賞【$atari4：$pets[$no4][1] (前後$pets[$no4_sub][1])】<br>ｺｲﾝ賞【$atari5：$no5 ｺｲﾝ (前後$no5_sub ｺｲﾝ)】<br></font>|;
	$mes .= qq|<font color="#FFCCCC">【第$round回の賞品】<br>武器賞【$weas[$next_no1][1] (前後$weas[$next_no1_sub][1])】<br>ﾀﾏｺﾞ賞【$eggs[$next_no2][1] (前後$eggs[$next_no2_sub][1])】<br>金貨賞【$next_no3 G (前後$next_no3_sub G)】<br>ﾍﾟｯﾄ賞【$pets[$next_no4][1] (前後$pets[$next_no4_sub][1])】<br>ｺｲﾝ賞【$next_no5 ｺｲﾝ (前後$next_no5_sub ｺｲﾝ)】<br></font>|;
	$mes .= "宝くじは１枚 $need_money Gだよ<br>";
	$mes .= "第$round回の当選発表\は $lmonth月$lday日$lhour時$lmin分頃だよ<br>";
	$mes .= '新しいのを買う場合は、今持っているくじを引き取るよ<br>' if $m{lot};
	
	&menu('やめる', '買う');
}

sub tp_1 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $need_money) {
		open my $fh, "< $logdir/lot.cgi" or &error('宝くじﾌｧｲﾙが読み込めません');
		my $line = <$fh>;
		close $fh;
		my($lot_next_time, $round) = (split /<>/, $line)[0..1];
		++$round;
		$round  = $round > 9 ? 1 : $round;
		
		my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
		++$lmonth;
		
		$m{lot} = $round . sprintf("%03d", int(rand($lot_denominator)) );
		$m{money} -= $need_money;
		
		$mes .= "まいど!<br>当選発表\は $lmonth月$lday日$lhour時$lmin分頃だよ<br>";
	}
	else {
		$mes .= "お金がなければ夢も買えやしないよ<br>";
	}
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}


1; # 削除不可
