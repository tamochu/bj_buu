my $this_file = "$logdir/offertory_box.cgi";
#================================================
# 賽銭箱
#=================================================

# お賽銭を入れられる間隔（秒）
my $offertory_time = 24 * 60 * 60;

@buu_item = (
	#種類,  番号, 耐久値など, ★, 数量
	[2,54,0,0,1],# ﾀｷｵﾝ
	[1,33,500,0,1],# ﾐｻｲﾙ
	[3,125,0,0,1],# ﾑｰ
	[3,21,0,0,1],# ｶﾞﾌﾞﾘｴﾙ
	[3,183,0,0,1],# ﾀｸﾐ
	[3,184,0,0,20],# ﾚﾝｼﾞ10
	[3,187,0,0,5],# ﾊﾟﾙﾌﾟﾝﾃ5
);

@god_item = (
	#種類,  番号, 耐久値など, ★, 数量
	[2,3,999,0,10],# 孵化夢10
	[1,32,500,30,1],# ｸﾛﾑ★30
	[3,64,0,0,5],# ｾﾞｳｽ5
	[3,125,0,0,1],# ﾑｰ
	[3,127,0,0,1],# ｱｵｲﾄﾘ
	[3,17,0,0,1],# ﾗﾌｧｴﾙちゃん
	[3,18,0,0,1],# ﾐｶｴﾙ
	[3,21,0,0,1],# ｶﾞﾌﾞﾘｴﾙ
	[2,37,999,0,5],# 孵化神卵5
	[3,75,0,0,5],# ｳｪﾎﾟﾝLv4 5
	[3,143,0,0,5],# ﾂｸﾖﾐ5
	[3,144,0,0,5],# ｱﾎﾟﾛﾝ5
	[3,132,0,0,10],# ﾘﾎﾞﾝ10
	[3,164,0,0,10],# ｴﾛｽ10
	[2,53,0,0,10],# ｱﾀﾘｴｯｸﾞ10
	[3,168,0,0,1],# ﾍﾟｲﾝﾀｰ
	[3,183,0,0,1],# ﾀｸﾐ
	[3,184,0,0,10],# ﾚﾝｼﾞ10
	[3,187,0,0,3],# ﾊﾟﾙﾌﾟﾝﾃ3
	[3,189,0,0,10],# ﾒｶﾞﾎﾝ10
	[3,190,0,0,10],# ｱﾘﾖｼ10
);
#はずれ
@bad_item = (
	[2,22,0,0,10],# ｱﾝﾃﾞｯﾄ爆撃
	[2,42,0,0,10],# ﾊｽﾞﾚ爆撃
	[3,120,0,0,10],# ﾏｼﾞｽｶ爆撃
	[3,121,0,0,10],# ﾎﾟｲｿﾞﾝ爆撃
	[3,176,0,0,10],# ﾜﾛｽ爆撃
	[3,198,0,0,10],# ｶｼﾗ爆撃
);

#堪忍袋
my $flow_anger = 10;

#これ以下の乱数（毎回計算）以上に累計額が超えるとアイテムをもらえる
#乱数なので大きめに設定すること
my $flow_total = 50000000;

# 供えると神様が怒る糞アイテム
my %anger_items = (
	wea => [1,6,11,16,21,26,], # 武器
	egg => [22,24,42,], # ﾀﾏｺﾞ
	pet => [120,121,], # ﾍﾟｯﾄ
	gua => [], # 防具
);

# レアアイテム（適当なので適宜追加してください）
my %satisfy_items = (
	wea => [5,10,15,20,25,30,31,32,], # 武器
	egg => [37,38,39,40,41,45,46,47,], # ﾀﾏｺﾞ
	pet => [3,7,8,17,18,19,20,21,48,58,59,60,63,127,150,151,183], # ﾍﾟｯﾄ
	gua => [], # 防具
);

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何する?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '神様出てくるさーせん箱<br>';
		$mes .= '金入れる<br>';
	}
	
	&menu('やめる','お賽銭を入れる','お供え物をする');
}

sub tp_1 {
	return if &is_ng_cmd(1..2);
	
	if ($cmd eq '1') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1">金額<input type="text" name="send_money" value="0" class="text_box1" style="text-align:right">G<br>| if $m{money} > 0;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="入れる" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	elsif ($cmd eq '2') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1">[$weas[$m{wea}][2]]$weas[$m{wea}][1]★$m{wea_lv}($m{wea_c}/$weas[$m{wea}][4])<br>| if $m{wea};
		$mes .= qq|<input type="radio" name="cmd" value="2">[卵]$eggs[$m{egg}][1]($m{egg_c}/$eggs[$m{egg}][2])<br>| if $m{egg};
		$mes .= qq|<input type="radio" name="cmd" value="3">[ペ]$pets[$m{pet}][1]★$m{pet_c}<br>| if $m{pet};
		$mes .= qq|<input type="radio" name="cmd" value="4">[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>| if $m{gua};
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="お供えする" class="button1"></p></form>|;
		$m{tp} = 200;
	}
	else {
		&begin;
	}
}

#=================================================
# 賽銭を入れる
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]はまずきれいな身になれ<br>";
		&begin;
		return;
	}

	if ($m{offertory_time} > $time) {
		my $o_time = $m{offertory_time} - $time;
		my $next_offertory_time = sprintf("%02d時%02d分", int($o_time / 3600), int($o_time % 3600 / 60) );
		$mes .= "お参り一日一回でいい。あと $next_offertory_time 待て<br>";
		&begin;
		return;
	}
	if ($cmd eq '1' && $in{send_money} > 0 && $in{send_money} !~ /[^0-9]/) {
		if ($m{money} >= $in{send_money}) {
			$m{offertory_time} = $time + $offertory_time;
			my $all_money = $m{money};
			$m{money} -= $in{send_money};
			if ($m{bank} ne '') {
				my $shop_id = unpack 'H*', $m{bank};
				my $save_money = 0;

				if( -f "$userdir/$shop_id/shop_bank.cgi"){
					open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
					my $head_line = <$fh>;
					while (my $line = <$fh>) {
						my($year, $name, $money) = split /<>/, $line;
						if ($m{name} eq $name) {
							$save_money = $money;
							last;
						}
					}
					close $fh;
					$all_money += $save_money;
				}
			}
			my $total;
			my $anger;

			my @lines = ();
			if(-s $this_file){
				open my $ofh, "< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
				while (my $line = <$ofh>) {
					push @lines, $line;
				}
				close $ofh;
				my $get_line = shift @lines;
				($total, $anger) = split /<>/, $get_line;
			}else {
				$total = 0;
				$anger = 0;
			}
			$total += $in{send_money};

			if($in{send_money} == $all_money){
				$total += 1000000;
			}
			if($total > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				if (rand(10) < 1) {
					&get_god_item(7);

					$mes .= "黒豚神<ぶー<br>";
					&mes_and_world_news("黒豚神様からアイテムをもらいました", 1);
					&send_twitter("黒豚神様からアイテムをもらいました", 1);
				} else {
					&get_god_item(5);

					$mes .= "ぼくはここの神様だよ<br>";
					$mes .= "いっつもお参りありがとう。<br>";
					$mes .= "お礼にアイテムあげるね<br>";
					&mes_and_world_news("神様からアイテムをもらいました", 1);
					&send_twitter("神様からアイテムをもらいました", 1);
				}
			}
			unshift @lines, "$total<>$anger";

			open my $wfh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
			print $wfh @lines;
			close $wfh;
			
			&log_errors("$in{send_money} / $all_money offertory by $m{name}");
		}
		else {
			$mes .= "お金が足りません<br>";
		}
	}
	&begin;	
}

#=================================================
# お供え物をする
#=================================================
sub tp_200 {
	return if &is_ng_cmd(1..4);
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]はまずきれいな身になれ<br>";
		&begin;
		return;
	}

	if ($m{offertory_time} > $time) {
		my $o_time = $m{offertory_time} - $time;
		my $next_offertory_time = sprintf("%02d時%02d分", int($o_time / 3600), int($o_time % 3600 / 60) );
		$mes .= "お参り一日一回でいい。あと $next_offertory_time 待て<br>";
		&begin;
		return;
	}
	if (($cmd eq '1' && $m{wea}) || ($cmd eq '2' && $m{egg}) || ($cmd eq '3' && $m{pet}) || ($cmd eq '4' && $m{gua})) {
		$m{offertory_time} = $time + $offertory_time;
		my $total;
		my $add_total = 20000;
		my $anger;
		my $is_anger = 0;
		my $is_satisfy = 0;
		my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
		for my $anger_item (@{ $anger_items{ $kinds[$cmd] } }) {
			if ($anger_item eq $m{ $kinds[$cmd] }) {
				$is_anger = 1;
				$add_total = 10000;
			}
		}
		for my $satisfy_item (@{ $satisfy_items{ $kinds[$cmd] } }) {
			if ($satisfy_item eq $m{ $kinds[$cmd] }) {
				$is_satisfy = 1;
				$add_total = 100000;
			}
		}
		my @lines = ();
		if(-s $this_file){
			open my $ofh, "< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
			while (my $line = <$ofh>) {
				push @lines, $line;
			}
			close $ofh;
			my $get_line = shift @lines;
			($total, $anger) = split /<>/, $get_line;
		}else {
			$total = 0;
			$anger = 0;
		}
		$total += $add_total;

		if($is_anger){
			$anger++;
			if($anger > $flow_anger){
				$anger = 0;
				if (rand(300) < 1) {
					&get_god_item(7);

					$mes .= "黒豚神<ぶー<br>";
					&mes_and_world_news("黒豚神様からアイテムをもらいました", 1);
					&send_twitter("黒豚神様からアイテムをもらいました", 1);
				} else {
					&get_god_item(0);

					$mes .= "ぼくはここの神様だよ！<br>";
					$mes .= "いっつもお参りありがとう！<br>";
					$mes .= "お礼にアイテムあげるね！<br>";
					&mes_and_world_news("神様からアイテムをもらいました？", 1);
					&send_twitter("神様からアイテムをもらいました？", 1);
				}
			}
		}elsif($is_satisfy){
			if($total * 2 > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				
				if (rand(2) < 1) {
					&get_god_item(7);

					$mes .= "黒豚神<ぶー<br>";
					&mes_and_world_news("黒豚神様からアイテムをもらいました", 1);
					&send_twitter("黒豚神様からアイテムをもらいました", 1);
				} else {
					&get_god_item(6);

					$mes .= "ぼくはここの神様だよ<br>";
					$mes .= "いっつもお参りありがとう。<br>";
					$mes .= "お礼にアイテムあげるね<br>";
					&mes_and_world_news("神様からアイテムをもらいました", 1);
					&send_twitter("神様からアイテムをもらいました", 1);
				}
			}
		}else{
			if($total > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				
				if (rand(20) < 1) {
					&get_god_item(7);

					$mes .= "黒豚神<ぶー<br>";
					&mes_and_world_news("黒豚神様からアイテムをもらいました", 1);
					&send_twitter("黒豚神様からアイテムをもらいました", 1);
				} else {
					&get_god_item(4);

					$mes .= "ぼくはここの神様だよ<br>";
					$mes .= "いっつもお参りありがとう。<br>";
					$mes .= "お礼にアイテムあげるね<br>";
					&mes_and_world_news("神様からアイテムをもらいました", 1);
					&send_twitter("神様からアイテムをもらいました", 1);
				}
			}
		}
		unshift @lines, "$total<>$anger";

		open my $wfh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
		print $wfh @lines;
		close $wfh;
	}	
	if ($cmd eq '1' && $m{wea}) {
		&sale_data_log(1, $m{wea}, $m{wea_c}, $m{wea_lv}, 500, 5);
		if($m{wea_name}){
			$mes .= "$m{wea_name}を神に返しました";
			$m{wea_name} = "";
			&get_god_item(4);
		}
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
	}
	elsif ($cmd eq '2' && $m{egg}) {
		&sale_data_log(2, $m{egg}, $m{egg_c}, 0, 500, 5);
		$m{egg} = $m{egg_c} = 0;
	}
	elsif ($cmd eq '3' && $m{pet}) {
		&sale_data_log(3, $m{pet}, $m{pet_c}, 0, 500, 5);
		$m{pet} = 0;
	}
	elsif ($cmd eq '4' && $m{gua}) {
		&sale_data_log(4, $m{gua}, 0, 0, 500, 5);
		$m{gua} = 0;
	}
	&begin;	
}

sub get_god_item {
	my $type = shift;
	if ($type >= 7 && rand(3) < 1) {
		my $item_no = int(rand($#buu_item + 1));
		&send_item($m{name},$buu_item[$item_no][0],$buu_item[$item_no][1],$buu_item[$item_no][2],$buu_item[$item_no][3],1) for 1 .. $buu_item[$item_no][4];
	} elsif (rand(7) < $type) {
		my $item_no = int(rand($#god_item + 1));
		&send_item($m{name},$god_item[$item_no][0],$god_item[$item_no][1],$god_item[$item_no][2],$god_item[$item_no][3],1) for 1 .. $god_item[$item_no][4];
	} else {
		my $item_no = int(rand($#bad_item + 1));
		&send_item($m{name},$bad_item[$item_no][0],$bad_item[$item_no][1],$bad_item[$item_no][2],$bad_item[$item_no][3],1) for 1 .. $bad_item[$item_no][4];		
	}

}

sub send_god_item {
	my ($type, $send_name) = @_;
	if ($type >= 7 && rand(3) < 1) {
		my $item_no = int(rand($#buu_item + 1));
		&send_item($send_name,$buu_item[$item_no][0],$buu_item[$item_no][1],$buu_item[$item_no][2],$buu_item[$item_no][3],1) for 1 .. $buu_item[$item_no][4];
	} elsif (rand(7) < $type) {
		my $item_no = int(rand($#god_item + 1));
		&send_item($send_name,$god_item[$item_no][0],$god_item[$item_no][1],$god_item[$item_no][2],$god_item[$item_no][3],1) for 1 .. $god_item[$item_no][4];
	}else {
		my $item_no = int(rand($#bad_item + 1));
		&send_item($send_name,$bad_item[$item_no][0],$bad_item[$item_no][1],$bad_item[$item_no][2],$bad_item[$item_no][3],1) for 1 .. $bad_item[$item_no][4];		
	}

}


1; # 削除不可
