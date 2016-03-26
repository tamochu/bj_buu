#================================================
# 大貧民
#================================================
my $set_flag = 0;
my @rates = (100, 1000, 10000);

sub run {
	if ($in{mode} eq "play") {
	    $in{comment} = &play_card;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "start") {
	    $in{comment} = &deal_card;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "participate") {
	    $in{comment} = &participate;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
	    &write_comment if $in{comment};
	}elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member, $turn, $rate, $state_c, $state_n, $players, $pmember, $c_player) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}else {
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
	print $turn eq '' ? qq|準備中 レート:$rate<br>$pmember<br>|:qq|ターン:$turn レート:$rate プレイ人数:$players<br><br>$pmember<br>|;

	if($m{c_turn} == 0 || ($m{c_turn} > 2 && $players == 0)){
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="participate">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="ｹﾞｰﾑに参加" class="button_s"></form><br>|;		
	}

	if($turn && !$set_flag){
		if($m{name} eq $turn){
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="play">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			&print_checkbox;
			print qq|<input type="submit" value="カードを出す" class="button_s"></form><br>|;
		}else{
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="write">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			&print_checkbox if $m{c_turn} == 2;
			print qq|</form><br>|;
		}
	}elsif($m{c_turn} == 1) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="start">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|レート<select name="rate" class="menu1">|;
		for my $i(0..$#rates){
			print qq|<option value="$i">$rates[$i]</option>|;
		}
		print qq|<br><input type="submit" value="ｹﾞｰﾑを始める" class="button_s"></form><br>|;
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
	if($set_flag){
		&game_set;
	}
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $players = 0;
	my $pmember = '';
	my $f_player = '';
	my $nt_flag = 0;
	my $this_set_flag = 0;
	my $turn_error = 1;
	my $turn_error_c = 1;
    my @num = ('3','4','5','6','7','8','9','10','J','Q','K','A','2'); # 低い順
    my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	$pmember .= "場のカード：$num[$state_n] ";
	$pmember .= $state_c == 1 ? "一枚 ":
				$state_c == 2 ? "ダブル ":
				$state_c == 3 ? "トリプル ":
				$state_c == 4 ? "革命 ":
				"その他 ";
	$pmember .= "($c_player)<br>";
	$pmember .= "状態：";
	$pmember .= "革命 " if $revolution;
	$pmember .= "イレバ " if $back;
	$pmember .= "縛り(スペード) " if $bind_s == 2;
	$pmember .= "縛り(ハート) " if $bind_h == 2;
	$pmember .= "縛り(クラブ) " if $bind_c == 2;
	$pmember .= "縛り(ダイヤ) " if $bind_d == 2;
	$pmember .= "<br>";
	
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0 && $mturn <= 2){
				if($mname eq $m{name}){
					$m{c_turn} = 0;
					$m{c_value} = 0;
					&write_user;
				}
				$mturn = 4;
				$mvalue = &lose_player;
				if($turn eq $mname){
					$nt_flag = 1;
				}
				&regist_you_data($mname,'c_turn',$mturn);
				&regist_you_data($mname,'c_value',$mvalue);
			}elsif($mturn == 0) {
				next;
			}
		}else{
			if($f_player eq ''){
				$f_player = $mname;
			}
			if($nt_flag){
				$turn = $mname;
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
		if ($mturn == 2) {
			$pmember .= "$mname";
			my @mhand = &v_to_hj($mvalue);
			my $hands = @mhand;
			$pmember .= "：$hands枚";
			if($turn eq $mname){
				$pmember .= "★";
				$turn_error = 0;
			}
			if($c_player eq $mname || $c_player eq ''){
				$turn_error_c = 0;
			}
			$pmember .= "<br>";
			$players++;
		}elsif($mturn >= 3){
				$pmember .= "$mname";
				my $rank = $mvalue;
				$pmember .= "：$rank位<br>";
		}elsif($mturn == 1){
			$pmember .= "$mname：待機中";
			$pmember .= $mvalue == 1 ? "大富豪":
						$mvalue == 2 ? "富豪":
						$mvalue == -1 ? "大貧民":
						$mvalue == -2 ? "貧民":
										"平民";
			$pmember .= "<br>";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	if($nt_flag){
		$turn = $f_player;
		if($f_player eq ''){
			$this_set_flag = 1;
		}
	}
	unshift @members, "$turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;


	if($turn && ($turn_error || $turn_error_c) && !$set_flag){
		&system_comment("ターン異常修正しました $turn_error $turn_error_c");
		my $next_flag = 1;
		my $next_turn = '';
		my $err_set_flag = 1;
		my @e_members = ();
		open my $efh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		eval { flock $efh, 2; };
		my $head_line = <$efh>;
		my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
		while (my $line = <$efh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
			push @e_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
			if($mturn == 2 && $next_flag == 1){
				$next_turn = $mname;
				$next_flag = 0;
				$c_player = '';
				$bind_s = 0;
				$bind_h = 0;
				$bind_c = 0;
				$bind_d = 0;
				$err_set_flag = 0;
			}
			if($turn eq $mname){
				$next_flag = 1;
			}
		}
		unshift @e_members, "$next_turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
		seek  $efh, 0, 0;
		truncate $efh, 0;
		print $efh @e_members;
		close $efh;
		if($err_set_flag){
			#&game_set;
		}
	}

	if($this_set_flag){
		&game_set;
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $turn, $rate, $state_c, $state_n, $players, $pmember, $c_player);
}

sub play_card {
	my @members = ();
	my %sames = ();
	my $play_flag = 0;
	my $p_set_flag = 0;
	
	return("参加してません") if $m{c_turn} <= 1;
	my @hand = &v_to_hj($m{c_value});
	my @new_hand= ();
	my @play_card = ();
	
	my @seven_g = ();
	
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back) = split /<>/, $head_line;
	close $ifh;
	return("あなたの順番ではありません") if $turn ne $m{name};
	
	for my $i (0..$#hand){
		if($in{"play_$i"}){
			push @play_card, $hand[$i];
			if($in{"play_$i"} && defined($in{"sub_$i"})){
				if($hand[$i] % 13 == 4){
					push @seven_g, $in{"sub_$i"};
				}
				if($hand[$i] % 13 == 7){
					push @ten_g, $in{"sub_$i"};
				}
			}
		}else{
			push @new_hand, $hand[$i];
		}
	}
	
	
	my ($n, $sn, $sc, @flags) = &w_pair(@play_card);
	
	if($n ne 'パス'){
		my $nhands = @new_hand;
		if($nhands == 0){
			$n = "あがり " . $n;
			$m{c_value} = &win_player;
			$m{c_turn} = 3;
			$p_set_flag = 1;
		}else{
			$m{c_value} = &h_to_vj(@new_hand);
		}
		$play_flag = 1;
	}
	&write_user;

	my $next_flag = 1;
	my $next_turn = '';
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mname eq $m{name}){
			$mturn = $m{c_turn};
			$mvalue = $m{c_value};
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		if($mturn == 2 && $next_flag == 1){
			$next_turn = $mname;
			$next_flag = 0;
		}
		if($turn eq $mname){
			$next_flag = 1;
		}
	}
	if($play_flag){
		$state_c = $sc;
		$state_n = $sn;
		$c_player = $m{name};
		$bind_s = $flags[13];
		$bind_h = $flags[14];
		$bind_c = $flags[15];
		$bind_d = $flags[16];
		
		if($flags[5] && !$p_set_flag){#八切
			$next_turn = $m{name};
			$c_player = '';
			$bind_s = 0;
			$bind_h = 0;
			$bind_c = 0;
			$bind_d = 0;
		}
		if($flags[8]){#イレブンバック
			$back = 1;
		}else{
			$back = 0;
		}
		if($flags[12] && !$p_set_flag){#２切（暫定）
			$next_turn = $m{name};
			$c_player = '';
			$bind_s = 0;
			$bind_h = 0;
			$bind_c = 0;
			$bind_d = 0;
		}
		if($state_c == 4 || ($state_c >= 6 && $state_c <= 9)){#革命
			$revolution = $revolution ? 0 : 1;
		}
	}elsif($next_turn eq $c_player){#一巡
		$c_player = '';
		$bind_s = 0;
		$bind_h = 0;
		$bind_c = 0;
		$bind_d = 0;
	}
	if($turn eq $next_turn || $p_set_flag){#1人または上がり流し
		$c_player = '';
		$bind_s = 0;
		$bind_h = 0;
		$bind_c = 0;
		$bind_d = 0;
	}
	unshift @members, "$next_turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	if($flags[4] && $play_flag && !$p_set_flag){#七渡し
		&give(@seven_g);
	}
	if($flags[7] && $play_flag && !$p_set_flag){#十捨て
		&release(@ten_g);
	}

	return $n;
}

sub deal_card {
	my $a_players;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($mturn == 1) {
			$a_players++;
		}
	}
	close $fh;

	my @members = ();
	my %sames = ();
	my @g_deck = &shuffled_deck;
	my @d_player = ();
	my $d_mes = '';
	for my $i (@g_deck){
		$d_mes .= "$i,";
	}
	my $card_no = 0;
	my $plcards = int(52 / $a_players) - 1;
	$plcards = $plcards > 7 ? 7 : $plcards;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	if($turn eq ''){
		$turn = $m{name};
		$rate = $rates[$in{rate}];
		$state_n = 0;
		$state_c = 1;
		$c_player = '';
		$revolution = 0;
		$back = 0;
		$bind_s = 0;
		$bind_h = 0;
		$bind_c = 0;
		$bind_d = 0;
		$m{c_turn} = 2;
		my @phand = ();
		for my $i ($card_no..$card_no+$plcards-1){
			push @phand, $g_deck[$i];
			if(int($g_deck[$i] / 13) == 3){
				$d_player[$g_deck[$i] % 13] = $m{name};
			}
		}
		
		@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
		$card_no += $plcards;
		$m{c_value} = &h_to_vj(@phand);
		$m{coin} -= $rate;
		&write_user;
	}
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn == 1){
			if($mname eq $m{name}){
				$m{coin} -= $rate;
				push @members, "$mtime<>$mname<>$maddr<>$m{c_turn}<>$m{c_value}<>\n";
			}else{
				my @phand = ();
				for my $i ($card_no..$card_no+$plcards-1){
					push @phand, $g_deck[$i];
					if(int($g_deck[$i] / 13) == 3){
						$d_player[$g_deck[$i] % 13] = $mname;
					}
				}
				@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
				$card_no += $plcards;
				my $d_hand = &h_to_vj(@phand);
				&regist_you_data($mname,'c_turn',2);
				&regist_you_data($mname,'c_value',$d_hand);
				my %datas = &get_you_datas($mname);
				my $red_coin = $datas{coin} - $rate;
				$red_coin = $red_coin < 0 ? 0:$red_coin;
				&regist_you_data($mname,'coin',$red_coin);
				push @members, "$mtime<>$mname<>$maddr<>2<>$d_hand<>\n";
			}
		}else {
			&regist_you_data($mname,'c_turn',0);
			&regist_you_data($mname,'c_value',0);
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
		}
	}
	for my $i (0..12){
		next unless defined($d_player[$i]);
		$turn = $d_player[$i];
		last;
	}
	unshift @members, "$turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;



#	return ("ｹﾞｰﾑを始めます$turnの番です<br>$d_mes");
	return ("ｹﾞｰﾑを始めます$turnの番です");
}

sub participate{
	return("ｺｲﾝがありません") if $m{coin} <= 0;
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	close $ifh;
	return("次のゲームに参加したいです") if $turn;
	$m{c_turn} = 1;
	$m{c_value} = 0;
	&write_user;
	return("$m{name} が参加します");
}

sub exit_game{
	if ($m{c_turn} == 1){
		$m{c_turn} = 0;
	}else {
		return("ｹﾞｰﾑが始まっています");
	}
	&write_user;
	return("$m{name} は やめました");
}

sub win_player{
	my @members = ();
	my %sames = ();

	my $players = 0;
	my $w_players = 1;
	my $l_players = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mturn >= 2) {
			$players++;
			if($mturn == 3){
				$w_players++;
			}
			if($mturn == 4){
				$l_players++;
			}
		}
	}
	close $fh;
	
	if(($rate == 0 && $players == $w_players + $l_players) || ($rate != 0 && ($players == $w_players + $l_players || $w_players >= 2))){
		$set_flag = 1;
	}
	return $w_players;
}

sub lose_player {
	my @members = ();
	my %sames = ();

	my $players = 0;
	my $w_players = 1;
	my $l_players = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	push @members, "$turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mturn >= 2) {
			$players++;
			if($mturn == 3){
				$w_players++;
			}
			if($mturn == 4){
				$l_players++;
			}
		}
	}
	my $l_value = $players - $l_players;
	close $fh;

	if($players == $w_players + $l_players){
		$set_flag = 1;
	}
	return $l_value;
}

sub error_lose{
	my $pname = shift;
	
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mname eq $pname){
			$mturn = 4;
			$mvalue = &lose_player;
			&regist_you_data($mname,'c_turn',4);
			&regist_you_data($mname,'c_value',$mvalue);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
	}
	unshift @members, "$next_turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub w_pair{
    my @num = ('3','4','5','6','7','8','9','10','J','Q','K','A','2'); # 低い順
    my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	my @pair = @_;
	my @flags = ();
	my $h_mes = '';
	my $h_state;
	my @b_suit = ();
	my $miss_bind = 0;
	my $one_suit_flag = 0;
	my $step_flag = 1;

	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	close $fh;
	
	for my $i(@pair){
		$flags[$i%13]++;
		$b_suit[int($i/13)]++;
	}
	
	if($b_suit[0]){
		if($bind_s == 0 || $bind_s == 1){
			$bind_s++;
		}
		$one_suit_flag++;
	}else{
		if($bind_s == 2){
			$miss_bind = 1;
		}else{
			$bind_s = 0;
		}
	}
	if($b_suit[1]){
		if($bind_h == 0 || $bind_h == 1){
			$bind_h++;
		}
		$one_suit_flag++;
	}else{
		if($bind_h == 2){
			$miss_bind = 1;
		}else{
			$bind_h = 0;
		}
	}
	if($b_suit[2]){
		if($bind_c == 0 || $bind_c == 1){
			$bind_c++;
		}
		$one_suit_flag++;
	}else{
		if($bind_c == 2){
			$miss_bind = 1;
		}else{
			$bind_c = 0;
		}
	}
	if($b_suit[3]){
		if($bind_d == 0 || $bind_d == 1){
			$bind_d++;
		}
		$one_suit_flag++;
	}else{
		if($bind_d == 2){
			$miss_bind = 1;
		}else{
			$bind_d = 0;
		}
	}
	
	for my $j (2..$#pair){
		if($pair[0]%13 + $j * ($pair[1]%13 - $pair[0]%13) != $pair[$j]%13){
			$step_flag = 0;
		}
	}
	
	if($miss_bind){
		return ('パス', 0, 0, @flags);
	}else{
		$flags[13] = $bind_s;
		$flags[14] = $bind_h;
		$flags[15] = $bind_c;
		$flags[16] = $bind_d;
	}
	
	if($flags[4]){
		$h_mes .= "七渡し ";
	}
	if($flags[5]){
		$h_mes .= "八切 ";
	}
	if($flags[7]){
		$h_mes .= "十\捨て ";
	}
	if($flags[8]){
		$h_mes .= "イレブンバック ";
	}

	if(@pair == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13]一枚";
		$h_state = 1;
	}elsif(@pair == 2 && $pair[0]%13 == $pair[1]%13){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13]ダブル";
		$h_state = 2;
	}elsif(@pair == 3 && $pair[0]%13 == $pair[1]%13 && $pair[0]%13 == $pair[2]%13){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13]トリプル";
		$h_state = 3;
	}elsif(@pair == 4 && $pair[0]%13 == $pair[1]%13 && $pair[0]%13 == $pair[2]%13 && $pair[0]%13 == $pair[3]%13){
		$h_mes .= "$num[$pair[0]%13] 革命";
		$h_state = 4;
	}elsif(@pair == 3 && $one_suit_flag == 1 && $step_flag == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13] 3枚階段";
		$h_state = 5;
	}elsif(@pair == 4 && $one_suit_flag == 1 && $step_flag == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13] $suit[$pair[3]/13] $num[$pair[3]%13] 4枚階段";
		$h_state = 6;
	}elsif(@pair == 5 && $one_suit_flag == 1 && $step_flag == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13] $suit[$pair[3]/13] $num[$pair[3]%13] $suit[$pair[4]/13] $num[$pair[4]%13] 5枚階段";
		$h_state = 7;
	}elsif(@pair == 6 && $one_suit_flag == 1 && $step_flag == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13] $suit[$pair[3]/13] $num[$pair[3]%13] $suit[$pair[4]/13] $num[$pair[4]%13] $suit[$pair[5]/13] $num[$pair[5]%13] 6枚階段";
		$h_state = 8;
	}elsif(@pair == 7 && $one_suit_flag == 1 && $step_flag == 1){
		$h_mes .= "$suit[$pair[0]/13] $num[$pair[0]%13] $suit[$pair[1]/13] $num[$pair[1]%13] $suit[$pair[2]/13] $num[$pair[2]%13] $suit[$pair[3]/13] $num[$pair[3]%13] $suit[$pair[4]/13] $num[$pair[4]%13] $suit[$pair[5]/13] $num[$pair[5]%13] $suit[$pair[6]/13] $num[$pair[6]%13] 7枚階段";
		$h_state = 9;
	}else{
		return ('パス', 0, 0, @flags);
	}


	if($c_player eq ''){
		if($h_state != 0){
			return ($h_mes, $pair[0]%13, $h_state, @flags);
		}else{
			return ('パス', 0, 0, @flags);
		}
	}elsif(($state_n < $pair[0]%13 && $revolution == $back) || ($state_n > $pair[0]%13 && $revolution != $back)){
		if($h_state == $state_c){
			return ($h_mes, $pair[0]%13, $h_state, @flags);
		}else{
			return ('パス', 0, 0, @flags);
		}
	}else {
		return ('パス', 0, 0, @flags);
	}
}

sub game_set{
	my @members = ();
	my %sames = ();
	my @ranks = ();
	my $r_mes = '';
	my $err_flag = 0;
	my $blank_player = '';
	my $eplayers = 0;

	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn > 2){
			$ranks[$mvalue-1] = $mname;
			$eplayers++;
		}elsif($mturn == 2){
			$blank_player = $mname;
			$eplayers++;
		}
	}
	close $fh;
	$r_mes .= "<br>結果：<br>";
	for my $i(0..$eplayers-1){
		if($ranks[$i] eq ''){
			$err_flag = 1;
		}
		my $ir = $i + 1;
		$r_mes .= "$ir位：$ranks[$i]<br>";
	}
	if($blank_player ne ''){
		&error_lose($blank_player);
		&game_set;
	}elsif($err_flag){
		&system_comment("順位異常");
		&all_reset;
	}else{
		&system_comment($r_mes);
		&get_coin;
		&all_reset($eplayers);
	}
}

sub all_reset{
	my $all_players = shift;
	my @members = ();
	my %sames = ();
	my @ranks = ();
	my $r_mes = '';
	my $err_flag = 0;

	if($m{c_turn} >= 2){
		$m{c_turn} = 1;
		if($all_players < 4){
			if($m{c_value} == $all_players){
				$m{c_value} = -2;
			}elsif($m{c_value} == 1){
				$m{c_value} = 2;
			}else{
				$m{c_value} = 0;
			}
		}else{
			if($m{c_value} == $all_players){
				$m{c_value} = -1;
			}elsif($m{c_value} == $all_players-1){
				$m{c_value} = -2;
			}elsif($m{c_value} != 1 && $m{c_value} != 2){
				$m{c_value} = 0;
			}
		}
	}else{
		$m{c_turn} = 0;
		$m{c_value} = 0;
	}
	&write_user;
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	push @members, "<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn >= 2){
			if($all_players < 4){
				if($mvalue == $all_players){
					$mvalue = -2;
				}elsif($mvalue == 1){
					$mvalue = 2;
				}else{
					$mvalue = 0;
				}
			}else{
				if($mvalue == $all_players){
					$mvalue = -1;
				}elsif($mvalue == $all_players-1){
					$mvalue = -2;
				}elsif($mvalue != 1 && $mvalue != 2){
					$mvalue = 0;
				}
			}
			push @members, "$mtime<>$mname<>$maddr<>1<>$mvalue<>\n";
			if($mname ne $m{name}){
				&regist_you_data($mname,'c_turn',1);
				&regist_you_data($mname,'c_value',$mvalue);
			}
		}else{
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
			if($mname ne $m{name}){
				&regist_you_data($mname,'c_turn',0);
				&regist_you_data($mname,'c_value',0);
			}
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub get_coin{
	my @members = ();
	my %sames = ();
	my @ranks = ();
	my $total_coin = 0;

	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn >= 2){
			$total_coin += $rate;
		}
		if($mturn > 2){
			$ranks[$mvalue-1] = $mname;
		}
	}
	close $fh;
	if($ranks[0] ne ''){
		my $temp = int($total_coin * 0.7);
		&coin_move($temp, $ranks[0]);
	}
	if($ranks[1] ne ''){
		$temp = int($total_coin * 0.3);
		&coin_move($temp, $ranks[1]);
	}
}

sub g_end_flag {
	my @members = ();
	my %sames = ();

	my $players = 0;
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if ($mturn == 2) {
			$players++;
		}
	}
	close $fh;

	if($players > 0){
		return 1;
	}else {
		return 0;
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

sub shuffled_deck{
	my @deck;
	for my $i (0..51){
		push @deck, $i;
	}
	for my $i (0..51){
		my $j = int(rand(@deck));
		my $temp = $deck[$i];
 		$deck[$i] = $deck[$j];
 		$deck[$j] = $temp;
	}
	return @deck;
}

sub print_checkbox{
    my @num = ('3','4','5','6','7','8','9','10','J','Q','K','A','2'); # 低い順
    my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	my @hand = &v_to_hj($m{c_value});
	for my $i(0..$#hand){
		my $si = $i+1;
		print qq|<input type="checkbox" name="play_$i" value="1">$si枚目($suit[$hand[$i] / 13] $num[$hand[$i] % 13])を出す|;
		if($hand[$i] % 13 == 4 || $hand[$i] % 13 == 7){
			print qq|<select name="sub_$i" class="menu1">|;
			for my $j(0..$#hand){
				next if($j == $i);
				print qq|<option value="$hand[$j]">$suit[$hand[$j] / 13] $num[$hand[$j] % 13]</option>|;
			}
			print qq|</select>|;
		}
		print qq|<br>|;
	}
}

sub give {
	my @g_cards = @_;
	my @members = ();
	my %sames = ();
	my $give_flag = 0;
	my $first_player;
	my $index = 0;
	my @g_hands = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn == 2){
			if(!defined($first_player)){
				$first_player = $index;
			}
			if($mname eq $m{name}){
				my @hand = &v_to_hj($m{c_value});
				my @my_hand = ();

				for my $i (@hand){
					my $gc_flag = 1;
					for my $j (@g_cards){
						if($i == $j){
							push @g_hands, $i;
							$gc_flag = 0;
							last;
						}
					}
					if($gc_flag){
						push @my_hand, $i;
					}
				}
				my $m_hands = @my_hand;
				if($m_hands == 0){
					$m{c_value} = &win_player;
					$m{c_turn} = 3;
					$c_player = '';
					$bind_s = 0;
					$bind_h = 0;
					$bind_c = 0;
					$bind_d = 0;
					&system_comment("七上がり");
				}else{
					$m{c_value} = &h_to_vj(@my_hand);
				}
				&write_user;
				push @members, "$mtime<>$mname<>$maddr<>$m{c_turn}<>$m{c_value}<>\n";
				$give_flag = 1;
			}elsif($give_flag){
				my @phand = &v_to_hj($mvalue);
				push @phand, @g_hands;
				@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
				my $d_hand = &h_to_vj(@phand);
				&regist_you_data($mname,'c_value',$d_hand);
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$d_hand<>\n";
				$give_flag = 0;
			}else {
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
			}
		}else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$index++;
	}
	if($give_flag){
		my $line = $members[$first_player];
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if($mname ne $m{name}){
			my @phand = &v_to_hj($mvalue);
			push @phand, @g_hands;
			@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
			my $d_hand = &h_to_vj(@phand);
			&regist_you_data($mname,'c_value',$d_hand);
			$members[$first_player] =  "$mtime<>$mname<>$maddr<>$mturn<>$d_hand<>\n";
		}
	}
	unshift @members, "$turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub release {
	my @g_cards = @_;
	my @members = ();
	my %sames = ();
	my @g_hands = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $state_c, $state_n, $c_player, $revolution, $back, $bind_s, $bind_h, $bind_c, $bind_d) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn == 2){
			if($mname eq $m{name}){
				my @hand = &v_to_hj($m{c_value});
				my @my_hand = ();

				for my $i (@hand){
					my $gc_flag = 1;
					for my $j (@g_cards){
						if($i == $j){
							push @g_hands, $i;
							$gc_flag = 0;
							last;
						}
					}
					if($gc_flag){
						push @my_hand, $i;
					}
				}
				my $m_hands = @my_hand;
				if($m_hands == 0){
					$m{c_value} = &win_player;
					$m{c_turn} = 3;
					$c_player = '';
					$bind_s = 0;
					$bind_h = 0;
					$bind_c = 0;
					$bind_d = 0;
					&system_comment("十\上がり");
				}else{
					$m{c_value} = &h_to_vj(@my_hand);
				}
				&write_user;
				push @members, "$mtime<>$mname<>$maddr<>$m{c_turn}<>$m{c_value}<>\n";
				$give_flag = 1;
			}else {
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
			}
		}else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
	}
	unshift @members, "$turn<>$rate<>$state_c<>$state_n<>$c_player<>$revolution<>$back<>$bind_s<>$bind_h<>$bind_c<>$bind_d<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub h_to_vj {
    my $i = 0;
    my $v = 0;
    my $k = 1;
    until ($_[$i] eq ''){
    	  $v += ($_[$i] + 1) * $k;
	  $k *= 53;
	  $i++;
    }
    return $v;
}

sub v_to_hj {
    my $v = $_[0];
    my $i = 0;
    my @h = ();
    until ($v <= 0){
    	  $h[$i] = ($v % 53) - 1;
	  $v -= $v % 53;
	  $v /= 53;
	  $i++;
    }
    return @h;
}

sub coin_move{
	my ($m_coin, $s_name) = @_;
	
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $e_player, $s_player, $w_player, $n_player, $trash_e, $trash_s, $trash_w, $trash_n, $hands_e, $hands_s, $hands_w, $hands_n, $bonus, $rest) = split /<>/, $head_line;
	close $fh;
	
	if($m_coin > 0){
		&system_comment("$s_name は $m_coin ｺｲﾝ得ました");
	}else{
		my $temp = -1 * $m_coin;
		&system_comment("$s_name は $temp ｺｲﾝ払いました");
	}
	if($s_name eq $m{name}){
		my $temp = $m{coin} + $m_coin;
		$temp = 0 if $temp < 0;
		$m{coin} = $temp;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($s_name);
		my $temp = $datas1{coin} + $m_coin;
		$temp = 0 if $temp < 0;
		&regist_you_data($s_name,'coin',$temp);
	}
}

1;#削除不可
