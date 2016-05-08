#================================================
# ｶｼﾞﾉ共用関数
#================================================
sub coin_move{
	my ($m_coin, $name, $no_system_comment) = @_;
	my $ret_v;
	
	my $player_id = unpack 'H*', $name;

	# 存在しない場合はスキップ
	unless (-f "$userdir/$player_id/user.cgi") {
		return $ret_v;
	}
	if($name eq $m{name}){
		if ($m{coin} + $m_coin < 0){
			$ret_v = -1 * $m{coin};
		}else {
			$ret_v = $m_coin;
		}
		
		$m{coin} += $ret_v;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $m_coin;

		if ($temp < 0){
			$temp = 0;
			$ret_v = -1 * $datas1{coin};
		} else {
			if ($temp > 2500000) {
				$temp = 2500000;
			}
			$ret_v = $m_coin;
		}
		&regist_you_data($name,'coin',$temp);
	}

	unless ($no_system_comment) {
		if($ret_v > 0){
			&system_comment("$name は $ret_v ｺｲﾝ得ました");
		}else{
			my $temp = -1 * $ret_v;
			&system_comment("$name は $temp ｺｲﾝ払いました");
		}
	}
	
	if ($m_coin < $ret_v) {
		my $diff = ($ret_v - $m_coin) * 10;
			
		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_fileが開けません");
			eval { flock $fh, 2; };
			
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff;
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	
	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# 存在しない場合はスキップ
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name は $mes_as として $prize を獲得しました");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name が $mes_news</font>|);
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

sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

1;#削除不可
