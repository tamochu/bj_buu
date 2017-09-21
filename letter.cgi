#!/usr/local/bin/perl --
require './config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# 手紙 Created by Merino
#================================================

$max_log = 100; # 手紙のログ数

# 手紙の受信箱設定 項目数増えたら system.cgi の set_letter_flag も要変更

&get_data;
&header_myroom;
if ($in{mode} eq 'delete_kiji' && $in{flag} == 1) { &delete_kiji; }
elsif ($in{mode} eq 'delete_kiji' && $in{flag} == 2) { &output_kiji; }
elsif ($in{mode} eq "write" && $in{comment}) { &_send_letter; }
elsif ($in{mode} eq "refuse") { &add_refuse; }
&letter_box;
&footer;
exit;

#================================================
sub _send_letter { # 手紙の送信処理 受信箱の表示関数内である必要あんまなさそうだから外に出した
	my $rflag = 0;
	open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
		$rflag++ if $line eq $m{name};
	}
	close $fh;

	&send_letter($in{name}, $in{is_save_log}) if $in{name} ne $admin_name || $rflag == 0;
	print qq|<p>$in{name} に手紙を送りました$mes</p>|;

	# プライバシーを考慮し、誰が誰に送信したかだけをロギング
	my $ltime = time();
	open my $fh, ">> $logdir/letter_log.cgi";
	print $fh "$m{name}<>$in{name}<>$ltime\n";
	close $fh;
}

sub letter_box { # 元は get と send で別の関数に分けていたが、基本的に読み込むログが違うぐらいでほぼ同じなのでまとめてしまう 似てるのに受信箱と送信箱の2つを定義するのが面倒
	my $month = (localtime($time))[4]; # 年賀状用
	&header_letter_box($month); # 「手紙」内のﾍｯﾀﾞｰ

	if ($in{type} eq 'new_year' && $month eq '0' && -f "$userdir/$id/greeting_card.cgi") { # 年賀状
		&letter_box_greeting_card;
		return;
	}

	my $count = 0;
	my $this_file = $in{type} eq 'send' ? "$userdir/$id/letter_log.cgi" : "$userdir/$id/letter.cgi";
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	if ($in{type} eq 'send') { # 送信箱
		&letter_box_send($fh, \$count);
	}
	else { # 受信箱
		&letter_box_get($fh, \$count);
	}
	close $fh;

	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><select name="flag" class="menu1">|;
	print qq|<option value="1">削除</option>|;
	print qq|<option value="2">保存</option>|;
	print qq|</select><input type="submit" value="実行" class="button_s"> ($count/$max_log)</p></form>|;

	my $letter_backup = "$userdir/$id/letter.txt";
		$letter_backup = "$userdir/$id/letter_log.txt" if $in{type} eq 'send';
	if (-f "$letter_backup") {
		my $backup_time = (stat $letter_backup)[9];
		my($min, $hour, $mday, $month) = ( localtime($backup_time) )[1..4];
		$month++;
		print qq|<a href="link.cgi?$letter_backup" target="_blank">手紙のﾊﾞｯｸｱｯﾌﾟﾌｧｲﾙ</a> ﾊﾞｯｸｱｯﾌﾟ日 $month/$mday $hour:$min|;
	}

	if ($m{name} eq $admin_name && $in{type} ne 'new_year' && $in{type} ne 'send') { # 受信箱では着拒ﾌｫｰﾑ
		print qq|<form method="$method" action="letter.cgi">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="no" value="$in{no}">|;
		print qq|名 <input type="text" name="rname" class="text_box1" value="$in{send_name}"><br>|;
		print qq|<input type="submit" value="refuse" class="button_s"></form>|;
		print qq|refuse list<br>|;
		open my $rfh, "< $logdir/refuse_list.cgi" or &error("$logdir/$id/letter.cgiﾌｧｲﾙが開けません");
		while (my $line = <$rfh>) {
			print qq|$line<br>|;
		}
		close $rfh;
	}
}

sub letter_box_get {
	my ($fh, $count) = @_;
	my $rows = $is_mobile ? 2 : 8;
	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
	print qq|送り先名 <input type="text" name="name" class="text_box1" value="$in{send_name}"><br>|;
	print qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="手紙を送る" class="button_s">|;
	print qq|　 <input type="checkbox" name="is_save_log" value="1" checked>送信箱に保存</form><br>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		next if(($bcomment =~ /<hr>【.*?全員に送信】/ || $bcomment =~ /<hr>【改造案から送信】/ || $bcomment =~ /<hr>【日記.*?へのｺﾒﾝﾄ】/) && $in{type} eq 'ncountry'); # 個人宛 全通か改造案、日記宛ならnext
		next if($bcomment !~ /<hr>【.*?全員に送信】/ && $in{type} eq 'country'); # 全通 全通じゃないならnext
		next if($bcomment !~ /<hr>【日記.*?へのｺﾒﾝﾄ】/ && $in{type} eq 'diary'); # 日記 日記へのｺﾒﾝﾄじゃないならnext
		next if($bcomment !~ /<hr>【改造案から送信】/ && $in{type} eq 'horyu'); # 改造案 改造案じゃないならnext
		$bshogo = $bshogo ? "[$bshogo]" : '';
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;

		# 手紙の送信者表示 匿名の手紙は送信者の国名を非表示
		my $from_data = $bcountry eq '-1'
			? qq|From <a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>$bshogo <font size="1">($bdate)</font>|
			: qq|From <font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font><a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>$bshogo <font size="1">($bdate)</font>|
			;

		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|$from_data<hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
			# デザイン崩れる気しかしないけど匿名処理考えると称号非表示はマズいかも
#			$bshogo = "" if $is_smart;
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|$from_data<br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$$count;
	}
}

sub letter_box_send {
	my ($fh, $count) = @_;
	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$$count;
	}
}

sub letter_box_greeting_card {
	my $pic_size = q|width="25px" height="25px"|;
	my $count = 0;
	open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("$userdir/$id/greeting_card.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my ($from_name, $from_id, $number) = split /<>/, $line;
		if ($is_mobile) {
			print qq|From $from_name<br>|;
			if ($number % 3 == 0) {
				print qq|┌(┌^o^)┐あけおめ|;
			}
			elsif ($number % 3 == 1) {
				print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>＜謹賀新年|;
			}
			else {
				print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
			}
			print qq|<br>お年玉付き年賀状抽選番号 $number<br><hr><br>|;
		}
		else {
			print qq|<table class="blog_letter" cellpadding="5"><tr><th align="left">|;
			print qq|From $from_name</th></tr>|;
			print qq|<tr><td>|;
			if ($number % 3 == 0) {
				print qq|┌(┌^o^)┐あけおめ|;
			}
			elsif ($number % 3 == 1) {
				print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>＜謹賀新年|;
			}
			else {
				print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
			}
			print qq|<hr>お年玉付き年賀状抽選番号 $number|;
			print qq|</td></tr></table><br>|;
		}
	}
	close $fh;
}

sub header_letter_box {
	my $month = shift;
	my $len = 5 - 1; # letter.cgi の受信箱の数 - 1 配列の上限値 system.cgi でも定義 set_letter_flag
	my @letters = ();
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi" or &error('ﾚﾀｰﾌｧｲﾙが開けません');
		my $line = <$fh>;
		close $fh;
		@letters = split /<>/, $line;
	}

	my $g_card_link;
	if ($month == 0) {
		$g_card_link = $in{type} eq 'new_year' ?  qq|/ 年賀状| : qq| / <a href="?id=$id&pass=$pass&no=$in{no}&type=new_year">年賀状</a>|;
	}

	my $box_send_element = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=send">送信箱</a>|;
	my @box_get_elements = ();
	$box_get_elements[0] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=get">すべて|;
	$box_get_elements[1] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">個人宛|;
	$box_get_elements[2] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=country">一括送信|;
	$box_get_elements[3] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=diary">日記宛|;
	$box_get_elements[4] = qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=horyu">改造案|;
	$box_get_elements[$_] .= $letters[$_] ? "($letters[$_])</a>" : '</a>' for (0 .. $len);

	my $is_rewrite = 1;
	if ($in{type} eq 'ncountry') {
		$box_get_elements[1] = '個人宛';
		$letters[1] = 0;
	}
	elsif ($in{type} eq 'country') {
		$box_get_elements[2] = '一括送信';
		$letters[2] = 0;
	}
	elsif ($in{type} eq 'diary') {
		$box_get_elements[3] = '日記宛';
		$letters[3] = 0;
	}
	elsif ($in{type} eq 'horyu') {
		$box_get_elements[4] = '改造案';
		$letters[4] = 0;
	}
	elsif ($in{type} eq 'send') {
		$box_send_element = '送信箱';
		$is_rewrite = 0;
	}
	else {
		$box_get_elements[0] = 'すべて';
		$letters[0] = 0;
	}

	my $is_delete = 1; # letter_flag.cgi を削除するかどうか
	for my $i (0 .. $len) {
		$is_delete = 0 if $is_delete && $letters[$i]; # 未読があるならば letter_flag.cgi を削除しない
	}
	if ($is_rewrite && !$is_delete) { # letter_flag.cgi が削除されないなら未読状態を更新
		open my $fh, "> $userdir/$id/letter_flag.cgi" or &error('ﾚﾀｰﾌｧｲﾙが開けません');
		my $line = '';
		$line .= "$letters[$_]<>" for (0 .. $len);
		print $fh $line;
		close $fh;
	}
	elsif ($is_delete) {
		unlink "$userdir/$id/letter_flag.cgi";
	}

	print qq|<p>|;
	print qq|受信箱($box_get_elements[0] / $box_get_elements[1] / $box_get_elements[2] / $box_get_elements[3] / $box_get_elements[4]) / $box_send_element$g_card_link|;
	print qq|</p>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_all">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="全チェック" class="button_s"></p></form>|;
}

sub add_refuse {
	my @lines = ();
	open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgiﾌｧｲﾙが読み込めません");
	eval { flock $rfh, 2; };
	while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
		$rflag++ if $line eq $m{name};
		push @lines, "$line\n";
	}
	push @lines, "$in{rname}\n";
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;
}

#================================================
# 記事削除
#================================================
sub delete_kiji {
	return if @delfiles <= 0;
	
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$is_delete = 1;
				print "$bdate $bnameの手紙を削除しました<br>";
				splice(@delfiles, $i, 1);
				last;
			}
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

sub delete_all {
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 1;
		if($bcomment =~ /全員に送信】/ && $in{type} eq 'ncountry') {
			$is_delete = 0;
		}
		if($bcomment !~ /全員に送信】/ && $in{type} eq 'country') {
			$is_delete = 0;
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	print "手紙を削除しました<br>";
}

#================================================
# 記事保存
#================================================
sub output_kiji {
	return if @delfiles <= 0;

	my $this_file = "$userdir/$id/letter.cgi";
		$this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';

	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon, @bcomments) = split /<>/, $line;
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$bshogo = $bshogo ? "[$bshogo] " : '';

				# 手紙の送信者表示 匿名の手紙は送信者の国名を非表示
				my $from_data = $bcountry eq '-1'
					? qq|From $bname $bshogo($bdate)|
					: qq|From $cs{name}[$bcountry] $bname $bshogo($bdate)|
					;

				$bcomment =~ s/<br>/\n/g;
				$bcomment =~ s/<hr>/\n\n/g;
				if (@lines) {
					push @lines, "\n\n$btime $from_data\n$bcomment";
				}
				else {
					push @lines, "$btime $from_data\n$bcomment";
				}
				splice(@delfiles, $i, 1);
				last;
			}
		}
	}
	close $fh;

	my $letter_backup = "$userdir/$id/letter.txt";
		$letter_backup = "$userdir/$id/letter_log.txt" if $in{type} eq 'send';

	open my $fh, "> $letter_backup" or &error("$letter_backupﾌｧｲﾙが読み込めません");
	print $fh @lines;
	close $fh;

	print qq|<a href="link.cgi?$letter_backup" target="_blank">手紙のﾊﾞｯｸｱｯﾌﾟﾌｧｲﾙ</a>|;
#	print "$userdir/$id/letter.txt";
}
