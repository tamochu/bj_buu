#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# ｶｼﾞﾉﾗﾝｷﾝｸﾞ 
#=================================================

# 表示するもの(./log/にあるもの)　◎追加/変更/削除/並べ替え可能
my @files = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名(shop_list_xxxx←の部分)'],
	['商人のお店',	'',			'個'],
	['美の画伯館',	'picture',	'枚'],
	['ﾌﾞｯｸﾏｰｹｯﾄ',	'book',		'冊'],
	['商人の銀行',	'bank',		'回'],
);

# 最低限必要な売上数
my $min_sale_c = 20;

# 上納金
my $treasury_base = 100000;

#=================================================
&decode;
&header;
&read_cs;

my $type = '_casino';
my $flag_file = "$logdir/sales_ranking_casino_cycle_flag.cgi";
my $this_file = "$logdir/shop_list_casino.cgi";
my $casino_cycle_day = int($sales_ranking_cycle_day / 5);
$casino_cycle_day = 1 if $casino_cycle_day <= 0;

&update_sales_ranking if -M $flag_file > $casino_cycle_day;
&run;
&footer;
exit;

#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	my $flag_time = (stat $flag_file)[9];
	my($min, $hour, $mday, $month) = ( localtime( $flag_time + $sales_ranking_cycle_day * 24 * 3600) )[1..4];
	++$month;

	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	for my $i (0 .. $#files) {
		print qq|<a href="sales_ranking.cgi?no=$i">$files[$i][0]</a> / |;
	}
	print qq|違法ｶｼﾞﾉ / |;
	print qq|<h1>違法ｶｼﾞﾉ売上ﾗﾝｷﾝｸﾞ</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞと各お店の売上金と売上数は、$sales_ranking_cycle_day日ごとにﾘｾｯﾄされ更新されます|;

	print qq|<li>更新のﾀｲﾐﾝｸﾞでプレイ回数数が $min_sale_c個未満のお店は閉店となります|;
	print qq|<li>次の更新時間：$month月$mday日$hour時$min分</ul></div><br>|;
	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>売上金</th><th>売上数</th><th>店名</th><th>店長</th><th>ﾒｯｾｰｼﾞ</th></tr>| unless $is_mobile;
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while ($line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		print $is_mobile     ? qq|<hr><b>$rank</b>位/$sale_money ｺｲﾝ/$sale_c 回/$shop_name/$name/$message/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$rank位</th><td align="right">$sale_money ｺｲﾝ</td><td align="right">$sale_c 回</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$rank位</th><td align="right">$sale_money ｺｲﾝ</td><td align="right">$sale_c 回</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# 売上ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_sales_ranking  {
	# 更新周期ﾌﾗｸﾞﾌｧｲﾙを更新
	open my $fh9, "> $flag_file";
	close $fh9;
	
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		# ﾊﾞｸﾞでお店が二つになっているものを除く
		next if ++$sames{$name} > 1;

		my $id = unpack 'H*', $name;
		next unless -f "$userdir/$id/shop${type}.cgi";
		
		open my $fh2, "+< $userdir/$id/casino_pool.cgi";
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
		
		# 人気チェック
		if ($slot_runs <= $min_sale_c) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			
			&write_send_news("<b>$nameの経営する$shop_nameは経営破綻のため閉店しました</b>", 1, $name);
		} else {
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "$pool<>0<>0<>";
			close $fh2;
			
			push @lines, "$shop_name<>$name<>$message<>$slot_runs<>$this_term_gain<>\n";
		}
	}
	@lines = map{ $_->[0] } sort { $b->[4] <=> $a->[4] } map { [$_, split /<>/] } @lines;
	
	my @new_lines = ();
	if (@lines) {
		my $line = pop @lines;
		my $min_sale_c = 0;
		while (@lines) {
			my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
			if (!$min_sale_c) {
				$min_sale_c = $sale_c;
			}
			if ($sale_c == $min_sale_c) {
				my $id = unpack 'H*', $name;
				unlink "$userdir/$id/shop${type}.cgi";
				unlink "$userdir/$id/shop_sale${type}.cgi";
				&write_send_news("<b>$nameの経営する$shop_nameは経営破綻のため閉店しました</b>", 1, $name);
				open my $fh, ">> $userdir/$id/ex_c.cgi";
				print $fh "ban_c<>1<>\n";
				close $fh;
			} else {
				unshift @new_lines, $line;
			}
			$line = pop @lines;
		}
		unshift @new_lines, $line;
	}

	$top_name = '';
	$treasury = 0;
	for my $line (@new_lines) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($top_name eq '') {
			$top_name = $name;
		} else {
			my $id = unpack 'H*', $name;
			open my $fh2, "+< $userdir/$id/casino_pool.cgi";
			eval { flock $fh2, 2; };
			my $line2 = <$fh2>;
			my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
			$treasury_s = $treasury_base + int($pool * 0.01);
			if ($pool > $treasury_s) {
				$treasury += $treasury_s;
				$pool -= $treasury_s;
			} else {
				$treasury += $pool;
				$pool = 0;
			}
			
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "$pool<>0<>0<>";
			close $fh2;
		}
	}
	my $id = unpack 'H*', $top_name;
	open my $fh2, "+< $userdir/$id/casino_pool.cgi";
	eval { flock $fh2, 2; };
	my $line2 = <$fh2>;
	my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
	
	$pool += $treasury;
	
	seek  $fh2, 0, 0,;
	truncate $fh2, 0;
	print $fh2 "$pool<>0<>0<>";
	close $fh2;
	
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @new_lines;
	close $fh;
}