#================================================
# こいこい
#================================================
@rates = (100, 1000, 3000, 10000, 30000);
require './lib/_casino_funcs.cgi';

sub run {
	if ($in{mode} eq "play") {
	    $in{comment} = &play_card;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "continue") {
	    $in{comment} = &koikoi;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "win_teyaku") {
	    $in{comment} = &win_game(1);
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "win") {
	    $in{comment} = &win_game(0);
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "leader") {
	    $in{comment} = &make_leader;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "participate") {
	    $in{comment} = &participate;
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
	    $in{comment} = &reset_game($m{name});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "result_table") {
		&result_table;
		return;
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $rate, $waiting, $state, $wmember) = &get_member;
	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
		
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="result_table">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="結果一覧" class="button_s"></form><br>|;
	}elsif($m{name} ne $leader) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="exit">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="やめる" class="button_s"></form><br>|;
	}
	if ($leader && &is_player) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="reset">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="ちゃぶ台返し" class="button_s"></form><br>|;
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
	print $leader eq '' ? qq|親:募集中 レート:<br>|:qq|親:$leader レート:$rate 対戦相手:$wmember<br>|;
	if($leader){
		&print_field;
		print qq|<br>|;
		&print_gotten;
		if(($state eq $m{name} || $state eq $m{name}.'_山札') && $m{c_turn}){
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="play">|;
			&print_hand;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="札を出す" class="button_s"></form><br>|;
			
			if (&is_teyaku) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="win_teyaku">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="手上がり" class="button_s"></form><br>|;
			}
		}elsif(($state eq $m{name}.'_こいこい' || $state eq $m{name}.'_山札_こいこい') && $m{c_turn}){
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="continue">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="こいこい" class="button_s"></form><br>|;
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="win">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="終了" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="参加する" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} eq $leader && $in{mode} ne 'leader' && $waiting) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="start">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="開始" class="button_s"></form><br>|;
		}
		&print_my_hand;
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|レート<select name="rate" class="menu1">|;
		for my $i(0..$#rates){
			print qq|<option value="$i">$rates[$i]</option>|;
		}
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

sub result_table {
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	
	print qq|<script type="text/javascript" src="$htmldir/jquery.tablesorter.js?$jstime"></script>\n|;
	print <<'EOM';
<script type="text/javascript">
	$(function() {
		$("#result").tablesorter();
	});
</script>
EOM
	print qq|<table class="tablesorter" id="result">|;
	print qq|<thead><tr><th>親</th><th>勝</th><th>負</th><th>手役</th><th>文数</th><th>こいこい</th><th>レート</th><th>ｺｲﾝ</th><th>日付</th></tr></thead>|;
	print qq|<tbody>|;
	open my $fhr, "< $logdir/koikoi_result.cgi" or &error('結果ﾌｧｲﾙが開けません'); 
	while (my $line = <$fhr>) {
		my($leader, $win, $lose, $yaku, $hand_value, $koikoi, $rate, $mcoin, $rtime) = split /<>/, $line;
		my ($rsec, $rmin, $rhour, $rmday, $rmon, $ryear, $rwday, $ryday, $risdst) = localtime($rtime);
		$ryear += 1900;
		$rmon++;
		my $rdate = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$ryear,$rmon,$rmday,$rhour,$rmin,$rsec);
		print qq|<tr><td>$leader</td><td>$win</td><td>$lose</td><td>$yaku</td><td>$hand_value</td><td>$koikoi</td><td>$rate</td><td>$mcoin</td><td>$rdate</td></tr>|;
	}
	close $fhr;
	print qq|</tbody>|;
	print qq|</table>|;
}

sub get_member {
	my $is_find = 0;
	my $leave_name = '';
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	push @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$leave_name = $mname if $state ne 'waiting';
				&regist_you_data($mname,'c_turn',0);
				&regist_you_data($mname,'c_value',0);
				&regist_you_data($mname,'c_stock',0);
			}else {
				next;
			}
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
		if ($mturn > 0 && $mname ne $leader){
			$waiting++;
			$wmember = $mname;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	if($leave_name){
		&reset_game($leave_name);
	}
	my $member_c = @members - 1;
	return ($member_c, $member, $leader, $rate, $waiting, $state, $wmember);
}

sub play_card {
	my $e_name;
	my $e_hand;
	my ($pre_hand_value, $pre_yaku) = &h_value($m{c_value});
	my $hand_value;
	my $yaku;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	my @month = (0,0,0,0,0,0,0,0,0,0,0,0);
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_hand = $mstock;
		}
	}
	close $fh;
	return("相手の番です") if ($state ne $m{name} && $state ne $m{name}.'_山札');
	
	if($in{card}){
		my @deck_cards = split /,/, $deck;
		my @fields = split /,/, $field_card;
		my @hand_cards = split /,/, $m{c_stock};
		my @new_fields = ();
		my @new_hands = ();
		for my $card (@fields){
			$month[int($card/10)-1]++;
		}
		if($in{card} =~ /(\d+)_(\d+)/){
			my $rm_hand = $1;
			my $rm_card = $2;
			for my $card (@hand_cards){
				next if $card == $rm_hand;
				next if ($card % 10 > 4 || $card % 10 == 0 || $card < 0 || $card > 124);
				push @new_hands, $card;
			}
			if(@new_hands > 1){
				$m{c_stock} = $new_hands[0];
				for my $i (1..$#new_hands){
					$m{c_stock} .= ",$new_hands[$i]";
				}
			}elsif(@new_hands == 1){
				$m{c_stock} = $new_hands[0];
			}else{
				$m{c_stock} = '';
			}
			if($m{c_value}){
				if($month[int($rm_hand/10)-1] == 3){
					$t_month1 = int($rm_hand/10)*10 + 1;
					$t_month2 = int($rm_hand/10)*10 + 2;
					$t_month3 = int($rm_hand/10)*10 + 3;
					$t_month4 = int($rm_hand/10)*10 + 4;
					$m{c_value} .= ",$t_month1,$t_month2,$t_month3,$t_month4";
				}else{
					$m{c_value} .= ",$rm_hand,$rm_card";
				}
			}else{
				if($month[int($rm_hand/10)-1] == 3){
					$t_month1 = int($rm_hand/10)*10 + 1;
					$t_month2 = int($rm_hand/10)*10 + 2;
					$t_month3 = int($rm_hand/10)*10 + 3;
					$t_month4 = int($rm_hand/10)*10 + 4;
					$m{c_value} = "$t_month1,$t_month2,$t_month3,$t_month4";
				}else{
					$m{c_value} = "$rm_hand,$rm_card";
				}
			}
			for my $card (@fields){
				next if $card == $rm_card;
				if($month[int($rm_hand/10)-1] == 3){
					$t_month1 = int($rm_hand/10)*10 + 1;
					$t_month2 = int($rm_hand/10)*10 + 2;
					$t_month3 = int($rm_hand/10)*10 + 3;
					$t_month4 = int($rm_hand/10)*10 + 4;
					next if $card == $t_month1;
					next if $card == $t_month2;
					next if $card == $t_month3;
					next if $card == $t_month4;
				}
				next if ($card % 10 > 4 || $card % 10 == 0 || $card < 0 || $card > 124);
				push @new_fields, $card;
			}
			if(@new_fields > 1){
				$field_card = $new_fields[0];
				for my $i (1..$#new_fields){
					$field_card .= ",$new_fields[$i]";
				}
			}elsif(@new_fields == 1){
				$field_card = $new_fields[0];
			}else{
				$field_card = '';
			}
		}else{
			my $rm_hand = $in{card};
			for my $card (@hand_cards){
				next if $card == $rm_hand;
				next if ($card % 10 > 4 || $card % 10 == 0 || $card < 0 || $card > 124);
				push @new_hands, $card;
			}
			if(@new_hands > 1){
				$m{c_stock} = $new_hands[0];
				for my $i (1..$#new_hands){
					$m{c_stock} .= ",$new_hands[$i]";
				}
			}elsif(@new_hands == 1){
				$m{c_stock} = $new_hands[0];
			}else{
				$m{c_stock} = '';
			}
			push @fields, $rm_hand;
			for my $card (@fields){
				next if ($card % 10 > 4 || $card % 10 == 0 || $card < 0 || $card > 124);
				push @new_fields, $card;
			}
			if(@new_fields > 1){
				$field_card = $new_fields[0];
				for my $i (1..$#new_fields){
					$field_card .= ",$new_fields[$i]";
				}
			}elsif(@new_fields == 1){
				$field_card = $new_fields[0];
			}else{
				$field_card = '';
			}
		}
		if($state eq $m{name}){
			my $d_card = shift @deck_cards;
			$deck = shift @deck_cards;
			for my $card (@deck_cards){
				$deck .= ",$card";
			}
			if($m{c_stock}){
				$m{c_stock} .= ",$d_card";
			}else{
				$m{c_stock} = $d_card;
			}
			$state = $m{name} . '_山札';
		}else{
			$state = $e_name;
		}
		&write_user;
		($hand_value, $yaku) = &h_value($m{c_value});
		unless($e_hand || $m{c_stock}){
			&no_game;
#			&leader_win unless ($koikoi);
			$reset_flag = 1;
		}
		if($hand_value > $pre_hand_value){
			if($state eq $e_name){
				$state = $m{name}.'_山札_こいこい';
			}else{
				$state = $m{name}.'_こいこい';
			}
			$reset_flag = 0;
		}
		unshift @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		print $fh @members;
		close $fh;
	}
	
	if($reset_flag){
		&reset_game;
	}
	
	return ($ret_mes);
}

sub koikoi {
	my $e_name;
	my $e_hand;
	my $ret_mes = 'こいこい';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_hand = $mstock;
		}
	}
	close $fh;
	return("相手の番です") if ($state ne $m{name}.'_こいこい' && $state ne $m{name}.'_山札_こいこい');
	
	if($state eq $m{name}.'_こいこい'){
		$state = $m{name}.'_山札';
	}else{
		$state = $e_name;
	}
	unless($e_hand || $m{c_stock}){
		$reset_flag = 1;
	}
	$koikoi++;
	unshift @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	print $fh @members;
	close $fh;
	
	if($reset_flag){
		&reset_game;
	}
	
	return ($ret_mes);
}

sub win_game {
	my $teyaku = shift;
	my $hand_value;
	my $yaku;
	my $e_name;
	my $ret_mes = '';
	my @members = ();
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
		}
	}
	close $fh;
	($hand_value, $yaku) = &h_value($m{c_value});
	if ($teyaku) {
		my $mteyaku = &is_teyaku;
		if ($mteyaku eq '1') {
			$hand_value = 6;
			$yaku = '手四';
		} elsif ($mteyaku eq '2') {
			$hand_value = 6;
			$yaku = 'くっつき';
		}
	}
	$ret_mes .= "$yaku $hand_value 文 勝利";
	my $mcoin = $rate*$hand_value;
	if($koikoi){
		for (1..$koikoi){
			$mcoin *= 2;
		}
	}
	open my $fhr, ">> $logdir/koikoi_result.cgi" or &error('結果ﾌｧｲﾙが開けません'); 
	print $fhr "$leader<>$m{name}<>$e_name<>$yaku<>$hand_value<>$koikoi<>$rate<>$mcoin<>$time<>\n";
	close $fhr;
	my $cv = &coin_move(-1*$mcoin, $e_name);
	&coin_move(-1*$cv, $m{name});
	$state = '';
	$leader = '';
	$rate = 0;
	unshift @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	print $fh @members;
	close $fh;
	&reset_game;
	
	return ($ret_mes);
}

sub no_game {
	my $hand_value;
	my $yaku;
	my $e_name;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
		}
	}
	close $fh;
	open my $fhr, ">> $logdir/koikoi_result.cgi" or &error('結果ﾌｧｲﾙが開けません'); 
	print $fhr "$leader<>$m{name}<>$e_name<>つかず<>0<>$koikoi<>$rate<>0<>$time<>\n";
	close $fhr;
}

sub leader_win {
	my $e_name;
	my $ret_mes = '';
	my @members = ();
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $leader){
			$e_name = $mname;
		}
	}
	close $fh;
	&system_comment("親権 5 文");
	&coin_move($rate*5, $leader);
	&coin_move(-1*$rate*5, $e_name);
	$state = '';
	$leader = '';
	$rate = 0;
	unshift @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	open my $fh, "> ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	print $fh @members;
	close $fh;
	&reset_game;
	
	return ($ret_mes);
}

sub print_hand {
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	close $fh;
	my @field_cards = split /,/, $field_card;
	my @hand_cards = split /,/, $m{c_stock};
	
	if($state eq $m{name}.'_山札'){
		my $d_card = pop @hand_cards;
		@hand_cards = ($d_card);
	}
	my $first_card = 1;
	for my $hcard (@hand_cards){
		next unless($hcard);
		my $match_card = 0;
		for my $fcard (@field_cards){
			next unless($fcard);
			if(int($hcard / 10) == int($fcard / 10)){
				my $gif_str = &num_to_gif($hcard);
				$gif_str .= &num_to_gif($fcard);
				if($first_card){
					print qq|<input type="radio" name="card" value="${hcard}_${fcard}" selected>$gif_str<br>|;
					$first_card = 0;
				}else{
					print qq|<input type="radio" name="card" value="${hcard}_${fcard}">$gif_str<br>|;
				}
				$match_card = 1;
			}
		}
		unless($match_card){
			my $gif_str = &num_to_gif($hcard);
			if($first_card){
				print qq|<input type="radio" name="card" value="$hcard" selected>$gif_str<br>|;
				$first_card = 0;
			}else{
				print qq|<input type="radio" name="card" value="$hcard">$gif_str<br>|;
			}
		}
	}
}

sub print_my_hand {
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	close $fh;
	my @hand_cards = split /,/, $m{c_stock};
	my $d_card;
	
	if($state eq $m{name}.'_山札' || $state eq $m{name}.'_こいこい'){
		$d_card = pop @hand_cards;
	}
	print qq|<br>手札：|;
	for my $hcard (@hand_cards){
		next unless($hcard);
		next if $hcard == $d_card;
		my $gif_str = &num_to_gif($hcard);
		print qq|$gif_str|;
	}
}

sub print_field {
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	close $fh;
	my @field_cards = split /,/, $field_card;
	my @decks = split /,/, $deck;
	my $num_deck = @decks;
	
	print qq|山札 $num_deck 枚<br>|;
	print qq|こいこい $koikoi 回<br>|;
	for my $card (@field_cards){
		my $gif_str = &num_to_gif($card);
		print qq|$gif_str|;
	}
}

sub print_gotten {
	my $e_gotten;
	my $m_gotten;
	my $player = '';
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mturn > 0){
			if($mname eq $leader){
				$m_gotten = $mvalue;
			}else{
				$e_gotten = $mvalue;
				$player = $mname;
			}
		}
	}
	close $fh;
	
	my @m_cards = split /,/, $m_gotten;
	my @e_cards = split /,/, $e_gotten;
	print qq|<br>$leader：|;
	for my $card (@m_cards){
		my $gif_str = &num_to_gif($card);
		print qq|$gif_str|;
	}
	print qq|<br>$player：|;
	for my $card (@e_cards){
		my $gif_str = &num_to_gif($card);
		print qq|$gif_str|;
	}
}

sub make_leader {
	my @number;
	return("ｺｲﾝがありません") if $m{coin} <= 0;
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
#		$rate = $m{coin};
		$rate = $rates[$in{rate}];
		$state = 'waiting';
		$m{c_turn} = 1;
		$m{c_value} = '';
		$m{c_stock} = '';
		&write_user;
	}
	push @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ("$leader が親です レート:$rate");
}

sub start_game{
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	$state = $leader;
	$koikoi = 0;
	my $e_card = '';
	while (1) {
		my @decks = &shuffled_deck;
		my @mmonth = (0,0,0,0,0,0,0,0,0,0,0,0);
		$field_card = shift @decks;
		$mmonth[int($field_card / 10) - 1]++;
		for(2..8){
			my $card = shift @decks;
			$mmonth[int($card / 10) - 1]++;
			$field_card .= ",$card";
		}
		my $bayon = 0;
		for my $mm (@mmonth) {
			if ($mm == 4) {
				$bayon++;
			}
		}

		$e_card = shift @decks;
		for(2..8){
			my $card = shift @decks;
			$e_card .= ",$card";
		}
		$m{c_stock} = shift @decks;
		for(2..8){
			my $card = shift @decks;
			$m{c_stock} .= ",$card";
			&write_user;
		}
		$deck = shift @decks;
		for my $card (@decks){
			$deck .= ",$card";
		}
		if ($bayon) {
			$koikoi++;
			&system_comment("場四蒔き直し");
		} else {
			last;
		}
	}
	
	push @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	while (my $line = <$fh>) {
		push @members, $line;
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			&regist_you_data($mname,'c_stock',$e_card);
		}
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
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	$m{c_turn} = 0;
	$m{c_value} = 0;
	$m{c_stock} = 0;
	&write_user;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		my $y_id = unpack 'H*', $mname;
		if(-f "$userdir/$y_id/user.cgi"){
			if($leave_name ne '' && $mturn){
				if($mname eq $leave_name){
					&coin_move(-1*$rate, $mname);
				}else{
					&coin_move($rate, $mname);
				}
			}
			if($mturn){
				&regist_you_data($mname,'c_turn',0);
				&regist_you_data($mname,'c_value',0);
				&regist_you_data($mname,'c_stock',0);
			}
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
		}else{
			next;
		}
	}
	$state = '';
	$leader = '';
	$rate = 0;
	unshift @members, "$leader<>$rate<>$state<>$field_card<>$deck<>$koikoi<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ("リセットしました");
}

sub participate{
	my @number;
	my @members = ();
	return("ｺｲﾝがありません") if $m{coin} <= 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
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
		$m{c_turn} = 1;
		$m{c_value} = '';
		$m{c_stock} = '';
		&write_user;
		return("$m{name} が席に着きました");
	}
}

sub exit_game{
	my $waiting = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
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
	$m{c_value} = 0;
	$m{c_stock} = 0;
	&write_user;
	return("$m{name} は やめました");
}

sub is_teyaku {
	my $ret = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	if ($state eq $m{name}) {
		while (my $line = <$fh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
			if ($mturn > 0 && $mname eq $m{name}) {
				my @mhand = split /,/, $mstock;
				my @mmonth = (0,0,0,0,0,0,0,0,0,0,0,0);
				for my $mh (@mhand) {
					$mmonth[int($mh / 10) - 1]++;
				}
				my $dcount = 0;
				for my $mm (@mmonth) {
					if ($mm == 4) {
						$ret = 1;
					}
					if ($mm == 2) {
						$dcount++;
					}
				}
				if ($dcount == 4) {
					$ret = 2;
				}
			}
		}
	}
	close $fh;
	return $ret;
}

sub is_player {
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $rate, $state, $field_card, $deck, $koikoi) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($mturn > 0 && $mname eq $m{name}) {
			return 1;
		}
	}
	close $fh;
	
	return 0;
}

sub h_value{
	my $hvalue = shift;
	my @cards = split /,/, $hvalue;
	my $mon = 0;
	my $yaku = '';
	
	my $kasu = 0;
	my $tan = 0;
	my $tane = 0;
	my $isc = 0;
	my $red = 0;
	my $blue = 0;
	my $kou = 0;
	my $rain = 0;
	my $glass = 0;
	my $flower = 0;
	my $moon = 0;
	for my $card (@cards){
		if($card % 10 == 1 || ($card % 10 == 2 && $card != 112) || $card == 123 || $card == 94){
			$kasu++;
		}
		if($card == 13 || $card == 23 || $card == 33 || $card == 43 || $card == 53 || $card == 63 || $card == 73 || $card == 93 || $card == 103 || $card == 112){
			$tan++;
		}
		if($card == 24 || $card == 44 || $card == 54 || $card == 64 || $card == 74 || $card == 83 || $card == 94 || $card == 104 || $card == 113){
			$tane++;
		}
		if($card == 64 || $card == 74 || $card == 104){
			$isc++;
		}
		if($card == 13 || $card == 23 || $card == 33){
			$red++;
		}
		if($card == 63 || $card == 93 || $card == 103){
			$blue++;
		}
		if($card == 14 || $card == 34 || $card == 84 || $card == 124){
			$kou++;
		}
		if($card == 114){
			$rain++;
		}
		if($card == 94){
			$glass++;
		}
		if($card == 34){
			$flower++;
		}
		if($card == 84){
			$moon++;
		}
	}
	if($kasu >= 10){
		$mon += $kasu - 9;
		$yaku .= "カス$kasu,";
	}
	if($tan >= 5){
		$mon += $tan - 4;
		$yaku .= "短$tan,";
	}
	if($tane >= 5){
		$mon += $tane - 4;
		$yaku .= "タネ$tane,";
	}
	if($red == 3){
		$mon += 5;
		$yaku .= "赤短,";
	}
	if($blue == 3){
		$mon += 5;
		$yaku .= "青短,";
	}
	if($isc == 3){
		$mon += 5;
		$yaku .= "猪鹿蝶,";
	}
	if($glass && $moon){
		$mon += 5;
		$yaku .= "月見に一杯,";
	}
	if($glass && $flower){
		$mon += 5;
		$yaku .= "花見に一杯,";
	}
	if($kou == 3){
		if($rain){
			$mon += 7;
			$yaku .= "雨四光,";
		}else{
			$mon += 5;
			$yaku .= "三光,";
		}
	}elsif($kou == 4){
		if($rain){
			$mon += 10;
			$yaku .= "五光,";
		}else{
			$mon += 8;
			$yaku .= "四光,";
		}
	}
	
	return ($mon, $yaku);
}

sub num_to_gif{
	my $i = shift;
	unless($i){
		return "";
	}
	if($i % 10 > 4 || $i % 10 == 0 || $i < 0 || $i > 124){
		return "";
	}
	return "<IMG SRC=\"hanahuda/$i.jpg\" WIDTH=30 HEIGHT=40>";
}

sub shuffled_deck{
	my @deck;
	for my $i (1..12){
		for my $j (1..4){
			push @deck, $i*10+$j;
		}
	}
	for my $i (0..47){
		my $j = int(rand(48-$i)) + $i;
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}
1;#削除不可
