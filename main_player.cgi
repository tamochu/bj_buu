#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 廃人ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

my $max_ranking = 100;

my %calc_name = (
	rank => "階級",
	lea => "統率",
	nou_c => "農業",
	sho_c => "商業",
	hei_c => "徴兵",
	mil5_sum => "軍事5種合計",
	mil3_sum => "軍事3種合計",
	str => "強さ",
	win_c => "戦争勝利数",
	win_par => "勝率",
	gai_c => "外交",
	gou_c => "強奪",
	cho_c => "諜報",
	sen_c => "洗脳",
	gik_c => "偽計",
	tei_c => "偵察",
	mat_c => "待伏",
	year_strong => "一年奪国力",
	year_nou => "一年農業",
	year_sho => "一年商業",
	year_hei => "一年徴兵",
	year_gou => "一年強奪",
	year_cho => "一年諜報",
	year_sen => "一年洗脳",
	year_gou_t => "一年強奪(累計)",
	year_cho_t => "一年諜報(累計)",
	year_sen_t => "一年洗脳(累計)",
	year_gik => "一年偽計",
	year_res => "一年救出",
	year_esc => "一年脱獄",
	year_tei => "一年偵察",
	year_stop => "一年停戦",
	year_pro => "一年友好",
	year_dai => "一年国畜"
);

#=================================================
&decode;
&header;
&read_cs;

my $this_file = "$logdir/main_player.cgi";
my $this_script = 'main_player.cgi';

my $default_calc = "rank:8:1::lea:300:1:::nou_c:500:1::sho_c:500:1:::nou_c:500:1::sho_c:500:1::hei_c:500:1:::mil5_sum:2500:1:::mil5_sum:5000:1:::gai_c:350:1:::win_c:200:1::win_par:75:1:::win_c:400:1::win_par:80:1";
#my $default_calc = "rank:15:1::lea:900:1:::nou_c:1000:1::sho_c:1000:1:::nou_c:1000:1::sho_c:1000:1::hei_c:1000:1:::mil5_sum:7000:1:::mil5_sum:10000:1:::gai_c:1400:1:::win_c:800:1::win_par:75:1:::win_c:1000:1::win_par:80:1";

&update_main_player if $in{reload} == 1;
&run;
&footer;
exit;

#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	print qq|<h1>主力表\</h1>|;
	print qq|<div class="mes">ﾗﾝｷﾝｸﾞは出力される度にﾘｾｯﾄされ更新されます</div><br>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="reset" value="1"><input type="submit" value="条件リセット" class="button1"></form>|;

	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	$head_line = <$fh>;
	my($output_time, $calc_min, $calc) = split /<>/, $head_line;
	print qq|<form method="$method" action="$this_script">|;
	print qq|<table class="table1"><tr><th>条件</th><th>加算値</th></tr>|;
	&input_form($calc);
	$calc_min = $in{reset} ? 1 : $calc_min;
	print qq|閾値<input type="text" name="min" value="$calc_min" class="text_box_s"><br>|; # value="4"
	print qq|<input type="hidden" name="reload" value="1"><input type="submit" value="出力" class="button1">|;
	print qq|</form>|;

	my($min,$hour,$mday,$mon,$year) = (localtime($output_time))[1..4];
	my $output_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
	print qq|<h2>出力日:$output_date 閾値:$calc_min</h2>|;
	
	my $rank = 1;
	my $pre_number = 0;
	my $d_rank;

	print qq|<h3>全国の主力</h3>|;
	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th><th>評価</th></tr>| unless $is_mobile;
	my @lines = ();
	while ($line = <$fh>) {
		push @lines, $line;
		my($number,$name,$country,$type) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
		print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
	
	for my $country_i(0..$w{country}) {
		$rank = 1;
		print qq|<h3>$cs{name}[$country_i]の主力</h3>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th><th>評価</th></tr>| unless $is_mobile;
		
		for my $line (@lines) {
			my($number,$name,$country,$type) = split /<>/, $line;
			next if $country != $country_i;
			my $player_id =  unpack 'H*', $name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				;
			++$rank;
		}
		close $fh;
		
		print qq|</table>| unless $is_mobile;
	}
}

sub input_form {
	my @calc = split(/;/, shift);
	@calc = (10, 300, 500, 500, 500, 2500, 5000, 350, 200, 75, 400, 80) if $in{reset};

	# 階級 x 以上かつ統率 y 以上
	print qq|<tr><td>階級<select name="rank" class="select1">|;
	for my $i (0 .. $#ranks) {
		my $j = $#ranks-$i;
		my $selected = $j eq @calc[0] ? " selected=\"selected\"" : "";
		print qq|<option value="$j" label="$ranks[$j]"$selected>$ranks[$j]</option>|;
	}
	print qq|</select>以上＆統率<input type="text" name="lea" value="$calc[1]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 農業 x 以上かつ商業 y 以上
	print qq|<tr><td>農業<input type="text" name="nou_c" value="$calc[2]" class="text_box_s">以上＆商業<input type="text" name="sho_c" value="$calc[3]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 農業 x 以上かつ商業 y 以上かつ徴兵 z 以上
	print qq|<tr><td>↑条件を満たした上で徴兵<input type="text" name="hei_c" value="$calc[4]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 軍事5種合計 n 以上
	print qq|<tr><td>軍事5種合計<input type="text" name="mil5_1" value="$calc[5]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 軍事5種合計 n+a 以上
	print qq|<tr><td>軍事5種合計<input type="text" name="mil5_2" value="$calc[6]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 外交 n 以上
	print qq|<tr><td>外交<input type="text" name="gai_c" value="$calc[7]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 戦争勝利数 x 以上かつ勝率 y 以上
	print qq|<tr><td>戦勝数<input type="text" name="win_c_1" value="$calc[8]" class="text_box_s">以上＆勝率<input type="text" name="win_par_1" value="$calc[9]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 戦争勝利数 x+a 以上かつ勝率 y+b 以上
	print qq|<tr><td>戦勝数<input type="text" name="win_c_2" value="$calc[10]" class="text_box_s">以上＆勝率<input type="text" name="win_par_2" value="$calc[11]" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	print qq|</table>|;

# 途中で飽きた柔軟性を捨てた弊害
=pod
	# 世代 x 以上
	print qq|<tr><td>世代<input type="text" name="sedai" value="5" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 階級 x 以上
	print qq|<tr><td>階級<select name="rank" class="select1">|;
	for my $i (0 .. $#ranks) {
		my $j = $#ranks-$i;
		my $selected = $i eq 6 ? " selected=\"selected\"" : "";
		print qq|<option value="$j" label="$ranks[$j]"$selected>$ranks[$j]</option>|;
	}
	print qq|</select>以上</td>|;
	print qq|<td>+1～2</td></tr>|;

	# 内政3種合計 n 以上
	print qq|<tr><td>内政3種合計<input type="text" name="dom3_2" value="1500" class="text_box_s">以上</td>|;
	print qq|<td>+2</td></tr>|;

	# 内政3種合計 n 以上
	print qq|<tr><td>内政3種合計<input type="text" name="dom3_1" value="600" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 軍事3種合計 n 以上
	print qq|<tr><td>軍事3種合計<input type="text" name="mil3_2" value="1500" class="text_box_s">以上</td>|;
	print qq|<td>+2</td></tr>|;

	# 軍事3種合計 n 以上
	print qq|<tr><td>軍事3種合計<input type="text" name="mil3_1" value="600" class="text_box_s">以上</td>|;
	print qq|<td>+1</td></tr>|;

	# 戦争勝利数 x 以上
	print qq|<tr><td>戦勝数<input type="text" name="win_c_2" value="100" class="text_box_s">以上</td>|;
	print qq|<td>+2</td></tr>|;

	# 戦争勝利数 x 以上
	print qq|<tr><td>戦勝数<input type="text" name="win_c_1" value="50" class="text_box_s">以上</td>|;
	print qq|<td>+2</td></tr>|;
=cut
}

#=================================================
# 主力表を更新
#=================================================
sub update_main_player  {
	my %sames = ();
	my @p_ranks = ();
	my @ranks_num = (0, 0, 0, 0, 0, 0, 0, 0);

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/user.cgi") {
				next;
			}
			my %p = &get_you_datas($player_id, 1);
			$p{dom3} = $p{nou_c} + $p{sho_c} + $p{hei_c};
			$p{mil5} = $p{gou_c} + $p{cho_c} + $p{sen_c} + $p{gik_c} + $p{tei_c};
			$p{win_par} = $p{win_c} > 0 ? int( $p{win_c} / ($p{win_c} + $p{lose_c} + $p{draw_c}) * 100 ) : 0;
			$p{pt} = 0;

			# 階級 x 以上かつ統率 y 以上
			if ($p{rank} >= $in{rank} && $p{lea} >= $in{lea}) {
				$p{pt} += 1;
			}

			# 農業 x 以上かつ商業 y 以上
			if ($p{nou_c} >= $in{nou_c} && $p{sho_c} >= $in{sho_c}) {
				$p{pt} += $p{hei_c} >= $in{hei_c} ? 2 : 1; # かつ徴兵 z 以上
			}

			# 軍事5種合計 n 以上
			if ($p{mil5} >= $in{mil5_1}) {
				$p{pt} += $p{mil5} >= $in{mil5_2} ? 2 : 1; # かつ +a 以上
			}

			# 外交 n 以上
			if ($p{gai_c} >= $in{gai_c}) {
				$p{pt} += 1;
			}

			# 戦争勝利数 x 以上かつ勝率 y 以上
			if ($p{win_c} >= $in{win_c_1} && $p{win_par} >= $in{win_par_1}) {
				$p{pt} += $p{win_c} >= $in{win_c_2} && $p{win_par} >= $in{win_par_2} ? 2 : 1; # かつ戦争勝利数 x+a 以上かつ勝率 y+b 以上
			}

			next if $p{pt} < $in{min};

			# 特徴決定 たしか 内政*1 軍事*0.3 戦争*3 で計算してた気がする
			$p{mil5} *= 0.5;
			$p{win_c} *= 3;
			$p{lose_c} *= 3;
			$p{draw_c} *= 3;

			if ($p{dom3} > ($p{mil5} * 2) && $p{dom3} > ($p{win_c} * 2)) { # 内政が軍事戦争の倍なら特化と判定
				$p{$type} = "内政廃人";
				if ( ($p{dom3}/3) > $p{hei_c} ) {
					$p{$type} .= "（守銭奴）";
				}
			}
			elsif ($p{mil5} > ($p{dom3} * 2) && $p{mil5} > ($p{win_c} *2)) { # 軍事が内政戦争の倍なら特化と判定
				$p{$type} = "軍事廃人";
				if ( ($p{mil5}/5) < $p{gik_c} ) {
					$p{$type} .= "（ナナコ）";
				}
				elsif ( ($p{mil5}/5) < $p{gik_c} ) {
					$p{$type} .= "（アクロマ）";
				}
			}
			elsif ($p{win_c} > ($p{dom3} * 2) && $p{win_c} > ($p{mil5} *2)) { # 戦争が内政軍事の倍なら特化と判定
				$p{$type} = "戦争廃人";
			}

			# 内政しないで戦争ばっかアーサー

			# 挿入ソート？ 通称は分からんがフォルダとファイルをソートするのによく見た手法だったような
			# ﾎﾟｲﾝﾄ毎にどれぐらい挿入したか記録しておき各ｸﾞﾙｰﾌﾟの末尾に挿入していくとﾎﾟｲﾝﾄ毎にソートされる
			my $pt = $#ranks_num - $p{pt};
			my $num = 0;
			for my $i (0 .. $pt) {
				$num += $ranks_num[$i];
				$ranks_num[$i] += 1 if $i == $pt;
			}
			splice(@p_ranks, $num, 0, "$p{pt}<>$p{name}<>$p{country}<>$p{type}\n");
		}
		close $cfh;
	}

	#my @nums = (5, 11, 3, 2);
#	@p_ranks = sort {$b[0] <=> $a[0]} @p_ranks;

	my $calc = join(";" , (
		$in{rank}, $in{lea},
		$in{nou_c}, $in{sho_c}, $in{hei_c},
		$in{mil5_1}, $in{mil5_2},
		$in{gai_c},
		$in{win_c_1}, $in{win_par_1}, $in{win_c_2}, $in{win_par_2}));
	unshift @p_ranks, "$time<>$in{min}<>$calc\n";

	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	print $fh @p_ranks;
	close $fh;
}
