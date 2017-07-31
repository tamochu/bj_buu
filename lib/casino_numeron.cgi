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
	sub get_member
	sub show_game_info
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
# 戻り値は第一と第二が固定($member_c, $member)、それ以降はｶｼﾞﾉ毎にｵﾘｼﾞﾅﾙ要素、それらがshow_game_infoに渡ってくる
sub get_member {
	# 固定変数
	my $member  = ''; # 参加者・閲覧者などすべてのﾌﾟﾚｲﾔｰ名を持つ
	my @members = (); # ↑の配列
	my @active_players = (); # ﾌﾟﾚｲ中の参加者の配列
	my @non_active_players = (); # 除外された参加者の配列

	# ｶｼﾞﾉ毎の変数
	my $penalty_coin = 0;
	my @result_my_datas = ();

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
			@result_my_datas = ($m{c_turn}, $mvalue, $mstock);
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
#		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>0<>0<>\n"; # 自動で脱落するので余計なﾃﾞｰﾀ要らない（他のｶｼﾞﾉ行き来された時にc_turnは必要）
		@result_my_datas = ($m{c_turn}, $mvalue, $mstock);
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
		my @array = (['c_turn', '0'], ['c_value', '0'], ['c_stock', '0']);
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
			&regist_you_array($leave_player, @array);
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
				&regist_you_array($active_players[0], @array);
			}
			&system_comment("参加者が$active_players[0]だけとなったためｹﾞｰﾑをﾘｾｯﾄしました");
		}
	}

	# 固定処理
	my $member_c = @members - 1;
	return ($member_c, $member, $state, $participants, $rate, @result_my_datas);
}

sub show_game_info {
	my ($state, $participants, $rate, @result_my_datas) = @_;

	my @participants = split /,/, $participants;

	print qq|<br>ﾇﾒﾛﾝ修正中につきあんまり触らない方が良いと思う<br>|;
	print qq|ﾌﾟﾚｲ中に参加者が10分放置し(思考猶予\を超え)ているのを他の参加者が閲覧すると放置ﾌﾟﾚｲﾔｰが負け<br>|;
	print qq|ｹﾞｰﾑの最終ﾌﾟﾚｲから20分放置されているのをｹﾞｰﾑに参加していない閲覧者が閲覧すると流れ<br><br>|;
	if ($participants) {
		print qq|賭け上限:$rate 参加者:$participants|;
	}
	else {
		print qq|ﾒﾝﾊﾞｰ募集中|;
	}

	if ($state) { # ｹﾞｰﾑが開始している
		print qq|<br>自分の番号:$result_my_datas[1]| if -1 < index($participants, "$m{name},");
		&play_form($participants, @result_my_datas);
	}
	else { # ｹﾞｰﾑが開始していない
		if (-1 < index($participants, "$m{name},")) { # ｹﾞｰﾑに参加している
			&start_game_form($participants, @result_my_datas); # 開始ﾌｫｰﾑ
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

sub show_game {
	my @members = ();
	$m{c_turn} = 0;
	&write_user;

	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my %sames = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if (-1 < index($participants, "$mname,") && $mname eq $m{name}) { # 参加者のﾃﾞｰﾀだけ
			print qq|<br>自分の番号:$mvalue<br>|;
		}
	}
	close $fh;
	return;
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
	if ($in{number} > 0 && $in{number} !~ /[^0-9]/) {
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
			$mvalue = $number[0] * 100 + $number[1] * 10 + $number[2];
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
	my ($participants, @result_my_datas) = @_;
	my @participants = split /,/, $participants;

	print qq|<br>自分の番号:$result_my_datas[1]<br>|;
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
	my ($participants, @result_my_datas) = @_;
	return unless index($participants, "$m{name},") == 0;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> 番号<input type="hidden" name="mode" value="play">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="番号を当てる" class="button_s"></form>|;

	print qq|ｱｲﾃﾑ系未移植|;
=pod
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="use_item">アイテム<input type="text"  name="number" class="text_box_b"> 番号<br>|;
	if(int($result_my_datas[2] / 32) == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 16) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 8) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 4) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 2) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if($result_my_datas[2] % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="6">CHANGE<br>|;
		print qq|</label>| unless $is_moble;
	}
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="アイテムを使う" class="button_s"></form>|;
=cut
}

sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if ($mname eq $player[1]) {
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
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit イート $blow バイト";
		$lastupdate = $time;
		if($hit == 3){
			$result_mes .= "勝利";
			@game_members = split /,/, $participants;
			$penalty_coin = $rate;
			($state, $lastupdate, $participants, $rate) = ('', '', '', '');
			$is_reset = 1;
		}
		$participants =~ s/^(.*?),(.*)/$2$1,/g if $is_find; # 操作中のﾌﾟﾚｲﾔｰを最後尾に移動
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# 終了処理
	if ($is_reset) {
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
#=====
=pod
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("相手の番です") if $state ne $m{name}; # 動作未確認だけど、whileループ入る前に $state 代入された直後に close return した方が良いのでは

	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{comment}, $e_value);
		$state = $e_name;
		$ret_mes = "$in{comment}:$hit イート $blow バイト";
		if($hit == 3){
			$ret_mes .= "勝利";
			my $cv = -1 * &coin_move(-1 * $max_bet, $e_name);
			&coin_move($cv, $m{name});
			$state = '';
			$leader = '';
			$max_bet = 0;
			$reset_flag = 1;
		}
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}

	if($reset_flag){
		&reset_game;
	}

	return ($ret_mes);
=cut
}

sub hb_count {
    my ($m_number, $y_number) = @_;
	my @number = (int($m_number / 100), int($m_number / 10) % 10, $m_number % 10);
	my @answer = (int($y_number / 100), int($y_number / 10) % 10, $y_number % 10);
	my $hit = 0;
	my $blow = 0;
	for my $i (0..2) {
		if($answer[$i] == $number[$i]){
			$hit++;
		}else{
			my $d = 0;
			for my $j (0..$i - 1){
				if($number[$j] == $number[$i]) {
					$d++;
				}
			}
			if($d == 0){
				for my $j (0..2){
					if($answer[$j] == $number[$i]) {
						$blow++;
					}
				}
			}
		}
	}
	return ($hit, $blow);
}


=pod
sub run {
	if ($in{mode} eq "play") {
	    $in{comment} = &play_number;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "item") {
	    $in{comment} = &use_item;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "leader") {
	    $in{comment} = &make_leader;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bet") {
	    $in{comment} = &bet($in{max_bet});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "start") {
	    $in{comment} = &start_game;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "reset") {
	    $in{comment} = &reset_game;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}elsif($m{name} ne $leader) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="exit">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="やめる" class="button_s"></form><br>|;
	}
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|自動ﾘﾛｰﾄﾞ<select name="reload_time" class="select1"><option value="0">なし|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]秒| : qq|<option value="$i">$reload_times[$i]秒|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c人:$member</font><br>|;
	print $leader eq '' ? qq|親:募集中 賭け上限:<br>|:qq|親:$leader 賭け上限:$max_bet 対戦相手:$wmember<br>あなたの番号:$m{c_value}<br>|;

	if($leader){
		
		if($state eq $m{name} && $m{c_turn}){
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="comment" class="text_box_b"> 番号<input type="hidden" name="mode" value="play">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="番号を当てる" class="button_s"></form><br>|;
			
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="item">アイテム<input type="text"  name="comment" class="text_box_b"> 番号<br>|;
			if(int($m{c_stock} / 32) == 1){
				print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
			}
			if(int($m{c_stock} / 16) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
			}
			if(int($m{c_stock} / 8) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
			}
			if(int($m{c_stock} / 4) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
			}
			if(int($m{c_stock} / 2) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
			}
			if($m{c_stock} % 2 == 1){
				print qq|<input type="radio" name="itemno" value="6">CHANGE<br>|;
			}
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="アイテムを使う" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="number" class="text_box_b"> 自分の番号<br><input type="text"  name="comment" class="text_box_b"> ｺｲﾝ <input type="hidden" name="mode" value="bet"><input type="hidden" name="max_bet" value="$max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="賭ける" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} eq $leader && $in{mode} ne 'leader' && $waiting) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="start">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="開始" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} eq $leader && $in{mode} ne 'leader' && !$waiting) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="reset">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="やめる" class="button_s"></form><br>|;
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="text"  name="number" class="text_box_b"> 自分の番号<br><input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="親になる" class="button_s"></form><br>|;
	}
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

sub get_member { # flock
	my $is_find = 0;
	my $leave_name = '';
	my @leave_members = ();
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	my $leader_find = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$leave_name = $mname if $state ne 'waiting';
				push @leave_members, $mname;
			}else {
				next;
			}
		}
		# push @leave_members, $mname; よりも以前にないとマズい気もする
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		if ($mturn > 0 && $mname ne $leader){
			$waiting++;
			$wmember = $mname;
		}elsif($mname eq $leader){
			$leader_find = 1;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if (@leave_members) {
		for my $name (@leave_members) {
			&you_c_reset($name);
		}
	}

	if($leave_name){
		&reset_game($leave_name);
	}elsif($leader && !$leader_find){
		&reset_game;
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember);
}
=cut
sub play_number {
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("相手の番です") if $state ne $m{name}; # 動作未確認だけど、whileループ入る前に $state 代入された直後に close return した方が良いのでは

	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{comment}, $e_value);
		$state = $e_name;
		$ret_mes = "$in{comment}:$hit イート $blow バイト";
		if($hit == 3){
			$ret_mes .= "勝利";
			my $cv = -1 * &coin_move(-1 * $max_bet, $e_name);
			&coin_move($cv, $m{name});
			$state = '';
			$leader = '';
			$max_bet = 0;
			$reset_flag = 1;
		}
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}

	if($reset_flag){
		&reset_game;
	}

	return ($ret_mes);
}

sub use_item {
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("相手の番です") if $state ne $m{name};
	
	if($in{itemno} == 1 && int($m{c_stock} / 32) == 1){
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			my($hit, $blow) = &hb_count($in{comment}, $e_value);
			$m{c_stock} -= 32;
			&write_user;
			my $open_card = int(rand(3)+1);
			my $open_num = 0;
			if($open_card == 1){
				$open_num = int($m{c_value} / 100);
			}elsif($open_card == 2){
				$open_num = int($m{c_value} / 10) % 10;
			}else{
				$open_num = $m{c_value} % 10;
			}
			$ret_mes .= "DOUBLE $m{name}の$open_card枚目は$open_numです<br>";
			$ret_mes .= "$in{comment}:$hit イート $blow バイト";
			if($hit == 3){
				$ret_mes .= "勝利";
				my $cv = -1 * &coin_move(-1*$max_bet, $e_name);
				&coin_move($cv, $m{name});
				$state = '';
				$leader = '';
				$max_bet = 0;
				$reset_flag = 1;
			}
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
			print $fh @members;
			close $fh;
		}
	}elsif($in{itemno} == 2 && int($m{c_stock} / 16) % 2 == 1){
		$m{c_stock} -= 16;
		&write_user;
		$state = $e_name;
		my @hl = ();
		if(int($e_value / 100) >= 5){
			$hl[0] = "high";
		}else{
			$hl[0] = "low";
		}
		if(int($e_value / 10) % 10 >= 5){
			$hl[1] = "high";
		}else{
			$hl[1] = "low";
		}
		if($e_value % 10 >= 5){
			$hl[2] = "high";
		}else{
			$hl[2] = "low";
		}
		$ret_mes = "HIGH&LOW $hl[0],$hl[1],$hl[2]";
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 3 && int($m{c_stock} / 8) % 2 == 1){
		if($in{comment} >= 0 && $in{comment} !~ /[^0-9]/){
			$m{c_stock} -= 8;
			&write_user;
			my $target_num = $in{comment} % 10;
			my $target_place;
			if(int($e_value / 100) == $target_num){
				$target_place = "1枚目です";
			}elsif(int($e_value / 10) % 10 == $target_num){
				$target_place = "2枚目です";
			}elsif($e_value % 10 == $target_num){
				$target_place = "3枚目です";
			}else{
				$target_place = "ありません";
			}
			$ret_mes .= "TARGET $target_numは$target_place";
			$state = $e_name;
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
			print $fh @members;
			close $fh;
		}
	}elsif($in{itemno} == 4 && int($m{c_stock} / 4) % 2 == 1){
		$m{c_stock} -= 4;
		&write_user;
		$state = $e_name;
		my $e_max = int($e_value / 100);
		my $e_min = int($e_value / 100);
		if(int($e_value / 10) % 10 > $e_max){
			$e_max = int($e_value / 10) % 10;
		}
		if(int($e_value / 10) % 10 < $e_min){
			$e_min = int($e_value / 10) % 10;
		}
		if($e_value % 10 > $e_max){
			$e_max = $e_value % 10;
		}
		if($e_value % 10 < $e_min){
			$e_min = $e_value % 10;
		}
		my $s_num = $e_max - $e_min;
		$ret_mes = "SLASH $s_num";
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 5 && int($m{c_stock} / 2) % 2 == 1){
		$m{c_stock} -= 2;
		$state = $e_name;
		$ret_mes = "SHUFFLE";
		my @num_arr = (int($m{c_value} / 100), int($m{c_value} / 10) % 10, $m{c_value} % 10);
		my @n_rank = (int(rand(3)), int(rand(3)), int(rand(3)));
		if($n_rank[0] == $n_rank[1]){
			$n_rank[1] = ($n_rank[1] + 1) % 3;
		}
		while($n_rank[0] == $n_rank[2] || $n_rank[1] == $n_rank[2]){
			$n_rank[2] = ($n_rank[2] + 1) % 3;
		}
		my $new_num = 100 * $num_arr[$n_rank[0]] + 10 * $num_arr[$n_rank[1]] + $num_arr[$n_rank[2]];
		$m{c_value} = $new_num;
		&write_user;
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 6 && $m{c_stock} % 2 == 1){
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$m{c_stock} -= 1;
			$state = $e_name;
			my @old_arr = (int($m{c_value} / 100), int($m{c_value} / 10) % 10, $m{c_value} % 10);
			my @new_arr = (int($in{comment} / 100) % 10, int($in{comment} / 10) % 10, $in{comment} % 10);
			my $diff = 0;
			my $diff_hl;
			if($old_arr[0] != $new_arr[0]){
				$diff++;
				$diff_pos = 1;
				if($old_arr[0] < 5 && $new_arr[0] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[0] >= 5 && $new_arr[0] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGEで変えられるのはHIGH同士かLOW同士です"
				}
			}
			if($old_arr[1] != $new_arr[1]){
				$diff++;
				$diff_pos = 2;
				if($old_arr[1] < 5 && $new_arr[1] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[1] >= 5 && $new_arr[1] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGEで変えられるのはHIGH同士かLOW同士です"
				}
			}
			if($old_arr[2] != $new_arr[2]){
				$diff++;
				$diff_pos = 3;
				if($old_arr[2] < 5 && $new_arr[2] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[2] >= 5 && $new_arr[2] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGEで変えられるのはHIGH同士かLOW同士です"
				}
			}
			if($diff != 1){
				return "CHANGEで変えられるのは一枚です $diff"
			}
			my $new_num = 100 * $new_arr[0] + 10 * $new_arr[1] + $new_arr[2];
			$m{c_value} = $new_num;
			&write_user;
			$ret_mes .= "CHANGE $m{name}の$diff_pos枚目は$diff_hlです<br>";
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
			print $fh @members;
			close $fh;
		}
	}else{
		return;
	}
	
	if($reset_flag){
		&reset_game;
	}
	return ($ret_mes);
}

sub make_leader { # flock
	my @number;
	return("ｺｲﾝがありません") if $m{coin} < 0;
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("同じ数字は二度使えません");
		}
	}else{
		return ("3つの異なる数字を入れてください");
	}
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		$max_bet = $m{coin};
#		$max_bet = 10;
		$state = 'waiting';
		$m{c_turn} = 1;
		$m{c_value} = $number[0] * 100 + $number[1] * 10 + $number[2];
		$m{c_stock} = 63;
		&write_user;
	}
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return ("$leader が親です 賭け上限:$max_bet");
}
=pod
sub start_game{
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	$state = $leader;
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		push @members, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ("勝負！");
}
=cut
sub reset_game{ # flock
	my $leave_name = shift;
	my $is_find = 0; # $leave_name のﾌﾟﾚｲﾔｰが存在するか
	my @winners = (); # ｹﾞｰﾑ勝利者
	my @members = (); # 閲覧者含む全ﾌﾟﾚｲﾔｰ

	$m{c_turn} = 0;
	&write_user;

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($leave_name ne '' && $mturn) { # 敗者が存在するｹﾞｰﾑの参加者
			if ($leave_name eq $mname) { # 敗者
				$is_find = 1;
			}
			else {
				push @winners, $mname; # 勝者
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n"; # 閲覧者含む全ﾌﾟﾚｲﾔｰ
	}
	unshift @members, "<>0<><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my($leader, $max_bet, $state) = split /<>/, $head_line; # ｹﾞｰﾑの情報
	my $ev = 0;

	# ｺｲﾝ闇湧き対策 まず敗者からｺｲﾝむしり取る
	if ($is_find) {
		$ev = -1 * &coin_move(-1*$max_bet, $leave_name);
		&you_c_reset($leave_name);
	}

	# 敗者からむしり取ったｺｲﾝを勝利者に分配
	for my $name (@winners) {
		&coin_move($ev, $name) if $is_find;
		&you_c_reset($name);
	}

	return ("リセットしました");
}

sub bet{
	my @number;
	my @members = ();
	return("ｺｲﾝがありません") if $m{coin} < 0;
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("同じ数字は二度使えません");
		}
	}else{
		return ("3つの異なる数字を入れてください");
	}
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mname eq $leader) {
			$waiting--;
		}
		$waiting++ if $mturn > 0;
	}
	close $fh;
	
	if($waiting){
		return("すでに対戦者がいます");
	}else{
		my $max = shift;
		my $v;
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$v = $in{comment};
			$v = $m{coin} if $v > $m{coin};
			if($v > 0){
				$v = $max if $v > $max;
				$max_bet = $v;
				$m{c_turn} = 1;
				$m{c_value} = $number[0] * 100 + $number[1] * 10 + $number[2];
				$m{c_stock} = 63;
				&write_user;
				unshift @members, "$leader<>$max_bet<>$state<>\n";
				open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
				print $fh @members;
				close $fh;
				return("$m{name} は $v ｺｲﾝ 賭けました");
			}
		}
	}
}

sub exit_game{
	my $waiting = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($mturn > 0 && $mname ne $leader){
			$waiting++;
		}
	}
	close $fh;
	
	if($m{name} eq $leader && $waiting){
		return("対戦相手が決まっています")
	}
	if ($state ne 'waiting'){
		return("ゲームが始まっています");
	}
	
	$m{c_turn} = 0;
	&write_user;
	return("$m{name} は やめました");
}

1;#削除不可
