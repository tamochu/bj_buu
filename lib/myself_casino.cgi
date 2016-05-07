my $this_file       = "$userdir/$id/shop_casino.cgi";
my $this_pool_file  = "$userdir/$id/casino_pool.cgi";
my $shop_list_file  = "$logdir/shop_list_casino.cgi";
require "$datadir/slots.cgi";
#================================================
# 違法ｶｼﾞﾉ
#================================================

# 建設費用
my $build_money = 100000;


if ($m{coin} > 2500000) {
	$m{coin} = 2500000;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "自分のｶｼﾞﾉの設定をします<br>";
		$mes .= "※$sales_ranking_cycle_day日間お店の売上がないとお店は自動的に閉店になります<br>";
	}
	&menu('やめる','台閲覧', '台追加', 'お店の紹介', 'お店を建てる', 'ｺｲﾝをプールする');
}

sub tp_1 {
	return if &is_ng_cmd(1..5);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "すでに自分のお店を持っています<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '商人') {
			$mes .= "職業が商人でないとお店を建てることができません<br>";
			&begin;
		}
		else {
			$mes .= "お店を建てるには $build_money Gかかります<br>";
			$mes .= "※商人のお店ﾗﾝｷﾝｸﾞの更新が近い時に建てるとすぐに閉店してしまいます<br>";
			&menu('やめる','建てる');
		}
	}
	elsif (!-f $this_file) {
		$mes .= 'まずは、お店を建てる必要があります<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# 建設
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "すでに自分のお店を持っています<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('お店を建てるのに失敗しました');
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_casino.cgi" or &error('ｾｰﾙｽﾌｧｲﾙが開けません');
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_casino.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('お店ﾘｽﾄﾌｧｲﾙが開けません');
			print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
			close $fh3;
			
			open my $fh4, "> $this_pool_file" or &error('プールﾌｧｲﾙが開けません');
			print $fh4 "0<>0<>0<>";
			close $fh4;
			chmod $chmod, "$this_pool_file";
	
			&mes_and_send_news("<b>個人ｶｼﾞﾉを建てました</b>", 1);
			$mes .= '<br>さっそくお店に新台を並べましょう<br>';
			$m{money} -= $build_money;
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	&begin;
}

#=================================================
# 台閲覧
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;

	$mes .= '台を破棄しますか?<br>';
	$mes .= 'お店の台一覧<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>台名</th><th>レート</th><th>利益率</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
	while (my $line = <$fh>) {
		my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="checkbox" name="cmd_$no" value="1">$slots[$slot_no][1]</td><td align="right">$ratio ｺｲﾝ</td><td align="right">$profit</td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>レート：<input type="text" name="ratio" value="1" class="text_box1" style="text-align:right">ｺｲﾝ</p>|;
	$mes .= qq|<p>利益率：<input type="text" name="profit" value="-100" class="text_box1" style="text-align:right">%</p>|;
	$mes .= qq|<p>破棄<input type="checkbox" name="delete" value="1"></p>|;
	$mes .= qq|<p><input type="submit" value="変更" class="button1"></p></form>|;
	
	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	my $checked = 0;
	
	if ($in{ratio} =~ /[^0-9]/ || $in{ratio} < 0 || $in{ratio} > 2500000) {
		$mes .= 'レートが不正です。';
		&begin;
		return;
	}
	if ($in{profit} !~ /^-?[0-9]+$/ || $in{profit} > 100 || $in{profit} < -100) {
		$mes .= '利益率が不正です。';
		&begin;
		return;
	}
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
		
		if ($in{"cmd_$no"} && $in{ratio} ne '0') {
			$checked = 1;
			if ($in{delete} eq '1') {
				$mes .= "$slot_nameを破棄しました<br>";
			} else {
				if ($slots[$slot_no][5]) {
					$profit = $in{profit} / 100.0;
				}
				push @lines, "$no<>$slot_no<>$in{ratio}<>$profit<>\n";
			}
		} else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if($checked){
		&tp_100;
	}else{
		&begin;
	}
}

#=================================================
# 新台追加
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;
	
	$mes .= 'どれを追加しますか?<br>';
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	for my $i (1..$#slots) {
		$profit = $slots[$i][5] ? qq|<input type="text" name="profit_$i" value="0" class="text_box1" style="text-align:right">%| : $slots[$i][2];
		$mes .= qq|<input type="radio" name="cmd" value="$i">$slots[$i][1] 利益率:$profit 導入料:$slots[$i][3]<br>|;
	}
	
	$mes .= qq|<p>レート：<input type="text" name="ratio" value="1" class="text_box1" style="text-align:right">ｺｲﾝ</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="新台追加" class="button1"></p></form>|;
	
	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	if ($cmd && $m{money} >= $slots[$cmd][3]) {
		my @shop_items = ();
		open my $in, "< $this_file" or &error("$this_fileが読み込めません");
		push @shop_items, $_ while <$in>;
		close $in;
		
		if ($in{ratio} =~ /[^0-9]/ || $in{ratio} <= 0 || $in{ratio} > 2500000) {
			$mes .= 'レートは 1 ｺｲﾝ 以上 250万0000 ｺｲﾝ以内にする必要があります<br>';
			&begin;
			return;
		}
		$profit = $slots[$cmd][2];
		if ($slots[$cmd][5]) {
			if ($in{"profit_$cmd"} !~ /^-?[0-9]+$/ || $in{"profit_$cmd"} > 100 || $in{"profit_$cmd"} < -100) {
				$mes .= '利益率は -100以上 100以下にする必要があります<br>';
				&begin;
				return;
			}
			$profit = $in{"profit_$cmd"} / 100.0;
		}
		
		my($last_no) = (split /<>/, $shop_items[-1])[0];
		++$last_no;
		
		open my $fh2, ">> $this_file" or &error("$this_fileが開けません");
		print $fh2 "$last_no<>$slots[$cmd][0]<>$in{ratio}<>$profit<>\n";
		close $fh2;
		
		$m{money} -= $slots[$cmd][3];
		
		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# お店の設定
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('お店ﾘｽﾄが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|前回の売上：$sale_c個 $sale_money G<br>|;
			$mes .= qq|<hr>お店の名前[全角8(半角16)文字まで]：<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|紹介文[全角20(半角40)文字まで]：<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="変更する" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# お店があるのにﾘｽﾄにないのはおかしいのでもう一度追加
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('お店ﾘｽﾄﾌｧｲﾙが開けません');
		print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
		close $fh3;
	}
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= 'やめました';
		&begin;
		return;
	}
	
	&error('お店の名前が長すぎます。全角8(半角16)文字まで') if length $in{name} > 16;
	&error('紹介文が長すぎます。全角20(半角40)文字まで') if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	my %names = ();
	open my $fh, "+< $shop_list_file" or &error('お店ﾘｽﾄが開けません');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		next if $names{$name}++;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "お店の名前を $in{name} に変えました<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "紹介文を $in{message} に変えました<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}
			
			if ($is_rewrite) {
				unless ($m{guild_number}){
					$m{guild_number} = 0;
				}
				$guild_number = $m{guild_number};
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("すでに同じ名前のお店が存在します");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#=================================================
# ｺｲﾝプール
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_pool_file" or &error("$this_pool_fileが開けません");
	my $pool, $this_term_gain, $slot_runs;
	while (my $line = <$fh>){
		($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
	}
	close $fh;
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|現在のプールｺｲﾝ数：$poolｺｲﾝ<br>|;
	$mes .= qq|<input type="radio" name="multiple" value="1" checked>プールする<br>|;
	$mes .= qq|<input type="radio" name="multiple" value="-1">引き出す<br>|;
	$mes .= qq|<input type="text" name="pool" value="0" class="text_box_b"> ｺｲﾝ<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="プールする" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_510 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	unless (-f $this_pool_file) {
		&begin;
		return;
	}
	
	$push = $in{multiple} * $in{pool};

	if ($m{coin} < $push) {
		$push = $m{coin};
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "+< $this_pool_file" or &error("$this_pool_fileが開けません");
	eval { flock $fh, 2; };
	
	while (my $line = <$fh>){
		my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
		if ($pool + $push > 0) {
			$pool += $push;
			$m{coin} -= $push;
		}
		push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
	}
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "ｺｲﾝをプールしました<br>";
	&begin;
}

1; # 削除不可
