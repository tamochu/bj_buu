my $this_file      = "$userdir/$id/shop_$goods_dir.cgi";
my $this_path_dir  = "$userdir/$id/$goods_dir";
my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
#=================================================
# 自分の作品 Created by Merino
#=================================================
# ※このCGI単体では動きません myself_book.cgi,myself_picture.cgiを参照

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$m{tp} = 1;
		$mes .= "他に何かしますか?<br>";
	}
	else {
		$mes .= "$goods_nameの所有は最大$max_goods個までです<br>";
	}
	&menu("やめる", "$goods_nameを見る", "$goods_nameを捨てる", "$goods_nameを送る", "展示品を見る", "$goods_nameを展示する", "お店の設定", "お店を建てる");
}
sub tp_1 {
	return if &is_ng_cmd(1..7);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '7') {
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
			&menu("やめる","建てる");
		}
	}
	elsif ( $cmd >= 4 && $cmd <= 6 && !-f $this_file ) {
		$mes .= "まずは、お店を建てる必要があります<br>";
		&begin;
	}
	else {
		&{ "tp_". $m{tp} };
	}
}

#=================================================
# 作品を見る
#=================================================
sub tp_100 {
	$layout = 2;
	my $count = 0;
	my $sub_mes .= qq|<form method="$method" action="$script"><hr><input type="radio" name="file_name" value="0" checked>やめる|;
	opendir my $dh, $this_path_dir or &error("$this_path_dirﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;

		my $file_title = &get_goods_title($file_name);
		$sub_mes .= $goods_type eq 'img'  ? qq|<hr><img src="$this_path_dir/$file_name" style="vertical-align:middle;"> $file_title |
				  : $goods_type eq 'html' ? qq|<li><a href="$this_path_dir/$file_name" target="_blank">$file_title</a>|
				  :                         qq|<li>$file_title|;
				  ;
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">| if $file_name =~ /^_/;
		++$count;
	}
	closedir $dh;
	
	$mes .= qq|所有数 $count / $max_goods個<br>|;
	$mes .= qq|$non_titleの$goods_nameはﾀｲﾄﾙをつけることで、売ったり送ったりすることができます<br>|;
	$mes .= qq|<font color="#FF0000">※一度つけたﾀｲﾄﾙは変更することができません</font><br>|;
	$mes .= qq|$sub_mes<hr>|;
	$mes .= qq|ﾀｲﾄﾙ[全角8(半角16)文字まで]<br><input type="text" name="title" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="is_ad" value="1">$goods_nameを宣伝する($need_ad_money G)<br>|;
	$mes .= qq|<input type="checkbox" name="is_send_public" value="1">$goods_nameをデフォルトアイコンに追加する<br>| if $goods_type eq 'img';
	$mes .= qq|<input type="checkbox" name="is_send_library" value="1">$goods_nameを図書館に寄贈する<br>| if $goods_type eq 'html';
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ﾀｲﾄﾙをつける" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	if ($in{is_ad} && $m{money} < $need_ad_money) {
		$mes .= "宣伝費用金が足りません<br>";
	}
	elsif ($in{file_name} =~ /^_/) {
		&error("ﾀｲﾄﾙを記入してください") unless $in{title};
		&error("ﾀｲﾄﾙにﾋﾟﾘｵﾄﾞ(.)は使えません") if $in{title} =~ /\./;
		&error("ﾀｲﾄﾙの先頭にｱﾝﾀﾞｰﾗｲﾝ(_)は使えません") if $in{title} =~ /^_/;
		&error("文字数が大きすぎます最大全角8(半角16)文字まで") if length $in{title} > 16;
		
		my $file_title = unpack 'H*', "$in{title} 作:$m{name}";
		$file_title .= $goods_type eq 'img'  ? '.jpeg'
					 : $goods_type eq 'html' ? '.html'
					 :                         '.cgi'
					 ;
		
		&error("すでに同じ名前の作品が存在します") if -f "$this_path_dir/$file_title";
		
		if (-f "$this_path_dir/$in{file_name}") {
			rename "$this_path_dir/$in{file_name}", "$this_path_dir/$file_title" or &error("ﾘﾈｰﾑ処理に失敗しました");
			$mes .= "$in{title}というﾀｲﾄﾙをつけました<br>";
			
			# 宣伝
			if ($in{is_ad}) {
				if    ($goods_dir eq 'picture') { &write_picture_news(qq|$cs{name}[$m{country}]の$m{name}が <a href="$this_path_dir/$file_title"><img src="$this_path_dir/$file_title" style="vertical-align:middle;" width="25px" heigth="25px"></a>『$in{title}』という作品を発表\しました|); }
				elsif ($goods_dir eq 'book')    { &write_book_news(qq|$cs{name}[$m{country}]の$m{name}が『$in{title}』という作品を発表\しました|); }
				$mes .= "作品を発表\しました<br>";
				$m{money} -= $need_ad_money;
			}elsif($in{is_send_public}){
				my $def_file_title = unpack 'H*', "$time 作:$m{name}";
				rename "$this_path_dir/$file_title", "$icondir/_add_$def_file_title" or &error("ﾘﾈｰﾑ処理に失敗しました");
				$mes .= "デフォルトアイコンに追加しました<br>";
			}elsif($in{is_send_library}){
				rename "$this_path_dir/$file_title", "$logdir/library/$file_title" or &error("ﾘﾈｰﾑ処理に失敗しました");
				$mes .= "図書館に寄贈しました<br>";
			}
		}
		else {
			$mes .= "選択した$goods_nameが存在しません<br>";
		}
	}
	else {
		$mes .= "やめました<br>";
	}
	&begin;
}


#=================================================
# 作品を捨てる
#=================================================
sub tp_200 {
	$layout = 2;
	$mes .= qq|どの$goods_nameを捨てますか?<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p><input type="submit" value="捨てる" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	if ($in{file_name}) {
		my $file_title = &get_goods_title($in{file_name});
		unlink "$this_path_dir/$in{file_name}" or &error("選択した$goods_name($file_title)が存在しません");
		$mes .= qq|$file_titleを捨てました<br>|;

		&remove_shop_goods($in{file_name});
	}
	else {
		$mes .= "やめました<br>";
	}
	&begin;
}

#=================================================
# 作品を送る
#=================================================
sub tp_300 {
	$layout = 2;
	$mes .= "誰にどの$goods_nameを送りますか?<br>国内手数料：$need_send_money G<br>国外手数料：$need_send_money_other G<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<p>送信先：<input type="text" name="send_name" class="text_box1"></p>|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p><input type="submit" value="送る" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	if (!$in{file_name}) {
		$mes .= "やめました<br>";
		&begin;
		return;
	}
	elsif ($in{file_name} =~ /^_/) {
		$mes .= "$non_titleの作品は送ることができません<br>";
		&begin;
		return;
	}
	elsif ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方は送ることができません<br>";
		&begin;
		return;
	}
	elsif ($in{send_name} eq "") {
		$mes .= "送り先が記入されていません<br>";
		&begin;
		return;
	}

	my $send_id = unpack "H*", $in{send_name};
	my %datas = &get_you_datas($send_id, 1);
	my $pay = $datas{country} eq $m{country} ? $need_send_money : $need_send_money_other;
	
	if ($m{money} < $pay) {
		$mes .= "郵送手数料( $pay G)が足りません<br>";
	}
	elsif (!-f "$this_path_dir/$in{file_name}") {
		$mes .= "選択した$goods_nameは存在しません<br>";
	}
	elsif (-f "$userdir/$send_id/$goods_dir/$in{file_name}") {
		$mes .= "$datas{name}はすでにその$goods_nameを所持しています<br>";
	}
	elsif (&my_goods_count("$userdir/$send_id/$goods_dir") >= $max_goods) {
		$mes .= "$in{send_name}の所持品がいっぱいです<br>";
	}
	else {
		rename "$this_path_dir/$in{file_name}", "$userdir/$send_id/$goods_dir/$in{file_name}" or &error("$goods_nameを送るのに失敗しました");
		my $file_title = &get_goods_title($in{file_name});
		&mes_and_send_news("$datas{name}に$file_titleを送りました");
		$m{money} -= $pay;

		my $img_title = $file_title;
		$img_title =~ s/.*作://;
		&send_money($img_title,"$file_titleの印税収入として国",int($pay*0.1));
		
		# 作品があるよﾌﾗｸﾞをたてる
		open my $fh, "> $userdir/$send_id/goods_flag.cgi";
		close $fh;

		&remove_shop_goods($in{file_name});
	}
	
	&begin;
}

#=================================================
# 建設
#=================================================
sub tp_700 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "すでに自分のお店を持っています<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error("お店を建てるのに失敗しました");
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_$goods_dir.cgi" or &error("$userdir/$id/shop_sale_$goods_dir.cgi ﾌｧｲﾙが開けません");
			print $fh2 "0<>1<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_$goods_dir.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error("$shop_list_fileﾌｧｲﾙが開けません");
			print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>$goods_nameのお店を建てました</b>", 1);
			$mes .= "<br>さっそくお店に作品を並べましょう<br>";
			$m{money} -= $build_money;
		}
		else {
			$mes .= "お金が足りません<br>";
		}
	}
	else {
		$mes .= "やめました<br>";
	}
	&begin;
}

#=================================================
# 展示品を見る
#=================================================
sub tp_400 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale_$goods_dir.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale_$goods_dir.cgi" or &error("$userdir/$id/shop_sale_$goods_dir.cgiﾌｧｲﾙが読み込めません");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money) = split /<>/, $line;
	
	$mes .= "最終売上日時：$month/$mday $hour:$min<br>";
	$mes .= "現在の売上げ：$sale_c個 $sale_money G<br>";
	
	$mes .= "<hr>展示するのをやめますか?<br>";
	$mes .= "お店の作品一覧<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="file_name" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>ﾀｲﾄﾙ</th><th>値段</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($file, $name, $price) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="radio" name="file_name" value="$file">$name</td>|;
		$mes .= $price > 4999999 ? qq|<td align="right">非売品($price G)<br></td></tr>| : qq|<td align="right">$price G<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="展示をやめる" class="button1"></p></form>|;
	
	$m{tp} = 410;
	&n_menu;
}
sub tp_410 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($in{file_name}) {
		if (&my_goods_count($this_path_dir) >= $max_goods) {
			$mes .= "所持品がいっぱいです<br>";
			&begin;
		}
		else {
			&remove_shop_goods($in{file_name});
			&tp_400;
		}
	}
	else {
		&begin;
	}
}


#=================================================
# 展示する
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	$layout = 2;
	$mes .= "どの$goods_nameを展示に出しますか?<br>";
	$mes .= "値段を500万G以上にすることで非売品にすることができます<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p>値段：<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p><input type="submit" value="展示する" class="button1"></p></form>|;
	$m{tp} = 510;
	&n_menu;
}
sub tp_510 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	if (!$in{file_name}) {
		$mes .= "やめました<br>";
		&begin;
	}
	elsif ($in{file_name} =~ /^_/) {
		$mes .= "$non_titleの作品は展示することができません<br>";
		&begin;
	}
	elsif (-f "$this_path_dir/$in{file_name}") {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($file) = (split /<>/, $line)[0];
			&error("すでに展示されています") if $file eq $in{file_name};
			push @lines, $line;
		}
		
		if (@lines >= $max_shop_item) {
			$mes .= "これ以上お店に作品を展示することはできません<br>";
			&begin;
			return;
		}
		elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0) {
			$mes .= "値段は 1 G 以上にする必要があります<br>";
			&begin;
			return;
		}
		
		my $file_title = &get_goods_title($in{file_name});
		unshift @lines, "$in{file_name}<>$file_title<>$in{price}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		$mes .= $in{price} > 4999999 ? "$file_titleを非売品として展示しました<br>" : "$file_titleを $in{price} Gで展示しました<br>";
		&tp_500;
	}
	else {
		&begin;
	}
}

#=================================================
# お店の設定
#=================================================
sub tp_600 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error("$shop_list_file ﾌｧｲﾙが読み込めません");
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
		open my $fh3, ">> $shop_list_file" or &error("$shop_list_file ﾌｧｲﾙが開けません");
		print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
		close $fh3;
	}

	$m{tp} += 10;
	&n_menu;
}
sub tp_610 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= "やめました";
		&begin;
		return;
	}
	
	&error("お店の名前が長すぎます。全角8(半角16)文字まで") if length $in{name} > 16;
	&error("紹介文が長すぎます。全角20(半角40)文字まで") if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error("$shop_list_file ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
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
# <input type="radio" 付の自分の絵
#=================================================
sub radio_my_goods {
	my $sub_mes .= qq|<input type="radio" name="file_name" value="0" checked>やめる<hr>|;
	opendir my $dh, $this_path_dir or &error("$this_path_dir ﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<img src="$this_path_dir/$file_name" style="vertical-align:middle;" $mobile_icon_size>| if $goods_type eq 'img';
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">$file_title<hr>|;
	}
	closedir $dh;
	$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	
	return $sub_mes;
}


#=================================================
# 展示品から除く
#=================================================
sub remove_shop_goods {
	my $file_name = shift;

	return unless -f $this_file;

	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($file, $name, $price) = split /<>/, $line;
		
		if ($file_name eq $file) {
			$mes .= "$nameを展示品から除きました<br>";
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





1; # 削除不可
