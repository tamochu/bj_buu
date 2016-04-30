#================================================
# 限定じゃんけん
#================================================
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

# 参加者一覧
my $all_member_file = "$logdir/espoir_member.cgi";

# ユーザーデータ
my $my_espoir_file = "$userdir/$id/espoir.cgi";

# 基準額
my $rate = 1000000;

# 出港に必要な最低プレイヤー数
my $min_espoir = 5;

unless (-f $all_member_file) {
	open my $fh, "> $all_member_file" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
	print $fh "<>0<>0<>0<>\n";
	close $fh;
}

sub run {
	my ($game_year, $all_rest_a, $all_rest_b, $all_rest_c, $participate, @all_member) = &get_state;
	
	
	if ($in{mode} eq "participate") {
		$in{comment} = &participate;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "send_star") {
		&send_star($in{to});
	}
	elsif ($in{mode} eq "send_a") {
		&send_a($in{to});
	}
	elsif ($in{mode} eq "send_b") {
		&send_b($in{to});
	}
	elsif ($in{mode} eq "send_c") {
		&send_c($in{to});
	}
	elsif ($in{mode} eq "receive") {
		&receive($in{type});
	}
	elsif ($in{mode} eq "refuse") {
		&refuse($in{type});
	}
	elsif ($in{mode} eq "check_a") {
		&check_a($in{to});
	}
	elsif ($in{mode} eq "check_b") {
		&check_b($in{to});
	}
	elsif ($in{mode} eq "check_c") {
		&check_c($in{to});
	}
	elsif ($in{mode} eq "recheck") {
		&recheck($in{hand});
	}
	elsif ($in{mode} eq "uncheck") {
		&uncheck;
	}
	elsif ($in{mode} eq "goal") {
		&goal;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if ($game_year eq $w{year}) {
		print qq|全体残り グー:$all_rest_a チョキ:$all_rest_b パー:$all_rest_c<br>|;
		if ($participate) {
			my ($rest_a, $rest_b, $rest_c, $star, $count, $year, %stack) = &get_my_state;
			print qq|残り グー:$my_rest_a チョキ:$my_rest_b パー:$my_rest_c|;
			my $no_stack = 1;
			if (@{$stack{star}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{star}}[0]からの星を受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{star}}[0]からの星を受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{a}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{a}}[0]からのグーを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{a}}[0]からのグーを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{b}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{b}}[0]からのチョキを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{b}}[0]からのチョキを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{c}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{c}}[0]からのパーを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{c}}[0]からのパーを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{check}}) {
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="recheck">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					for my $i (0..2) {
						if (($i == 0 && $rest_a <= 0) || ($i == 1 && $rest_b <= 0) || ($i == 2 && $rest_c <= 0)) {
							next;
						}
						
						print qq|<input type="radio" name="hand" value="$i">|;
						print $i == 0 ? 'グー' :
								$i == 1 ? 'チョキ' :
										'パー';
					}
					print qq|<input type="submit" value="${stack{check}}[0]と勝負" class="button_s"><br>|;
					print qq|</form>|;
				}
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="uncheck">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{check}}[0]と勝負しない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{send}}) {
				$no_stack = 0;
			}
			if ($no_stack) {
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<select name="mode">|;
					if ($rest_a > 0) {
						print qq|<option value="check_a">グーで勝負</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="check_b">チョキで勝負</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="check_c">パーで勝負</option>|;
					}
					if ($rest_a > 0) {
						print qq|<option value="send_a">グーを渡す</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="send_b">チョキを渡す</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="send_c">パーを渡す</option>|;
					}
					if ($star > 1) {
						print qq|<option value="send_star">星を渡す</option>|;
					}
					print qq|</select>|;
					print qq|相手：<input type="hidden" name="to" value="">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="送信" class="button_s"><br>|;
					print qq|</form>|;
				} else {
					if (($count > 1 && $star >= 4) ||$star >= 3) {
						print qq|<form method="$method" action="$this_script" name="form">|;
						print qq|<input type="hidden" name="mode" value="goal">|;
						print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
						print qq|<input type="submit" value="あがり" class="button_s"><br>|;
						print qq|</form>|;
					}
				}
			}
		}
	} else {
		print qq|乗船者募集中|;
		if ($participate) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="乗船" class="button_s"><br>|;
			print qq|</form>|;
		} else {
			print qq|あなたは乗船予定です。|;
		}
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;
	print qq|</form>|;

	print qq|<div id="body_mes"><font size="2">$member_c人:$member</font><br>|;
	
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment = &comment_change($bcomment, 1);
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
	print qq|</div>|;
	print qq|</td>|;
	print qq|</tr></table>|;
}
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub get_state {
	my @all_players = ();
	my $participate = 0;
	my $star;
	my $my_rest_a = 0;
	my $my_rest_b = 0;
	my $my_rest_c = 0;
	
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$participate = 1;
			}
		}
	}
	close $fh;
	
	return ($play_year, $rest_a, $rest_b, $rest_c, $participate, @all_players);
}

sub get_my_state {
	my %stack = ();
	my @star = ();
	my @a = ();
	my @b = ();
	my @c = ();
	my @check = ();
	my @send = ();
	open my $fhm, "< $my_espoir_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	my ($star, $rest_a, $rest_b, $rest_c, $count, $year) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my ($type, $name) = split /<>/, $line;
		if ($type eq '1') {
			push @star, $name;
		} elsif ($type eq '2') {
			push @a, $name;
		} elsif ($type eq '3') {
			push @b, $name;
		} elsif ($type eq '4') {
			push @c, $name;
		} elsif ($type eq '5') {
			push @check, $name;
		} else {
			push @send, $name;
		}
	}
	close $fhm;
	
	$stack{star} = \@star;
	$stack{a} = \@a;
	$stack{b} = \@b;
	$stack{c} = \@c;
	$stack{check} = \@check;
	$stack{send} = \@send;
	
	return ($rest_a, $rest_b, $rest_c, $star, $count, $year, %stack);
}

sub participate {
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	my @all_players = ();
	my $find = 0;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$find = 1;
			}
		}
	}
	close $fh;
	
	unless ($find) {
		push @all_players, $m{name};
		
		if (@all_players >= $min_espoir) {
			if ($play_year != $w{year} + 1) {
				system_comment("$play_yearにエスポワール<希望>は出港いたします。");
			}
			$play_year = $w{year} + 1;
		}
		$headline = "$play_year<>0<>0<>0<>";
		
		unshift @all_players, $headline;
		
		open my $wfh, "> $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
		for my $line (@all_players) {
			print $wfh "$line\n";
		}
		close $wfh;
		return "$m{name}が乗船しました。";
	}
	return "";
}

sub send_star {
	my $to = shift;
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_star', -1);
	&add_my_status_line($id, -1, $to);
	&add_my_status_line($to_id, 1, $m{name});
}

sub send_a {
	my $to = shift;
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_a', -1);
	&add_my_status_line($id, -2, $to);
	&add_my_status_line($to_id, 2, $m{name});
}

sub send_b {
	my $to = shift;
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_b', -1);
	&add_my_status_line($id, -3, $to);
	&add_my_status_line($to_id, 3, $m{name});
}

sub send_c {
	my $to = shift;
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_c', -1);
	&add_my_status_line($id, -4, $to);
	&add_my_status_line($to_id, 4, $m{name});
}

		&receive($in{type});
		&refuse($in{type});
		&check_a($in{to});
		&check_b($in{to});
		&check_c($in{to});
		&recheck($in{hand});
		&uncheck;
		&goal;

sub add_my_status_line {
	my $to_id = shift;
	my $type = shift;
	my $name = shift;
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	push @lines, "$type<>$name<>\n";
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
}
sub remove_my_status_line {
	my $to_id = shift;
	my $type = shift;
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	push @lines, $head_line;
	
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	push @lines, "$type<>$name<>\n";
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
}

sub change_my_status {
	my $change_id = shift;
	my $key = shift;
	my $value = shift;
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$change_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	my($star, $rest_a, $rest_b, $rest_c, $count, $year) = split /<>/, $headline;
	if ($key eq 'star') {
		$star = $value;
	} elsif ($key eq 'star_add') {
		$star += $value;
	} elsif ($key eq 'a') {
		$rest_a = $value;
	} elsif ($key eq 'a_add') {
		$rest_a += $value;
	} elsif ($key eq 'b') {
		$rest_b = $value;
	} elsif ($key eq 'b_add') {
		$rest_b += $value;
	} elsif ($key eq 'c') {
		$rest_c = $value;
	} elsif ($key eq 'c_add') {
		$rest_c += $value;
	} elsif ($key eq 'count_add') {
		$count += $value;
	} elsif ($key eq 'year') {
		$year = $value;
	}
	push @lines, "$star<>$rest_a<>$rest_b<>$rest_c<>$count<>$year<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	open my $fhw, "> $userdir/$change_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
}

sub item_or_coin {
	my ($m_coin, $name) = @_;
	
	while ($m_coin > 2500000) {
		$m_coin -= 1000000;
		&bonus($name, '', 'ﾄﾄの景品を貰いました');
	}
	&coin_move($m_coin, $name, 1);
}

1;