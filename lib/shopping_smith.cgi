#=================================================
# 鍛冶屋 Created by Merino
#=================================================

# 修理金
my $need_money = int( ($weas[$m{wea}][3]+$weas[$m{wea}][5]) * 50 + $weas[$m{wea}][4] * 2 + $m{wea_lv} * 1000);


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if (!$m{wea}) {
		$mes .= '武器を装備してからまた来な!<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	elsif($m{wea_c} > 10) {
		$mes .= 'アンタの武器はまだ修理する必要はないだろう。もっと使い込んでからまた来な!<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}


#=================================================
sub begin {
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	$mes .= 'ここは鍛冶屋だ。装備している武器を修理するぜ<br>';
	$mes .= "ずいぶんと使い込んだ $wname だな<br>";
	$mes .= "修理費は、$need_money Gになるぜ。どうする?";
	&menu('やめる', '修理を頼む');
}

sub tp_1 { # 修理
	if ($cmd eq '1' && $m{wea} && $m{wea_c} <= 10) {
		my $v = int($weas[$m{wea}][3] * 100); 
		
		if ($m{money} >= $need_money) {
			$need_money = &use_pet('smith', $need_money);
			$need_money = &seed_bonus('smith', $need_money);
			$m{money} -= $need_money;
			++$m{wea_lv} if $m{wea_lv} < 30;


			if ($m{wea} eq '31' && $m{wea_lv} >= 30) {
				$mes .= "$weas[$m{wea}][1]は粉々に砕け散り$weas[32][1]になりました<br>";
				$m{wea} = 32;
				$m{wea_lv} = 10;
			}
			else {
				$mes .= 'おし!新品同様に修理完了したぜ!またな!<br>';
			}

			$m{wea_c} = $weas[$m{wea}][4];
		}
		else {
			$mes .= "金が足りないぜ!またな!<br>";
		}
	}
	
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}


1; # 削除不可
