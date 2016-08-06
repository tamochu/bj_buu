#!/usr/local/bin/perl --
require './config.cgi';
require './config_game.cgi';
require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
require "$datadir/profile.cgi";
#================================================
# 日記 Created by Merino
#================================================

# 連続書き込み禁止時間(秒)
$bad_time    = 60;

# 最大ﾛｸﾞ保存件数
$blog_max_log     = 30;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 3000;

# 他人の日記にｺﾒﾝﾄつけられる機能(0:使わない,1:使う)
$is_comment = 1;

# ｺﾒﾝﾄﾛｸﾞファイルは各プレイヤー参入時に空のを用意するように変更しファイル非存在の処理を削る
#================================================

&decode;
$this_file = "$userdir/$in{id}/blog"; # _bbs_chat.cgiを使う時は.cgiをつけたらダメ

&header;
if ($in{id} && $in{pass}) {
	if ($in{mode} eq 'comment_exe') { &header_profile; &comment_exe; } # ｺﾒﾝﾄ追加処理
	elsif ($in{mode} eq 'comment_log') { &view_comment_log; } # ｺﾒﾝﾄﾛｸﾞ表示処理
	else                            { &myself_blog; } # 自分用
}
elsif ($in{mode} eq 'comment_form') { &header_profile; &comment_form; } # ｺﾒﾝﾄ追加ﾌｫｰﾑ
elsif ($in{mode} eq 'good') { &header_profile; &good_exe; } # いいね
elsif ($in{mode} eq 'bad') { &header_profile; &bad_exe; } # わるいね
elsif (-s "$this_file.cgi")         { &header_profile; &view_blog; } # 他人用
else                                { &header_profile; } # 記事/ﾌﾟﾚｲﾔｰが存在しない
&footer;
exit;

#================================================
# 自分の日記を書く
#================================================
sub myself_blog {
	&read_user;
	
	if ($in{mode} eq 'delete_kiji') {
		&delete_kiji;
	}
	elsif ($in{mode} eq "write" && $in{comment}) {
		&read_cs;
		&error('題名が長すぎます') if length $in{title} > 60;

		$in{title} ||= $non_title;
		$addr = $in{title}; # ﾀｲﾄﾙをつけたいので、addrにﾀｲﾄﾙを入れる

		my $name = $m{name};
		$name .= "[$m{shogo}]" if $m{shogo};

		$in{comment} = &comment_change($in{comment}, 0);
		$in{comment} .= qq|<hr><font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $name|;

		my $icon_temp = $m{icon};
		$m{icon} = $in{is_secret} || 0; # 公開/非公開ﾌﾗｸﾞをicon
		my $is_ok = &write_comment;
		
		&write_blog_news(qq|『$in{title}』<a href="blog.cgi?id=$in{id}&country=$m{country}&title=Blog">$m{name}の日記</a>|) if $is_ok && !$in{is_secret};
		
		if (&on_summer && &time_to_date($time) ne &time_to_date($m{blog_time}) && !$m{icon}) {
			$m{blog_time} = $time;
			$m{summer_blog}++;
			$m{icon} = $icon_temp;
			&write_user;
		}
	}
	
	require "$datadir/header_myroom.cgi";
	&header_myroom;

	print qq|$delete_message| if $delete_message;
	print qq|<p>日記 / <a href="?id=$id&pass=$pass&no=$in{no}&mode=comment_log">ｺﾒﾝﾄﾛｸﾞ</a></p>|;
	print qq|<ul><li>$blog_max_log件まで保存(古いものから自動削除)</ul>|;

	my $rows = $is_mobile ? 2 : 14;
	print qq|<form method="$method" action="blog.cgi"><input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|題名[全角30(半角60)文字まで]：<input type="text" name="title" class="text_box_b"><br>|;
	print qq|<textarea name="comment" cols="80" rows="$rows" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="日記を書く" class="button_s"><input type="hidden" name="no" value="1">|;
	print qq|　 <input type="checkbox" name="is_secret" value="1">この記事を非公開にする</form>|;

	print qq|<form method="$method" action="blog.cgi"><input type="hidden" name="mode" value="delete_kiji"><input type="hidden" name="no" value="$in{no}">|;

	my $count = 0;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($line1, $line2) = split /<<>>/, $line;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		my ($bcomment_c,$bgood,$bbad) = split /<>/, $line2;
		my $secret_mark = $bicon ? '【ﾋﾐﾂ】' : '';
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment_c = 0 unless $bcomment_c;
		$bgood = 0 unless $bgood;
		$bbad = 0 unless $bbad;

		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;

		if ($is_mobile) {
			print qq|<br><input type="checkbox" name="delete" value="$btime"> $bdate|;
			print qq|<hr>$baddr $secret_mark|;
			print qq|<hr>$bcomment<br>|;
			if ($is_comment) {
				print qq|<hr>ｺﾒﾝﾄ($bcomment_c) ｲｲ!($bgood) ｲｸﾅｲ!($bbad)|;
				print qq|<br>@bcomments| if @bcomments;
			}
			print qq|<hr><br>|;
		}
		else {
#			print qq|<table class="table1" cellpadding="5" width="440">|;
			print qq|<table class="blog_letter" cellpadding="5">|;
			print qq|<tr><th align="left"><input type="checkbox" name="delete" value="$btime"> $baddr <font size="1">($bdate)</font> $secret_mark<br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			if ($is_comment) {
				print qq|<tr><td>ｺﾒﾝﾄ($bcomment_c) ｲｲ!($bgood) ｲｸﾅｲ!($bbad)|;
				print qq|<br>@bcomments| if @bcomments;
				print qq|</td></tr>|;
			}
			print qq|</table><br>|;
		}
		++$count;
	}
	close $fh;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<p><input type="submit" value="削除" class="button_s"> ($count/$blog_max_log)</p></form>|;
}

#================================================
# 自分のｺﾒﾝﾄﾛｸﾞを見る
#================================================
sub view_comment_log {
	&read_user;

	require "$datadir/header_myroom.cgi";
	&header_myroom;

	print qq|<p><a href="?id=$id&pass=$pass&no=$in{no}">日記</a> / ｺﾒﾝﾄﾛｸﾞ</p>|;
	my $comment_file = "$userdir/$in{id}/comment_log";
	&error("$comment_file.cgiﾌｧｲﾙが開けません") unless (-e "$comment_file.cgi");

	print qq|<ul>|;
	open $fh, "< $comment_file.cgi" or &error("$comment_file.cgiﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($bno,$bid,$btitle,$bname,$bcountry,$btime) = split /<>/, $line;
		print qq|<li>$btime <a href="?id=$bid&country=$bcountry&kiji=$bno&mode=comment_form">$btitle</a> $bnameさんへのｺﾒﾝﾄ</li>|;
	}
	close $fh;
	print qq|</ul>|;
}


#================================================
# 他人の日記を見る
#================================================
sub view_blog {
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($line1, $line2) = split /<<>>/, $line;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		my ($bcomment_c,$bgood,$bbad) = split /<>/, $line2;
		next if $bicon;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment_c = 0 unless $bcomment_c;
		$bgood = 0 unless $bgood;
		$bbad = 0 unless $bbad;
		# 行数は増えるが三項演算子は重いイメージがあるので分割
#		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			$bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g;
#			print qq|<br>$bdate|;
#			print qq|<hr>$baddr|;
#			print qq|<hr>$bcomment<br>|;
#			print qq|<hr><a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">ｺﾒﾝﾄを書く</a><br>@bcomments| if $is_comment;
#			print qq|<hr><br>|;
			print qq|$bdate <a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">$baddr</a><hr>|;
		}
		else {
			$bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
#			print qq|<table class="table1" cellpadding="5" width="440">|;
#			print qq|<div class="disp_scroll">| if $is_smart; # iPhoneはダメ
			print qq|<table class="blog_letter" cellpadding="5">|;
			print qq|<tr><th align="left">$baddr <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			print qq|<tr><td><a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">ｺﾒﾝﾄを書く($bcomment_c)</a> <a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=good">ｲｲ!($bgood)</a> <a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=bad">ｲｸﾅｲ!($bbad)</a>|;
			print qq|<br>@bcomments| if $is_comment;
			print qq|</td></tr>|;
			print qq|</table><br>|;
#			print qq|</div>| if $is_smart; # iPhoneはダメ
		}
	}
	close $fh;
}


#================================================
# ｺﾒﾝﾄ書き込みﾌｫｰﾑ
#================================================
sub comment_form {
	return unless $is_comment;
	my($cook_name, $cook_pass) = &get_cookie;

	my $cline = '';
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($line1, $line2) = split /<<>>/, $line;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		next if $bicon;
		if ($in{kiji} eq $btime) {
			$cline = $line;
			last;
		}
	}
	close $fh;

	if ($cline) {
		print '以下の記事にｺﾒﾝﾄします<hr>';
		my ($line1, $line2) = split /<<>>/, $cline;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		my ($bcomment_c,$bgood,$bbad) = split /<>/, $line2;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment_c = 0 unless $bcomment_c;
		$bgood = 0 unless $bgood;
		$bbad = 0 unless $bbad;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			print qq|<br>$bdate|;
			print qq|<hr>$baddr|;
			print qq|<hr>$bcomment<br>|;
			print qq|<hr>ｺﾒﾝﾄ($bcomment_c) ｲｲ!($bgood) ｲｸﾅｲ!($bbad)|;
			print qq|<br>@bcomments| if @bcomments;
			print qq|<hr><br>|;
		}
		else {
#			print qq|<table class="table1" cellpadding="5" width="440">|;
			print qq|<table class="blog_letter" cellpadding="5">|;
			print qq|<tr><th align="left">$baddr <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			print qq|<tr><td>ｺﾒﾝﾄ($bcomment_c) ｲｲ!($bgood) ｲｸﾅｲ!($bbad)|;
			print qq|<br>@bcomments</td></tr>| if @bcomments;
			print qq|</table><br>|;
		}
	
		print qq|<form method="$method" action="blog.cgi">|;
		print qq|<input type="hidden" name="mode" value="comment_exe"><input type="hidden" name="id" value="$in{id}">|;
		print qq|<input type="hidden" name="country" value="$in{country}"><input type="hidden" name="kiji" value="$in{kiji}">|;
		print qq|<table class="blog_letter"><tr><th><tt>ﾌﾟﾚｲﾔｰ名:</tt></th><td><input type="text" name="name" value="$cook_name" class="text_box1"><br></td></tr>|;
		print qq|<tr><th><tt>ﾊﾟｽﾜｰﾄﾞ:</tt></th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"><br></td></tr></table>|;
		print qq|全角300(半角600)文字まで：<br><textarea name="comment" cols="60" rows="4" class="textarea1"></textarea><br>|;
		print qq|<input type="submit" value="書き込む" class="button_s"></form>|;
	}
	else {
		print '該当記事が見つかりません<br>';
	}
}

#================================================
# ｺﾒﾝﾄ書き込み処理
#================================================
sub comment_exe {
	return unless $is_comment;
	if ($in{name} eq '' || $in{pass} eq '' || $in{comment} eq '' || $in{comment} =~ /^(<br>|\s|　)+$/) {
		print "やめました<br>";
		return;
	}
	&error("文字数ｵｰﾊﾞｰ全角300(半角600)文字までです") if length $in{comment} > 600;

	# 全体的にもっとなんかスマートに書き直せる気がするけど面倒なので放置
	my $blog_uid = $in{id}; # 読んでたブログのID（他プレイヤーのID）
	my $send_name = pack 'H*', $in{id}; # ブログを書いた人の名前
	$in{id} = unpack 'H*', $in{name}; # 自分の名前をIDに変換
	my $m_id = $in{id}; # あとで使うので退避
	&read_user;
	# ↑自分が存在するかのチェック後に読んでたブログIDを戻さないと、
	# コメント投稿直後に表示されるブログの「ｺﾒﾝﾄを書く」先が自分の日記になってしまう
	$in{id} = $blog_uid;

	if (-f "$userdir/$blog_uid/blacklist.cgi") {
		open my $fh, "< $userdir/$blog_uid/blacklist.cgi" or &error("$userdir/$blog_uid/blacklist.cgiﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			my($blackname) = split /<>/, $line;
			if ($blackname eq $m{name}) {
				&error('ﾌﾞﾗﾀﾓﾘ');
			}
		}
		close $fh;
	}

	my $is_rewrite = 0;
	my @lines = ();
	my @log_lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($line1, $line2) = split /<<>>/, $line;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		my ($bcomment_c,$bgood,$bbad) = split /<>/, $line2;
		$bcomment_c = 0 unless $bcomment_c;
		$bgood = 0 unless $bgood;
		$bbad = 0 unless $bbad;
		if (!$bicon && $in{kiji} eq $btime) {
			$is_rewrite = 1;
			$bcomment_c++;
			push @bcomments, qq|<><b>$m{name}</b>『$in{comment}』<font size="1">($date)</font><br>|;
			$line = "$btime<>$bdate<>$bname<>$bcountry<>$bshogo<>$baddr<>$bcomment<>$bicon<>@bcomments<<>>$bcomment_c<>$bgood<>$bbad<>";

			unless ($send_name eq $m{name}) {
				# ｺﾒﾝﾄ手紙を送る 
				$in{comment} .= "<hr>【日記$baddrへのｺﾒﾝﾄ】";
				&send_letter($send_name);

				#ｺﾒﾝﾄログに追加
				push(@log_lines, "$btime<>$blog_uid<>$baddr<>$send_name<>$bcountry<>$date<>\n");
			}
		}
		push @lines, "$line\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		# 各プレイヤー参入時にｺﾒﾝﾄﾛｸﾞファイルを準備するようにすれば非存在チェックは不要
		my $lfh;
		my $comment_file = "$userdir/$m_id/comment_log";
		if (-e "$comment_file.cgi") {
			my $i = 1;
			open $lfh, "+< $comment_file.cgi" or &error("$comment_file.cgiﾌｧｲﾙが開けません");
			eval { flock $lfh, 2; };
			while (my $line2 = <$lfh>) {
				push(@log_lines, "$line2") if $i < 30; # ｺﾒﾝﾄﾛｸﾞは30件
				$i++;
			}
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
		}
		else {
			open $lfh, "> $comment_file.cgi" or &error("$comment_file.cgiﾌｧｲﾙが開けません");
		}
		print $lfh @log_lines;
		close $lfh;

		print "ｺﾒﾝﾄを書き込みました<br>";
		&view_blog;
	}
	else {
		close $fh;
		close $lfh;
		print "該当記事が見つかりません<br>";
	}
}


#================================================
# 自分の日記の記事削除
#================================================
sub delete_kiji {
	return if @delfiles <= 0; 
	
	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$is_delete = 1;
				$delete_message .= "$bdate $baddrの記事を削除しました<br>";
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

#================================================
# いいね わるいね
#================================================
sub good_bad {
	my $good_bad = shift;
	if ($in{id} eq '' || $in{kiji} eq '') {
		print "やめました<br>";
		return;
	}

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($line1,$line2)  = split /<<>>/, $line;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line1;
		my($bcomment_c,$bgood, $bbad) = split /<>/, $line2;
		$bcomment_c = 0 unless $bcomment_c;
		$bgood = 0 unless $bgood;
		$bbad = 0 unless $bbad;
		if (!$bicon && $in{kiji} eq $btime) {
			$is_rewrite = 1;
			if ($good_bad) {
				$bgood++;
			}
			else {
				$bbad++;
			}
			$line = "$btime<>$bdate<>$bname<>$bcountry<>$bshogo<>$baddr<>$bcomment<>$bicon<>@bcomments<<>>$bcomment_c<>$bgood<>$bbad<>";
		}
		push @lines, "$line\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		if ($good_bad) {
			print "ｲｲ!しました";
		}
		else {
			print "ｲｸﾅｲ!しました";
		}
		&view_blog;
	}
	else {
		close $fh;
		close $lfh;
		print "該当記事が見つかりません<br>";
	}
}
sub good_exe {
	&good_bad(1);
}
sub bad_exe {
	&good_bad(0);
}
