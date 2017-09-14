#================================================
# ｽﾛｯﾄ沼（プログレッシブジャックポット）
#================================================
#require "$datadir/casino_bonus.cgi";
# ｼﾞｬｯｸﾎﾟｯﾄの仕様変えたいので、共用されてる↑は使わないことに…
@bonus_5 = ( # 50000 / 225 * 3000 = 666666ｺｲﾝ
	[2,17,0,0],		# ﾌﾟﾘﾃｨｴｯｸﾞ
	[2,19,0,0],		# ｽｰﾊﾟｰｴｯｸﾞ
	[2,34,0,0],		# ｷｰｴｯｸﾞ
	[3,121,0,0],	# ﾎﾟｲｽﾞﾝｿﾞﾝﾋﾞ
);

@bonus_10 = ( # 100000 / 225 * 3000 = 1333333ｺｲﾝ
	[2,3,0,0],		# 夢卵
	[3,1,0,0],		# ｺﾃﾂ
	[3,14,0,0],		# ﾏﾈｷﾈｺ
	[3,124,0,0],	# ﾃﾞｽ
);

@bonus_25 = (  # 250000 / 225 * 3000 = 3333333ｺｲﾝ
	[2,2,0,0],		# ？卵
	[3,16,0,0],		# ﾋﾞｯｷｰ
	[3,17,0,0],		# ﾗﾌｧｴﾙ
	[3,18,0,0],		# ﾐｶｴﾙ
);

@bonus_50 = (  # 500000 / 225 * 3000 = 6666666ｺｲﾝ
	[2,32,0,0],		# ﾗﾌﾞﾘｰｴｯｸﾞ
	[2,38,0,0],		# ｴﾘｰﾄｴｯｸﾞ
	[2,39,0,0],		# ﾃﾞｽｴｯｸﾞ
);

@bonus_100 = (  # 500000 / 225 * 3000 = 6666666ｺｲﾝ
	[2,37,0,0],		# ｺﾞｯﾄﾞｴｯｸﾞ
	[2,41,0,0],		# ﾏｽﾀｰｴｯｸﾞ
	[2,46,0,0],		# ﾊﾞﾂｴｯｸﾞ
	[2,47,0,0],		# ｸﾗｲﾑｴｯｸﾞ
);

@bonus_200 = (  # 1000000 / 225 * 3000 = 13333333ｺｲﾝ
	[1,32,500,30],	#ｸﾛﾑﾊｰﾂ★30
	[3,168,0,0],	# ﾍﾟｲﾝﾀｰ
	[3,7,0,0],		# ﾀﾞｸﾎ
	[3,8,0,0],		# ｺﾞｰｽﾄ
);

@bonus_300 = ( # 2000000 / 225 * 3000 = 26666666ｺｲﾝ
	[2,54,0,0],		# ﾀｷｵﾝ
	[3,183,0,0],	# ﾀｸﾐ
	[3,21,0,0],		# ｶﾞﾌﾞﾘｴﾙ
);

require "./lib/_casino_funcs.cgi";

$header_size = 2; # ｽﾛｯﾄ沼用のﾍｯﾀﾞｰｻｲｽﾞ JP、強制JP
($_jp, $_ceil) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ

sub run {
	$option_form .= qq|<form method="$method" action="$this_script" name="form">|;
	$option_form .= &create_submit("view_log", "JPログ");
	$option_form .= qq|</form>|;

	&_default_run;
}

sub show_head_info { # すべてのﾌﾟﾚｲﾔｰに表示したい情報1
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	# ｶｼﾞﾉ毎の処理
	print qq|ｼﾞｬｯｸﾎﾟｯﾄ：$head[$_jp]|;
	my @bets = ('1bet', '2bet', '3bet');
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_select_menu("bet_value", $in{bet_value}, @bets);
	print &create_submit("play", "回す");
	print qq|</form>|;
}

sub play {
	my $value = $in{bet_value} + 1;

	# my $this_pool_file  = "$userdir/$id/casino_pool.cgi"; # 定義忘れ？ 定義されてなかった
	# 何の処理か分からん ｺｲﾝが 1000 しかない場合に 3 bet できてしまい、
	# 所持ｺｲﾝが -2000 になる不具合を修正したとき、それでも以下の処理が必要なのか？
	if ($m{coin} < (1000 * $value)) { # 所持ｺｲﾝが 1000 未満かどうかしか見ていなかったので、1000 ｺｲﾝあれば 3 bet 3000 ｺｲﾝ消費できた
=pod
所持ｺｲﾝが 1000 未満のとき、違法ｶｼﾞﾉを建てていて、かつﾌﾟｰﾙｺｲﾝが 1 以上ではないなら所持ｺｲﾝが 0 になる
$this_pool_file が定義されてなかったので、結局のところｺｲﾝが 1000 未満の状態で回そうとするとみんな所持ｺｲﾝが消えていた
		my $pool_find = 0;
		if (-f "$userdir/$id/casino_pool.cgi") {
			open my $fh, "< $this_pool_file" or &error("$this_pool_fileが開けません");
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				if ($pool > 0) {
					$pool_find = 1;
				}
				last;
			}
			close $fh;
		}
		unless ($pool_find) {
			$m{coin} = 0;
			&write_user;
		}
=cut
		return ('ｺｲﾝがありません');
	}
	$m{coin} -= (1000 * $value);

	my @m = ('７');
	my @m_exval = ('∞','♪','★','☆','△','▼','◆','○','●','■','▲','◎','♀','♂','〒','♭','♯'); # 17個 ,'†','¶','×'
	for my $val (@m_exval) {
		push @m, $val for (0..3); # 4個 元は 6
	}
	# 17種のﾏｰｸを4個ずつ追加 計68個のﾏｰｸの中に 7 が1つ 1/69 の確率で 7
	my @s = ();
	my $gflag = 0;
	my ($rets, $jp_log) = ('', '');
	my @prizes = ();
	$s[$_] = int(rand(@m)) for (0 .. 8);
	# 17種のﾏｰｸを4個ずつ追加 計68個のﾏｰｸの中に 7 が1つ 1/69 の確率で 7 7 が3つ出るのは 1/(69^3) = 1/250047
	# 9箇所のマスで一列揃えば当たり 1/(9^2) = 1/81 の確率で揃う（7以外は複数あるので違うはず）
	# 1/(63^3) = 1/250047 1/(9^2) = 1/81 つまりJPが出る確率は 1/20253807？
	# 2/13468869 poppo

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
	}

	# ｼﾞｬｯｸﾎﾟｯﾄにｺｲﾝ溜まりすぎないようにするための強制ｼﾞｬｯｸﾎﾟｯﾄ
	$s[0] = $s[1] = $s[2] = 0 if 2500000 < $head[$_jp] && 2500000 < $head[$_ceil] && $head[$_ceil] < $head[$_jp];

	$rets .= "<p>【$m[$s[3]]】【$m[$s[4]]】【$m[$s[5]]】</p>";
	$rets .= "<p>【$m[$s[0]]】【$m[$s[1]]】【$m[$s[2]]】</p>";
	$rets .= "<p>【$m[$s[6]]】【$m[$s[7]]】【$m[$s[8]]】</p>";

	if ($m[$s[0]] eq $m[$s[1]] && $m[$s[0]] eq $m[$s[2]]) {
		if ($s[0] != 0) { # jackpot以外
			$m{coin} += 50000;
			$rets .= "なんと!! $m[$s[0]] が3つそろいました!!ｺｲﾝ 50000 枚獲得<br>";
		}
		else {
			$rets .= "Jackpot!!!";
			$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
		}
		$gflag = 1;
	}

	if ($value >= 2) {
		if ($m[$s[3]] eq $m[$s[4]] && $m[$s[3]] eq $m[$s[5]]) {
			if ($s[3] != 0) { # jackpot以外
				$m{coin} += 50000;
				$rets .= "なんと!! $m[$s[3]] が3つそろいました!!ｺｲﾝ 50000 枚獲得<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[7]] && $m[$s[6]] eq $m[$s[8]]) {
			if ($s[6] != 0) { # jackpot以外
				$m{coin} += 50000;
				$rets .= "なんと!! $m[$s[6]] が3つそろいました!!ｺｲﾝ 50000 枚獲得<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
			}
			$gflag = 1;
		}
	}
	
	if ($value == 3) {
		if ($m[$s[3]] eq $m[$s[1]] && $m[$s[3]] eq $m[$s[8]]) {
			if ($s[3] != 0) { # jackpot以外
				$m{coin} += 50000;
				$rets .= "なんと!! $m[$s[3]] が3つそろいました!!ｺｲﾝ 50000 枚獲得<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[1]] && $m[$s[6]] eq $m[$s[5]]) {
			if ($s[6] != 0) { # jackpot以外
				$m{coin} += 50000;
				$rets .= "なんと!! $m[$s[6]] が3つそろいました!!ｺｲﾝ 50000 枚獲得<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
			}
			$gflag = 1;
		}
	}

	unless ($gflag) {
		$head[$_jp] += 50 * ($value);
		$rets .= '<p>ﾊｽﾞﾚ</p>';
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	for my $i (0 .. $#prizes) {
		my @bonus = split /<>/, $prizes[$i];
		&send_item($m{name},$bonus[0],$bonus[1],$bonus[2],$bonus[3], 1);
	}

	if ($jp_log) {
		my @logs = ();
		my $log_num = 0;
		open my $fh, "+< ${this_file}_log.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			push @logs, $line;
			$log_num++;
			last if 29 <= $log_num;
		}
		unshift @logs, "$m{name} $jp_log $date\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @logs;
		close $fh;

		&mes_and_world_news("<b>ｼﾞｬｯｸﾎﾟｯﾄを出しました</b>", 1);
	}

	&write_user;
	return ($rets);
}

sub jackpot {
	my ($ref_jp, $ref_ceil, $ref_prizes, $ref_log) = @_;
	my $prize = '';

	$$ref_log .= "jackpot:$$ref_jp my_coin:$m{coin} ";
	my $jp = 2500000 - $m{coin}; # 所持ｺｲﾝのｶﾝｽﾄを優先して余ったｺｲﾝをｱｲﾃﾑ化
	$$ref_log .= "get_coin:$jp枚 ";
	$$ref_jp = $$ref_jp - $jp;
	$m{coin} = 2500000;

	# 関数化した方が良いがちょっとなんか別に良いかなのコピペ
	if ($$ref_jp > 3000000) {
		my $item_no = int(rand($#bonus_300+1));
		push @$ref_prizes, join('<>', @{$bonus_300[$item_no]});
		if ($bonus_300[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_300[$item_no][1]][1]";
		}
		elsif ($bonus_300[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_300[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_300[$item_no][1]][1]";
		}
		$$ref_jp -= 3000000;
	}
	if ($$ref_jp > 2000000) {
		my $item_no = int(rand($#bonus_200+1));
		push @$ref_prizes, join('<>', @{$bonus_200[$item_no]});
		if ($bonus_200[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_200[$item_no][1]][1]";
		}
		elsif ($bonus_200[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_200[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_200[$item_no][1]][1]";
		}
		$$ref_jp -= 2000000;
	}
	if ($$ref_jp > 1000000) {
		my $item_no = int(rand($#bonus_100+1));
		push @$ref_prizes, join('<>', @{$bonus_100[$item_no]});
		if ($bonus_100[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_100[$item_no][1]][1]";
		}
		elsif ($bonus_100[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_100[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_100[$item_no][1]][1]";
		}
		$$ref_jp -= 1000000;
	}
	if ($$ref_jp > 500000) {
		my $item_no = int(rand($#bonus_50+1));
		push @$ref_prizes, join('<>', @{$bonus_50[$item_no]});
		if ($bonus_50[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_50[$item_no][1]][1]";
		}
		elsif ($bonus_50[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_50[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_50[$item_no][1]][1]";
		}
		$$ref_jp -= 500000;
	}
	if ($$ref_jp > 250000) {
		my $item_no = int(rand($#bonus_25+1));
		push @$ref_prizes, join('<>', @{$bonus_25[$item_no]});
		if ($bonus_25[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_25[$item_no][1]][1]";
		}
		elsif ($bonus_25[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_25[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_25[$item_no][1]][1]";
		}
		$$ref_jp -= 250000;
	}
	if ($$ref_jp > 100000) {
		my $item_no = int(rand($#bonus_10+1));
		push @$ref_prizes, join('<>', @{$bonus_10[$item_no]});
		if ($bonus_10[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_10[$item_no][1]][1]";
		}
		elsif ($bonus_10[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_10[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_10[$item_no][1]][1]";
		}
		$$ref_jp -= 100000;
	}
	if ($$ref_jp > 50000) {
		my $item_no = int(rand($#bonus_5+1));
		push @$ref_prizes, join('<>', @{$bonus_5[$item_no]});
		if ($bonus_5[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_5[$item_no][1]][1]";
		}
		elsif ($bonus_5[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_5[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_5[$item_no][1]][1]";
		}
		$$ref_jp -= 50000;
	}
=pod
	while ($$ref_jp > 2500000) {
		my $item_no = int(rand($#bonus+1));
		push @$ref_prizes, $item_no;
		if ($bonus[$item_no][0] == 1) {
			$prize .= "$weas[$bonus[$item_no][1]][1]";
		}
		elsif ($bonus[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus[$item_no][1]][1]";
		}
		$$ref_jp -= 1000000;
	}
=cut

#	$m{coin} += $$ref_jp;
#	$$ref_jp = $$ref_jp > 0 ? $$ref_jp + 2500000 : 2500000 ;
	$$ref_jp = 2500000;
	# 強制JP 当たる確率めっちゃ低くしてJP貯めさせてこれで吐かせるより、そこそこ吐かせてJP溜まらないようにした方が健全なのでは？
	# なかなかJP当たらないのにこれで吐かれると全然当たらないのに当たった人には大量リターンで不公平感強い
	$$ref_ceil = int(rand(5000000) + 2500000);
	$$ref_log .= "get_prize:$prize";
	return "ｺｲﾝ $jp 枚 $prize を獲得しました<br>";
}

sub view_log {
	open my $fh, "< ${this_file}_log.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	while (my $line = <$fh>) {
		$mes .= "$line<br>";
	}
	close $fh;
	return '';
}

1;#削除不可
