#================================================
# ﾇﾒﾛﾝ
#================================================
require './lib/_casino_funcs.cgi'; # ｺﾒﾝﾄ参照

$header_size = 0; # ﾇﾒﾛﾝ用のﾍｯﾀﾞｰｻｲｽﾞ
$coin_lack = 0; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 2; # 最低2人
$max_entry = 2; # 最高2人

sub run {
	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|賭け上限:$head[$_rate]|;
}
sub show_start_info { # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|自分の番号:$m_value<br>|;
}
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|<br>自分の番号:$m_value|;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants]) if &is_member($head[$_participants], "$m{name}"); # ｹﾞｰﾑに参加している
}

#================================================
# 参加するﾌｫｰﾑ
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "参加する" : "親になる";
	# ｶｼﾞﾉ毎の処理
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> 自分の番号<br>|;
	print qq|<input type="text"  name="bet" class="text_box_b"> 賭けるｺｲﾝ<br>| unless $leader;
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

	if ($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3) {
		my @number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		return '同じ数字は二度使えません' if $number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2];
		&_participate($in{bet}, $in{number}, '63');
	}
	else { return ("3つの異なる数字を入れてください"); }
}

#================================================
# 開始する処理 実際のファイル操作は _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ﾍｯﾀﾞｰ
	my @participants = split /,/, $head[$_participants];
	my $is_start = 0;
	# ｶｼﾞﾉ毎の処理

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		$$head_line = &h_to_s(@head);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ｶｼﾞﾉ毎の処理
			($mtime, $mturn) = ($time, 2);

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	unless (&is_my_turn($participants, $m{name})) {
		print qq|<br>相手が思考中です|;
		return;
	}

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> 番号|;
	print &create_submit('play', '番号を当てる');
	print qq|</form>|;
	return if $m_stock == 0;

	print qq|<hr><form method="$method" action="$this_script" name="form">|;
	print qq|アイテム<input type="text"  name="number" class="text_box_b"> 番号<br>|;
	print &create_radio_button('itemno', '1', 'DOUBLE 二回行動できる<br>') if int($m_stock / 32) == 1;
	print &create_radio_button('itemno', '2', 'HIGH&LOW 0～4, 5～9の位置を調べる<br>') if int($m_stock / 16) % 2 == 1;
	print &create_radio_button('itemno', '3', 'TARGET 数字の位置を調べる<br>') if int($m_stock / 8) % 2 == 1;
	print &create_radio_button('itemno', '4', 'SLASH 最大値 - 最小値を調べる<br>') if int($m_stock / 4) % 2 == 1;
	print &create_radio_button('itemno', '5', 'SHUFFLE 自分の数列を混ぜる<br>') if int($m_stock / 2) % 2 == 1;
	if ($m_stock % 2 == 1) {
		print &create_radio_button('itemno', '6', 'CHANGE ');
		for my $num (0 .. 2) {
			my $c = substr($m_value, $num, 1);
			print &create_radio_button('choicenum', $c, "$c 交換");
		}
		print '<br>';
	}
	print &create_submit('use_item', 'アイテムを使う');
	print '</form>';
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	return "3つの数字を入れてください" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3);

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name} && 2 <= $m{c_turn};
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if ($mname eq $game_members[1] && $is_my_turn) {
			($e_name, $e_value, $is_find) = ($mname, $mvalue, 1);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my $is_reset = 0;
	my $penalty_coin = 0;
	if ($is_find) {
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit イート $blow バイト";
		$head[$_lastupdate] = $time;
		if ($hit == 3) {
			$result_mes .= "勝利";
			$penalty_coin = $head[$_rate];
			$is_reset = 1;
			&init_header(\@head);
			&reset_members(\@members);
		}
		$head[$_participants] = &change_turn($head[$_participants]); # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# 終了処理
	if ($is_my_turn && $is_find && $is_reset) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
		my $cv = -1 * &coin_move(-1 * $penalty_coin, $e_name);
		&coin_move($cv, $m{name});
	}

	return $result_mes;
}

sub hb_count {
	my ($m_number, $y_number) = @_;
	my @number = (int($m_number / 100), int($m_number / 10) % 10, $m_number % 10);
	my @answer = (int($y_number / 100), int($y_number / 10) % 10, $y_number % 10);
	my ($hit, $blow) = (0, 0);
	for my $i (0..2) {
		if ($answer[$i] == $number[$i]) {
			$hit++;
		}
		else {
			my $d = 0;
			$d = $number[$_] == $number[$i] ? $d + 1 : $d for (0 .. $i - 1);
			if ($d == 0) {
				$blow = $answer[$_] == $number[$i] ? $blow + 1 : $blow for (0 .. 2);
			}
		}
	}
	return ($hit, $blow);
}

sub use_item {
	unless ($in{itemno}) { return "使うｱｲﾃﾑを選んでください"; }
	elsif ( ($in{itemno} == 1) && !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3) ) {
		return "3つの数字を入れてください";
	}
	elsif ($in{itemno} == 3) {
		return "1つの数字を入れてください" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 1);
	}
	elsif ($in{itemno} == 6) {
		return "1つの数字を入れてください" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 1);
		return "CHANGE 交換する数を選んでください" if $in{choicenum} eq '';
		return "CHANGE 1桁の数字を選んでください" if 9 < $in{number};
		return "CHANGEで変えられるのはHIGH同士かLOW同士です" if (($in{number} < 5) xor ($in{choicenum} < 5));
	}

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @members = ();
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name};
	my ($e_name, $e_value) = ('', '');
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0);
	my $my_index = -1; # @membersに格納されている自分のデータのインデックス

	my %sames = ();
	my @is_find = (0, 0); # 相手データ読み込んだか、自分データ読み込んだか
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		$my_index++ unless $is_find[1];
		if ($mname eq $game_members[1] && $is_my_turn) {
			($e_name, $e_value, $is_find[0]) = ($mname, $mvalue, 1);
		}
		elsif ($mname eq $m{name} && $is_my_turn) {
			($m_turn, $m_value, $m_stock, $is_find[1]) = ($mturn, $mvalue, $mstock, 1);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my ($is_reset, $is_double, $is_ng) = (0, 0, 0);
	my $penalty_coin = 0;
	if ($is_my_turn && $is_find[0] && $is_find[1]) {
		# DOUBLE ランダムに選ばれた自分の1桁を公開する代わりに2回コールできる
		if ($in{itemno} == 1 && int($m_stock / 32) == 1) {
			my ($hit, $blow) = &hb_count($in{number}, $e_value);
			$m_stock -= 32;
			my $open_card = int(rand(3)+1);
			$result_mes .= "DOUBLE $m{name}の$open_card枚目は" . substr($m_value, $open_card-1, 1) . "です<br>";
			$result_mes .= "$in{number}:$hit イート $blow バイト";
			if ($hit == 3) {
				$result_mes .= "勝利";
				$penalty_coin = $head[$_rate];
				&init_header(\@head);
				&reset_members(\@members);
				$is_reset = 1;
			}
			$is_double = 1;
		}
		# HIGH&LOW 相手の各桁が5以上かどうか知ることができる
		elsif ($in{itemno} == 2 && int($m_stock / 16) % 2 == 1) {
			$m_stock -= 16;
			my @hl = ();
			$hl[$_] = 5 <= substr($e_value, $_, 1) ? 'high' : 'low' for (0 .. 2); # 3桁の数字を1桁ずつ走査
			$result_mes = "HIGH&LOW $hl[0],$hl[1],$hl[2]";
		}
		# TARGET 指定した値が相手の何桁目にあるのか知ることができる
		elsif ($in{itemno} == 3 && int($m_stock / 8) % 2 == 1) {
			$m_stock -= 8;
			my ($target_num, $target_place) = ($in{number} % 10, 'ありません');
			$target_place = $target_num == substr($e_value, $_, 1) ? ($_ + 1)."枚目です" : $target_place for (0 .. 2); # 3桁の数字を1桁ずつ走査
			$result_mes .= "TARGET $target_numは$target_place";
		}
		# SLASH 相手の手持ちの数字の最大値から最小値を引いた数を知ることができる
		elsif ($in{itemno} == 4 && int($m_stock / 4) % 2 == 1) {
			$m_stock -= 4;
			my @mm = ();
			$mm[$_] = substr($e_value, $_, 1) for (0 .. 2); # 3桁の数字を配列に変換
			my ($e_max, $e_min) = ($mm[0], $mm[1]);
			for my $i (0 .. 2) {
				$e_max = $mm[$i] if $e_max < $mm[$i];
				$e_min = $mm[$i] if $mm[$i] < $e_min;
			}
			$result_mes = "SLASH ".($e_max - $e_min);
		}
		# SHUFFLE 自分の数字をシャッフルする
		elsif ($in{itemno} == 5 && int($m_stock / 2) % 2 == 1) {
			$m_stock -= 2;
			$result_mes = "SHUFFLE";
			my @num_arr = ();
			$num_arr[$_] = substr($m_value, $_, 1) for (0 .. 2); # 3桁の数字を配列に変換
			for my $i (0 .. 2) {
				my $j = int(rand($i + 1)); # 周回する度に乱数範囲を広げる 1周目:0～0 2周目:0～1 3周目:0～2
				my $tmp_n = $num_arr[$j]; # ただのスワップ
				$num_arr[$j] = $num_arr[$i];
				$num_arr[$i] = $tmp_n;
			}
			$m_value = "$num_arr[0]$num_arr[1]$num_arr[2]";
		}
		# CHANGE 自分の番号の1桁をHIGH・LOW同士で新しい数字に交換
		elsif ($in{itemno} == 6 && $m_stock % 2 == 1) {
			$m_stock -= 1;
			my $index = index($m_value, $in{choicenum});
			my $old_num = substr($m_value, $index, 1);
			if ($index == -1) {
				$result_mes = "CHANGE 交換する数を選んでください";
				$is_ng = 1;
			}
			elsif (($in{number} < 5) xor ($old_num < 5)) {
				$result_mes = "CHANGE 変えられるのはHIGH同士かLOW同士です";
				$is_ng = 1;
			}
			elsif ($old_num eq $in{number}) {
				$result_mes = "CHANGE 交換前と交換後の数字が同じです";
				$is_ng = 1;
			}
			elsif (-1 < index($m_value, $in{number})) {
				$result_mes = "CHANGE 重複しない数字を選んでください";
				$is_ng = 1;
			}
			else {
				my $diff_hl = 5 <= $old_num ? 'high' : 'low';
				substr($m_value, $index, 1, $in{number});
				$result_mes = "CHANGE $m{name}の".($index + 1)."枚目は$diff_hlです";
			}
		}
	}

	if ($is_my_turn && $result_mes && !$is_ng && !$is_reset) {
		splice(@members, $my_index, 1, "$time<>$m{name}<>$addr<>$m_turn<>$m_value<>$m_stock<>\n");
		$head[$_lastupdate] = $time;
		$head[$_participants] = &change_turn($head[$_participants]) if $is_find[0] && $is_find[1] && !$is_double; # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# 終了処理
	if ($is_my_turn && $is_reset) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
		my $cv = -1 * &coin_move(-1 * $penalty_coin, $e_name);
		&coin_move($cv, $m{name});
	}

	return $result_mes;
}

1;#削除不可