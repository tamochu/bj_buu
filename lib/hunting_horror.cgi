my $this_monster_file = "$logdir/monster/horror.cgi";
#=================================================
# 肝試し Created by Merino
#=================================================

# ｱｲﾃﾑ拾う確率(分の1)
my $get_item_par = 20;

my @egg_nos = (12, 22, 24, 26, 35, 39);

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($hour < 1 || $hour > 3) {
		$mes .= "肝試しする時間じゃないね<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "肝試しするのに$e2j{hp}が少なすぎます<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{turn} = 0;
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= '肝試しに行きます<br>';
	$mes .= 'どこに向かいますか?<br>';
	
	my $m_st = &m_st;
	my @menus = ('やめる', '行く');
	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		&_get_hunt_you_data;
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#=================================================
# Get 相手データ
#=================================================
sub _get_hunt_you_data {
	my $line = '';
	open my $fh, "< $this_monster_file" or &error("$this_monster_fileﾌｧｲﾙがありません");
	$line = <$fh>;
	close $fh;

	my @datas = split /<>/, $line;
	my $i = 0;
	for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
		$y{$k} = $datas[$i];
		++$i;
	}
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};
	$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
	$y{wea_name} = '';
	$y{gua} = 0;
	if ( rand($m{cha}) < rand($y{cha}) ) {
		$m{tp} = 200;
		$mes .= "$y{name} が襲いかかってきました<br>";
		&n_menu;
	}
	else {
		$m{tp} = 100;
		$mes .= "$y{name} がいます<br>";
		&menu('戦う','逃げる');
	}
}

#=================================================
# 戦う or 逃げる
#=================================================
sub tp_100 {
	if ($cmd eq '0') {
		$mes .= "$y{name} と戦います<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand($y{ag}) ) {
		$mes .= '逃げました<br>';
		&begin;
	}
	else {
		$mes .= '逃げられませんでした。戦闘態勢に入ります<br>';
		$m{tp} = 200;
		&n_menu;
	}
}

#=================================================
# 戦闘
#=================================================
sub tp_200 {
	require './lib/hunting_battle.cgi';

	# 負け
	if ($m{hp} <= 0) {
		$m{pop_vote}++;
		$mes .= "投票権を拾った<br>";
		$m{act} += 20;
		&refresh;
		&n_menu;
	}
	# 勝ち
	elsif ($y{hp} <= 0) {
		$m{pop_vote}++;
		$mes .= "投票権を拾った<br>";
		# ﾄｰﾀﾙｽﾃｰﾀｽが自分より弱者だと経験値少なめ
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		my $vv = int(3000 + $y_st * 0.3);
		
		$m{exp} += $v;
		$m{act} += 20;
		$m{egg_c} += int(rand(60)+70) if $m{egg};
		$m{money} += $vv;
		$mes .= "$v の$e2j{exp}と $vv Gを手に入れました<br>";
		
		# ｱｲﾃﾑｹﾞｯﾄ
		&_get_item if int(rand($get_item_par)) == 0;
		
		$mes .= '肝試しを続けますか?<br>';
		&menu('続ける','やめる');
		$m{tp} += 10;
	}
}

#=================================================
# 継続 or やめる
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}else {
		$mes .= '肝試しを終了します<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# ｱｲﾃﾑ(ﾀﾏｺﾞ)拾う処理
#=================================================
sub _get_item {
	my $egg_no = $egg_nos[int(rand(@egg_nos))];
	
	$mes .= qq|<font color="#FFCC00">$eggs[$egg_no][1]を拾いました!</font><br>|;
	if ($m{is_full}) {
		$mes .= "しかし、預かり所がいっぱいなので$eggs[$egg_no][1]をあきらめました<br>";
	}
	else {
		$mes .="$eggs[$egg_no][1]を預かり所に送りました!<br>";
		&send_item($m{name}, 2, $egg_no);
	}
}

#=================================================
# 適当なアイコンを表示
#=================================================
sub random_icon {
	my $ricon;
	my @icons = ();
	opendir my $dh, "$icondir" or &error('アイコンフォルダが開けません');
	while(my $file_name = readdir $dh){
		next if $file_name =~ /^\./;
		next if $file_name =~ /\.html$/;
		next if $file_name =~ /\.db$/;
		
		push @icons, $file_name;
	}
	$ricon = @icons[int(rand(@icons))];
	if($ricon eq ''){
		$ricon = $default_icon;
	}
	return $ricon;
}

#=================================================
# モンスターレベルアップ
#=================================================
sub monster_lv_up {
	my $up = shift;

	my @lines = ();
	open my $fh, "+< $this_monster_file" or &error("$this_monster_fileﾌｧｲﾙがありません");
	eval { flock $fh, 2 };
	$line = <$fh>;

	my @datas = split /<>/, $line;
	for my $i (2..9) {
		if ($up) {
			if (rand(30) < 1) {
				$datas[$i]++;
			}
		} else {
			if (rand(10) < 1) {
				$datas[$i]--;
			}
		}
	}
	my $new_line = join '<>', @datas;
	push @lines, "$new_line<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # 削除不可
