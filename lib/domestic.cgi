#=================================================
# 内政 Created by Merino
#=================================================

# 税率：下の70の数字を増やすと難易度が簡単に、減らすと難易度が難しくなるよ
sub tax { ($cs{tax}[$m{country}] + 70) * 0.01 };

# 小規模の時間
my $GWT_s = int($GWT * 0.6);

# 大規模の時間
my $GWT_b = int($GWT * 2);

# 超規模の時間
my $GWT_l = int($GWT * 4);

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		if ($m{act} >= 100) {
			$mes .= "休息をとります<br>次に行動できるのは $GWT分後です";
			$m{act} = 0;
			&refresh;
			&wait;
			return 0;
		}
		else {
			$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
			&refresh;
			&n_menu;
			return 0;
		}
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何か行いますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= '内政を行い自国の資源を増やします<br>どれを行いますか?<br>';
		if ($m{tutorial_switch}) {
			require './lib/tutorial.cgi';
			&show_tutorial_message('内政によって戦争をするのに必要な物資を貯めることができるよ！<br>農業・商業・徴兵のいずれかの熟練度が 50 になる度に報奨金が貰えるから、まずはそれを狙ってみよう');
		}
	}
	
	&menu('やめる','農業','商業','徴兵','長期内政');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	my @size = ('やめる', "小規模    ($GWT_s分)", "中規模    ($GWT分)", "大規模    ($GWT_b分)");

	if    ($cmd eq '1') { $mes .= "穀物を採取して国の$e2j{food}を増やします<br>"; }
	elsif ($cmd eq '2') { $mes .= "国民からお金を徴税をして$e2j{money}を増やします<br>"; }
	elsif ($cmd eq '3') { $mes .= "兵士を募集して国の$e2j{soldier}を増やします<br>※1人につき1G<br>"; }
	elsif ($cmd eq '4') { $mes .= "農業,商業,徴兵をまとめて行います<br>"; $GWT_s *= 3; $GWT_b *= 3; $GWT *= 3; $GWT_l *= 3; push @size, "超規模    ($GWT_l分)"; }

	$m{tp} = $cmd * 100;
	$mes .= 'どのくらい行いますか?<br>';

	&menu(@size);
}

#=================================================
# 内政
#=================================================
sub tp_100 { &exe1('穀物を採取します<br>') }
sub tp_200 { &exe1('お金を徴税します<br>') }
sub tp_300 { &exe1('兵士を雇用します<br>') }
sub tp_400 { &exe1('まとめて内政を行います<br>') }
sub exe1 {
	my $i = 1;
	if ($m{tp} == 400 && !&is_ng_cmd(1..4)) { # 長期内政
		unless ($m{nou_c} >= 5 && $m{sho_c} >= 5 && $m{hei_c} >= 5) {
			$mes .= "長期内政を行うには、農業,商業,徴兵の熟練度が5回以上でないとできません<br>";
			&begin;
			return;
		}
		$i = 3; # 内政 3 種
	}
	elsif (&is_ng_cmd(1..3)) {
		return;
	}

	$GWT =  $cmd eq '1' ? $GWT_s * $i
			: $cmd eq '3' ? $GWT_b * $i
			: $cmd eq '4' ? $GWT_l * $i
			:               $GWT   * $i
			;

	$m{tp} += 10;
	$m{turn} = $cmd;
	$mes .= "$_[0]結果は$GWT分後<br>";
	&before_action('icon_pet_exp', $GWT);
	&wait;
}

#=================================================
# 内政効果量ボーナス（x倍補正 一定数量ボーナスを付け足すならば位置に注意）
#=================================================
sub multi_bonus {
	my ($k, $v) = @_;

	# 内政官は内政力1.1倍
	$v *= 1.1 if $cs{dom}[$m{country}] eq $m{name};

	# 君主は内政力1.05倍、暴君時ならば1.2倍
	$v *= ( ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05 ) if $cs{ceo}[$m{country}] eq $m{name};

	# 国設定補正
	$v *= &get_modify('dom');

	# 種族補正
	$v = &seed_bonus($k, $v);
	$v = &seed_bonus('red_moon', $v);

	return $v;
}

#=================================================
# 農業結果
#=================================================
sub tp_110 {
	my $v = ($m{nou_c} + $m{mat}) * $m{turn} * 10;
	$v  = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '1') {
		$v *= 1.5; # 豊作
	}
	elsif ($cs{state}[$m{country}] eq '3') {
		$v *= 0.5; # 暴風
	}
	
	$v = &multi_bonus('nou', $v);
	$v = &use_pet('nou', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '28');
	$v = int($v);
	
	$cs{food}[$m{country}] += $v;
	$mes .= "穀物を $v 採取しました<br>";
	
	&c_up('nou_c') for (1..$m{turn});
	&write_yran('nou', $v, 1);
	
	return if $m{tp} eq '410';

	&after1;
	&after2;
}
#=================================================
# 商業結果
#=================================================
sub tp_210 {
	my $v = ($m{sho_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '2') {
		$v *= 1.5; # 景気
	}
	elsif ($cs{state}[$m{country}] eq '4') {
		$v *= 0.5; # 不況
	}
	
	$v = &multi_bonus('sho', $v);
	$v = &use_pet('sho', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '29');
	$v = int($v);

	$cs{money}[$m{country}] += $v;
	$mes .= "お金を $v 徴税しました<br>";

	&c_up('sho_c') for (1..$m{turn});
	&write_yran('sho', $v, 1);

	return if $m{tp} eq '410';

	&after1;
	&after2;
}
#=================================================
# 徴兵結果
#=================================================
sub tp_310 {
	my $v = ($m{hei_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '5') {
		$v *= 0.5; # 飢饉
	}
	
	$v = &multi_bonus('hei', $v);
	if ($v < $m{money}){
		$v = &use_pet('hei', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '30');
	}
	$v = int($v);

	$v = $m{money} if $v > $m{money};
	$v = 0 if 0 > $m{money};
	$m{money} -= $v;

	$cs{soldier}[$m{country}] += $v;
	$mes .= "兵士を $v 人雇用しました<br>";

	if (0 < $v && 0 < $m{money}){
		&c_up('hei_c') for (1..$m{turn});
		&write_yran('hei', $v, 1);
	}

	return if $m{tp} eq '410';

	&after1;
	# 徴兵はお金がかかるので、経験値と評価をちょっとﾌﾟﾗｽ
	$m{turn} += 2 if 0 < $v && 0 < $m{money};
	&after2;
}
#=================================================
# 長期内政結果
#=================================================
sub tp_410 {
	&tp_110;
	&tp_210;
	&tp_310;

	&after1;
	$m{turn} = 5 if $m{turn} eq '4';
	$m{turn} *= 4;
	&after2;
}

#=================================================
# 終了処理
#=================================================
sub after1 { # $m{turn} から拘束時間を割り出せる最後のタイミングで呼ばれる
	require './lib/_rampart.cgi'; # 城壁
	my $i = $m{tp} == 410 ? 3 : 1; # 内政 3 種：内政 1 種
	my $g = $m{turn} eq '1' ? $GWT_s * $i
			: $m{turn} eq '3' ? $GWT_b * $i
			: $m{turn} eq '4' ? $GWT_l * $i
			:                   $GWT   * $i
			;
	&gain_dom_barrier($g);
}
sub after2 {
	my $v = int( (rand(3)+4) * $m{turn} );
	$v = &use_pet('domestic', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '160');
	$m{exp} += $v;
	$m{rank_exp} += int( (rand($m{turn}) + $m{turn}) * 2);
	$m{egg_c} += int(rand(3)+3) if $m{egg};
	
	$mes .= "$m{name}に対する評価が上がりました<br>";
	$mes .= "$v の$e2j{exp}を手に入れました<br>";

	# 疲労回復
	$m{act} = 0;
	$mes .= '疲労が回復しました<br>';
	
	&special_money;

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('domestic');
	}
	
	&daihyo_c_up('dom_c'); # 代表熟練度
	&run_tutorial_quest('tutorial_dom_1');

	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# 功労金
#=================================================
sub special_money {
	return unless ($w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1'));
	my $v = int($m{rank} * 150 * $m{turn});
	$m{money} += $v;
	$mes .= "今までの功績が認められ $v Gの功労金があたえられた<br>";
}

1; # 削除不可
