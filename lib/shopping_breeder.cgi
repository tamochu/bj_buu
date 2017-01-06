#=================================================
# 育て屋
#=================================================

#何秒ごとに孵化値を上げるか
my $egg_per_sec = 600;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if (!$m{breed} && !$m{egg}) {
		$mes .= '卵を持ってきな<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}


#=================================================
sub begin {
	if($m{breed} eq '0' || $m{breed} eq ''){
		my $v = 30000 +  $eggs[$m{egg}][2] * 50;
		$mes .= "飼育料は $v Gだよ<br>";
		$mes .= "育てるかい?";
		&menu('やめる', '頼む');
	}else {
		$m{breed_c} += int(($time - $m{breed_time}) / $egg_per_sec);
		$m{breed_time} = $time;
		$mes .= "お前さんの $eggs[$m{breed}][1] は今 $m{breed_c} / $eggs[$m{breed}][2]だよ<br>";
		$mes .= "持っていくかい?";
		&menu('やめる', '引き取る');
	}
}

sub tp_1 { #
	if($cmd eq '1'){
		if($m{breed} eq '0' || $m{breed} eq ''){
			my $v = 30000 +  $eggs[$m{egg}][2] * 50;
			if ($m{money} >= $v) {
				$m{money} -= $v;
				$mes .= "預かったよ<br>";
				$m{breed} = $m{egg};
				$m{breed_c} = $m{egg_c};
				$m{egg} = 0;
				$m{egg_c} = 0;
				$m{breed_time} = $time;
				&run_tutorial_quest('tutorial_breeder_1');
			}
			else {
				$mes .= "金を用意してきな!<br>";
			}
		}
		else {
			&send_item($m{name},2,$m{breed},$m{breed_c},0, int(rand(100)));
			$m{breed} = 0;
			$m{breed_c} = 0;
			$mes .= "送ったよまたよろしくな<br>";
		}
	}
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}

1; # 削除不可
