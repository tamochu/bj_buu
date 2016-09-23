require "$datadir/hunting.cgi";
#=================================================
# 討伐 Created by Merino
#=================================================

# ｱｲﾃﾑ拾う確率(分の1)
my $get_item_par = 200;

# 超ボスもしくが出てくる確率(分の1)
my $boss_par = $pets[$m{pet}][2] eq 'hunt_lv' ? 5:
				$pets[$m{pet}][2] eq 'no_boss' ? 100:
				20;

# はぐれメタルが出てくる確率(分の1)
my $metal_par = $pets[$m{pet}][2] eq 'no_boss' ? (50-2*$m{pet_c}) :50;

# ボスが逃げる確率(分の1)
my $boss_run_away = 50;

# 普通のNPCモンスターが出る確率(分の1)
my $npc_par = 5;

# 超ボス勝利ボーナス
my @bonus = (
	['weapon', 33, 0, 0],
	['money', 1000000, 0, 0],
	['money', 500000, 0, 0],
	['money', 100000, 0, 0],
	['money', 50000, 0, 0],
	['money', 10000, 0, 0],
	['money', 5000, 0, 0],
);

my @no_boss_eggs = (4..29);

# 新兵訓練所利用可能世代
my $new_sedai = 5;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "討伐するのに$e2j{hp}が少なすぎます<br>";
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
	$mes .= '魔物を討伐しに行きます<br>';
	$mes .= 'どこに向かいますか?<br>';
	
	my $m_st = &m_st;
	my @menus = ('やめる');
	for my $i (0..$#places) {
		next if $i == 0 && $m{sedai} > $new_sedai;
		push @menus, "$places[$i][2]" if $m_st * 2 >= $places[$i][1] || $pets[$m{pet}][2] eq 'hunt_lv';
	}
	
	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		$m{stock} = $cmd-1;
		$m{stock}++ if $m{sedai} > $new_sedai;
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
	my $data_num = $places[$m{stock}][0];
	unless ($pets[$m{pet}][2] ne 'hunt_lv' && $data_num eq 'boss') {
		open my $fh, "< $logdir/monster/$data_num.cgi" or &error("$logdir/monster/$data_num.cgiﾌｧｲﾙがありません");
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			while ($line = <$fh>) {
				last if index($line, 'デポジット') > -1;
			}
		}
		else {
=cut
			rand($.) < 1 and $line = $_ while <$fh>;
#		}

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
	}
	if ($data_num eq 'boss') {
		open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
		$line = <$bfh>;
		close $bfh;
		my @datas = split /<>/, $line;
		my $i = 0;
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $datas[$i];
			++$i;
		}
		$y{hp} = $y{max_hp};
		$y{mp} = $y{max_mp};
#			$y{icon} = &random_icon;
		$y{gua} = 0;
		if( rand($m{cha}) < rand(2000) ){
			$m{tp} = 400;
			$mes .= "超ボス $y{name} が襲いかかってきました<br>";
			&n_menu;
		}else{
			$m{tp} = 300;
			$mes .= "超ボス $y{name} がいます<br>";
			&menu('戦う','逃げる');
		}
	} elsif(!$m{no_boss} && $m{stock} > 5 && rand($metal_par) < 1 && -f "$datadir/metal.cgi"){
		require "$datadir/metal.cgi";
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $metal[$m{stock}]{$k};
		}
		$y{hp} = $y{max_hp};
		$y{mp} = $y{max_mp};
#			$y{icon} = &random_icon;
		$y{gua} = 0;
		$m{tp} = 500;
		$mes .= "ボーナスモンスター $y{name} に遭遇した！<br>";
		&n_menu;
	} elsif(!$m{no_boss} && $m{stock} > 5 && rand($boss_par) < 1 && -f "$logdir/monster/boss.cgi"){
		open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
		$line = <$bfh>;
		close $bfh;
		my @datas = split /<>/, $line;
		my $i = 0;
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $datas[$i];
			++$i;
		}
		$y{hp} = $y{max_hp};
		$y{mp} = $y{max_mp};
#			$y{icon} = &random_icon;
		$y{gua} = 0;
		if( rand($m{cha}) < rand(2000) ){
			$m{tp} = 400;
			$mes .= "超ボス $y{name} が襲いかかってきました<br>";
			&n_menu;
		}else{
			$m{tp} = 300;
			$mes .= "超ボス $y{name} がいます<br>";
			&menu('戦う','逃げる');
		}
	} elsif(rand($npc_par) < 1) {
		require "$datadir/npc_hunting.cgi";
		my $stock_npcs_ref = $npc[$m{stock}];
		my @stock_npcs = @$stock_npcs_ref;
		my $enemy = int(rand($stock_npcs));
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $stock_npcs[$enemy]{$k};
		}
		$y{hp} = $y{max_hp};
		$y{mp} = $y{max_mp};
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
	} else{
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
		if($m{stock} == 0){
			$m{act} += 8;
		}else {
			my $lossp = $m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
	   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
	   		$m{money} -= $vloss;
			$mes .= "$vloss Gを失いました<br>";
			$m{act} += 12;
		}
		&refresh;
		&n_menu;
		
	}
	# 勝ち
	elsif ($y{hp} <= 0) {
		# ﾄｰﾀﾙｽﾃｰﾀｽが自分より弱者だと経験値少なめ
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$vv *= 1.5 if $m{master_c} eq 'tou_c';
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}elsif($m{no_boss}){
			$m{egg_c} += int(rand($m{stock}-1)) if $m{egg};
		}else{
			$m{egg_c} += int(rand($m{stock}-1)+$m{stock}) if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v の$e2j{exp}と $vv Gを手に入れました<br>";
		
		# ｱｲﾃﾑｹﾞｯﾄ(特殊ﾍﾟｯﾄ職業だと取得率up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '遊び人' || $m{master_c} eq 'tou_c';
		$get_item_par = 400 if $m{stock} == 0;
		$get_item_par = 1000 if $m{no_boss};
		&_get_item if int(rand($get_item_par)) == 0;
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('hunting');
		}
		
		$mes .= '討伐を続けますか?<br>';
		&menu('続ける','やめる','討伐地変更');
		$m{tp} += 10;
	}
}

#=================================================
# 継続 or やめる
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}elsif ($cmd eq '2') {
		&begin;
	}else {
		$mes .= '討伐を終了します<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# 戦う or 逃げる(超ボス)
#=================================================
sub tp_300 {
	if ($cmd eq '0') {
		$mes .= "$y{name} と戦います<br>";
		$m{tp} = 400;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand(2000) ) {
		$mes .= '逃げました<br>';
		&begin;
	}
	else {
		$mes .= '逃げられませんでした。戦闘態勢に入ります<br>';
		$m{tp} = 400;
		&n_menu;
	}
}
#=================================================
# 超ボス戦闘
#=================================================
sub tp_400 {
	require './lib/boss_battle.cgi';

	# 負け
	if ($m{hp} <= 0) {
		open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
		my $head_line = <$bfh>;
		my $is_added = 1;
		my @lines = ();
		push @lines, "$y{name}<>$y{country}<>$y{hp}<>$y{max_mp}<>$y{at}<>$y{df}<>$y{mat}<>$y{mdf}<>$y{ag}<>$y{cha}<>$y{wea}<>$y{skills}<>$y{mes_win}<>$y{mes_lose}<>$y{icon}<>$y{wea_name}<>\n";
		if($y{max_hp} > $y{hp}){
			while(my $line = <$bfh>){
				my($bname, $bdamage) = split /<>/, $line;
				if($bname eq $m{name}){
					$bdamage += $y{max_hp} - $y{hp};
					$is_added = 0;
				}
				push @lines, "$bname<>$bdamage<>\n";
			}
			if($is_added){
				my $bdamage = $y{max_hp} - $y{hp};
				push @lines, "$m{name}<>$bdamage<>\n";
			}
		}
		seek  $bfh, 0, 0;
		truncate $bfh, 0;
		print $bfh @lines;
		close $bfh;

		if($m{stock} == 0){
			$m{act} += 8;
		}else {
			my $lossp = $m{stock} >= 9 ? 0.5:
					$m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
			if ($y{at} > 999999 && $m{stock} < 9) {
				$mes .= "次のボスが現れるのを待ってね。<br>";
			} else {
		   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
		   		$m{money} -= $vloss;
				$mes .= "$vloss Gを失いました<br>";
				$m{act} += $m{stock} >= 9 ? 100 : 12;
			}
		}
		&refresh;
		&n_menu;
	}
	# 勝ち
	elsif ($y{hp} <= 0) {
		&win_boss_bonus;
		
		# ﾄｰﾀﾙｽﾃｰﾀｽが自分より弱者だと経験値少なめ
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}else{
			$m{egg_c} += int(rand($m{stock}-1)+$m{stock}) if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v の$e2j{exp}と $vv Gを手に入れました<br>";
		
		# ｱｲﾃﾑｹﾞｯﾄ(特殊ﾍﾟｯﾄ職業だと取得率up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '遊び人';
		$get_item_par = 400 if $m{stock} == 0;
		&_get_item if int(rand($get_item_par)) == 0;
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('boss');
		}
		
		$mes .= '討伐を続けますか?<br>';
		&menu('続ける','やめる','討伐地変更');
		$m{tp} = 210;
	} elsif (rand($boss_run_away) < 1) {
		open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
		my $head_line = <$bfh>;
		my $is_added = 1;
		my @lines = ();
		push @lines, "$y{name}<>$y{country}<>$y{hp}<>$y{max_mp}<>$y{at}<>$y{df}<>$y{mat}<>$y{mdf}<>$y{ag}<>$y{cha}<>$y{wea}<>$y{skills}<>$y{mes_win}<>$y{mes_lose}<>$y{icon}<>$y{wea_name}<>\n";
		if($y{max_hp} > $y{hp}){
			while(my $line = <$bfh>){
				my($bname, $bdamage) = split /<>/, $line;
				if($bname eq $m{name}){
					$bdamage += $y{max_hp} - $y{hp};
					$is_added = 0;
				}
				push @lines, "$bname<>$bdamage<>\n";
			}
			if($is_added){
				my $bdamage = $y{max_hp} - $y{hp};
				push @lines, "$m{name}<>$bdamage<>\n";
			}
		}
		seek  $bfh, 0, 0;
		truncate $bfh, 0;
		print $bfh @lines;
		close $bfh;

		$m{act} += 8;
		$mes .= "$y{name}「疲れたから帰る。運がよかったな！」<br>";
		&refresh;
		&n_menu;
	}
}

#=================================================
# ボーナス戦闘
#=================================================
sub tp_500 {
	require './lib/bonus_battle.cgi';

	# 負け
	if ($m{hp} <= 0) {
		if($m{stock} == 0){
			$m{act} += 8;
		}else {
			my $lossp =$m{stock} >= 9 ? 0.5:
					$m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
	   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
	   		$m{money} -= $vloss;
			$mes .= "$vloss Gを失いました<br>";
			$m{act} += $m{stock} >= 9 ? 100 : 12;
		}
		&refresh;
		&n_menu;
	}
	# 勝ち
	elsif ($y{hp} <= 0) {
		# ﾄｰﾀﾙｽﾃｰﾀｽが自分より弱者だと経験値少なめ
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = 30 * $m{stock};
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}else{
			$m{egg_c} += int(rand(25)) + int($m{stock} - 4) * 25 if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v の$e2j{exp}と $vv Gを手に入れました<br>";
		
		# ｱｲﾃﾑｹﾞｯﾄ(特殊ﾍﾟｯﾄ職業だと取得率up)
		$get_item_par = 80;
		&_get_item if int(rand($get_item_par)) == 0;
		
		$mes .= '討伐を続けますか?<br>';
		&menu('続ける','やめる','討伐地変更');
		$m{tp} = 210;
	}
}

#=================================================
# ｱｲﾃﾑ(ﾀﾏｺﾞ)拾う処理
#=================================================
sub _get_item {
	my @egg_nos = @{ $places[$m{stock}][3] };
	@egg_nos = @no_boss_eggs if $m{no_boss};
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
# 超ボスに勝利
#=================================================
sub win_boss_bonus {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '名無し';
	}
	my $message = "<b>$m{name}とその仲間たちがボスを撃破しました</b>";
	$mes .= "$message<br>";
	&write_world_news("<b>$c_mの$w_nameとその仲間たちがボスを撃破しました</b>", 1);
	&send_twitter("$c_mの$w_nameとその仲間たちがボスを撃破しました");
#	&mes_and_world_news("", 1);

	open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgiﾌｧｲﾙがありません");
	my $head_line = <$bfh>;
	my @lines = ();
	my @attackers = ();
	push @lines, "負けイベント<>0<>999999999999<>999999999999<>99999999<>99999999<>99999999<>99999999<>99999999<>99999999<>32<>67,67,67,67,67<>強制負けイベントだから次の超ボスイベントを待ってね<>なぜ勝てたし<>$default_icon<>パンチ（魔法）<>\n";
	my $is_find = 0;
	while(my $line = <$bfh>){
		my($bname, $bdamage) = split /<>/, $line;
		if($bname eq $m{name}){
			$bdamage += $y{max_hp};
			$is_find = 1;
			push @attackers, "$m{name}<>$bdamage<>\n";
		}else{
			push @attackers, $line;
		}
	}
	seek  $bfh, 0, 0;
	truncate $bfh, 0;
	print $bfh @lines;
	close $bfh;
	
	unless($is_find){
		push @attackers, "$m{name}<>$y{max_hp}<>\n";
	}
	
	@attackers = reverse(map { $_->[0] }
				sort { $a->[2] <=> $b->[2] }
					map { [$_, split /<>/ ] } @attackers);
	my $rank = 0;
	my $debug_mes = '';
	for my $line (@attackers){
		my($bname, $bdamage) = split /<>/, $line;
		if($rank >= @bonus){
			&send_money($bname, "超ボス撃破貢献", 1000);
		}else{
			if($bonus[$rank][0] eq 'money'){
				&send_money($bname, "超ボス撃破貢献", $bonus[$rank][1]);
			}elsif($bonus[$rank][0] eq 'weapon'){
				&send_item($bname, 1, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}elsif($bonus[$rank][0] eq 'egg'){
				&send_item($bname, 2, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}elsif($bonus[$rank][0] eq 'pet'){
				&send_item($bname, 3, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}
		}
		$rank++;
	}
}
1; # 削除不可
