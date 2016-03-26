#================================================
# ﾁﾝﾁﾛﾘﾝ
#================================================

sub run {
	if ($in{mode} eq "role") {
	    $in{comment} = &dice_role;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "l_role") {
	    $in{comment} = '親';
	    $in{comment} .= &dice_role;
	    if($m{c_turn} == 1){
		$in{comment} .= &leader_dice;
	    }
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "leader") {
	    $in{comment} = &make_leader($in{max_bet});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bet") {
	    $in{comment} = &bet($in{max_bet});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "close") {
	    $in{comment} = &play_game($in{waiting});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
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
	print $leader eq '' ? qq|親:募集中 賭け上限:<br>|:qq|親:$leader 賭け上限:$max_bet 待ち人数:$waiting<br>$wmember<br>|;

	if($leader){
		if($state eq 'playing' && $m{c_turn} > 1){
			if($m{name} eq $leader){
				if($waiting <= 0 && $in{mode} ne 'close'){
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="l_role">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="振る" class="button_s"></form><br>|;
				}
			}else {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="role">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="振る" class="button_s"></form><br>|;
			}
		}elsif($m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			my $bet_limit = $m{coin};
			print qq|<input type="text"  name="comment" class="text_box_b" value="$bet_limit"> ｺｲﾝ <input type="hidden" name="mode" value="bet"><input type="hidden" name="max_bet" value="$max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="賭ける" class="button_s"></form><br>|;
		}elsif($m{name} eq $leader && $in{mode} ne 'leader') {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="close">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="締切" class="button_s"></form><br>|;
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="leader">|;
		my $max_bet = $m{coin};
		print qq|賭け上限<input type="text" name="max_bet" value="$max_bet" class="text_box_b"> ｺｲﾝ|;
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
	my $l_is_in = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$mturn = 1;
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
			$wmember .= "$mname";
			if($mturn == 1){
				if ($mvalue == -1) {
					$wmember .= "：ヒフミ";
				}elsif ($mvalue == 0) {
					$wmember .= "：目なし";
				}elsif ($mvalue < 7) {
					$wmember .= "：$mvalue";
				}elsif ($mvalue == 7) {
					$wmember .= "：シゴロ";
				}else{
					my $v = $mvalue % 10;
					$wmember .= "：$vゾロ";
				}
			}
			$wmember .= "<br>";
		}
		$waiting++ if $mturn > 1;
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

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember);
}

sub dice_role {
	return("もう振れません") if $m{c_turn} <= 1;
	my $dice;
	my @d_set = ();
	$dice = int(rand(6)+1);
	push @d_set, $dice;
	$dice = int(rand(6)+1);
	push @d_set, $dice;
	$dice = int(rand(6)+1);
	push @d_set, $dice;
	@d_set = sort {$a <=> $b} @d_set;
	if($d_set[0] == $d_set[1]){
		$m{c_value} = $d_set[2];
		if($d_set[1] == $d_set[2]){	
			$m{c_value} += 10;
			$m{c_value} += 10 if $d_set[2] == 1;
		}
		$m{c_turn} = 1;
	}elsif($d_set[1] == $d_set[2]){
		$m{c_value} = $d_set[0];
		$m{c_turn} = 1;
	}elsif($d_set[2] == 3){
		$m{c_value} = -1;
		$m{c_turn} = 1;
	}elsif($d_set[0] == 4){
		$m{c_value} = 7;
		$m{c_turn} = 1;
	}else{
		$m{c_turn}--;
		if($m{c_turn} == 1){
			$m{c_value} = 0;
		}
	}
	&write_user;

	my $n = 4 - $m{c_turn};
	$n = $n == 3 ? 'ラスト' :$n . ' 投目';
	return ("$n $d_set[0],$d_set[1],$d_set[2]");
}

sub make_leader {
	$max_bet_input = shift;
	return("ｺｲﾝがありません") if $m{coin} < 0;
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		$max_bet = $m{coin} < $max_bet_input ? $m{coin} : $max_bet_input;
		$state = 'waiting';
		$m{c_turn} = 4;
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

sub leader_dice{
	my @members = ();
	my %sames = ();
	my $mes = "";
	my $total = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	$leader = '';
	$max_bet = 0;
	$state = '';
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if($mturn == 1 && $mname ne $m{name}){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			if ($datas{c_value} > $m{c_value}){
				$v = $datas{c_stock};
				$v *= $m{c_value} == -1 ? 2:1;
				$v *= $datas{c_value} == 21 ? 5:
				$datas{c_value} > 10 ? 3:
				$datas{c_value} == 7 ? 2:1;
			}elsif ($datas{c_value} < $m{c_value}){
				$v = $datas{c_stock} * -1;
				$v *= $datas{c_value} == -1 ? 2:1;
				$v *= $m{c_value} == 21 ? 5:
				$m{c_value} > 10 ? 3:
				$m{c_value} == 7 ? 2:1;
			}
			$total -= $v;
			$m{coin} -= $v;
			&regist_you_data($mname,'coin',$datas{coin} + $v);
			&regist_you_data($mname,'c_turn',0);
			&regist_you_data($mname,'c_value',0);
			if($v > 0){
				$mes .= "<br>$mname は $v ｺｲﾝ 勝ちました";
			}elsif($v < 0){
				$v *= -1;
				$mes .= "<br>$mname は $v ｺｲﾝ 負けました";
			}else{
				$mes .= "<br>$mname は分けです";
			}
		}

		next if $time - $limit_member_time > $mtime;
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;


	if($total > 0){
		$mes .= "<br>$m{name} は $total ｺｲﾝ の浮きです";
	}elsif($total < 0){
		$total *= -1;
		$mes .= "<br>$m{name} は $total ｺｲﾝ の沈みです";
	}else{
		$mes .= "<br>$m{name} は浮きなしです";
	}
	$m{c_turn} = 0;
	&write_user;
	return $mes;
}

sub play_game{
	my $waiting = shift;
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	$state = 'playing';
	if($waiting <= 0){
		$leader = '';
		$max_bet = 0;
		$state = '';
		$m{c_turn} = 0;
		&write_user;
	}
	push @members, "$leader<>$max_bet<>$state<>\n";
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
	return ("勝負！");
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
			$m{c_turn} = 4;
			&write_user;
			return("$m{name} は $v ｺｲﾝ 賭けました");
		}
	}
}

sub exit_game{
	if ($m{c_turn} == 4){
		$m{c_turn} = 0;
	}else {
		return("$m{name} は 既に振っています");
	}
	&write_user;
	return("$m{name} は やめました");
}

sub leader_penalty{
	my @members = ();
	my %sames = ();
	my $mes = "";
	my $sum_penalty = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	my $lname = $leader;
	$leader = '';
	$max_bet = 0;
	$state = '';
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次

		if($mturn == 1 && $mname ne $lname){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			$v = $datas{c_stock};
			$sum_penalty += $v;
			&regist_you_data($mname,'coin',$datas{coin} + $v);
			&regist_you_data($mname,'c_turn',0);
			&regist_you_data($mname,'c_value',0);
			$mes .= "<br>親が無断退席したため $mname は $v ｺｲﾝ 貰いました";
		}

		push @members, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my %datas = &get_you_datas($lname);
	&regist_you_data($lname,'coin',$datas{coin} - $sum_penalty);
	&regist_you_data($lname,'c_turn',0);
	&regist_you_data($lname,'c_value',0);
	return $mes;
}

1;#削除不可
