#================================================
# fx
#================================================
require './lib/fx_func.cgi';

sub run {
	if ($in{mode} eq "ask") {
		$mes = &ask($in{perica});
		$in{comment} = "L:$in{perica} ﾍﾟﾘｶ";
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bid") {
		$mes = &bid($in{perica});
		$in{comment} = "S:$in{perica} ﾍﾟﾘｶ";
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "kessai") {
		$mes = &kessai;
		$in{comment} = "決済しました";
		&write_comment if $in{comment};
	}
	&write_user;
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $rate, $waiting, $state, $wmember) = &get_member;
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;

	print qq|<h2>$this_title</h2>|;
	
	my $v = &get_value;
	
	print qq|$mes|;
	print qq|今のレートは 1 ﾍﾟﾘｶ = $v ｺｲﾝ<br>|;
	print(&print_leverage);
	print(&print_gain_loss($v));
	print(&print_chart);

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

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="perica" class="text_box_b"> ﾍﾟﾘｶ<input type="hidden" name="mode" value="trade">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="radio" name="mode" value="quit" checked>やめる<br>|;
	print qq|<input type="radio" name="mode" value="ask">long<br>|;
	print qq|<input type="radio" name="mode" value="bid">short<br>|;
	print qq|<input type="radio" name="mode" value="kessai">決済<br>|;
	print qq|<input type="submit" value="取引" class="button_s"></form><br>|;
			
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
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
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
	
	my $member_c = @members - 1;
	return ($member_c, $member);
}

1;#削除不可
