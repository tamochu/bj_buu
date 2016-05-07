#================================================
# テキサスホールデムポーカー
#================================================
require './lib/_casino_funcs.cgi';
my @rates = (100, 1000, 10000);

sub run {
	if ($in{mode} eq "bet") {
		$in{comment} = &bet;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "call") {
		$in{comment} = &call;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "max_bet") {
		$in{comment} = &max_bet;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "falled") {
		$in{comment} = &falled;
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
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member, $turn, $rate, $players, $pmember) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq '' || $m{c_turn} eq '4'){
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
		if($players == 0){
			print qq|レート<select name="rate" class="menu1">|;
			for my $i(0..$#rates){
				print qq|<option value="$i">$rates[$i]</option>|;
			}
		}
		print qq|<input type="submit" value="ｹﾞｰﾑに参加" class="button_s"></form><br>|;		
	}

	if($turn){
		if($m{name} eq $turn){
			&print_cards;
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="b_coin" value="$rate" class="text_box_b"><input type="hidden" name="mode" value="bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="ベット" class="button_s"></form>|;
			
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="call">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="コール" class="button_s"></form><br>|;	
					
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="倍プッシュ" class="button_s"></form><br>|;
			
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="falled">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="フォールド" class="button_s"></form><br>|;
		}else{
			&print_cards if $m{c_turn} == 2;
		}
	}elsif($m{c_turn} == 1) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="start">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<br><input type="submit" value="ｹﾞｰﾑを始める" class="button_s"></form><br>|;
	}
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		if($is_mobile){
			$bcomment =~ s|&#9824|S|g;
			$bcomment =~ s|&#9825|H|g;
			$bcomment =~ s|&#9827|C|g;
			$bcomment =~ s|&#9826|D|g;
		}
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $players = 0;
	my $active = 0;
	my $pmember = '';
	my $f_player = '';
	my $nt_flag = 0;
	my $this_set_flag = 0;
	my $turn_error = 1;
	my $allin_else = 0;
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	$pmember .= "コミュニティカード：";
	my @c_cards = split /,/, $comunity_card;
	for my $card (@c_cards){
		last if $card == -1;
		$pmember .= "$suit[$card/13] $num[$card%13]  ";
	}
	$pmember .= "<br>";
	
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn == 2){
				if($mname eq $m{name}){
					$m{c_turn} = 4;
					&write_user;
				}
				$mturn = 4;
				if($turn eq $mname){
					$nt_flag = 1;
				}
				&regist_you_data($mname,'c_turn',$mturn);
				&regist_you_data($mname,'c_value',$mvalue);
			}elsif($mturn <= 1) {
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
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
		if ($mturn == 2) {
			$pmember .= "$mname：$mstock ｺｲﾝ";
			if($turn eq $mname){
				$pmember .= "★";
				$turn_error = 0;
			}
			if($d_player eq $mname){
				$pmember .= "ディーラー";
			}
			$pmember .= "<br>";
			$players++;
			$active++;
			$allin_else++;
		}elsif($mturn >= 3){
			$pmember .= "$mname";
			if($mturn == 3){
				$pmember .= "：オールイン<br>";
				$active++;
			}else{
				$pmember .= "：フォールド<br>";
			}
			$players++;
		}elsif($mturn == 1){
			$pmember .= "$mname：待機中";
			$pmember .= "<br>";
			$players++;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
		$member .= "$m{name},";
	}
	if($nt_flag){
		$turn = $f_player;
		if($f_player eq ''){
			$this_set_flag = 1;
		}
	}
	unshift @members, "$turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;


	if($turn && $turn_error){
		&system_comment("ターン異常修正しました");
		my $next_flag = 1;
		my $next_turn = '';
		my @e_members = ();
		open my $efh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
		eval { flock $efh, 2; };
		my $head_line = <$efh>;
		my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
		while (my $line = <$efh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
			push @e_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
			if($mturn == 2 && $next_flag == 1){
				$next_turn = $mname;
				$next_flag = 0;
				$err_set_flag = 0;
			}
			if($d_player eq $mname){
				$next_flag = 1;
			}
		}
		unshift @e_members, "$next_turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
		seek  $efh, 0, 0;
		truncate $efh, 0;
		print $efh @e_members;
		close $efh;
		if($next_turn eq ''){
			&reset_game;
		}
	}

	if($turn && $active == 1){
		&all_falled;	
	}
	if($turn && $allin_else <= 1){
		&next_stage;
	}
	if($turn && $active == 0){
		&reset_game;
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $turn, $rate, $players, $pmember);
}

sub bet {
	my @members = ();
	my $max_bet = 0;
	my $min_bet = 999999999;
	
	return("参加してません") if $m{c_turn} <= 1;
	
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$ifh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($max_bet < $mstock && $mturn == 2){
			$max_bet = $mstock;
		}
		if($min_bet > $mstock && $mturn == 2 && $mname ne $m{name}){
			$min_bet = $mstock;
		}
	}
	close $ifh;
	return("あなたの順番ではありません") if $turn ne $m{name};
	
	if($in{b_coin} + $m{c_stock} > $max_bet * 2){
		$in{b_coin} = $max_bet * 2 - $m{c_stock};
	}
	if($in{b_coin} < 0){
		$in{b_coin} = 0;
	}
	if($m{coin} < $in{b_coin}){
		$in{b_coin} = $m{coin};
		$m{c_turn} = 3;
	}
	$m{coin} -= int($in{b_coin});
	$m{c_stock} += int($in{b_coin});
	&write_user;

	my $next_flag = 1;
	my $next_turn = '';
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mname eq $m{name}){
			$mturn = $m{c_turn};
			$mvalue = $m{c_value};
			$mstock = $m{c_stock};
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		if($mturn == 2 && $next_flag == 1){
			$next_turn = $mname;
			$next_flag = 0;
		}
		if($turn eq $mname){
			$next_flag = 1;
		}
	}

	if($max_bet > $m{c_stock}){
		$next_turn = $m{name};
	}
	if($l_player eq $m{name}){
		$l_player = '';
	}
	unshift @members, "$next_turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	&system_comment("$m{name} は $in{b_coin} ｺｲﾝベットしました");
	
	if($max_bet == $m{c_stock} && $max_bet == $min_bet && $l_player eq ''){
		&next_stage;
	}
	
	return;
}

sub call {
	my @members = ();
	my $max_bet = 0;
	my $min_bet = 999999999;
	
	return("参加してません") if $m{c_turn} <= 1;
	
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$ifh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($max_bet < $mstock && $mturn == 2){
			$max_bet = $mstock;
		}
		if($min_bet > $mstock && $mturn == 2 && $mname ne $m{name}){
			$min_bet = $mstock;
		}
	}
	close $ifh;
	return("あなたの順番ではありません") if $turn ne $m{name};
	
	$in{b_coin} = $max_bet - $m{c_stock};
	if($m{coin} < $in{b_coin}){
		$in{b_coin} = $m{coin};
		$m{c_turn} = 3;
	}
	$m{coin} -= int($in{b_coin});
	$m{c_stock} += int($in{b_coin});
	&write_user;

	my $next_flag = 1;
	my $next_turn = '';
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mname eq $m{name}){
			$mturn = $m{c_turn};
			$mvalue = $m{c_value};
			$mstock = $m{c_stock};
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		if($mturn == 2 && $next_flag == 1){
			$next_turn = $mname;
			$next_flag = 0;
		}
		if($turn eq $mname){
			$next_flag = 1;
		}
	}

	if($max_bet > $m{c_stock}){
		$next_turn = $m{name};
	}
	if($l_player eq $m{name}){
		$l_player = '';
	}
	unshift @members, "$next_turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	&system_comment("$m{name} は $in{b_coin} ｺｲﾝベットしました");
	
	if($l_player eq '' && (($max_bet == $m{c_stock} && $max_bet == $min_bet) || $min_bet == 999999999)){
		&next_stage;
	}
	
	return;
}

sub max_bet {
	my @members = ();
	my $max_bet = 0;
	my $min_bet = 999999999;
	
	return("参加してません") if $m{c_turn} <= 1;
	
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$ifh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($max_bet < $mstock && $mturn == 2){
			$max_bet = $mstock;
		}
		if($min_bet > $mstock && $mturn == 2 && $mname ne $m{name}){
			$min_bet = $mstock;
		}
	}
	close $ifh;
	return("あなたの順番ではありません") if $turn ne $m{name};
	
	$in{b_coin} = $max_bet * 2 - $m{c_stock};
	if($m{coin} < $in{b_coin}){
		$in{b_coin} = $m{coin};
		$m{c_turn} = 3;
	}
	$m{coin} -= int($in{b_coin});
	$m{c_stock} += int($in{b_coin});
	&write_user;

	my $next_flag = 1;
	my $next_turn = '';
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mname eq $m{name}){
			$mturn = $m{c_turn};
			$mvalue = $m{c_value};
			$mstock = $m{c_stock};
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		if($mturn == 2 && $next_flag == 1){
			$next_turn = $mname;
			$next_flag = 0;
		}
		if($turn eq $mname){
			$next_flag = 1;
		}
	}

	if($max_bet > $m{c_stock}){
		$next_turn = $m{name};
	}
	if($l_player eq $m{name}){
		$l_player = '';
	}
	unshift @members, "$next_turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	&system_comment("$m{name} は $in{b_coin} ｺｲﾝベットしました");
	
	return;
}

sub falled {
	my @members = ();
	my $max_bet = 0;
	my $min_bet = 999999999;
	my $active = 0;
	
	return("参加してません") if $m{c_turn} <= 1;
	
	open my $ifh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$ifh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$ifh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		$active++ if ($mturn == 2 || $mturn == 3);
		if($max_bet < $mstock){
			$max_bet = $mstock;
		}
		if($min_bet > $mstock && $mturn == 2 && $mname ne $m{name}){
			$min_bet = $mstock;
		}
	}
	close $ifh;
	return("あなたの順番ではありません") if $turn ne $m{name};
	
	$m{c_turn} = 4;
	&write_user;

	my $next_flag = 1;
	my $next_turn = '';
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mname eq $m{name}){
			$mturn = $m{c_turn};
			$mvalue = $m{c_value};
			$mstock = $m{c_stock};
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		if($mturn == 2 && $next_flag == 1){
			$next_turn = $mname;
			$next_flag = 0;
		}
		if($turn eq $mname){
			$next_flag = 1;
		}
	}
	if($l_player eq $m{name}){
		$l_player = '';
	}
	unshift @members, "$next_turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	
	&system_comment("$m{name} は 降りました");
	if($active <= 1){
		&all_falled;
	}
	
	if($max_bet == $min_bet && $l_player eq ''){
		&next_stage;
	}
	
	return;
}

sub next_stage{
	&system_comment("ベットラウンドが終了しました");
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	my @c_cards = split /,/, $comunity_card;
	my $n_c_card = '';
	my $m_one_p = 0;
	my $f_name = '';
	my $l_name = '';
	my $d_find = 0;
	my $next_turn = '';
	my $last_turn = '';
	for my $card (@c_cards){
		last if $card == -1;
		$m_one_p++;
	}
	if($m_one_p == 0){
		$n_c_card = "$c_cards[1],$c_cards[2],$c_cards[3],-1,$c_cards[4],$c_cards[5]";
	}elsif($m_one_p == 3){
		$n_c_card = "$c_cards[0],$c_cards[1],$c_cards[2],$c_cards[4],-1,$c_cards[5]";
	}elsif($m_one_p == 4){
		$n_c_card = "$c_cards[0],$c_cards[1],$c_cards[2],$c_cards[3],$c_cards[5],-1";
	}else{
		$n_c_card = $comunity_card;
	}
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		if($mturn == 2 && $f_name eq ''){
			$f_name = $mname;
		}
		if($mturn == 2){
			$l_name = $mname;
			if($d_find){
				if($next_turn eq ''){
					$next_turn = $mname;
				}
			}else{
				$last_turn = $mname;
			}
		}
		if($mname eq $d_player){
			$d_find = 1;
		}
	}
	if($next_turn eq ''){
		$next_turn = $f_name;
	}
	if($last_turn eq ''){
		$last_turn = $l_name;
	}
	unshift @members, "$next_turn<>$rate<>$n_c_card<>$d_player<>$last_turn<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	if($m_one_p == 5){
		&show_down;
	}
}

sub show_down{
	my $win_name = '';
	my $sum_pot = 0;
	my $best_hand= 0;
	my $sys_mes = 'ショーダウン<br>';
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mturn == 2 || $mturn == 3){
			my @mhand = &v_to_hj($mvalue);
			$sys_mes .= "$mname : $suit[$mhand[0] / 13] $num[$mhand[0] % 13]  $suit[$mhand[1] / 13] $num[$mhand[1] % 13] ";
			if(&check_hands($comunity_card, $best_hand, $mvalue)){
				$win_name = $mname;
				$best_hand = $mvalue;
			}
			$sys_mes .= "<br>";
		}
		if($mturn >= 2){
			$sum_pot += $mstock;
		}
	}

	close $fh;
	&system_comment($sys_mes);
	&coin_move($sum_pot, $win_name);
	&game_set;
}

sub check_hands{
	my ($comunity_card, $best_hand, $check_hand) = @_;
	return 1 if($best_hand == 0);
	my $ret_flag = 0;
	my $max_hand = 0;
	my $high_card = 0;
	my $max_hand_c = 0;
	my $high_card_c = 0;
	my $hand_v;
	my $hand_h;
	my $ret = 0;
	
	my @b_hand = &v_to_hj($best_hand);
	my @c_hand = &v_to_hj($check_hand);
	
	my @c_cards = split /,/, $comunity_card;
#	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	($hand_v, $hand_h) = &check_hand_sub($b_hand[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $b_hand[0], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $b_hand[0], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $b_hand[0], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_cards[3], $b_hand[0]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($b_hand[1], $c_cards[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $b_hand[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $b_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $b_hand[1], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_cards[3], $b_hand[1]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($b_hand[0], $b_hand[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($b_hand[0], $c_cards[1], $b_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($b_hand[0], $c_cards[1], $c_cards[2], $b_hand[1], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($b_hand[0], $c_cards[1], $c_cards[2], $c_cards[3], $b_hand[1]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $b_hand[0], $b_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $b_hand[0], $c_cards[2], $b_hand[1], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $b_hand[0], $c_cards[2], $c_cards[3], $b_hand[1]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $b_hand[0], $b_hand[1], $c_cards[4]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $b_hand[0], $c_cards[3], $b_hand[1]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $b_hand[0], $b_hand[1]);
	if($max_hand < $hand_v || ($max_hand == $hand_v && $high_card < $hand_h)){
		$max_hand = $hand_v;
		$high_card = $hand_h;
	}
	
	
	
	($hand_v, $hand_h) = &check_hand_sub($c_hand[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_hand[0], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_hand[0], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_hand[0], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_hand[0]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_hand[1], $c_cards[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_hand[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_hand[1], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_hand[1]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_hand[0], $c_hand[1], $c_cards[2], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_hand[0], $c_cards[1], $c_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_hand[0], $c_cards[1], $c_cards[2], $c_hand[1], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_hand[0], $c_cards[1], $c_cards[2], $c_cards[3], $c_hand[1]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_hand[0], $c_hand[1], $c_cards[3], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_hand[0], $c_cards[2], $c_hand[1], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_hand[0], $c_cards[2], $c_cards[3], $c_hand[1]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_hand[0], $c_hand[1], $c_cards[4]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_hand[0], $c_cards[3], $c_hand[1]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	($hand_v, $hand_h) = &check_hand_sub($c_cards[0], $c_cards[1], $c_cards[2], $c_hand[0], $c_hand[1]);
	if($max_hand_c < $hand_v || ($max_hand_c == $hand_v && $high_card_c < $hand_h)){
		$max_hand_c = $hand_v;
		$high_card_c = $hand_h;
	}
	if($max_hand_c == 10){
		print "ロイヤルストレートフラッシュ";
	}elsif($max_hand_c == 9){
		print "ストレートフラッシュ";
	}elsif($max_hand_c == 8){
		print "フォーカード";
	}elsif($max_hand_c == 7){
		print "フルハウス";
	}elsif($max_hand_c == 6){
		print "フラッシュ";
	}elsif($max_hand_c == 5){
		print "ストレート";
	}elsif($max_hand_c == 4){
		print "スリーカード";
	}elsif($max_hand_c == 3){
		print "ツーペアー";
	}elsif($max_hand_c == 2){
		print "ワンペア";
	}elsif($max_hand_c == 1){
		print "ブタ";
	}
	if($max_hand < $max_hand_c || ($max_hand == $max_hand_c && $high_card < $high_card_c)){
		$ret = 1;
	}
	return $ret;
}

sub check_hand_sub{
	my @h = @_;
	@h = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @h;
	my $hand_value = 0;
	my $high_card = 0;
	
	my $is_straight = 0;
	my $is_royal = 0;
	my $is_flash = 0;
	my $is_four = 0;
	my $is_three = 0;
	my $pair_num = 0;
	my $pair_high = 0;
	my $pair_low = 0;
	my @subh = ();
	my @suith = ();
	my $i;

	for $i (0..4){
		$subh[$i] = $h[$i] % 13;
		$suith[$i] = ($h[$i] - $subh[$i]) / 13;
	}
	$i = 1;
	while(1){
		last if $subh[$i] eq '';
		if($subh[$i-1] > $subh[$i]){
			my $tem = $subh[$i-1];
			$subh[$i-1] = $subh[$i];
			$subh[$i] = $tem;
			$i = 1;
			next;
		}
		$i++;
	}
	if($subh[0]+1 == $subh[1]&& $subh[0]+2 == $subh[2] && $subh[0]+3 == $subh[3] && $subh[0]+4 == $subh[4]){
		$is_straight = 1;
		$high_card = $h[4];
	}
	if($subh[0] == 0 && $subh[1] == 9 && $subh[2] == 10 && $subh[3] == 11 && $subh[4] == 12){
		$is_royal = 1;
		$is_straight = 1;
		$high_card = $h[0];
	}
	if($suith[0] == $suith[1] && $suith[0] == $suith[2] && $suith[0] == $suith[3] && $suith[0] == $suith[4]){
		$is_flash = 1;
		$high_card = $h[0] % 13 == 0 ? $h[0]:$h[5];
	}
	for $i (0..12){
		my $card = 0;
		for my $j (0..4){
			$card++ if $subh[$j] == $i;
		}
		if($card == 4){
			$is_four = $i+1;
			for my $j (0..4){
				if($h[$j] % 13 != $i && $high_card %13 != 0){
					$high_card = $h[$j];
				}
			}
		}elsif($card == 3){
			$is_three = $i+1;
			if($h[$j] % 13 != $i && $high_card %13 != 0){
				$high_card = $h[$j];
			}
		}elsif($card == 2){
			$pair_num++;
			if($pair_high){
				$pair_low = $pair_high;
			}
			$pair_high = $i+1;
			if($h[$j] % 13 != $i && $high_card %13 != 0){
				$high_card = $h[$j];
			}
			if($pair_low){
				if($h[$j] % 13 != $pair_low - 1 && $h[$j] % 13 != $pair_high - 1){
					$high_card = $h[$j];
				}
			}
		}
	}

	my $htemp;
	if($is_royal && $is_straight && $is_flash){
		$hand_value = 10;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
	}elsif($is_straight && $is_flash){
		$hand_value = 9;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
	}elsif($is_four){
		$hand_value = 8;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
		$htemp += $is_four == 1 ? 52 * 14:52 * $is_four;
	}elsif($is_three && $pair_num == 1){
		$hand_value = 7;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
		$htemp += $is_three == 1 ? 52 * 14:52 * $is_three;
	}elsif($is_flash){
		$hand_value = 6;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
	}elsif($is_straight){
		$hand_value = 5;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
	}elsif($is_three){
		$hand_value = 4;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
		$htemp += $is_three == 1 ? 52 * 14:52 * $is_three;
	}elsif($pair_num == 2){
		$hand_value = 3;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
		$htemp += $pair_low == 1 ? 52 * 14:52 * $pair_low;
		$htemp += $pair_high == 1 ? 2704 * 14:2704 * $pair_high;
	}elsif($pair_num == 1){
		$hand_value = 2;
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
		$htemp += $pair_high == 1 ? 52 * 14:52 * $pair_high;
	}else{
		$hand_value = 1;
		if($h[$j] % 13 != $i){
			$high_card = $h[$j];
		}
		$htemp = (($high_card + 12) % 13) * 4 + ($high_card / 13);
	}
	$high_card = $htemp;
	
	return ($hand_value, $high_card);
}

sub all_falled{
	my $win_name = '';
	my $sum_pot = 0;
	
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mturn == 2 || $mturn == 3){
			$win_name = $mname;
		}
		if($mturn >= 2){
			$sum_pot += $mstock;
		}
	}
	close $fh;
	&coin_move($sum_pot, $win_name);
	&game_set;
}

sub deal_card {
	my $a_players;
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mturn == 1) {
			$a_players++;
		}
	}
	close $fh;

	my @members = ();
	my %sames = ();
	my @g_deck = &shuffled_deck;
	my @player_name = ();
	my $card_no = 0;
	my $plcards = 2;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	if($turn eq ''){
		$turn = $m{name};
		$comunity_card = '-1';
		$m{c_turn} = 2;
		my @phand = ();
		for my $i ($card_no..$card_no+$plcards-1){
			push @phand, $g_deck[$i];
		}
		
		@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
		$card_no += $plcards;
		$m{c_value} = &h_to_vj(@phand);
		&write_user;
	}
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		if($mturn == 1){
			if($mname eq $m{name}){
				push @members, "$mtime<>$mname<>$maddr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			}else{
				my @phand = ();
				for my $i ($card_no..$card_no+$plcards-1){
					push @phand, $g_deck[$i];
				}
				@phand = sort { $a%13 <=> $b%13 || $a/13 <=> $b/13 } @phand;
				$card_no += $plcards;
				my $d_hand = &h_to_vj(@phand);
				&regist_you_data($mname,'c_turn',2);
				&regist_you_data($mname,'c_value',$d_hand);
				push @members, "$mtime<>$mname<>$maddr<>2<>$d_hand<>$mstock<>\n";
			}
			push @player_name, $mname;
		}else {
			&regist_you_data($mname,'c_turn',0);
			&regist_you_data($mname,'c_value',0);
			&regist_you_data($mname,'c_stock',0);
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
		}
	}
	for my $i ($card_no..$card_no+4){
		$comunity_card .= ",$g_deck[$i]";
	}
	my $d_num = int(rand(@player_name));
	$d_player = $player_name[$d_num];
	
	my $b_num = $d_num + 1;
	$b_num = 0 if $b_num == @player_name;
	if($player_name[$b_num] eq $m{name}){
		$m{coin} -= $rate;
		$m{c_stock} = $rate;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($player_name[$b_num]);
		my $temp = $datas1{coin} - $rate;
		$temp = 0 if $temp < 0;
		&regist_you_data($player_name[$b_num],'coin',$temp);
		&regist_you_data($player_name[$b_num],'c_stock',$rate);
	}
	$turn = $player_name[$b_num];
	
	my $s_num = $b_num + 1;
	$s_num = 0 if $s_num == @player_name;
	if($player_name[$s_num] eq $m{name}){
		$m{coin} -= int($rate / 2);
		$m{c_stock} = int($rate / 2);
		&write_user;
	}else{
		my %datas2 = &get_you_datas($player_name[$s_num]);
		my $temp2 = $datas2{coin} - int($rate / 2);
		$temp2 = 0 if $temp2 < 0;
		&regist_you_data($player_name[$s_num],'coin',$temp2);
		$temp2 = int($rate / 2);
		&regist_you_data($player_name[$s_num],'c_stock',$temp2);
	}
	$l_player = '';
	unshift @members, "$turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return ("ｹﾞｰﾑを始めます$turnの番です");
}

sub game_set {
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mturn){
			if($mname eq $m{name}){
				$m{c_turn} = 1;
				$m{c_value} = 0;
				$m{c_stock} = 0;
				&write_user;
				push @members, "$mtime<>$mname<>$maddr<>1<>0<>0<>\n";
			}else{
				&regist_you_data($mname,'c_turn',1);
				&regist_you_data($mname,'c_value',0);
				&regist_you_data($mname,'c_stock',0);
				push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
			}
		}else {
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
		}
	}
	unshift @members, "<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub reset_game {
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if($mturn){
			if($mname eq $m{name}){
				$m{c_turn} = 0;
				$m{c_value} = 0;
				$m{c_stock} = 0;
				&write_user;
				push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
			}else{
				&regist_you_data($mname,'c_turn',0);
				&regist_you_data($mname,'c_value',0);
				&regist_you_data($mname,'c_stock',0);
				push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
			}
		}else {
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>0<>\n";
		}
	}
	unshift @members, "<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
}

sub participate{
	return("ｺｲﾝがありません") if $m{coin} <= 0;
	my $rate_set = 1;
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $comunity_card, $d_player, $l_player) = split /<>/, $head_line;	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
		if ($mturn >= 1) {
			$rate_set = 0;
		}
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
		$member .= "$m{name},";
	}
	if($rate_set){
		$rate = $rates[$in{rate}];
	}
	unshift @members, "$turn<>$rate<>$comunity_card<>$d_player<>$l_player<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	$m{c_turn} = 1;
	$m{c_value} = 0;
	&write_user;
	return("$m{name} が参加します");
}

sub exit_game{
	if ($m{c_turn} == 1 || $m{c_stock} == 0){
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
	}else {
		return("ｹﾞｰﾑが始まっています");
	}
	&write_user;
	return("$m{name} は やめました");
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

sub print_cards{
	my @num = ('A','2','3','4','5','6','7','8','9','10','J','Q','K'); # 低い順
	my @suit = $is_mobile ? ('S','H','C','D'):('&#9824','&#9825','&#9827','&#9826');
	my @hand = &v_to_hj($m{c_value});
	for my $i(0..$#hand){
		print qq|$suit[$hand[$i] / 13] $num[$hand[$i] % 13]  |;
	}
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


1;#削除不可
