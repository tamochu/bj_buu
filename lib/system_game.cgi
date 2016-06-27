#================================================
# ｹﾞｰﾑ(bj.cgi)でよく使う処理 Created by Merino
#================================================
require './lib/jcode.pl';
require './lib/summer_system_game.cgi';
require './lib/seed.cgi';
use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# 国 + 世界 データ書き込み ./log/countries.cgiに書き込み
#================================================
sub write_cs {
	&error("国ﾃﾞｰﾀの書き込みに失敗しました") if $cs{name}[1] eq '';
	
	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可)
	my @keys = (qw/
		name strong tax food money soldier state is_die member capacity color
		win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
		modify_war modify_dom modify_mil modify_pro
		extra extra_limit disaster disaster_limit
		new_commer
	/);
	# 国名　総国力　税率　総兵糧　国家予算　総兵士数　状態　滅亡ﾌﾗｸﾞ　所属人数　定員　国色
	# 統一数　旧代表者　代表者　参謀　内政官　策士　外交官　参謀ﾎﾟｲﾝﾄ　内政官ﾎﾟｲﾝﾄ　策士ﾎﾟｲﾝﾄ　外交官ﾎﾟｲﾝﾄ　代表年期
	# 各国設定戦争　内政　軍事　外交
	# 追加効果　追加効果期限　国別災害　国別災害有効期間
	# 新規数
	
	# -------------------
	# 物資の最大値
	my $max_resource = ($w{world} eq '14' || ($w{world} eq '19' && $w{world_sub} eq '14')) ? 300000 : 999999; # 世界情勢[大殺界なら500000まで]
	$cs{food}[$m{country}]    = $max_resource if $cs{food}[$m{country}]    > $max_resource;
	$cs{money}[$m{country}]   = $max_resource if $cs{money}[$m{country}]   > $max_resource;
	$cs{soldier}[$m{country}] = $max_resource if $cs{soldier}[$m{country}] > $max_resource;
	
	# 拙速
	if ($w{world} eq $#world_states - 5) {
		$cs{state}[$m{country}] = 0;
	}
	
	my $world_line = &_get_world_line; # 世界情報
	my @lines = ($world_line);
	for my $i (1 .. $w{country}) {
		my $line;
		for my $k (@keys) {
			$line .= "$k;$cs{$k}[$i]<>";
		}
		push @lines, "$line\n";
	}
	
	open my $fh, "> $logdir/countries.cgi" or &error("国データが開けません");
	print $fh @lines;
	close $fh;
}
#================================================
# 世界情報
#================================================
sub _get_world_line { # Get %w line
	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可)
	my @keys = (qw/
		country year game_lv limit_time reset_time win_countries player world playing world_sub sub_time twitter_bot
	/);
	# 国の数　年　難易度　統一期限　ﾘｾｯﾄされた時間　前回の統一国(複数)　ﾌﾟﾚｲﾔｰ人数　世界情勢　ﾌﾟﾚｲ中人数　サブ情勢　サブ時間　twitter用カウント
	
	my $line = '';
	for my $k (@keys) {
		$line .= "$k;$w{$k}<>";
	}
	
	# -------------------
	# 友好度/条約
	for my $i (1 .. $w{country}) {
		for my $j ($i+1 .. $w{country}) {
			my $f_c_c  = "f_${i}_${j}";
			my $p_c_c = "p_${i}_${j}";
			$line .= "$f_c_c;$w{$f_c_c}<>";
			$line .= "$p_c_c;$w{$p_c_c}<>";
		}
	}
	$line .= "\n";
	
	return $line;
}
#================================================
# ﾌﾟﾚｲﾔｰﾃﾞｰﾀ書き込み
#================================================
# turn value stock y_***** は自分のｽﾃｰﾀｽと関係ないので自由に取り回してよい
sub write_user {
	&error("ﾌﾟﾚｲﾔｰﾃﾞｰﾀの書き込みに失敗しました") if !$id || !$m{name};
	$m{ltime} = $time;
	$m{ldate} = $date;
	# -------------------
	# topのﾛｸﾞｲﾝﾘｽﾄに表示
	if ($time > $m{login_time} + $login_min * 60) {
		$m{login_time} = $time;
		open my $fh2, ">> $logdir/login.cgi";
		print $fh2 "$time<>$m{name}<>$m{country}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
		close $fh2;
	}
	# -------------------
	# ｽﾃｰﾀｽの最大値
	if ($m{cha_org}) {
		$m{cha} = $m{cha_org};
	}
	for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
		$m{$k} = 999 if $m{$k} > 999;
	}
	$m{money}  = int($m{money});
	my $money_limit = 4999999;
	if ($m{money_overflow}) {
		if ($money_limit < $m{money_limit}) {
			$money_limit = $m{money_limit};
		} else {
			$m{money_overflow} = 0;
		}
	}
	$m{money}  = $money_limit if $m{money} > $money_limit;
	$m{coin}   = 2500000 if $m{coin}  > 2500000;
	# -------------------
	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可(login_time以外))
	my @keys = (qw/
		login_time ldate start_time name pass lib tp wt act sex shogo sedai vote
		country job seed lv exp rank rank_exp super_rank rank_name unit sol sol_lv medal money coin skills renzoku renzoku_c total_auction skills_sub skills_sub2 skills_sub3 money_limit
		max_hp hp max_mp mp at df mat mdf ag cha lea wea wea_c wea_lv wea_name gua egg egg_c pet pet_c shuffle master master_c boch_pet
		marriage lot is_full next_salary icon mes mes_win mes_lose mes_touitsu ltime gacha_time gacha_time2 offertory_time trick_time breed_time silent_time
		rest_a rest_b rest_c
		
		turn stock value is_playing bank
		y_max_hp y_hp y_max_mp y_mp y_at y_df y_mat y_mdf y_ag y_cha y_lea y_wea y_wea_name y_skills
		y_name y_country y_rank y_sol y_unit y_sol_lv y_icon y_mes_win y_mes_lose y_pet y_value y_gua
		y_rest_a y_rest_b y_rest_c
		
		nou_c sho_c hei_c gai_c gou_c cho_c sen_c gik_c tei_c mat_c cas_c tou_c shu_c col_c mon_c
		win_c lose_c draw_c hero_c huk_c met_c war_c dom_c mil_c pro_c esc_c res_c fes_c war_c_t dom_c_t mil_c_t pro_c_t boch_c storm_c
		shogo_t icon_t breed breed_c depot_bonus akindo_guild silent_kind silent_tail guild_number disp_casino chat_java disp_top disp_news disp_chat disp_ad disp_daihyo salary_switch no_boss incubation_switch disp_gacha_time delete_shield
		valid_blacklist war_select_switch
		c_turn c_stock c_value c_type tp_r cataso_ratio
		no1_c money_overflow random_migrate ceo_c tam_c ban_c wt_c wt_c_latest
		
		sox_kind sox_no exchange_count
	/);
	# ﾛｸﾞｲﾝ時間　更新日時　作成日時　名前　ﾊﾟｽﾜｰﾄﾞ　ﾗｲﾌﾞﾗﾘ　ﾀｰﾆﾝｸﾞﾎﾟｲﾝﾄ　待ち時間　疲労度　性別　称号　世代　投票　
	# 所属国　職業　種族　ﾚﾍﾞﾙ　経験値　ﾗﾝｸ　ﾗﾝｸ経験値　兵種　兵士数　士気　勲章　お金　ｺｲﾝ　技(複数)　連続攻めた国　連続ｶｳﾝﾄ　
	# 最大HP　HP　最大MP　MP　力　守り　魔力　魔防　素早　魅力　統率　武器　武器耐久　武器ﾚﾍﾞﾙ　防具　特殊武器名　ﾀﾏｺﾞ　ﾀﾏｺﾞ成長　ﾍﾟｯﾄ　シャッフルフラグ　
	# 結婚相手　宝ｸｼﾞ　預かり所満杯ﾌﾗｸﾞ　次の給与　ｱｲｺﾝ　ﾒｯｾｰｼﾞ　勝ちｾﾘﾌ　負けｾﾘﾌ　統一ｾﾘﾌ　更新時間　ｶﾞﾁｬ時間 ｶﾞﾁｬ時間2 賽銭時間　いたずら解除時間　発言禁止時間
	# ﾀｰﾝ　ｽﾄｯｸ　ﾊﾞﾘｭｰ　ﾌﾟﾚｲ中ﾌﾗｸﾞ　相手ﾃﾞｰﾀ …
	# 農業　商業　徴兵　外交　強奪　諜報　洗脳　偽計　偵察　待伏　ｶｼﾞﾉ　討伐　修行　闘技場　魔物　脱獄　救出　祭　混乱用　ボッチ
	# 戦争勝ち　戦争負け　戦争引分　統一　復興　滅亡　戦争　内政　軍事　外交　
	# 真称号　真ｱｲｺﾝ　育て屋１　育て屋２　預り所ボーナス　商人ギルド　対人ｶｼﾞﾉ表示　交流JAVA表示
	# ｶｼﾞﾉ用 …
	# 隠蔽熟練度
	# _cはカウント(count)の略, y_は相手(you)の略
	
	my $line;
	for my $k (@keys) {
		$line .= $k =~ /^y_(.+)$/ ? "$k;$y{$1}<>" : "$k;$m{$k}<>";
	}
	
	open my $fh, "> $userdir/$id/user.cgi";
	print $fh "$line\n";
	print $fh "$addr<>$host<>$agent<>\n";
	close $fh;
	
	&alltime_event;
}
#================================================
# その他
#================================================
# 待ち時間を秒に変換 + 次へ
sub wait {
	$m{wt} = $GWT * 60;
	$m{wt_c} += $m{wt};
	&n_menu;
	$m{is_playing} = 0;
	--$w{playing};
	$w{playing} = 0 if $w{playing} < 0;
	&write_cs;
}
# 通常時の利用条件
sub is_satisfy { 1 }
# 値をﾘｾｯﾄ
sub refresh {
	$m{lib} = '';
	$m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
}
#================================================
# 疲労状態のときの利用条件
#================================================
sub is_act_satisfy {
	if ($m{act} >= 100) {
		$mes .= '疲労がたまっています。一度内政を行ってください<br>';
		&refresh;
		&n_menu;
		return 1;
	}
	return 0;
}
#================================================
# ｺﾏﾝﾄﾞ汚染ﾁｪｯｸ。期待している値と違う場合は 1(true) が返り&begin(初期ﾒﾆｭｰ表示)
#================================================
sub is_ng_cmd {
	my @check_cmds = @_;
	for $check_cmd (@check_cmds) {
		return 0 if $cmd eq $check_cmd;
	}
	&begin;
	return 1;
}
#================================================
# ﾒｲﾝﾒﾆｭｰなどの処理 main.cgi country.cgi myself.cgi shopping.cgi
#================================================
sub b_menu {
	my @menus = @_;
	
	if (!$m{is_playing} && $w{playing} >= $max_playing) {
		$mes .= qq|<font color="#FFFF00">ﾌﾟﾚｲ規制中 $w{playing}/$max_playing人</font><br>しばらくお待ちください|;
		&begin;
	}
	elsif (defined $menus[$cmd]) {
		$m{lib} = $menus[$cmd][1];
		$m{tp}   = 1;
		require "./lib/$m{lib}.cgi";
		
		# lib実行条件okならbeginﾒﾆｭｰ
		&begin if &is_satisfy;
		
		unless ($m{is_playing}) {
			$m{is_playing} = 1;
			++$w{playing};
			&write_cs;
		}
	}
	else {
		&begin;
	}
}
#================================================
# ﾒﾆｭｰｺﾏﾝﾄﾞ
#================================================
sub menu {
	my @menus = @_;
	if($is_smart){
=pod
		$menu_cmd .= qq|<div>|;
#		$menu_cmd .= qq|<div style="float:right;">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<form method="$method" action="$script" class="cmd_form">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button2s"><input type="hidden" name="cmd" value="$i">|;
#			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
#			print "$i ", ($i+1) % 4, " " , ($i+1) % 6, "<br>";

#			$menu_cmd .= qq|</div>| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
			$menu_cmd .= qq|<br class="smart_br" />| if ($i+1) % 4 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr" />| if ($i+1) % 4 == 0;
			$menu_cmd .= qq|<br class="tablet_br" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="tablet_hr" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr">| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
		}
		$menu_cmd .= qq|</div>|;
#		$menu_cmd .= qq|<br style="display:none;">|;
=cut

		$menu_cmd .= qq|<table boder=0 cols=4 width=110 height=110>|;
		for my $i (0 .. $#menus) {
			if($i % 4 == 0){
				$menu_cmd .= qq|<tr>|;
			}
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 4 == 3){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#menus % 4 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;

	}else{
		$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<option value="$i">$menus[$i]</option>|;
		}
		$menu_cmd .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= $is_mobile ? qq|<br><input type="submit" value="決 定" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="決 定" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}
}
#================================================
# Nextﾒﾆｭｰ
#================================================
sub n_menu {
	$menu_cmd  = qq|<form method="$method" action="$script">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="Next" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}
#================================================
# 携帯用Pager 次へ前へ shopping_hospital.cgi
#================================================
sub pager_next {
	my $page = shift;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="次のﾍﾟｰｼﾞ" class="button1"></form>|;
}
sub pager_back {
	my $page = shift;
	$page = 0 if $page < 0;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="前のﾍﾟｰｼﾞ" class="button1"></form>|;
}
#================================================
# 熟練度ｱｯﾌﾟ
#================================================
sub c_up { # count up
	my $c = shift;
	++$m{$c};
	# 連続でc_upされる用としてｸﾞﾛｰﾊﾞﾙな退避変数と判定に必要な配列作成
	if ($cash_c ne $c) {
		$cash_c = $c;
		@cash_shogos = ();
		for my $shogo (@shogos) {
			my($k) = keys %{ $shogo->[1] }; # なせかeachだと2回目がとれない…
			push @cash_shogos, [$shogo->[0], $shogo->[1]->{$k}, $shogo->[2]] if $c eq $k;
		}
		@cash_secret_shogos = ();
		for my $secret_shogo (@secret_shogos) {
			my($k) = keys %{ $secret_shogo->[1] }; # なせかeachだと2回目がとれない…
			push @cash_secret_shogos, [$secret_shogo->[0], $secret_shogo->[1]->{$k}, $secret_shogo->[2]] if $c eq $k;
		}
	}
	
	for my $cash_shogo (@cash_shogos) {
		if ($cash_shogo->[1] eq $m{$c}) {
			&mes_and_world_news("$cash_shogo->[0]の称号を与えられました", 1);
			&send_twitter("$cash_shogo->[0]の称号を与えられました", 1);
			$m{money} += $cash_shogo->[2];
			$mes .= "$cash_shogo->[2]Gの報奨金を受け取りました<br>";
		}
	}
	
	@cash_secret_shogos = sort { $a->[1] <=> $b->[1] } @cash_secret_shogos;
	
	# 永遠の証に計上されない特殊称号
	my $secret = ['', 0, 0];
	for my $cash_secret_shogo (@cash_secret_shogos) {
		if ($cash_secret_shogo->[1] <= $m{$c}) {
			$secret = $cash_secret_shogo;
		}
	}
	
	if ($secret->[0]) {
		&mes_and_world_news("$secret->[0]の称号を与えられました", 1);
		&send_twitter("$secret->[0]の称号を与えられました", 1);
		$m{money} += $secret->[2];
		$mes .= "$secret->[2]Gの報奨金を受け取りました<br>";
		$m{shogo} = $secret->[0];
	}
	
	# 軍事系の師匠効果は ./lib/military.cgi で military_master_c_up
	return if $c == 'gou_c' || $c == 'cho_c' || $c == 'sen_c' || $c == 'tei_c' || $c == 'gik_c' || $c == 'mat_c';
	# 弟子の場合2倍取得
	if ($m{master_c} eq $c) {
		++$m{$c};
		# 連続でc_upされる用としてｸﾞﾛｰﾊﾞﾙな退避変数と判定に必要な配列作成
		if ($cash_c ne $c) {
			$cash_c = $c;
			@cash_shogos = ();
			for my $shogo (@shogos) {
				my($k) = keys %{ $shogo->[1] }; # なせかeachだと2回目がとれない…
				push @cash_shogos, [$shogo->[0], $shogo->[1]->{$k}, $shogo->[2]] if $c eq $k;
			}
		}
		
		for my $cash_shogo (@cash_shogos) {
			if ($cash_shogo->[1] eq $m{$c}) {
				&mes_and_world_news("$cash_shogo->[0]の称号を与えられました", 1);
				&send_twitter("$cash_shogo->[0]の称号を与えられました", 1);
				$m{money} += $cash_shogo->[2];
				$mes .= "$cash_shogo->[2]Gの報奨金を受け取りました<br>";
			}
		}
	}
}
#================================================
# 代表者ﾎﾟｲﾝﾄｱｯﾌﾟ
#================================================
sub daihyo_c_up {
	my $c = shift;
	++$m{$c};
	my($k) = $c =~ /^(.+)_c$/;
	if ($cs{$k}[$m{country}] eq $m{name}) {
		$cs{$c}[$m{country}] = $m{$c};
	}
	elsif (!&is_daihyo && $m{$c} > $cs{$c}[$m{country}] && $m{$c} >= 10) {
		&mes_and_world_news(qq|<font color="#FF9999">★日頃の国への貢献が認められ$cs{name}[$m{country}]代表\の$e2j{$k}に任命されました★</font>|,1);
		$cs{$k}[$m{country}] = $m{name};
		$cs{$c}[$m{country}] = $m{$c};
	}
}
#================================================
# 国にいるプレイヤー名取得
#================================================
sub get_country_members {
	my $country = shift;
	&error("国No[ $country ] その国が存在しないよ") unless -d "$logdir/$country";
	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("国$countryプレイヤーデータが開けません");
	push @lines, $_ while <$fh>;
	close $fh;
	
	return @lines;
}
#================================================
# 他ﾌﾟﾚｲﾔｰにｱｲﾃﾑを郵送
#================================================
sub send_item {
	my($send_name, $kind, $item_no, $item_c, $item_lv, $force_send) = @_;
	my $send_id = unpack 'H*', $send_name;
	my $s_mes;
	$item_c  ||= 0;
	$item_lv ||= 0;
	
	unless(-f "$userdir/$send_id/user.cgi"){
		return;
	}
	my %datas = &get_you_datas($send_name);
	
	if (-f "$userdir/$send_id/depot.cgi" && ($force_send || !$datas{is_full})) {
		open my $fh, ">> $userdir/$send_id/depot.cgi";
		print $fh "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		close $fh;
		
		open my $fh2, "> $userdir/$send_id/depot_flag.cgi";
		close $fh2; 
	}
	
	$s_mes = &get_item_name($kind, $item_no); # アイテム名だけ
	if (-f "$userdir/$send_id/depot_watch.cgi"){
		my $depot_line = '';
		open my $rfh, "< $userdir/$send_id/depot.cgi";
		while (my $line = <$rfh>){
			my ($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			$depot_line .= "$rkind,$ritem_no,$ritem_c,$ritem_lv<>";
		}
		close $rfh;
		
		open my $wfh, ">> $userdir/$send_id/depot_watch.cgi";
		my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
		$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
		print $wfh "$send_nameから$s_mes ($tdate)<>$depot_line\n";
		close $wfh;
	}
	unless ($send_name eq $m{name}){
		if (-f "$userdir/$send_id/money.cgi") {
			open my $fh, ">> $userdir/$send_id/money.cgi";
			print $fh "$m{name}<>$s_mes<>2<>\n";
			close $fh;
		}
	}
}
#================================================
# 他ﾌﾟﾚｲﾔｰにお金を送金
#================================================
sub send_money {
	my($send_name, $from_name, $money, $is_shop_sale) = @_;
	my $send_id = unpack 'H*', $send_name;
	$is_shop_sale||= 0;
	if (-f "$userdir/$send_id/money.cgi") {
		open my $fh, ">> $userdir/$send_id/money.cgi";
		print $fh "$from_name<>$money<>$is_shop_sale<>\n";
		close $fh;
	}
}
#================================================
# 表示しつつﾆｭｰｽにも書き込む
#================================================
sub mes_and_world_news {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '名無し';
	}
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_world_news("<b>$c_mの$w_nameが</b>$message", @_)
	: $message =~ /^<i>/  ? &write_world_news("<i>$c_mの$w_nameが</i>$message", @_)
	: $message =~ /^<em>/ ? &write_world_news("<em>$c_mの$w_nameが</em>$message", @_)
	:					    &write_world_news("$c_mの$w_nameが$message", @_)
	;
}
sub mes_and_send_news {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '名無し';
	}
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_send_news("<b>$c_mの$w_nameが</b>$message", @_)
	: $message =~ /^<i>/  ? &write_send_news("<i>$c_mの$w_nameが</i>$message", @_)
	: $message =~ /^<em>/ ? &write_send_news("<em>$c_mの$w_nameが</em>$message", @_)
	:					    &write_send_news("$c_mの$w_nameが$message", @_)
	;
}
#================================================
# 過去の栄光、物流情報ログ書き込み処理
#================================================
#sub write_world_news     { &_write_news('world_news', @_) }
sub write_world_news     {
	my($message, $is_memory, $memory_name) = @_;
	if ($w{world} ne '10' || $message =~ /^</) { # ”世界情勢【沈黙】以外”または大きな出来事
		&_write_news('world_news', @_);
	}
	elsif ($is_memory) { # 世界情勢【沈黙】で戦歴フラグがあった場合
		$message = &coloration_country($message);
		&write_memory($message, $memory_name);
	}
	&twitter_bot;
}
sub write_send_news      { &_write_news('send_news',  @_) }
sub write_blog_news      { &_write_news('blog_news',  @_) }
sub write_colosseum_news { &_write_news('colosseum_news',  @_) }
sub write_picture_news   { &_write_news('picture_news',  @_) }
sub write_book_news      { &_write_news('book_news',  @_) }
sub write_entry_news      { &_write_news('entry_news',  @_) }
sub _write_news {
	my($file_name, $message, $is_memory, $memory_name) = @_;
	
	&write_world_big_news($message) if $message =~ /^</;
	$message = &coloration_country($message);
	my @lines = ();
	open my $fh, "+< $logdir/$file_name.cgi" or &error("$file_name.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	my $combo = 0;
	if ($head_line =~ /<input type="hidden" name="combo" value="(\d+)_(\d+)">/) {
		if ($1 eq $m{country}) {
			$combo = $2 + 1;
		}
	}
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	my $combo_class = $combo < 5 ? 'no_combo' :
						$combo < 10 ? 'first_bullet' :
						$combo < 15 ? 'second_bullet' :
						$combo < 20 ? 'last_bullet' :
						$combo < 25 ? 'alter_bullet' :
						'max_combo';
	unshift @lines, qq|<span class="$combo_class">$message <font size="1">($date)</font><input type="hidden" name="combo" value="$m{country}_$combo"></span>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&write_memory($message, $memory_name) if $is_memory;
}
#================================================
# 世界の流れ
#================================================
sub write_world_big_news {
	my $message = shift;
	$message = &coloration_country($message);
	my @lines = ();
	open my $fh, "+< $logdir/world_big_news.cgi" or &error("$logdir/world_big_news.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
# ------------------
# 国名があれば色付け
sub coloration_country {
	my $message = shift;
	return $message if $w{country} < 1;
	for my $i (0 .. $w{country}) {
		my $add_color_country = qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		$message =~ s/\Q$cs{name}[$i]\E/$add_color_country/g;
	}
	return $message;
}
#================================================
# 石碑
#================================================
sub write_legend {
	my($file_name, $message, $is_memory, $memory_name) = @_;
	
	my @lines = ();
	open my $fh, "+< $logdir/legend/$file_name.cgi" or &error("$logdir/legend/$file_name.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	$message = &coloration_country($message);
	unshift @lines, qq|$world_name暦$w{year}年【$world_states[$w{world}]】：$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	&write_memory($message, $memory_name) if $is_memory;
}
#================================================
# 思い出ログ書き込み処理
#================================================
# 引数に名前がある場合は、その人の戦歴に、ない場合は自分の戦歴に書き込まれる
sub write_memory {
	my($message, $memory_name) = @_;
	$m_id = $memory_name ? unpack 'H*', $memory_name : $id;
	
	return unless -f "$userdir/$m_id/memory.cgi";
	
	my @lines = ();
	open my $fh, "+< $userdir/$m_id/memory.cgi" or &error("Memoryﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
#================================================
# 自分と相手の強さ判別  2:強い 1:普通 0:弱い
#================================================
sub st_lv {
	my $y_st = shift || &y_st;
	my $m_st =          &m_st;
	
	return $y_st > $m_st * 1.5 ? 2
		:  $y_st < $m_st * 0.5 ? 0
		:                        1
		;
}
sub y_st { int($y{max_hp} + $y{max_mp} + $y{at} + $y{df} + $y{mat} + $y{mdf} + $y{ag} + $y{cha}*0.5) }
sub m_st { int($m{max_hp} + $m{max_mp} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag} + $m{cha}*0.5) }
#================================================
# 災害 滅亡時低確率、ﾛﾌﾟﾄ使用時
#================================================
sub disaster {
	my $more = shift;
	my @disasters = (
		['自然災害','food'],
		['経済破綻','money'],
		['大地震','soldier'],
	);
	if ($more) {
		push @disasters, ['一定時間国防が脆弱化','paper'];
		push @disasters, ['一定時間指揮系統が混乱','mismatch'];
		push @disasters, ['大泥棒が出現','concentrate'];
		unless ($w{world} eq $#world_states || $w{world} eq $#world_states-1 || $w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-4 || $w{world} eq $#world_states-5) {
			push @disasters, ['魔人復活','strong'];
		}
		if ($w{world} eq '12') {
			push @disasters, ['大飢饉', 'big_food'];
			push @disasters, ['大恐慌', 'big_money'];
			push @disasters, ['大津波', 'big_soldier'];
		}
	}
	my $v = int(rand(@disasters));
	if ($disasters[$v][1] eq 'food' || $disasters[$v][1] eq 'money' || $disasters[$v][1] eq 'soldier') {
		for my $i (1 .. $w{country}) {
			next if $cs{ is_die }[$i];
			$cs{ $disasters[$v][1] }[$i] = int($cs{ $disasters[$v][1] }[$i] * 0.5);
		}
		&write_world_news("<b>世界中に $disasters[$v][0] が起こりました</b>");
	} elsif ($disasters[$v][1] eq 'strong' && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{ $disasters[$v][1] }[$target] -= int(rand(10)+5) * 100;
		&write_world_news("<b>$cs{name}[$target]に $disasters[$v][0] が起こりました</b>");
	} elsif (($disasters[$v][1] eq 'paper' || $disasters[$v][1] eq 'mismatch') && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{disaster}[$target] = $disasters[$v][1];
		$cs{disaster_limit}[$target] = $time + 1 * 60 * 60;
		&write_world_news("<b>$cs{name}[$target]で $disasters[$v][0] しました</b>");
	} elsif ($disasters[$v][1] eq 'concentrate') {
		my @rlist = ('food', 'money', 'soldier');
		my $r = $rlist[int(rand(@rlist))];
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			next if $i eq $m{country};
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.5);
			$cs{$r}[$m{country}] += $cs{$r}[$i];
		}
		&write_world_news("<b>世界中に $disasters[$v][0] しました</b>");
	} elsif ($disasters[$v][1] =~ 'big_(.*)') {
		$r = $1;
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.1);
		}
		&write_world_news("<b>世界中に $disasters[$v][0] が起こりました</b>");
	}
}
#================================================
# 相手ﾃﾞｰﾀがあるかチェック
#================================================
sub you_exists {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;
	
	if (-f "$userdir/$y_id/user.cgi") {
		return 1;
	}
	return 0;
}
#================================================
# 相手ﾃﾞｰﾀをGet 戻り値はハッシュ
#================================================
# 使い方: &get_you_datas('相手の名前');
sub get_you_datas {
	my($name, $is_unpack) = @_;
	
	my $y_id = $is_unpack ? $name : unpack 'H*', $name;
	
	open my $fh, "< $userdir/$y_id/user.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません$y_id");
	my $line_data = <$fh>;
	my $line_info = <$fh>;
	close $fh;
	
	my($paddr, $phost, $pagent) = split /<>/, $line_info;
	
	my %you_datas = (
		addr	=> $paddr,
		host	=> $phost,
		agent	=> $pagent,
	);
	for my $hash (split /<>/, $line_data) {
		my($k, $v) = split /;/, $hash;
		next if $k =~ /^y_/;
		
		$you_datas{$k} = $v;
	}
	
	return %you_datas;
}
#================================================
# 相手ﾃﾞｰﾀ変更  結婚時と闘技場の熟練度UP時に使用
#================================================
# 使い方: &regist_you_data('相手の名前', '変更したい変数', '値');
sub regist_you_data {
	my($name, $k, $v) = @_;
	return if $name eq '' || $k eq '';
	
	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";
	
	if ($k eq 'lib' || $k eq 'value'){
		my %you_datas = &get_you_datas($y_id,1);
		if(($k eq 'lib' && $you_datas{lib} eq 'military' && $you_datas{tp} eq '610') || ($k eq 'value' && $you_datas{value} eq 'military_ambush')){
			my @lines = ();
			open my $fh, "+< $logdir/$you_datas{country}/patrol.cgi" or &error("$logdir/$you_datas{country}/patrol.cgiﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my($pat_time,$p_name) = split /<>/, $line;
				next if $p_name eq $name;
				push @lines, $line;
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	
	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	if(index($line, "<>$k;") >= 0){
		$line =~ s/<>($k;).*?<>/<>$1$v<>/;
	}else{
		$line = "$k;$v<>" . $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}
#================================================
# 相手ﾃﾞｰﾀ変更  結婚時と闘技場の熟練度UP時に使用
#================================================
# my @array = (['変更したい変数1', '値1'], ['変更したい変数2', '値2']);
# &regist_you_array('相手の名前', @array);
sub regist_you_array {
	my $name = shift;
	my @data = @_;
	return if $name eq '' || !@data;
	
	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	# 書き換え対象によっては待ち伏せを解除 1度やれば済むので2回目以降はなし
	my $bool = 0;
	for my $i (0 .. $#data) {
		last if $bool;
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if ($k eq 'lib' || $k eq 'value') {
			my %you_datas = &get_you_datas($y_id,1);
			if(($k eq 'lib' && $you_datas{lib} eq 'military' && $you_datas{tp} eq '610') || ($k eq 'value' && $you_datas{value} eq 'military_ambush')){
				$bool = 1;
				my @lines = ();
				open my $fh, "+< $logdir/$you_datas{country}/patrol.cgi" or &error("$logdir/$you_datas{country}/patrol.cgiﾌｧｲﾙが開けません");
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($pat_time,$p_name) = split /<>/, $line;
					next if $p_name eq $name;
					push @lines, $line;
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}
		}
	}

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	for my $i (0 .. $#data) {
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if(index($line, "<>$k;") >= 0){
			$line =~ s/<>($k;).*?<>/<>$1$v<>/;
		}else{
			$line = "$k;$v<>" . $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}
#================================================
# 牢獄に追加
#================================================
sub add_prisoner {
	$mes .= "$m{name}は、敵国兵に取り囲まれ捕まってしまった!<br>";
	$mes .= "牢獄へ連行されます。次に行動できるのは$GWT分後です<br>";
	$m{lib} = 'prison';
	$m{renzoku_c} = $m{act} = 0;
	$m{tp} = 100;
	&wait;
	my $flag = 0;
	$flag = 1 if ($pets[$m{pet}][2] eq 'no_rescue');
	# 牢獄ﾘｽﾄに追加
	open my $fh, ">> $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi が開けません");
	print $fh "$m{name}<>$m{country}<>$flag<>\n";
	close $fh;
	
	require './lib/_bbs_chat.cgi';
	$this_file = "$logdir/$y{country}/bbs";
	my $w_name = ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) ? '名無し':$m{name};
	$in{comment} = "$m{mes_lose}【朗報】$w_nameが牢獄に連行されました";
	$bad_time = 0;
	&write_comment;
}
#================================================
# 国力が一番高い国
#================================================
sub get_most_strong_country {
	my $skip_my_county = shift;
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		if (!$skip_my_country) {
			next if $i eq $m{country};
			next if $i eq $union;
		}
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}
#================================================
# 一年ランキングデータ書き込み
#================================================
sub write_yran {
	my($data_name, $data_value, $is_add) = @_;
	&error("ﾌﾟﾚｲﾔｰﾃﾞｰﾀの書き込みに失敗しました") if !$data_name || !$data_value;
	# -------------------
	if ($data_name =~ /contr_.*/ && $w{year} !~ /[1-5]$/) {
		return;
	}
	
	my @lines = ();
	my $y_find = 0;
	my $find = 0;
	my $new_line = '';
	if(-e "$userdir/$id/year_ranking.cgi"){
		open my $fh, "< $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			my %ydata;
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				$ydata{$k} = $v;
				if($k eq 'year'){
					if($v != $w{year}){
						if($v >= $w{year} - 3){
							push @lines, $line;
						}
						last;
					}
				}
			}
			if($ydata{year} == $w{year} && $y_find == 0){
				$y_find = 1;
				if($ydata{$data_name}){
					$find = 1;
					if($is_add){
						$ydata{$data_name} += $data_value;
					}else {
						if($ydata{$data_name} < $data_value){
							$ydata{$data_name} = $data_value;
						}
					}
				}
				for my $key (keys(%ydata)){
					next if(!$key || !$ydata{$key});
					$new_line .= "$key;$ydata{$key}<>";
				}
			}
		}
		close $fh;
	}
	unless($y_find){
		$new_line = "year;$w{year}<>";
	}
	unless($find){
		$new_line .= "$data_name;$data_value<>";
	}
	push @lines, "$new_line\n";
	
	open my $fh, "> $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
	print $fh @lines;
	close $fh;
}
#================================================
# 一年ランキングデータ書き込み
#================================================
sub write_yran2 {
	my @data = @_;
	my $size = 3;
	my $count = @data / $size - 1;

	my @lines = ();
	my $new_line = '';
	if(-e "$userdir/$id/year_ranking.cgi"){
		open my $fh, "< $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			# 過去3年よりも古いデータは削除
			if ($line =~ /year;(.*?)<>/ && $1 ne $w{year}) {
				push @lines, $line if $1 >= $w{year} - 3;
				next;
			}
			$line =~ tr/\x0D\x0A//d;
			$new_line = $line if index($line, "year;$w{year}") > -1;
		}
		close $fh;
	}

	if ($new_line) { # 今年のデータがある
		for my $i (0 .. $count) {
			my ($data_name, $data_value, $is_add) = ($data[$i*$size+0], $data[$i*$size+1], $data[$i*$size+2]);
			# 対象の要素が存在するなら書き換える
			if ($new_line =~ /$data_name;(.*?)<>/) {
				my $value = $is_add
					? $1 + $data_value # 累計記録
					: ($1 < $data_value ? $data_value : $1) ; # 最高記録
				$new_line =~ s/$data_name;.*?<>/$data_name;$value<>/;
			}
			# 対象の要素が存在しないなら書き足す
			else {
				$new_line .= "$data_name;$data_value<>";
			}
		}
	}
	else { # 今年のデータがない
		$new_line = "year;$w{year}<>";
		for my $i (0 .. $count) {
			my ($data_name, $data_value) = ($data[$i*$size+0], $data[$i*$size+1]);
			$new_line .= "$data_name;$data_value<>";
		}
	}

	push @lines, "$new_line\n";
	open my $fh, "> $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
	print $fh @lines;
	close $fh;
}
#================================================
# 国貢献集計
#================================================
sub summary_contribute {
	return if $w{year} !~ /[1-6]$/;
	return unless (-e "$userdir/$id/year_ranking.cgi");

	my %action_log = ();
	my @lines = ();
	open my $fh, "< $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my $new_line = '';
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			if ($k =~ /contr_(.*)/) {
				$action_log{$1} += $v;
				$v = 0;
			}
			$new_line .= "$k;$v<>";
		}
		push @lines, "$new_line\n";
	}
	close $fh;

	open my $fh, "> $userdir/$id/year_ranking.cgi" or &error("ﾌｧｲﾙが開けません");
	print $fh @lines;
	close $fh;

	unless (-e "$logdir/action_log_country_$m{country}.cgi") {
		open my $fht, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
		print $fht "\n";
		close $fht;
	}
	
	open $fh1, "< $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
	$line = <$fh1>;
	$line =~ tr/\x0D\x0A//d;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} += $v;
	}
	close $fh1;

	for my $k (keys(%action_log)) {
		$nline .= "$k;$action_log{$k}<>";
	}

	open $fh1, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgiが開けません");
	print $fh1 "$nline\n";
	close $fh1;
}

#================================================
# 直営店没収
#================================================
sub confiscate_shop {
	my ($guild, $c_force) = @_;
	$guild = 1 unless $guild;
	my $value_flie = $logdir . '/bbs_akindo_' . $guild . '_value.cgi';
	my $member_file = $logdir . '/bbs_akindo_' . $guild . '_allmember.cgi';
	my $g_shop_file = $logdir . '/guild_shop' . $guild . '.cgi';
	my $g_sale_file = $logdir . '/guild_shop' . $guild . '_sale.cgi';
	open my $fhv, "< $value_flie" or &error("$value_flie価格ﾘｽﾄﾌｧｲﾙが開けません");
	my $w_line = <$fhv>;
	my @v_weapon = split /<>/, $w_line;
	my $e_line = <$fhv>;
	my @v_egg = split /<>/, $e_line;
	my $p_line = <$fhv>;
	my @v_pet = split /<>/, $p_line;
	close $fhv;
	
	open my $fha, "< $member_file" or &error("$member_file が開けません");
	my $headline = <$fha>;
	while (my $line = <$fha>) {
		my($mname, $vote, $master) = split /<>/, $line;
		next unless $mname;
		my $id = unpack 'H*', $mname;
		my @lines = ();
		if(-f "$userdir/$id/shop.cgi"){
			open my $fhs, "+< $userdir/$id/shop.cgi" or &error("$userdir/$id/shop.cgi が開けません");
			eval { flock $fhs, 2; };
			while (my $line = <$fhs>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
				my @mpr = $kind == 1 ? @v_weapon:
							$kind == 2 ? @v_egg:
										@v_pet;
				if ($mpr[$item_no] < 9999999 && $price < $mpr[$item_no] && (($kind == 1 && $item_lv == 0) || $item_c == 0)) {
					my @shop_items = ();
					open my $in, "< $g_shop_file" or &error("$g_shop_fileが読み込めません");
					push @shop_items, $_ while <$in>;
					close $in;
					my($last_no) = (split /<>/, $shop_items[-1])[0];
					++$last_no;
					
					open my $fh2, ">> $g_shop_file" or &error("$g_shop_fileが開けません");
					print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$mpr[$item_no]<>\n";
					close $fh2;
				}else {
					push @lines, $line;
				}
			}
			seek  $fhs, 0, 0;
			truncate $fhs, 0;
			print $fhs @lines;
			close $fhs;
		}
	}
	close $fha;
	
	if($c_force){
		open my $fh2, "< $g_sale_file" or &error("売上ﾌｧｲﾙが開けません");
		my $line2 = <$fh2>;
		my($guild_c, $guild_money, $g_update_t) = split /<>/, $line2;
		close $fh2;
	
		open my $fho, "< $logdir/shop_list.cgi" or &error("$member_file が開けません");
		my $headline = <$fho>;
		while (my $line = <$fho>) {
			my($shop_name, $mname, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
			next unless $mname;
			next if $guild_number == $guild;
			my $sid = unpack 'H*', $mname;
			my @lines = ();
			if(-f "$userdir/$sid/shop.cgi"){
				open my $fhs, "+< $userdir/$sid/shop.cgi" or &error("$userdir/$sid/shop.cgi が開けません");
				eval { flock $fhs, 2; };
				while (my $line = <$fhs>) {
					my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
					my @mpr = $kind == 1 ? @v_weapon:
								$kind == 2 ? @v_egg:
											@v_pet;
					if ($mpr[$item_no] < 9999999 && $price < $mpr[$item_no] && (($kind == 1 && $item_lv == 0) || $item_c == 0) && $guild_money > $price) {
						my @shop_items = ();
						open my $in, "< $g_shop_file" or &error("$g_shop_fileが読み込めません");
						push @shop_items, $_ while <$in>;
						close $in;
						my($last_no) = (split /<>/, $shop_items[-1])[0];
						++$last_no;
						
						open my $fh2, ">> $g_shop_file" or &error("$g_shop_fileが開けません");
						print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$mpr[$item_no]<>\n";
						close $fh2;
						
						$guild_money -= $price;
						my $item_name = $kind eq '1' ? $weas[$item_no][1]
									  : $kind eq '2' ? $eggs[$item_no][1]
									  :				   $pets[$item_no][1]
									  ;
						&send_money($mname, "【$shop_name($item_name)】ギルド", $price, 1);
						
						open my $fh3, "+< $userdir/$sid/shop_sale.cgi" or &error("売上ﾌｧｲﾙが開けません");
						eval { flock $fh3, 2; };
						my $line2 = <$fh3>;
						my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
						$sale_money += $price;
						seek  $fh3, 0, 0;
						truncate $fh3, 0;
						print $fh3 "$sale_c<>$sale_money<>$update_t<>";
						close $fh3;
					}else {
						push @lines, $line;
					}
				}
				seek  $fhs, 0, 0;
				truncate $fhs, 0;
				print $fhs @lines;
				close $fhs;
			}
		}
		
		open my $fh2, "> $g_sale_file" or &error("売上ﾌｧｲﾙが開けません");
		print $fh2 "$guild_c<>$guild_money<>$g_update_t<>\n";
		close $fh2;
	}
}
#================================================
# 常時発動イベント
#================================================
sub alltime_event {
	if ($w{world} eq '20') {
		my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
		if ($hour >= 6 && $hour <= 18) {
			if (rand(100000) < 1) {
				for my $i (1..$w{country}) {
					for my $j ($i+1..$w{country}) {
						$w{"f_${i}_${j}"} = int(rand(20));
						$w{"p_${i}_${j}"}=2;
					}
				}
				&write_cs;
				&write_world_news("<b>世界中に隕石が降り注いできた</b>");
			}
		} else {
			if (rand(10000) < 1) {
				for my $i (1..$w{country}) {
					for my $j ($i+1..$w{country}) {
						unless ($w{"p_${i}_${j}"} == 1) {
							$w{"f_${i}_${j}"} = int(rand(20));
							$w{"p_${i}_${j}"} = 2;
						}
					}
				}
				&write_cs;
				&write_world_news("<b>花火大会開始のお知らせ</b>");
			}
		}
	}
	if (($w{world} eq '12') || ($w{world_sub} eq '12')) {
		if (rand(2500) < 1) {
			&disaster(1);
			&write_cs;
		}
	}
	if ($w{world} eq $#world_states-4) {
		if (rand(1000) < 1) {
			require './lib/fate.cgi';
			&super_attack('random');
		}
	}
	&debug_log("$m{lib}:$m{tp}", 'play_log');
}

#================================================
# login.cgi→bj.cgi
# ログインしユーザーデータの取得後、真っ先に呼び出される
#================================================
sub before_bj {
	my($lmin,$lhour,$lmday,$lmon,$lyear) = (localtime($m{ltime}))[1..5];
	my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..5];

	# その日最初のアクセスなら
	if ($lmday ne $tmday || $lmon ne $tmon || $lyear ne $tyear) {
		# 誕生日プレゼント
		my %datas = ();
		open my $fh, "< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgiﾌｧｲﾙが開けません");
		my $line = <$fh>;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$datas{$k} = $v;
		}
		close $fh;

		if ($datas{birthday} && $datas{birthday} =~ /(\d{4})\/(\d{2})\/(\d{2})/) {
			if ($tmon + 1 == $2 && $tmday == $3) {
				$mes .= "Happy Birthday $m{name}!!<br>誕生日おめでとう!!<br>";
				require './lib/shopping_offertory_box.cgi';
				my $gvar = $m{sedai};
				if ($m{start_time} + 30 * 24 * 60 * 60 < $time) {
					$gvar += 7;
				}
				&get_god_item($gvar);
			}
		}
	}

	if (&on_summer) {
		if (rand(100) < 1) {
			$mes .= "おじさん「君、おじさんの投票権をあげよう」<br>";
			$m{pop_vote}++;
		}
	}
}

#================================================
# 各国設定値取得
#================================================
sub get_modify {
	my $var = shift;
	my $modify = $cs{'modify_' . $var}[$m{country}] <= 0 ? ($var eq 'pro' ? 1.0 + 0.05 * $cs{'modify_' . $var}[$m{country}] : 1.0 + 0.1 * $cs{'modify_' . $var}[$m{country}]):
				$cs{'modify_' . $var}[$m{country}] <= 5 ? (1.0 + 0.04 * $cs{'modify_' . $var}[$m{country}]):
													(1.1 + 0.02 * $cs{'modify_' . $var}[$m{country}]);
	return $modify;
}

#================================================
# 新規数カウント
#================================================
sub refresh_new_commer {
	for my $i (1..$w{country}) {
		$cs{new_commer}[$i] = 0;
	}
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $uid = readdir $dh) {
		next if $uid =~ /\./;
		next if $uid =~ /backup/;
		my %datas = &get_you_datas($uid, 1);
		if ($datas{sedai} == 1) {
			$cs{new_commer}[$datas{country}]++;
		}
	}
	closedir $dh;
	
	&write_cs;
}

#================================================
# 国追加
#================================================
sub create_country {
	$w{country}++;
	my $max_c = int($w{player} / $w{country}) + 3;
	
	my $num = rmtree("$logdir/$w{country}");
	mkdir "$logdir/$w{country}" or &error("$logdir/$w{country} ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$w{country}";
	for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
		my $output_file = "$logdir/$w{country}/$file_name.cgi";
		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		if ($file_name eq 'depot') {
			print $fh "1<>1<><>\n";
		}
		close $fh;
		chmod $chmod, $output_file;
	}
	for my $file_name (qw/leader member/) {
		my $output_file = "$logdir/$w{country}/$file_name.cgi";
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		close $fh;
		chmod $chmod, $output_file;
	}
	&add_npc_data($w{country});
	# create union file
	for my $j (1 .. $w{country}-1) {
		# まだ滅亡してたら強制復興
		if ($cs{is_die}[$j]) {
			$cs{is_die}[$j] = 0;
			--$w{game_lv};
		}
		
		
		my $file_name = "$logdir/union/${j}_$w{country}";
		$w{ "f_${j}_$w{country}" } = int(rand(100));
		$w{ "p_${j}_$w{country}" } = 0;

		next if -f "$file_name.cgi";
		open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
		close $fh;
		chmod $chmod, "$file_name.cgi";
		open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
		close $fh2;
		chmod $chmod, "${file_name}_log.cgi";
		open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
		close $fh3;
		chmod $chmod, "${file_name}_member.cgi";
	}
	unless (-f "$htmldir/$w{country}.html") {
		open my $fh_h, "> $htmldir/$w{country}.html" or &error("$htmldir/$w{country}.html ﾌｧｲﾙが作れません");
		close $fh_h;
	}
	$cs{name}[$w{country}]     = "$m{name}の国";
	$cs{color}[$w{country}]    = '#ffffff';
	$cs{member}[$w{country}]   = 0;
	$cs{win_c}[$w{country}]    = 999;
	$cs{tax}[$w{country}]      = 99;
	$cs{strong}[$w{country}]   = 4999;
	$cs{food}[$w{country}]     = 0;
	$cs{money}[$w{country}]    = 0;
	$cs{soldier}[$w{country}]  = 0;
	$cs{state}[$w{country}]    = 0;
	$cs{capacity}[$w{country}] = $max_c;
	$cs{is_die}[$w{country}]   = 1;
	my @lines = &get_countries_mes();
	if ($w{country} > @lines - 1) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "<>$default_icon<>\n";
		close $fh9;
	}
	
	&write_cs;
}
# NPCデータ作成
sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]属性[1]武器No	[2]必殺技
		['無', [0],			[61..65],],
		['剣', [1 .. 5],	[1 .. 5],],
		['槍', [6 ..10],	[11..15],],
		['斧', [11..15],	[21..25],],
		['炎', [16..20],	[31..35],],
		['風', [21..25],	[41..45],],
		['雷', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) 亀の家庭医学(NPC) pigure(NPC) ウェル(NPC) vipqiv(NPC) DT(NPC) ハル(NPC) アシュレイ(NPC) ゴミクズ(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}
#================================================
# 国削除
# $target_country 0（ﾈﾊﾞﾗﾝ）から始まる国番号
# $mode 削除された国に属していた人の仕官先 0 でﾈﾊﾞﾗﾝ 1 でﾈﾊﾞﾗﾝ除くﾗﾝﾀﾞﾑ
#================================================
sub delete_country {
	my ($target_country, $mode) = @_;
	
	require "./lib/move_player.cgi";
	my %members = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %p = &get_you_datas($pid, 1);
		
		if ($p{country} > $target_country) {
			if ($p{name} ne $m{name}) {
				&move_player($line, $p{country}, $p{country} - 1);
				&regist_you_data($p{name}, 'country', $p{country} - 1);
			} else {
				$m{country} = $m{country} - 1;
			}
			$p{country} = $p{country} - 1;
		} elsif ($p{country} == $target_country) {
			my $to_country = $mode ? int(rand($w{country}-1)+1) : 0;
			if ($p{name} ne $m{name}) {
				&move_player($line, $p{country}, $to_country);
				&regist_you_data($p{name}, 'country', $to_country);
			} else {
				$m{country} = $to_country;
			}
			$p{country} = $to_country;
		}
		if ($m{lib} eq 'prison') {
			&regist_you_data($p{name}, 'lib', '');
		}
		&regist_you_data($p{name}, 'random_migrate', '');

		push @{ $members{$p{country}} }, "$p{name}\n";
	}
	for my $i (0 .. $w{country}) {
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
	}

	for my $i ($target_country+1 .. $w{country}) {
		
		my @keys_cs = (qw/
			name strong tax food money soldier state is_die member capacity color
			win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
			modify_war modify_dom modify_mil modify_pro
		/);
		for my $k (@keys_cs) {
			$cs{$k}[$i - 1] = $cs{$k}[$i];
		}
		
		
		for my $j (1 .. $w{country}) {
			for my $k ($j+1 .. $w{country}) {
				my $nj = $j >= $i ? $j-1 : $j;
				my $nk = $k >= $i ? $k-1 : $k;
				my $f_c_c  = "f_${j}_${k}";
				my $p_c_c = "p_${j}_${k}";
				my $nf_c_c  = "f_${nj}_${nk}";
				my $np_c_c = "p_${nj}_${nk}";
				$w{$nf_c_c} = $w{$f_c_c};
				$w{$np_c_c} = $w{$p_c_c};
			}
		}
		my $im1 = $i - 1;
		my $from = "$logdir/$i";
		my $to = "$logdir/$im1";
		rcopy($from, $to);
	}
	
	my @lines = ();
	$country_mes_i = 0;
	open my $fh, "+< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgiﾌｧｲﾙが読み込めません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$country_mes_i++;
		next if $target_country == $country_mes_i;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	my $num = rmtree("$logdir/$w{country}");

	--$w{country};
}
#================================================
# データ修正
#================================================
sub cs_data_repair{
	&read_cs;
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %p = &get_you_datas($pid, 1);
		
		if ($p{country} > $w{country}) {
			if ($p{name} ne $m{name}) {
				&regist_you_data($p{name}, 'country', 0);
			} else {
				$m{country} = 0;
			}
			$p{country} = 0;
		}

		push @{ $members{$p{country}} }, "$p{name}\n";
		++$count;
	}
	closedir $dh;
	$w{player} = $count;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;

		for my $k (qw/dom war mil pro/) {
			if ($cs{$k}[$i] eq '') {
				$cs{$k . '_c'}[$i] = 0;
			}
		}
	}
	&write_cs;
}
#================================================
# 相場ビッグデータ
#================================================
sub sale_data_log {
	my ($kind, $item_no, $item_c, $item_lv, $price, $place) = @_;
	
	my $sale_data_file = "$logdir/shop_big_data.cgi";
	open my $fh, ">> $sale_data_file" or &error("$sale_data_fileが開けません");
	print $fh "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$place<>$time<>\n";
	close $fh;
}
#================================================
# 相場ビッグデータ取得
#================================================
sub get_sale_data_log {
	my ($k, $n) = @_;
	my @lines = ();
	
	my $sale_data_file = "$logdir/shop_big_data.cgi";
	open my $fh, "< $sale_data_file" or &error("$sale_data_fileが開けません");
	while (my $line = <$fh>) {
		my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
		if (($kind eq $k && $item_no eq $n) || (!$k && !$n)) {
			push @lines, $line;
		}
	}
	close $fh;
	
	return @lines;
}
#================================================
# 相場ビッグデータHTML出力
#================================================
sub create_sale_data_chart {
	my ($k, $n) = @_;
	my @lines = &get_sale_data_log($k, $n);
	
	if (@lines > 1) {
		my @data_lines = @lines;
		while (@lines > 30) {
			shift @lines;
		}
		
		@lines = map { $_->[0] } sort { $a->[5] <=> $b->[5] } map { [$_, split /<>/ ]} @lines;
		my $max_price = (split /<>/, $lines[-1])[4];
		my $min_price = (split /<>/, $lines[0])[4];
		
		if ($max_price == $min_price) {
			$max_price++;
		}
		
		@lines = map { $_->[0] } sort { $a->[7] <=> $b->[7] } map { [$_, split /<>/ ]} @lines;
		my $max_time = (split /<>/, $lines[-1])[6];
		my $min_time = (split /<>/, $lines[0])[6];
		
		if ($max_time == $min_time) {
			$max_time++;
		}
		
		my @x = ();
		my @y = ();
		
		my $c_str = $k eq '1' ? '耐久値':
				$k eq '2' ? '孵化値':
				$k eq '3' ? '★':
							'';
		
		my $lv_str = $k eq '1' ? '★':
				$k eq '2' ? '':
				$k eq '3' ? '':
							'';
		
		my $csv = "時間,金額,種別,$c_str,$lv_str\n";
		my $price_table = "<table><tr><th>時間</th><th>金額</th><th>種別</th><th>$c_str</th><th>$lv_str</th></tr>";
		for my $line (@lines) {
			my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
			push @x, (($i_time - $min_time) / ($max_time - $min_time) * 100);
			push @y, (($price - $min_price) / ($max_price - $min_price) * 100);
		}
		for my $line (@data_lines) {
			my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
			my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($i_time);
			$year += 1900;
			$mon++;
			my $time_str = "$year年$mon月$mday日 $hour時$min分$sec秒";
			my $time_str_csv = "$year-$mon-$mday $hour:$min:$sec";
			my $type_str = $place eq '1' ? '商人の店':
							$place eq '2' ? 'ｵｰｸｼｮﾝ':
							$place eq '3' ? 'ｵｰｸｼｮﾝ（即決）':
							$place eq '4' ? 'ｼﾞｬﾝｸｼｮｯﾌﾟ':
											'破棄等'; 
			$price_table .= "<tr><td>$time_str</td><td>$price</td><td>$type_str</td><td>$item_c</td><td>$item_lv</td></tr>";
			$csv .= "$time_str_csv,$price,$type_str,$item_c,$item_lv\n";
		}
		$price_table .= '</table>';
		
		my $chdx = join ',', @x;
		my $chdy = join ',', @y;
		my $item_title = &get_item_title($k, $n);;
		$csv = $item_title . "\n" . $csv;
		# CSVﾌｧｲﾙ作成
		my $csv_file = "./html/item_$k" . "_" . "$n.csv";
		open my $out_csv, "> $csv_file";
		print $out_csv $csv;
		close $out_csv;
		
		my $html = '';
		$html .= qq|<html><head>|;
		$html .= qq|<meta http-equiv="Pragma" content="no-cache">|;
		$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
		$html .= qq|<meta http-equiv="Expires" content="0">|;
		$html .= qq|<title>$title</title>|;
		$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		$html .= qq|</head><body $body>|;
		$html .= qq|<p>更新日時 $date</p>|;
		$html .= qq|<hr size="1"><h1>$cs{name}[$country]</h1>|;
		$html .= qq|<hr size="1"><h1>$world_name$item_title相場</h1>|;
		$html .= qq{<img src="http://chart.apis.google.com/chart?cht=lxy&chs=500x350&chxt=y&chxl=0:|$min_price|$max_price}
			  .  qq{&chd=t:$chdx|$chdy">};
		$html .= qq|<br>$price_table|;
		$html .= qq|<br><a href="item_${k}_${n}.csv">csvファイルダウンロード</a>|;
		$html .= qq|<br><div align="right" style="font-size:11px">|;
		$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama楽.net</a><br>|;  # 著作表示:削除・非表示 禁止!!
		$html .= qq|$copyright|;
		$html .= qq|</div></body></html>|;
		
		# HTMLﾌｧｲﾙ作成
		my $html_file = "./html/item_$k" . "_" . "$n.html";
		open my $out, "> $html_file";
		print $out $html;
		close $out;
	}
}

#================================================
# 階級名取得
#================================================
sub get_rank_name {
	my($rank, $name) = @_;
	my $is_ceo = 0;
	if ($name) {
		for my $i (1..$w{country}) {
			if ($name eq $cs{ceo}[$i]) {
				$is_ceo = 1;
			}
		}
	}
	if ($rank == $#ranks && $is_ceo) {
		return '皇帝';
	}
	return $ranks[$rank];
}

#================================================
# アイテム名取得
# 第１引数と第２引数だけで名前
# 第３引数まででﾍﾟｯﾄだけ★情報追加 ｼﾞｬﾝｸでﾍﾟｯﾄだけ★情報使うので
# 第４引数まで指定すると全アイテム情報追加
# 第５引数はアイテムの種類を非表示 ショップなど一部では種類が非表示なので
# $kind アイテムの種類(1武器 2卵 3ﾍﾟｯﾄ 4防具)
# $item_no アイテムの番号
# $item_c アイテムが持つ数値(耐久値 孵化値 ★ なし)
# $item_lv アイテムのレベル(★ なし なし なし)
# $flag 1 で種類表示オフ
# 新しいアイテム種を追加したらここを変更すること
#================================================
sub get_item_name {
	my($kind, $item_no, $item_c, $item_lv, $flag) = @_;

	my $result;
	if (defined($item_lv)) { # 全引数有効ならアイテム情報
		$result = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : $kind eq '3' ? "[ぺ]$pets[$item_no][1]★$item_c"
				  :                "[$guas[$item_no][2]]$guas[$item_no][1]"
			  ;
		$result = substr($result, 4) if $flag; # $flag が有効ならアイテム種を非表示
	}
	else { # 全引数有効じゃないならアイテム名
		$result = $kind eq '1' ? "$weas[$item_no][1]"
				  : $kind eq '2' ? "$eggs[$item_no][1]"
				  : $kind eq '3' ? (defined($item_c) ? "$pets[$item_no][1]★$item_c" : "$pets[$item_no][1]") # 第３引数有効かつﾍﾟｯﾄならレベル付加
				  :                "$guas[$item_no][1]"
				  ;
	}
	return $result;
}

#================================================
# アイテム名取得（相場表で使うアイテムのタイトル用…）
#================================================
sub get_item_title {
	my($kind, $item_no) = @_;

	my $result;
	$result = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]"
			  : $kind eq '2' ? "[卵]$eggs[$item_no][1]"
			  : $kind eq '3' ? "[ペ]$pets[$item_no][1]"
			  :                "[$guas[$item_no][2]]$guas[$item_no][1]"
			  ;
	return $result;
}

#================================================
# Twitterボット
#================================================
sub twitter_bot {
	require "$datadir/twitter_bots.cgi";
#	my $mes = &{$twitter_bots[$w{twitter_bot}]};
	my $mes = &{$twitter_bots[int(rand(@twitter_bots))]};
	&send_twitter($mes);
#	$w{twitter_bot}++;
#	if ($w{twitter_bot} >= @twitter_bots) {
#		$w{twitter_bot} = 0;
#	}
#	&write_cs;
}

1; # 削除不可
