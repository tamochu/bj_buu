#================================================
# ﾁﾝﾁﾛﾘﾝ
#================================================
require './lib/_casino_funcs.cgi';

$header_size = 1; # ﾁﾝﾁﾛﾘﾝ用のﾍｯﾀﾞｰｻｲｽﾞ 親
($_leader) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ
$coin_lack = 1; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 2; # 最低2人
$max_entry = 32; # 最高32人

sub run {
	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @participants = &get_members($head[$_participants]);

	if ($head[$_state]) {
		print qq|親:$head[$_leader] 賭け上限:$head[$_rate]|;
	}
	else {
		print qq|親:$participants[0] 賭け上限:|;
		my @participants_datas = split /;/, $head[$_participants_datas];
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
#			my $name = pack 'H*', $datas[0];
			print $datas[2] if $datas[0] eq $participants[0];
		}
	}
}
#sub show_start_info { } # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants_datas], $head[$_leader]); # ｹﾞｰﾑに参加している
}
sub show_tale_info { # 定義してなくても動作に問題ない
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&show_status($head[$_participants_datas]) if $head[$_participants];
}

#================================================
# 参加するﾌｫｰﾑ
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "参加する" : "親になる";
	# ｶｼﾞﾉ毎の処理
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="bet" class="text_box_b" value="$m{coin}"> ｺｲﾝ |;
	print &create_submit("participate", "$button");
	print qq|</form>|;
}

#================================================
# 参加する処理 ﾚｰﾄのためのﾜﾝｸｯｼｮﾝ
#================================================
sub participate {
	$in{bet} ||= 0;
	return '数字を入れてください' unless $in{bet} !~ /[^0-9]/;
	$in{bet} = $m{coin} if $m{coin} < $in{bet};
#	$in{bet} = int($m{coin} / 10) if $m{coin} < $in{bet};
#	$in{bet} = int($m{coin} / 10) if int($m{coin} / 10) < $in{bet};
	
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	close $fh;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	$in{bet} = $head[$_rate] if $head[$_rate] && $head[$_rate] < $in{bet};
	&_participate($in{bet}, '', $in{bet});
}

#================================================
# 開始する処理 実際のファイル操作は _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);
	my $is_start = 0;

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_leader]) = (1, 1, $time, $participants[0]);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			$head[$_rate] = $mstock if $mname eq $head[$_leader];

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	$$head_line = &h_to_s(@head);
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants_datas, $leader) = @_;

	my $diced_num = 0;
	my @participants_datas = split /;/, $participants_datas;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		$diced_num++ if $datas[1] ne '';
	}

	if ( 1 < $m_turn && $m_turn < 5 && ($leader ne $m{name} || $diced_num == (@participants_datas-1)) ) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("play", "ｻｲｺﾛを振る");
		print qq|</form>|;
	}
	else { print qq|<br>| }
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	my @members = ();
	my ($result_mes, $result_mes2) = ('', '');
	my $is_play = 0;
	my ($m_value, $m_stock) = (0, 0);
	my @participants_datas = ();
	my $tmp_leader = '';

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = split /,/, $head[$_participants];
	my $diced_num = 0;
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		$diced_num++ if $datas[1] ne '';
	}

	my $is_my_turn = $head[$_state] && 1 < $m{c_turn} && $m{c_turn} < 5 && ($leader ne $m{name} || $diced_num == (@participants_datas-1)); # 開始しているｹﾞｰﾑに参加していて自分のﾀｰﾝ ﾁﾝﾁﾛﾘﾝはｻｲｺﾛの振れる数も含む 2 + 3
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			($head[$_lastupdate], $mtime) = ($time, $time);

			# ｶｼﾞﾉ毎の処理
			if (5 <= $m{c_turn}) { $result_mes = 'もう振れません'; } # ｻｲｺﾛ振る度にﾀｰﾝ数+1 2 を 0 とし 3 個ｻｲｺﾛ振るので 5
			else {
				$is_play = 1;
				my @d_set = ();
				$d_set[$_] = int(rand(6)+1) for (0 .. 2);
				@d_set = sort {$a <=> $b} @d_set;
				if ($d_set[0] == $d_set[1]) {
					$mvalue = $d_set[2];
					if ($d_set[1] == $d_set[2]) {
						$mvalue += 10;
						$mvalue += 10 if $d_set[2] == 1;
					}
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[1] == $d_set[2]) {
					$mvalue = $d_set[0];
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[2] == 3) {
					$mvalue = -1;
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[0] == 4) {
					$mvalue = 7;
					$mturn = $m{c_turn} = 5;
				}
				else {
					$mturn++;
					$m{c_turn} = $mturn;
					$mvalue = 0 if $mturn == 5;
				}
				my $n = $mturn - 2;
				if (5 <= $mturn && $m{name} eq $head[$_leader]) { # 親ﾗｽﾄ
					$n = '親ラスト';
					($m_value, $m_stock) = ($mvalue, $mstock);
					@participants_datas = split /;/, $head[$_participants_datas];
					$tmp_leader = $head[$_leader];
					&init_header(\@head);
				}
				else {
					$n = $n == 3 ? 'ラスト' : $n . ' 投目';
				}
				$result_mes = "$n $d_set[0],$d_set[1],$d_set[2]";
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	if ($is_play && $m{name} eq $tmp_leader && $m{c_turn} == 5) {
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_play) {
		if ($m{name} eq $tmp_leader && $m{c_turn} == 5) {
			my $total = 0;
			my %p_players = ();
			for my $i (0 .. $#participants_datas) {
				my @datas = split /:/, $participants_datas[$i];
#				&system_comment("$datas[0]");
				next if $datas[0] eq '';
				next if $datas[0] eq $tmp_leader;
				my $v = 0;
				if ($m_value < $datas[1]) {
					$v = $datas[2];
					$v *= $m_value == -1 ? 2 : 1;
					$v *= $datas[1] == 21 ? 5 :
					10 < $datas[1] ? 3 :
					$datas[1] == 7 ? 2 : 1;
				}
				elsif ($datas[1] < $m_value) {
					$v = $datas[2] * -1;
					$v *= $datas[1] == -1 ? 2 : 1;
					$v *= $m_value == 21 ? 5 :
					10 < $m_value ? 3 :
					$m_value == 7 ? 2 : 1;
				}
				$v = &coin_move($v, $datas[0], 1);
#				&system_comment("おそらく試しの1回目");
				&coin_move(-1 * $v, $datas[0], 1);
#				&system_comment("試した分のチャラ");
				$total -= $v;
				$p_players{$datas[0]} = $v;
				&regist_you_data($datas[0], 'c_turn', '0');
				if (0 < $v) {
					$result_mes2 .= "<br>$datas[0] は $v ｺｲﾝ 勝ちました[".&get_yaku_name($datas[1])."]";
				}
				elsif ($v < 0) {
					$v *= -1;
					$result_mes2 .= "<br>$datas[0] は $v ｺｲﾝ 負けました[".&get_yaku_name($datas[1])."]";
				}
				else {
					$result_mes2 .= "<br>$datas[0] は分けです[".&get_yaku_name($datas[1])."]";
				}
			}

			my $p_rate = 1.0;
			if ($m{coin} < -1 * $total) {
				$p_rate = $m{coin} / (-1 * $total);
#				&system_comment("$m{name} 内部的負けｺｲﾝ数 $m{coin} / (-1 * $total) = $p_rate");
			}
			for my $mn (keys(%p_players)) {
				my $v = int($p_players{$mn} * $p_rate);
				&coin_move($v, $mn, 1);
#				&system_comment("$mn 内部的勝ちｺｲﾝ数 $p_players{$mn} * $p_rate = $v");
			}
			&coin_move($total, $m{name}, 1);
#			&system_comment("$m{name} 内部的負けｺｲﾝ数その2 $total");
			if (0 < $total) {
				$result_mes .= "<br>$m{name} は $total ｺｲﾝ の浮きです[".&get_yaku_name($m_value)."]";
			}
			elsif ($total < 0) {
				$total *= -1;
				$result_mes .= "<br>$m{name} は $total ｺｲﾝ の沈みです[".&get_yaku_name($m_value)."]";
			}
			else {
				$result_mes .= "<br>$m{name} は浮きなしです[".&get_yaku_name($m_value)."]";
			}
			$m{c_turn} = 0;
			&write_user;
		}
		else {
			&write_user;
		}
	}

	return "$result_mes$result_mes2"; # ﾌﾟﾚｲの報告
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
#		my $name = pack 'H*', $datas[0];
			print "$datas[0]";
			print " 出目：" . &get_yaku_name($datas[1]) if $datas[1] ne '';
			print " ﾍﾞｯﾄ：$datas[2]ｺｲﾝ";
			print "<br>" if $i != $#participants_datas;
	}
}

sub get_yaku_name {
	my $yaku = shift;
	return $yaku == -1 ? "ヒフミ" : $yaku == 0 ? "目なし" : $yaku < 7 ? $yaku : ($yaku % 10)."ゾロ";
}

1;#削除不可
