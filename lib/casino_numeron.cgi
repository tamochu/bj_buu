#================================================
# ﾇﾒﾛﾝ
#================================================
require './lib/_casino_funcs.cgi';

=pod
主な処理の流れ
_casino_funcs.cgi
	sub _default_run
		call &{$in{mode}} ﾛｰﾀﾞｰ
		call @datas = &get_menber
		call &show_game_info(@datas)

this_file.cgi
	sub run
		call _default_run
	sub @datas = get_member
	sub show_game_info(@datas)
	sub &{$in{mode}}

ｺﾏﾝﾄﾞの値から関数を呼び出す
get_memberでｶｼﾞﾉのﾍｯﾀﾞｰを定義 ここでｶｼﾞﾉ毎の独自の変数を定義
show_game_infoでﾌﾟﾚｲ画面などを表示 ここにｶｼﾞﾉ毎の独自の変数が渡ってくる
ﾌﾟﾚｲ画面で表示するｺﾏﾝﾄﾞの定義(このｺﾏﾝﾄﾞ値を関数として呼び出す)
ｺﾏﾝﾄﾞ値から呼び出される関数を定義
=cut

sub run {
#	$m{c_turn} = 0;
#	&write_user;
	&_default_run;
}

# ﾒﾝﾊﾞｰﾌｧｲﾙの読み込み
# 戻り値は第一から第六が固定($member_c, $member, $m_turn, $m_value, $m_stock, $state)、それ以降はｶｼﾞﾉ毎にｵﾘｼﾞﾅﾙ要素、それらがshow_game_infoに渡ってくる
sub get_member {
	my $member  = ''; # 参加者・閲覧者などすべてのﾌﾟﾚｲﾔｰ名を持つ
	my @members = (); # ↑の配列
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0); # 自分のデータ
	my @active_players = (); # ﾌﾟﾚｲ中の参加者の配列
	my @non_active_players = (); # 除外された参加者の配列
	my $penalty_coin = 0; # 除外 or ﾘｾｯﾄ時のﾍﾟﾅﾙﾃｨ

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	# ｶｼﾞﾉ毎のｵﾘｼﾞﾅﾙﾃﾞｰﾀ
	# ｹﾞｰﾑの状態、ｹﾞｰﾑの最終更新時間、ｹﾞｰﾑの参加者、ﾚｰﾄ
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my $is_reset = 0; # 第三者によるﾘｾｯﾄ：GAME_RESET、参加者による脱落確認：LEAVE_PLAYER
	if (-1 < index($participants, "$m{name},")) { # 参加者によるﾛｰﾄﾞでｹﾞｰﾑの最終更新時間を更新
		$lastupdate = $time;
	}
	elsif (($lastupdate + $limit_game_time < $time) && $participants && (index($participants, "$m{name},") < 0) && $m{c_turn} < 1) { # 非参加者が止まっているｹﾞｰﾑを閲覧したらﾘｾｯﾄ
		$is_reset = GAME_RESET;
		@non_active_players = split /,/, $participants;
		$penalty_coin = $rate if $state; # すでにｹﾞｰﾑを開始していたらｺｲﾝ没収
		($state, $lastupdate, $participants, $rate) = ('', '', '', '');
	}

	my %sames = ();
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		my $index = index($participants, "$mname,");
		if ($mname eq $m{name}) {
			$is_find = 1;
#			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$mvalue<>$mstock<>\n"; # 自動で脱落するので余計なﾃﾞｰﾀ要らない（他のｶｼﾞﾉ行き来された時にc_turnは必要）
			($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
			$member .= "$mname,";

			push @active_players, "$mname" if -1 < $index;
		}
		else {
			# ｱｸﾃｨﾌﾞな参加者とｱｸﾃｨﾌﾞな閲覧者だけ残す
			if ( ((-1 < $index) && ($time < $mtime + $limit_think_time)) || ($time < $mtime + $limit_member_time) ) {
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
				$member .= "$mname,";

				push @active_players, "$mname" if -1 < $index;
			}
			else {
				if (-1 < $index && -1 < index($participants, "$m{name},")) { # 参加者を弾けるのは参加者の確認が必要
					substr($participants, $index, length("$mname,"), ''); # 参加者文字列から非ｱｸﾃｨﾌﾞﾌﾟﾚｲﾔｰを除外
					push @non_active_players, "$mname"; # 除外された参加者を追加
					$rate = $m{coin} unless $state; # ﾌﾟﾚｲ中でなければ賭け上限を残ったﾌﾟﾚｲﾔｰの全ｺｲﾝに
				}
			}
		}
	}
	unless ($is_find) { # 自分が閲覧者にいないなら追加
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>0<>0<>\n"; # 自動で脱落するので余計なﾃﾞｰﾀ要らない（他のｶｼﾞﾉ行き来された時にc_turnは必要）
		($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
		$member .= "$m{name},";
	}

	if (!$is_reset && @non_active_players > 0) { # GAME_RESETで初期化されておらず、放置ﾌﾟﾚｲﾔｰがいる場合
		$is_reset = LEAVE_PLAYER;
		$penalty_coin = $rate if $state;
		($state, $lastupdate, $participants, $rate) = ('', '', '', '') if @active_players == 1 && $penalty_coin;
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_reset) { # 放置されたｹﾞｰﾑか放置しているﾌﾟﾚｲﾔｰの片付け
		my @zeros = (['c_turn', '0'], ['c_value', '0'], ['c_stock', '0']);
		for my $leave_player (@non_active_players) {
			if ($is_reset eq GAME_RESET) {
#				&coin_move(-0.5 * $penalty_coin, $leave_player) if $penalty_coin;
			}
			elsif ($is_reset eq LEAVE_PLAYER) {
				if ($penalty_coin) {
					my $cv = -1 * &coin_move(-1 * $penalty_coin, $leave_player);
					&coin_move($cv, $active_players[0]);
					&system_comment("ﾌﾟﾚｲ中の放置ﾌﾟﾚｲﾔｰ$leave_playerを除外しました");
				}
				else {
					&system_comment("募集中の放置ﾌﾟﾚｲﾔｰ$leave_playerを除外しました");
				}
			}
			&regist_you_array($leave_player, @zeros);
		}
		if ($is_reset eq GAME_RESET) {
			&system_comment($penalty_coin ? "放置されたﾌﾟﾚｲ中のｹﾞｰﾑをﾘｾｯﾄしました" : '放置された募集中のｹﾞｰﾑをﾘｾｯﾄしました');
		}
		elsif ($penalty_coin && @active_players == 1) {
			if ($active_players[0] eq $m{name}) {
				$m{c_turn} = $m{c_value} = $m{c_stock} = '0';
				&write_user;
			}
			else {
				&regist_you_array($active_players[0], @zeros);
			}
			&system_comment("参加者が$active_players[0]だけとなったためｹﾞｰﾑをﾘｾｯﾄしました");
		}
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $m_turn, $m_value, $m_stock, $state, $participants, $rate);
}

sub show_game_info {
	my ($m_turn, $m_value, $m_stock, $state, $participants, $rate) = @_;

	my @participants = split /,/, $participants;

	if ($participants) {
		print qq|賭け上限:$rate 参加者:$participants|;
	}
	else {
		print qq|ﾒﾝﾊﾞｰ募集中|;
	}

	if ($state) { # ｹﾞｰﾑが開始している
		print qq|<br>自分の番号:$m_value| if -1 < index($participants, "$m{name},");
		&play_form($m_turn, $m_value, $m_stock, $participants);
	}
	else { # ｹﾞｰﾑが開始していない
		if (-1 < index($participants, "$m{name},")) { # ｹﾞｰﾑに参加している
			&start_game_form($m_turn, $m_value, $m_stock, $participants); # 開始ﾌｫｰﾑ
		}
		else { # ｹﾞｰﾑに参加していない
			if ($participants[0] && $participants[1]) { # 親と子が決まっている
				print qq|<br>ｹﾞｰﾑの開始を待っています|;
			}
			else { # 親と子どちらか決まってない
				&participate_form($participants[0], $participants[1], $rate); # 参加ﾌｫｰﾑ
			}
		}
	}
}

sub participate_form { # 「参加する」のﾌｫｰﾑ
	my ($leader, $opponent, $rate) = @_;

	my $button = $leader ? "参加する" : "親になる";

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="participate">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="text"  name="number" class="text_box_b"> 自分の番号<br>|;
	print qq|<input type="text"  name="bet" class="text_box_b"> 賭けるｺｲﾝ<br>| if $leader;
	print qq|<input type="submit" value="$button" class="button_s"></form>|;
}

sub participate { # 「参加する」処理
	return "ｺｲﾝがありません" unless $m{coin};

	my @number;
	if ($in{number} ne '' && $in{number} !~ /[^0-9]/) {
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("同じ数字は二度使えません");
		}
	}
	else {
		return ("3つの異なる数字を入れてください");
	}

	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$mtime = $time;
			$mturn = 1;
			$mvalue = sprintf("%03d", $number[0] * 100 + $number[1] * 10 + $number[2]);
			$mstock = 63;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @participants = split /,/, $participants;

	my $is_entry = 0;
	my $is_entry_full = 0;
	my $is_no_bet = 0;
	if (@participants > 1) {
		$is_entry_full = 1;
	}
	elsif (-1 < index($participants, "$m{name},")) {
		$is_entry = 1;
	}
	elsif (!$state && $m{c_turn} == 0) { # 募集人数埋まっておらず未参加かつ開始前で対人ｶｼﾞﾉをやっていない
		unless ($participants[0]) { # 参加者がいないなら親
			$rate = $m{coin};
			$participants .= "$m{name},";
			$lastupdate = $time;
		}
		elsif ($in{bet}) { # 親がいて賭け金を設定しているなら
			$rate = $in{bet} > $rate ? $rate : $in{bet} ;
			$participants .= "$m{name},";
			$lastupdate = $time;
		}
		else { # 親はいて子が賭け金を設定していない
			$is_no_bet = 1;
		}
	}
	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n";

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($state) {
		return "すでにｹﾞｰﾑが始まっています";
	}
	elsif ($is_entry) {
		return "すでに参加しています";
	}
	elsif ($is_entry_full) {
		return "すでに参加者が集まっています";
	}
	elsif ($is_no_bet) {
		return "子になるにはｺｲﾝをﾍﾞｯﾄしてください";
	}
	elsif ($m{c_turn}) {
		return "対人ｶｼﾞﾉをﾌﾟﾚｲ中です";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} が席に着きました";
	}
}

sub start_game_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	my @participants = split /,/, $participants;

	print qq|<br>自分の番号:$m_value<br>|;
	if (@participants == 2) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="start_game">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="開始する" class="button_s"></form>|;
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="observe">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="参加しない" class="button_s"></form>|;
	}
	else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="observe">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="参加しない" class="button_s"></form>|;
	}
}

sub observe { # 「参加しない」処理
	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		push @members, $line;
	}
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my $is_entry = 0;
	my $index = index($participants, "$m{name},");
	if (!$state && -1 < $index && $m{c_turn} == 1) { # 参加はしているがｹﾞｰﾑは開始していない
		$is_entry = 1;
		substr($participants, $index, length("$m{name},"), '');
	}

	my $is_reset = 0;
	if (length($participants)) { # ﾒﾝﾊﾞｰが一人でもいるなら
		my @participants = split /,/, $participants;
		my %tmp_y = get_you_datas($participants[0]);
		unshift @members, "$state<>$time<>$participants<>$tmp_y{coin}<>\n";
	}
	else { # ﾒﾝﾊﾞｰの最後の一人が席を離れたらﾘｾｯﾄ
		unshift @members, "<><><><><><>\n";
		$is_reset = GAME_RESET;
	}

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($state) {
		return "すでにｹﾞｰﾑが始まっています";
	}
	elsif (!$is_entry) {
		return "ｹﾞｰﾑに参加していません";
	}
	else {
		$m{c_turn} = $m{c_value} = $m{c_stock} = '0';
		&write_user;
		my $result_mes = "$m{name} が席を離れました";
		if ($is_reset eq GAME_RESET) {
			&system_comment('参加者不在のためｹﾞｰﾑをﾘｾｯﾄしました');
			$result_mes = '';
		}
		return $result_mes;
	}
}

sub start_game {
	my @members = ();
	my @game_members = ();

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @participants = split /,/, $participants;

	my $is_start = 0;
	if (@participants == 2 && !$state && -1 < index($participants, "$m{name},") && $m{c_turn} == 1) { # 参加者が自分を含め二人、ｹﾞｰﾑ開始前なら
		$state = 1;
		$is_start = 1;
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && -1 < index($participants, "$mname,")) {
			push @game_members, $mname;
			$mturn = 2;
			$mtime = $time;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, "$state<>$time<>$participants<>$rate<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_start) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 2;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '2');
			}
		}
		return '勝負！';
	}
}

sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	unless (index($participants, "$m{name},") == 0) {
		print qq|<br>相手が思考中です|;
		return;
	}

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> 番号<input type="hidden" name="mode" value="play">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="番号を当てる" class="button_s"></form>|;

	return if $m_stock == 0;

	print qq|<hr><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="use_item">アイテム<input type="text"  name="number" class="text_box_b"> 番号<br>|;
	if (int($m_stock / 32) == 1) {
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 16) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 8) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 4) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 2) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if($m_stock % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="6">CHANGE |;
		print qq|</label>| unless $is_moble;
		for my $num (0 .. 2) {
			my $c = substr($m_value, $num, 1);
			print qq|<label>| unless $is_moble;
			print qq|<input type="radio" name="choicenum" value="$c">$c 交換|;
			print qq|</label>| unless $is_moble;
		}
		print qq|<br>|;
	}
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="アイテムを使う" class="button_s"></form>|;
}

sub play {
	return "3つの数字を入れてください" if !($in{number} ne '' && $in{number} !~ /[^0-9]/);

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my $is_my_turn = $player[0] eq $m{name};
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if ($mname eq $player[1] && $is_my_turn) {
			$e_name = $mname;
			$e_value = $mvalue;
			$is_find = 1;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my @game_member = ();
	my $is_reset = 0;
	my $penalty_coin = 0;
	if ($is_find) {
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit イート $blow バイト";
		$lastupdate = $time;
		if ($hit == 3) {
			$result_mes .= "勝利";
			@game_members = split /,/, $participants;
			$penalty_coin = $rate;
			($state, $lastupdate, $participants, $rate) = ('', '', '', '');
			$is_reset = 1;
		}
		$participants =~ s/^(.*?),(.*)/$2$1,/g; # 操作中のﾌﾟﾚｲﾔｰを最後尾に移動
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ﾍｯﾀﾞｰ
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
			for my $j (0..$i - 1) {
				$d++ if $number[$j] == $number[$i];
			}
			if ($d == 0) {
				for my $j (0..2) {
					$blow++ if $answer[$j] == $number[$i];
				}
			}
		}
	}
	return ($hit, $blow);
}

sub use_item {
	unless ($in{itemno}) {
		return "使うｱｲﾃﾑを選んでください";
	}
	elsif ( ($in{itemno} == 1 || $in{itemno} == 3 || $in{itemno} == 6) && !($in{number} ne '' && $in{number} !~ /[^0-9]/) ) {
		return "数字を入れてください";
	}
	elsif ($in{itemno} == 6) {
		return "CHANGE 交換する数を選んでください" if $in{choicenum} eq '';
		return "CHANGE 1桁の数字を選んでください" if 9 < $in{number};
		return "CHANGEで変えられるのはHIGH同士かLOW同士です" if (($in{number} < 5) xor ($in{choicenum} < 5));
	}

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my $is_my_turn = $player[0] eq $m{name};
	my ($e_name, $e_value);
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0);
	my $my_index = -1; # @membersに格納されている自分のデータのインデックス

	my %sames = ();
	my @is_find = (0, 0); # 相手データ読み込んだか、自分データ読み込んだか
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		$my_index++ unless $is_find[1];
		if ($mname eq $player[1] && $is_my_turn) {
			$e_name = $mname;
			$e_value = $mvalue;
			$is_find[0] = 1;
		}
		elsif ($mname eq $player[0] && $is_my_turn) {
			($m_turn, $m_value, $m_stock) = ($mturn, $mvalue, $mstock);
			$is_find[1] = 1;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my @game_member = ();
	my $is_reset = 0;
	my $is_double = 0;
	my $penalty_coin = 0;
	my $is_ng = 0;
	if ($is_my_turn && $is_find[0] && $is_find[1]) {
		# DOUBLE ランダムに選ばれた自分の1桁を公開する代わりに2回コールできる
		if ($in{itemno} == 1 && int($m_stock / 32) == 1) {
			my($hit, $blow) = &hb_count($in{number}, $e_value);
			$m_stock -= 32;
			my $open_card = int(rand(3)+1);
			my @open_num = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3桁の数字を配列に変換
			$result_mes .= "$m_value DOUBLE $m{name}の$open_card枚目は".$open_num[$open_card-1]."です<br>";
			$result_mes .= "$in{number}:$hit イート $blow バイト";
			if($hit == 3){
				$result_mes .= "勝利";
				@game_members = split /,/, $participants;
				$penalty_coin = $rate;
				($state, $lastupdate, $participants, $rate) = ('', '', '', '');
				$is_reset = 1;
			}
			else {
				$is_double = 1;
			}
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
			my @mm = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3桁の数字を配列に変換
			my ($e_max, $e_min) = ($mm[0], $mm[1]);
			for my $i (0 .. 2) {
				$e_max = $mm[$i] if $e_max < $mm[$i];
				$e_min = $mm[$i] if $e_min > $mm[$i];
			}
			$result_mes = "SLASH ".($e_max - $e_min);
		}
		# SHUFFLE 自分の数字をシャッフルする
		elsif ($in{itemno} == 5 && int($m_stock / 2) % 2 == 1) {
			$m_stock -= 2;
			$result_mes = "SHUFFLE";
			my @num_arr = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3桁の数字を配列に変換
			for my $i (0 .. 2) {
				my $j = int(rand($i + 1)); # 周回する度に乱数範囲を広げる 1周目:0～0 2周目:0～1 3周目:0～2
				my $tmp_n = $num_arr[$j]; # ただのスワップ
				$num_arr[$j] = $num_arr[$i];
				$num_arr[$i] = $tmp_n;
			}
			$m_value = int("$num_arr[0]$num_arr[1]$num_arr[2]");
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

	if ($is_my_turn && $result_mes && !$is_ng) {
		splice(@members, $my_index, 1, "$time<>$m{name}<>$addr<>$m_turn<>$m_value<>$m_stock<>\n");
		$lastupdate = $time;
		$participants =~ s/^(.*?),(.*)/$2$1,/g if $is_find[0] && $is_find[1] && !$is_double; # 操作中のﾌﾟﾚｲﾔｰを最後尾に移動
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ﾍｯﾀﾞｰ
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
