#================================================
# ｽﾛｯﾄ沼（プログレッシブジャックポット）
#================================================
require "$datadir/casino_bonus.cgi";
require "./lib/_casino_funcs.cgi";

$header_size = 2; # ｽﾛｯﾄ沼用のﾍｯﾀﾞｰｻｲｽﾞ JP、強制JP
($_jp, $_ceil) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ

sub run {

	&_default_run;
}

sub show_head_info { # すべてのﾌﾟﾚｲﾔｰに表示したい情報1
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	# ｶｼﾞﾉ毎の処理
	print qq|ｼﾞｬｯｸﾎﾟｯﾄ：$head[$_jp]|;
	my @bets = ('1bet', '2bet', '3bet');
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("play", "回す");
	print &create_select_menu("bet_value", $in{bet_value}, @bets);
	print qq|</form>|;
}

sub play {
	return unless $m{name} eq 'VIPPER' || $m{name} eq 'nanamie';
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
	my @m_exval = ('∞','♪','†','★','☆','△','▼','◆','○','●','×','■','¶','▲','◎','♀','♂','〒','♭','♯'); # 20個
	for my $val (@m_exval){
		push @m, $val for (0..5); # 6個
	}
	# 20個のﾏｰｸを6個ずつ追加 120個のﾏｰｸの中に 7 が1つ 1/121 の確率で 7
	my @s = ();
	my $gflag = 0;
	my $rets = '';
	my @prizes = ();
	$s[$_] = int(rand(@m)) for (0 .. 8);

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
	$s[0] = $s[1] = $s[2] = 0 if $head[$_jp] > $head[$_ceil];

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
			$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
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

	&send_item($m{name},$bonus[$prizes[$_]][0],$bonus[$prizes[$_]][1],$bonus[$prizes[$_]][2],$bonus[$prizes[$_]][3], 1) for (0 .. $#prizes);

	&write_user;
	return ($rets);
}

sub jackpot {
	my ($ref_jp, $ref_ceil, $ref_prizes) = @_;
	my $prize = '';

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

#	&mes_and_world_news("<b>ｼﾞｬｯｸﾎﾟｯﾄを出しました</b>", 1);

	$m{coin} += $$ref_jp;
	$$ref_jp = 3000000;
	$$ref_ceil = int(rand(100000000) + 3000000);
	return "ｺｲﾝ $jp 枚 $prize を獲得しました<br>";
}

1;#削除不可
