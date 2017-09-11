#================================================
# ﾀﾞｳﾄ
#================================================
require './lib/_casino_funcs.cgi'; # ｺﾒﾝﾄ参照

$header_size = 2; # ﾀﾞｳﾄ用のﾍｯﾀﾞｰｻｲｽﾞ ﾀｰﾝ、場札
($_turn, $_field_cards) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ
$coin_lack = 0; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 4; # 最低4人
$max_entry = 11; # 最高11人

my @rates = (0, 100, 1000, 3000, 10000, 30000);

my @nums = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K');
my @suits = ('ｽﾍﾟｰﾄﾞ', 'ﾊｰﾄ', 'ｸﾗﾌﾞ', 'ﾀﾞｲﾔ');

sub run {
	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|ﾚｰﾄ:$head[$_rate]|;
}
#sub show_start_info { } # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @field_card = split /,/, $head[$_field_cards];
	my $field_card_num = @field_card;
	print qq|<br>場札：$field_card_num枚|;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_field_cards]) if &is_member($head[$_participants], "$m{name}"); # ｹﾞｰﾑに参加している
	&show_members_hand($head[$_participants_datas]);
}

#================================================
# 参加するﾌｫｰﾑ
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "参加する" : "親になる";
	# ｶｼﾞﾉ毎の処理
	print qq|<form method="$method" action="$this_script" name="form">|;
	print "レート：".&create_select_menu("rate", 0, @rates) unless $leader;
	print &create_submit("participate", "$button");
	print qq|</form>|;
}

#================================================
# 参加する処理 ﾚｰﾄのためのﾜﾝｸｯｼｮﾝ
#================================================
sub participate {
	&_participate($rates[$in{rate}], '', '');
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
	my @cards;

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_turn], $head[$_field_cards]) = (1, 1, $time, 0, '');
		$$head_line = &h_to_s(@head);
		# ｶｼﾞﾉ毎の処理
		my $deck_n = @participants < 8 ? 1 : 2; # 8人以上からﾃﾞｯｸ2個
		my @deck = &shuffled_deck($deck_n);
		my $i = 0;
		while (@deck) {
			push @{$cards[$i]}, shift @deck;
			$i = $#participants <= $i ? 0 : $i + 1;
		}
	}
	my $c = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ｶｼﾞﾉ毎の処理
			@{$cards[$c]} = sort { $a <=> $b } @{$cards[$c]};
			($mtime, $mturn, $mvalue, $mstock) = ($time, 2, '', join(",", @{$cards[$c]}));
			$c++;

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $field_cards) = @_;
	my @hand_cards = split /,/, $m_stock;
	my @participants = &get_members($participants);

	my @cards = ();
	if ($participants[0] eq $m{name}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "手札：".@hand_cards."枚 ".&create_select_menu("card", 0, @cards);
		print &create_submit("play", "ｶｰﾄﾞを出す");
		print qq|</form>|;
	}
	else {
		print qq|<br>$participants[0]が思考中です<br>|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "手札：".@hand_cards."枚 ".&create_select_menu("card", 0, @cards);
		print "<br>";
	}

	if ($field_cards && $participants[-1] ne $m{name}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("doubt", "ﾀﾞｳﾄ");
		print qq|</form>|;
	}
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	my @members = ();
	my $result_mes = '';
	my $winner = '';
	my @lose_members = ();
	my $penalty_coin = 0;

	# ｶｼﾞﾉ毎の処理
	my $play_card;

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = split /,/, $head[$_participants];
	my $is_my_turn = $head[$_state] && &is_my_turn($head[$_participants], $m{name}) && 2 <= $m{c_turn}; # 開始しているｹﾞｰﾑに参加していて自分のﾀｰﾝ
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			$head[$_lastupdate] = $time;
			$mtime = $time;

			# ｶｼﾞﾉ毎の処理
			my @hand_cards = split /,/, $mstock;
			$play_card = splice(@hand_cards, $in{card}, 1);
			$head[$_field_cards] .= "$play_card,";
			my $num = $head[$_turn] % 13;
			$head[$_turn]++;
			$result_mes = "$nums[$num]のｶｰﾄﾞを出しました";
			$mstock = join(",", @hand_cards);
			unless ($mstock) {
				$winner = $mname;
				@lose_members = &get_members($head[$_participants]);
				$penalty_coin = $rate;
				$result_mes .= "<br>手札がなくなった$mnameの勝ちです";
				&init_header(\@head);
				&reset_members(\@members);
			}
			else {
				$head[$_participants] = &change_turn($head[$_participants]); # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($winner) {
		my $cv = 0;
		for my $loser (@lose_members) {
			if ($loser ne $winner) {
				&regist_you_data($loser, 'c_turn', '0');
				$cv += -1 * &coin_move(-1 * $penalty_coin, $loser);
			}
		}
		&coin_move($cv, $winner);
		$m{c_turn} = 0;
		&write_user;
	}

	return $result_mes; # ﾌﾟﾚｲの報告
}

sub doubt {
	my @members = ();
	my $result_mes = '';

	# ｶｼﾞﾉ毎の処理
	my $play_card;
	my $is_doubt = 0;
	my $target_player;

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]); # idとｺﾝﾏの文字列を名前の配列に変換
	my @field_cards = split /,/, $head[$_field_cards];
	if (@field_cards) {
		$is_doubt = 1;
		$head[$_field_cards] = '';
		my $card_num = $nums[($head[$_turn] - 1) % 13];
		my @top_card = &get_card($field_cards[-1]);

		if ($card_num eq $nums[$top_card[0]]) {
			$result_mes = "DOUBT失敗！";
			$target_player = $m{name};
		}
		else {
			$result_mes = "DOUBT成功！";
			$target_player = $participants[-1];
		}
		$result_mes .= " $participants[-1]の出したｶｰﾄﾞは$suits[$top_card[1]]の$nums[$top_card[0]]です";
	}

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_doubt && $mname eq $target_player) {
			my @hand_cards = split /,/, $mstock;
			push @hand_cards, @field_cards;
			@hand_cards = sort { $a <=> $b } @hand_cards;
			$mstock = join(",", @hand_cards);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return $result_mes;
}

sub show_members_hand {
	my $participants_datas = shift;

	my @participants_datas = split /;/, $participants_datas;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		my @hand_cards = split /,/, $datas[2];
#		my $name = pack 'H*', $datas[0];
		my $size = @hand_cards;
		print "$datas[0]：$size枚 ";
		print "<br>" if ($i+1) % 4 == 0;
	}
}

sub shuffled_deck {
	my $deck_n = shift; # ﾃﾞｯｸ数
	my $size = $deck_n * 52 - 1; # ｶｰﾄﾞ枚数
	my @deck;

	@deck[$_] = $_+1 for (0 .. $size);
	for my $i (0 .. $size) {
		my $j = int(rand($i + 1)); # 周回する度に乱数範囲を広げる
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}

sub get_card {
	my $card = shift;
	my $num = ($card-1) % 13; # 1～52 の値から -1 したものを 13 で割った余りが 0～12 になる
	my $suit = int(($card-1)/13); # 0ｽﾍﾟｰﾄﾞ 1ﾊｰﾄ 2ｸﾗﾌﾞ 3ﾀﾞｲﾔ
	return ($num, $suit);
}

1;#削除不可