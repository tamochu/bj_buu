require "$datadir/hunting.cgi";
require "$datadir/skill.cgi";
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
#================================================
# 討伐の魔物追加 Created by Merino
#================================================

# 最大生息数(古い魔物から自動削除)
my $max_monster = 30;

# 魔物から送られてくるﾀﾏｺﾞ
my @egg_nos = (1..34,42..51);

# 魔物の最後の言葉
my @m_messages = (qw/ｵﾊﾖｰ ｵｯﾊﾟﾋﾟｰ ｵｯﾍﾟｹﾍﾟｰ ﾓｹﾞﾓｹﾞ ﾎｹﾞﾎｹﾞ ｺﾞﾆｮｺﾞﾆｮ ﾎﾟﾛﾝﾎﾟﾛﾝ ﾎﾟｲﾝﾋﾟﾖﾝ ﾑｷｮｷｮｷｮｷｮ ｳｷｷｷｷｷ ｳｼｼｼｼ ﾃｹﾃｹﾃｹﾃ ｼﾃﾔｯﾀﾅﾘ ﾆｮﾝﾆｮﾝ ﾃｰｯﾃｯﾃﾃｰ/);


#================================================
sub tp_100 {
	my $v = &use_pet('myself');
	my $skill_st = 0;
	my $i = 0;
	for my $skill (split /,/, $m{skills}) {
		$i++;
		if ($skills[$skill][2] eq $weas[$m{wea}][2]) {
			$skill_st += $skills[$skill][7];
		} else {
			$skill_st += $skills[0][7];
		}
	}
	for (my $j = $i; $j < 5; $j++) {
		$skill_st += $skills[0][7];
	}
	$skill_st = 100 if $skill_st > 100;
	$skill_st = 0 if $skill_st < 0;
	my $m_st = int(&m_st * $v * 0.5 * (0.5 + 1.0 * $skill_st / 100));
	my $place = '';
	for my $i (0 .. $#places) {
		my $j = $#places-$i;
		if ($m_st >= $places[$j][1]) {
			$place = $places[$j][2];
			last;
		}
	}

	$layout = 1;
	$mes .= qq|魔物の名前を決めてください<br>|;
	$mes .= qq|強さ：$m_st 生息地：$place<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|名前[全角10(半角20)文字まで]：<input type="text" name="name" value="$m{name}ﾓﾝｽﾀｰ" class="text_box1"><br>|;
	$mes .= qq|勝ちｾﾘﾌ[全角20(半角40)文字まで]：<input type="text" name="mes_win"  value="$m{mes_win}" class="text_box1"><br>|;
	$mes .= qq|負けｾﾘﾌ[全角20(半角40)文字まで]：<input type="text" name="mes_lose" value="$m{mes_lose}" class="text_box1"><br>|;

	if ($default_icon) {
		$mes .= qq|<hr>魔物の画像を選択してください<br>|;
		$mes .= qq|※自作画像の場合は、魔物が生息地からいなくなったときに戻ってきます<br>|;
	
		$mes .= qq|<input type="radio" name="file_name" value="$default_icon" checked><img src="$icondir/$default_icon" style="vertical-align:middle;" $mobile_icon_size><hr>|;
		opendir my $dh, "$userdir/$id/picture" or &error("$userdir/$id/picture ﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /^_/;
			next if $file_name =~ /^index.html$/;
			$mes .= qq|<input type="radio" name="file_name" value="$file_name"><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;" $mobile_icon_size><hr>|;
		}
		closedir $dh;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="決定" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

# ------------------
sub tp_110 {
	my $is_error = 0;
	unless ($in{name}) {
		$is_error = 1;
	}
	
	my %e2j_checks = (name => '名前', mes_win => '勝ちｾﾘﾌ', mes_lose => '負けｾﾘﾌ');
	for my $k (keys %e2j_checks) {
		if ($in{$k} =~ /[,;\"\'&<>]/) {
			$mes .= "$e2j_checks{$k}に不正な文字( ,;\"\'&<> )が含まれています<br>";
			$is_error = 1;
			last;
		}
		elsif ($in{$k} =~ /　/ || $in{name} =~ /\s/) {
			$mes .= "$e2j_checks{$k}に不正な空白が含まれています<br>";
			$is_error = 1;
			last;
		}
		else {
			if ($k eq 'name' && length($in{$k}) > 20) {
				$mes .= "$e2j_checks{$k}は全角10(半角20)文字以内です<br>";
				$is_error = 1;
				last;
			}
			elsif (length($in{$k}) > 40) {
				$mes .= "$e2j_checks{$k}は全角20(半角40)文字以内です<br>";
				$is_error = 1;
				last;
			}
		}
	}
	
	if ($is_error) {
		$m{tp} = 100;
		&{ 'tp_'. $m{tp} };
	}
	else {
		my $v = &use_pet('myself');
		
		if ($v > 0) {
			my $skill_st = 0;
			my $i = 0;
			for my $skill (split /,/, $m{skills}) {
				$i++;
				if ($skills[$skill][2] eq $weas[$m{wea}][2]) {
					$skill_st += $skills[$skill][7];
				} else {
					$skill_st += $skills[0][7];
				}
			}
			for (my $j = $i; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			$skill_st = 100 if $skill_st > 100;
			$skill_st = 0 if $skill_st < 0;
			my $m_st = int(&m_st * $v * 0.5 * (0.5 + 1.0 * $skill_st / 100));
		
			for my $i (0 .. $#places) {
				my $j = $#places-$i;
				if ($m_st >= $places[$j][1]) {
					&add_monster($j, $v, (0.5 + 1.0 * $skill_st / 100));
					&c_up('mon_c');
					$mes .= "$in{name}を$places[$j][2]の中に埋めました<br>";
					&remove_pet;
					last;
				}
			}
		}
		
		&refresh;
		&n_menu;
	}
}

# ------------------
sub add_monster {
	my($place, $v, $vv) = @_;
	my $p_name = $places[$place][0];
	
	my $monster = "$in{name}<>$m{country}<>";
	for my $k (qw/max_hp max_mp at df mat mdf ag cha /) {
		$monster .= int($m{$k} * $v * 0.5 * $vv) .'<>';
	}
	my $m_icon = $default_icon;
	if ($default_icon && $in{file_name} !~ /^_/ && -f "$userdir/$id/picture/$in{file_name}") {
		if (-f "$icondir/$in{file_name}") {
			$mes .= "同じﾀｲﾄﾙのｱｲｺﾝがすでに使われていたので、ｱｲｺﾝをつけることはできませんでした<br>";
		}
		else {
			$m_icon = $in{file_name};
			rename "$userdir/$id/picture/$in{file_name}", "$icondir/$in{file_name}";
		}
	}
	$monster .= "$m{wea}<>$m{skills}<>$in{mes_win}<>$in{mes_lose}<>$m_icon<>$m{name}<>\n";
	
	my @lines = ();
	open my $fh, "+< $logdir/monster/$p_name.cgi" or &error("$logdir/monster/$p_name.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		# 魔物画像を返す処理
		if (@lines+1 >= $max_monster) {
			next unless $default_icon;
			my($ymname, $ymes_win, $yicon, $yname) = (split /<>/, $line)[0,-5,-3,-2];
			next if $yicon eq $default_icon;
			next unless -f "$icondir/$yicon"; # 画像がない
			my $y_id  = unpack 'H*', $yname;
			next unless -d "$userdir/$y_id/picture"; # ﾌﾟﾚｲﾔｰが存在しない
			
			# 魔物から主への手紙
			my $m_message = $m_messages[ int( rand(@m_messages) ) ];
			$in{comment}  = qq|$places[$place][2]に住む魔物$ymnameの最後を見届けた$m{name}からの手紙<br><br>|;
			$in{comment} .= qq|$ymnameの最後の言葉『$m_message$ymes_win』<br>|;
			$in{comment} .= qq|$ymnameの画像はﾏｲﾋﾟｸﾁｬに戻りました<br>|;
			$in{comment} .= qq|$ymnameからﾀﾏｺﾞが贈られたようだ<br>|;

			$bad_time = 0;
			&send_letter($yname);
			rename "$icondir/$yicon", "$userdir/$y_id/picture/$yicon"; 
			
			my $egg_no = $egg_nos[int(rand(@egg_nos))];
			&send_item($yname, 2, $egg_no, 0, 0, 1);
		}
		else {
			push @lines, $line;
		}
	}
	unshift @lines, $monster;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}



1; # 削除不可
