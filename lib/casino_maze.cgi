#================================================
# 迷路
#================================================
require './lib/_casino_funcs.cgi';

my $maze_file = "$logdir/maze.cgi";

$leverage = 3;
$boss_str = 3;

$wall = 1;
$road = 0;
$pre_wall = 2;
$treasure = 3;
$unknown = -1;

$max_size = 30;
$mutate = 50;

sub run {
	if ($in{mode} eq "move") {
	    $in{comment} = &move($in{direction}, $in{leader});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "leader") {
	    $in{comment} = &make_leader;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "make_maze") {
	    $in{comment} = &make_maze($in{size_x}, $in{size_y});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "treasure") {
	    $in{comment} = &set_treasure($in{x}, $in{y});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "entry") {
	    $in{comment} = &entry;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "reset" && $in{switch}) {
	    $in{comment} = &reset_maze;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $maze_bet, $state) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	if($leader){
		($position_x, $position_y, $flag, $maze, $map) = &get_position;
		if($m{name} eq $leader) {
			if($state eq 'ready'){
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="make_maze">|;
				print qq|<select name="size_x">|;
				for my $i (5..$max_size){
					print qq|<option value="$i">$i</option>|;
				}
				print qq|</select>|;
				print qq|×|;
				print qq|<select name="size_y">|;
				for my $i (5..$max_size){
					print qq|<option value="$i">$i</option>|;
				}
				print qq|</select>|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="迷宮作成" class="button_s"></form><br>|;
			}elsif($state eq 'ready2'){
				&print_linked_map($maze);
			}else{
				my $count = &get_count;
				print qq|$count人が挑戦中です|;
				if($position_x == -1 || $position_y == -1){
					&set_position(2, 1, 0);
				}
				&print_map($maze, $position_x, $position_y);
				&print_arrow(1);
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="reset">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<select name="switch">|;
				print qq|<option value="0" selected>----</option>|;
				print qq|<option value="1">リセット</option>|;
				print qq|</select>|;
				print qq|<input type="submit" value="リセット" class="button_s"></form><br>|;
			}
		}else{
			my $count = &get_count;
			print qq|$count人が挑戦中です|;
			if($position_x > 0 && $position_y > 0){
				if($flag){
					print qq|<font size="+2" color="#ffff00">財宝獲得</font><br>|;
				}
				&print_map($map, $position_x, $position_y);
				&print_arrow(0);
			}elsif($state eq 'go'){
				my ($size_x, $size_y) = &get_size($maze);
				print qq|迷宮サイズ:$size_x×$size_y<br>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="entry">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="迷宮に入る" class="button_s"></form><br>|;
			}else{
				print qq|迷宮作成中<br>|;
			}
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="text"  name="comment" class="text_box_b" value="10"> ｺｲﾝ |;
		print qq|<input type="submit" value="親になる" class="button_s"></form><br>|;
	}
	
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
	print $leader eq '' ? qq|ミノタウロス:募集中<br>|:qq|ミノタウロス:$leader 死亡ペナルティ:$maze_bet<br>|;
	
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
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $leader_find = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $leader) {
			$leader_find = 1;
		}
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	unless ($leader_find){
		if($state ne 'go'){
			$state = '';
			$leader = '';
		}
	}
	unshift @members, "$leader<>$maze_bet<>$state<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members - 1;

	return ($member_c, $member, $leader, $maze_bet, $state);
}

sub get_count{
	my $count = -2;
	open my $fhc, "< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	while(my $line = <$fhc>){
		$count++;
	}
	close $fhc;
	
	return $count;
}

sub make_leader {
#	return("ｺｲﾝがありません") if $m{coin} < 0;
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$v = $in{comment};
			$v = $m{coin} if $v > $m{coin};
			$maze_bet = $v;
		}else{
			$maze_bet = 100;
		}
		$state = 'ready';
	}else{
		return "他のプレイヤーが迷宮を作成中です";
	}
	push @members, "$leader<>$maze_bet<>$state<>\n";
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

	return "$leader が親です 賭け上限:$maze_bet";
}

sub get_position{
	open my $fh, "< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	my $maze = <$fh>;
	chomp $maze;
	my $posx = -1;
	my $posy = -1;
	my $flag = 0;
	my $map;
	while (my $line = <$fh>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		
		if($mname eq $m{name}){
			$posx = $mposx;
			$posy = $mposy;
			$flag = $mflag;
			$map = $mmap;
		}
	}
	close $fh;
	return ($posx, $posy, $flag, $maze, $map);
}

sub set_position{
	my ($x, $y, $flag) = @_;
	my @lines = ();
	my %sames = ();
	open my $fh, "+< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $maze = <$fh>;
	chomp $maze;
	push @lines, "$maze\n";
	while (my $line = <$fh>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		
		if($mname eq $m{name}){
			$mposx = $x;
			$mposy = $y;
			$mflag = $flag;
		}
		push @lines, "$mname<>$mposx<>$mposy<>$mflag<>$mmap<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return;
}

sub encount{
	my($position_x, $position_y, $flag, $maze, $map) = &get_position;
	
	open my $fh, "< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	my $maze = <$fh>;
	chomp $maze;
	while (my $line = <$fh>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		
		if($mname ne $m{name}){
			if($mposx == $position_x && $mposy == $position_y){
				&maze_battle($m{name}, $mname);
			}
		}
	}
	close $fh;
}

sub maze_battle{
	my ($name1, $name2) = @_;
	
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	close $fh;
	
	if($name1 eq $leader){
		if(rand($boss_str) < 1){
			&battle_result($name2, $name1);
		}else{
			&battle_result($name1, $name2);
		}
	}elsif($name2 eq $leader){
		if(rand($boss_str) < 1){
			&battle_result($name1, $name2);
		}else{
			&battle_result($name2, $name1);
		}
	}else{
		if(rand(2) < 1){
			&battle_result($name1, $name2);
		}else{
			&battle_result($name2, $name1);
		}
	}
}

sub battle_result{
	my ($winner, $loser) = @_;
	
	my @lines = ();
	my %sames = ();
	open my $fhm, "+< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	eval { flock $fhm, 2; };
	my $maze = <$fhm>;
	chomp $maze;
	push @lines, "$maze\n";
	my ($rand_x, $rand_y) = &maze_warp($maze);
	while (my $line = <$fhm>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		
		if($mname eq $loser){
			$mposx = $rand_x;
			$mposy = $rand_y;
			$mflag = 0;
		}
		push @lines, "$mname<>$mposx<>$mposy<>$mflag<>$mmap<>\n";
	}
	seek  $fhm, 0, 0;
	truncate $fhm, 0;
	print $fhm @lines;
	close $fhm;
	
	open my $fh, "< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	close $fh;
	&coin_move_atob($loser, $leader, $maze_bet, 0);
	&system_comment("$winnerと$loserが迷宮内で遭遇し$winnerが$loserを打ち破りました");
}

sub maze_warp{
	my ($maze) = @_;
	my $x;
	my $y;

	my @mlines = split '/', $maze;
	my @line = split /,/, $mlines[0];
	my $size_y = @mlines;
	my $size_x = @line;
	$size_x = int($size_x / 2) - 1;
	$size_y = int($size_y / 2) - 1;
	
	while(1){
		$x = int(rand($size_x)) * 2 + 2;
		$y = int(rand($size_y)) * 2 + 2;
		my $type = &get_point($maze, $x, $y);
		if($type == $road){
			last;
		}
	}
	return ($x, $y);
}

sub make_maze{
	my ($size_x, $size_y) = @_;
	my $mret = '';
	my $m_size_x = $size_x*2+3;
	my $m_size_y = $size_y*2+3;
	my $maze = &maze_init($m_size_x, $m_size_y);
	while(1){
		$is_finish = &maze_finish_check($maze);
		if($is_finish){
			last;
		}
		my ($x, $y) = &maze_warp($maze);
		$maze = &maze_sub($maze, $x, $y);
	}
	for my $x (2..$m_size_x-3){
		for my $y (2..$m_size_y-3){
			my $type = &get_point($maze, $x, $y);
			if($type == $wall){
				my $utype = &get_point($maze, $x, $y-1);
				my $ltype = &get_point($maze, $x-1, $y);
				my $rtype = &get_point($maze, $x+1, $y);
				my $dtype = &get_point($maze, $x, $y+1);
				my $roads = 0;
				if($utype == $road){
					$roads++;
				}
				if($ltype == $road){
					$roads++;
				}
				if($rtype == $road){
					$roads++;
				}
				if($dtype == $road){
					$roads++;
				}
				if($roads == 2 && rand($mutate) < 1){
					$maze = &set_point($maze, $x, $y, $road);
				}
			}
		}
	}
	open my $fhm, "> $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	print $fhm "$maze\n";
	close $fhm;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	$state = 'ready2';
	push @members, "$leader<>$maze_bet<>$state<>\n";
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
	
	return "迷宮を作成しました";
}

sub move{
	my ($direction, $leader) = @_;
	my $px = 0;
	my $py = 0;
	my $ret = '';
	if($direction == 0){
		$px = 0;
		$py = -1;
	}elsif($direction == 1){
		$px = 1;
		$py = 0;
	}elsif($direction == 2){
		$px = 0;
		$py = 1;
	}elsif($direction == 3){
		$px = -1;
		$py = 0;
	}
	my($position_x, $position_y, $flag, $maze, $map) = &get_position;
	my $type = &get_point($maze, $position_x+$px, $position_y+$py);
	if($position_x == 2 && $position_y == 1 && $direction == 0){
		if($flag){
			&clear;
		}else{
			$ret = "宝を見つけるまで出られません";
		}
	}else{
		if($type == $road){
			&set_position($position_x+$px, $position_y+$py, $flag);
		}elsif($type == $treasure && $leader != 1){
			&set_position($position_x+$px, $position_y+$py, 1);
		}else{
			$ret = "通路以外へは移動できません";
		}
		&map_reflesh;
	}
	&encount;
	return $ret;
}

sub maze_init{
	my ($m_size_x, $m_size_y) = @_;
	my $maze;
	my @mlines;
	for my $y (0..$m_size_y-1){
		my @line;
		my $mline;
		for my $x (0..$m_size_x-1){
			push @line, $wall;
		}
		$mline = join ',', @line;
		push @mlines, $mline;
	}
	$maze = join '/', @mlines;
	for my $y (0..$m_size_y-1){
		$maze = &set_point($maze, 0, $y, $road);
		$maze = &set_point($maze, $m_size_x-1, $y, $road);
	}
	for my $x (0..$m_size_x-1){
		$maze = &set_point($maze, $x, 0, $road);
		$maze = &set_point($maze, $x, $m_size_y-1, $road);
	}
	$maze = &set_point($maze, 2, 2, $road);
	return $maze;
}

sub maze_sub{
	my($maze, $x, $y) = @_;
	my $rest_length = 5;
	my $type = &get_point($maze, $x, $y);
	if($type == $road){
		my $x1 = $x;
		my $y1 = $y;
		my $end_flag = 0;
		while(1){
			my $direction = int(rand(4));
			my $first_dir = $direction;
			while(1){
				my $px;
				my $py;
				if($direction == 0){
					$px = 0;
					$py = -1;
				}elsif($direction == 1){
					$px = 1;
					$py = 0;
				}elsif($direction == 2){
					$px = 0;
					$py = 1;
				}else{
					$px = -1;
					$py = 0;
				}
				$direction++;
				$direction %= 4;
				my $ntype = &get_point($maze, $x1+$px*2, $y1+$py*2);
				if($ntype == $wall){
					$maze = &set_point($maze, $x1+$px, $y1+$py, $road);
					$maze = &set_point($maze, $x1+$px*2, $y1+$py*2, $road);
					$x1 = $x1+$px*2;
					$y1 = $y1+$py*2;
					$rest_length--;
					last;
				}else{
					if($direction == $first_dir){
						$end_flag = 1;
						last;
					}
				}
			}
			if($end_flag || $rest_length <= 0){
				last;
			}
		}
	}
	return $maze;
}

sub set_treasure{
	my ($x, $y) = @_;
	return if ($x == 2 && $y == 1);
	open my $fhz, "< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	my $maze = <$fhz>;
	chomp $maze;
	close $fhz;
	my $type = &get_point($maze, $x, $y);
	if($type == $road){
		$maze = &set_point($maze, $x, $y, $treasure);
		
		open my $fhm, "> $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
		print $fhm "$maze\n";
		print $fhm "$m{name}<>$x<>$y<>0<>$maze<>\n";
		close $fhm;
		
		if(&treasure_setted($maze)){
			open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
			eval { flock $fh, 2; };
			my $head_line = <$fh>;
			my($leader, $maze_bet, $state) = split /<>/, $head_line;
			$state = 'go';
			push @members, "$leader<>$maze_bet<>$state<>\n";
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
			return "財宝をセットしました";
		}
	}
	return "財宝は通路上においてください";
}

sub entry{
	my $is_find = 0;
	my @lines = ();
	my %sames = ();
	open my $fhm, "+< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	eval { flock $fhm, 2; };
	my $maze = <$fhm>;
	chomp $maze;
	push @lines, "$maze\n";
	while (my $line = <$fhm>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if($mname eq $m{name}){
			$is_find = 1;
			unless($mposx > 0 && $mposy > 0){
				$mposx = 2;
				$mposy = 1;
			}
		}
		push @lines, "$mname<>$mposx<>$mposy<>$mflag<>$mmap<>\n";
	}
	unless($is_find){
		my $umap = $maze;
		$umap =~ s/$wall|$road|$treasure/$unknown/g;
		push @lines, "$m{name}<>2<>1<>0<>$umap<>\n";
	}
	seek  $fhm, 0, 0;
	truncate $fhm, 0;
	print $fhm @lines;
	close $fhm;
	
	&map_reflesh;
	
	return "迷宮に突入しました";
}

sub clear{
	my $count = &get_count;
	close $fhc;
	open my $fhm, "> $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	print $fhm "";
	close $fhm;
	my $lname;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	$lname = $leader;
	$leader = '';
	$state = '';
	push @members, "$leader<>$maze_bet<>$state<>\n";
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

	my $prize = int($maze_bet*$leverage*$count*$count);
	&coin_move_atob($lname, $m{name}, $prize, 1);
	&system_comment("$m{name}が迷宮を攻略しました");
}

sub reset_maze{
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $maze_bet, $state) = split /<>/, $head_line;
	my $lname = $leader;
	$leader = '';
	$state = '';
	push @members, "$leader<>$maze_bet<>$state<>\n";
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
	
	my $count = 0;
	open my $fhc, "< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	my $headline = <$fhc>;
	while (my $line = <$fhc>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		push @players, $mname if ($mname ne $lname);
		$count++;
	}
	close $fhc;
	open my $fhm, "> $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	print $fhm "";
	close $fhm;

	my $prize = int($maze_bet*$leverage*$count);
	my $total = int(-1 * &coin_move(-1*$prize*$count, $lname) / $count);
	for my $name (@players){
		&coin_move($total, $name);
	}
	return "リセットしました";
}

sub map_reflesh{
	my @lines = ();
	my %sames = ();
	open my $fhm, "+< $maze_file" or &error('迷宮ﾌｧｲﾙが開けません');
	eval { flock $fhm, 2; };
	my $maze = <$fhm>;
	chomp $maze;
	push @lines, "$maze\n";
	while (my $line = <$fhm>) {
		my($mname, $mposx, $mposy, $mflag, $mmap) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		
		if($mname eq $m{name}){
			for my $i (-1..1){
				for my $j (-1..1){
					my $type = &get_point($maze, $mposx+$i, $mposy+$j);
					$mmap = &set_point($mmap, $mposx+$i, $mposy+$j, $type);
				}
			}
		}
		push @lines, "$mname<>$mposx<>$mposy<>$mflag<>$mmap<>\n";
	}
	seek  $fhm, 0, 0;
	truncate $fhm, 0;
	print $fhm @lines;
	close $fhm;
}

sub print_arrow{
	my ($leader) = @_;
	
	print qq|<table>|;
	
	print qq|<tr><td></td>|;
	print qq|<td><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="move">|;
	print qq|<input type="hidden" name="leader" value="$leader">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="direction" value="0">|;
	print qq|<input type="submit" value="上" class="button_s" accesskey="2"></form></td>|;
	print qq|<td></td></tr>|;

	print qq|<tr>|;
	print qq|<td><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="move">|;
	print qq|<input type="hidden" name="leader" value="$leader">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="direction" value="3">|;
	print qq|<input type="submit" value="左" class="button_s" accesskey="4"></form></td>|;
	print qq|<td></td>|;
	print qq|<td><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="move">|;
	print qq|<input type="hidden" name="leader" value="$leader">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="direction" value="1">|;
	print qq|<input type="submit" value="右" class="button_s" accesskey="6"></form></td>|;
	print qq|</tr>|;
	
	print qq|<tr><td></td>|;
	print qq|<td><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="move">|;
	print qq|<input type="hidden" name="leader" value="$leader">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="direction" value="2">|;
	print qq|<input type="submit" value="下" class="button_s" accesskey="8"></form></td>|;
	print qq|<td></td></tr>|;

	print qq|</table>|;
	
	print qq|<a href="javascript:void(0);" onclick="window.open('maze_small.cgi?id=$id&pass=$pass&leader=$leader', '迷宮操作用', 'width=250,height=350,scrollbars=no,resizable=no,menubar=no,toolbar=no,location=no,status=no');">方向キーを別窓で開く(firefox未対応)</a>|;
}

sub print_map{
	my($maze, $position_x, $position_y) = @_;
	my $ret = '';

	if($is_mobile){
		my @mlines = split '/', $maze;
		for my $my (1..$#mlines-1){
			my @line = split /,/, $mlines[$my];
			for my $mx (1..$#line-1){
				my $type = $line[$mx];
				my $color;
				if($mx == $position_x && $my == $position_y){
					$color = "#00ffff";
				}elsif($type == $road || ($mx == 2 && $my == 1)){
					$color = "#ff0000";
				}elsif($type == $wall){
					$color = "#0000ff";
				}elsif($type == $unknown){
					$color = "#00ff00";
				}elsif($type == $treasure){
					$color = "#ffff00";
				}
				$ret .= qq|<span style="background-color:$color"><font color="$color">*</font></span>|;
			}
			$ret .= '<br>';
		}
	}else{
		$ret .= '<table>';
		my @mlines = split '/', $maze;
		for my $my (1..$#mlines-1){
			$ret .= '<tr>';
			my @line = split /,/, $mlines[$my];
			for my $mx (1..$#line-1){
				my $type = $line[$mx];
				my $color;
				if($mx == $position_x && $my == $position_y){
					$color = "#00ffff";
				}elsif($type == $road || ($mx == 2 && $my == 1)){
					$color = "#ff0000";
				}elsif($type == $wall){
					$color = "#0000ff";
				}elsif($type == $unknown){
					$color = "#00ff00";
				}elsif($type == $treasure){
					$color = "#ffff00";
				}
				$ret .= qq|<td bgcolor="$color"><font color="$color">*</font></td>|;
			}
			$ret .= '</tr>';
		}
		$ret .= '</table>';
	}
	print $ret;
}

sub print_linked_map{
	my($maze) = @_;

	my $ret = '<table>';
	my @mlines = split '/', $maze;
	for my $my (1..$#mlines-1){
		$ret .= '<tr>';
		my @line = split /,/, $mlines[$my];
		for my $mx (1..$#line-1){
			my $type = $line[$mx];
			my $color;
			if($type == $road || ($mx == 2 && $my == 1)){
				$color = "#ff0000";
			}elsif($type == $wall){
				$color = "#0000ff";
			}elsif($type == $unknown){
				$color = "#00ff00";
			}
			$ret .= qq|<td bgcolor="$color"><font color="$color"><a href="?id=$id&pass=$pass&mode=treasure&x=$mx&y=$my">*</a></font></td>|;
		}
		$ret .= '</tr>';
	}
	$ret .= '</table>';
	print $ret;
}

sub get_size{
	my($maze) = @_;
	my @mlines = split '/', $maze;
	my @line = split /,/, $mlines[0];
	my $size_x = int(@line / 2) - 1;
	my $size_y = int(@mlines / 2) - 1;
	return ($size_x, $size_y);
}
sub maze_finish_check{
	my($maze) = @_;
	my $ret = 1;
	
	my @mlines = split '/', $maze;
	for my $my (0..$#mlines){
		my @line = split /,/, $mlines[$my];
		for my $mx (0..$#line){
			if($mx % 2 == 0 && $my % 2 == 0){
				if($line[$mx] != $road){
					$ret = 0;
				}
			}
		}
	}
	return $ret;
}

sub set_point{
	my($maze, $x, $y, $type) = @_;
	my @mlines = split '/', $maze;
	for my $my (0..$#mlines){
		my @line = split /,/, $mlines[$my];
		for my $mx (0..$#line){
			if($mx == $x && $my == $y){
				$line[$mx] = $type;
			}
		}
		$mlines[$my] = join ',', @line;
	}
	$maze = join '/', @mlines;
	return $maze;
}

sub get_point{
	my($maze, $x, $y) = @_;
	if($x == 2 && $y == 1){
		return $road;
	}
	my @mlines = split '/', $maze;
	for my $my (0..$#mlines){
		my @line = split /,/, $mlines[$my];
		for my $mx (0..$#line){
			if($mx == $x && $my == $y){
				$type = $line[$mx];
			}
		}
	}
	return $type;
}

sub treasure_setted{
	my($maze) = @_;
	my $treasure_num = 0;
	my @mlines = split '/', $maze;
	for my $my (0..$#mlines){
		my @line = split /,/, $mlines[$my];
		for my $mx (0..$#line){
			if($line[$mx] == $treasure){
				$treasure_num++;
			}
		}
	}
	return $treasure_num;
}

sub coin_move_atob{
	my ($from, $to, $coin, $display) = @_;
	
	my $v = -1 * &coin_move(-1*$coin, $from, !$display);
	&coin_move($v, $to, !$display);
}

1;#削除不可
