#=================================================
# 戦争出撃準備 Created by Merino
#=================================================

# 拘束時間
$GWT = int($GWT * 1.5);

my @needs = (0.5, 1.0, 2.0); #通常部隊
if ($m{unit} eq '16') { # 軽装部隊 消費物資0.75倍
	$needs[$_] = $needs[$_] * 0.75 for (0 .. $#needs);
}
elsif ($m{unit} eq '18') { # 狡知部隊 消費物資1.5倍
	$needs[$_] = $needs[$_] * 1.5 for (0 .. $#needs);
}
if ($m{pet} eq '193') { $needs[$_] = $needs[$_] * 0.5 for (0 .. $#needs); } # ﾀﾞｰｸﾗﾋﾞｯﾄ 消費物資0.5倍


# 進軍種類
my @war_marchs = (
#	[0]名前,[1]進軍時間兵士の倍率,[2]経費の倍率,[3]必要条件
	['少数精鋭',	0.5,	$needs[0],	sub{ $pets[$m{pet}][2] ne 'speed_down' }],
	['通常戦争',	1.0,	$needs[1],	sub{ $m{win_c} >= 1  }],
	['長期遠征',	1.5,	$needs[2],	sub{ $m{unit} ne '11' && $m{win_c} >= 10 && $m{win_c} > $m{lose_c} }]
);
if($m{value} < 0 || $m{value} >= @war_marchs){$m{value} = $#war_marchs;}
my $need_costs = $rank_sols[$m{rank}] * $war_marchs[$m{value}][2];

#=================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= '終戦期間中は戦争と軍事はできません<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ( $cs{is_die}[$m{country}] && ($w{world} eq '9' || $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13'))) ) {
		$mes .= "世界情勢が$world_states[$w{world}]で、自国が滅亡しているので戦争することはできません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$m{tp} = 1;
		$mes .= 'どのように攻め込みますか?<hr>';
	}
	else {
		$mes .= "他国へ攻め込み$e2j{strong}を奪います<br>";
		$mes .= "どのように攻め込みますか?<hr>";
	}

	my @menus = ('やめる');
	for my $war_march (@war_marchs) {
		if (&{ $war_march->[3] }) {
			my $need_fm  = $rank_sols[$m{rank}] * $war_march->[2];
			my $need_GWT = &_unit_march($GWT * $war_march->[1]);
			# ちょっと強引 _unit_march() の内部で $m{value} を参照するので未代入の begin 呼び出し時に意図しない数値が返る
			# 長期進軍より長い拘束時間の進軍方法が実装された場合に、また表示と内部の拘束時間のズレが生じそう
			$need_GWT = 20 if $war_march->[1] > 1 && $need_GWT < 20;
			$mes .= "$war_march->[0] [消費兵糧：$need_fm 消費予\算：$need_fm 時間：$need_GWT分]<br>";
			push @menus, $war_march->[0];
		}
		else {
			push @menus, '';
		}
	}

	&menu(@menus);
}

#================================================
# 国選択
#================================================
sub tp_1 {
	return if &is_ng_cmd(1..$#war_marchs+1);
	--$cmd;

	# 暗殺部隊は長期遠征禁止
	if ($m{unit} eq '11' && $cmd eq '2') {
		$mes .= "$units[$m{unit}][1]は$war_marchs[$cmd][0]で進軍することができません<br>";
		&begin;
	}
	elsif (!&{$war_marchs[$cmd][3]}) {
		$mes .= "$war_marchs[$cmd][0]で進軍する条件を満たしていません<br>";
		&begin;
	}
	elsif (defined $war_marchs[$cmd]) {
		$m{value} = $cmd;
		$mes .= "$war_marchs[$cmd][0]で進軍します<br>";
		$mes .= 'どの国に攻め込みますか?<br>';
		
		&menu('やめる', @countries);
		$m{tp} = 100;
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#================================================
# 戦争ｾｯﾄ
#================================================
sub tp_100 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{country} eq $cmd) {
		$mes .= '自国は選べません<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '滅んでいる国は攻め込めません<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '同盟国に攻め込むことはできません<br>';
		&begin;
	}
	elsif ($need_costs > $cs{food}[$m{country}]) {
		$mes .= "進軍するのに必要な$e2j{food}が足りません<br>";
		&begin;
	}
	elsif ($need_costs > $cs{money}[$m{country}]) {
		$mes .= "進軍するのに必要な$e2j{money}が足りません<br>";
		&begin;
	}
	elsif ($rank_sols[$m{rank}] * $war_marchs[$m{value}][1] > $cs{soldier}[$m{country}]) {
		$mes .= "$e2j{soldier}が足りません<br>自国を守る兵士がいなくなってしまいます<br>";
		&begin;
	}
	# 進軍
	elsif ($cmd && defined $war_marchs[$m{value}]) {
		$m{lib} = 'war';
		$m{tp}  = 100;
		$y{country} = $cmd;
		
		# 世界情勢「迷走」
		if (($w{world} eq '15' || ($w{world} eq '19' && $w{world_sub} eq '15'))) {
			$y{country} = int(rand($w{country}))+1;
			if ($cs{is_die}[&get_most_strong_country]){
				my $loop = 0;
				while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
					if($loop > 30) {
						$y{country} = &get_most_strong_country;
					}
					$y{country} = int(rand($w{country}))+1;
					$loop++;
				}
			}else {
				$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
			}
		} elsif ($w{world} eq $#world_states - 5) {
			$y{country} = int(rand($w{country}))+1;
			my $loop = 0;
			while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
				if($loop > 30) {
					$y{country} = &get_most_strong_country;
				}
				$y{country} = int(rand($w{country}))+1;
				$loop++;
			}
		}
		
		my $v = int( $rank_sols[$m{rank}] * $war_marchs[$m{value}][1] );

		$cs{soldier}[$m{country}] -= $v;
		$cs{food}[$m{country}]    -= int($need_costs);
		$cs{money}[$m{country}]   -= int($need_costs);
		
		$m{sol} = int( $v + int($m{cha} * 0.005) * 500 ); # cha200超えごとに+500
		$m{sol} += 500 if($m{cha} == 999); # cha999で+500
		$m{value} = $war_marchs[$m{value}][1];

		$GWT = &_unit_march($GWT * $m{value});

		$mes .= "$vの兵を率いて$cs{name}[$y{country}]に進軍を開始します<br>";
		$mes .= "$GWT分後に到着する予\定です<br>";

		if ($y{country} eq $m{renzoku}) {
			++$m{renzoku_c};
		}
		else {
			$m{renzoku} = $y{country};
			$m{renzoku_c} = 1;
		}

		&before_action('icon_pet_exp', $GWT);
		&wait;
		&write_cs;
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#================================================
# 部隊により進軍時間の増減(極端に長すぎ・短すぎはｹﾞｰﾑﾊﾞﾗﾝｽ崩壊するので時間制限)
#================================================
sub _unit_march {
	my $need_GWT = shift;
	# 重兵。最高進軍時間90分
	if ($m{unit} eq '1' && ($pets[$m{pet}][2] ne 'speed_up' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && $need_GWT * 1.5 < 90) {
		$need_GWT = $need_GWT * 1.5;
	}
	# 天馬,飛竜。最低進軍時間20分
	elsif ( ($m{unit} eq '7' || $m{unit} eq '8' || ($pets[$m{pet}][2] eq 'speed_up' && $w{world} ne '17')) && $need_GWT * 0.5 > 20 && $m{unit} ne '18') {
		$need_GWT = $need_GWT * 0.5;
	}

	if ($pets[$m{pet}][2] eq 'speed_down' && $w{world} ne '17') {
		$need_GWT *= $m{unit} eq '7' || $m{unit} eq '8' ? 4 : 2;
		$m{value} *= 3 unless $m{unit} eq '18';
	}
	elsif ($m{pet} eq '193' && $w{world} ne '7'
#	&& $w{world} ne $#world_states	
	) {
		$need_GWT -= 10;
		$need_GWT = 20 if $m{value} > 1 && $need_GWT < 20;
	}
	return int($need_GWT);
}


1; # 削除不可
