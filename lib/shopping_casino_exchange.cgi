$mes .= qq|ｺｲﾝ $m{coin} 枚<br>| if $is_mobile;
#================================================
# ｶｼﾞﾉ交換所 Created by Merino
#================================================

# 交換賞品
my @prizes = (
# 種類 1=武器,2=卵,3=ﾍﾟｯﾄ 
#	[0]種類,[1]No,[2]ﾒﾀﾞﾙ,[3]その他ﾌﾗｸﾞ
	[0,	0,	0,		0,],
	[2,	22,	1000,	0,],
	[2,	24,	3000,	0,],
	[2,	16,	5000,	0,],
	[2,	51,	5000,	0,],
	[2,	23,	5000,	0,],
	[1,	2,	10000,	0,],
	[1,	7,	10000,	0,],
	[1,	22,	10000,	0,],
	[2,	25,	20000,	0,],
	[3,	126,40000,	0,],
	[3,	197,40000,	0,],
	[2,	3,	80000,	0,],
	[2,	2,	200000,	0,],
	[2,	54,	2500000,1,],
);


#================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]はお断りだ<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ここは、手持ちのお金をｺｲﾝに交換したり<br>';
		$mes .= 'ｺｲﾝと賞品の交換をすることができます<br>';
		$mes .= 'どうしますか？<br>';
	}
	&menu('やめる','ｺｲﾝに交換','賞品と交換');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# お金→ｺｲﾝに交換
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= "$m{name}様はｺｲﾝを$m{coin}枚お持ちです<br>";
	$mes .= 'ｺｲﾝ1枚20Gです<br>いくらお求めですか?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="coin" value="0" class="text_box1" style="text-align:right">枚|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="交換する" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($in{coin} && $in{coin} !~ /[^0-9]/) {
		my $v = int($in{coin} * 20);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{coin}  += $in{coin};
			$mes .= "$v Gをｺｲﾝ $in{coin} 枚に交換しました<br>";
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	&begin;
}


#=================================================
# ｺｲﾝ→賞品に交換
#=================================================
sub tp_200 {
	$layout = 1;
	
	$mes .= "$m{name}様はｺｲﾝを$m{coin}枚お持ちです<br>";
	$mes .= "どの賞品と交換しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>賞品</th><th>必要ｺｲﾝ<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked> やめる<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i"> |;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[卵]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[ペ]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		if($prizes[$i][3]){
			$mes .= qq|<td align="right">$prizes[$i][2]ｺｲﾝ+所持金すべて(4999999G以上)<br></td></tr>|;
		}else{
			$mes .= qq|<td align="right">$prizes[$i][2]ｺｲﾝ<br></td></tr>|;
		}
	}
	$mes .= qq|</table>|;
	$mes .= qq|<p>×<input type="text" name="loop" value="1" class="text_box1" style="text-align:right"></p>|;
	$mes .= qq|<p><input type="submit" value="交換する" class="button1"></p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"></form>|;
	$m{tp} += 10;
}
sub tp_210 {
	if ($in{loop} && $in{loop} !~ /[^0-9]/ && $in{loop} < 300) {
		for my $loop (1..$in{loop}) {
			if ($cmd) {
				for my $i (1 .. $#prizes) {
					next unless $cmd eq $i;
					
					my $other_flag = 0;
					my $total_money = $m{money};
					if($m{bank} && -f "$userdir/$shop_id/shop_bank.cgi"){
						my $shop_id = unpack 'H*', $m{bank};
						open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");

						my $head_line = <$fh>;
						my $v;
						while (my $line = <$fh>) {
							my($year, $name, $money) = split /<>/, $line;

							if ($m{name} eq $name) {
								$total_money += $money;
							}
						}
						close $fh;
					}
					if($total_money >= 4999999){
						$other_flag = 1;
					}
					unless($prizes[$i][3]){
						$other_flag = 1;
					}
					
					if ($m{coin} >= $prizes[$i][2] && $other_flag) {
						$m{coin} -= $prizes[$i][2];
						if($prizes[$i][3]){
							$m{money} = 0;
							if($m{bank}){
								my $shop_id = unpack 'H*', $m{bank};
								my $is_rewrite = 0;
								my @lines = ();
								open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
								eval { flock $fh, 2; };

								my $head_line = <$fh>;
								push @lines, $head_line;
								while (my $line = <$fh>) {
									my($year, $name, $money) = split /<>/, $line;

									if ($m{name} eq $name) {
										$is_rewrite = 1;
									} else {
										push @lines, $line;
									}
								}
								if ($is_rewrite) {
									seek  $fh, 0, 0;
									truncate $fh, 0;
									print $fh @lines;
								}
								close $fh;
								$m{bank} = '';
							}
						}
						if ($prizes[$i][0] eq '1') {
							$mes .= "$weas[ $prizes[$i][1] ][1]に交換しました<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], $weas[ $prizes[$i][1] ][4], 0, 1);
						}
						elsif ($prizes[$i][0] eq '2') {
							$mes .= "$eggs[ $prizes[$i][1] ][1]に交換しました<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], 0, 0, 1);
						}
						elsif ($prizes[$i][0] eq '3') {
							$mes .= "$pets[ $prizes[$i][1] ][1]に交換しました<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], 0, 0, 1);
						}
					}
					else {
						$mes .= 'ｺｲﾝが足りません<br>';
					}
					last;
				}
			}
		}
	}
	&begin;
}




1; # 削除不可
