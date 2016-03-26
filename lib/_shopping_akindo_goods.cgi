my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
#================================================
# 自分の作品のお店 Created by Merino
#================================================
# ※このCGI単体では動きません shopping_akindo_book.cgi,shopping_akindo_picture.cgiを参照

#================================================
# お店の名前一覧表示
#================================================
sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "どのお店で買物しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
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
sub tp_1 {
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
		&begin;
	}
	# 自分のお店で買い物できてしまうと、売上ﾗﾝｷﾝｸﾞが崩壊してしまうので。
	elsif ($m{name} eq $y{name}) {
		$mes .= "自分のお店で買い物することはできません<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= qq|【$m{stock}】$y{name}「$shop_message」<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="file_name" value="0" checked>やめる<br>|;
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
		$m{tp} = 100;
	}
	else {
#		$mes .= "【$y{name}】準備中<br>";
		&begin;
	}
	&n_menu;
}

#================================================
# 買い物処理
#================================================
sub tp_100 {
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
		&tp_1;
	}
	else {
		$mes .= 'やめました<br>';
		&begin
	}
}


1; # 削除不可
