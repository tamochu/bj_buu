use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_rampart.cgi'; # 城壁
#=================================================
# 戦争結果 Created by Merino
#=================================================
# war.cgiにあってもいいけどごちゃごちゃになりそうなので分離

# 救出人数
my $max_rescue = 1;

# m{value} は兵士の倍率や奪国力の補正など取り回されていてややこしい上に、進軍種類を楽に求められないので不便
# 進軍種類さえ問えればそれらも求められるので根本的に仕様変更したい
# m{value} を進軍種類と再定義し、0, 1, 2 といった風に しかしコードの変更箇所が多いので諦める（特にﾀﾞｰﾄﾙの進軍時周りの書き直しがネックか）
# ﾀﾞｰﾄﾙは進軍時に情勢を見て補正を掛けているので着弾時の情勢は無関係、$m{value} が * 3 されているかが重要 進軍種類が追加されるとバグりそう
my $war_form = ($pets[$m{pet}][2] eq 'speed_down' && $m{unit} ne '18' && $m{value} >= 3) ? $m{value} / 3 : $m{value};
$war_form = ($war_form == 1.5) ? 2 : int($war_form); # 進軍種類 少数：0 通常：1 長期：2

#=================================================
# 引き分け
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "$m{name}に対する評価が下がりました<br>";
	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	
	my $is_rewrite = 0;
	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
#	if ($y{sol} > 0) {
#		$cs{soldier}[$y{country}] += int($y{sol} / 3);
#		$is_rewrite = 1;
#	}

	# 城壁データ±
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# 負け
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "部隊全滅という不名誉な敗北の為、$m{name}に対する評価が著しく下がりました<br>";
	$mes .= "$vの$e2j{exp}を手に入れました<br>";

	if($m{master_c} eq 'lose_c'){
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(21)+50) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "しかし殿役を立派に務めた為、$m{name}に対する評価が上がりました<br>";
		$mes .= "さらに$vの$e2j{exp}を手に入れました<br>";
	}
	
#	$cs{soldier}[$y{country}] += int($y{sol} / 3) if $y{sol} > 0;

	# 城壁データ±
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	&down_friendship;

	# 連続で同じ国だと高確率でﾀｲｰﾎ
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( ( ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 ) || ( ($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2  || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		my $mname = &name_link($m{name});
		&write_world_news("$c_mの$mnameが$c_yの牢獄に幽閉されました");
		&add_prisoner;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# 退却
#=================================================
sub war_escape {
	$mes .= "$m{name}に対する評価が下がりました<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );
	&write_yran('war', 1, 1);

	$cs{soldier}[$m{country}] += $m{sol};
#	$cs{soldier}[$y{country}] += int($y{sol} / 3);

	# 城壁データ±
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# 勝ち
#=================================================
sub war_win {
	my $is_single = shift;


	# 奪国力ﾍﾞｰｽ:階級が高いほどﾌﾟﾗｽ。下克上、革命の時は階級が低いほどﾌﾟﾗｽ
	my $v = ($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2')) ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# 定員が少ない分ﾌﾟﾗｽ多い分ﾏｲﾅｽ
#	if ($m{country}) {
#		$mem = &modified_member($m{country});
#	} else {
#		$mem = 0;
#	}
#	$v += ($cs{capacity}[$m{country}] - $mem) * 10 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 5 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));


	# 国情勢により奪国力増加
	if (($w{world} eq '4' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '4' || $w{world_sub} eq '5')))) { # 暴君、混沌
		$v *= 2.5;
	}
	elsif (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # 革命:弱国有利
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
		if ($m{sedai} < 5) {
			$v *= 3;
		}
		elsif ($m{sedai} < 10) {
			$v *= 2.5;
		}
	}
	elsif (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) { # 白兵
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
			$v *= 1.2;	
	}
	else {
		$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
	}
	
	# 交戦中なら2倍
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	# 各国設定
	$v *= &get_modify('war');

	# 城壁補正
	my ($r_v, $r_vv) = &get_rampart_modify($y{country}); # 城壁による奪国力と奪国上限の補正が返る
	$v *= $r_v;

	# 参謀は奪国力1.1倍
	if ($cs{war}[$m{country}] eq $m{name}) {
		$v = int($v * 1.1) ;
	}
	# 君主は奪国力1.05倍、暴君時ならば1.2倍
	elsif ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$v = int($v * $ceo_value);
	}
#	#代表ボーナス
#	$v = int($v * 1.1) if $cs{war}[$m{country}] eq $m{name};    
#	$v = int($v * 1.05) if $cs{ceo}[$m{country}] eq $m{name};

	# 獣化
	$v = &seed_bonus('red_moon', $v);
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &seed_bonus('war_win', $v);

	if ($m{pet} eq '193') { # ﾀﾞｰﾗﾋﾞ時、階級補正と世代補正に進軍補正
		$v = 0;
		if (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # 革命:弱国有利
			$v = (@ranks - $m{rank}) * 10 + 10; # 階級補正
			if ($m{sedai} < 5) { # 革命児世代補正
				$v *= 3;
			}
			elsif ($m{sedai} < 10) { # 革命児世代補正
				$v *= 2.5;
			}
		}
		else {
			$v = $m{rank} * 8 + 10; # 階級補正
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10; # 世代補正
		}
		$v *= $m{value}; # 進軍補正
	}

	if($m{unit} eq '18'){
		$v = $v * 1.5;
		$v = &use_pet('war_result', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) || $m{pet} eq '12');
	}
	elsif ($m{unit} eq '7' || $m{unit} eq '8') {
		$v = &use_pet('war_result', $v) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17') || ($m{pet} eq '12' && ($time + 2 * 24 * 3600 < $w{limit_time})) );
	}
	else{
		$v = &use_pet('war_result', $v) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	}
	
	if ($cs{extra}[$m{country}] eq '1' && $cs{extra_limit}[$m{country}] >= $time) {
		$v = 999;
	}
	
	if ($w{world} eq $#world_states - 5) {
		$v = int($v / 10);
	}
	

	# 奪国力上限
	if ($v !~ /^(\d)\1+$/) { # ｿﾞﾛ目(ｳﾛﾎﾞﾛｽ使用時など)
		if ($m{value} < 1) { # 少数精鋭
#			$v = $v > 200 ? int(rand(50)+150) : int($v);
			$v = $v > 200 ? int(rand(80)+120) : int($v);
		}
		else { # 通常・長期
			if($m{unit} eq '18'){
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # 統一期限残り１日
					$v = $v > (2000 + $r_vv) ? int(rand(500+($r_vv*0.5))+1500+($r_vv*0.5)) : int($v);
				}
				else {
					$v = $v > (1500 + $r_vv) ? int(rand(500+($r_vv*0.5))+1000+($r_vv*0.5)) : int($v);
#					$v = $v > 1500  ? int(rand(200)+1300) : int($v);
				}
			}else{
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # 統一期限残り１日
					$v = $v > (1500 + $r_vv) ? int(rand(500+($r_vv*0.5))+1000+($r_vv*0.5)) : int($v);
#					$v = $v > 1500 ? int(rand(250)+1250) : int($v);
				}
				else {
#					$v = $v > 600  ? int(rand(200)+400) : int($v);
					$v = $v > (800 + $r_vv)  ? int(rand(200+($r_vv*0.5))+600+($r_vv*0.5)) : int($v);
				}
			}
			# 統一期限が近づいてきたらﾌﾟﾗｽ
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# 滅亡国の場合罰則
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty;
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	if ($cs{disaster}[$y{country}] eq 'paper' && $cs{disaster_limit}[$y{country}] >= $time) {
		$v += 100;
	}
	# 国力データ±
	$cs{strong}[$m{country}] += ($w{world} eq '13' || $w{world} eq $#world_states - 2 || $w{world} eq $#world_states - 3) ? int($v * 0.75):$v;
	$cs{strong}[$y{country}] -= $v unless ($w{world} eq $#world_states - 5);
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	&write_yran(
		'strong', $v, 1,
		"strong_$y{country}", $v, 1,
		'win', 1, 1,
		'war', 1, 1
	);
#	&write_yran('strong', $v, 1);
#	&write_yran("strong_$y{country}", $v, 1);
#	&write_yran('win', 1, 1);
#	&write_yran('war', 1, 1);
	
	if ($w{world} eq $#world_states - 5) {
		$mes .= "$vの$e2j{strong}を得ました<br>";
	} else {
		$mes .= "$c_yから$vの$e2j{strong}を奪いました<br>";
	}
	
	my $mname = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$mname = '名無し';
	}
	if ($w{world} eq $#world_states - 5) {
		&write_world_news(qq|$c_mの$mnameが<font color="#FF00FF"><b>$v</b> の$e2j{strong}を得る事に成功</font>したようです|);
	} else {
		if ($is_single) {
			&write_world_news(qq|$c_mの$mnameが$c_yに侵攻、$y{name}と一騎討ちの末これを下し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪う事に成功</font>したようです|);
		}
		else {
			$m{value} < 1
				? &write_world_news(qq|何者かが$c_yに侵攻、$y{name}の部隊を撃破し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪うことに成功</font>したようです|)
				: &write_world_news(qq|$c_mの$mnameが$c_yに侵攻、$y{name}の部隊を撃破し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪うことに成功</font>したようです|)
				;
		}
	}

	# 城壁データ±
	&change_barrier($y{country}, -$units[$m{unit}][7][$war_form]);

	&after_success_action('war', $is_single);

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}に対する評価が大きく上がりました<br>";
	$mes .= "$vvの$e2j{exp}を手に入れました<br>";

	if($m{master_c} eq 'win_c'){
		++$m{medal};
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(11)+20) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "その功績を大きく喧伝した為、$m{name}に対する評価がさらに上がりました<br>";
		$mes .= "さらに$vの$e2j{exp}を手に入れました<br>";
	}
	# ﾚｽｷｭｰ
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>1<>\n";
		close $fh;
	}

	&refresh;

	&daihyo_c_up('war_c'); # 代表熟練度

	# 暗黒
	if ($w{world} eq $#world_states) {
		my @acs = (1..$w{country} - 1);
		my $dark_side = $m{country} eq $w{country} ? $union : ($union eq $w{country} ? $m{country} : 0) ; # 暗黒の同盟国は封印側として数えない
		splice(@acs, $dark_side - 1, 1) if $dark_side;
		# ｱﾎｱﾘｱ自体は暗黒の同盟国が暗黒を滅ぼすと同盟国を経由して暗黒に統一フラグが立ち暗黒勝利になる現象
		my $ahoalia = 1;
		for my $ac (@acs) {
			$ahoalia = 0 if !$cs{is_die}[$ac]; # 封印側が滅亡してないなら封印側全国滅亡フラグ下ろす
		}
		if ($cs{strong}[$m{country}] >= $touitu_strong
			|| ($cs{strong}[$w{country}] <= 0
				&& $union ne $w{country}) # こっちがｱﾎｱﾘｱ対策
			|| ($ahoalia && $m{country} eq $w{country})) { # こっちは封印側がすべて滅亡しているか
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
=pod
		無改造の暗黒ｶｳﾝﾀｰ
		elsif ( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			require './lib/vs_npc.cgi';
			&npc_war;
		}
		暗黒の国力が 30000 以上の時は 1/4 でｶｳﾝﾀｰ発生
		暗黒の国力が 30000 未満なら 1/3 かと思ってたけどよく考えたら加算なので (1/4) + (1/3) - (1/4*1/3) = 0.5 で無改造の最高ｶｳﾝﾀｰ率は 50%
		※確率の加法定理 Aが生じる確率 + Bが生じる確率 - (AとBが生じる確率)
=cut
		else {
			# 統一期限や暗黒の国力を終盤判定の要素としてｶｳﾝﾀｰ率うｐ調節
			# 国数の増減は本来暗黒の強弱とは関係ないと思われる
			# 暗黒が、3国に殴られようが5国に殴られようが10国に殴られようが封印側の国数に関係なく総戦争数は同一
			# 布告してくる国数が増えるほど暗黒不利になるとは思うが、奪国ｶｳﾝﾀｰの奪国力を上げれば布告されていようが暗黒有利にすることは可能
			# 無改造はそもそも布告されてる前提の奪国力で反撃するので布告してくる国数増えても暗黒の強弱には関係ないはず
			# 黒豚鯖は布告で封印側の奪国力が一方的に上がるようになってるので布告してくる国が増えるほど暗黒が不利になる→国数によって暗黒の強弱が変わってしまうのが黒豚鯖の仕様
			# 結論、国数による暗黒の強弱の変化は封印側の奪国力と暗黒の奪国力の差が出てしまうことによるので、暗黒の強弱のバランス調整するならカウンター率よりも奪国力を調整した方が良い
			# ここでのｶｳﾝﾀｰ調整は拘束が長い＆鯖人員が少ない鯖だと暗黒が活発になる前に統一期限が切れそうになるの対策
			# 鯖人員が増えたらたぶん要らない調整
			my $npc_par = $cs{strong}[$w{country}] < 30000 ? 1 : 0;# 国力30000未満 = 2/4 = 50%
#			    : $time + 2 * 24 * 3600 > $w{limit_time} ? 0.2 # 国力30000以上 + 統一期限残り1日 = 1.2/4 = 30%
#			    : $time + 3 * 24 * 3600 > $w{limit_time} ? 0.15 # 国力30000以上 + 統一期限残り2日 = 1.15/4 = 28.7%
#			    : $time + 4 * 24 * 3600 > $w{limit_time} ? 0.1 # 国力30000以上 + 統一期限残り3日 = 1.1/4 = 27.5%
#			    : $time + 5 * 24 * 3600 > $w{limit_time} ? 0.05 # 国力30000以上 + 統一期限残り4日 = 1.05/4 = 26.2%
#			    :                                          0 # 国力30000以上 + 統一期限5日以上 = 1/4 = 25%
#			    ;

			require './lib/vs_npc.cgi';
#			if( rand(4) < $npc_war  || ($cs{strong}[$w{country}] < 30000 && rand(3) < $npc_war) ) {
			if( rand(4) < (1 + $npc_par) ) { # 確率の加法定理使ってｶｳﾝﾀｰ率計算するの面倒なので人間が分かりやすいように省略
			    &npc_war;
			}
		}
	}
	# 終焉
	elsif (($w{world} eq '13' || ($w{world} eq '19' && $w{world_sub} eq '13'))) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
	}
	# 不倶戴天
	elsif ($w{world} eq $#world_states - 2) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_touitu;
		}
	}
	# 三国志
	elsif ($w{world} eq $#world_states - 3) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
			$cs{strong}[$m{country}] += 3000;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
	}
	# 拙速
	elsif ($w{world} eq $#world_states - 5) {
		my $cou = 0;
		my $max_value = 0;
		for my $i (1 .. $w{country}) {
			if ($cs{strong}[$i] > $max_value) {
				$cou = $i;
				$max_value = $cs{strong}[$i];
			}
		}
		$strongest_country = $cou;
		if ($y{country} eq $strongest_country) {
			if (rand(3) < 1) {
				my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 10  );
				&write_world_news("<b>ﾘｳﾞｧｲｱｻﾝの大嵐！$cs{name}[$m{country}]は$cs{name}[$y{country}]の$e2j{$kkk}を $vvv 奪いました</b>");
			}
		} else {
			if (rand(3) < 1) {
				my $type = int(rand(12));
				if ($type == 0) {
					for my $i (1..$w{country}) {
						next if $i eq $m{country};
						$cs{strong}[$i] -= int(rand(40)+40);
					}
					&write_world_news("<b>各国の$e2j{strong}が下がりました</b>");
				} elsif ($type <= 10) {
					if (rand(3) < 1) {
						$cs{food}[$m{country}] += 100000;
						&write_world_news("$c_mの$e2j{food}が100000増加しました");
					} elsif (rand(2) < 1) {
						$cs{money}[$m{country}] += 100000;
						&write_world_news("$c_mの$e2j{money}が100000増加しました");
					} else {
						$cs{soldier}[$m{country}] += 50000;
						&write_world_news("$c_mの$e2j{soldier}が50000増加しました");
					}
				} else {
					for my $i (1..$w{country}) {
						for my $j ($i+1..$w{country}) {
							$w{"f_${i}_${j}"}=int(rand(20));
							$w{"p_${i}_${j}"}=2;
						}
					}
					&write_world_news("<b>世界中が開戦となりました</b>");
				}
			}
		}
	}
	# 統一
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# 滅亡
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# 復興
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '9' || ($w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13')))) ) {
		&_hukkou;
	}
	# 鉄壁
	elsif (($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>ﾘｳﾞｧｲｱｻﾝの大嵐！$cs{name}[$m{country}]は$cs{name}[$y{country}]の$e2j{$kkk}を $vvv 奪いました</b>");
	}
	if($w{world} eq '19'){# 謎
		if($w{sub_time} < $time){
			$w{world_sub} = int(rand(@world_states-4));
			$w{sub_time} = $time + 6 * 3600;
		}
	}
	

	&write_cs;

	&n_menu;
}

#=================================================
# 牢獄に仲間がいるなら救出
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	my @y_names = ();
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi が開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country,$flag) = split /<>/, $line;
		if ($flag == 0 && $count < $max_rescue && ($country eq $m{country} || $union eq $country) && $country ne '0' ) {
			$is_rescue = 1;
			push @y_names, $name;
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	# ↑でまずﾌｧｲﾙﾊﾝﾄﾞﾙ閉じてから諸々の処理
	if ($is_rescue) {
		&write_yran('res', $count, 1);
		my $mname = $m{name};
		$mname = '名無し' if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16'));
		for my $i (1 .. $count) {
			my $name = $y_names[$i-1];
			$mes .= "$c_yに捕らえられていた$nameを救出しました<br>";
			&write_world_news("$c_mの$mnameが$c_yに捕らえられていた$nameの救出に成功しました");
		
			# ﾚｽｷｭｰﾌﾗｸﾞ作成
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgiﾌｧｲﾙが作れません");
				close $fh2;
			}

			&c_up('res_c');
			&use_pet('rescue');

			if ($w{world} eq $#world_states-4) {
				require './lib/fate.cgi';
				&super_attack('rescue');
			}
		}
	}
}

#=================================================
# 統一
#=================================================
sub _touitu {
	# すげー気持ち悪い多重統一処理防止
	# 同年同情勢同一キャラによる統一がされてたらとりあえず情勢選択へ移行
	open my $fh, "< $logdir/legend/touitu.cgi" or &error("$logdir/legend/touitu.cgi ﾌｧｲﾙが開けません");
	my $line = <$fh>;
	close $fh;
	if ($line =~ /$world_name暦$w{year}年【$world_states[$w{world}]】.*$m{name}.*/) {
		$m{lib} = 'world';
		$m{tp}  = 100;
		return;
	}

	&c_up('hero_c');
#	&debug_log(\%w, 'touitsu_w');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];

	my $mname = &name_link($m{name});
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC国側の勝利
			&mes_and_world_news("<em>悪魔達の率先者として$world_name大陸を支配することに成功しました</em>",1);
			&write_legend('touitu', "深き闇より目覚めた$cs{name}[$w{country}]の猛者達が$mnameを筆頭とし$world_name大陸を支配する");
			&send_twitter("深き闇より目覚めた$cs{name}[$w{country}]の猛者達が$m{name}を筆頭とし$world_name大陸を支配する");
			$is_npc_win = 1;
		}
		else { # 封印国側の勝利
			&mes_and_world_news("<em>魔界を再び封印し、$world_name大陸にひとときの安らぎがおとずれました</em>",1);
			&write_legend('touitu', "$c_mの$mnameとその仲間達が魔界を再び封印し、$world_name大陸にひとときの安らぎがおとずれる");
			&send_twitter("$c_mの$m{name}とその仲間達が魔界を再び封印し、$world_name大陸にひとときの安らぎがおとずれる");

			require './lib/shopping_offertory_box.cgi';
			my %sames = ();
			for my $wc (@win_countries) {
				open my $cfh, "< $logdir/$wc/member.cgi" or &error("$logdir/$wc/member.cgiﾌｧｲﾙが開けません");
				while (my $player = <$cfh>) {
					$player =~ tr/\x0D\x0A//d;
					next if ++$sames{$player} > 1;
					&send_item($player, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
				close $cfh;
			}
		}
	}
	elsif ($w{world} eq $#world_states-2) {
		&mes_and_world_news("<em>$world_name大陸を二分する戦いは$c_mの$mnameとその仲間達の勝利に終わった</em>",1);
		&write_legend('touitu', "$c_mの$mnameが$world_name大陸を統一する");
		&send_twitter("$c_mの$m{name}が$world_name大陸を統一する");
		$w{win_countries} = $m{country};
	}
	elsif ($w{world} eq $#world_states-3) {
		&mes_and_world_news("<em>$world_name大陸を三分する戦いは$c_mの$mnameとその仲間達の勝利に終わった</em>",1);
		&write_legend('touitu', "$c_mの$mnameが$world_name大陸を統一する");
		&send_twitter("$c_mの$m{name}が$world_name大陸を統一する");
		$w{win_countries} = $m{country};
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name大陸を統一しました</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]同盟の$mnameが$world_name大陸を統一しました</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]同盟の$mnameが$world_name大陸を統一する");
			&send_twitter("$c_m$cs{name}[$union]同盟の$m{name}が$world_name大陸を統一する");
		}
		else {
			&mes_and_world_news("<em>$world_name大陸を統一しました</em>",1);
			&write_legend('touitu', "$c_mの$mnameが$world_name大陸を統一する");
			&send_twitter("$c_mの$m{name}が$world_name大陸を統一する");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
}

#=================================================
# 復興
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_mを復興させることに成功しました</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# 滅亡
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	$w{world_sub} = int(rand(@world_states-4));
	&mes_and_world_news("<b>$c_yを滅ぼしました</b>", 1);

	# 物資Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# 国状態変化
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# 滅亡国から国力を奪取した時の罰則
#=================================================
sub _penalty {
	# 災害
	if ( (($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12')) && rand(3) < 1) || rand(12) < 1 ) {
		&disaster( $w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12') ); # 厄年 or 謎(厄年)のみ追加ﾍﾟﾅﾙﾃｨ
	}
}

#=================================================
# 友好度Down
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	$w{'f_'.$c_c} -= ($m{pet_c} - 10) if ($m{pet} eq '193' && $m{pet_c} > 10);
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10 && $y{country} ne $union) {
		$w{'p_'.$c_c} = 2;
		my $mname = &name_link($m{name});
		&write_world_news("<b>$c_mの$mnameの進軍により$c_yと交戦状態になりました</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}

#=================================================
# 修正後所属人数
#=================================================
sub modified_member {
	my $i = shift;
	return $cs{member}[$i] - $cs{new_commer}[$i];
}


1; # 削除不可
