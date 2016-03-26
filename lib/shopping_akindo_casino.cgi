$mes .= qq|ｺｲﾝ $m{coin} 枚<br>| if ($is_mobile || $is_smart);
#================================================
# 違法カジノ
#================================================
require "$datadir/slots.cgi";

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方は出入り禁止です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "どのｶｼﾞﾉで打ちますか?<br>";
	
	my $count = 0;
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>店名</th><th>店長</th><th>紹介文<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list_casino.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop_casino.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
		$count++;
	}
	close $fh;

	$m{stock} = $count;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ｶｼﾞﾉに入る" class="button1"></p></form>|;
}

#================================================
# お店の商品一覧表示
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_casino.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが開けません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;

	# お店が存在しない
	if (!$is_find || !-f "$userdir/$shop_id/shop_casino.cgi") {
		$mes .= "$m{stock}というお店は閉店してしまったようです<br>";
		&begin;
	}
	# 自分のお店で買い物できてしまうと、売上ﾗﾝｷﾝｸﾞが崩壊してしまうので。
	elsif ($m{name} eq $y{name}) {
		$mes .= "自分のお店で買い物することはできません<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop_casino.cgi") {
		$mes .= qq|【$m{stock}】$y{name}「$shop_message」<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<table class="table1"><tr><th>台</th><th>レート<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop_casino.cgi" or &error("$y{name}に入れません");
		while (my $line = <$fh>) {
			my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
			$mes .= qq|<tr><td><input type="radio" name="cmd" value="$no">$slots[$slot_no][1]</td><td align="right">$ratio ｺｲﾝ<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="打つ" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	else {
		&begin;
	}
}

#================================================
# ｶｼﾞﾉ開始処理
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop_casino.cgi") {
		open my $fh, "< $userdir/$shop_id/shop_casino.cgi" or &error("商品ﾘｽﾄが開けません");
		while (my $line = <$fh>) {
			my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$y{cha} = 0;
				$y{lea} = $slot_no;
				$y{wea} = $ratio;
				$y{ag} = $profit;
				$m{tp} = 110;
				&menu('Play', 'やめる');
			}
		}
		close $fh;
	} else {
		$mes .= 'やめました<br>';
		&begin
	}
}

sub tp_110 {
	&{ $slots[$y{lea}][4][$y{cha}] };
}

1; # 削除不可
