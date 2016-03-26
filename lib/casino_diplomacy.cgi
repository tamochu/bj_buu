require './lib/_casino_funcs.cgi';
#================================================
# ディプロマシー
#================================================
my @places = (
	#[0]ID	[1]Name	[2]kind	[3]Next
	[0,		'hoge',	0,		[]]
);

sub run {
	if ($in{mode} eq "play") {
		$in{comment} = &play;
	} elsif ($in{mode} eq "start") {
		$in{comment} = &start_game;
		&write_comment if $in{comment};
	} elsif ($in{mode} eq "add") {
	    $in{comment} = &add_order;
	} elsif ($in{mode} eq "del") {
	    $in{comment} = &del_order;
	} elsif ($in{mode} eq "write" &&$in{comment}) {
		&write_comment;
	}
	my ($member_c, $member) = &get_member;
	my $state = &get_state;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
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

	if($state->turn()){
		&print_order;
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="play">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="命令を出す" class="button_s"></form><br>|;
	}else {
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
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>\n";
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
}

sub set_state {
	my $state = shift;
}

sub print_order {
	if ($m{country}) {
		my $state = &get_state;
		my $i = 0;
		for my $order ($state->getOrders($m{country} - 1)) {
			print qq|$order|;
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="del">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="hidden" name="delOrder" value="$i">|;
			print qq|<input type="submit" value="削除" class="button_s"></form>|;
			print qq|<br>|;
			$i++;
		}
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="add">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="text" name="order">|;
		print qq|<input type="submit" value="追加" class="button_s"></form>|;
	}
}

sub play {
	if ($m{country} && $cs{pro}[$m{country}] eq $m{name}) {
		my $state = &get_state;
		
		$state->thinkEnd($m{country} - 1);
		
		&set_state($state);
	}
}

sub add {
	if ($m{country} && $cs{pro}[$m{country}] eq $m{name}) {
		my $state = &get_state;
		
		my $order = $in{order};
		
		$state->addOrder($m{country} - 1, $order);
		&set_state($state);
	}
}

sub del {
	if ($m{country} && $cs{pro}[$m{country}] eq $m{name}) {
		my $state = &get_state;
		
		$state->delOrder($m{country} - 1, $in{delOrder});
		&set_state($state);
	}
}

sub start_game {
	if ($m{country} && $cs{pro}[$m{country}] eq $m{name}) {
		my $state = &get_state;
		
		&set_state($state);
		return ("ｹﾞｰﾑを始めます$turnの番です");
	}
}

1;#削除不可
