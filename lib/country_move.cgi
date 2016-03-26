require './lib/move_player.cgi';
#=================================================
# 仕官 Created by Merino
#=================================================

# 拘束時間
$GWT *= 2;

# 仕官するのに必要なﾚﾍﾞﾙ
my $need_lv = 1;

# 仕官するのに必要な金額
my $need_money = $m{sedai} > 100 ? $rank_sols[$m{rank}]+300000 : $rank_sols[$m{rank}]+$m{sedai}*3000;

# 世界情勢が暗黒の場合、NPC国へ仕官するのに必要な金額
my $need_money_npc = 1000000;

# 適当仕官の神様降臨確立(分の一)
my $random_god_par = 20;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]は仕官することができません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{lv} < $need_lv) {
		$mes .= "仕官するには $need_lv ﾚﾍﾞﾙ以上必要です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{random_migrate} eq $w{year}) {
		$mes .= "今年いっぱいは移籍できません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{country}) {
		$mes .= "仕官する手続きとして$GWT分かかります<br>";
		$mes .= "他の国に仕官すると代表\者ﾎﾟｲﾝﾄと階級が下がります<br>";
		$mes .= "同盟国に仕官する場合は階級が下がりません<br>" if $union;
		$mes .= "移籍料として $need_money G支払う必要があります<br>";
		
		# 暗黒
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]に仕官する場合は、次の年になるまで他の国に仕官することはできません<br>|;
			$mes .= qq|$cs{name}[$w{country}]に仕官する場合は、代表\ﾎﾟｲﾝﾄが 0 になり、$need_money_npc G支払う必要があります<br></font>|;
		}
		
		$mes .= 'どの国に仕官しますか?<br>';
		
		&menu('やめる', @countries, '放浪する');
	}
	else {
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]に仕官する場合は、次の年になるまで他の国に仕官することはできません<br>|;
			$mes .= qq|$cs{name}[$w{country}]に仕官する場合は、代表\ﾎﾟｲﾝﾄが 0 になり、$need_money_npc G支払う必要があります<br></font>|;
		}
		$mes .= 'どの国に仕官しますか?<br>';
		&menu('やめる', @countries, '適当');
	}
}

sub tp_1 {
	return if &is_ng_cmd(1 .. $w{country}+1);

	$m{tp} = 200;
	&{ 'tp_'.$m{tp} };
}

sub tp_200 {
	if (&is_ng_cmd(1 .. $w{country}+1)){
		&refresh;
		return;
	}
	if($cmd <= $w{country}){
		my $line = &get_countries_mes($cmd);
		my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
		$mes .= $country_rule;
	}
	$mes .= '<br>本当に仕官しますか？';
	$m{value} = $cmd;
	&menu('やめる','仕官');
	$m{tp} = 300;
}

sub tp_300 {
	if (&is_ng_cmd(1)){
		&refresh;
		&n_menu();
		$mes = 'やめました';
		return;
	}
	
	$cmd = $m{value};
	if (&is_ng_cmd(1 .. $w{country}+1)){
		&refresh;
		return;
	}
	
	if ($cmd eq $m{country}) {
		$mes .= "自国に仕官はできません<br>";
		&begin;
	}
	# 国→放浪
	elsif ($cmd == $w{country} + 1) {
	      	if($m{country}){
			# 立候補者
			if ($m{name} eq $m{vote}) {
			   $mes .= "$c_mの$e2j{ceo}の立候補を辞任する必要があります<br>";
			   &begin;
			   return;
			}
			# 暗黒
			if ($w{world} eq $#world_states) {
			   if ($m{country} eq $w{country}) {
				$mes .= "$cs{name}[$m{country}]から抜け出すことは許されません<br>";
				&begin;
				return;
			   }
			}
			# 混乱
			if($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5){
				     $mes .= "国を離れることはできません<br>";
				     &begin;
				     return;
			}
			&move_player($m{name}, $m{country}, 0);
			$m{country} = 0;
			$m{rank} = 0;
			$m{rank_exp} = 0;
		
			&mes_and_world_news("$c_mから立ち去り放浪の旅に出ました",1);
		
			# 代表ﾎﾟｲﾝﾄ0
			for my $k (qw/war dom mil pro/) {
			    $m{$k.'_c'} = 0;
			}

			$mes .= "次に行動できるのは$GWT分後です<br>";
			&refresh;
			&wait;
		}else {
			$cmd = int(rand($w{country}) + 1);
			# 暗黒
			if ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]から抜け出すことは許されません<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "悪魔と契約するには $need_money_npc G必要です<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
					$m{money} -= $need_money;
					$mes .= "移籍料として $need_money G支払いました<br>";
					$mes .= "階級が$ranks[$m{rank}]になりました<br>";
					$mes .= "移籍の手続きに$GWT分かかります<br>" ;
					&wait;
				}
			}
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
			if($w{world} eq $#world_states-2){
				$cmd = $w{country} - int(rand(2));
			}
			elsif($w{world} eq $#world_states-3){
				$cmd = $w{country} - int(rand(3));
			}
			&move_player($m{name}, $m{country}, $cmd);
			$m{next_salary} = $time + 3600 * $salary_hour;
			$m{country} = $cmd;
			$m{vote} = '';
			$m{random_migrate} = $w{year};
			&mes_and_world_news("適当に$cs{name}[$cmd]に仕官しました",1);
			if (rand($random_god_par) < 1) {
				require './lib/shopping_offertory_box.cgi';
				&get_god_item(5);
			}
			&refresh;
		}
	}
	elsif ($cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]は定員がいっぱいです<br>";
		&begin;
	}
	elsif($w{world} eq $#world_state-2){
		if($cmd eq $w{country} || $cmd eq $w{country}-1){
			$cmd2 = $cmd;
		}else{
			$mes .= "今はその国には仕官できません<br>";
			&begin;
		}
	}
	elsif (defined $cs{name}[$cmd]) { # 国が存在する
		# 国→他の国
		if ($m{country}) {
			# 君主
			if ($m{name} eq $cs{ceo}[$m{country}]) {
				$mes .= "$c_mの$e2j{ceo}を辞任する必要があります<br>";
				&begin;
				return;
			}
			elsif ($need_money > $m{money}) {
				$mes .= "移籍するには $need_money G必要です<br>";
				&begin;
				return;
			}
			# 暗黒
			elsif ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]から抜け出すことは許されません<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "悪魔と契約するには $need_money_npc G必要です<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
				}
			}
			# 混乱
			if($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5){
				$mes .= "国を裏切ることはできません<br>";
				&begin;
				return;
			}
		
			$m{money} -= $need_money;
			$cs{money}[$m{country}] += $need_money;
			$mes .= "移籍料として $need_money G支払いました<br>";
			
			unless ($union eq $cmd) {
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} = 1 if $m{rank} < 1;
				$mes .= "階級が$ranks[$m{rank}]になりました<br>";

				# 代表ﾎﾟｲﾝﾄ半分
				for my $k (qw/war dom mil pro/) {
					$m{$k.'_c'} = int($m{$k.'_c'} * 0.5);
				}
			}
			
			$mes .= "移籍の手続きに$GWT分かかります<br>" ;
			&wait;
		}
		# 無所属→国
		else {
			# 暗黒
			if ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]から抜け出すことは許されません<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "悪魔と契約するには $need_money_npc G必要です<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
					$m{money} -= $need_money;
					$mes .= "移籍料として $need_money G支払いました<br>";
					$mes .= "階級が$ranks[$m{rank}]になりました<br>";
					$mes .= "移籍の手続きに$GWT分かかります<br>" ;
					&wait;
				}
			}
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
		}

		if($w{world} eq $#world_states-2){
			$cmd = $w{country} - int(rand(2));
		}
		elsif($w{world} eq $#world_states-3){
			$cmd = $w{country} - int(rand(3));
		} elsif($w{world} eq $#world_states-1) {
			$cmd = int(rand($w{country}) + 1);
		}
		
		&move_player($m{name}, $m{country}, $cmd);
		$m{next_salary} = $time + 3600 * $salary_hour;
		$m{country} = $cmd;
		$m{vote} = '';
		
		&mes_and_world_news("$cs{name}[$cmd]に仕官しました",1);
		
		&refresh;
	}
	else {
		&begin;
	}
}

sub tp_100 {
	$mes .= '他国から勧誘を受けました<br>';
	$m{tp} += 10;
	&n_menu;
}

sub tp_110 {
	my @head_hunt;
	$mes .= 'どの勧誘を受けますか?<br>';
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($hname, $hcountry) = split /<>/, $line;
		push @head_hunt, $cs{name}[$hcountry];
	}
	close $fh;
	$m{tp} += 10;
	&menu('断る', @head_hunt);
}

sub tp_120 {
	my $i_c = 0;
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$i_c;
		if($i_c == $cmd){
			my($hname, $hcountry) = split /<>/, $line;
			if ($hcountry eq $m{country}) {
				$mes .= "自国に仕官はできません<br>";
				&begin;
			}
			elsif (defined $cs{name}[$hcountry]) { # 国が存在する
				if ($m{country}) {
					# 君主
					if ($m{name} eq $cs{ceo}[$m{country}]) {
						$mes .= "$c_mの$e2j{ceo}を辞任する必要があります<br>";
						&begin;
						return;
					}
					$cs{money}[$m{country}] += $need_money;
				}
				&move_player($m{name}, $m{country}, $hcountry);
				$m{country} = $hcountry;
				$m{vote} = '';
				&mes_and_world_news("$hnameの誘いで$cs{name}[$hcountry]に仕官しました",1);
			}
			else {
				&begin;
			}
			last;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;
	&refresh;
	&n_menu;
}


1; # 削除不可
