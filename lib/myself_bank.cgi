my $this_file      = "$userdir/$id/shop_bank.cgi";
my $shop_list_file = "$logdir/shop_list_bank.cgi";
#================================================
# 商人の銀行 Created by Merino
#================================================

# 建設費用
my $build_money = 300000;

# 最少預金限度
my $min_deposit = 1000000;
# 最大預金限度
my $max_deposit = 4999999;

# 最少手数料
my $min_fee = 500;
# 最大手数料
my $max_fee = 100000;

# 最少預金者数
my $min_mem = 2;
# 最大預金者数
my $max_mem = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "以下の場合に銀行が倒産となります<br>";
		$mes .= "<li>$m{name}の資金が 0 G未満";
		$mes .= "<li>ﾗﾝｷﾝｸﾞ更新のﾀｲﾐﾝｸﾞで銀行への総預金額が 100万 G以下";
		$mes .= "<li>ﾗﾝｷﾝｸﾞ更新のﾀｲﾐﾝｸﾞで(自分以外)誰も銀行を利用していない";
	}
	&menu('やめる', '銀行の設定', '銀行を建てる','顧客データ','遺産没収');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '2') {
		if (-f $this_file) {
			$mes .= "すでに自分の銀行を持っています<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '商人') {
			$mes .= "職業が商人でないと銀行を建てことができません<br>";
			&begin;
		}
		else {
			$mes .= "銀行を建てるには $build_money Gかかります<br>";
			$mes .= "※銀行ﾗﾝｷﾝｸﾞの更新が近い時に建てるとすぐに倒産してしまいます<br>";
			&menu('やめる','建てる');
		}
	}
	elsif (!-f $this_file) {
		$mes .= 'まずは、銀行を建てる必要があります<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# 建設
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('銀行を建てるのに失敗しました');
			print $fh "1000<>5<>10<>4999999<>\n";
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_bank.cgi" or &error('ｾｰﾙｽﾌｧｲﾙが開けません');
			print $fh2 "0<>0<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_bank.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('銀行ﾘｽﾄﾌｧｲﾙが開けません');
			print $fh3 "$m{name}銀行<>$m{name}<>$date開店<>0<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>銀行を建てました</b>", 1);
			$m{money} -= $build_money;
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	&begin;
}

#=================================================
# 銀行の設定
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $head_line = <$fh>;
	close $fh;
	my($fee,$rishi,$max_pla,$max_dep) = split /<>/, $head_line;
	$max_pla = 10 unless $max_pla;
	$max_dep = 4999999 unless $max_dep;
	
	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('銀行ﾘｽﾄが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		my($year, $name, $money) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|前回[手続き数： $sale_c回 / 利益：$sale_money G]<br>|;
			$mes .= qq|<hr>手数料[$min_fee～$max_fee G]：<input type="text" name="fee" value="$fee" class="text_box_s" style="text-align: right">G<br>|;
			$mes .= qq|利率[0.1%～20.0%]：<input type="text" name="rishi" value="$rishi" class="text_box_s" style="text-align: right">×0.1%<br>|;
			$mes .= qq|利用人数[$min_mem～$max_mem人]：<input type="text" name="max_pla" value="$max_pla" class="text_box_s" style="text-align: right">人<br>|;
			$mes .= qq|預金限度[$min_deposit～$max_deposit G]：<input type="text" name="max_dep" value="$max_dep" class="text_box_s" style="text-align: right">G<br>|;
			$mes .= qq|<hr>銀行の名前[全角8(半角16)文字まで]：<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|紹介文[全角20(半角40)文字まで]：<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="変更する" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# 銀行があるのにﾘｽﾄにないのはおかしいのでもう一度追加
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('銀行ﾘｽﾄﾌｧｲﾙが開けません');
		print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
		close $fh3;
	}
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= 'やめました';
		&begin;
		return;
	}
	
	&error("銀行の名前が長すぎます。全角8(半角16)文字まで") if length $in{name} > 16;
	&error("紹介文が長すぎます。全角20(半角40)文字まで") if length $in{mes} > 40;
	&error("手数料は$min_fee～$max_fee Gまでです") if $in{fee} eq '' || $in{fee} =~ /[^0-9]/ || $in{fee} < $min_fee || $in{fee} > $max_fee;
	&error("利率は0.1%～20.0%までです") if $in{rishi} eq '' || $in{rishi} =~ /[^0-9]/ || $in{rishi} < 1 || $in{rishi} > 200;
	&error("利用人数は$min_mem～$max_mem人までです") if $in{max_pla} eq '' || $in{max_pla} =~ /[^0-9]/ || $in{max_pla} < $min_mem || $in{max_pla} > $max_mem;
	&error("預金限度は$min_deposit～$max_deposit Gまでです") if $in{max_dep} eq '' || $in{max_dep} =~ /[^0-9]/ || $in{max_dep} < $min_deposit || $in{max_dep} > $max_deposit;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('銀行ﾘｽﾄが開けません');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "銀行の名前を $in{name} に変えました<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "紹介文を $in{message} に変えました<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}
			
			if ($is_rewrite) {
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("すでに同じ名前の銀行が存在します");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	&regist_my_bank;

	&begin;
}

#=================================================
# 顧客情報
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		$mes .= qq|「$name 様」$world_name暦$year年から $money G 預けています<br>|;
	}
	close $fh;

	&begin;
}

#=================================================
# 遺産没収（キャラがなくなった人の預金データを消します）
#=================================================
sub tp_400 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		my $id = unpack 'H*', $name;
		unless(-f "$userdir/$id/user.cgi"){
			$mes .= qq|故$name 様の預金 $money G を回収しました<br>|;
			&send_money($m{name}, "【遺産没収】$name", $money);
		}else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&begin;
}



sub regist_my_bank {
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($fee,$rishi,$max_pla,$max_dep) = split /<>/, $head_line;
	$max_pla = 10 unless $max_pla;	
	$max_dep = 4999999 unless $max_dep;

	unless ($fee eq $in{fee}) {
		$mes .= "手数料を $in{fee} Gに変えました<br>";
		$is_rewrite = 1;
	}
	unless ($rishi eq $in{rishi}) {
		my $r = $in{rishi} / 10.0;
		$mes .= "利率を $r%に変えました<br>";
		$is_rewrite = 1;
	}
	unless ($max_pla eq $in{max_pla}) {
		$mes .= "利用人数を $in{max_pla}人に変えました<br>";
		$is_rewrite = 1;
	}
	unless ($max_dep eq $in{max_dep}) {
		$mes .= "預金限度額を $in{max_dep} Gに変えました<br>";
		$is_rewrite = 1;
	}
	if ($is_rewrite) {
		push @lines, "$in{fee}<>$in{rishi}<>$in{max_pla}<>$in{max_dep}<>\n";
	}
	else {
		return;
	}
	
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # 削除不可
