#================================================
# 転職所 Created by Merino ###
#================================================

# 転職に必要な金額
my $need_money = $m{sedai} > 10 ? 20000 : $m{sedai} * 2000;


#=================================================
sub begin {
	$mes .= 'ここは転職所じゃ。お主の職業を変えることができるぞ<br>';
	$mes .= "ただし、転職するには $need_money G必要じゃぞ<br>";
	$mes .= '職業を変えるのか?<br>';

	my @menus = ('やめる');
	for my $i (0 .. $#jobs) {
		push @menus, $jobs[$i][11]->() ? $jobs[$i][1] : '';
	}
	&menu(@menus);
}

sub tp_1 {
	--$cmd;
	if ($m{job} eq $cmd) {
		$mes .= "$jobs[$cmd][1]になりたいと申\すか…<br>え?でも、すでにその職業になっておるではないか?<br>";
	}
	elsif ($m{job} eq '24') {
		$mes .= '魔法少女が魔法少女でなくなるのは最終回だけじゃ<br>';
	}
	elsif ($cmd >= 0 && &{ $jobs[$cmd][11] }) {
		if ($m{money} >= $need_money) {
			$m{money} -= $need_money;
			&remove_pet if $cmd eq '21';
			$m{job} = $cmd;
			$mes .= "$jobs[$cmd][1]となって新たな道を進むがよい<br>$m{name}は$jobs[$cmd][1]に転職しました<br>";
			&run_tutorial_quest('tutorial_job_change_1');
		}
		else {
			$mes .= 'お金が足りんぞい<br>お金をためてまた来なされ<br>';
		}
	}
	else {
		$mes .= 'その職業に転職する条件が満たされていないようじゃ<br>';
	}

	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}




1; # 削除不可
