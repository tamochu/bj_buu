my $this_file       = "$userdir/$id/shop.cgi";
my $shop_list_file  = "$logdir/shop_list.cgi";
my $this_file_detail= "$userdir/$id/shop_sale_detail.cgi";
#================================================
# ¤l‚Ì‚¨“X Created by Merino
#================================================

# Œšİ”ï—p
my $build_money = 100000;

# ‚¨“X‚É‚¨‚¯‚éÅ‘å”
my $max_shop_item = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "‘¼‚É‰½‚©‚µ‚Ü‚·‚©?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "©•ª‚Ì¤l‚Ì‚¨“X‚Ìİ’è‚ğ‚µ‚Ü‚·<br>";
		$mes .= "¦$sales_ranking_cycle_day“úŠÔ‚¨“X‚Ì”„ã‚ª‚È‚¢‚Æ‚¨“X‚Í©“®“I‚É•Â“X‚É‚È‚è‚Ü‚·<br>";
	}
	&menu('‚â‚ß‚é','¤•i‰{——', '“X“ª‚É’u‚­', '‚¨“X‚ÌĞ‰î', '‚¨“X‚ğŒš‚Ä‚é','“X“ª®—','’ •ëŠm”F');
}

sub tp_1 {
	return if &is_ng_cmd(1..6);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "‚·‚Å‚É©•ª‚Ì‚¨“X‚ğ‚Á‚Ä‚¢‚Ü‚·<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '¤l') {
			$mes .= "E‹Æ‚ª¤l‚Å‚È‚¢‚Æ‚¨“X‚ğŒš‚Ä‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
			&begin;
		}
		else {
			$mes .= "‚¨“X‚ğŒš‚Ä‚é‚É‚Í $build_money G‚©‚©‚è‚Ü‚·<br>";
			$mes .= "¦¤l‚Ì‚¨“X×İ·İ¸Ş‚ÌXV‚ª‹ß‚¢‚ÉŒš‚Ä‚é‚Æ‚·‚®‚É•Â“X‚µ‚Ä‚µ‚Ü‚¢‚Ü‚·<br>";
			&menu('‚â‚ß‚é','Œš‚Ä‚é');
		}
	}
	elsif (!-f $this_file) {
		$mes .= '‚Ü‚¸‚ÍA‚¨“X‚ğŒš‚Ä‚é•K—v‚ª‚ ‚è‚Ü‚·<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# Œšİ
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "‚·‚Å‚É©•ª‚Ì‚¨“X‚ğ‚Á‚Ä‚¢‚Ü‚·<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('‚¨“X‚ğŒš‚Ä‚é‚Ì‚É¸”s‚µ‚Ü‚µ‚½');
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale.cgi" or &error('¾°Ù½Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ');
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('‚¨“XØ½ÄÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ');
			print $fh3 "$m{name}“X<>$m{name}<>$dateŠJ“X<>0<>0<>1<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>¤l‚Ì‚¨“X‚ğŒš‚Ä‚Ü‚µ‚½</b>", 1);
			$mes .= '<br>‚³‚Á‚»‚­‚¨“X‚É¤•i‚ğ•À‚×‚Ü‚µ‚å‚¤<br>';
			$m{money} -= $build_money;
			$m{guild_number} = 0;
		}
		else {
			$mes .= '‚¨‹à‚ª‘«‚è‚Ü‚¹‚ñ<br>';
		}
	}
	&begin;
}

#=================================================
# ¤•i‰{——
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale.cgi" or &error("‚¨“XÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money, $update_t) = split /<>/, $line;
	$mes .= "ÅI”„ã“úF$month/$mday $hour:$min<br>";
	$mes .= "Œ»İ‚Ì”„ã‚°F$sale_cŒÂ $sale_money G<br>";
	
	$mes .= '<hr>—a‚©‚èŠ‚É–ß‚µ‚Ü‚·‚©?<br>';
	$mes .= '‚¨“X‚Ì¤•iˆê——<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>¤•i–¼</th><th>’l’i</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="checkbox" name="cmd_$no" value="1">|;
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>’l’iF<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p><input type="submit" value="’l’i•ÏX" class="button1"></p></form>|;
	
	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	my $checked = 0;
	if ($m{is_full} && $in{price} == 0) {
		$mes .= '—a‚©‚èŠ‚ª‚¢‚Á‚Ï‚¢‚Å‚·<br>';
		&begin;
		return;
	}
	else {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($in{"cmd_$no"}) {
				$checked = 1;
				if ($in{price} == 0) {
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv);
					$mes .= &get_item_name($kind, $item_no);
					$mes .= '‚ğ—a‚©‚èŠ‚É–ß‚µ‚Ü‚µ‚½<br>';
				} elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} > 5000000) {
					$mes .= '’l’i‚Í 1 G ˆÈã 500–œ0000 GˆÈ“à‚É‚·‚é•K—v‚ª‚ ‚è‚Ü‚·<br>';
					&begin;
					return;
				} else {
					push @lines, "$no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
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
	if($checked){
		&tp_100;
	}else{
		&begin;
	}
}

#=================================================
# “X“ª‚É’u‚­
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;
	
	$mes .= '‚Ç‚ê‚ğ‚¨“X‚Éo‚µ‚Ü‚·‚©?<br>';
	$mes .= qq|<form method="$method" action="$script"><br>|;

	open my $fh, "< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$mes .= qq|<input type="checkbox" name="cmd$i" value="1" /><a href="shop_big_data.cgi?item=${kind}_${item_no}" target="_blank">|;
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		++$i;
		$mes .= qq|</a><br>|;
	}
	close $fh;
	$mes .= qq|<p>’l’iF<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="‚¨“X‚É’u‚­" class="button1"></p></form>|;
	
	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my $put = 0;
	my @shop_items = ();
	open my $in, "< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	push @shop_items, $_ while <$in>;
	close $in;
	
	my $item_num = @shop_items;
	if ($item_num >= $max_shop_item) {
		$mes .= '‚±‚êˆÈã‚¨“X‚É¤•i‚ğ’u‚­‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>';
		&begin;
		return;
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} > 5000000) {
		$mes .= '’l’i‚Í 1 G ˆÈã 500–œ0000 GˆÈ“à‚É‚·‚é•K—v‚ª‚ ‚è‚Ü‚·<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	my $i = 1;
	my($last_no) = (split /<>/, $shop_items[-1])[0];
	open my $fh, "+< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($in{'cmd' . $i} && $item_num < $max_shop_item) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			
			++$last_no;
			
			open my $fh2, ">> $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
			print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
			close $fh2;
			
			$mes .= &get_item_name($kind, $item_no, $item_c);
			$mes .= "‚ğ $in{price} G‚Å“X“ª‚É•À‚×‚Ü‚µ‚½<br>";
			$item_num++;
			$put = 1;
		}
		else {
			push @lines, $line;
		}
		
		++$i;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($put) {
		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# ‚¨“X‚Ìİ’è
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('‚¨“XØ½Ä‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display ,$guild_number) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|‘O‰ñ‚Ì”„ãF$sale_cŒÂ $sale_money G<br>|;
			$mes .= qq|<hr>‚¨“X‚Ì–¼‘O[‘SŠp8(”¼Šp16)•¶š‚Ü‚Å]F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|Ğ‰î•¶[‘SŠp20(”¼Šp40)•¶š‚Ü‚Å]F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="checkbox" name="display" value="1" checked>¤•i‰¿Ši‚ğˆê——‚Éæ‚¹‚é<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="•ÏX‚·‚é" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# ‚¨“X‚ª‚ ‚é‚Ì‚ÉØ½Ä‚É‚È‚¢‚Ì‚Í‚¨‚©‚µ‚¢‚Ì‚Å‚à‚¤ˆê“x’Ç‰Á
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('‚¨“XØ½ÄÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ');
		print $fh3 "$m{name}“X<>$m{name}<>$dateŠJ“X<>0<>0<>1<>0<>\n";
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
		$mes .= '‚â‚ß‚Ü‚µ‚½';
		&begin;
		return;
	}
	
	&error('‚¨“X‚Ì–¼‘O‚ª’·‚·‚¬‚Ü‚·B‘SŠp8(”¼Šp16)•¶š‚Ü‚Å') if length $in{name} > 16;
	&error('Ğ‰î•¶‚ª’·‚·‚¬‚Ü‚·B‘SŠp20(”¼Šp40)•¶š‚Ü‚Å') if length $in{message} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('‚¨“XØ½Ä‚ªŠJ‚¯‚Ü‚¹‚ñ');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "‚¨“X‚Ì–¼‘O‚ğ $in{name} ‚É•Ï‚¦‚Ü‚µ‚½<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "Ğ‰î•¶‚ğ $in{message} ‚É•Ï‚¦‚Ü‚µ‚½<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}
			unless ($display eq $in{display}) {
				$mes .= "¤•i‰¿Ši‚ğˆê——‚Éæ‚¹‚Ü‚µ‚½<br>" if $in{display};
				$display = $in{display};
				$is_rewrite = 1;
			}
			
			if ($is_rewrite) {
				unless ($m{guild_number}){
					$m{guild_number} = 0;
				}
				$guild_number = $m{guild_number};
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>$display<>$guild_number<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("‚·‚Å‚É“¯‚¶–¼‘O‚Ì‚¨“X‚ª‘¶İ‚µ‚Ü‚·");
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
# ‚¨“X‚Ì®—
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	
	while (my $line = <$fh>){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$line = "$no<>2<>42.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 2 && $item_no == 53);
		$line = "$no<>3<>76.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 3 && $item_no == 180);
		$line = "$no<>3<>77.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 3 && $item_no == 181);
		push @lines, $line;
	}
	@lines = map { $_->[0] }
				sort { $a->[2] <=> $b->[2] || $a->[3] <=> $b->[3] }
					map { [$_, split /<>/ ] } @lines;
	my $i = 1;
	for my $line (@lines){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		if($kind == 2 && $item_no == 42.5){
			$line = "$i<>2<>53<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 76.5){
			$line = "$i<>3<>180<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 77.5){
			$line = "$i<>3<>181<>$item_c<>$item_lv<>$price<>\n";
		}else {
			$line = "$i<>$kind<>$item_no<>$item_c<>$item_lv<>$price<>\n";
		}
		push @sub_lines, $line;
		$i++;
	}
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @sub_lines;
	close $fh;
	
	$mes .= "“X“ª‚ğ®—‚µ‚Ü‚µ‚½<br>";
	&begin;
}

#=================================================
# ’ •ëŠm”F
#=================================================
sub tp_600 {
	unless (-f $this_file_detail) {
		&begin;
		return;
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "< $this_file_detail" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>){
		$layout = 2;
		my($item_name, $buyer, $sell_time) = split /<>/, $line;
		my($sell_min,$sell_hour,$sell_mday,$sell_mon,$sell_year) = (localtime($sell_time))[1..4];
		$sell_date = sprintf("%d/%d %02d:%02d", $sell_mon+1,$sell_mday,$sell_hour,$sell_min);
		$mes .= "$item_nameF$buyer‚ª”ƒ‚¤($sell_date)<br>";
	}
	close $fh;
	
	&begin;
}

1; # íœ•s‰Â
