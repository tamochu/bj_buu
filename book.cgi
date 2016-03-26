#!/usr/local/bin/perl --
require './config.cgi';
require './config_game.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# 本作成 Created by Merino
#================================================

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 4000;

# 宣伝費
$need_ad_money = 500;


#================================================
&decode;
&header;
&read_user;
&header_myroom;
&run;
&footer;
exit;

#================================================
# 本作成
#================================================
sub run {
	&write_book if $in{mode} eq "write";
	
	my $sub_mes = '';
	my $count = 0;
	opendir my $dh, "$userdir/$id/book" or &error("$userdir/$id/bookﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		next if $file_name =~ /^backup$/;
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<li><a href="$userdir/$id/book/$file_name" target="_blank">$file_title</a>|;
		++$count;
	}
	closedir $dh;

	print qq|<p>$mes</p>|;
	print qq|<p>$m{name}の本の所持数 $count / $max_my_book冊</p>|;

	if ($max_my_book > $count) {
		print qq|<ul><li>作成したﾃｷｽﾄについては、著作権・肖像権等について法令上の義務に従い、<br>作成したﾌﾟﾚｲﾔｰの自己責任において登録・掲載されるものとします。</ul>|;
		my $rows = $is_mobile ? 2 : 20;
		print qq|<form method="$method" action="book.cgi"><input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|ﾀｲﾄﾙ[全角30(半角60)文字まで]<br><input type="text" name="title" class="text_box_b"><br>|;
		print qq|本文[全角| .int($max_comment * 0.5). qq|(半角$max_comment)文字まで]<br>|;
		print qq|<textarea name="comment" cols="80" rows="$rows" class="textarea1"></textarea><br>|;
		print qq|<input type="radio" name="option" value="" checked>通常<br>|;
		print qq|<input type="radio" name="option" value="ad">作った本を宣伝する($need_ad_money G)<br>|;
		print qq|<input type="radio" name="option" value="contest">ｺﾝﾃｽﾄ用(ﾀｲﾄﾙとは別にﾌｧｲﾙ名が無題となります)<br>|;
		print qq|<input type="submit" value="本を作成" class="button_s"></form>|;
	}
	
	print qq|<hr>所持している本<ul>$sub_mes</ul><br>|;
}

sub write_book {
	&error("ﾀｲﾄﾙを記入してください") unless $in{title};
	&error("ﾀｲﾄﾙにﾋﾟﾘｵﾄﾞ(.)は使えません") if $in{title} =~ /\./;
	&error("ﾀｲﾄﾙの先頭にｱﾝﾀﾞｰﾗｲﾝ(_)は使えません") if $in{title} =~ /^_/;
	&error("ﾀｲﾄﾙの文字数ｵｰﾊﾞｰ。半角60文字までです") if length $in{title} > 60;
	&error("本文を記入してください") unless $in{comment};
	&error("本文の文字数ｵｰﾊﾞｰ。半角$max_comment文字までです") if length $in{comment} > $max_comment;

	my $file_title = '';
	if ($in{option} eq 'contest') {
		$file_title = "_$time.html";
	}
	else {
		$file_title = unpack 'H*', "$in{title} 作:$m{name}";
		$file_title .= '.html';
	}
	&error("すでに同じ名前の作品が存在します") if -f "$userdir/$id/book/$file_title";

	my $goods_c = &my_goods_count("$userdir/$id/book");
	&error("$max_my_book冊以上本を所有することができません") if $goods_c >= $max_my_book;

	$html .= qq|<html><head>|;
	$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	$html .= qq|<link rel="stylesheet" type="text/css" href="../../../$htmldir/bj.css">|;
	$html .= $in{option} eq 'contest' ? qq|<title>$in{title}</title>| : qq|<title>$in{title} 作:$m{name}</title>|;
	$html .= qq|</head><body $body>|;
	$html .= qq|<form action="../../../"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	$html .= $in{option} eq 'contest' ? qq|<h1>$in{title}</h1>| : qq|<h1>$in{title} 作:$m{name}</h1>|;
	$html .= qq|<div>$in{comment}</div>|;
	$html .= qq|<br><div align="right" style="font-size:11px">|;
	$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama楽.net</a><br>|; # 著作表示:削除・非表示 禁止!!
	$html .= qq|$copyright|;
	$html .= qq|</div></body></html>|;
	
	open my $fh, "> $userdir/$id/book/$file_title" or &error("$userdir/$id/book/$file_titleﾌｧｲﾙが作れません");
	print $fh $html;
	close $fh;
	
	if ($in{option} eq 'contest') {
		$mes .= "$non_titleの本を作りました<br>";
	}
	else {
		$mes .= "『$in{title}』という本を作りました<br>";

		# 宣伝
		if ($in{option} eq 'ad') {
			&read_cs;
			&write_book_news("$cs{name}[$m{country}]の$m{name}が『$in{title}』という作品を発表\しました");
			$mes .= "『$in{title}』という作品を発表\しました<br>";
			$m{money} -= $need_ad_money;
			&write_user;
		}
	}
}
