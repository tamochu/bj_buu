$this_vote_file = "$logdir/pop_vote.cgi";
$this_vote2_file = "$logdir/pop_vote2.cgi";
$this_lot_file = "$logdir/event_lot.cgi";
$this_lot_name_file = "$logdir/event_lot_name.cgi";
$this_horror_story_file = "$logdir/horror_story.cgi";
$this_blog_vote_file = "$logdir/blog_vote.cgi";
$this_blog_vote_result_file = "$logdir/blog_vote_result.cgi";
$this_radio_dir = "$logdir/summer_radio";
#================================================
# 夏祭り
#=================================================
# 夜店
@shop_list = (
#    cmd, 商品, 金額
	[1, '食べ物', 100000],
);

# 夜店で買えるもの
@shop_items = (
		#種類,  番号, 耐久値など, ★, 確率
	[
		[2,1,0,0,50],
		[2,50,0,0,50],
		[3,23,0,0,10],
		[3,24,0,0,10],
		[3,65,0,0,10],
		[3,67,0,0,10],
		[3,76,0,0,5],
		[3,87,0,0,10],
		[3,99,0,0,10],
		[3,104,0,0,10],
		[3,169,0,0,10],
		[3,171,0,0,10],
	],
);

# 宝くじの値段
my $lot_money = 1000;

# 武器賞の賞品
my $wea_no = 33;

# ﾀﾏｺﾞ賞の賞品
my $egg_no = 54;

# 日記大賞称号
my $nikki_shogo = '★ｴﾆｯｷﾏｽﾀｰ';

my @morning_glory_height = (
	# [0]高さ,	[1]状態
	[10000, 'え、どこまで伸びるのこれ？'],
	[300, '花が咲いた。やった！'],
	[100, '蔓が伸びてきた'],
	[50, '葉が出てきた'],
	[20, '芽が出てきた'],
);

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if (&on_summer) {
		return 1;
	}
	else {
		$mes .= '楽しいはずの夏休みは終わったんだね…<br>';
		&refresh;
		&n_menu;
		return 0;
	}
}
#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他にどこ行こうか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '夏祭り会場はこっちだよ<br>';
		$mes .= '何をしようか?<br>';
	}
	
	&menu('やめる','人気投票（銀）', '夜店', 'サマージャンボ宝くじ', 'ラヂオ体操', '日記を書く', '肝試し', '百物語', '朝顔育成', '人気投票（金）');
}

sub tp_1 {
	return if &is_ng_cmd(1..9);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "投票権:$m{pop_vote}票所有";
		$mes .= "投票権がある分だけ投票できるよ!<br>投票権はいろんなとこからもらえるよ!<br>";
		&menu('やめる','投票');
	}
	elsif ($cmd eq '2') {
		$mes .= "こんなところに夜店があるね!何か買ってかない?<br>";
		&menu('やめる', '買う');
	}
	elsif ($cmd eq '3') {
		$mes .= 'いつもより豪華な宝くじだね!<br>必ず一人は当選するらしいよ!<br>';
		if (-f "$this_lot_name_file") {
			my @my_num = ();
			my $lot_amount = 0;
			open my $fh, "< $this_lot_name_file" or &error('サマージャンボファイルが開けません');
			while (my $line = <$fh>) {
				my($name, $lot_num) = split /<>/, $line;

				if ($name eq $m{name}) {
					$lot_amount++;
					if (@my_num < 5) {
						push @my_num, $lot_num;
					}
				}
			}
			close $fh;
			if ($lot_amount) {
				$mes .= join ",", @my_num;
				if ($lot_amount >= 5) {
					$mes .= '他';
				}
				$mes .= '計' . $lot_amount . '枚買っているよ';
			}
		}
		&menu('やめる', '買う');
	}
	elsif ($cmd eq '4') {
		$mes .= '毎朝6時になるとラジオ体操やってるらしいよ!<br>スタンプ集めよう!<br>';
		$mes .= "スタンプ：<br>";
		$mes .= qq|<table class="table2">|;
		$mes .= qq|<tr>|;
		for my $d (1..31) {
			$mes .= qq|<td>|;
			$mes .= qq|$d日:|;
			if (-f "$this_radio_dir/$d.cgi") {
				open my $fh, "< $this_radio_dir/$d.cgi" or &error('ラジオ体操ファイルが開けません');
				while (my $line = <$fh>) {
					my($name, $rtime) = split /<>/, $line;

					if ($name eq $m{name}) {
						$mes .= qq|○|;
					}
				}
				close $fh;
			}
			$mes .= qq|</td>|;
			if ($d % 7 == 0) {
				$mes .= qq|</tr><tr>|;
			}
		}
		$mes .= qq|</tr>|;
		$mes .= qq|</table>|;
		&menu('やめる', '体操する');
	}
	elsif ($cmd eq '5') {
		$mes .= '今日の思い出を日記に残そう!<br>';
		if ($m{summer_blog}) {
			$mes .= "書いた日数：$m{summer_blog}日分<br>";
		}
		&menu('やめる', '書く');
	}
	elsif ($cmd eq '6') {
		$mes .= '草木も眠る丑三つ時、肝試しに出かけよう<br>';
		&menu('やめる', '行く');
	}
	elsif ($cmd eq '7') {
		$mes .= '草木も眠る丑三つ時、みんなで怖い話をしよう<br>';
		&menu('やめる', 'やる');
	}
	elsif ($cmd eq '8') {
		$mes .= '朝顔を育てよう!<br>';
		&menu('やめる', 'やる');
	}
	elsif ($cmd eq '9') {
		$mes .= '一人一票の人気投票!<br>';
		&menu('やめる', '投票する');
	}
	else {
		&begin;
	}
}

#=================================================
# 人気投票
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{pop_vote} > 0) {
		$mes .= '誰に投票しようか?<br>';
		$mes .= qq|<form method="$method" action="$script"><p>投票相手：<input type="text" name="vote_name" class="text_box1"></p>|;
		$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1" checked>投票する<br>|;
		$mes .= qq|<input type="text" name="num" value="1" class="text_box1"/>票<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="投票" class="button1"></p></form>|;
		$m{tp} += 10;
	} else {
		$mes .= '投票権がないよ…<br>';
		&begin;
	}
}

sub tp_110 {
	return if &is_ng_cmd(1);
	if ($in{vote_name} eq '') {
		$mes .= '投票先が記入されてないよ<br>';
		&begin;
		return;
	}
	if ($in{vote_name} eq $m{name}) {
		$mes .= '自分には投票できないよ<br>';
		&begin;
		return;
	}
	
	my $vote_id = unpack 'H*', $in{vote_name};
	my $vote_num = $m{pop_vote} < $in{num} ? $m{pop_vote} : $in{num};

	if (-f "$userdir/$vote_id/user.cgi") {
		my @lines = ();
		my $is_find = 0;
		open my $fh, "+< $this_vote_file" or &error('人気投票ファイルが開けません');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($name, $vote) = split /<>/, $line;

			if ($name eq $in{vote_name}) {
				$vote += $vote_num;
				$is_find = 1;
			}

			push @lines, "$name<>$vote<>\n";
		}
		unless ($is_find) {
			push @lines, "$in{vote_name}<>$vote_num<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$m{pop_vote} -= $vote_num;
		$mes .= "$in{vote_name} さんに $vote_num 票入れたｗｗｗｗｗ<br>";
		&refresh;
		&n_menu;
	} else {
		$mes .= '誰それ?<br>';
		&begin;
		return;
	}
}



#=================================================
# 夜店
#=================================================
sub tp_200 {
	$layout = 1;
	$mes .= '何買おっか？<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
 	$mes .= $is_mobile ? qq|<hr>商品/金額<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>商品</th><th>金額<br></th>|;

	for my $shop_ref (@shop_list) {
		my @shop = @$shop_ref;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$shop[0]">$shop[1]/$shop[2] G<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$shop[0]">$shop[1]</td><td align="right">$shop[2] G<br></td></tr>|;
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="買う" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_210 {
	if ($cmd) {
		$index = 1;
		for my $items_arr (@shop_items) {
			if ($index == $cmd) {
				my @items = @$items_arr;
				my $max_par = 0;
				for $item_ref (@items) {
					my @item = @$item_ref;
					$max_par += $item[4];
				}
				$r_par = int(rand($max_par)) + 1;
				my $par = 0;
				for $item_ref (@items) {
					my @item = @$item_ref;
					$par += $item[4];
					if ($par >= $r_par) {
						my $money = $shop_list[$cmd-1][2];
						if ($m{money} >= $money) {
							$m{money} -= $money;
							$mes .= $item[0] eq '1' ? "$weas[$item[1]][1]"
								  : $item[0] eq '2' ? "$eggs[$item[1]][1]"
								  : $item[0] eq '3' ? "$pets[$item[1]][1]"
								  : 				  "$guas[$item[1]][1]"
								  ;
							$mes .= 'を買ったよ!';
							&send_item($m{name}, $item[0],$item[1],$item[2],$item[3],1);
							my $v = int(rand(100) + 1);
							$m{pop_vote} += $v;
							$mes .= "投票権を$v枚もらったよ";
						}
						last;
					}
				}
			}
			$index++;
		}
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}
#=================================================
# サマージャンボ宝くじ
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1);
	
	if ($m{money} >= $lot_money) {
		unless(-f "$this_lot_file"){
			open my $fh, "> $this_lot_file" or &error('宝くじﾌｧｲﾙが読み込めません');
			close $fh;
		}
		open my $fh, "+< $this_lot_file" or &error('宝くじﾌｧｲﾙが読み込めません');
		eval { flock $fh, 2 };
		$line = <$fh>;
		my($max_lot) = split /<>/, $line;
		$max_lot++;
		push @lines, "$max_lot<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		my $lot_num = sprintf("%06d", $max_lot);
		open my $fhn, ">> $this_lot_name_file" or &error('宝くじﾌｧｲﾙが読み込めません');
		print $fhn "$m{name}<>$lot_num<>\n";
		close $fhn;
		
		$m{money} -= $lot_money;
		if (rand(2) < 1) {
			$m{pop_vote}++;
			$mes .= "投票権をもらったよ";
		}
		$mes .= "当たるといいね!<br>";
	}
	else {
		$mes .= "お金が足りない…<br>";
	}
	&begin;
}

#=================================================
# ラジオ体操
#=================================================
sub tp_400 {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($hour eq '6') {
		if ($m{radio_time} + 23 * 3600 < $time) {
			mkdir "$this_radio_dir" or &error("$this_radio_dir ﾌｫﾙﾀﾞが作れませんでした") unless -d "$this_radio_dir";
			$mes .= '運動したよ、はぁいい汗かいたね!';
			open my $fh, ">> $this_radio_dir/$mday.cgi" or &error('ラジオ体操ﾌｧｲﾙが読み込めません');
			print $fh "$m{name}<>$time<>\n";
			close $fh;
			$m{radio_time} = $time;
			$m{act} = 0;
			my $v = int(rand(100) + 1);
			$m{pop_vote} += $v;
			$mes .= "投票権を$v枚もらったよ";
		} else {
			$mes .= '今日はもうスタンプ貰ったよ';
		}
	} else {
		$mes .= 'ラジオ体操は朝6時の間しかできないみたい…<br>';
	}
	&begin;
}

#=================================================
# 絵日記
#=================================================
sub tp_500 {
	$layout = 2;
	if (&time_to_date($time) ne &time_to_date($m{blog_time})) {
		$mes .= qq|今日の思い出を日記に残そう!<br>|;
		$mes .= qq|<form method="$method" action="blog.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="日記" class="button1"></form>|;
	} else {
		$mes .= '今日の日記はもう書いたよ!<br>';
	}
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($wday eq '0') {
		$mes .= qq|今週の日記大賞を決めよう!<br>|;

		my $index = 0;
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $user_id = readdir $dh) {
			next if $user_id =~ /\./;
			
			if (-f "$userdir/$user_id/blog.cgi") {
				open my $fh, "< $userdir/$user_id/blog.cgi" or &error("そのような日記は存在しません");
				while (my $line = <$fh>) {
					$line =~ tr/\x0D\x0A//d;
					my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
					if ($btime > &date_to_time(&time_to_date($time - 7 * 24 * 3600))) {
						$bcomment = join "<br>", @bcomment_arr;
						if ($is_mobile) {
							if ($index >= $m{stock} && $index < $m{stock} + 20) {
								$mes .= qq|<hr>『$baddr』$bnameの日記<br>$bcomment|;
								$mes .= qq|<form method="$method" action="$script">|;
								$mes .= qq|<input type="hidden" name="cmd" value="$user_id:$btime:"><input type="submit" value="この日記に投票" class="button1">|;
								$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
								$mes .= qq|</form>|;
								$mes .= qq|<hr><br>|;
							}
						}
						else {
							$mes .= qq|<table class="table1" cellpadding="5" width="440">|;
							$mes .= qq|<tr><td>『$baddr』$bnameの日記$bcomment</td>|;
							$mes .= qq|<td><form method="$method" action="$script">|;
							$mes .= qq|<input type="hidden" name="cmd" value="$user_id:$btime:"><input type="submit" value="この日記に投票" class="button1">|;
							$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
							$mes .= qq|</form></td></tr>|;
							$mes .= qq|</table><br>|;
						}
						$index++;
					}
				}
				close $fh;
			}
		}
		closedir $dh;
		if ($is_mobile) {
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="cmd" value="0"><input type="hidden" name="mode" value="prev"><input type="submit" value="前へ" class="button1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="cmd" value="0"><input type="hidden" name="mode" value="next"><input type="submit" value="次へ" class="button1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
		}
		
		$m{tp} += 10;
		&n_menu;
	} else {
		my $is_find = 0;
		unless(-f "$this_blog_vote_result_file"){
			open my $fh, "> $this_blog_vote_result_file" or &error('日記投票結果ファイルが開けません');
			close $fh;
		}
		open my $fh, "+< $this_blog_vote_result_file" or &error('日記投票結果ファイルが開けません');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($name, $date) = split /<>/, $line;
			if ($date eq &time_to_date($time - $wday * 24 * 3600)) {
				$is_find = 1;
			}

			push @lines, "$name<>$date<>\n";
		}
		unless(-f "$this_blog_vote_file"){
			open my $vfh, "> $this_blog_vote_file" or &error('日記投票ファイルが開けません');
			close $vfh;
		}
		unless ($is_find) {
			%votes = ();
			open my $vfh, "< $this_blog_vote_file" or &error('日記投票ファイルが開けません');
			while (my $line = <$vfh>) {
				my($name, $vote) = split /<>/, $line;
				my ($user_id, $btime) = split /:/, $vote;
				if ($btime > &date_to_time(&time_to_date($time - (7 + $wday) * 24 * 3600))) {
					$votes{$user_id}++;
				}
			}
			close $vfh;
			
			$max_vote = 0;
			$max_id = '';
			foreach my $key_id (keys(%votes)) {
				if ($max_vote < $votes{$key_id}) {
					$max_vote = $votes{$key_id};
					$max_id = $key_id;
				}
			}
			$max_name = pack 'H*', $max_id;
			&regist_you_data($max_name, 'shogo', $nikki_shogo);
			&write_send_news("今週の日記大賞は$max_nameさんです");
			
			$vote_date = &time_to_date($time - $wday * 24 * 3600);
			push @lines, "$max_id<>$vote_date<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		&begin;
	}
}

sub tp_510 {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($wday eq '0') {
		if ($cmd) {
			my ($cmd_id, $cmd_time) = split /:/, $cmd;
			unless (-f "$userdir/$cmd_id/blog.cgi") {
				&begin;
				return;
			}
			open my $bfh, "< $userdir/$cmd_id/blog.cgi";
			my $blog_find = 0;
			while (my $line = <$bfh>) {
				$line =~ tr/\x0D\x0A//d;
				my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
				if ($btime eq $cmd_time) {
					$blog_find = 1;
				}
			}
			close $bfh;
			unless ($blog_find) {
				$mes .= 'huga';
				&begin;
				return;
			}
			my @lines = ();
			my $is_find = 0;
			unless(-f "$this_blog_vote_file"){
				open my $fh, "> $this_blog_vote_file" or &error('日記投票ファイルが開けません');
				close $fh;
			}
			open my $fh, "+< $this_blog_vote_file" or &error('日記投票ファイルが開けません');
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $vote) = split /<>/, $line;
				if ($name eq $m{name}) {
					my ($user_id, $btime) = split /:/, $vote;
					if ($btime > &date_to_time(&time_to_date($time - 7 * 24 * 3600))) {
						$vote = $cmd;
						$is_find = 1;
					}
				}

				push @lines, "$name<>$vote<>\n";
			}
			unless ($is_find) {
				push @lines, "$m{name}<>$cmd<>\n";
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} else {
			if ($in{mode} eq 'prev') {
				$m{stock} -= 20;
				$m{stock} = 0 if $m{stock} < 0;
				$m{tp} -= 10;
				&tp_510;
				return;
			} elsif ($in{mode} eq 'next') {
				$m{stock} += 20;
				$m{tp} -= 10;
				&tp_510;
				return;
			}
		}
	}
	&begin;
}

#=================================================
# 肝試し
#=================================================
sub tp_600 {
	$m{lib} = 'hunting_horror';
	$m{tp} = 0;
	&n_menu;
}

#=================================================
# 百物語
#=================================================
sub tp_700 {
	$mes .= 'ほかの人の話を聞いたり、自分で話したりできるよ<br>';
	$m{tp} += 10;
	&menu('やめる','語る', '聞く');
}

sub tp_710 {
	if ($cmd) {
		$layout = 2;
		if ($cmd eq '1') {
			$mes .= qq|<form method="$method" action="$script"><textarea name="comment"></textarea>|;
			$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
			$mes .= qq|<input type="radio" name="cmd" value="1" checked>語る<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="語る" class="button1"></form>|;
		}
		my $index = 0;
		open my $fh, "< $this_horror_story_file";
		while (my $line = <$fh>) {
			my($name, $story, $good, $bad) = split /<>/, $line;
			my @goods = split /,/, $good;
			my $goodn = @goods;
			my @bads = split /,/, $bad;
			my $badn = @bads;
			$index++;
			if ($m{stock} <= $index && $m{stock} + 10 > $index) {
				$mes .= $story;
				$mes .= qq|<br>|;
				$mes .= qq|ｲｲ!:$goodn ｲｸﾅｲ!:$badn|;
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="cmd" value="2">|;
				$mes .= qq|<input type="hidden" name="index" value="$index">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="submit" value="ｲｲ!" class="button1"></form>|;
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="cmd" value="3">|;
				$mes .= qq|<input type="hidden" name="index" value="$index">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="submit" value="ｲｸﾅｲ!" class="button1"></form>|;
				$mes .= '<hr>';
			}
		}
		close $fh;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="cmd" value="4">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="前へ" class="button1"></form>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="cmd" value="5">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="次へ" class="button1"></form>|;
		$m{tp} += 10;
		&n_menu;
	} else {
		&begin;
	}
}

sub tp_720 {
	if ($cmd) {
		if ($cmd eq '1') {
			my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
			if ($hour < 1 || $hour > 3) {
				$mes .= "語る時間じゃないね<br>";
				&begin;
				return;
			}
			open my $fh, ">> $this_horror_story_file";
			print $fh "$m{name}<>$in{comment}<><><>\n";
			close $fh;
		} elsif ($cmd eq '2') {
			my $index = 0;
			my @lines = ();
			open my $fh, "+< $this_horror_story_file";
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $story, $good, $bad) = split /<>/, $line;
				$index++;
				if ($index == $in{index}) {
					my @goods = split /,/, $good;
					my $find = 0;
					for $g (@goods) {
						if ($g eq $m{name}) {
							$find = 1;
						}
					}
					if (!$find) {
						if ($good eq '') {
							$good .= "$m{name}";
						} else {
							$good .= ",$m{name}";
						}
					}
					push @lines, "$name<>$story<>$good<>$bad<>\n";
				} else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} elsif ($cmd eq '3') {
			my $index = 0;
			my @lines = ();
			open my $fh, "+< $this_horror_story_file";
			eval { flock $fh, 2 };
			while (my $line = <$fh>) {
				my($name, $story, $good, $bad) = split /<>/, $line;
				$index++;
				if ($index == $in{index}) {
					my @bads = split /,/, $bad;
					my $find = 0;
					for $b (@bads) {
						if ($b eq $m{name}) {
							$find = 1;
						}
					}
					if (!$find) {
						if ($bad eq '') {
							$bad .= "$m{name}";
						} else {
							$bad .= ",$m{name}";
						}
					}
					push @lines, "$name<>$story<>$good<>$bad<>\n";
				} else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		} elsif ($cmd eq '4') {
			$m{stock} -= 10;
			$m{stock} = 0 if $m{stock} < 0;
			$m{tp} -= 10;
			&{'tp_' . $m{tp}};
			return;
		} elsif ($cmd eq '5') {
			$m{stock} += 10;
			$m{tp} -= 10;
			&{'tp_' . $m{tp}};
			return;
		}
	}
	$m{stock} = 0;
	&begin;
}

#=================================================
# 朝顔育成
#=================================================
sub tp_800 {
	$m{tp} += 10;
	&menu('帰る', '水をやる', '肥料をやる', '他の朝顔を見る');
}

sub tp_810 {
	unless ($m{morning_glory}) {
		$m{morning_glory} = 1;
	}
	$m{morning_glory}++ if rand(100) < 1;
	if ($m{morning_glory_time} + 24 * 60 * 60 < $time) {
		$m{morning_glory} += 5;
		$m{morning_glory_time} = $time;
	}
	$mes .= "現在の高さ:$m{morning_glory}mm<br>";
	for my $hi (0..$#morning_glory_height) {
		if ($m{morning_glory} >= $morning_glory_heigh[$hi][0]) {
			$mes .= $morning_glory_heigh[$hi][1] . '<br>';
			last;
		}
	}
	if ($cmd) {
		if ($cmd eq '3') {
			$m{tp} += 20;
			&{'tp_' . $m{tp}};
			return;
		}
		if ($cmd eq '1' && $eggs[$m{egg}][1] =~ /ｳｫｰﾀｰ/) {
			$mes .= '水を朝顔にあげたよ';
			$m{egg} = 0;
			$m{morning_glory} *= 2;
		}
		if ($cmd eq '2' && $m{pet}) {
			$mes .= $pets[$m{pet}][1] . 'を朝顔にあげるよ';
			$m{tp} += 10;
			&menu('いいえ', 'はい');
			return;
		}
	}
	&begin;
}

sub tp_820 {
	if ($cmd && $m{pet}) {
		$mes .= $pets[$m{pet}][1] . 'を朝顔にあげたよ';
		$m{pet} = 0;
		$m{morning_glory} += 5;
	}
	&begin;
}

sub tp_830 {
	my @list = ();
	
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		
		my $name = pack 'H*', $pid;
		my %ys = &get_you_datas($pid, 1);
		if ($ys{morning_glory}) {
			push @list, "$name<>$ys{morning_glory}<>\n"
		}
	}
	closedir $dh;
	@list = map { $_->[0] } sort {$b->[2] <=> $a->[2]} map { [$_, split /<>/] } @list;
	my $i = 1;
	my $last_height = -1;
	for my $line (@list) {
		my ($name, $height) = split /<>/, $line;
		if ($i > 10 && $last_height != $height) {
			last;
		}
		$mes .= "$i位 $nameさんの朝顔：$height mm";
		for my $hi (@morning_glory_height) {
			if ($height >= $$hi[0]) {
				$mes .= $$hi[1] . '<br>';
				last;
			}
		}
		$mes .= '<hr>';
		$last_height = $height;
		$i++;
	}
	&begin;
}

#=================================================
# 人気投票
#=================================================
sub tp_900 {
	return if &is_ng_cmd(1);
	
	$mes .= '誰に投票しようか?<br>';
	$mes .= qq|<form method="$method" action="$script"><p>投票相手：<input type="text" name="vote_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>投票する<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="投票" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_910 {
	return if &is_ng_cmd(1);
	if ($in{vote_name} eq '') {
		$mes .= '投票先が記入されてないよ<br>';
		&begin;
		return;
	}
	if ($in{vote_name} eq $m{name}) {
		$mes .= '自分には投票できないよ<br>';
		&begin;
		return;
	}
	
	my $vote_id = unpack 'H*', $in{vote_name};

	if (-f "$userdir/$vote_id/user.cgi") {
		my @lines = ();
		my $is_find = 0;
		unless (-f "$this_vote2_file") {
			open my $fh, "> $this_vote2_file" or &error('人気投票ファイルが開けません');
			close $fh;
		}
		open my $fh, "+< $this_vote2_file" or &error('人気投票ファイルが開けません');
		eval { flock $fh, 2 };
		while (my $line = <$fh>) {
			my($pop_name, $vote_name) = split /<>/, $line;

			if ($vote_name eq $m{name}) {
				$is_find = 1;
				$pop_name = $in{vote_name}
			}

			push @lines, "$pop_name<>$vote_name<>\n";
		}
		unless ($is_find) {
			push @lines, "$in{vote_name}<>$m{name}<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "$in{vote_name} さんに投票した<br>";
		&refresh;
		&n_menu;
	} else {
		$mes .= '誰それ?<br>';
		&begin;
		return;
	}
}

1; # 削除不可
