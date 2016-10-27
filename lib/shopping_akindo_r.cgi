#================================================
# 商人のお店 Created by Merino
#================================================
$script_r = 'bj_rest_shop.cgi';
require "$datadir/buyable.cgi";
my $this_file_a = "$logdir/auction.cgi";

my $mobile_max = 50;

sub begin {
	$layout = 2;
	
	$m{tp_r} = 1 if $m{tp_r} > 1;
	$mes .= "どのお店で買物しますか?<br>";
	
	my $count = 0;
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="total_list" checked><label for="no_0">商品一覧</label><br>|;
	$mes .= qq|<table class="table1"><tr><th>店名</th><th>店長</th><th>紹介文<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		my $gc = "#ffffff";
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name"><font color="$gc">$shop_name</font><br>|
			 : qq|<tr><td><input type="radio" id="$shop_id" name="cmd" value="$name"><font color="$gc"><label for="$shop_id">$shop_name</label></font></td><td>$name</td><td>$message<br></td></tr>|;
		$count++;
	}
	close $fh;

	$m{stock} = $count;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に入る" class="button1"></p></form>|;
	$mes .= qq|<br><form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="やめる" class="button1"></p></form>|;
	
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="cmd" value="shop_auction">|;
	$mes .= qq|<p><input type="submit" value="ｵｰｸｼｮﾝ会場" class="button1"></p></form>|;
	
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="cmd" value="shop_book">|;
	$mes .= qq|<p><input type="submit" value="ﾌﾞｯｸﾏｰｹｯﾄ" class="button1"></p></form>|;
	
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="cmd" value="shop_picture">|;
	$mes .= qq|<p><input type="submit" value="美の画伯館" class="button1"></p></form>|;
}

#================================================
# お店の商品一覧表示
#================================================
sub tp_1 {
	$layout = 2;
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	if ($cmd eq 'total_list') {
		$m{tp_r} = $is_mobile ? 300:200;
		if($is_smart){
			$mes .= qq|<table boder=0 cols=3 width=90 height=90><tr>|;
			$mes .= qq|<td><form method="$method" action="$script_r">|;
			$mes .= qq|<input type="submit" value="上限なし" class="button1s"><input type="hidden" name="cmd" value="0">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|</td>|;
			$mes .= qq|<td><form method="$method" action="$script_r">|;
			$mes .= qq|<input type="submit" value="所持金以下" class="button1s"><input type="hidden" name="cmd" value="1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|</td>|;
			$mes .= qq|</tr>|;
			$mes .= qq|</table>|;
		}else{
			$mes  = qq|<form method="$method" action="$script_r"><select name="cmd" class="menu1">|;
			$mes .= qq|<option value="0">上限なし</option>|;
			$mes .= qq|<option value="1">所持金以下</option>| unless $is_mobile;
			$mes .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= $is_mobile ? qq|<br><input type="submit" value="決 定" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="決 定" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
		}
		return;
	}
	if ($cmd eq 'shop_auction') {
		$m{tp_r} = 400;
		&{ 'tp_'. $m{tp_r} };
		return;
	} elsif ($cmd eq 'shop_book') {
		$m{tp_r} = 500;
		&{ 'tp_'. $m{tp_r} };
		return;
	} elsif ($cmd eq 'shop_picture') {
		$m{tp_r} = 600;
		&{ 'tp_'. $m{tp_r} };
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが開けません');
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
	if (!$is_find || !-f "$userdir/$shop_id/shop.cgi") {
		$mes .= "$m{stock}というお店は閉店してしまったようです<br>";
		&begin;
	}
	# 自分のお店で買い物できてしまうと、売上ﾗﾝｷﾝｸﾞが崩壊してしまうので。
	elsif ($m{name} eq $y{name}) {
		$mes .= "自分のお店で買い物することはできません<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop.cgi") {
		$mes .= qq|【$m{stock}】$y{name}「$shop_message」<br>|;
		$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
		$mes .= qq|<table class="table1"><tr><th>商品名</th><th>値段<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}に入れません");
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			next if ($price == 5000000);
			$mes .= qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no">|;
			$mes .= qq|<label for="$no">| unless $is_mobile;
			$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # 種類非表示
			$mes .= qq|</label>| unless $is_mobile;
			$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="買う" class="button1"></p></form>|;
		$m{tp_r} = 100;
	}
	else {
#		$mes .= "【$cmd】準備中<br>";
		&begin;
	}
}

#================================================
# 買い物処理
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $line = ''; # 買ったアイテム情報が入る
		my @lines = (); # その他の商品が入る
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("商品ﾘｽﾄが開けません");
		eval { flock $fh, 2; };
		while (my $_line = <$fh>) {
			if (index($_line, "$cmd<>") == 0) { $line = $_line; }
			else { push @lines, $_line; }
		}
		if ($line) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			if ($m{money} >= $price) {
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
			}
			close $fh;
			if ($m{money} >= $price) {
				$m{money} -= $price;
				my $item_name = &get_item_name($kind, $item_no);
				$mes .= "$item_nameを買いました<br>$item_nameは預かり所に送られました<br>";
				my $sell_id = int(rand(1000)+1); # 鯖缶権限で見れる取引ID？ send_item では爆発無視フラグとしか使われてない
				&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, $sell_id);
				&send_money($y{name}, "【$m{stock}($item_name)】$m{name}", $price, 1);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $price, 1);

				# 売上金加算
				open my $fh2, "+< $userdir/$shop_id/shop_sale.cgi" or &error("売上ﾌｧｲﾙが開けません");
				eval { flock $fh2, 2; };
				my $line2 = <$fh2>;
				my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
				$sale_c++;
				$sale_money += $price;
				seek  $fh2, 0, 0;
				truncate $fh2, 0;
				print $fh2 "$sale_c<>$sale_money<>$update_t<>";
				close $fh2;

				# 売上内訳
				if(-f "$userdir/$shop_id/shop_sale_detail.cgi"){
					my @sell_detail = ();
					open my $fh3, "+< $userdir/$shop_id/shop_sale_detail.cgi" or &error("帳簿ﾌｧｲﾙが開けません");
					eval { flock $fh3, 2; };
					while (my $line3 = <$fh3>){
						last if @sell_detail >= 30;
						push @sell_detail, $line3;
					}
					unshift @sell_detail, "$item_name<>$m{name}<>$time<>\n" if $sell_id; # true にしかならない
					seek  $fh3, 0, 0;
					truncate $fh3, 0;
					print $fh3 @sell_detail;
					close $fh3;
				}else{
					open my $fh3, "> $userdir/$shop_id/shop_sale_detail.cgi" or &error("帳簿ﾌｧｲﾙが開けません");
					print $fh3 "$item_name<>$m{name}<>$time<>\n" if $sell_id; # true にしかならない
					close $fh3;
				}

				# send_itemのロギング機能してない あっちのが総括的なのでそのうち移動
				# ショッピングをロギング
				open my $fh4, ">> $logdir/shopping_log.cgi";
				print $fh4 "$m{name}<>$y{name}<>$item_name<>$price<>$time\n";
				close $fh4;
			}
			else {
				$mes .= "$y{name}「お金が足りません」<br>";
			}
		}
		else {
			$mes .= "$y{name}「その商品は、たった今売り切れてしまいました」<br>" ;
			close $fh;
		}

		$cmd = $y{name}; # 名前をcmdに入れて&tp_1
		&tp_1;
	}
	else {
		$mes .= 'やめました<br>';
		&begin
	}
=pod
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("商品ﾘｽﾄが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$is_find = 1;

				if ($m{money} >= $price && &is_buyable($kind, $item_no)) {
					$m{money} -= $price;
					
					my $item_name = &get_item_name($kind, $item_no); # アイテム名のみ
					$mes .= "$item_nameを買いました<br>$item_nameは預かり所に送られました<br>";
					my $sell_id = int(rand(1000)+1);
					
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, $sell_id);
					&send_money($y{name}, "【$m{stock}($item_name)】$m{name}", $price, 1);
					&sale_data_log($kind, $item_no, $item_c, $item_lv, $price, 1);
					$is_rewrite = 1;

					# ショッピングをロギング
					my $ltime = time();
					open my $fh, ">> $logdir/shopping_log.cgi";
					print $fh "$m{name}<>$y{name}<>$item_name<>$price<>$ltime\n";
					close $fh;

					# 売上金加算
					open my $fh2, "+< $userdir/$shop_id/shop_sale.cgi" or &error("売上ﾌｧｲﾙが開けません");
					eval { flock $fh2, 2; };
					my $line2 = <$fh2>;
					my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
					$sale_c++;
					$sale_money += $price;
					seek  $fh2, 0, 0;
					truncate $fh2, 0;
					print $fh2 "$sale_c<>$sale_money<>$update_t<>";
					close $fh2;
					
					# 売上内訳
					if(-f "$userdir/$shop_id/shop_sale_detail.cgi"){
						open my $fh3, "+< $userdir/$shop_id/shop_sale_detail.cgi" or &error("帳簿ﾌｧｲﾙが開けません");
						while (my $line3 = <$fh3>){
							last if @sell_detail >= 30;
							push @sell_detail, $line3;
						}
						unshift @sell_detail, "$item_name<>$m{name}<>$time<>\n" if $sell_id;
						seek  $fh3, 0, 0;
						truncate $fh3, 0;
						print $fh3 @sell_detail;
						close $fh3;
					}else{
						open my $fh3, "> $userdir/$shop_id/shop_sale_detail.cgi" or &error("帳簿ﾌｧｲﾙが開けません");
						print $fh3 "$item_name<>$m{name}<>$time<>\n" if $sell_id;
						close $fh3;
					}
				}
				else {
					$mes .= "$y{name}「お金が足りません」<br>";
					last;
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
		
		unless ($is_find) {
			$mes .= "$y{name}「その商品は、たった今売り切れてしまいました」<br>" ;
		}
		$cmd = $y{name}; # 名前をcmdに入れて&tp_1
		&tp_1;
	}
	else {
		$mes .= 'やめました<br>';
		&begin
	}
=cut
}


#================================================
# 一覧表示
#================================================

sub tp_200 {
	$layout = 2;

	$m{tp_r} = 1 if $m{tp_r} > 1;

	my @item_list = ();
	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		next if ($display ne '1' && $in{d_flag} ne '1');

		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_nameの商品が読み込めません");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				next if (($cmd eq '1' && $price > $m{money}) || $price == 5000000);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>$display<>$guild_number<>\n";
			}
			close $ifh;
		}
	}
	close $fh;
	
	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;
	
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
	$mes .= qq|<table class="table1"><tr><th>商品名</th><th>店主</th><th>価格<br></th></tr>|;
	my $b_name = -1;
	my $b_kind = -1;
	my $b_item_no = -1;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name, $display, $guild_number) = split /<>/, $line;
		if($name eq $b_name && $kind == $b_kind && $item_no == $b_item_no){
			next;
		}
		my $gc = "#ffffff";
		$mes .= qq|<tr><td><input type="radio" id="$name$item_no" name="cmd" value="$name">|;
		$mes .= qq|<label for="$name$item_no">| unless $is_mobile;
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # 種類非表示
		$price = '非表示' if $price == 99999999;
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|</td><td><font color="$gc">$name</font></td><td>$price<br></td></tr>|;
		$b_name = $name;
		$b_kind = $kind;
		$b_item_no = $item_no;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に入る" class="button1"></p></form>|;
}


sub tp_300 {#mobile

	$layout = 2;
	$m{tp_r} = 310;
	my $num = 0;
	my @item_list = ();
	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display) = split /<>/, $line;
		
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_nameの商品が読み込めません");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				next if ($price == 5000000);
				$price = 99999999 if $display ne '1';
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>\n";
			}
			close $ifh;
		}
	}
	close $fh;

	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;
	
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>商品名</th><th>店主</th><th>価格<br></th></tr>|;
	my $b_name = -1;
	my $b_kind = -1;
	my $b_item_no = -1;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name, $display) = split /<>/, $line;
		if($name eq $b_name && $kind == $b_kind && $item_no == $b_item_no){
			next;
		}
		$num++;
		if ($num >= $cmd * $mobile_max && $num < ($cmd + 1) * $mobile_max){
			$mes .= qq|<tr><td><input type="radio" name="cmd" value="$name">|;
			$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # 種類非表示
			$price = '非表示' if $price == 99999999;
			$mes .= qq|</td><td>$name</td><td>$price<br></td></tr>|;
		}
		$b_name = $name;
		$b_kind = $kind;
		$b_item_no = $item_no;
	}
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に入る" class="button1"></p></form><br>|;

	$mes  .= qq|<form method="$method" action="$script_r"><select name="cmd" class="menu1">|;
	$pre = $cmd-1;
	$nex = $cmd+1;
	$mes .= qq|<option value="$pre">前へ</option>|;
	$mes .= qq|<option value="$nex">次へ</option>|;
	$mes .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="mode" value="list">|;
	$mes .= qq|<br><input type="submit" value="決 定" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}

sub tp_310 {
    if($in{mode} eq 'list'){
    		 &tp_300;
    }else {
    	  $m{tp_r} = 1;
    	  &tp_1;
    }
}

#================================================
# ｵｰｸｼｮﾝ
#================================================

sub tp_400 {
	# 落札時間(日)
	my $auction_limit_day = 3;

	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方はお断りしています<br>";
		&begin;
		return;
	}
	
	$layout = 1;
	
	$mes .= qq|ｵｰｸｼｮﾝの落札日数は、出品日から $auction_limit_day日前後です<br>|;
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
 	$mes .= $is_mobile ? qq|<hr>落札品/入札額/入札者/出品者/最低入札額<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>落札品</th><th>入札額</th><th>即決額</th><th>入札者</th><th>出品者</th><th>状態</th><th>最低入札額<br></th>|;

	open my $fh, "< $this_file_a" or &error("$this_file_aが読み込めません");
	$m{total_auction} = 0;
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
		my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
		my $item_state = $time + 3600 * 24 > $bit_time ? "そろそろ":
						$time + ($auction_limit_day - 1) * 3600 * 24 > $bit_time ? "まだまだ":"new";
		unless($buyout_price){
			$buyout_price = 'なし';
		}
		my $next_min_price = int($item_price * 1.2);
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/即$buyout_price G/$to_name/$from_name/$item_state/$next_min_price<br>|
			: qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no"><label for="$no">$item_title</label></td><td align="right">$item_price G</td><td align="right">$buyout_price G</td><td>$to_name</td><td>$from_name</td><td>$item_state</td><td>$next_min_price<br></td></tr>|;
		$m{total_auction} += $item_price if($to_name eq $m{name} && $from_name ne $m{name});
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>入札金額：<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="入札する" class="button1"></p></form>|;
	
	$m{tp_r} += 10;
}

sub tp_410 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money} + $m{total_auction}) {
		$mes .= 'そんなにお金を持っていません<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my $is_sokketsu = 0;
		my @lines = ();
		open my $fh, "+< $this_file_a" or &error("$this_file_aが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
			next unless $item_no; # どういう経緯で起きたのか分からんがデータなしが落札されたので弾く
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ($buyout_price && $need_money > $buyout_price) {
					$need_money = $buyout_price;
				}
				if ( $in{money} >= $need_money && &is_buyable($kind, $item_no) ) {
					my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
					
					$m{total_auction} += $in{money};
					$mes .= "$item_titleに $in{money} Gで入札しました<br>";
					if($buyout_price && $in{money} >= $buyout_price){
						my $to_id = unpack 'H*', $m{name};
						if(-e "$userdir/$to_id/user.cgi"){
							&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, 1);
						}
						&send_money($m{name}, 'ｵｰｸｼｮﾝ会場', "-$in{money}");
						&send_money($from_name, 'ｵｰｸｼｮﾝ会場', $in{money});
						&sale_data_log($kind, $item_no, $item_c, $item_lv, $in{money}, 3);
						$mes .= "即決価格を提示しました<br>";
						&write_send_news("$from_nameの出品した$item_titleを$m{name}が $in{money} G(即決)で落札しました");
						&send_twitter("$from_nameの出品した$item_titleを$m{name}が $in{money} G(即決)で落札しました");
						$is_sokketsu = 1;
						$is_rewrite = 1;
					}else{
						$line = "$bit_time<>$no<>$kind<>$item_no<>$item_c<>$item_lv<>$from_name<>$m{name}<>$in{money}<>$buyout_price<>\n";
						$is_rewrite = 1;
					}
				}
				else {
					$mes .= "入札は現在の落札額の1.2倍以上の金額( $need_money G)が必要です<br>";
				}
				unless($is_sokketsu){
					push @lines, $line;
				}
			}
			# 落札処理
			elsif ($time > $bit_time) {
				my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
				
				my $to_id = unpack 'H*', $to_name;
				if(-e "$userdir/$to_id/user.cgi"){
					&send_item($to_name, $kind, $item_no, $item_c, $item_lv, 1);
				}
				&send_money($to_name, 'ｵｰｸｼｮﾝ会場', "-$item_price");
				&send_money($from_name, 'ｵｰｸｼｮﾝ会場', $item_price);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $item_price, 2);
				&write_send_news("$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました");
				&send_twitter("$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました");
				$is_rewrite = 1;
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
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

sub is_buyable{
	my ($kind, $item_no) = @_;
	return 1;
	if($m{is_full}){
		if($kind eq '1'){
			for my $i (@full_buyable_wea){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}elsif($kind eq '2'){
			for my $i (@full_buyable_egg){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}else{
			for my $i (@full_buyable_pet){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}
	}
	return 1;
}


#================================================
# お店の名前一覧表示
#================================================
sub begin_goods {
	my($goods_dir, $goods_type, $goods_name) = @_;
	$layout = 2;
	my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
	
	$m{tp_r} = int($m{tp_r} / 100) * 100 + 1 if $m{tp_r} > 1;
	$mes .= "どのお店で買物しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" name="cmd" value="" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>店名</th><th>店長</th><th>紹介文<br></th></tr>| unless $is_mobile;

	open my $fh, "< $shop_list_file" or &error("$shop_list_file ﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop_$goods_dir.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に入る" class="button1"></p></form>|;
}

#================================================
# お店の商品一覧表示
#================================================
sub disp_goods {
	my($goods_dir, $goods_type, $goods_name) = @_;
	my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find    = 0;
	open my $fh, "< $shop_list_file" or &error("$shop_list_file ﾌｧｲﾙが開けません");
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
	if (!$is_find || !-f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= "$m{stock}というお店は閉店してしまったようです<br>";
		&begin_goods($goods_dir, $goods_type, $goods_name);
	}
	# 自分のお店で買い物できてしまうと、売上ﾗﾝｷﾝｸﾞが崩壊してしまうので。
	elsif ($m{name} eq $y{name}) {
		$mes .= "自分のお店で買い物することはできません<br>";
		&begin_goods($goods_dir, $goods_type, $goods_name);
	}
	elsif (-s "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= qq|【$m{stock}】$y{name}「$shop_message」<br>|;
		$mes .= qq|<form method="$method" action="$script_r"><input type="radio" name="file_name" value="0" checked>やめる<br>|;
		$mes .= qq|<table class="table1"><tr><th>商品名</th><th>値段<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$y{name}に入れません");
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($price > 4999999) {
				$mes .= qq|<tr><td>|;
				$mes .= $goods_type eq 'img'  ? qq|<img src="$userdir/$shop_id/$goods_dir/$file" style="vertical-align:middle;">$name<br>|
					  : $goods_type eq 'html' ? qq|<a href="$userdir/$shop_id/$goods_dir/$file" target="_blank">$name</a><br>|
					  :                         qq|$name<br>|;
					  ;
				$mes .= qq|</td><td align="right">非売品<br></td></tr>|;
			}
			else {
				$mes .= qq|<tr><td><input type="radio" name="file_name" value="$file">|;
				$mes .= $goods_type eq 'img' ? qq|<img src="$userdir/$shop_id/$goods_dir/$file" style="vertical-align:middle;">$name<br>|
					  :                        qq|$name<br>|;
					  ;
				$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
			}
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="買う" class="button1"></p></form>|;
		$m{tp_r} = int($m{tp_r} / 100) * 100 + 10;
	}
	else {
#		$mes .= "【$y{name}】準備中<br>";
		&begin_goods($goods_dir, $goods_type, $goods_name);
	}
	&n_menu;
}

#================================================
# 買い物処理
#================================================
sub buy_goods {
	my($goods_dir, $goods_type, $goods_name) = @_;
	my %e2j_goods = (
		picture => 'ﾏｲﾋﾟｸﾁｬ',
		book    => 'ﾏｲﾌﾞｯｸ',
		music   => 'ﾏｲﾐｭｰｼﾞｯｸ',
		etc     => 'ﾏｲｴﾄｾﾄﾗ',
	);

	my $shop_id = unpack 'H*', $y{name};
	
	if ($in{file_name} && -f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$userdir/$shop_id/shop_$goods_dir.cgi ﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($in{file_name} eq $file) {
				# ﾌｧｲﾙがない場合
				unless (-f "$userdir/$shop_id/$goods_dir/$file") {
					$is_rewrite = 1;
					next;
				}

				$is_find = 1;

				if ($m{money} >= $price) {
					$m{money} -= $price;
					
					rename "$userdir/$shop_id/$goods_dir/$file", "$userdir/$id/$goods_dir/$file" or &error("ﾘﾈｰﾑ処理に失敗しました");
					if($goods_type eq 'img' || $goods_type eq 'html'){
				     		my $img_title = $name;
				     		$img_title =~ s/.*作://;
						if($img_title ne $ y{name}){
				     			&send_money($img_title,"印税収入として$m{stock}",int($price*0.1));
						}		
					}
					&send_money($y{name}, "【$m{stock}($name)】$m{name}", $price, 1);
					$is_rewrite = 1;

					$mes .= "$nameを買いました<br>$nameは$e2j_goods{$goods_dir}に送られました<br>";
					
					# 作品があるよﾌﾗｸﾞをたてる
					open my $fh5, "> $userdir/$id/goods_flag.cgi";
					close $fh5;
					
					# 売上金加算
					open my $fh2, "+< $userdir/$shop_id/shop_sale_$goods_dir.cgi" or &error("売上ﾌｧｲﾙが開けません");
					eval { flock $fh2, 2; };
					my $line2 = <$fh2>;
					my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
					$sale_c++;
					$sale_money += $price;
					seek  $fh2, 0, 0;
					truncate $fh2, 0;
					print $fh2 "$sale_c<>$sale_money<>$update_t<>";
					close $fh2;
				}
				else {
					$mes .= "$y{name}「お金が足りません」<br>";
					last;
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
		
		unless ($is_find) {
			$mes .= "$y{name}「その商品は、たった今売り切れてしまいました」<br>" ;
		}
		$cmd = $y{name}; # 名前をcmdに入れて&tp_1
		&disp_goods($goods_dir, $goods_type, $goods_name);
	}
	else {
		$mes .= 'やめました<br>';
		&begin_goods($goods_dir, $goods_type, $goods_name);
	}
}

sub tp_500 {
	&begin_goods('book', 'html', '本');
}

sub tp_501 {
	&disp_goods('book', 'html', '本');
}

sub tp_510 {
	&buy_goods('book', 'html', '本');
}

sub tp_600 {
	&begin_goods('picture', 'img', '絵');
}

sub tp_601 {
	&disp_goods('picture', 'img', '絵');
}

sub tp_610 {
	&buy_goods('picture', 'img', '絵');
}

1; # 削除不可
