#================================================
# ｶｼﾞﾉ共用関数
#================================================

use constant GAME_RESET => 1; # ｹﾞｰﾑの更新が止まっている
use constant LEAVE_PLAYER => 2; # 参加者が非ｱｸﾃｨﾌﾞになっている

$_header_size = 5; # ﾍｯﾀﾞｰ配列のﾍﾞｰｽｻｲｽﾞ
($_state, $_lastupdate, $_participants, $_participants_datas, $_rate) = (0 .. $_header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ

$limit_think_time = 60 * 10; # 10分放置でﾌﾟﾚｲﾔｰ除外 60 * 10
$limit_game_time = 60 * 20; # 20分放置でｹﾞｰﾑﾘｾｯﾄ 60 * 20

=pod
間黒男：こんな感じで時間ある時に複垢なり手伝い頼むなりしてやってみてよ (蜀 : 9/10 21:53)
間黒男：パターン５（パターン２で切るカードを８にしてみる） (蜀 : 9/10 21:52)
間黒男：パターン４（Ｃは発言ボタンで更新、その後ＡまたはＢのうち自分の番のプレイヤーがパターン２） (蜀 : 9/10 21:52)
間黒男：パターン３（Ｃは発言ボタンで更新、その後ＡまたはＢがパターン１） (蜀 : 9/10 21:51)
間黒男：パターン２（Ｃはそのまま更新せずに待機、ＡまたはＢのうち自分の番のプレイヤーがカードを切る）←いちばん怪しい (蜀 : 9/10 21:51)
間黒男：ここからパターン１（Ｃはそのまま更新せずに待機、ＡまたはＢが発言でゲームを更新） (蜀 : 9/10 21:50)
間黒男：Ｃ、30秒後に止まっている大貧民を閲覧する (蜀 : 9/10 21:49)
間黒男：更新をやめる前にＣに連絡して30秒後に大貧民に来るよう合図を送っておく (蜀 : 9/10 21:49)
間黒男：AとＢで適当にゲーム進めて、二人同時に更新をやめる（発言ボタンも押さない） (蜀 : 9/10 21:48)
間黒男：AとBでゲーム開始、Ｃはｶｼﾞﾉの外で待機 (蜀 : 9/10 21:47)
間黒男：プレイヤー３人用意する（Ａ、Ｂ、Ｃ） (蜀 : 9/10 21:47)
間黒男：明日からあんまりＩＮ出来ないから手順だけ書いとくぞ (蜀 : 9/10 21:47)
間黒男：二人でゲーム開始して20秒更新しないまま誰かに閲覧してもらってどうなるか見てみたい (蜀 : 9/10 21:43)
間黒男：ああ、でも$is_resetフラグが立てられてるから、この時点ではバグらない (蜀 : 9/10 21:40)
間黒男：if文の中で@non_active_players = &get_members($head[$_participants]); (蜀 : 9/10 21:37)
間黒男：あー、_casino_func.cgiで285行目のif文の条件が$is_no_participants==true (蜀 : 9/10 21:36)
間黒男：ななみえー何時に帰ってくるのよもう…！ (蜀 : 9/10 21:13)
間黒男：まあでも20秒止まったゲームを非参加者が閲覧するとinit_headerが呼ばれる (蜀 : 9/10 21:11)
間黒男：あ、秒数だった (蜀 : 9/10 21:10)
間黒男：$limit_game_timeが20に設定されてるけど$timeと（多分）$head[$_lastupdate]ってミリ秒だろ (蜀 : 9/10 21:03)
間黒男：$head[$_lastupdate] + $limit_game_time < $time (蜀 : 9/10 21:03)
間黒男：_casino_func.cgi 285行目だな (蜀 : 9/10 21:01)
=cut

sub init_header {
	my $ref_arr = shift; # ﾘﾌｧﾚﾝｽは shift じゃないと取得できない（$_だと実体の[0]が取り出される？）
	$ref_arr->[$_] = '' for (0 .. $_header_size + $header_size - 1);
}

sub h_to_s { # ﾍｯﾀﾞｰ配列を文字列にして返す
	my @arr = @_;
	my $str = '';
	$str .= "$arr[$_]<>" for (0 .. $_header_size + $header_size - 1);
	return "$str\n";
}

sub d_to_s { # ﾕｰｻﾞｰﾃﾞｰﾀを文字列にして返す
	my @arr = @_;
	my $str = '';
	$str .= "$arr[$_]:" for (0 .. $#arr-1);
	return "$str$arr[$#arr];";
}

sub admin_reset {
	$m{c_turn} = 0;
	&write_user;

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh '';
	close $fh;

	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);
	for my $game_member (@participants) {
		if ($game_member eq $m{name}) {
			$m{c_turn} = 0;
			&write_user;
		}
		else {
	 		&regist_you_data($game_member, 'c_turn', '0');
		}
	}
}

sub admin_reset2 {
	&regist_you_data($in{name}, 'c_turn', '0');
#	my $r = '';
#	my %p = &get_you_datas($in{name}, 0);
#	$mes .= "$in{name} c_turn $p{c_turn}";
#	my @members = ();

#	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
#	while (my $id = readdir $dh) {
#		next if $id =~ /\./;
#		next if $id =~ /backup/;

#		my %p = &get_you_datas($id, 1);
#		if ($p{c_turn} ne '0') {
#			my $name = pack 'H*', $id;
#			push @members, $name;
#			$r .= "$name $p{c_turn} ";
#		}
#	}
#	closedir $dh;

#	for my $i (0 .. $#members) {
#		&regist_you_data($members[$i], 'c_turn', '0');
#	}

	return $r;
}

=pod
主な処理の流れ
_casino_funcs.cgi
	sub _default_run
		call &{$in{mode}} ﾛｰﾀﾞｰ ｺﾏﾝﾄﾞの値から関数を呼び出す
		call @datas = &_get_menber
	sub _get_menber
		call &show_game_info(@datas)
	sub _participate 「参加する」処理
	sub observe 「参加しない」処理

this_file.cgi
	sub run
		call _default_run
	sub show_game_info(@datas)
	sub participate_form 「参加する」のﾌｫｰﾑ
	sub participate 「参加する」処理 ﾚｰﾄを渡すだけ
	sub start_game_form 「開始する」「参加しない」のﾌｫｰﾑ
	sub start_game 「開始する」処理 ﾍｯﾀﾞｰを定義
	「参加しない」処理は_casino_funcs.cgiで定義
	sub play_form ﾌﾟﾚｲのﾌｫｰﾑ
	sub play ﾌﾟﾚｲ処理
	以上のｻﾌﾞﾙｰﾁﾝが揃っていればとりあえず動く
	sub &{$in{mode}} その他ﾛｰﾀﾞｰに対応する処理

show_game_infoでﾌﾟﾚｲ画面などを表示 ここにﾍｯﾀﾞｰﾃﾞｰﾀが渡ってくる
ﾌﾟﾚｲ画面で表示するｺﾏﾝﾄﾞの定義(このｺﾏﾝﾄﾞ値を関数として呼び出す)
ｺﾏﾝﾄﾞ値から呼び出される関数を定義
=cut

#================================================
# 対人ｶｼﾞﾉの基本的なﾒｲﾝ画面
# $option_form に追加のﾌｫｰﾑを設定しておけば追加できる
#================================================
sub _default_run {
#	my $_default = $_; # ﾁｬｯﾄ部分の有無
	$in{comment} = &{$in{mode}} if $in{mode} && $in{mode} ne 'write'; # 各ｺﾏﾝﾄﾞに対応する関数へのﾛｰﾀﾞｰ
	&write_comment if $in{comment};

	my ($member_c, $member, @datas) = &_get_member;

#	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;

	if ($m{c_turn}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="comment" value="ちょっと離席"><input type="hidden" name="mode" value="write">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="ちょっと離席" class="button_s">|;
		print qq|</form>|;
	}
	if ($m{name} eq 'nanamie') {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("admin_reset", "ﾘｾｯﾄ");
		print qq|</form>|;

		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="text"  name="name" class="text_box_b"> ﾕｰｻﾞｰ名|;
		print &create_submit('admin_reset2', 'c_turn');
		print qq|</form>|;
	}

	print $option_form;
#	}

	print qq|<h2>$this_title</h2>|;
	print qq|$mes|;
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

	print qq|<font size="3">|;
	&_show_game_info(@datas);
	print qq|</font>|;

	print qq|<hr>|;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

#================================================
# 対人ｶｼﾞﾉのﾒﾝﾊﾞｰ管理
# show_game_info に渡す戻り値の固定部分 ($m_turn, $m_value, $m_stock, $state, $lastupdate, $participants, $participants_datas, $rate)
# 以降の戻り値はｶｼﾞﾉ毎のｵﾘｼﾞﾅﾙﾃﾞｰﾀ ｵﾘｼﾞﾅﾙﾃﾞｰﾀ自体は start_game で設定する
# $participants_datas に全参加者の name, value, stock を持つ文字列が入っている ex. name1:value1:stock1;name2:value2:stock2;
# $participants_datas を操作する必要は特にない ｺﾏﾝﾄﾞ→_get_memberの順で呼ばれるので、ｺﾏﾝﾄﾞでﾌﾟﾚｲﾔｰﾃﾞｰﾀを書き換えればあとは自動で読み直す
# $participants はﾀｰﾝの流れも示しているので並び順から登録順を逆算できない
# 代わりに、member.cgi ファイルの並び順が参加順になっている（一人目の参加者（親）は member.cgi の2行目(1行目はﾍｯﾀﾞｰ)、二人目の参加者は3行目...）
#================================================
sub _get_member {
	my $member  = ''; # 参加者・閲覧者などすべてのﾌﾟﾚｲﾔｰ名を持つ
	my @members = (); # ↑の配列
	my ($m_turn, $m_value, $m_stock) = (0, '', ''); # 自分のデータ
	my @active_players = (); # ﾌﾟﾚｲ中の参加者の配列
	my @non_active_players = (); # 除外された参加者の配列
	my $penalty_coin = 0; # 除外 or ﾘｾｯﾄ時のﾍﾟﾅﾙﾃｨ
	my $is_game = 0; # ｹﾞｰﾑが開始しているか

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	# ｶｼﾞﾉのﾃﾞｰﾀ情報
	# ｹﾞｰﾑの状態、ｹﾞｰﾑの最終更新時間、ｹﾞｰﾑの参加者、参加者のﾃﾞｰﾀ、ﾚｰﾄ、以降はｶｼﾞﾉ毎のｵﾘｼﾞﾅﾙﾃﾞｰﾀ
	my @head = split /<>/, $head_line;
	my $is_no_participants = $head[$_participants] eq '';

	# 参加者のﾃﾞｰﾀ順は固定なので常に新規作成
	# 参加者文字列はﾀｰﾝ順も表すので書き換える必要がある
	$head[$_participants_datas] = '';

	my $is_member = 0 < $m{c_turn};
#	$mes .= "c_turn $m{c_turn}<br>";

	my %sames = ();
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if ($is_no_participants) { # 参加者がいない
			push @non_active_players, $mname if $mturn;
			if ($mname eq $m{name}) {
				$is_find = 1;
				push @members, "$time<>$m{name}<>$maddr<>0<><><>\n";
				$member .= "$mname($m{c_turn}),";
			}
			else {
				if ($time < $mtime + $limit_member_time) {
					push @members, "$mtime<>$mname<>$maddr<>0<><><>\n";
					$member .= "$mname($mturn),";
				}
			}
			next;
		}

		if ($mname eq $m{name}) {
			$is_find = 1;
			$member .= "$mname($m{c_turn}),";
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$mvalue<>$mstock<>\n"; # 自動で脱落するので余計なﾃﾞｰﾀ要らない（他のｶｼﾞﾉ行き来された時にc_turnは必要）
			($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
			if ($is_member) {
				push @active_players, "$m{name}";
#				$head[$_participants] .= "$m{name}," if !$head[$_state];
				$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
			}
		}
		else {
#			$mes .= "name $mname<br>";
			my $is_entry = 0 < $mturn;
#			$mes .= "entry $mturn<br>";
			# ｱｸﾃｨﾌﾞな参加者とｱｸﾃｨﾌﾞな閲覧者だけ残す
			if ( ($is_entry && ($time < $mtime + $limit_think_time)) || ($time < $mtime + $limit_member_time) ) {
				$member .= "$mname($mturn),";
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
				if ($is_entry) {
					push @active_players, "$mname";
#					$head[$_participants] .= "$mname," if !$head[$_state];
					$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
				}
			}
			else {
				if ($is_entry && $is_member) { # 参加者を弾けるのは参加者の確認が必要
					$head[$_participants] = &remove_member($head[$_participants], $mname); # 参加者文字列から非ｱｸﾃｨﾌﾞﾌﾟﾚｲﾔｰを除外
					push @non_active_players, "$mname"; # 除外された参加者を追加
					# ほぼほぼヌメロン用？
#					$rate = $m{coin} unless $state; # ﾌﾟﾚｲ中でなければ賭け上限を残ったﾌﾟﾚｲﾔｰの全ｺｲﾝに
				}
			}
		}
	}
	unless ($is_find) { # 自分が閲覧者にいないなら追加
		push @members, "$time<>$m{name}<>$addr<>0<><><>\n"; # 自動で脱落するので余計なﾃﾞｰﾀ要らない（他のｶｼﾞﾉ行き来された時にc_turnは必要）
		($m_turn, $m_value, $m_stock) = (0, '', '');
		$member .= "$m{name}(0),";
		push @non_active_players, $m{name} if $m{c_turn};
	}

	my $is_reset = 0; # 第三者によるﾘｾｯﾄ：GAME_RESET、参加者による脱落確認：LEAVE_PLAYER
	if (!$is_no_participants) { # 参加者がいる
		if ($is_member) { # 参加者によるﾛｰﾄﾞでｹﾞｰﾑの最終更新時間を更新
			$head[$_lastupdate] = $time;
		}
		elsif ($head[$_lastupdate] && $m{c_turn} < 1 && ($head[$_lastupdate] + $limit_game_time < $time) && $head[$_participants]) { # 非参加者が止まっているｹﾞｰﾑを閲覧したらﾘｾｯﾄ
			$is_reset = GAME_RESET;
			@non_active_players = &get_members($head[$_participants]);
			$penalty_coin = $head[$_rate] if $head[$_state]; # すでにｹﾞｰﾑを開始していたらｺｲﾝ没収
			$is_game = $head[$_state];
			&init_header(\@head);
			&reset_members(\@members);
		}
		if ($is_member && !$is_reset && 0 < @non_active_players) { # GAME_RESETで初期化されておらず、参加者と放置ﾌﾟﾚｲﾔｰがいる場合
			$is_reset = LEAVE_PLAYER;
			$penalty_coin = $head[$_rate] if $head[$_state];
			$is_game = $head[$_state];
			if (@active_players == 1 && $is_game) {
				&init_header(\@head);
				&reset_members(\@members);
			}
		}
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_reset) { # 放置されたｹﾞｰﾑか放置しているﾌﾟﾚｲﾔｰの片付け
		for my $leave_player (@non_active_players) {
			# ｹﾞｰﾑﾘｾｯﾄ
#			if ($is_reset eq GAME_RESET) {
#				&coin_move(-0.5 * $penalty_coin, $leave_player) if $penalty_coin;
#			}
#			elsif ($is_reset eq LEAVE_PLAYER) {
			if ($is_reset eq LEAVE_PLAYER) {
				if ($is_game) {
					my $cv = -1 * &coin_move(-1 * $penalty_coin, $leave_player);
					&coin_move($cv, $active_players[0]);
					&system_comment("ﾌﾟﾚｲ中の放置ﾌﾟﾚｲﾔｰ$leave_playerを除外しました");
				}
				else {
					&system_comment("募集中の放置ﾌﾟﾚｲﾔｰ$leave_playerを除外しました");
				}
			}
			&regist_you_data($non_active_players[$i], 'c_turn', 0);
		}
		if ($is_reset eq GAME_RESET) {
			&system_comment($is_game ? "放置されたﾌﾟﾚｲ中のｹﾞｰﾑをﾘｾｯﾄしました" : '放置された募集中のｹﾞｰﾑをﾘｾｯﾄしました');
		}
		elsif ($is_game && @active_players == 1) {
			if ($active_players[0] eq $m{name}) {
				$m{c_turn} = '0';
				&write_user;
			}
			else {
				&regist_you_data($non_active_players[$i], 'c_turn', 0);
			}
			&system_comment("参加者が$active_players[0]だけとなったためｹﾞｰﾑをﾘｾｯﾄしました");
		}
	}
	elsif ($is_no_participants && @non_active_players) {
		for my $i (0 .. $#non_active_players) {
			if ($non_active_players[$i] eq $m{name}) {
				$m{c_turn} ='0';
				&write_user;
			}
			else {
				&regist_you_data($non_active_players[$i], 'c_turn', 0);
			}
		}
		&system_comment("何らかの理由によりｹﾞｰﾑがﾘｾｯﾄされました");
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $m_turn, $m_value, $m_stock, @head);
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub _show_game_info {
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @participants = &get_members($head[$_participants]);

	if ($head[$_participants]) {
		&show_game_info($m_turn, $m_value, $m_stock, @head);
		print qq| 参加者:|;
		print qq|$participants[$_],| for (0 .. $#participants);
	}
	else {
		unless ($this_file =~ "chat_casino_s") {
			print qq|ﾒﾝﾊﾞｰ募集中|; 
		}
	}
	&show_head_info($m_turn, $m_value, $m_stock, @head) if defined(&show_head_info); # すべてのﾌﾟﾚｲﾔｰに表示したい情報1
	if ($head[$_state]) { # ｹﾞｰﾑが開始している
		&show_started_game($m_turn, $m_value, $m_stock, @head);
	}
	else { # ｹﾞｰﾑが開始していない
		if (&is_member($head[$_participants], "$m{name}")) { # ｹﾞｰﾑに参加している
			print qq|<br>|;
			&show_start_info($m_turn, $m_value, $m_stock, @head) if defined(&show_start_info); # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報
			&_start_game_form($m_turn, $m_value, $m_stock, $head[$_participants]); # 開始・参加しないﾌｫｰﾑ
		}
		else { # ｹﾞｰﾑに参加していない
			if ($max_entry <= @participants) { print qq|<br>ｹﾞｰﾑの開始を待っています|; } # 参加者が埋まっている
			else { # 参加者が埋まっていない
				if (!$coin_lack && $m{coin} < $head[$_rate]) { print '<br>ｺｲﾝがﾚｰﾄに足りていません'; } # ｺｲﾝが足りていない
				else { &participate_form(@participants) if defined(&participate_form); }
#				elsif ($head[$_participants]) { # 参加ﾌｫｰﾑ
#					&participate_form;
#				}
#				else { # 親ﾌｫｰﾑ
#					&leader_form;
#				}
			}
		}
	}
	&show_tale_info($m_turn, $m_value, $m_stock, @head) if defined(&show_tale_info); # すべてのﾌﾟﾚｲﾔｰに表示したい情報2
}

#================================================
# 対人ｶｼﾞﾉの親になる
#================================================
sub _leader { # 「親になる」処理
	my ($in_rate, $m_value, $m_stock, $is_rate) = @_;

	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$is_find = 1;
			if (!$head[$_state] && @participants < $max_entry) {
				($mtime, $mturn, $mvalue, $mstock) = ($time, 1, $m_value, $m_stock);
				splice(@members, @participants, 0, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"); # ﾒﾝﾊﾞｰﾌｧｲﾙ上で参加順を表現するために参加者の後ろに移動
			}
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
	}
	unless ($is_find) { # 長期離席していたなど、ﾒﾝﾊﾞｰﾌｧｲﾙ上から消えていた場合
		if (!$head[$_state] && @participants < $max_entry) {
			splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>1<>$m_value<>$m_stock<>\n");
		}
	}

	my ($is_entry, $is_entry_full, $is_no_coin) = (0, 0, 0);
	my $leader_mes = '';
	if ($max_entry <= @participants) {
		$is_entry_full = 1;
	}
	elsif (0 < $m{c_turn}) {
		$is_entry = 1;
	}
	elsif (!$is_rate && $m{coin} < $rate) {
		$is_no_coin = 1;
	}
	elsif (!$head[$_state] && $m{c_turn} == 0) { # 募集人数埋まっておらず未参加かつ開始前で対人ｶｼﾞﾉをやっていない
		unless ($participants[0]) { # 参加者がいないなら親
			$head[$_rate] = $in_rate;
			$head[$_participants] .= "$m{name},";
			$leader_mes = " ﾚｰﾄ:$head[$_rate]";
			$head[$_lastupdate] = $time;
		}
		else {
			$head[$_participants] .= "$m{name},";
			$head[$_lastupdate] = $time;
		}
		$head[$_participants_datas] .= &d_to_s($m{name}, $m_value, $m_stock);
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
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
	elsif ($is_no_coin) {
		return "ｺｲﾝがﾚｰﾄに足りていません";
	}
	elsif ($m{c_turn}) {
		return "対人ｶｼﾞﾉをﾌﾟﾚｲ中です";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} が席に着きました$leader_mes";
	}
}

#================================================
# 参加するﾌｫｰﾑ
#================================================
#sub participate_form {
#	print qq|<form method="$method" action="$this_script" name="form">|;
#	print &create_submit("participate", "参加する");
#	print qq|</form>|;
#}

#================================================
# 対人ｶｼﾞﾉに参加する
#================================================
sub _participate { # 「参加する」処理
	my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;

	my @members = ();
	my $is_find = 0;
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ﾍｯﾀﾞｰ
	my @participants = &get_members($head[$_participants]);

	# ｺｲﾝがﾚｰﾄに足りていて募集人数埋まっておらず開始前のｹﾞｰﾑに参加していない
	my $is_participate = @participants ? ($coin_lack || $head[$_rate] <= $m{coin}) : ($coin_lack || $in_rate <= $m{coin});
	$is_participate = $is_participate && !$head[$_state] && $m{c_turn} == 0 && @participants < $max_entry;

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$is_find = 1;
			if ($is_participate) { # 参加条件を満たしている
				splice(@members, @participants, 0, "$time<>$mname<>$maddr<>1<>$m_value<>$m_stock<>\n"); # ﾒﾝﾊﾞｰﾌｧｲﾙ上で参加順を表現するために参加者の後ろに移動
			}
			else { push @members, "$time<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"; }
		}
		else { push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"; }
	}
	unless ($is_find) { # 長期離席していたなど、ﾒﾝﾊﾞｰﾌｧｲﾙ上から消えていた場合
		splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>1<>$m_value<>$m_stock<>\n") if $is_participate;
	}

	my $leader_mes = '';
	if ($is_participate) { # 参加条件を満たしている
		unless (@participants) { # 参加者がいないなら親
			# ｹﾞｰﾑ毎のｵﾘｼﾞﾅﾙﾍｯﾀﾞｰを設定
			$head[$_] = $tmp_head[$_-$_header_size] for ($_header_size .. ($_header_size+$header_size-1));

			$head[$_rate] = $in_rate;
			$head[$_participants] .= "$m{name},";
			$leader_mes = " ﾚｰﾄ:$head[$_rate]";
			$head[$_lastupdate] = $time;
		}
		else {
			$head[$_participants] .= "$m{name},";
			$head[$_lastupdate] = $time;
		}
		$head[$_participants_datas] .= &d_to_s($m{name}, $m_value, $m_stock);
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($head[$_state]) {
		return "すでにｹﾞｰﾑが始まっています";
	}
	elsif ($m{c_turn}) {
		return "すでに参加しています";
	}
	elsif ($max_entry <= @participants) {
		return "すでに参加枠が埋まっています";
	}
	elsif (!$coin_lack && $m{coin} < $head[$_rate]) {
		return "ｺｲﾝがﾚｰﾄに足りていません";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} が席に着きました$leader_mes";
	}
}

#================================================
# 参加中の対人ｶｼﾞﾉから離れる
#================================================
sub _observe { # 「参加しない」処理
	$mes .= "_observe<br>";
	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my $is_observe = !$head[$_state] && $m{c_turn} == 1; # 募集中のｹﾞｰﾑに参加している
	my $me = '';

	if ($is_observe) {
		$head[$_participants] = '';
		$head[$_participants_datas] = '';
	}

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if (!$head[$_state] && $mturn == 1) { # 募集中のｹﾞｰﾑに参加している
			if ($m{name} eq $mname) {
				$me = "$time<>$mname<>$maddr<>0<><><>\n";
			}
			else {
				$head[$_participants] .= "$mname,";
				$head[$_participants_datas] .= &d_to_s($mname, $mvalue, $mstock);
				push @members, $line;
			}
		}
		else {
			push @members, $line;
		}
	}
	my @participants = &get_members($head[$_participants]);
	if ($me) {
		splice(@members, @participants, 0, $me); # ﾒﾝﾊﾞｰﾌｧｲﾙ上で参加順を表現しているので、席を離れたら参加者の後ろに移動
	}
	elsif ($is_observe) {
		splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>0<><><>\n"); # ﾒﾝﾊﾞｰﾌｧｲﾙ上で参加順を表現しているので、席を離れたら参加者の後ろに移動
	}

	my $is_reset = 0;
	unless ($head[$_participants]) { # ﾒﾝﾊﾞｰの最後の一人が席を離れたらﾘｾｯﾄ
		$is_reset = GAME_RESET;
		&init_header(\@head);
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($head[$_state]) {
		return "すでにｹﾞｰﾑが始まっています";
	}
	elsif ($m{c_turn} == 0) {
		return "ｹﾞｰﾑに参加していません";
	}
	else {
		$m{c_turn} = 0;
		&write_user;
		my $result_mes = "$m{name} が席を離れました";
		if ($is_reset eq GAME_RESET) {
			&system_comment("$m{name} が席を離れたためｹﾞｰﾑをﾘｾｯﾄしました");
			$result_mes = '';
		}
		return $result_mes;
	}
}

#================================================
# 開始する・参加しないﾌｫｰﾑ
#================================================
sub _start_game_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	my @participants = &get_members($participants);

	if ($participants[0] eq $m{name} && $min_entry <= @participants && @participants <= $max_entry) { # 参加者が必要十分なら開始ﾎﾞﾀﾝ表示
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("_start_game", "開始する");
		print qq|</form>|;
	}
	elsif ($participants[0] ne $m{name} && $min_entry <= @participants && @participants <= $max_entry) {
		print "親のｹﾞｰﾑ開始を待っています";
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("_observe", "参加しない");
	print qq|</form>|;
}

#================================================
# 開始の共通処理
#================================================
sub _start_game {
	my @members = ();
	my @game_members = ();

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @old_head = split /<>/, $head_line;

	# ﾌｧｲﾙﾊﾝﾄﾞﾙ、ﾍｯﾀﾞｰ、全ﾌﾟﾚｲﾔｰ、全参加者
	&start_game($fh, \$head_line, \@members, \@game_members);

	unshift @members, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;


	if (!$old_head[$_state]) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 2;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '2');
			}
		}
	}
	return '勝負！' if !$old_head[$_state];
}

#================================================
# 開始する処理 実際のファイル操作は _casino_funcs.cgi _start_game
#================================================
sub reset_members {
	my $ref_members = shift;
	for my $i (0 .. $#$ref_members) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $ref_members->[$i];
		$ref_members->[$i] = "$mtime<>$mname<>$maddr<>0<><><>\n";
	}
}

#================================================
# 開始の共通処理
#================================================
=pod
sub _start_game {
	my (@game_members) = @_;
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
=cut
#================================================
# ﾀｰﾝの切り替え
#================================================
sub change_turn {
	my $participants = shift;
#	$mes .= "<br>member $participants";
	my $new_members = '';#"$participants[0],"; #$$participants = '';
	if ($participants) {
		my @participants = &get_members($participants);
		for my $i (1 .. $#participants) {
	#		$mes .= "i $i<br>";
			$new_members .= "$participants[$i],";# for (0 .. $#participants);
		}
		$new_members .= "$participants[0],";
	}
#	push @participants, splice(@participants, 0, 1);
#	my $new_members = ''; #$$participants = '';
#	$new_members .= "$participants[$_]," for (0 .. $#participants);
	return $new_members;
#	$$participants .= "$participants[$_]," for (0 .. $#participants);
#	$$participants =~ s/^(.*?),(.*)/$2$1,/; # 操作中のﾌﾟﾚｲﾔｰを最後尾に移動
}

#================================================
# ｺｲﾝの増減
#================================================
sub coin_move{
# 811275
# 500611
	my ($add_coin, $name, $no_system_comment) = @_;
	return 0 if $add_coin == 0 || $add_coin eq '';
	return 0 unless &you_exists($name);

	# 所持ｺｲﾝの取得
	my $m_coin = $m{coin};
	if ($name ne $m{name}) { # 所持ｺｲﾝの書き換え対象が他人なら
		my %datas1 = &get_you_datas($name);
		$m_coin = $datas1{coin};
	}

	# 移動できるｺｲﾝ数の取得
	my $ret_v;
	if ($m_coin + $add_coin < 0) { # 所持ｺｲﾝ + 払うｺｲﾝ でマイナスになるなら
		$ret_v = -1 * $m_coin; # 払うｺｲﾝは所持ｺｲﾝが限度
		$m_coin = 0; # 所持ｺｲﾝは 0
	}
	elsif (2500000 < ($m_coin_ + $add_coin)) { # 所持ｺｲﾝ + 得るｺｲﾝ が 2500000 を超えるなら
		$ret_v = (2500000 - $m_coin); # 得るｺｲﾝは 2500000 が限度
		$m_coin = 2500000; # 所持ｺｲﾝは 2500000
	}
	else { # ｺｲﾝの移動で所持できるｺｲﾝの上限や下限に引っかからない
		$ret_v = $add_coin;
		$m_coin += $add_coin;
	}

	# 所持ｺｲﾝの設定
	if ($name eq $m{name}) {
		$m{coin} = $m_coin;
		&write_user;
	}
	else {
		&regist_you_data($name, 'coin', $m_coin);
	}
	&system_comment("$name 移動させたいｺｲﾝ $add_coin 移動させたｺｲﾝ $ret_v 所持ｺｲﾝ $m_coin");

=pod
	if ($name eq $m{name}) {
		if ($m{coin} + $add_coin < 0) { # 所持ｺｲﾝ + 払うｺｲﾝ でマイナスになるなら
			$ret_v = -1 * $m{coin}; # 払うｺｲﾝは所持ｺｲﾝが限度
		}
		elsif (2500000 < ($m{coin} + $add_coin)) { # 所持ｺｲﾝ + 得るｺｲﾝ が 2500000 を超えるなら
			$ret_v = (2500000 - $m{coin}); # 得るｺｲﾝは 2500000 が限度
		}
		else { # ｺｲﾝの移動で所持できるｺｲﾝの上限下限に引っかからない
			$ret_v = $add_coin;
		}
		$m{coin} += $ret_v;
		&system_comment("$m{name} 移動させたいｺｲﾝ $add_coin 実際に移動させるｺｲﾝ $ret_v");
		&write_user;
	}
	else {
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $add_coin; # 所持ｺｲﾝ + 支払われる(支払う)ｺｲﾝ

		if ($temp < 0){ # 所持ｺｲﾝ + 払うｺｲﾝ でマイナスになるなら
			$temp = 0; # 所持ｺｲﾝ没収
			$ret_v = -1 * $datas1{coin}; # 払うｺｲﾝは所持ｺｲﾝが限度
		}
		elsif (2500000 < $temp) { # 所持ｺｲﾝ + 得るｺｲﾝ が 2500000 を超えるなら
			$ret_v = (2500000 - $datas1{coin}); # 得るｺｲﾝは 2500000 が限度
		}
		else { # ｺｲﾝの移動で所持できるｺｲﾝの上限下限に引っかからない
			$ret_v = $add_coin;
			&system_comment("$name 移動させたいｺｲﾝ $add_coin 実際に移動させるｺｲﾝ $ret_v");
		}
		&regist_you_data($name,'coin',$temp);
		&system_comment("$name 持ちｺｲﾝ $temp");
	}
=cut
#	$m_coin = -100
#	50 - 100
#	$ret_v = -50
#	

	unless ($no_system_comment) {
		if (-1 < $ret_v) { # 移動させたｺｲﾝがマイナスではない
			&system_comment("$name は $ret_v ｺｲﾝ得ました");
		}
		else { # 移動させたｺｲﾝがマイナス
			my $temp = -1 * $ret_v;
			&system_comment("$name は $temp ｺｲﾝ払いました");
		}
	}

	# 支払われる(支払う)ｺｲﾝよりも支払われた(支払った)ｺｲﾝが多い
	# 実際に後者が前者より多くなるのはマイナスでしか考えられない（100万勝って150万貰えることはない）
	# 150万負けて100万しか支払えなかったような場合は -150万 < -100万 となり後者のが大きくなる
	# でも一応マイナスなのか確認
	if ($add_coin < 0 && $ret_v < 0 && $add_coin < $ret_v) {
		$add_coin *= -1;
		my $diff = ($add_coin + $ret_v) * 10;
		&system_comment("プールから持ち出されるｺｲﾝ $diff");

		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_fileが開けません");
			eval { flock $fh, 2; };

			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff if 0 < ($pool - $diff);
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}

	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# 存在しない場合はスキップ
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name は $mes_as として $prize を獲得しました");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name が $mes_news</font>|);
	}
}

sub system_comment{
	my $s_mes = shift;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };

	# ｵｰﾄﾘﾝｸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>システムメッセージ<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# 対人ｶｼﾞﾉ関係の変数を初期化
#================================================
sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

#================================================
# 対人ｶｼﾞﾉ関係の変数を初期化(複数ﾕｰｻﾞｰ)
#================================================
sub you_lot_c_reset {
	my @names = @_;

	my @data = (
		['c_turn', 0],
		['c_value', 0],
		['c_stock', 0],
	);

	for $name (@names) {
		if ($name eq $m{name}) {
			$m{c_turn} = $m{c_value} = $m{c_stock} = 0;
			&write_user;
		}
		else {
			&regist_you_array($datas{name}, @data);
		}
	}
}

#================================================
# サブミットボタン formタグの間に挟む
#================================================
sub create_submit {
	my ($mode, $value) = @_;
	my $result_str = '';
	$result_str .= qq|<input type="hidden" name="mode" value="$mode">|;
	$result_str .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$result_str .= qq|<input type="hidden" name="guid" value="ON">|;
	$result_str .= qq|<input type="submit" value="$value" class="button_s">|;
	return $result_str;
}

#================================================
# セレクトメニュー formタグの間に挟む
#================================================
sub create_select_menu {
	my ($name, $select, @menus) = @_;
	my $result_str = '';
	$result_str .= qq|<select name="$name" class="menu1">|;
	for my $i (0 .. $#menus) {
		my $select_str = ' selected' if $i == $select;
		$result_str .= qq|<option value="$i"$select_str>$menus[$i]</option>| if $menus[$i] <= $m{coin};
	}
	$result_str .= qq|</select>|;
	return $result_str;
}

#================================================
# ラジオボタン formタグの間に挟む
#================================================
sub create_radio_button {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="radio" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

#================================================
# チェックボックス formタグの間に挟む
#================================================
sub create_check_box {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="checkbox" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

sub get_members {
	my @members = split /,/, shift; # ﾒﾝﾊﾞｰはｺﾝﾏ区切り
	return @members;
}
sub remove_member {
	my ($game_members, $remove_name) = @_;
	my @game_members = &get_members($game_members);
	my $new_game_members = '';
	for my $i (0 .. $#game_members) {
		$new_game_members .= "$game_members[$i]," if $game_members[$i] ne $remove_name;
	}
	return $new_game_members;
}

sub is_member {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
#	my $is_find = 0;
	for my $i (0 .. $#game_members) {
		return 1 if $game_members[$i] eq $find_name;
#		if ($find_name eq $game_member) {
#			$is_find = 1;
#			last;
#		}
	}
	return 0;
}

sub is_my_turn {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
	return $find_name eq $game_members[0];

#	my ($target_str, $find_str) = @_;
#	$find_str = unpack 'H*', $find_str;
#	return $target_str =~ "^$find_str,";
}

sub get_member_datas {
	my @member_datas = split /;/, shift;
#	$members[$_] = pack 'H*', $members[$_] for (0 .. $#members);
	return @member_datas;
}

sub remove_member_datas {
	my ($game_member_datas, $remove_name) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		$new_game_member_datas .= "$game_member_datas[$i];" if $game_member_data[0] ne $remove_name;
	}
	return $new_game_member_datas;
}

sub update_member_datas {
	my ($game_member_datas, $name, $value, $stock) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		if ($game_member_data[0] eq $name) {
			$game_member_datas[$i] = "$name:$value:$stock";
		}
		$new_game_member_datas .= "$game_member_datas[$i];";
	}
	return $new_game_member_datas;
}

sub esc4re {
	my $str = shift;
	$str =~ s/([\x21\x24-\x26\x28-\x2b\x2e\x2f\x3f\x40\x5b-\x5e\x7b-\x7d])/\\$1/g if $str;
	return $str;
}

sub is_match {
	my ($target_str, $find_str) = @_;

	$target_str = &esc4re($target_str);
	$find_str = &esc4re($find_str);
	return $target_str =~ $find_str;
}

1;#削除不可
