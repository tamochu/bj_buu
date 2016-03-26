#================================================
# 年末イベント
#=================================================

# 買う値段
my $buy_price  = 500;

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= 'メリー天皇誕生日<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'よい年越しを<br>';
	}
	
	&menu('やめる','靴下を買う','年賀状を送る');
}

sub tp_1 {
	return if &is_ng_cmd(1..2);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "靴下買うか?<br>片方しかないから $buy_price Gでやる<br>";
		&menu('やめる','買う');
	}
	elsif ($cmd eq '2') {
		$mes .= "おどしたまつき $buy_price Gで送る<br>";
		&menu('やめる', '送る');
	}
	else {
		&begin;
	}
}

#=================================================
# 靴下
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= 'お前貧乏。かわいそうだからやる。片方しかないけどな。<br>';
	}
	else {
		$m{money} -= $buy_price;
	}
	if ($m{sox_kind}) {
		$mes .= 'もう靴下は用意してあるけど別のと取り替えよう<br>';
	}
	$mes .= '靴下にどんな願い入れようか';
	
	$m{tp} += 10;
	&menu('受胎告知', 'ﾘﾌｫｰﾑ', 'あの絵が欲しい', 'かっこいい武器が欲しい');
}

sub tp_110 {
	if ($cmd eq '1') {
		$m{sox_kind} = 3;
		$m{sox_no} = 183;
	} elsif ($cmd eq '2') {
		$m{sox_kind} = 3;
		$m{sox_no} = 168;
	} elsif ($cmd eq '3') {
		if (rand(30) < 1) {
			$m{sox_kind} = 1;
			$m{sox_no} = 33;
		} else {
			$m{sox_kind} = 3;
			$m{sox_no} = 191;
		}
	} else {
		$m{sox_kind} = 3;
		$m{sox_no} = 21;
	}
	&begin;
}

#=================================================
# 年賀状
#=================================================
sub tp_200 {
	$mes .= "誰に年賀状を送りますか?<br>";
	$mes .= "裏面は印刷済みなので書く必要はないよ?<br>";

	$mes .= qq|<form method="$method" action="$script"><p>宛名：<input type="text" name="to_name" class="text_box1"></p>|;
	$mes .= qq|<p>送り主：<input type="text" name="from_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">送る<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="送る" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_210 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= 'はがき代足りない。帰れ。<br>';
	}
	else {
		$m{money} -= $buy_price;
		my $to_id = unpack 'H*', $in{to_name};
		my $number = int(rand(1000000000));
		open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("ポストが開けません");
		print $fh "$in{from_name}<>$id<>$number<>\n";
		close $fh;
	}
	&begin;
}
1; # 削除不可
