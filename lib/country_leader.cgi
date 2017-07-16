my $this_file = "$logdir/$m{country}/leader.cgi";
#=================================================
# 代表投票 Created by Merino
#=================================================

# 代表者になるのに必要な票
my $need_ceo_point = int($cs{member}[$m{country}] * 0.1)+2;

# 立候補に必要な費用
my $need_money = $config_test ? 0 : 50000;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ( $m{vote_year} && $w{year} ne $m{vote_year} && (abs($w{year} - $m{vote_year}) >= $reset_ceo_cycle_year || $w{year} % $reset_ceo_cycle_year <= $m{vote_year} % $reset_ceo_cycle_year) ) {
		$m{vote} = '';
		$m{vote_year} = $w{year};
	}

	if ($m{tp} > 1) {
		$mes .= "他に何か行いますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "$c_mの$e2j{ceo}を決定します<br>";
		$mes .= "$e2j{ceo}になるには最低でも$need_ceo_point票必要です<br>";
	}
	&menu('やめる', "$e2j{ceo}を選ぶ", '立候補する', '辞任する');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{'tp_' . $m{tp} };
}

#=================================================
# 支持・不支持の選択
#=================================================
sub tp_100 {
	if (!-s $this_file) {
		$mes .= '立候補者がいません<br>';
		$m{vote} = '';
		$m{vote_year} = $w{year};
		&begin;
		return;
	}
	
	my $sub_mes = '';
	my $is_find = 0; # 投票しているか
	my $is_find2 = 0; # 立候補しているか
	open my $fh, "< $this_file" or &error('国リーダーファイルが読み込めません');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		$is_find = 1 if $name eq $m{vote};
		$is_find2 = 1 if $name eq $m{name};
		$sub_mes .= qq|<input type="radio" name="vote" value="$name">$name：$vote票<br>|;
	}
	close $fh;
	
	$mes .= '誰を支持しますか?<br>';

	# 国データ上で立候補していないかつ個人データ上で立候補していた場合には立候補を取り消す
	if (!$is_find2 && $m{name} eq $m{vote}) {
		$m{vote} = '';
		$m{vote_year} = $w{year};
	}
	$mes .= qq|$m{vote} を支持しています<br>| if $is_find;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="vote" value="$m{vote}" checked>そのまま<br>| if $is_find;
	$mes .= qq|<input type="radio" name="vote" value="">支持しない<hr>|;
	$mes .= qq|$sub_mes|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="決 定" class="button1"></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($m{vote} eq $m{name}) {
		$mes .= '立候補者は投票できません<br>';
		&begin;
		return;
	}
	# そのまま
	elsif ($m{vote} eq $in{vote}) {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error('国リーダーファイルが開けません');
	eval { flock $fh, 2 };
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;

		$vote-- if $m{vote} eq $name && ($in{vote} eq '' || $in{vote} ne $m{vote}); # 誰かを支持中⇒他の人を支持 or 支持しない
		$vote++ if $name eq $in{vote}; # 支持

		push @lines, "$name<>$vote<>\n" if $vote > 0; # 0票は消える
	}
	# 票が多い順に並び替え
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# 一番票が多い人と今の代表が違う場合の処理
	my($top_name, $top_vote) =  split /<>/, $lines[0];
	if ($cs{ceo}[$m{country}] ne $top_name && $top_vote >= $need_ceo_point) {
		$cs{ceo}[$m{country}] = $top_name;
		&write_world_news("<b>$top_nameが$c_mの新しい$e2j{ceo}になりました</b>", 1, $top_name);
		if($cs{old_ceo}[$m{country}] eq $top_name && $cs{ceo_continue}[$m{country}] > 2){
			&regist_you_data($top_name,'shogo','★独裁者');
			&regist_you_data($top_name,'shogo_t','★独裁者');
		}
		
		# 他の代表になっていたら外す
		for my $k (qw/war pro dom mil/) {
			if ($cs{$k}[$m{country}] eq $top_name) {
				$cs{$k}[$m{country}] = '';
				$cs{$k.'_c'}[$m{country}] = 0;
			}
		}
		&write_cs;
	}
	# 君主がいる場合に、君主の得票数が代表に必要な票未満になった時
	elsif ($cs{ceo}[$m{country}] && $top_vote < $need_ceo_point) {
		$cs{ceo}[$m{country}] = '';
		&write_cs;
		&write_world_news("<b>$top_nameが$c_mの$e2j{ceo}からはずされました</b>");
	}
	
	$m{vote} = $in{vote};
	$m{vote_year} = $w{year};
	$mes .= $in{vote} ? "$m{vote}を支持します<br>" : '支持するのをやめました<br>';
	
	&begin;
}

#=================================================
# 立候補
#=================================================
sub tp_200 {
	$mes .= "$c_mの$e2j{ceo}に立候補しますか?<br>";
	$mes .= "立候補するには $need_money G必要です<br>";
	&menu('やめる','立候補する');
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1);
	
	my $is_find = 0; # 立候補しているか
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		$is_find = 1 if $name eq $m{name};
		push @lines, $line;
	}
	close $fh;

	if ($cs{old_ceo}[$m{country}] eq $m{name}) {
		$mes .= "貴方は$e2j{ceo}を$cs{ceo_continue}[$m{country}]回務めています<br>";
	}
	if ($is_find) {
		$mes .= 'すでに立候補者になっています<br>';
		&begin;
		return;
	}
	elsif ($m{money} < $need_money) {
		$mes .= '立候補するのにお金が足りません<br>';
		&begin;
		return;
	}
	elsif ($m{vote}) {
		$mes .= "立候補する場合は、$e2j{ceo}を選ぶで支持しないを選択してください<br>";
		&begin;
		return;
	}
	
	open my $fh, ">> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	print $fh "$m{name}<>1<>\n";
	close $fh;

	$mes .= "$e2j{ceo}に立候補しました<br>";
	&write_world_news("<b>$m{name}が$c_mの$e2j{ceo}に立候補しました</b>",1);
	$m{vote} = $m{name};
	$m{vote_year} = $w{year};
	$m{money} -= $need_money;

	&run_tutorial_quest('tutorial_ceo_1');
	&begin;
}

#=================================================
# 辞任
#=================================================
sub tp_300 {
	$mes .= "$c_mの$e2j{ceo}の立候補から辞任しますか?<br>";
	&menu('やめる','辞任する');
	$m{tp} += 10;
}
sub tp_310 {
	return if &is_ng_cmd(1);

	unless ($m{vote} eq $m{name}) {
		$mes .= '立候補者でないので辞任はできません<br>';
		&begin;
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_file" or &error('国リーダーファイルが開けません');
	eval { flock $fh, 2 };
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		next if $m{name} eq $name;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	$mes .= '立候補から辞任しました<br>';
	$m{vote} = '';
	$m{vote_year} = $w{year};

	# 代表者が辞任
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$cs{ceo}[$m{country}] = '';
		&mes_and_world_news("<b>$e2j{ceo}を辞任しました</b>",1);
		&write_cs;
	}
	
	&begin;
}

sub tp_400 {
	my %votes;
	my @names = &get_country_members($m{country});
	for my $name (@names) {
		$name =~ tr/\x0D\x0A//d;
		if($name eq $m{name}){
			$votes{"$m{vote}"}++;
			$mes .= "$name:$m{vote}<br>";
		}else{
			my %you_datas = &get_you_datas($name);
			$votes{"$you_datas{vote}"}++;
			$mes .= "$name:$you_datas{vote}<br>";
		}
	}
	
	my @lines = ();
	while (my ($name, $vote) = each %votes) {
		push @lines, "$name<>$vote<>\n" if $name; # 0票は消える
	}
	open my $fh, "+< $this_file" or &error('国リーダーファイルが開けません');
	eval { flock $fh, 2 };
	# 票が多い順に並び替え
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	&begin;
}

1; # 削除不可
