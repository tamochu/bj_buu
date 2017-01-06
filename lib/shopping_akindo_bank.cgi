#================================================
# 商人の銀行 Created by Merino
#================================================

# 一つの銀行で利用できる最大人数
my $max_player_bank = 10;

# 最低入金額
my $min_save_money = 10000;

# 初期預金制限
my $default_max = 4999999;

# 潰れない銀行
my $guild_bank_name = 'guild_bank_kurabota_world_bank';
my $guild_bank_shop_name = '黒豚世界銀行';
my $guild_bank_fee = 20000;
my $guild_bank_player_max = 2000;
my $guild_bank_rishi = -5;

#================================================
# 銀行の名前一覧表示
#================================================
sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "現在契約している銀行【経営者 $m{bank}】<br>" if $m{bank};
	$mes .= "どこの銀行に行きますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= $m{bank} ? qq|<input type="radio" name="cmd" value="0">やめる<br>|:qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>銀行名</th><th>経営者</th><th>紹介文<br></th></tr>| unless $is_mobile;

	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		my $shop_id = unpack 'H*', $name;
		next unless -f "$userdir/$shop_id/shop_bank.cgi";

		if ($m{bank} eq $name){
			$is_find = 1;
			$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name" checked>$shop_name<br>|
				 : qq|<tr><td><input type="radio" name="cmd" value="$name" checked>$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
		}else {
			$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
				 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
		}
	}
	close $fh;
	if ($m{bank} eq $guild_bank_name){
		$is_find = 1;
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$guild_bank_name" checked>$guild_bank_shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$guild_bank_name" checked>$guild_bank_shop_name</td><td>システム</td><td>メッセージ募集中<br></td></tr>|;
	}else {
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$guild_bank_name">$guild_bank_shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$guild_bank_name">$guild_bank_shop_name</td><td>システム</td><td>メッセージ募集中<br></td></tr>|;
	}
	$m{bank} = '' unless $is_find;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="銀行に入る" class="button1"></p></form>|;
}

#================================================
# 銀行入店
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	if ($y{name} eq $guild_bank_name) {
		$m{stock} = $guild_bank_shop_name;
		my($fee, $rishi, $max_pla, $max_dep) = ($guild_bank_fee, $guild_bank_rishi, $guild_bank_player_max, $default_max); 
		$mes .= "【$m{stock}】手数料$fee G / 利率 $rishi % / 預金上限 $max_dep G<br>";
		$mes .= "黒豚「ぶー」<br>";
		
		&menu('やめる', 'ご入金', 'お引出し');
		$m{tp} = 20;
	} else {
		my $shop_id = unpack 'H*', $y{name};

		my $shop_message = '';
		my $is_find = 0;
		open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiﾌｧｲﾙが開けません");
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
		# 銀行が存在しない
		if (!$is_find || !-f "$userdir/$shop_id/shop_bank.cgi") {
			$mes .= "$m{stock}という銀行は閉店してしまったようです<br>";
			&begin;
		}
		else {
			my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
			$mes .= "【$m{stock}】手数料$fee G / 利率 $rishi % / 預金上限 $max_dep G<br>";
			$mes .= "$y{name}「$shop_message」<br>";
			
			&menu('やめる', 'ご入金', 'お引出し');
			$m{tp} = 10;
		}
	}
}

sub tp_10 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

sub tp_20 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100 + 200;
	&{ 'tp_'. $m{tp} };
}

sub bank_price {
	my $bank_file = shift;
	
	open my $fh, "< $bank_file" or &error("$bank_fileﾌｧｲﾙが開けません");
	my $line = <$fh>;
	close $fh;
	
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $line;
	$max_pla = $max_player_bank unless $max_pla;	
	$max_dep = $default_max unless $max_dep;
	$rishi /= 10.0;
	return $fee, $rishi, $max_pla, $max_dep;
}



#================================================
# 入金
#================================================
sub tp_100 {
	if ($m{bank} ne '' && $m{bank} ne $y{name}) {
		$mes .= "他の銀行を利用する場合は、現在利用している銀行から全額引出す必要があります<br>";
		&begin;
		return;
	}
	my $shop_id = unpack 'H*', $y{name};
	
	my $count = 0;
	my $last_year = '';
	my $save_money = 0;
	open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
		++$count;
	}
	close $fh;
	
	my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
	if ($save_money > 0 || $count < $max_pla) {
		$mes .= qq|【$m{stock}】手数料$fee G / 利率 $rishi% / 預金上限 $max_dep G<br>|;
		$mes .= qq|$world_name暦$last_year年から $save_money G 預けています<br>| if $save_money > 0;
		$mes .= qq|いくら入金しますか?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="text" name="save_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<p><input type="submit" value="入金" class="button1"></p></form>|;
		
		$m{tp} = 110;
		&n_menu;
	}
	else {
		$mes .= "$m{stock}は定員がいっぱいで、ご利用することができません<br>";
		&begin;
	}
}
sub tp_110 {
	if ($in{save_money} <= 0 || $in{save_money} =~ /[^0-9]/) {
		$mes .= "やめました<br>";
		&begin;
		return;
	}
	elsif ($min_save_money > $in{save_money}) {
		$mes .= "入金額は最低でも $min_save_money G以上必要です<br>";
		&tp_100;
		return;
	}

	my $shop_id = unpack 'H*', $y{name};
	my $save_money = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $head_line;
	$max_pla = $max_player_bank unless $max_pla;	
	$max_dep = $default_max unless $max_dep;

	# 全額
	if ($in{save_money} > $m{money}) {
		$in{save_money} = $m{money} - $fee;
		if ($m{name} ne $y{name} && $in{save_money} < $fee) {
			close $fh;
			$mes .= "手数料($fee G)が足りません<br>";
			&tp_100;
			return;
		}
	}
	elsif ($m{name} ne $y{name} && $m{money} - $in{save_money} < $fee) {
		close $fh;
		$mes .= "手数料($fee G)が足りません<br>";
		&tp_100;
		return;
	}
	
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($name eq $m{name}) {
			$save_money = $money;
		}
		else {
			push @lines, $line;
		}
	}
	
	if ($save_money + $in{save_money} > $max_dep) {
		$in{save_money} = $max_dep - $save_money;
		$save_money = $max_dep;
	}
	else {
		$save_money += $in{save_money};
	}
	$m{money} -= $in{save_money};

	if ($m{name} ne $y{name}) {
		$m{money} -= $fee;
		&send_money($y{name}, "【$m{stock}(手数料)】$m{name}", $fee);

		# 売上金加算
		open my $fh2, "+< $userdir/$shop_id/shop_sale_bank.cgi" or &error("売上ﾌｧｲﾙが開けません");
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($sale_c, $sale_money,$update_t) = split /<>/, $line2;
		$sale_c++;
		$sale_money += $fee;
		seek  $fh2, 0, 0;
		truncate $fh2, 0;
		print $fh2 "$sale_c<>$sale_money<>$update_t<>";
		close $fh2;
		$mes .= "手数料 $fee Gを支払い、";
	}

	push @lines, "$w{year}<>$m{name}<>$save_money<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "$in{save_money} G入金しました(預金額 $save_money G)<br>";
	$m{bank} = $y{name};

	&run_tutorial_quest('tutorial_bank_1');
	$mes .= $tutorial_mes;

	&tp_1;
}

#================================================
# お引出し処理
#================================================
sub tp_200 {
	my $shop_id = unpack 'H*', $y{name};
	
	my $last_year = 0;
	my $save_money = 0;
	open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
	}
	close $fh;
	
	if ($save_money == 0) {
		if($y{name} eq $m{bank}){
			$m{bank} = '';
		}
		$mes .= "$m{name}さんからのお金は預かっていません<br>";
		&begin;
	}
	else {
		my($fee, $rishi, $max_pla, $max_dep) = &bank_price("$userdir/$shop_id/shop_bank.cgi"); 
		$mes .= qq|【$m{stock}】手数料$fee G / 利率 $rishi% / 預金上限 $max_dep G<br>|;
		$mes .= qq|$world_name暦$last_year年から $save_money G 預けています<br>いくら引出しますか?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="get_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="引出し" class="button1"></p></form>|;
		
		$m{tp} += 10;
		&n_menu;
	}
}
sub tp_210 {
	$cmd = $y{name};
	if ($in{get_money} <= 0 || $in{get_money} =~ /[^0-9]/) {
		$mes .= "やめました<br>";
		&tp_1;
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };

	my $head_line = <$fh>;
	my($fee, $rishi, $max_pla, $max_dep) = split /<>/, $head_line;
	my $v;
	
	if ($m{name} ne $y{name} && $m{money} < $fee) {
		$mes .= "手数料($fee G)が足りません";
		&tp_1;
		return;
	}
	
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;

		if ($m{name} eq $name) {
			$is_rewrite = 1;
			
			$v = int( $money * ($w{year} - $year) * $rishi * 0.001);
			$in{get_money} = $money if $in{get_money} >= $money;
			$m{money} += int($in{get_money} + $v);
			$money -= $in{get_money};
			
			if ($m{name} ne $y{name}) {
				$m{money} -= $fee;
				&send_money($y{name}, "【$m{stock}(手数料)】$m{name}", $fee);
				$mes .= "手数料 $fee G を支払い、" ;
			}

			$mes .= "$in{get_money} G引出しました(預金額 $money G)<br>";
			
			if ($v > 0 && $m{name} ne $y{name}) {
				$mes .= "年利として $v G引出し額にﾌﾟﾗｽされました<br>";
			}
			
			if ($money <= 0) {
				$m{bank} = '';
				$mes .= "入金金額が 0 G以下になりましたので、$m{stock}と契約が終了しました<br>";
			}
			else {
				push @lines, "$w{year}<>$m{name}<>$money<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	if ($v > 0 && $m{name} ne $y{name}) {
		&send_rishi($v);
	}
	&begin;
}

#================================================
# 入金
#================================================
sub tp_300 {
	if ($m{bank} ne '' && $m{bank} ne $y{name}) {
		$mes .= "他の銀行を利用する場合は、現在利用している銀行から全額引出す必要があります<br>";
		&begin;
		return;
	}
	my $count = 0;
	my $last_year = '';
	my $save_money = 0;
	open my $fh, "< $logdir/guild_bank.cgi" or &error("$logdir/guild_bank.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
		++$count;
	}
	close $fh;
	
	my($fee, $rishi, $max_pla, $max_dep) = ($guild_bank_fee, $guild_bank_rishi, $guild_bank_player_max, $default_max); 
	if ($save_money > 0 || $count < $max_pla) {
		$mes .= qq|【$m{stock}】手数料$fee G / 利率 $rishi% / 預金上限 $max_dep G<br>|;
		$mes .= qq|$world_name暦$last_year年から $save_money G 預けています<br>| if $save_money > 0;
		$mes .= qq|いくら入金しますか?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="text" name="save_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<p><input type="submit" value="入金" class="button1"></p></form>|;
		
		$m{tp} = 310;
		&n_menu;
	}
	else {
		$mes .= "$m{stock}は定員がいっぱいで、ご利用することができません<br>";
		&begin;
	}
}
sub tp_310 {
	if ($in{save_money} <= 0 || $in{save_money} =~ /[^0-9]/) {
		$mes .= "やめました<br>";
		&begin;
		return;
	}
	elsif ($min_save_money > $in{save_money}) {
		$mes .= "入金額は最低でも $min_save_money G以上必要です<br>";
		&tp_300;
		return;
	}

	my $save_money = 0;
	my @lines = ();
	open my $fh, "+< $logdir/guild_bank.cgi" or &error("$logdir/guild_bank.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my($fee, $rishi, $max_pla, $max_dep) = ($guild_bank_fee, $guild_bank_rishi, $guild_bank_player_max, $default_max); 
	$max_pla = $max_player_bank unless $max_pla;	
	$max_dep = $default_max unless $max_dep;

	# 全額
	if ($in{save_money} > $m{money}) {
		$in{save_money} = $m{money} - $fee;
		if ($m{name} ne $y{name} && $in{save_money} < 0) {
			close $fh;
			$mes .= "手数料($fee G)が足りません<br>";
			&tp_300;
			return;
		}
	}
	elsif ($m{name} ne $y{name} && $m{money} - $in{save_money} < $fee) {
		close $fh;
		$mes .= "手数料($fee G)が足りません<br>";
		&tp_300;
		return;
	}
	
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($name eq $m{name}) {
			$v = int( $money * ($w{year} - $year) * $rishi * 0.001);
			$save_money = $money + $v;
			if ($v < 0) {
				$mes .= "マイナス年利として $v Gマイナスされました<br>";
			}
		}
		else {
			push @lines, $line;
		}
	}
	
	if ($save_money + $in{save_money} > $max_dep) {
		$in{save_money} = $max_dep - $save_money;
		$save_money = $max_dep;
	}
	else {
		$save_money += $in{save_money};
	}
	$m{money} -= $in{save_money};

	if ($m{name} ne $y{name}) {
		$m{money} -= $fee;
		$mes .= "手数料 $fee Gを支払い、";
	}

	push @lines, "$w{year}<>$m{name}<>$save_money<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "$in{save_money} G入金しました(預金額 $save_money G)<br>";
	$m{bank} = $y{name};
	&tp_1;
}

#================================================
# お引出し処理
#================================================
sub tp_400 {
	my $last_year = 0;
	my $save_money = 0;
	open my $fh, "< $logdir/guild_bank.cgi" or &error("$logdir/guild_bank.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($m{name} eq $name) {
			$save_money = $money;
			$last_year = $year;
			last;
		}
	}
	close $fh;
	
	if ($save_money == 0) {
		if($y{name} eq $m{bank}){
			$m{bank} = '';
		}
		$mes .= "$m{name}さんからのお金は預かっていません<br>";
		&begin;
	}
	else {
		my($fee, $rishi, $max_pla, $max_dep) = ($guild_bank_fee, $guild_bank_rishi, $guild_bank_player_max, $default_max); 
		$mes .= qq|【$m{stock}】手数料$fee G / 利率 $rishi% / 預金上限 $max_dep G<br>|;
		$mes .= qq|$world_name暦$last_year年から $save_money G 預けています<br>いくら引出しますか?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="get_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="引出し" class="button1"></p></form>|;
		
		$m{tp} += 10;
		&n_menu;
	}
}
sub tp_410 {
	$cmd = $y{name};
	if ($in{get_money} <= 0 || $in{get_money} =~ /[^0-9]/) {
		$mes .= "やめました<br>";
		&tp_1;
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $logdir/guild_bank.cgi" or &error("$logdir/guild_bank.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };

	my($fee, $rishi, $max_pla, $max_dep) = ($guild_bank_fee, $guild_bank_rishi, $guild_bank_player_max, $default_max); 
	my $v;
	
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;

		if ($m{name} eq $name) {
			$is_rewrite = 1;
			
			$v = int( $money * ($w{year} - $year) * $rishi * 0.001);
			$in{get_money} = $money if $in{get_money} >= $money;
			$m{money} += int($in{get_money} + $v);
			$money -= $in{get_money};
			
			$m{money} -= $fee;
			$mes .= "手数料 $fee G を支払い、" ;

			$mes .= "$in{get_money} G引出しました(預金額 $money G)<br>";
			
			if ($v < 0) {
				$mes .= "マイナス年利として $v Gマイナスされました<br>";
			}
			
			if ($money <= 0) {
				$m{bank} = '';
				$mes .= "入金金額が 0 G以下になりましたので、$m{stock}と契約が終了しました<br>";
			}
			else {
				push @lines, "$w{year}<>$m{name}<>$money<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}

sub send_rishi {
	my $v = shift;
	my $y_id = unpack 'H*', $y{name};
	my %owner_datas = &get_you_datas($y_id, 1);
	my $same_bank = 0;
	
	if($owner_datas{bank} ne ''){
		my $shop_id = unpack 'H*', $owner_datas{bank};
	
		my $is_find = 0;
		open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgiﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
			if ($owner_datas{bank} eq $name) {
				$is_find = 1;
				last;
			}
		}
		close $fh;
	
		if (!$is_find || !-f "$userdir/$shop_id/shop_bank.cgi") {
			&send_money($y{name}, "【$m{stock}(年利代)】$m{name}", "-$v");
		}
		else {
			my @lines = ();
			open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };

			my $head_line = <$fh>;
			push @lines, $head_line;
			while (my $line = <$fh>) {
				my($year, $name, $money) = split /<>/, $line;

				if ($y{name} eq $name) {
					if ($v >= $money){
						my $diff = $v - $money;
						&send_money($y{name}, "【$m{stock}(年利代)】$m{name}", "-$diff");
						$v = $money;
					}
					$money -= $v;
			
					if ($money <= 0) {
						&regist_you_data($y{name},'bank','');
					}
					else {
						push @lines, "$year<>$name<>$money<>\n";
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
		}
	}
	else {
		&send_money($y{name}, "【$m{stock}(年利代)】$m{name}", "-$v");
	}
}

1; # 削除不可
