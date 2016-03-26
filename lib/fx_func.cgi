my $this_file = "$logdir/fx.cgi";
my $member_file = "$logdir/fx_member.cgi";
my $user_file = "$userdir/$id/fx.cgi";
#=================================================
# FX(笑)
#=================================================
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Response;

my $upload_time = 60;
my $margin_call = 0.5;
my $loss_cut = 0.3;

my $coin_max = 2500000;
my $leverage = 25;

@bflow_item = (
	#種類,  番号, 耐久値など, ★
	[1,32,500,30],
	[2,3,998,0],
	[2,53,0,0],
	[3,17,0,0],
	[3,18,0,0],
	[3,21,0,0],
	[3,64,0,0],
	[3,75,0,0],
	[3,125,0,0],
	[3,127,0,0],
	[3,143,0,0],
	[3,144,0,0],
	[3,132,0,0],
	[3,164,0,0],
	[3,168,0,0],
	[3,183,0,0],
	[3,184,0,0],
	[3,187,0,0],
	[3,189,0,0],
	[3,190,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
	[3,38,0,0],
);

@flow_item = (
	#種類,  番号, 耐久値など, ★
	[2,3,0,0],
	[3,17,0,0],
	[3,18,0,0],
	[3,38,0,0],
	[3,75,0,0],
	[3,132,0,0],
	[3,164,0,0],
	[3,184,0,0],
	[3,187,0,0],
	[3,189,0,0],
	[3,190,0,0],
);
#はずれ
@lflow_item = (
	[2,22,0,0],
	[2,42,0,0],
	[3,120,0,0],
	[3,121,0,0],
	[3,176,0,0],
);
#=================================================
sub ask{
	my $perica = shift;
	my $rate = &get_value;
	my $total_position = &get_total_position;
	if($total_position + $rate * $perica < $leverage * $m{coin}){
		open my $fh, ">> $user_file" or &error("$user_fileが読み込めません");
		my $buy_time = $time + 10 * 60;
		print $fh "L<>0<>$in{perica}<>$buy_time<>\n";
		close $fh;
	}else{
		return "レバレッジ限界を超えてるよ";
	}
}
sub bid{
	my $perica = shift;
	my $rate = &get_value;
	my $total_position = &get_total_position;
	if($total_position + $rate * $perica < $leverage * $m{coin}){
		my $buy_time = $time + 10 * 60;
		open my $fh, ">> $user_file" or &error("$user_fileが読み込めません");
		print $fh "S<>0<>$in{perica}<>$buy_time<>\n";
		close $fh;
	}else{
		return "レバレッジ限界を超えてるよ";
	}
}
sub get_total_position{
	my $rate = &get_value;
	my $total_position = 0;
	if(-f "$user_file"){
		open my $fh, "< $user_file" or &error("$user_fileが読み込めません");
		while(my $line = <$fh>){
			my($tkind, $trate, $tnum, $buy_time) = split /<>/, $line;
			unless($trate){
				$trate = $rate;
			}
			my $gold = $trate * $tnum;
			$total_position += $gold;
		}
		close $fh;
	}
	return $total_position;
}
sub print_leverage{
	return "掲示板に重要なお知らせがあります<br>レバレッジは $leverage までだよ<br>";
}
sub print_gain_loss{
	my $v = shift;
	my $ret_mes = '';

	if(-f "$user_file"){
		my @lines = ();
		open my $fh, "+< $user_file" or &error("$user_fileが読み込めません");
		eval { flock $fh, 2; };
		my $gain_loss = 0;
		while(my $line = <$fh>){
			my($kind, $rate, $num, $buy_time) = split /<>/, $line;
			if($rate){
				my $gold = $rate * $num;
				if($kind eq 'L'){
					$ret_mes .= "long $rate $numﾍﾟﾘｶ : $gold ｺｲﾝ<br>";
					$gain_loss += ($v - $rate) * $num;
				}else{
					$ret_mes .= "short $rate $numﾍﾟﾘｶ : $gold ｺｲﾝ<br>";
					$gain_loss -= ($v - $rate) * $num;
				}
			}else{
				$rate = &time_to_rate($buy_time);
				if($kind eq 'L'){
					$ret_mes .= "long 注文中 $numﾍﾟﾘｶ<br>";
				}else{
					$ret_mes .= "short 注文中 $numﾍﾟﾘｶ<br>";
				}
			}
			$buy_time =~ tr/\x0D\x0A//d;
			push @lines, "$kind<>$rate<>$num<>$buy_time<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if($gain_loss){
			if($gain_loss > 0){
				$ret_mes .= "現在 $gain_loss ｺｲﾝの儲けだよ<br>";
			}else{
				my $absgl = $gain_loss * -1;
				$ret_mes .= "現在 $absgl ｺｲﾝの損失だよ<br>";
				if($m{coin} * (1 - $loss_cut) < $absgl){
					$ret_mes.= "ロスカットしちゃったよ。とほほ<br>";
					&kessai;
				}elsif($m{coin} * $margin_call < $absgl){
					$ret_mes.= "マージンコール発生中注意<br>";
				}
			}
		}
	}
	return $ret_mes;
}
sub print_chart{
	my $ret_mes;
	
	open my $fhp, "< $this_file" or &error("$this_fileが読み込めません");
	my @plines = <$fhp>;
	close $fhp;
	my $chd = '';
	while(@plines > 30){
		shift @plines;
	}
	my @pdatas = ();
	my $pmax = 0;
	my $pmin = 1000;
	for my $pline (@plines){
		my ($rate, $time) = split /<>/, $pline;
		if($pmax < $rate){
			$pmax = $rate;
		}
		if($pmin > $rate){
			$pmin = $rate;
		}
		push @pdatas, $rate;
	}
	my $band = $pmax - $pmin;
	if($band == 0){
		$band = 1;
	}
	my $center = ($pmax + $pmin) / 2;
	for my $pdata (@pdatas){
		my $pdata2 = ($pdata - $center) * 50 / $band + 50;
		$chd .= "$pdata2,";
	}
	chop $chd;
	
	$ret_mes .= qq|<hr size="1"><h1>ﾍﾟﾘｶﾁｬｰﾄ</h1>|;
	$ret_mes .= qq{<img src="http://chart.apis.google.com/chart?cht=lc&chs=500x350&chd=t:$chd"><br>};
	return $ret_mes;
}
sub check_losscut{
	my $ret_mes = '';
	if(-f "$user_file"){
		my $v = &get_value;
		my @lines = ();
		open my $fh, "< $user_file" or &error("$user_fileが読み込めません");
		my $gain_loss = 0;
		while(my $line = <$fh>){
			my($kind, $rate, $num, $buy_time) = split /<>/, $line;
			if($rate){
				my $gold = $rate * $num;
				if($kind eq 'L'){
					$gain_loss += ($v - $rate) * $num;
				}else{
					$gain_loss -= ($v - $rate) * $num;
				}
			}
		}
		close $fh;
		
		if($gain_loss){
			if($gain_loss < 0){
				my $absgl = $gain_loss * -1;
				if($m{coin} * (1 - $loss_cut) < $absgl){
					$ret_mes.= "ロスカットしちゃったよ。とほほ<br>";
					&kessai;
				}
			}
		}
	}
	return $ret_mes;
}
sub get_value{
	my $ret_value;
	open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
	eval { flock $fh, 2; };
	my @lines = ();
	my $line;
	my $value;
	my $vtime;
	while($line = <$fh>){
		push @lines, $line;
		($value, $vtime) = split /<>/, $line;
	}
	
	if($time > $vtime + $upload_time){
		our $url = 'http://stocks.finance.yahoo.co.jp/stocks/history/?code=USDJPY=X';
		my $proxy = new LWP::UserAgent;
		
		my $req = HTTP::Request->new('GET' => $url);
		my $res = $proxy->request($req);
		my $content = $res->content;
		if($content =~ /<td class="stoksPrice">(\d\d\d).(\d\d\d\d\d\d)<\/td>/g){
			$ret_value = "$1\.$2";
		}elsif($content =~ /<td class="stoksPrice">(\d\d).(\d\d\d\d\d\d)<\/td>/g){
			$ret_value = "$1\.$2";
		}
		if($ret_value){
			push @lines, "$ret_value<>$time<>\n";
		}else{
			$ret_value = $value;
		}
	}else{
		$ret_value = $value;
	}
	while (@lines > 100){
		shift @lines;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	return $ret_value;
}
sub kessai{
	my $v = &get_value;
	if(-f "$user_file"){
		my @lines = ();
		open my $fh, "+< $user_file" or &error("$user_fileが読み込めません");
		eval { flock $fh, 2; };
		my $gain_loss;
		while(my $line = <$fh>){
			my($kind, $rate, $num, $buy_time) = split /<>/, $line;
			unless($rate){
				push @lines, $line;
				next;
			}
			if($kind eq 'L'){
				$gain_loss += ($v - $rate) * $num;
			}else{
				$gain_loss -= ($v - $rate) * $num;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$m{coin} += int($gain_loss);
		if($m{coin} < 0){
			$m{coin} = 0;
			$m{shogo} = $shogos[1][0];
			$m{shogo_t} = $shogos[1][0];
		}elsif($m{coin} > $coin_max){
			&coin_to_item;
		}
	}
}
sub coin_to_item{
	$mes .= '持ちきれない分を適当にアイテムに換金しといたよ';
	while($m{coin} > $coin_max){
		if($m{coin} > $coin_max + 1000000){
			$m{coin} -= 1000000;
			my $item_no = int(rand(@bflow_item));
			&send_item($m{name},$bflow_item[$item_no][0],$bflow_item[$item_no][1],$bflow_item[$item_no][2],$bflow_item[$item_no][3],1);
		}elsif($m{coin} > $coin_max + 100000){
			$m{coin} -= 500000;
			my $item_no = int(rand(@flow_item));
			&send_item($m{name},$flow_item[$item_no][0],$flow_item[$item_no][1],$flow_item[$item_no][2],$flow_item[$item_no][3],1);
		}else{
			$m{coin} -= 50000;
			my $item_no = int(rand(@lflow_item));
			&send_item($m{name},$lflow_item[$item_no][0],$lflow_item[$item_no][1],$lflow_item[$item_no][2],$lflow_item[$item_no][3],1);
		}
	}
}
sub add_member{
	my @lines = ();
	my $is_find = 0;
	open my $fh, "+< $member_file" or &error("$member_fileが読み込めません");
	eval { flock $fh, 2; };
	while(my $line = <$fh>){
		push @lines, $line;
		$line =~ tr/\x0D\x0A//d;
		if($line eq $m{name}){
			$is_find = 1;
		}
	}
	unless($is_find){
		push @lines, "$m{name}\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
sub del_member{
	my @lines = ();
	open my $fh, "+< $member_file" or &error("$member_fileが読み込めません");
	eval { flock $fh, 2; };
	while(my $line = <$fh>){
		$line =~ tr/\x0D\x0A//d;
		unless($line eq $m{name}){
			push @lines, "$line\n";
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
sub time_to_rate{
	$buy_time = shift;
	
	my $ret_rate = 0;
	open my $fhp, "< $this_file" or &error("$this_fileが読み込めません");
	my @plines = <$fhp>;
	close $fhp;
	for my $line (@plines){
		my ($rate, $rtime) = split /<>/, $line;
		if($rtime > $buy_time && $rate){
			$ret_rate = $rate;
			last;
		}
	}
	return $ret_rate;
}
1; # 削除不可
