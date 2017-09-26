require "$datadir/skill.cgi";
require "$datadir/pet.cgi";
#=================================================
# ｽﾃｰﾀｽ画面 Created by Merino
#=================================================

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['やめる',		'main'],
	['ｽﾀﾝﾌﾟ帳',		'myself_stamp'],
	['ｺﾚｸｼｮﾝﾙｰﾑ',	'myself_collection'],
	['ｽｷﾙ継承',		'myself_skill'],
	['称号を変更',	'myself_shogo'],
	['ｾﾘﾌを変更',	'myself_mes'],
	['自己紹介',	'myself_profile'],
	['商人のお店',	'myself_shop'],
	['違法カジノ',	'myself_casino'],
	['ﾏｲﾋﾟｸﾁｬ',		'myself_picture'],
	['ﾏｲﾌﾞｯｸ',		'myself_book'],
	['商人の銀行',	'myself_bank'],
	['個人設定',	'myself_config'],
	['ﾊﾞｯｸｱｯﾌﾟ',	'myself_backup'],
);

if ($m{valid_blacklist}) {
	push @menus, ['ﾌﾞﾗﾘ', 'myself_blacklist'];
}

#================================================
sub begin {
	if (-f "$userdir/$id/goods_flag.cgi") {
		unlink "$userdir/$id/goods_flag.cgi";
	}

	$layout = 2;
	$is_mobile ? &my_status_mobile : &my_status_pc;
	&menu(map{ $_->[0] }@menus);
}
sub tp_1 {
	# 「ﾏｲﾙｰﾑ」を開いてTOPに戻りログインすると謎の空間に挟まる（ﾒｲﾝ画面にいるがﾒｲﾝ画面が中途半端。挟まる）
	# 他の lib は is_ng_cmd でｺﾏﾝﾄﾞ汚染されていたら begin を実行するため問題はないが、ﾏｲﾙｰﾑは begin を呼んでいなかったためバグってた
	# is_ng_cmd でﾁｪｯｸできないｺﾏﾝﾄﾞなので、とりあえずｺﾏﾝﾄﾞが未入力なら汚染されていると想定し begin を実行
	# この修正前の話かつ、この修正で直るとは思えないが、ﾏｲﾙｰﾑに入った状態でスマホを再起動してログインしたら begin 関数未定義エラーが発生したという報告あり
	unless ($in{mode}) { # ﾏｲﾙｰﾑ用のｺﾏﾝﾄﾞ汚染ﾁｪｯｸ（中身がないイコール汚染）
		return if &is_ng_cmd(1..$#menus); # ﾏｲﾙｰﾑ用のｺﾏﾝﾄﾞと通常のｺﾏﾝﾄﾞどちらも汚染されている
		&b_menu(@menus); # ﾏｲﾙｰﾑ用のｺﾏﾝﾄﾞは汚染されているが、通常のｺﾏﾝﾄﾞは汚染されていない
		return;
	}

	# ﾍﾟｯﾄ使用
	if ($in{mode} eq 'use_pet' && $m{pet} && ($pets[$m{pet}][2] eq 'myself' || ($m{pet} == 31 && &is_ceo))) {
		&refresh;
		&n_menu;

		require './lib/_use_pet_log.cgi';

		# ﾏﾓﾉﾉﾀﾈの場合
		if ($m{pet} >= 128 && $m{pet} <= 130) {
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、$m{name}のことをじっと見ている…<br>";
			$m{lib} = 'add_monster';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 168){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、異次元への扉を開いた<br>";
			open my $fh, "> $userdir/$id/upload_token.cgi";
			close $fh;

			$m{lib} = 'shopping_upload';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 177){
			if ($m{act} >= 100) {
				$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、$m{name}を牢獄へと誘おうとしたが疲れていたので断った<br>";
			}else {
				&write_use_pet_log($id, $m{pet});
				$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、$m{name}を牢獄へと誘った<br>";

				$m{lib} = 'prison';
				$m{tp}  = 300;
			}
		}
		elsif ($m{pet} == 175){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、ｱｲｺﾝにいたずらを仕掛けようとした<br>";

			$m{lib} = 'trick';
			$m{tp}  = 100;
		}
		elsif ($m{pet} == 176){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、称号にいたずらを仕掛けようとした<br>";

			$m{lib} = 'trick';
			$m{tp}  = 200;
		}
		elsif ($m{pet} == 185){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、財布にいたずらを仕掛けようとした<br>";

			$m{lib} = 'trick';
			$m{tp}  = 300;
		}
		elsif ($m{pet} == 186){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、声を出せないようにしようとした<br>";

			$m{lib} = 'trick';
			$m{tp}  = 400;
		}
		elsif ($m{pet} == 188){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、他の国から有用な人材を引き抜こうとした<br>";

			$m{lib} = 'trick';
			$m{tp}  = 500;
		}
		elsif ($m{pet} == 189){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、全国に聞こえるくらい大きな声で叫んだ<br>";

			$m{lib} = 'trick';
			$m{tp}  = 600;
		}
		elsif ($m{pet} == 190){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、あだ名をつけた<br>";

			$m{lib} = 'trick';
			$m{tp}  = 700;
		}
		elsif ($m{pet} == 191){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、世界に一つだけの武器を見つけた<br>";

			$m{lib} = 'trick';
			$m{tp}  = 800;
		}
		elsif ($m{pet} == 31 && $m{country} && &is_ceo){
			$mes .= "ポッポッポーｗｗｗハトポッポーｗｗｗｗｗｗ<br>";
			if ($cs{strong}[$m{country}] >= 15000 && !$cs{is_die}[$m{country}]) {
				my $total = 1000;
				for my $i (1..$w{country}) {
					unless ($i eq $m{country} || $i eq $union) {
						my $v = 500 + int(rand(10)) * 100;
						$cs{strong}[$i] += $v;
						$total += $v;
					}
				}
				$cs{strong}[$m{country}] -= $total;
				&write_cs;
				&write_use_pet_log($id, $m{pet});
				&remove_pet;
				my %sames;
				open my $fh, "< $logdir/$m{country}/member.cgi";
				while (my $player = <$fh>) {
					$player =~ tr/\x0D\x0A//d;
					# 同じ名前の人が複数いる場合
					next if ++$sames{$player} > 1;
					&regist_you_data($player,'next_salary',$time);
				}
				close $fh;
				$m{next_salary} = $time;
				&mes_and_world_news("<b>$cs{name}[$m{country}]は$cs{name}[$m{country}]人だけの所有物ではない</b>");
			} else {
				$mes .= "売るだけの国力とかないからｗｗｗｗｗ<br>";
			}
		}
		elsif ($m{pet} == 198){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、変な語尾を付けようとしている<br>";

			$m{lib} = 'trick';
			$m{tp}  = 900;
		}
		elsif ($m{pet} == 201){
			&write_use_pet_log($id, $m{pet});
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}は、風説の流布しようとしている<br>";

			$m{lib} = 'trick';
			$m{tp}  = 1000;
		}
		else {
			my $use_flag = 1;
			if(($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))){
				my @world_pets = (61, 64, 65, 66, 67, 68, 69, 70, 71, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 151, 152);
				for my $i(@world_pets){
					if($m{pet} == $i){
						$use_flag = 0;
						last;
					}
				}
			}
			if($use_flag){
				&write_use_pet_log($id, $m{pet});
				&{ $pets[$m{pet}][3] };
				if ($m{pet} > 0) {
					$mes .= "役目を終えた $pets[$m{pet}][1]★$m{pet_c} は光の彼方へ消えていった…<br>$pets[$m{pet}][1]★$m{pet_c}　ﾉｼ<br>";
				}
				else {
					$mes .= "役目を終えた $pets[$m{pet}][1] は光の彼方へ消えていった…<br>$pets[$m{pet}][1]　ﾉｼ<br>";
				}
				&remove_pet;
			}
		}
	} elsif ($in{mode} eq 'use_attack' && $w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		if ($in{luxury}) {
			&super_attack('luxury');
			$mes .= "必殺技の設定を解除しました<br>再設定は $coolhour 時間後にできます";
		} else {
			&super_attack('myroom');
		}
		&refresh;
		&n_menu;
	} elsif ($in{mode} eq 'regist_attack' && $w{world} eq $#world_states-4 && $m{country}) {
		if ($in{voice}) {
			require './lib/fate.cgi';
			if (&regist_attack($in{trigger}, $in{timing}, $in{demerit}, $in{max_count}, $in{effect}, $in{voice}, $in{random})) {
				$mes .= '必殺技を設定しました。';
				&refresh;
				&n_menu;
				return;
			}
		}

		&begin;
	}
	else {
		&b_menu(@menus);
	}
}


#================================================
# 携帯用ｽﾃｰﾀｽ表示
#================================================
sub my_status_mobile {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1] 消費$e2j{mp} $skills[$m_skill][3]<br>";
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_lea  = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
		$mes .= qq|【武器情報】<br><ul>|;
		$mes .= qq|<li>名前:$wname|;
		$mes .= qq|<li>属性:$weas[$m{wea}][2]|;
		$mes .= qq|<li>強さ:$weas[$m{wea}][3]|;
		$mes .= qq|<li>耐久:$weas[$m{wea}][4]|;
		$mes .= qq|<li>重さ:$weas[$m{wea}][5]</ul><hr>|;
		if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $sub_at  = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /風|炎|雷/)    { $sub_mat = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }

		my $m_min_wea;
		if ($weas[$m{wea}][2] eq '剣') {
			$m_min_wea = 1;
		} elsif($weas[$m{wea}][2] eq '槍') {
			$m_min_wea = 6;
		} elsif($weas[$m{wea}][2] eq '斧') {
			$m_min_wea = 11;
		} elsif($weas[$m{wea}][2] eq '炎') {
			$m_min_wea = 16;
		} elsif($weas[$m{wea}][2] eq '風') {
			$m_min_wea = 21;
		} elsif($weas[$m{wea}][2] eq '雷') {
			$m_min_wea = 26;
		} elsif($m{wea} == 0) {
			$m_min_wea = 0;
		} else {
			$m_min_wea = 33;
		}
		$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
		$m_wea_modify = 100 if ($m{wea} == 14) || ($m{wea} == 32);
		$m_wea_modify = 0 if ($m{wea} == 31);
		$sub_lea = ($m_wea_modify >= 0) ? "+$m_wea_modify" : "-".abs($m_wea_modify);
	}
	else {
		$sub_lea = "-100";
	}
	if ($m{gua}) {
		$mes .= qq|【防具情報】<br><ul>|;
		$mes .= qq|<li>名前:$guas[$m{gua}][1]|;
		$mes .= qq|<li>属性:$guas[$m{gua}][2]|;
		$mes .= qq|<li>強さ:$guas[$m{gua}][3]|;
		$mes .= qq|<li>耐久:$guas[$m{gua}][4]|;
		$mes .= qq|<li>重さ:$guas[$m{gua}][5]</ul><hr>|;
		if    ($guas[$m{gua}][2] =~ /無|剣|斧|槍/) { $sub_df  = "+$guas[$m{gua}][3]"; $sub_ag .= "-$guas[$m{gua}][5]"; }
		elsif ($guas[$m{gua}][2] =~ /風|炎|雷/)    { $sub_mdf = "+$guas[$m{gua}][3]"; $sub_ag .= "-$guas[$m{gua}][5]"; }
	}
	
	if ($m{pet}) {
		my $pet_c = $m{pet} > 0 ? "★$m{pet_c}" : "($m{pet_c}/$pets[$m{pet}][5])";
		$mes .= qq|【ﾍﾟｯﾄ情報】<br><ul>|;
		$mes .= qq|<li>名前:$pets[$m{pet}][1]$pet_c|;
		$mes .= qq|<li>効果:$pet_effects[$m{pet}]|;
		if($pet_sub_effects[$m{pet}]){
			$mes .= qq|<li>追加効果:$pet_sub_effects[$m{pet}]|;
		}
		$mes .= qq|</ul>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="ﾍﾟｯﾄを使用する" class="button1"></form>|;
		}
		$mes .= qq|<hr>|;
	}

	if ($w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
		$mes .= '<hr>';
	}
	my $m_st = &m_st;
	$mes .=<<"EOM";
		<b>$m{sedai}</b>世代目<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>
		勲章 <b>$m{medal}</b>個<br>
		ｶｼﾞﾉｺｲﾝ <b>$m{coin}</b>枚<br>
		宝ｸｼﾞ【$m{lot}】<br>
		<hr>
		【ｽﾃｰﾀｽ】強さ:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/$e2j{max_mp} [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>$sub_at]/$e2j{df} [<b>$m{df}</b>$sub_df]/<br>
		$e2j{mat} [<b>$m{mat}</b>$sub_mat]/$e2j{mdf} [<b>$m{mdf}</b>$sub_mdf]/<br>
		$e2j{ag} [<b>$m{ag}</b>$sub_ag]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>$sub_lea]<br>
		<hr>
		【覚えている技】<br>
		 $skill_info
		<hr>
		【熟練度】<br>
		農業 <b>$m{nou_c}</b>/商業 <b>$m{sho_c}</b>/徴兵 <b>$m{hei_c}</b>/外交 <b>$m{gai_c}</b>/待伏 <b>$m{mat_c}</b>/<br>
		強奪 <b>$m{gou_c}</b>/諜報 <b>$m{cho_c}</b>/洗脳 <b>$m{sen_c}</b>/脱獄 <b>$m{esc_c}</b>/救出 <b>$m{res_c}</b>/<br>
		偵察 <b>$m{tei_c}</b>/偽計 <b>$m{gik_c}</b>/攻城 <b>$m{kou_c}</b>/ｶｼﾞﾉ <b>$m{cas_c}</b>/魔物 <b>$m{mon_c}</b>/<br>
		修行 <b>$m{shu_c}</b>/討伐 <b>$m{tou_c}</b>/闘技 <b>$m{col_c}</b>/ﾚｰﾄ  <b>$m{cataso_ratio}</b>/no1 <b>$m{no1_c}</b>/<br>
		統一 <b>$m{hero_c}</b>/復興 <b>$m{huk_c}</b>/滅亡 <b>$m{met_c}</b>/祭 <b>$m{fes_c}</b>/<br>
		<hr>
		【代表\者ﾎﾟｲﾝﾄ】<br>
		戦争 <b>$m{war_c}</b>/内政 <b>$m{dom_c}</b>/軍事 <b>$m{mil_c}</b>/外交 <b>$m{pro_c}</b>/
		<hr>
		【戦歴】<br>
		<b>$war_c</b>戦 <b>$m{win_c}</b>勝 <b>$m{lose_c}</b>負 <b>$m{draw_c}</b>引<br>
		勝率 <b>$win_par</b>%
EOM
}

#================================================
# PC用ｽﾃｰﾀｽ表示
#================================================
sub my_status_pc {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td><td align="right">$skills[$m_skill][3]<br></td></tr>|;
	}

	$mes .= '<hr>';
	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_lea  = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
		$mes .= qq|【武器情報】<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>名前</th><td>$wname</td>|;
		$mes .= qq|<th>属性</th><td>$weas[$m{wea}][2]</td>|;
		$mes .= qq|<th>強さ</th><td>$weas[$m{wea}][3]</td>|;
		$mes .= qq|<th>耐久</th><td>$weas[$m{wea}][4]</td>|;
		$mes .= qq|<th>重さ</th><td>$weas[$m{wea}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $sub_at  = "▲$weas[$m{wea}][3]"; $sub_ag = "▼$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /風|炎|雷/)    { $sub_mat = "▲$weas[$m{wea}][3]"; $sub_ag = "▼$weas[$m{wea}][5]"; }

		my $m_min_wea;
		if ($weas[$m{wea}][2] eq '剣') {
			$m_min_wea = 1;
		} elsif($weas[$m{wea}][2] eq '槍') {
			$m_min_wea = 6;
		} elsif($weas[$m{wea}][2] eq '斧') {
			$m_min_wea = 11;
		} elsif($weas[$m{wea}][2] eq '炎') {
			$m_min_wea = 16;
		} elsif($weas[$m{wea}][2] eq '風') {
			$m_min_wea = 21;
		} elsif($weas[$m{wea}][2] eq '雷') {
			$m_min_wea = 26;
		} elsif($m{wea} == 0) {
			$m_min_wea = 0;
		} else {
			$m_min_wea = 33;
		}
		$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
		$m_wea_modify = 100 if ($m{wea} == 14) || ($m{wea} == 32);
		$m_wea_modify = 0 if ($m{wea} == 31);
		$sub_lea = ($m_wea_modify >= 0) ? "▲$m_wea_modify" : "▼".abs($m_wea_modify);
	}
	else {
		$sub_lea = "▼100";
	}
	if ($m{gua}) {
		$mes .= qq|【防具情報】<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>名前</th><td>$guas[$m{gua}][1]</td>|;
		$mes .= qq|<th>属性</th><td>$guas[$m{gua}][2]</td>|;
		$mes .= qq|<th>強さ</th><td>$guas[$m{gua}][3]</td>|;
		$mes .= qq|<th>耐久</th><td>$guas[$m{gua}][4]</td>|;
		$mes .= qq|<th>重さ</th><td>$guas[$m{gua}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($guas[$m{gua}][2] =~ /無|剣|斧|槍/) { $sub_df  = "▲$guas[$m{gua}][3]"; $sub_ag .= "▼$guas[$m{gua}][5]"; }
		elsif ($guas[$m{gua}][2] =~ /風|炎|雷/)    { $sub_mdf = "▲$guas[$m{gua}][3]"; $sub_ag .= "▼$guas[$m{gua}][5]"; }
	}
	
	if ($m{pet}) {
		my $pet_c = $m{pet} > 0 ? "★$m{pet_c}" : "($m{pet_c}/$pets[$m{pet}][5])";
		$mes .= qq|【ﾍﾟｯﾄ情報】<br>|;
		$mes .= qq|<table class="table1" cellpadding="3">|;
		$mes .= qq|<tr><th>名前</th><td>$pets[$m{pet}][1]$pet_c</td>|;
		$mes .= qq|<th>効果</th><td>$pet_effects[$m{pet}]</td></tr>|;
		if($pet_sub_effects[$m{pet}]){
			$mes .= qq|<tr><th>追加効果</th><td colspan="3">$pet_sub_effects[$m{pet}]</td></tr>|;
		}
		$mes .= qq|</table>|;
		if ($pets[$m{pet}][2] eq 'myself' || ($m{pet} == 31 && &is_ceo)) {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="ﾍﾟｯﾄを使用する" class="button1"></form>|;
		}
		$mes .= qq|<hr size="1">|;
	}

	if ($w{world} eq $#world_states-4 && $m{country}) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
		$mes .= '<hr size="1">';
	}
	
	my $m_st = &m_st;
	$mes .= <<"EOM";
		【ｽﾃｰﾀｽ】強さ：$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}$sub_at</td>
			<th>$e2j{df}</th><td align="right">$m{df}$sub_df</td>
		</tr><tr>
			<th>$e2j{max_mp}</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}$sub_mat</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}$sub_mdf</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}$sub_lea</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}$sub_ag</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		【覚えている技】<br>
		<table class="table1" cellpadding="3">
		<tr><th>属性</th><th>技名</th><th>消費$e2j{mp}</th></tr>
		$skill_info
		</table>

		<hr size="1">
		【熟練度】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>農業</th><td align="right">$m{nou_c}</td>
			<th>商業</th><td align="right">$m{sho_c}</td>
			<th>徴兵</th><td align="right">$m{hei_c}</td>
			<th>外交</th><td align="right">$m{gai_c}</td>
			<th>待伏</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>強奪</th><td align="right">$m{gou_c}</td>
			<th>諜報</th><td align="right">$m{cho_c}</td>
			<th>洗脳</th><td align="right">$m{sen_c}</td>
			<th>脱獄</th><td align="right">$m{esc_c}</td>
			<th>救出</th><td align="right">$m{res_c}</td>
		</tr>
		<tr>
			<th>偵察</th><td align="right">$m{tei_c}</td>
			<th>偽計</th><td align="right">$m{gik_c}</td>
			<th>攻城</th><td align="right">$m{kou_c}</td>
			<th>ｶｼﾞﾉ</th><td align="right">$m{cas_c}</td>
			<th>魔物</th><td align="right">$m{mon_c}</td>
		</tr>
		<tr>
			<th>修行</th><td align="right">$m{shu_c}</td>
			<th>討伐</th><td align="right">$m{tou_c}</td>
			<th>闘技</th><td align="right">$m{col_c}</td>
			<th>ﾚｰﾄ</th><td align="right">$m{cataso_ratio}</td>
			<th>no1</th><td align="right">$m{no1_c}</td>
		</tr>
		<tr>
			<th>統一</th><td align="right">$m{hero_c}</td>
			<th>復興</th><td align="right">$m{huk_c}</td>
			<th>滅亡</th><td align="right">$m{met_c}</td>
			<th>祭</th><td align="right">$m{fes_c}</td>
			<th>　</th><td align="right">　</td>
		</tr>
		</table>
		
		<hr size="1">
		【代表\者ﾎﾟｲﾝﾄ】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>戦争</th><td align="right">$m{war_c}</td>
			<th>内政</th><td align="right">$m{dom_c}</td>
			<th>軍事</th><td align="right">$m{mil_c}</td>
			<th>外交</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>
		
		<hr size="1">
		【戦歴】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>戦回</th><td align="right">$war_c</td>    
			<th>勝ち</th><td align="right">$m{win_c}</td> 
			<th>負け</th><td align="right">$m{lose_c}</td>
			<th>引分</th><td align="right">$m{draw_c}</td>
			<th>勝率</th><td align="right">$win_par %</td>
		</tr>
		</table>
EOM
}


1; # 削除不可
