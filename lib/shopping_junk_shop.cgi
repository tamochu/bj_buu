my $this_file = "$logdir/junk_shop.cgi";
#================================================
# ｼﾞｬﾝｸｼｮｯﾌﾟ Created by Merino
#=================================================

# 何もないときの売物(武器)
my @wea_nos = (1,6,11,16,21,26);
my @gua_nos = (1..15,18,21);

# ｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞ
my @gacha_eggs = (
	# 値段,		ﾀﾏｺﾞNo
	[5000,	[42,42,43,43,43,43,51,51,51,1,4],		],
	[20000,	[42,42,42,42,42,43,43,1,4..15,33,50],	],
	[50000,	[42,43,1,3..24,33,33,33,50],			],
);

my @gacha_eggs2 = (
	# 値段,		ﾀﾏｺﾞNo,percent
	[150000,	[[42,20],
			[52,20],
			[16,15],
			[3,10],
			[36,4],
			[53,15],
			[55,16],],		],
);

# ｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞができる間隔(秒)
my $gacha_time = 24 * 60 * 60;
my $gacha_time2 = 6 * 60 * 60;

# 買う値段
my $buy_price  = 500;

# 売る値段
my $sall_price = 100;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何する?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ｼﾞｬﾝｸｼｮｯﾌﾟでなんでも買えなんでも売る<br>';
		$mes .= 'お前何する?<br>';
	}
	
	&menu('やめる','買う','売る', 'ｶﾞﾁｬﾀﾏ','高額ｶﾞﾁｬﾀﾏ');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "欲しいのあたか?<br>そこら辺のもの $buy_price Gでいける<br>";
		&menu('やめる','買う');
	}
	elsif ($cmd eq '2') {
		$mes .= "何を売てくれる $sall_price Gで買い取る<br>";
		my @menus = ('やめる');
		push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
		push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
		push @menus, $m{pet} ? "$pets[$m{pet}][1]★$m{pet_c}" : '';
		push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
		&menu(@menus);
	}
	elsif ($cmd eq '3') {
		$mes .= '運だましのｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞ。値段色々。何が出るかはお楽しめ<br>';
		$mes .= 'いだまけ投票権つく<br>';
		my @menus = ('やめる');
		for my $i (0..$#gacha_eggs) {
			push @menus, "$gacha_eggs[$i][0] G";
		}
		&menu(@menus);
	}
	elsif ($cmd eq '4') {
		$mes .= 'ちょっとﾘｯﾁなｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞ。何が出るかはお楽しめ<br>';
		$mes .= 'いだまけ投票権つく<br>';
		my @menus = ('やめる');
		for my $i (0..$#gacha_eggs2) {
			push @menus, "$gacha_eggs2[$i][0] G";
		}
		&menu(@menus);
	}
	else {
		&begin;
	}
}

#=================================================
# 買う
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= 'お前貧乏。売れない。貧乏暇なし働け<br>';
	}
	elsif ($m{is_full}) {
		$mes .= 'お前の預かり所いぱい。売れない<br>';
	}
	else {
		$m{money} -= $buy_price;

		if (-s $this_file) {
			my $count = 0;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
				last if ++$count > 50;
			}
			my $get_line = int(rand(2)) == 0 ? shift @lines : pop @lines;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c) = split /<>/, $get_line;
			
			open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgiﾌｧｲﾙが開けません");
			print $fh3 "$kind<>$item_no<>$item_c<>$m{name}<>$time<>1<>\n";
			close $fh3;
			
			&send_item($m{name}, $kind, $item_no, $item_c);
			&sale_data_log($kind, $item_no, $item_c, 0, $buy_price, 4);
			$mes .= $kind eq '1' ? $weas[$item_no][1]
				  : $kind eq '2' ? $eggs[$item_no][1]
				  : $kind eq '3' ? $pets[$item_no][1]
				  :				   $guas[$item_no][1]
				  ;
			$mes .= 'を買いました<br>';
			
		}
		# 何もない場合はデフォルトアイテム
		else {
			if(rand(2) < 1){
				my $wea_no = $wea_nos[int(rand(@wea_nos))];
				&send_item($m{name}, 1, $wea_no, $weas[$wea_no][4]);
				$mes .= "$weas[$wea_no][1]を買いました<br>";
			}else{
				my $gua_no = $gua_nos[int(rand(@gua_nos))];
				&send_item($m{name}, 4, $gua_no, $guas[$gua_no][4]);
				$mes .= "$guas[$gua_no][1]を買いました<br>";
			}
		}
		$mes .= "お前いい奴、友達。買た物は預かり所に送たよ<br>";
	}
	&begin;
}

#=================================================
# 売る
#=================================================
sub tp_200 {
	if (    ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet})
		 || ($cmd eq '4' && $m{gua}) ) {
		 
			if ($cmd eq '1') {
				if($m{wea_name}){
					$m{wea} = 32;
					$m{wea_c} = 0;
					$m{wea_lv} = 0;
					$mes .= "持ち主の手を離れた途端$m{wea_name}はただの$weas[$m{wea}][1]になってしまった<br>";
					$m{wea_name} = "";
				}
				$mes .= "$weas[$m{wea}][1]を売りました<br>";
				$line = "$cmd<>$m{wea}<>$m{wea_c}<>\n";
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2') {
				$mes .= "$eggs[$m{egg}][1]を売りました<br>";
				$line = "$cmd<>$m{egg}<>$m{egg_c}<>\n";
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3') {
				$mes .= "$pets[$m{pet}][1]★$m{pet_c}を売りました<br>";
				$line = "$cmd<>$m{pet}<>0<>\n";
				$m{pet} = 0;
			}
			elsif ($cmd eq '4') {
				$mes .= "$guas[$m{gua}][1]を売りました<br>";
				$line = "$cmd<>$m{gua}<>0<>\n";
				$m{gua} = 0;
			}
			else {
				&error('ｱｲﾃﾑの種類が異常です');
			}
			
			$mes .= "お前いい人、仲良し。良いもの持てる $sall_money Gやる<br>";
			$m{money} += $sall_price;
			
			open my $fh, ">> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
			print $fh $line;
			close $fh;
			open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgiﾌｧｲﾙが開けません");
			print $fh3 "$kind<>$item_no<>$item_c<>$m{name}<>$time<>0<>\n";
			close $fh3;
	}
	&begin;
}

#=================================================
# ｶﾞﾁｬﾀﾏ
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..$#gacha_eggs+1);
	--$cmd;
	
	if ($m{gacha_time} > $time) {
		my $g_time = $m{gacha_time} - $time;
		my $next_gacha_time = sprintf("%02d時%02d分", int($g_time / 3600), int($g_time % 3600 / 60) );
		$mes .= "ｶﾞﾁｬｶﾞﾁｬやり過ぎるとお前壊れる。あと $next_gacha_time くらい待て<br>";
	}
	elsif ($m{money} >= $gacha_eggs[$cmd][0]) {
		my @egg_nos = @{ $gacha_eggs[$cmd][1] };
		my $egg_no  = $egg_nos[int(rand(@egg_nos))];
		$m{money}  -= $gacha_eggs[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no, 0, 0, 1);
		$mes .= "ｶﾞﾁｬｶﾞﾁｬ♪ﾋﾟｰ♪<br>$eggs[$egg_no][1]が出ました<br>";
		
		$m{gacha_time} = $time + $gacha_time;
		if (&on_summer) {
			my $v = int(rand($gacha_eggs[$cmd][0] / 1000) + 1);
			$m{pop_vote} += $v;
			$mes .= "投票権を$v枚もらったよ";
		}
	}
	else {
		$mes .= 'お前貧乏。ｶﾞﾁｬｶﾞﾁｬﾀﾞﾒ。貧乏暇なし働け<br>';
	}

	&begin;
}

sub tp_400 {
	return if &is_ng_cmd(1..$#gacha_eggs2+1);
	--$cmd;
	
	if ($m{gacha_time2} > $time) {
		my $g_time2 = $m{gacha_time2} - $time;
		my $next_gacha_time2 = sprintf("%02d時%02d分", int($g_time2 / 3600), int($g_time2 % 3600 / 60) );
		$mes .= "ｶﾞﾁｬｶﾞﾁｬやり過ぎるとお前壊れる。あと $next_gacha_time2 くらい待て<br>";
	}
	elsif ($m{money} >= $gacha_eggs2[$cmd][0]) {
		my @egg_list2 = ();
		for(0..$#{$gacha_eggs2[$cmd][1]}){
			for(my $i = 0;$i < $gacha_eggs2[$cmd][1][$_][1];$i++){
			       push(@egg_list2,$gacha_eggs2[$cmd][1][$_][0]);
			}
		}
		my $egg_no2  = $egg_list2[int(rand(@egg_list2))];

		$m{money}  -= $gacha_eggs2[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no2, 0, 0, 1);
		$mes .= "ｶﾞﾁｬｶﾞﾁｬ♪ﾋﾟｰ♪<br>$eggs[$egg_no2][1]が出ました<br>";	
		$m{gacha_time2} = $time + $gacha_time2;
		if (&on_summer) {
			my $v = int(rand(150) + 1);
			$m{pop_vote} += $v;
			$mes .= "投票権を$v枚もらったよ";
		}
	}
	else {
		$mes .= 'お前貧乏。ｶﾞﾁｬｶﾞﾁｬﾀﾞﾒ。貧乏暇なし働け<br>';
	}

	&begin;
}

1; # 削除不可
