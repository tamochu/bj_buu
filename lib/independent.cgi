
#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($w{world} ne $#world_states-4) {
		$mes .= "まだ時期じゃない…<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{sedai} < 10) {
		$mes .= "10世代ぐらい経験を積んでから出直してきな<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		$mes .= "おじいちゃん独立はさっきしたでしょ！<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($w{country} >= 10) {
		$mes .= "独立する領土がもうないよ<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
# 独立
#================================================
sub begin {
	&tp_1;
}

sub tp_1 {
	$mes .= "一念発起して独立しますか?";
	$m{tp} = 100;
	&menu('やめる', '独立');
}

sub tp_100 {
	if ($cmd) {
		&create_country;
	
		require "./lib/move_player.cgi";
		
		&move_player($m{name}, $m{country}, $w{country});
		$m{country} = $w{country};

		$cs{ceo}[$w{country}] = $m{name};
		$m{vote} = $m{name};

		&write_cs;
		&mes_and_world_news("独立しました。");
		
		&cs_data_repair;
	}
	&refresh;
	&n_menu;
}
1; # 削除不可
