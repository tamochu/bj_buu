my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
#================================================
# ©•ª‚Ìì•i‚Ì‚¨“X Created by Merino
#================================================
# ¦‚±‚ÌCGI’P‘Ì‚Å‚Í“®‚«‚Ü‚¹‚ñ shopping_akindo_book.cgi,shopping_akindo_picture.cgi‚ğQÆ

# S‘©’†‚Ìs“®—pŠÖ”
sub is_rest { return $m{lib_r} eq 'shopping_akindo_book' || $m{lib_r} eq 'shopping_akindo_picture'; } # S‘©’†‚Ìs“®‚©
sub set_tp { (&is_rest ? $m{tp_r} : $m{tp}) = shift; } # S‘©’†E”ñS‘©’†‚Ìtp¾¯À°
sub get_tp { return &is_rest ? $m{tp_r} : $m{tp}; } # S‘©’†E”ñS‘©’†‚Ì¹Ş¯À°
sub refresh_r { $m{lib_r} = $m{tp_r} = ''; } # refresh‚ÌS‘©’†”Å

# S‘©’†‚Æ“¯‚¶s“®‚ğ”ñS‘©’†‚É‚µ‚½ê‡AS‘©’†‚Ì•û‚ğ·¬İ¾Ù
&refresh_r if $m{lib_r} eq $m{lib};

#================================================
# ‚¨“X‚Ì–¼‘Oˆê——•\¦
#================================================
sub begin {
	$layout = 2;

#	$m{tp} = 1 if $m{tp} > 1;
	&set_tp(1) if &get_tp > 1;
	$mes .= "‚Ç‚Ì‚¨“X‚Å”ƒ•¨‚µ‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>“X–¼</th><th>“X’·</th><th>Ğ‰î•¶<br></th></tr>| unless $is_mobile;

	open my $fh, "< $shop_list_file" or &error("$shop_list_file Ì§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# ¤•i‚ª‚È‚¢“X‚Í”ñ•\¦
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop_$goods_dir.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="‚¨“X‚É“ü‚é" class="button1"></p></form>|;
}

#================================================
# ‚¨“X‚Ì¤•iˆê——•\¦
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
	open my $fh, "< $shop_list_file" or &error("$shop_list_file Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
	
	# ‚¨“X‚ª‘¶İ‚µ‚È‚¢
	if (!$is_find || !-f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= "$m{stock}‚Æ‚¢‚¤‚¨“X‚Í•Â“X‚µ‚Ä‚µ‚Ü‚Á‚½‚æ‚¤‚Å‚·<br>";
		&begin;
	}
	# ©•ª‚Ì‚¨“X‚Å”ƒ‚¢•¨‚Å‚«‚Ä‚µ‚Ü‚¤‚ÆA”„ã×İ·İ¸Ş‚ª•ö‰ó‚µ‚Ä‚µ‚Ü‚¤‚Ì‚ÅB
	elsif ($m{name} eq $y{name}) {
		$mes .= "©•ª‚Ì‚¨“X‚Å”ƒ‚¢•¨‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= qq|y$m{stock}z$y{name}u$shop_messagev<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="file_name" value="0" checked>‚â‚ß‚é<br>|;
		$mes .= qq|<table class="table1"><tr><th>¤•i–¼</th><th>’l’i<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$y{name}‚É“ü‚ê‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($price > 4999999) {
				$mes .= qq|<tr><td>|;
				$mes .= $goods_type eq 'img'  ? qq|<img src="$userdir/$shop_id/$goods_dir/$file" style="vertical-align:middle;">$name<br>|
					  : $goods_type eq 'html' ? qq|<a href="$userdir/$shop_id/$goods_dir/$file" target="_blank">$name</a><br>|
					  :                         qq|$name<br>|;
					  ;
				$mes .= qq|</td><td align="right">”ñ”„•i<br></td></tr>|;
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
		$mes .= qq|<p><input type="submit" value="”ƒ‚¤" class="button1"></p></form>|;
#		$m{tp} = 100;
		&set_tp(100);
	}
	else {
#		$mes .= "y$y{name}z€”õ’†<br>";
		&begin;
	}
	&n_menu;
}

#================================================
# ”ƒ‚¢•¨ˆ—
#================================================
sub tp_100 {
	my %e2j_goods = (
		picture => 'Ï²Ëß¸Á¬',
		book    => 'Ï²ÌŞ¯¸',
		music   => 'Ï²Ğ­°¼Ş¯¸',
		etc     => 'Ï²´Ä¾Ä×',
	);

	my $shop_id = unpack 'H*', $y{name};
	
	if ($in{file_name} && -f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$userdir/$shop_id/shop_$goods_dir.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($in{file_name} eq $file) {
				# Ì§²Ù‚ª‚È‚¢ê‡
				unless (-f "$userdir/$shop_id/$goods_dir/$file") {
					$is_rewrite = 1;
					next;
				}

				$is_find = 1;

				if ($m{money} >= $price) {
					$m{money} -= $price;
					
					rename "$userdir/$shop_id/$goods_dir/$file", "$userdir/$id/$goods_dir/$file" or &error("ØÈ°Ñˆ—‚É¸”s‚µ‚Ü‚µ‚½");
					if($goods_type eq 'img' || $goods_type eq 'html'){
				     		my $img_title = $name;
				     		$img_title =~ s/.*ì://;
						if($img_title ne $ y{name}){
				     			&send_money($img_title,"ˆóÅû“ü‚Æ‚µ‚Ä$m{stock}",int($price*0.1));
						}		
					}
					&send_money($y{name}, "y$m{stock}($name)z$m{name}", $price, 1);
					$is_rewrite = 1;

					$mes .= "$name‚ğ”ƒ‚¢‚Ü‚µ‚½<br>$name‚Í$e2j_goods{$goods_dir}‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
					
					# ì•i‚ª‚ ‚é‚æÌ×¸Ş‚ğ‚½‚Ä‚é
					open my $fh5, "> $userdir/$id/goods_flag.cgi";
					close $fh5;
					
					# ”„ã‹à‰ÁZ
					open my $fh2, "+< $userdir/$shop_id/shop_sale_$goods_dir.cgi" or &error("”„ãÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
					$mes .= "$y{name}u‚¨‹à‚ª‘«‚è‚Ü‚¹‚ñv<br>";
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
			$mes .= "$y{name}u‚»‚Ì¤•i‚ÍA‚½‚Á‚½¡”„‚èØ‚ê‚Ä‚µ‚Ü‚¢‚Ü‚µ‚½v<br>" ;
		}
		$cmd = $y{name}; # –¼‘O‚ğcmd‚É“ü‚ê‚Ä&tp_1
		&tp_1;
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		&begin;
	}
}


1; # íœ•s‰Â
