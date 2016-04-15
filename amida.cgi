#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use List::Util;
use CGI;
my $this_script = 'amida.cgi';
$this_file = "$logdir/amida";
#================================================
# あみだくじ Created by nanamie
#================================================

# qq|－| 全角マイナスとか全角チルダはエラー

$max_log = 5;

$cgi = CGI->new;
#$items = $cgi->param("items");


#================================================
#&decode;
&header;

$in{id} = $cgi->param("id");
$in{login_name} = pack 'H*', $in{id};
$in{pass} = $cgi->param("pass");

&read_user;
&access_check;

&run;

&footer;
exit;

#================================================

sub run {
	my $title = $cgi->param("title");
	my $step = $cgi->param("step");
	my $amida = $cgi->param("amida");
	my $no = $cgi->param("no");

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;

	print "<h1>あみだくじ</h1>";

	# あみだ一覧とあみだ作成直後の一覧以外で一覧に戻るボタンを表示
	if (($step || $amida) && $step != 2) {
		&back_amida_form;
	}
	elsif ($step != 2) {
		&create_amida_form;
	}

	# あみだを開くかあみだ一覧を開く
	if ($step == 0) {
#		if ($amida) {
			&view_amida($amida);
#		}
#		else {
#			print "<ul>";
#			open my $fh, "< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
#			while (my $line = <$fh>) {
#				my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp) = split /<>/, $line;
	
#				if ($bcmp) { print "<li>[公開済]"; } else { print "<li>[募集中]"; } 
#				print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime">$btitle</a> $bmaker作 $bdate|;
#				if (!$bcmp && $in{login_name} eq $bmaker) {
#					print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime&step=3&cmp=1">公開する</a>|;
#				}
#				print qq|</li>|;
#			}
#			print "</ul>";
#			close $fh;
#		}
	}
	elsif ($step == 1) {
		my $count = $cgi->param("count");
		my $items = $cgi->param("items");
		$items =~ s/^\s+//g;
		$items =~ s/\s+$//g;
		$items =~ s/(?:\r\n){2,}/\r\n/g;
		$items =~ s/\r+/\r/g;
		$items =~ s/\n+/\n/g;
#		$items =~ tr/(?:\r\n)//s;
#		$items =~ tr/\r//s;
#		$items =~ tr/\n//s;
#		$items =~ s/(?:\r\n){1,}/\r\n/g;
#		$items =~ s/\r/\r/g;
#		$items =~ s/\n/,/g;
#		$items =~ s/\r\n{2,}//g;
#		$items =~ s/\r{2,}//g;
#		$items =~ s/\n{2,}//g;

		print qq|<form method="$method" action="$this_script">|;
		print qq|<table>|;
		print qq|<tr><td><label for="title">くじのタイトル：</label></td><td><input type="text" name="title" id="title" min="1" max="30" required="required" value="$title"></td></tr>|;
		print qq|<tr><td><label for="count">くじの本数：</label></td><td><input type="number" name="count" id="count" min="2" max="30" required="required" value="$count"></td></tr>|;
		print qq|<tr><td><label for="items">当たり賞品：<br>（1行1賞品）</label></td><td><textarea name="items" rows="8" cols="10" word="soft" id="items" required="required">$items</textarea></td></tr>|;
		print qq|<tr><td colspan="2" style="text-align:center;"><input type="submit" value="あみだ作成" class="button1"></td></tr>|;
		print qq|</table>|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="2"></form>|;
	}
	elsif ($step == 2) {
		my $count = $cgi->param("count");
		my $items = $cgi->param("items");
		$items =~ s/^\s+//g;
		$items =~ s/\s+$//g;
		$items =~ s/(?:\r\n){2,}/\r\n/g;
		$items =~ s/\r+/\r/g;
		$items =~ s/\n+/\n/g;

		&rewrite_amida_form('タイトルがありません', ($in{id}, $in{pass}, $title, $count, $items))	unless $title;
		&rewrite_amida_form('タイトルに不正な文字( ,;\"\'&<>\\\/ )が含まれています', ($in{id}, $in{pass}, $title, $count, $items))	if $title =~ /[,;\"\'&<>\\\/]/;#"
		&rewrite_amida_form('本数に入力できるのは 2 以上の数値だけです', ($in{id}, $in{pass}, $title, $count, $items))	unless $count  =~ /^[0-9]+$/;#"
		&rewrite_amida_form('賞品リストに不正な文字( ,;\"\'&<>\\\/ )が含まれています', ($in{id}, $in{pass}, $title, $count, $items))	if $items =~ /[,;\"\'&<>\\\/]/;#"
		&rewrite_amida_form('賞品リストに何も入力されていません', ($in{id}, $in{pass}, $title, $count, $items))	unless $items;

		$items =~ s/\r\n/,/g;
		$items =~ s/\r/,/g;
		$items =~ s/\n/,/g;
		$items =~ s/,{2,}/,/g;
		$items =~ s/,{1,}$//g;
		my @item_list = split /,/, $items;

		&rewrite_amida_form('賞品リストに何も入力されていません', ($in{id}, $in{pass}, $title, $count, $items))	unless @item_list;
		&rewrite_amida_form('賞品数がくじの本数を超えています', ($in{id}, $in{pass}, $title, $count, $items))	if @item_list > $count;

		my $users = "";
		for(my $i = 1; $i < $count; $i++) {
			$users .= ",";
		}
		my $sitems = "";
		for(my $i = 1; $i < @item_list; $i++) {
			$sitems .= ",";
		}

		my $maker = pack 'H*', $in{id};

		my @lines = ();
		my $new_line = "$time<>$date<>$maker<>$title<>$count<>$items<>$users<>0<>0<>$users<>$sitems<>";
		push @lines, "$new_line\n";

		&create_amida_form;
		print "あみだくじを作成しました<br>";
		print "<ul>";
		print qq|<li>[募集中]<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$time">$title</a> $maker作 $date|;
		print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$time&step=3&cmp=1">公開する</a></li>|;
		open my $fh, "+< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

			print qq|<li>|;
			if ($bcmp) { print "[公開済]"; } else { print "[募集中]"; } 
			print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime">$btitle</a> $bmaker作 $bdate|;
			if (!$bcmp && $in{login_name} eq $bmaker) {
				print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime&step=3&cmp=1">公開する</a>|;
			}
			print qq|</li>|;
			push @lines, "$line\n";
			last if @lines >= $max_log;
		}
		print "</ul>";

		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	elsif ($step == 3) {
		if ($amida) {
			my @lines = ();
			my $cmp = $cgi->param("cmp");
			open my $fh, "+< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				$line =~ tr/\x0D\x0A//d;
				my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

				if ($btime ne $amida) {
					push @lines, "$line\n";
					next;
				}
				my @user_list = $bcount;
				@user_list = split /,/, $busers;

				print qq|<p>$btitle 作：$bmaker $bdate</p>|;

				if ($bcmp) {
					print qq|<p>このあみだくじは終了しています</p>|;#	unless $items;
				}
				elsif ($in{login_name} eq $bmaker && $cmp) {
					print qq|<p>あみだくじを公開しました</p>|;
				}
				elsif (&is_entry($in{login_name}, @user_list)) {
					print qq|<p>すでにｴﾝﾄﾘｰ済みです。重複してｴﾝﾄﾘｰすることはできません</p>|;#	unless $items;
				}
				elsif ($user_list[$no]) {
					print qq|<p>そのくじはすでに$user_list[$no]さんがｴﾝﾄﾘｰしています</p>|;#	unless $items;
				}
				else {
					print "<p>".($no+1)."番目のくじにｴﾝﾄﾘｰしました</p>";#	unless $items;
					$user_list[$no] = $in{login_name};
					$bscount++;
					$busers = join(',', @user_list);

#					for (my $i = 0; $i < $bcount; $i++) {
#						if ($user_list[$i]) {
#							$user_count++;
#							$user_list[$i] = "";
#						}
#					}
				}


#				for (my $i = 0; $i < $bcount; $i++) {
#					unless ($user_list[$i]) {
#						$user_count--;
#						$user_list[$i] = "";
#					}
#				}

#				my $_cmp = 1;
#				for (my $i = 0; $i < $bcount; $i++) {
#					$_cmp = ($user_list[$i]) && $_cmp;
#				}

				print qq|<p>すべてのくじが埋まったため結果を公開します</p>|	if ($bcount <= $bscount) && !$cmp;
				print qq|<span>くじの本数：$bcount</span><br>|;
				print qq|<span>賞品リスト：$bitems</span><br>|;
				print qq|<span>現在の参加者：$bscount人</span><br><br>|;

				my $cmp_flg = ($bcmp || ($bcount <= $bscount)  || ($in{login_name} eq $bmaker && $cmp) ) ? 1 : 0;
				if ($cmp_flg) {
					# 参加者が埋まったか公開されたイコールくじ公開
					my @item_list = $bcount;
					@item_list = split /,/, $bitems;
#					for (my $i = 0; $i < $bcount; $i++) {
#						unless ($item_list[$i]) {
#							$item_list[$i] = "";
#						}
#					}
					my @suser_list = List::Util::shuffle(@user_list);
					$bsusers = join(',', @suser_list);
					@item_list = List::Util::shuffle(@item_list);
					$bsitems = join(',', @item_list);
#					for (my $i = 0; $i < $bcount; $i++) {
#						print "<tr><td>".($i+1).".";
#						print qq|$user_list[$i]|	if $user_list[$i];
#						print "</td><td>－あみだ線は省略－</td>";
#						print "<td>$suser_list[$i]</td>";
#						print "<td>$item_list[$i]</td>";
#						print "</tr>";
#					}
				}
#				else {
#					for (my $i = 0; $i < $bcount; $i++) {
#						print "<tr><td>".($i+1).".";
#						print qq|$user_list[$i]|	if $user_list[$i];
#						print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">このくじにする</a>|	unless $user_list[$i];
#						print "</td><td>－あみだ線は省略－</td>";
#						print "</tr>";
#					}
#				}

				print "<table>";
				for (my $i = 0; $i < $bcount; $i++) {
					print "<tr><td>".($i+1).".";
					print qq|$user_list[$i]|	if $user_list[$i];
					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">このくじにする</a>|	unless $user_list[$i] || $cmp_flg;
					print "</td><td>－あみだ線は省略－</td>";
					print "<td>$suser_list[$i]</td>"	if $cmp_flg;
					print "<td>$item_list[$i]</td>"	if $cmp_flg;
					print "</tr>";
				}
				print "</table>";
				$line = "$btime<>$bdate<>$bmaker<>$btitle<>$bcount<>$bitems<>$busers<>$cmp_flg<>$bscount<>$bsusers<>$bsitems<>";

				push @lines, "$line\n";
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
}

# あみだってこんな感じでしょの思い付き実装
# アルゴリズム詳しい人修正よろしく
sub amida_shuffle {
	my $vline = shift;
	my $hline = $vline * int(rand(4)+3); # 縦線の *3～6 の横線

	my @result;
	for (my $i = 0; $i < $vline; $i++) {
		$result[$i] = $i; # 各要素を要素数 +1 で初期化
	}

#	my @result2;

#result
#0 1 2 3 4

#result2
#0

#	for (my $i = 0; $i < $vline; $i++) {
#		$result2[$i] = int( rand($vline) + $i ); # 重複しないように一周毎に範囲を狭める
#		my $cnt = 0;
#		for (my $k = 0; $k < @result2; $k++) {
#			for (my $l = 0; $l < $i; $l++) {
#				$cnt += 1	$result2[$k] == $result[$l];
#			}
#		}
#		for (my $k = 0; $k < $i; $k++) {
#			foreach my $l (@result2) {
#				$flg = 1	if $result[$k] eq $l;
#			}
#		}
#		redo 
#		print "$name\n";
#	}

	my $j = 0;
	my $k = 0;
	my $l = -1;

	for (my $i = 0; $i < $hline; $i++) {
		while (1) {
			$j = int(rand($vline));
			if ($j != $l) {
				$l = $j;
				last;
			}
		}

		$k = $j eq 0 ? 1 : # 左端なら右に線を引く
			$j eq ($vline-1) ? -1 : # 右端なら左に線を引く
			int(rand(2)) ? 1 : -1; # どちらでもないなら左右どちらかに線を引く

		# 横線で繋がる縦線とスワップ
		($result[$j], $result[$k]) = ($result[$k], $result[$j]);
	}

	return @result;
}

sub back_amida_form {
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="0">|;
	print qq|<input type="submit" value="一覧に戻る" class="button1"></form>|;
}

sub create_amida_form {
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="1">|;
	print qq|<input type="submit" value="あみだを作る" class="button1"></form>|;
}

sub rewrite_amida_form {
	my ($err, @data) = @_;
	&back_amida_form;
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$data[0]"><input type="hidden" name="pass" value="$data[1]"><input type="hidden" name="title" value="$data[2]"><input type="hidden" name="count" value="$data[3]"><input type="hidden" name="items" value="$data[4]"><input type="hidden" name="step" value="1">|;
	print qq|<input type="submit" value="あみだを作り直す" class="button1"></form>|;
	&error($err);
}

sub view_amida {
	my $amida = shift;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgiﾌｧｲﾙが開けません");
	if ($amida) {
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

			next	if $btime != $amida;

			my @user_list = split /,/, $busers;
#			my $user_count = 0;
#			for (my $i = 0; $i < $bcount; $i++) {
#				if ($user_list[$i]) {
#					$user_count++;
#					$user_list[$i] = "";
#				}
#			}

			print qq|<p>$btitle 作：$bmaker $bdate</p>|;
			print qq|<p>このあみだくじは終了しています</p>|	if $bcmp;
			print qq|<span>くじの本数：$bcount</span><br>|;
			print qq|<span>賞品リスト：$bitems</span><br>|;
			print qq|<span>現在の参加者：$bscount人</span><br><br>|;

			my @suser_list = split /,/, $bsusers;
			my @sitem_list = split /,/, $bsitems;

			print "<table>";
				for (my $i = 0; $i < $bcount; $i++) {
					print "<tr><td>".($i+1).".";
					print qq|$user_list[$i]| if $user_list[$i];
					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">このくじにする</a>|	unless $user_list[$i] || $bcmp;
					print "</td><td>－あみだ線は省略－</td>";
					print "<td>$suser_list[$i]</td>"	if $bcmp;
					print "<td>$sitem_list[$i]</td>"	if $bcmp;
					print "</tr>";
				}
#			if ($bcmp) {
#				# 参加者が埋まったか公開フラグが立ったイコールくじ公開
#				for (my $i = 0; $i < $bcount; $i++) {
#					print "<tr><td>".($i+1).".";
#					print qq|$user_list[$i]|;
#					print "</td><td>－あみだ線は省略－</td>";
#					print "<td>$suser_list[$i]</td>";
#					print "<td>$sitem_list[$i]</td>";
#					print "</tr>";
#				}
#			}
#			else {
#				for (my $i = 0; $i < $bcount; $i++) {
#					print "<tr><td>".($i+1).".";
#					print qq|$user_list[$i]|	if $user_list[$i];
#					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">このくじにする</a>|	unless $user_list[$i];
#					print "</td><td>－あみだ線は省略－</td>";
#					print "</tr>";
#				}
#			}
			print "</table>";
		} # while (my $line = <$fh>)
	}
	else {
		print "<ul>";
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

#			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp, $susers, $sitems) = split /<>/, $line;
#			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $busers, $bcmp) = split /<>/, $line;

			if ($bcmp) { print "<li>[公開済]"; } else { print "<li>[募集中]"; } 
			print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime">$btitle</a> $bmaker作 $bdate|;
			if (!$bcmp && $in{login_name} eq $bmaker) {
				print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime&step=3&cmp=1">公開する</a>|;
			}
			print qq|</li>|;
		}
		print "</ul>";
	}
	close $fh;
}

sub create_user_list {
	my @user_list = split /,/, $busers;
	for (my $i = 0; $i < $bcount; $i++) {
		$user_list[$i] = ""	unless $user_list[$i]; # 人数分だけ配列を拡張
	}
}

sub is_entry {
	my ($name, @users) = @_;
	for (my $i = 0; $i < @users; $i++) {
		return 1	if ($name eq $users[$i]);
	}
	return 0;
}