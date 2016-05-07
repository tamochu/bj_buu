#================================================
# ﾁﾝﾁﾛﾘﾝ
#================================================
require './lib/_casino_funcs.cgi';

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

sub get_member {
	my $is_find = 0;
	my $leave_name = '';
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
				&you_c_reset($mname);
			}else {
				next;
			}
		}
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
	
	if($leave_name){
		&reset_game($leave_name);
	}elsif($leader && !$leader_find){
		&reset_game;
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember);
}

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

	return("相手の番です") if $state ne $m{name};
	
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

sub make_leader {
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

sub reset_game{
	my $leave_name = shift;
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	$m{c_turn} = 0;
	&write_user;
	my $eplayer = '';
	my $ev = 0;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if($leave_name ne '' && $mturn){
			if($mname eq $leave_name){
				$ev = -1 * &coin_move(-1*$max_bet, $mname);
			}else{
				$eplayer = $mname;
			}
		}
		if($mturn){
			&you_c_reset($mname);
		}
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	if ($eplayer ne '') {
		&coin_move($ev, $eplayer);
	}
	
	$state = '';
	$leader = '';
	$max_bet = 0;
	unshift @members, "$leader<>$max_bet<>$state<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
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

sub hb_count {
    my ($m_number, $y_number) = @_;
	my @number = (int($m_number / 100), int($m_number / 10) % 10, $m_number % 10);
	my @answer = (int($y_number / 100), int($y_number / 10) % 10, $y_number % 10);
	my $hit = 0;
	my $blow = 0;
	for my $i (0..2){
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

1;#削除不可
