require "$datadir/contest.cgi";
#================================================
# ｺﾝﾃｽﾄ Created by Merino
#================================================

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かしますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ｺﾝﾃｽﾄ会場に来ました<br>';
		$mes .= qq|<form method="$method" action="contest.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="作品を見る" class="button1"></form>|;
	}
	
	&menu('やめる', '作品を見る', 'ｴﾝﾄﾘｰする');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# 作品を見る
#=================================================
sub tp_100 {
	$mes .= qq|<form method="$method" action="contest.cgi">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="作品を見る" class="button1"></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	&begin;
}

#=================================================
# ｴﾝﾄﾘｰ
#=================================================
sub tp_200 {
	$mes .= qq|どのｺﾝﾃｽﾄにｴﾝﾄﾘｰしますか?<br>|;
	$mes .= qq|<li>$non_titleの作品しかｴﾝﾄﾘｰすることはできません<br>|;
	$mes .= qq|<li>ｴﾝﾄﾘｰをした場合、途中でやめることはできません<br>|;
	$mes .= qq|<li><font color="#FF0000">ｴﾝﾄﾘｰされた作品は、過去の作品展示が終わるまで手元には戻ってきません</font><br>|;
	
	&menu('やめる', map{ $_->[0] }@contests);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..$#contests+1);
	$m{value} = $cmd-1;
	
	open my $fh, "< $logdir/contest/$contests[$m{value}][1]/prepare.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/prepare.cgiﾌｧｲﾙが開けません");
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	close $fh;

	$mes .= qq|次回、第$round回$contests[$m{value}][0] ｴﾝﾄﾘｰﾌｫｰﾑ<br>|;
	$mes .= qq|どの作品でｴﾝﾄﾘｰしますか?<br>|;
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="file" value="0" checked>やめる<hr>|;
	
	opendir my $dh, "$userdir/$id/$contests[$m{value}][1]" or &error("$userdir/$id/$contests[$m{value}][1]ﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next unless $file_name =~ /^_/;
		
		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="file" value="$file_name">|;
		$mes .= $contests[$m{value}][2] eq 'img'  ? qq|$file_title <img src="$userdir/$id/$contests[$m{value}][1]/$file_name" style="vertical-align:middle;"><hr>|
			  : $contests[$m{value}][2] eq 'html' ? qq|<a href="$userdir/$id/$contests[$m{value}][1]/$file_name" target="_blank">$file_title</a><br>|
			  :                                     qq|$file_title<br>|;
			  ;
	}
	close $dh;
	
	$mes .= qq|ﾀｲﾄﾙ[全角30(半角60)文字まで]<br><input type="text" name="title" class="text_box_b"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="ｴﾝﾄﾘｰ" class="button1"></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_220 {
	unless ($in{file}) {
		$mes .= "やめました<br>";
		&begin;
		return;
	}
	&error("ﾀｲﾄﾙを記入してください") unless $in{title};
	&error("ﾀｲﾄﾙにﾋﾟﾘｵﾄﾞ(.)は使えません") if $in{title} =~ /\./;
	&error("ﾀｲﾄﾙの文字数ｵｰﾊﾞｰ。全角30(半角60)文字までです") if length $in{title} > 60;
	&error("選択した作品が存在しません") unless -f "$userdir/$id/$contests[$m{value}][1]/$in{file}";
	&error("現ｺﾝﾃｽﾄにｴﾝﾄﾘｰしているためｴﾝﾄﾘｰすることはできません") if !$is_renzoku_entry_contest && &is_entry_contest;
	
	my $count = 0;
	my @lines = ();
	open my $fh, "+< $logdir/contest/$contests[$m{value}][1]/prepare.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/prepare.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		&error("第$round回$contests[$m{value}][0]にはすでにｴﾝﾄﾘｰ済みです") if $name eq $m{name};
		++$count;
		push @lines, $line;
	}
	&error("残念ながら定員を締め切りました。これ以上ｴﾝﾄﾘｰすることはできません") if $count >= $max_entry_contest;
	++$count;
	rename "$userdir/$id/$contests[$m{value}][1]/$in{file}", "$logdir/contest/$contests[$m{value}][1]/$round/_${count}_$in{file}" or &error("ｴﾝﾄﾘｰに失敗しました");
	push @lines, "$count<>$m{name}<>$in{title}<>_${count}_$in{file}<>0<><><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "第$round回$contests[$m{value}][0]に【No.$count $in{title}】でｴﾝﾄﾘｰしました<br>";
	
	&begin;
}

# ------------------
sub is_entry_contest {
	open my $fh, "< $logdir/contest/$contests[$m{value}][1]/entry.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/entry.cgiﾌｧｲﾙが読み込めません");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		return 1 if $name eq $m{name};
	}
	close $fh;
	return 0;
}




1; # 削除不可
