#================================================
# 手本引き
#================================================
require './lib/_casino_funcs.cgi';

sub run {
	if ($in{mode} eq "p_set") {
	    $in{comment} = &player_set($in{b_1} + $in{b_2}*10 + $in{b_3}*100 + $in{b_4}*1000);
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "c_open") {
		$in{comment} .= &open_card;
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
	elsif ($in{mode} eq "c_set") {
	    $in{comment} = &set_card($in{waiting});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember, $number_log) = &get_member;

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
	print $leader eq '' ? qq|親:募集中 見せ金: 目：$number_log<br>|:qq|親:$leader 見せ金:$max_bet 目：$number_log<br>$wmember<br>|;
	if($leader){
		if($state eq 'playing' && $m{c_turn} > 1){
			if($m{name} eq $leader){
				if($waiting <= 0 && $in{mode} ne 'c_set'){
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="c_open">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="開く" class="button_s"></form><br>|;
				}
			}elsif($m{c_turn} eq '5') {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="p_set">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="radio" name="b_1" value="0">やめる<br>|;
				for my $i (1..$m{c_value}){
					print qq|<input type="radio" name="b_$i" value="1" checked>1<input type="radio" name="b_$i" value="2">2<input type="radio" name="b_$i" value="3">3<input type="radio" name="b_$i" value="4">4<input type="radio" name="b_$i" value="5">5<input type="radio" name="b_$i" value="6">6<br>|;
				}
				print qq|<input type="submit" value="張る" class="button_s"></form><br>|;
			}
		}elsif($m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="comment" class="text_box_b"> ｺｲﾝ <input type="hidden" name="mode" value="bet"><input type="hidden" name="max_bet" value="$max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="radio" name="cmd" value="1" checked>1点がけ<input type="radio" name="cmd" value="2">2点がけ<input type="radio" name="cmd" value="3">3点がけ<input type="radio" name="cmd" value="4">4点がけ|;
			print qq|<input type="submit" value="賭ける" class="button_s"></form><br>|;
		}elsif($m{name} eq $leader && $in{mode} ne 'leader') {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="c_set">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="radio" name="cmd" value="0" checked>洗う<br>|;
			print qq|<input type="radio" name="cmd" value="1">1<input type="radio" name="cmd" value="2">2<input type="radio" name="cmd" value="3">3<input type="radio" name="cmd" value="4">4<input type="radio" name="cmd" value="5">5<input type="radio" name="cmd" value="6">6<br>|;
			print qq|<input type="submit" value="入れる" class="button_s"></form><br>|;
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="text"  name="comment" class="text_box_b" value="10"> ｺｲﾝ <input type="submit" value="親になる" class="button_s"></form><br>|;
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
	my $l_is_in = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$mturn = 0;
				$mvalue = 0;
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
		if ($mname eq $leader && $time - $limit_member_time < $mtime) {
		    $l_is_in = 1;
		    $waiting--;
		}
		if ($mturn > 0) {
			my @values = ($mvalue % 10, int($mvalue / 10) % 10, int($mvalue / 100) % 10, int($mvalue / 1000));
			$wmember .= "$mname：";
			if($mname ne $leader){
				if($mturn == 1){
					$wmember .= "スイチ（5.5倍）$values[0]";
				}
				elsif($mturn == 2){
					$wmember .= "ケッタツ（3.5倍）$mvalue[0] (2.0倍)$mvalue[1]";
				}
				elsif($mturn == 3){
					$wmember .= "ポンウケ（3.8倍）$mvalue[0] (1.0倍)$mvalue[1] (1.0倍)$mvalue[2]";
				}
				elsif($mturn == 4){
					$wmember .= "ソ\ウダイ（3.0倍）$mvalue[0] (1.0倍)$mvalue[1] (1.0倍)$mvalue[2] (1.0倍)$mvalue[3]";
				}else {
					$wmember .= "考え中";
				}
			}else {
				$wmember .= "親";
			}
			$wmember .= "<br>";
		}
		$waiting++ if $mturn == 5;
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

	my $member_c = @members - 1;

	if($l_is_in eq '0' && $state ne ''){
	    &leader_penalty;
	}

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember, $number_log);
}

sub make_leader {
	return("ｺｲﾝがありません") if $m{coin} < 0;
	my @members = ();
	my %sames = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		my $v;
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$v = $in{comment};
			$v = $m{coin} if $v > $m{coin};
			if($v > 0){
				&coin_move(-1 * $v, $m{name}, 1);
				$m{c_turn} = 5;
				&write_user;
			}
		}
		$max_bet = $v;
#		$max_bet = 10;
		$state = 'waiting';
	}
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
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
	&write_user;
	return ("$leader が親です 賭け上限:$max_bet");
}

sub set_card{
	my @members = ();
	my $p_mes = "入りました！";
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	$state = 'playing';
	if($cmd == 0){
		$p_mes = "洗いました。$max_bet の受かり";
		&coin_move($max_bet, $m{name}, 1);
		$leader = '';
		$max_bet = 0;
		$state = '';
		$m{c_turn} = 0;
	}else {
		$m{c_value} = $cmd;
	}
	&write_user;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		if($m{c_turn} eq '0'){
			my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	    }else{
	    	push @members, $line;
	    }
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ($p_mes);
}

sub bet{
	my $max = shift;
	my $v;
	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		$v = $in{comment};
		$v = $m{coin} if $v > $m{coin};
		if($v > 0){
			$v = $max if $v > $max;
			$m{c_stock} = $v;
			$m{c_turn} = 5;
			$m{c_value} = $cmd;
			&write_user;
			return("$m{name} は $v ｺｲﾝ 張りました");
		}
	}
}

sub player_set {
	my $value = shift;
	my $dmes = '';
	$m{c_turn} = $m{c_value};
	$m{c_value} = $value;
	&write_user;
	my @values = ($value % 10, int($value / 10) % 10, int($value / 100) % 10, int($value / 1000));
	if($m{c_turn} == 1){
		$dmes = "スイチ（5.5倍）$values[0]";
	}
	elsif($m{c_turn} == 2){
		$dmes = "ケッタツ（3.5倍）$values[0] (2.0倍)$values[1]";
	}
	elsif($m{c_turn} == 3){
		$dmes = "ポンウケ（3.8倍）$values[0] (1.0倍)$values[1] (1.0倍)$values[2]";
	}
	else{
		$dmes = "ソ\ウダイ（3.0倍）$values[0] (1.0倍)$values[1] (1.0倍)$values[2] (1.0倍)$values[3]";
	}
	return ($dmes);
}


sub open_card{
	my @members = ();
	my %sames = ();
	my $lmes = "$m{c_value} !";
	my $total = 0;
	my $sum_win = 0;
	my %vs = ();
	my @names = ();
	my $rate = 1;

	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		my $kid = unpack 'H*', $mname;
		next unless (-f "$userdir/$kid/user.cgi");
		if($mturn ne '0' && $mturn ne '5' && $mname ne $m{name}){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			$v = $datas{c_stock};
			my @values = ($mvalue % 10, int($mvalue / 10) % 10, int($mvalue / 100) % 10, int($mvalue / 1000));
			if($mturn == 1){
				$v *= $values[0] eq $m{c_value} ? 4.5:
						-1;
			}
			elsif($mturn == 2){
				$v *= $values[0] eq $m{c_value} ? 2.5:
						$values[1] eq $m{c_value} ? 1.0:
						-1;
			}
			elsif($mturn == 3){
				$v *= $values[0] eq $m{c_value} ? 2.8:
						$values[1] eq $m{c_value} ? 0:
						$values[2] eq $m{c_value} ? 0:
						-1;
			}
			else{
				$v *= $values[0] eq $m{c_value} ? 2.0:
						$values[1] eq $m{c_value} ? 0:
						$values[2] eq $m{c_value} ? 0:
						$values[3] eq $m{c_value} ? 0:
						-1;
			}
			$v = int($v);
			push @names, $mname;
			$vs{$mname} = $v;
			$total += $v;
		}
		next if $time - $limit_member_time > $mtime;
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	if($total >= $max_bet) {
		$rate = 1.0 * $max_bet / $total;
	}
	my @new_log = (int($number_log / 100000), int($number_log / 10000) % 10, int($number_log / 1000) % 10, int($number_log / 100) % 10, int($number_log / 10) % 10, $number_log % 10);
	$number_log = $m{c_value};
	my $count = 0;
	for my $i (@new_log){
		if ($i == 0) {
			$number_log = 123456;
			last;
		}
		if ($i eq $m{c_value}) {
			if($count eq '0'){
				$lmes .= "根";
			}elsif($count eq '1'){
				$lmes .= "小戻り";
			}elsif($count eq '2'){
				$lmes .= "三間";
			}elsif($count eq '3'){
				$lmes .= "四間";
			}elsif($count eq '4'){
				$lmes .= "フルツキ";
			}else{
				$lmes .= "奥";
			}
			next;
		}
		$number_log *= 10;
		$number_log += $i;
		$count++;
	}
	for my $k (@names){
		my $kid = unpack 'H*', $k;
		if (-f "$userdir/$kid/user.cgi") {
			&coin_move(int($vs{$k} * $rate), $k, 1);
			&regist_you_data($k,'c_turn',0);
			if($vs{$k} > 0){
				$lmes .= "<br>$k は $vs{$k} ｺｲﾝ 勝ちました";
			}elsif($vs{$k} < 0){
				$vs{$k} *= -1;
				$lmes .= "<br>$k は $vs{$k} ｺｲﾝ 負けました";
			}else{
				$lmes .= "<br>$k は種です";
			}
		}
	}
	$max_bet -= $total;
	$state = 'waiting';
	
	if($max_bet <= 0){
		$max_bet = 0;
		$leader = '';
		$max_bet = 0;
		$state = '';
		$m{c_turn} = 0;
		&write_user;
	}
	
	shift @members;
	unshift @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return $lmes;
}


sub exit_game{
	$m{c_turn} = 0 if $m{c_turn} == 5;
	&write_user;
	return("$m{name} は やめました");
}

sub leader_penalty{
	my @members = ();
	my %sames = ();
	my $mes = "";
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	my $lname = $leader;
	my $sum_penalty = $max_bet;
	$leader = '';
	$max_bet = 0;
	$state = '';
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次

		if($mturn ne '0' && $mname ne $lname){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			$v = $datas{c_stock};
			$sum_penalty -= $v;
			&coin_move($v, $mname, 1);
			&regist_you_data($mname,'c_turn',0);
			$mes .= "<br>親が無断退席したため $mname は $v ｺｲﾝ 貰いました";
		}

		push @members, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my %datas = &get_you_datas($lname);
	&coin_move($sum_penalty, $lname, 1);
	&regist_you_data($lname,'c_turn',0);
	return $mes;
}

1;#削除不可
