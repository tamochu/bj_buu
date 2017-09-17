#================================================
# 大貧民
#================================================
=pod
ブオーン[★★ｴﾆｯｷﾏｽﾀｰ]：ほとんど読めねーですけどざーっと流れ追った感じ、確かに参加する周りが怪しそう (海底都市ﾙﾙｲｴ : 9/1 23:19)
ブオーン[★★ｴﾆｯｷﾏｽﾀｰ]：思い付いたこと3 人数多いと後ろの方のプレイヤーに10分放置がかかる？(ねーか？) (海底都市ﾙﾙｲｴ : 9/1 23:15)
ブオーン[★★ｴﾆｯｷﾏｽﾀｰ]：思い付いたこと2 中断されたプレイの10分放置でリセットかかってないか (海底都市ﾙﾙｲｴ : 9/1 23:13)
ブオーン[★★ｴﾆｯｷﾏｽﾀｰ]：思い付いたこと1 プレイ中に未参加者が親になるボタン押したときのメンバーファイル操作 (海底都市ﾙﾙｲｴ : 9/1 23:12)
1<>1504707895<>ブオーン,ムラビトＮ,ムクガイヤ,すこ,<>ムラビトＮ:0:32,8;ムクガイヤ:0:15,41,43,34,36,37;すこ:1:27,5,31,44,10,23,49,11,26,53;<>0<>ムクガイヤ<>16<><><>2<>1<><>

play card get
game data open
pass or play check
pass
field refresh check
turn change1
turn change2
header 1<>1504793392<>ぶぶお,すこ,ｱﾙﾋﾞｽ,ムラビトＮ,su-,<>ｱﾙﾋﾞｽ:1:3,29,17,19,20,47,9,36,54;ムラビトＮ:0:16,18,11;su-:1:15,8,13,53;ぶぶお:0:1,42,43,31,45,46,10,12,38;すこ:1:2,41,32,37,25,39;<>0<>su-<><><><><><><> 
=cut

require './lib/_casino_funcs.cgi';

$header_size = 7; # 大貧民用のﾍｯﾀﾞｰｻｲｽﾞ 親、場のｶｰﾄﾞ、勝者、複数出し・階段の縛り、スート縛り、革命、イレバ
($_leader, $_field_card, $_winner, $_bind_m, $_bind_s, $_revo, $_back) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ
$coin_lack = 0; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 2; # 最低2人
$max_entry = 8; # 最高8人

my @nums = ('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'Jo'); # 低い順
my @suits = $is_mobile ? ('S', 'H', 'C', 'D', '') : ('&#9824;', '&#9825;', '&#9827;', '&#9826;', '');

my @rates = (0, 100, 1000, 3000, 10000, 30000);

sub run {

	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|親:$head[$_leader] ﾚｰﾄ:$head[$_rate]|;
}
#sub show_start_info { } # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @members = &get_members($head[$_participants]);
	my @winners = &get_members($head[$_winner]);
	print "<br>";
	for my $i (1 .. @members) {
		print "$i位 $winners[$i-1],";
	}
	&show_status(@head);
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_field_card], $head[$_winner]) if &is_member($head[$_participants], "$m{name}"); # ｹﾞｰﾑに参加している
}
#sub show_tale_info { # 定義してなくても動作に問題ない
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#	&show_status($head[$_participants_datas]) if $head[$_participants];
#}

=pod
#================================================
# 親になるﾌｫｰﾑ
#================================================
sub participants_form {
	# ｶｼﾞﾉ毎の処理
	print qq|<form method="$method" action="$this_script" name="form">|;
	print "レート：".&create_select_menu("rate", @rates);
	print &create_submit("leader", "親になる");
	print qq|</form>|;
}

#================================================
# 親になる処理
#================================================
sub leader {
	&_participate(0, 0, '');
}
=cut
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
	&_participate($rates[$in{rate}], 0, '');
}

#================================================
# 開始する処理 実際のファイル操作は _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);
	my $is_start = 0;
	# ｶｼﾞﾉ毎の処理
	my @cards;
	my $leader_i = 0; # ﾀﾞｲﾔの3を持っている参加者のｲﾝﾃﾞｯｸｽ

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_field_card]) = (1, 1, $time, '');
		# ｶｼﾞﾉ毎の処理
		my $size = @participants;
		my @deck = &shuffled_deck($size);
		my $i = 0;
		while (@deck) {
			my $c = shift @deck;
			$leader_i = $i if $c == 40; # ﾀﾞｲﾔの3
			push @{$cards[$i]}, $c;
			$i = $#participants <= $i ? 0 : $i + 1;
		}
	}
	my $c = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ｶｼﾞﾉ毎の処理
			@{$cards[$c]} = sort { $a <=> $b } @{$cards[$c]};
			${"card_$_"} = '' for (0 .. 13);
			for my $i (0 .. $#{$cards[$c]}) {
				my $j = ${$cards[$c]}[$i];
				if ($j == 53 || $j == 54) { # ｶｰﾄﾞをﾗﾝｸ順にｿｰﾄ ﾗﾝｸ毎に変数に格納し最後に1つに結合
					${"card_13"} .= "$j,";
				}
				else {
					${"card_".($j-1)%13} .= "$j,";
				}
			}
			$mstock .= ${"card_$_"} for (0 .. 13); # 1つに結合
			($mtime, $mturn) = ($time, 2);
			if ($leader_i == $c) { # ﾀﾞｲﾔの3を持っている参加者を一番に移動
				$head[$_leader] = $mname;
			}
			$c++;

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	$head[$_participants] = &change_turn($head[$_participants]) for (0 .. $leader_i-1);

	$$head_line = &h_to_s(@head);
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $field_cards, $pass) = @_;
	my @hand_cards = split /,/, $m_stock;
	my @participants = &get_members($participants);

	if ($participants[0] eq $m{name}) {
		my $is_joker = 0;
		print "<br>手札：".@hand_cards."枚<br>";
		print qq|<form method="$method" action="$this_script" name="form">|;
		unless (0 < $m_value && 0 < $pass) {
			for my $hand_card (@hand_cards) {
				my ($num, $suit) = &get_card($hand_card);
				$is_joker = 1 if $num == 13;
				print &create_check_box("card_$hand_card", "$hand_card", "$suits[$suit]$nums[$num] を出す<br>");
			}
			if ($field_cards eq '' && $is_joker) { # 場札がなく、手札にｼﾞｮｰｶｰがあるとき
				print &create_radio_button('joker', 1, '複数枚出し');
				print ' ';
				print &create_radio_button('joker', 2, '階段出し<br>');
			}
		}
		print &create_submit("play", "ｶｰﾄﾞを出す");
		print qq|</form>|;
	}
	else {
		my @cards = ();
		print qq|<br>$participants[0]が思考中です<br>|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "手札：".@hand_cards."枚 ".&create_select_menu("card", 0, @cards);
		print "<br>";
	}
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	my @members = ();
	my $result_mes = '';
	my $winner = '';
	my $is_reset = 0;

	# ｶｼﾞﾉ毎の処理
	$mes .= "play card get<br>";
	my @play_cards = ();
	my $is_joker = 0;
	for my $i (1 .. 54) {
		if ($in{"card_$i"}) {
			$is_joker++ if $i == 53 || $i == 54;
			push @play_cards, $in{"card_$i"} ;
		}
	}

	# 謎の強制終了時 ﾌｧｲﾙｵｰﾌﾟﾝから while ﾙｰﾌﾟの間がゴッソリ抜けてる
	# 同時書き込みでファイルが壊れたとかファイルの中身を読み取れなかったか？
	# でもこの程度でそんなことになるなら国ファイルもっとヤバいはず
	# play card get game data open field refresh check header <><><><><><><><><><><><>

	my ($is_playable, $play_mes, $is_sequence, $is_double) = (0, '', 0, 0);
	my $is_pass = 0;
	my ($is_eight_cut, $is_s3_cut, $is_pass_cut) = (0, 0, 0);

	$mes .= "game data open<br>";
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);
	my @winners = &get_members($head[$_winner]);
	my %pass_datas = (); # 参加者のパス情報を持つ
	my $is_my_turn = $head[$_state] && $participants[0] eq $m{name} && 2 <= $m{c_turn}; # 開始しているｹﾞｰﾑに参加していて自分のﾀｰﾝ
	while (my $line = <$fh>) { # 全ﾌﾟﾚｲﾔｰﾃﾞｰﾀを上から走査
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			$head[$_lastupdate] = $time;
			$mtime = $time;

			$mes .= "pass or play check<br>";
			unless (@play_cards) { # パス
				$mes .= "pass<br>";
				$mvalue = 1;
				$is_pass = 1;
			}
			else { # カードを出している
				$mes .= "play card check<br>";
				# 出したｶｰﾄﾞすべてが手札にあるか 八切りなどﾀｰﾝを変更しないｶｰﾄﾞを出して「戻る」をし、再度今出した八切りなどﾀｰﾝを変更しないｶｰﾄﾞを再度出せる（同じｶｰﾄﾞを延々出せるだけで実害はない）
				my $eq_num = 0;
				my @hand_cards = split /,/, $mstock;
				for my $hand_card (@hand_cards) {
					for my $play_card (@play_cards) {
						$eq_num ++ if $hand_card == $play_card;
					}
				}
				unless ($eq_num == @play_cards) { # 出したｶｰﾄﾞが手札になかったらスルー
					$mes .= '<p>不正処理 手札にないｶｰﾄﾞを出そうとしています</p>';
#					$pass_datas{$mname} = $mvalue if 1 < $mturn; # 参加者のﾊﾟｽ情報の取得
#					$is_reset++ if 1 < $mturn && 1 < $mvalue;
					push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
					next;
				}

				my $play_cards = join(",", @play_cards);

				# 出したカードがﾙｰﾙに則っているか
				$mes .= "playable check<br>";
				($is_playable, $result_mes, $is_sequence, $is_double) = &is_playable($play_cards, $head[$_field_card], $head[$_bind_m], $head[$_bind_s], $head[$_revo]);

				$mes .= "joker check<br>";
				# ｼﾞｮｰｶｰを含む2枚以上のｶｰﾄﾞ
				if ($head[$_field_card] eq '' && 1 < @play_cards && $is_joker) {
					$is_joker = $in{joker}; # 1 複数枚出し 2 階段出し
					unless ($is_joker) {
						$mes .= '<p>ﾙｰﾙ違反 ｼﾞｮｰｶｰを出すときは役を宣言してください</p>';
						($is_playable, $result_mes) = (0, '');
					}
				}

				if ($is_playable) { # 出したｶｰﾄﾞがﾙｰﾙ上認められている
					$mes .= "playable ok<br>";

					$mes .= "multi or sequence check<br>";
					# 複数枚出し・階段出しの縛り設定
					if ($head[$_field_card] eq '' && 1 < @play_cards) { # 初手にのみ複数枚などの縛り発生
						if ($is_joker) {
							$mes .= "is_joker $is_joker is_sequence $is_sequence is_double $is_double";
							$head[$_bind_m] = $is_joker; # 1 複数枚出し 2 階段出し
						}
						else {
							$head[$_bind_m] = 1 if $is_double; # 複数枚出し;
							$head[$_bind_m] = 2 if $is_sequence; # 階段出し
						}
					}

					$mes .= "revolution check<br>";
					# 革命設定 複数枚出しで革命 階段では発生しない
 					if (3 < @play_cards && $head[$_bind_m] == 1 && !$is_sequence) {
						$head[$_revo] = !$head[$_revo];
						$result_mes .= '<br>革命を起こしました';
					}

					$mes .= "suit check<br>";
					# ｽｰﾄ縛りの設定 ｼﾞｮｰｶｰが含まれていない場札があり、出したｶｰﾄﾞにもｼﾞｮｰｶｰが含まれていないなら縛りﾁｪｯｸ
					if ($head[$_bind_s] eq '' && $head[$_field_card] && $head[$_field_card] !~ /53/ && $head[$_field_card] !~ /54/ && $is_joker == 0) {
						my $is_suit_lock = 1;
						my @suit_lock = ();
						my @field_cards = split /,/, $head[$_field_card];
						for my $i (0 .. $#play_cards) { # 出したｶｰﾄﾞと場のｶｰﾄﾞすべてを走査 出したｶｰﾄﾞと場札の数は同じ
							my @suit = ( (&get_card($play_cards[$i]))[1], (&get_card($field_cards[$i]))[1] );
							if ($suit[0] == $suit[1]) { # 出したｶｰﾄﾞと場のｶｰﾄﾞのｽｰﾄが同じ
								$suit_lock[$suit[0]] = 1;
							}
							else {
								$is_suit_lock = 0;
								last; # ｽｰﾄが違う時点でﾛｯｸされないことが確定
							}
						}
						if ($is_suit_lock) {
							$head[$_bind_s] = 0; # 初期化
							$head[$_bind_s] |= $suit_lock[$_] << $_ for (0 .. 3);
							$result_mes .= '<br>ｽｰﾄ縛りが発生しました';
						}
					}

					$mes .= "eight cut check<br>";
					# 八切り
					if ($head[$_bind_m] != 2 || $is_double && !$is_sequence) {
						for my $play_card (@play_cards) {
							unless ($play_card == 53 || $play_card == 54) {
								$is_eight_cut = 1 if ($play_card-1) % 13 == 5; # 1～52 の値から -1 したものを 13 で割った余りが 0～12 になる
							}
						}
					}

					$mes .= "s3 check<br>";
					# スペ3返し
					$is_s3_cut = 1 if (@play_cards == 1 && $play_cards[0] == 1 && ($head[$_field_card] == 53 || $head[$_field_card] == 54));

					$mes .= "new hand create<br>";
					my @new_hand_cards = ();
					for my $hand_card (@hand_cards) {
						my $is_eq = 0;
						for my $play_card (@play_cards) {
							if ($hand_card == $play_card) {
								$is_eq = 1;
								last;
							}
						}
						push @new_hand_cards, $hand_card unless $is_eq;
					}
					$mvalue = 0;
					$mstock = join(",", @new_hand_cards);
					$head[$_field_card] = $play_cards;

					$mes .= "win check<br>";
					unless ($mstock) {
						my $is_find = 0;
						if ($is_eight_cut || # 八切り上がり
							$is_s3_cut || # ｽﾍﾟ3返し上がり
							($is_double && (($head[$_field_card]-1) % 13) == 0) || # 革命中の ﾏﾙﾁ3 か
							($is_double && (($head[$_field_card]-1) % 13) == 12) || # 非革命中の ﾏﾙﾁ2 か
							(@play_cards == 1 && ( # 出したｶｰﾄﾞが1枚かつ
							($head[$_revo] && (($head[$_field_card]-1) % 13) == 0) || # 革命中の 3 か
							(!$head[$_revo] && (($head[$_field_card]-1) % 13) == 12) || # 非革命中の 2 か
							$head[$_field_card] eq '53' || $head[$_field_card] eq '54') ) ) { # ｼﾞｮｰｶｰ
							$mes .= "taboo win<br>";
							for my $i (0 .. @participants-1) {
								unless ($winners[$#participants-$i] || $is_find) {
									$winners[$#participants-$i] = $m{name};
									$is_find = 1;
								}
							}
							$result_mes .= "<br>禁止上がり";
							$is_eight_cut = $is_s3_cut = 0;
						}
						else {
							$mes .= "win<br>";
							for my $i (0 .. $#participants) {
								unless ($winners[$i] || $is_find) {
									$winners[$i] = $m{name};
									$is_find = 1;
								}
							}
							$result_mes .= "<br>上がり";
						}
						$head[$_winner] = join(",", @winners);
						$winner = $m{name};
						$mvalue = 2;
					}
				}
			}
		}
		if ($is_my_turn) {
			$pass_datas{$mname} = $mvalue if 1 < $mturn; # 参加者のﾊﾟｽ情報の取得
			$is_reset++ if 1 < $mturn && 1 < $mvalue; # 参加者かつ上がり
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	$mes .= "field refresh check<br>";
	if ($is_my_turn && ($is_playable || $is_pass || $is_eight_cut || $is_s3_cut)) {
		my $pass_num = 0;
		my @next_num = (0, 0);
		my $refresh_num = 0;
		my $is_find = 0;
		unless ($is_eight_cut || $is_s3_cut) {
			$mes .= "turn change1<br>";
			for my $i (0 .. $#participants) {
				if ($next_num[0] == 0 && $participants[$i] ne $m{name} && $pass_datas{$participants[$i]} == 0) { # ﾊﾟｽをしていない直近のﾌﾟﾚｲﾔｰ
					$next_num[0] = $i;
					$is_find = 1; # ﾊﾟｽをしていないﾌﾟﾚｲﾔｰが見つかった
				}
				elsif ($pass_datas{$participants[$i]} == 1) { # ﾊﾟｽをしているﾌﾟﾚｲﾔｰ
					$next_num[1] = $i if $next_num[1] == 0 && $participants[$i] ne $m{name}; # ﾊﾟｽをしている直近のﾌﾟﾚｲﾔｰ
					$pass_num++;
				}
				elsif ($participants[$i] ne $m{name} && $pass_datas{$participants[$i]} == 2) { # 上がっているﾌﾟﾚｲﾔｰ
					$refresh_num++;
				}
			}
		}

		$result_mes .= 'パス' if $is_pass;
		if ($is_eight_cut || $is_s3_cut || ($is_find && @participants == ($pass_num+$refresh_num+1)) || (!$is_find && @participants == ($pass_num+$refresh_num))) { 
			$mes .= "turn change2<br>";
			($head[$_field_card], $head[$_bind_m], $head[$_bind_s]) = ('', '', '');
			$result_mes .= '<br>八切り' if $is_eight_cut;
			$result_mes .= '<br>スペ3返し' if $is_s3_cut;
			$result_mes .= ' 場を流しました';
			for my $i (0 .. $#members) {
				my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $members[$i];
				next if $mturn < 2 || 1 < $mvalue;
				$members[$i] = "$mtime<>$mname<>$maddr<>$mturn<>0<>$mstock<>\n";
			}
		}

		# ﾊﾟｽをしていないﾌﾟﾚｲﾔｰがいるなら直近のﾊﾟｽをしていないﾌﾟﾚｲﾔｰのﾀｰﾝ
		# 全員がﾊﾟｽしているなら直近のﾊﾟｽをしているﾌﾟﾚｲﾔｰのﾀｰﾝ
		$head[$_participants] = &change_turn($head[$_participants]) for (1 .. $next_num[!$is_find]) unless $is_eight_cut || $is_s3_cut; # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
	}

	my $penalty_coin = 0;
	my $size2 = @participants;
	$mes .= "if init_header is_my_turn $is_my_turn && is_reset $is_reset == participants $size2<br>";
	if ($is_my_turn && $winner eq $m{name} && ($is_playable || $is_pass) && $is_reset == @participants) { # 若干不必要な感じもするけどとにかく終了条件厳しく
		$mes .= "reset1<br>";
		$penalty_coin = $head[$_rate];
		&init_header(\@head);
		&reset_members(\@members);
	}
	else { $is_reset = 0; }

	my $header = &h_to_s(@head);
	$mes .= "header $header<br>";
	unshift @members, $header; # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# 終了処理
	if ($is_reset) {
		$mes .= "reset2<br>";
		my $winner_mes = '';
		my $loser_mes = '';
		my $move_c = 2 <= (@winners / 2) ? 2 : 1; # 4人以上でｺｲﾝの移動が2回起きる 大富豪<->大貧民 富豪<->貧民 3人以下では 大富豪<->大貧民 の1回
		for my $i (0 .. $#winners) {
			if ($winners[$i] eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($winners[$i], 'c_turn', '0');
			}

			if ($i < $move_c) {
				&coin_move($penalty_coin / (1 + $i), $winners[$i], 1);
				$winner_mes .= "$winners[$i] は ".($penalty_coin / (1 + $i))." ｺｲﾝ得ました<br>";

				&coin_move(-1 * $penalty_coin / (1 + $i), $winners[$#winners-$i], 1);
				$loser_mes = "$winners[$#winners-$i] は ".($penalty_coin / (1 + $i))." ｺｲﾝ払いました<br>" . $loser_mes;
			}
			elsif ($i < @winners-$move_c) {
				$winner_mes .= "$winners[$i] は 0 ｺｲﾝ得ました<br>";
			}
		}
		&system_comment("$winner_mes$loser_mes");
	}

	return $result_mes; # ﾌﾟﾚｲの報告
}

sub show_status {
	my @head = @_;

	my @field_cards = split /,/, $head[$_field_card];
	my $field_num = @field_cards;

	print "<br>状態：";

	if ($head[$_revo]) {
		print "革命 ";
	}

	# 複数枚・階段出し縛り表示
	if ($field_num) {
		if ($head[$_bind_m] == 2) {
			print "$field_num枚階段縛り";
		}
		else {
			print "$field_num枚縛り";
		}
	}

	# ｽｰﾄ縛り表示
	if ($head[$_bind_s]) {
		print " ｽｰﾄ縛り(";
		my @suit_lock = ();
		for my $i (0 .. 3) {
			push @suit_lock, $suits[$i] if 1 & ($head[$_bind_s] >> $i);
		}
		print join " ", @suit_lock;
		print ")";
	}

	print "<br>場札：";
	for my $i (0 .. $#field_cards) {
		my ($num, $suit) = &get_card($field_cards[$i]);
		print " " if $i != 0;
		print "$suits[$suit]$nums[$num]";
	}

	print "<br>手札：";
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		my @hand_cards = split /,/, $datas[2];
		my $size = @hand_cards;
		print "$datas[0]：$size枚 ";
		print " ";
	}
}

sub shuffled_deck {
	my $participants = shift;
	my $size = 51; # ｶｰﾄﾞ枚数 54枚 Joker 2枚有
	my @deck;

	@deck[$_] = $_+1 for (0 .. $size);
	for my $i (0 .. $size) {
		my $j = int(rand($i + 1)); # 周回する度に乱数範囲を広げる
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}

	# ﾌﾞﾗｲﾝﾄﾞｶｰﾄﾞ 参加者全員が同じ手札枚数になるように調節
	my $blind_num = 54 % $participants;
	shift(@deck) for (0 .. $blind_num-1);
	splice(@deck, int(rand(@deck)), 0, "$_") for (53 .. 54); # ｼﾞｮｰｶｰは除外対象から外れる

	return @deck;
}

sub get_card {
	my $card = shift;
	my ($num, $suit) = ('', '');
	if ($card == 53 || $card == 54) {
		($num, $suit) = (13, 4);
	}
	else {
		$num = ($card-1) % 13; # 1～52 の値から -1 したものを 13 で割った余りが 0～12 になる
		$suit = int(($card-1)/13); # 0ｽﾍﾟｰﾄﾞ 1ﾊｰﾄ 2ｸﾗﾌﾞ 3ﾀﾞｲﾔ
	}
	return ($num, $suit);
}

sub is_playable {
	my ($play_cards, $field_cards, $bind_m, $bind_s, $revo) = @_;
	my @play_cards = split /,/, $play_cards; # 出したｶｰﾄﾞ
	my @field_cards = split /,/, $field_cards; # 場のｶｰﾄﾞ
	unless (@field_cards == 0 || @play_cards == @field_cards) { # ｶｰﾄﾞの枚数が揃っていない
		$mes .= '<p>ﾙｰﾙ違反 出すカードを'. @field_cards .'枚にしてください</p>';
		return (0, '');
	}

	my @play_card_datas = (); # 出したｶｰﾄﾞの詳細 [0]1枚目のﾗﾝｸ [1]1枚目のｽｰﾄ [2]2枚目のﾗﾝｸ [3]2枚目のｽｰﾄ ...
	($play_card_datas[$_*2], $play_card_datas[$_*2+1]) = &get_card($play_cards[$_]) for (0 .. $#play_cards);
	my @field_card_datas = (); # 場のｶｰﾄﾞの詳細 [0]1枚目のﾗﾝｸ [1]1枚目のｽｰﾄ [2]2枚目のﾗﾝｸ [3]2枚目のｽｰﾄ ...
	($field_card_datas[$_*2], $field_card_datas[$_*2+1]) = &get_card($field_cards[$_]) for (0 .. $#field_cards);

	# 数字縛り 革命関係なくｼﾞｮｰｶｰは常に最強かつｼﾞｮｰｶｰに対してはｽﾍﾟ3が最も強い
	my @num = ($play_card_datas[0], $field_card_datas[0]);
	unless ($revo) { # 非革命中
		$num[0] = 14 if @play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13; # ｽﾍﾟ3
	}
	else { # 革命中
		$num[0] = -2 if @play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13; # ｽﾍﾟ3
		$num[0] = -1 if $play_card_datas[0] == 13; # 手札のｼﾞｮｰｶｰ
		$num[1] = -1 if $field_card_datas[0] == 13; # 場のｼﾞｮｰｶｰ
=pod
		my $is_joker = 0;
		for my $i (0 .. $#play_cards) {
			if ($play_card_datas[($#play_cards-$i)*2] == 13) {
				$is_joker = 1;
				next;
			}
			else {
				if ($is_joker) {
					$num[0] = $play_card_datas[($#play_cards-$i)*2] + 1;
				}
				else {
					$num[0] = $play_card_datas[($#play_cards-$i)*2];
				}
				last;
			}
		}
		$mes .= "joker" if $is_joker;
		$is_joker = 0;
		for my $i (0 .. $#field_cards) {
			if ($field_card_datas[($#field_cards-$i)*2] == 13) {
				$is_joker = 1;
				next;
			}
			else {
				if ($is_joker) {
					$num[1] = $field_card_datas[($#field_cards-$i)*2] + 1;
				}
				else {
					$num[1] = $field_card_datas[($#field_cards-$i)*2];
				}
				last;
			}
		}
=cut
	}

	if (0 < @field_cards && $num[$revo] <= $num[!$revo]) { # 革命時は比較対象を入れ替える $revo でｽｲｯﾁ
		$mes .= '<p>ﾙｰﾙ違反 場札より強いｶｰﾄﾞを出してください</p>';
		return (0, '');
	}

	# ｽﾍﾟ3返しはｽｰﾄ縛り無視
	if (!(@play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13) && $bind_s) {
		my $play_suits = 0;
		my @play_suits = ();
		$play_suits[$play_card_datas[$_*2+1]] = 1 for (0 .. $#play_cards); # 出したｶｰﾄﾞすべてのｽｰﾄを取得
		$play_suits |= $play_suits[$_] << $_ for (0 .. 3); # ｽｰﾄ情報をビットフラグに変換
		unless ($bind_s == $play_suits) { # 縛りのビットフラグと同一ではない
			my $suit_xmatch = $bind_s ^ $play_suits;
			my $xmatch_num = 0;
			$xmatch_num += 1 & ($suit_xmatch >> $_) for (0 .. 3);

			my $joker_num = 0;
			for my $i (0 .. $#play_cards) {
				$joker_num++ if $play_card_datas[$i*2] == 13; # ｼﾞｮｰｶｰの枚数を取得
			}

			unless (($xmatch_num - $joker_num) == 0) { # ｽｰﾄ違いの数とｼﾞｮｰｶｰの枚数が同じじゃないならｽｰﾄが違反
				$mes .= '<p>ﾙｰﾙ違反 場札と同じｽｰﾄのｶｰﾄﾞを出してください</p>';
				return (0, '');
			}
		}
	}

	my @is_sequence = (); # [0] 出したｶｰﾄﾞが階段か [1] 場のｶｰﾄﾞが階段か
	my @is_double = (); # [0] 出したｶｰﾄﾞがﾀﾞﾌﾞﾙ以上か [1] 場のｶｰﾄﾞがﾀﾞﾌﾞﾙ以上か
	if (1 < @play_cards) { # 同位複数枚・階段ﾁｪｯｸ
		$is_sequence[0] = &is_sequence(@play_card_datas); # 階段ﾁｪｯｸ
		$is_double[0] = &is_double(@play_card_datas); # 同位札複数枚ﾁｪｯｸ
		unless ($is_sequence[0] || $is_double[0]) {
			$mes .= '<p>ﾙｰﾙ違反 複数枚出すときは同位で揃えるか階段にしてください</p>';
			return (0, '');
		}
	}
	if (0 < @field_cards && (($bind_m == 1 && !$is_double[0]) || ($bind_m == 2 && !$is_sequence[0])) ) {
		if ($bind_m == 1) {
			$mes .= (0, '<p>ﾙｰﾙ違反 出すカードを'. @field_cards .'枚にしてください</p>');
		}
		else {
			$mes .= (0, '<p>ﾙｰﾙ違反 出すカードを階段にしてください</p>');
		}
		return (0, '');
	}

	my $result_mes = '';
	$result_mes .= "$suits[$play_card_datas[$_*2+1]]$nums[$play_card_datas[$_*2]] " for (0 .. $#play_cards);
	$result_mes .= "を出しました";

	return (1, $result_mes, $is_sequence[0], $is_double[0]);
}

sub is_sequence {
	my @card_datas = @_;
	my $size = @card_datas / 2;
	my $is_sequence = 0;

	if (2 < $size) { # 3枚以上から階段 上限なし
		my ($is_suit, $is_joker) = (1, 0);
		my ($max, $min) = ($card_datas[0*2], $card_datas[1*2]); # 1枚目と2枚目を初期値に
		my @suit = ();
		$suit[0] = $card_datas[0*2+1]; # 1枚目のスートを取得
		for my $i (0 .. $size - 1) { # 最大値と最低値の取得
			$suit[1] = $card_datas[$i*2+1];
			$is_joker++ if $suit[1] == 4;
			if ($is_joker < 1 && $suit[0] != $suit[1]) {
				$is_suit = 0;
				last;
			}
			next if $is_joker; # ｼﾞｮｰｶｰは最大値として数えない
			$max = $card_datas[$i*2] if $max < $card_datas[$i*2];
			$min = $card_datas[$i*2] if $card_datas[$i*2] < $min;
		}

		# 札 4枚 0をｼﾞｮｰｶｰとする 0～2 になる
		# 4007 = 7 - 4 + 1 = 4
		# 4060 = 6 - 4 + 1 = 3
		# 4500 = 5 - 4 + 1 = 2
		# 札 5枚 0をｼﾞｮｰｶｰとする
		# 45008 = 8 - 4 + 1 = 5
		# 45070 = 7 - 4 + 1 = 4
		# 45600 = 6 - 4 + 1 = 3
		my $diff = ($max - $min + 1);
		if ($is_joker < 2) { # ｼﾞｮｰｶｰが1枚以下含まれる階段
			if ($is_joker) {							# ｼﾞｮｰｶｰが1枚含まれる階段ならば、
				my $diff2 = $size - $diff;			# ｶｰﾄﾞ枚数から (最高値 - 最低値 + 1) を引くと 0 ～ 1 になる
				$is_sequence = (($diff2 == 0 || $diff2 == 1) && $is_suit); # （最高位をJokerで代替すると 1、下位だと 0）
			}
			else { # ｼﾞｮｰｶｰが含まれない階段
				$is_sequence = ($diff == $size && $is_suit); # (最高値 - 最低値 + 1) == 出した枚数 && スート揃ってる
			}
		}
		else { # ｼﾞｮｰｶｰが2枚含まれる階段
			if ($size == 3) { $is_sequence = 1; } # ｼﾞｮｰｶｰ以外が1枚しかない階段
			else {											# ｼﾞｮｰｶｰが2枚含まれる4枚以上の階段ならば、
				my $diff2 = $size - $diff;				 # 出したｶｰﾄﾞ枚数から (最高値 - 最低値 + 1) を引くと 0 ～ 2 になる
				$is_sequence = ((-1 < $diff2 && $diff2 < 3) && $is_suit); # （最高位をJokerで代替すると 2、下位になるにつれ 1、0 となる）
			}
		}
	}
	return $is_sequence;
}

sub is_double {
	my @card_datas = @_;
	my $size = @card_datas / 2;
	my $is_double = 1;
	my @num = ($card_datas[0*2], '');
	for my $i (0 .. $size - 1) {
		$num[1] = $card_datas[$i*2];
		if ($num[1] != 13 && $num[0] != $num[1]) {
			$is_double = 0;
			last;
		}
	}
	return $is_double;
}

1;#削除不可
