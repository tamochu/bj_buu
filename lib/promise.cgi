my $u = &union($m{country}, $y{country});
#================================================
# 外交 Created by Merino
#================================================

# 滅亡時の輸送量上限
my $metsubou_transfer = 100000 + $cs{modify_pro}[$m{country}] * abs($cs{modify_pro}[$m{country}]) * 4000;

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
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
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
		$mes .= "他国と外交をします($GWT分)<br>何を行いますか?<br>";
	}
	
	my @menus = ('やめる','友好条約','停戦協定');
	
	if (&is_daihyo) {
		push @menus, '宣戦布告','協戦同盟','同盟破棄';
		push @menus, '食料輸送','資金提供','兵士派遣' if $union;
	}
	&menu(@menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..8);

	if    ($cmd eq '1') { $mes .= '友好条約を結び友好度を上げます<br>'; }
	elsif ($cmd eq '2') {
		if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
			$mes .= "世界情勢が$world_states[$w{world}]なので、停戦条約を結ぶことはできません<br>";
			$m{tp} = 2;
			&begin;
			return;
		}
		$mes .= '停戦条約を結び交戦状態を解除します<br>';
	}
	elsif ( &is_daihyo ) {
		if    ($cmd eq '3') { $mes .= '宣戦布告をし、交戦状態にします<br>'; }
		elsif ($cmd eq '4') { $mes .= '協戦同盟を結びます<br>'; }
		elsif ($cmd eq '5') { $mes .= '同盟を破棄します<br>'; }

		elsif ($cmd eq '6') { $mes .= "同盟国$cs{name}[$union]に自国の$e2j{food}を輸送します<br>"; }
		elsif ($cmd eq '7') { $mes .= "同盟国$cs{name}[$union]に自国の$e2j{money}を寄付します<br>"; }
		elsif ($cmd eq '8') { $mes .= "同盟国$cs{name}[$union]に自国の兵士を派遣します<br>"; }
	}
	else {
		$mes .= "そのｺﾏﾝﾄﾞは、国の代表\者しかできません<br>";
		$m{tp} = 2;
		&begin;
		return;
	}
	
	$m{tp} = $cmd * 100;
	
	if ($cmd >= 6) {
		$mes .= qq|どれくらい送りますか?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="value" value="0" class="text_box1" style="text-align: right">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="送る" class="button_s"></p></form>|;
		&n_menu;
	}
	else {
		$mes .= 'どの国に向かいますか?<br>';
		&menu('やめる', @countries);
	}
}


#=================================================
# 外交ｾｯﾄ
#=================================================
sub tp_100 { &exe1("友好条約を交渉しに") }
sub tp_200 { &exe1("停戦条約を交渉しに") }
sub tp_300 { &exe1("宣戦布告をしに") }
sub tp_400 { &exe1("同盟を交渉しに") }
sub tp_500 { &exe1("同盟を破棄しに") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{tp} >= 300 && !&is_daihyo) {
		$mes .= "そのｺﾏﾝﾄﾞは、国の代表\者しかできません<br>";
		&begin;
	}
	elsif ($m{country} eq $cmd) {
		$mes .= '自国は選べません<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd] > 1) {
		$mes .= '人のいない国とは交渉できません<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;

		$mes .= "$_[0]$cs{name}[$y{country}]に向かいました<br>";
		$mes .= "結果は$GWT分後です<br>";
		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
}


#=================================================
# 友好条約
#=================================================
sub tp_110 {
	# 各国設定
	$modify = &get_modify('pro');
	if ( rand($w{"f_$u"} * $modify) > 5 || rand(4 * $modify) > 1  ) {
		&mes_and_world_news("$c_yと友好条約を結びました");
		my $v = rand(5)+7;
		$v += 1 if $m{gai_c} > 500;
		$v += 1 if $m{gai_c} > 1000;
		$v += 1 if $m{gai_c} > 1400;
		$v += rand(3)+1 if $cs{pro}[$m{country}] eq $m{name};
		# 君主は友好条約+1、暴君時ならば+2～5
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$v += ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? int(rand(4)+2) : 1;
		}
#		$v += 1 if $cs{ceo}[$m{country}] eq $m{name};
		$v *= $modify;
		
		$w{"f_$u"} += int($v);
		$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
		&write_yran('pro', 1, 1);
		&success;
	}
	else {
		$mes .= "$c_yとの友好条約に失敗しました<br>";
		&failed;
	}
}
#=================================================
# 停戦
#=================================================
sub tp_210 {
	# 各国設定
	$modify = &get_modify('pro');
	if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
		$mes .= "世界情勢が$world_states[$w{world}]なので、停戦することができません<br>";
		&failed;
	}
	elsif ($w{"p_$u"} eq '2' && $modify > rand(1)) {
		&mes_and_world_news("<b>$c_yと停戦条約を結びました</b>");
		# 各国設定
		$w{"f_$u"} = int( (rand(20)+40) * $modify );
		$w{"p_$u"} = 0;
		&write_yran('stop', 1, 1);
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('cessation');
		}
		
		&success;
	}
	else {
		$mes .= "$c_yとの停戦条約に失敗しました<br>";
		&failed;
	}
}
#=================================================
# 宣戦布告
#=================================================
sub tp_310 {
	if ($w{"p_$u"} eq '1') {
		$mes .= "まず、$c_yとの同盟を破棄してください<br>";
		&failed;
	}
	elsif ($cs{is_die}[$m{country}]) {
		$mes .= "滅亡している国は、宣戦布告をすることができません<br>";
		&failed;
	}
	elsif ($cs{is_die}[$y{country}]) {
		$mes .= "滅亡している国に宣戦布告をすることはできません<br>";
		&failed;
	}
	else {
		&mes_and_world_news("<b>$c_yに宣戦布告をしました</b>");
		$w{"p_$u"} = 2;
		$w{"f_$u"} = int( rand(20) );
		&write_yran('dai', 1, 1);
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('declaration');
		}
		&success;
	}
}
#=================================================
# 同盟
#=================================================
sub tp_410 {
	if ( $w{world} eq '8'|| $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '8' || $w{world_sub} eq '13')) || $w{world} == $#world_states-5 || $w{world} == $#world_states-2 || $w{world} == $#world_states-3 ) {
		$mes .= "世界情勢が$world_states[$w{world}]なので、同盟することができません<br>";
		&failed;
	}
	elsif ( !$union && $w{"p_$u"} eq '0' && $w{"f_$u"} >= 80 && !&is_other_union($y{country}) && $cs{is_die}[$y{country}] < 2 ) {
		&mes_and_world_news("<b>$c_yと協戦同盟を結びました</b>");
		$w{"p_$u"} = 1;
		&write_yran('dai', 1, 1);
		&success;
	}
	else {
		$mes .= "$c_yとの同盟に失敗しました<br>";
		&failed;
	}
}
#=================================================
# 同盟破棄
#=================================================
sub tp_510 {
	if (($w{world} eq '6' || ($w{world} eq '19' && $w{world_sub} eq '6'))) {
		$mes .= "世界情勢が$world_states[$w{world}]なので、同盟を破棄することができません<br>";
		&failed;
	}
	elsif ( $union && $w{"p_$u"} eq '1') {
		&mes_and_world_news("<b>$c_yとの同盟を破棄しました</b>");
		$w{"p_$u"} = 0;
		&write_yran('dai', 1, 1);
		&success;
	}
	else {
		$mes .= "$c_yとは同盟を組んでいません<br>";
		&failed;
	}
}


#=================================================
# 同盟国に物資を提供
#=================================================
sub tp_600 { &exe2('food',    '食料') }
sub tp_700 { &exe2('money',   '資金') }
sub tp_800 { &exe2('soldier', '兵士') }
sub exe2 {
	if ($in{value} > 0 && $in{value} !~ /[^0-9]/) {
		if (!$union) {
			$mes .= '同盟してません<br>';
			&begin;
		}
		elsif ($cs{$_[0]}[$m{country}] <= $in{value}) {
			$mes .= "$c_mの$_[1]がなくなってしまいます<br>";
			&begin;
		}
		elsif ($in{value} < 10000) {
			$mes .= "物資の支援は最低でも 10000 以上にする必要があります<br>";
			&begin;
		}
		elsif ($cs{is_die}[$m{country}] && $in{value} > $metsubou_transfer) {
			$mes .= "現在その量の資源を輸送する国力がありません<br>";
			&begin;
		}
		else {
			$cs{$_[0]}[$m{country}] -= $in{value};
			&write_cs;
			
			$m{value} = $in{value};
	
			$m{tp} += 10;
			$y{country} = $union;

			&mes_and_send_news("同盟国の$cs{name}[$union]に$_[1]を $m{value} 送りました");
			$mes .= "$GWT分に到着する予\定です<br>";
			&before_action('icon_pet_exp', $GWT);
			&wait;
		}
	}
	else {
		$mes .= "やめました<br>";
		&begin;
	}
}
sub tp_610 { # 総兵糧
	if ($union) {
		$cs{food}[$union] += $m{value};
		&exe3('食料');
	}
	else {
		$mes .= "他の国と同盟を組んでいません<br>";
		&failed;
	}
}
sub tp_710 { # 国家予算
	if ($union) {
		$cs{money}[$union] += $m{value};
		&exe3('資金');
	}
	else {
		$mes .= "他の国と同盟を組んでいません<br>";
		&failed;
	}
}
sub tp_810 { # 兵士
	if ($union) {
		$cs{soldier}[$union] += $m{value};
		&exe3('兵士');
	}
	else {
		$mes .= "他の国と同盟を組んでいません<br>";
		&failed;
	}
}
sub exe3 {
	my $name = shift;

	# 各国設定
	$modify = &get_modify('pro');
	
	$w{"f_$u"} += int( (rand(10)+20) * $modify );
	$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
	&write_yran('dai', 1, 1);
	&write_cs;
	&write_send_news("$c_mの$m{name}の輸送部隊が同盟国の$cs{name}[$union]に到着し、$m{value} の$nameが無事に届けられました");
	$mes .= "輸送部隊が同盟国の$cs{name}[$union]に到着し、$m{value} の$nameが無事に届けられました<br>";
	&success;
}

#=================================================
# 成功
#=================================================
sub success {
	$m{act} += 1;
	&c_up('gai_c');
	
	my $v = int(rand(11)+10);
	$v = &use_pet('promise', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '31');
	
	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} += int(rand(6)+4);
	
	$mes .= "$m{name}に対する評価が上がりました<br>";
	$mes .= "$vの$e2j{exp}を手に入れました<br>";

	&daihyo_c_up('pro_c'); # 代表熟練度

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('promise');
	}

	&refresh;
	&n_menu;
	&write_cs;
}
#=================================================
# 失敗
#=================================================
sub failed {
	$m{act} += 1;

	my $v = int(rand(11)+5);
	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} -= int(rand(3)+2);
	
	$mes .= "交渉に失敗したため、$m{name}に対する評価が下がりました<br>";
	$mes .= "$v の$e2j{exp}を手に入れました<br>";
	
	&refresh;
	&n_menu;
}


#=================================================
# 他国と同盟をくんでいるか
#=================================================
sub is_other_union {
	my $country = shift;
	
	for my $i (1 .. $w{country}) {
		next if $country eq $i;
		my $c_c = &union($country, $i);
		return 1 if $w{ "p_$c_c" } eq '1';
	}
	return 0;
}




1; # 削除不可
