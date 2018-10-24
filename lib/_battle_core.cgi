require "$datadir/skill.cgi";
$is_battle = 1; # ﾊﾞﾄﾙﾌﾗｸﾞ1
#================================================
# 戦闘 Created by Merino
#================================================

#ﾈｺﾐﾐ問題
#　ﾈｺﾐﾐ相手に技を避けられるとこっちの一部の技はMP消費なしで効果が発揮される
#　逆にｾﾙﾊﾞなど相手に当たることを前提としない技は効果も発揮しない
#　そもそもﾈｺﾐﾐ避けすぎな気もする
#　諸々の問題を含め、攻撃ﾌﾗｸﾞを共用してるのがやりにくい

# 武器による優劣
my %tokkous = (
# '強い属性' => qr/弱い属性/,
	'剣' => qr/斧/銃,
	'斧' => qr/槍/銃,
	'槍' => qr/剣/銃,
	'炎' => qr/風|無/,
	'風' => qr/雷|無/,
	'雷' => qr/炎|無/,
	'無' => qr/剣|斧|槍/銃,
	'銃' => qr/炎|風|雷/無,
);

#================================================
# 使う値を Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# 画面表示やｽｷﾙで使うのでｸﾞﾛｰﾊﾞﾙ変数
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$m_mdf= $m{mdf};
$y_df = $y{df};
$y_mdf= $y{mdf};
$m_ag = $m{ag};
$y_ag = $y{ag};

if    ($guas[$m{gua}][2] =~ /無|剣|斧|槍/) { $m_df += $guas[$m{gua}][3]; }
elsif ($guas[$m{gua}][2] =~ /炎|風|雷/銃)    { $m_mdf+= $guas[$m{gua}][3]; }
if    ($guas[$y{gua}][2] =~ /無|剣|斧|槍/) { $y_df += $guas[$y{gua}][3]; }
elsif ($guas[$y{gua}][2] =~ /炎|風|雷/銃)    { $y_mdf+= $guas[$y{gua}][3]; }
# 使用するのは AT or MAT, DF or MDF のどちらか
if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /炎|風|雷/銃)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y_mdf; }
if    ($weas[$y{wea}][2] =~ /無|剣|斧|槍/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /炎|風|雷/銃)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m_mdf; }

$m_ag -= $guas[$m{gua}][5];
$m_ag -= $weas[$m{wea}][5] if $guas[$m{gua}][0] ne '7';
$m_ag = int(rand(5)) if $m_ag < 1;

$y_ag -= $guas[$y{gua}][5];
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea}, $y{wea})) {
		$m_at = int(1.5 * $m_at);
		$y_at = int(0.75 * $y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}
# 武器と防具の相性設定(攻撃力)
# 素手vs防具あり 0.3倍 素手vs防具なし 1.0倍
# 武器vs防具なし 1.0倍 武器vs防具属性違い 1.0倍 武器vs防具属性同じ 0.5倍
# 素手で防具持ち殴ったら下方修正同様、武器で防具なし殴ったら上方修正とかはしないの？ 素手不利で相対的に武器持ち有利とも言えるけど
if ($y{gua}) {
	if ($m{wea}) {
		if (&is_gua_valid($y{gua},$m{wea})) {
			$m_at = int(0.5 * $m_at);
			$is_y_tokkou2 = 1;
		}
	}
	else {
		$m_at = int(0.3 * $m_at);
		$is_y_tokkou2 = 1;
	}
}
#else {
#	$m_at = int($m_at * 1.2) if $m{wea};
#}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})) {
			$y_at = int(0.5 * $y_at);
			$is_m_tokkou2 = 1;
		}
	} else {
		$y_at = int(0.3 * $y_at);
		$is_m_tokkou2 = 1;
	}
}
#else {
#	$y_at = int($y_at * 1.2) if $y{wea};
#}

#================================================
# ﾒｲﾝ動作
#================================================
&run_battle2;
#&run_battle;

&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# 実行処理
#================================================
sub run_battle2 {
	if ($cmd eq '') {
		$mes .= '戦闘ｺﾏﾝﾄﾞを選択してください<br>';
	}
	elsif ($m{turn} >= 20) { # なかなか決着つかない場合
		$mes .= '戦闘限界ﾀｰﾝを超えてしまった…これ以上は戦えません<br>';
		&lose;
	}
	else {
		# 無改造と違ってターン順を無視して効果を発揮する処理が実装されている
		# 先攻・後攻どちらを優先して処理するか以前に両方のフラグ管理を行う

		# まず自分と相手の攻撃・必殺技判定 $m_s が未定義なら自分、$y_s が未定義なら相手は攻撃
		local $m_s = undef; # ﾌﾟﾚｲﾔｰの技データが入る 未定義なら攻撃
		local $pikorin; # ﾌﾟﾚｲﾔｰが技を閃いたか 1 閃いた 0 閃いてない
		if (!$metal) { # ﾒﾀﾙ相手には常に攻撃で必殺技も閃かない
			$m_s = $skills[ $m_skills[ $cmd - 1 ] ] if $cmd > 0 && $guas[$m{gua}][0] ne '21'; # 1ｺﾏﾝﾄﾞ以上を入力していて狂戦士の鎧じゃなくﾒﾀﾙ相手じゃないなら必殺技
			$m_s = undef if defined($m_s) && ($weas[$m{wea}][2] ne $m_s->[2] || !&m_mp_check($m_s)); # 必殺技を選択していても属性が違ったりMPが足りないなら攻撃
			# 技閃いてもフラグが立たない問題対策 フラグ自体は先攻後攻関係ないので予め閃き処理を済ませばフラグ立てられる
			$pikorin = &_learning if !defined($m_s); # 攻撃で技を閃いたならば 1 が返り、閃いた技は $m_s に入る
		}
		local $y_s = undef; # 敵の技データが入る 未定義なら攻撃
		$y_s = $skills[ $y_skills[ int(rand(6)) - 1 ] ] if $guas[$y{gua}][0] ne '21'; # 狂戦士の鎧じゃないなら必殺技
		$y_s = undef if defined($y_s) && ($weas[$y{wea}][2] ne $y_s->[2] || !&y_mp_check($y_s) || $metal); # 必殺技を選択していても属性が違ったりMPが足りないとかﾒﾀﾙなら攻撃

		# フラグをまず全部洗い出してから処理すれば変な挙動しなくなる
		# 例
		#   無効技をﾈｺﾐﾐで避けられるとMP消費せずに無効技を発揮できる
		#   ｽﾀﾝ技をﾔﾀﾉｶｶﾞﾐで返されても相手にｽﾀﾝ効果を与える
		# 戦闘は $who で自分と相手を切り替えてるのでそれ同様 $who でフラグ管理も切り替える

		local $who = '';
		$who = 'm';
		&get_battle_flags; # $m_is_guard, $m_is_stanch, ... などが入る skill.cgi 参照
		$who = 'y';
		&get_battle_flags; # $y_is_guard, $y_is_stanch, ... などが入る skill.cgi 参照

		# ここで防衛者の無効効果をオフにすれば無効技MP未消費バグ起きないはず
		# ただ、無効というよりﾈｺﾐﾐの高速移動で避けてるイメジが強すぎる(当てる気のない必殺技を避けても意味ない避けられないみたいな)のと、
		# 単純に無効が強いのでMP未消費バグ残ってるぐらいでちょうど良い気しかしない
		# $m_is_guard = 0 if $m_is_guard && $y_gua_avoid;
		# $y_is_guard = 0 if $y_is_guard && $m_gua_avoid;

		# ここで攻撃者のｽﾀﾝ効果をオフにすればｽﾀﾝ技反射バグ起きないはず
		# $m_is_stanch = 0 if $m_is_stanch && $y_gua_skill_mirror;
		# $y_is_stanch = 0 if $y_is_stanch && $m_gua_skill_mirror;

		# 基本的にプレイヤー不利になっているが、先攻後攻で分けるのも良いのでは？
		if ( rand($m_ag * 3) >= rand($y_ag * 3) ) { # プレイヤー先攻
			$who = 'm';
			my $v = &attack;
			if ($y{hp} <= 0 && $m{hp} > 0) { # ﾘｽｸﾀﾞﾒｰｼﾞで自分がHP0になっても敵の攻撃に移る↓
				&win; # ﾌﾟﾚｲﾔｰ先攻だからまずは勝利判定だと思われる
			}
			else {
				$who = 'y';
				&attack;
				if    ($m{hp} <= 0) { &lose; } # さらにﾘｽｸﾀﾞﾒｰｼﾞで相手がHP0になってもすでに自分はHP0なので負ける
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; } # ﾌﾟﾚｲﾔｰ先攻だから勝利判定先にしたら？
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		else { # NPC先攻
			$who = 'y';
			&attack;
			if ($m{hp} <= 0) { # ﾘｽｸﾀﾞﾒｰｼﾞで敵がHP0になってもこっちの攻撃に移る↓
				&lose; # NPC先攻だからまずは敗北判定だと思われる
			}
			else {
				$who = 'm';
				my $v = &attack;
				if    ($m{hp} <= 0) { &lose; } # さらにﾘｽｸﾀﾞﾒｰｼﾞでこっちがHP0になると負ける
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; }
					elsif ($y{hp} <= 0) { &win;  }
				}
			}
		}
		$m{turn}++;
	}
	$m{mp} = 0 if $m{mp} < 0;
	$y{mp} = 0 if $y{mp} < 0;
}

#=================================================
# 戦闘行動
#=================================================
sub attack {
	my $temp_y = $who eq 'm' ? 'y' : 'm'; # 攻撃側を「自分」とした場合の「相手」を設定
	my $temp_y_name = ${$temp_y}{name};
	my $skill = ${$who.'_s'} if defined(${$who.'_s'});

	if ($who eq 'm' && $pikorin) { # 従来ﾈｺﾐﾐ相手に攻撃して避けられると技を閃かなかった 閃くが当たらないに修正
		${$who.'_mes'} = "閃いた!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">☆閃き!!$m{name}の$m_s->[1]!!</font><br>|;
	}
	if ($who eq 'y' && $metal) {
		$mes .= "$y{name}は様子を見ている<br>";
		return;
	}
	if (${$temp_y.'_gua_avoid'}) { # 相手のﾈｺﾐﾐ判定
		$mes .= "$temp_y_nameはひらりと身をかわした<br>";
		return;
	}

	my $hit_damage = ${$temp_y}{hp}; # 与えたダメージを持つ
	if (defined($skill)) { # 必殺技
		if ($who eq 'm' && $pikorin) { # 従来通り閃いた技はMP消費もなければ無効技などのフラグ無視
			&{ $skill->[4] }($m_at);
		}
		else {
			# NPC側でｸﾜﾊﾞﾗのお守りが機能してない 強すぎるから？
			${$who}{mp} -= $who eq 'm' && $guas[${$who}{gua}][0] eq '6' ? int($skill->[3] / 2) : $skill->[3];
			${$who.'_mes'} = $skill->[5] ? "$skill->[5]" : "$skill->[1]!" unless ${$who.'_mes'};
			$mes .= "${$who}{name}の$skill->[1]!!<br>";
			if (${$temp_y.'_is_guard'}) { # 相手が無効技
				&{ $skill->[4] }(${$who.'_at'});
				${$temp_y}{hp} = $hit_damage;
			}
			elsif (${$temp_y.'_gua_skill_mirror'}) { # 相手が反射防具
				&{ $skill->[4] }(${$who.'_at'});
				${$who}{hp} -= $hit_damage - ${$temp_y}{hp};
				$mes .= "しかし$guas[${$temp_y}{gua}][1]が技を反射し ".($hit_damage - ${$temp_y}{hp})." のﾀﾞﾒｰｼﾞをうけました!!<br>";
				${$temp_y}{hp} = $hit_damage;
			}
			else {
				&{ $skill->[4] }(${$who.'_at'});
			}
		}
	}
	else { # 攻撃
		my $sc = 1;
		if ($guas[${$who}{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		}
		elsif ($guas[${$who}{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "${$who}{name}の攻撃!!";
			my $kaishin_flag = ${$who}{hp} < ${$who}{max_hp} * 0.25 && int(rand(${$who}{hp})) == 0; # 999->249.75 && 0～248 1/249
			$kaishin_flag = int(rand(${$who}{hp} / 10)) == 0 if $guas[${$who}{gua}][0] eq '8'; # 999->99.9 0～98 1/99 なんとなく1/3ぐらいで会心でもええんでないか
			my $gua_mes;
			my $m_at_bf = ${$who.'_at'};
			if ($guas[${$who}{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[${$who}{gua}][1]が駆動する!";
				${$who.'_at'} = int(${$who.'_at'} * 1.2);
			}
			elsif ($guas[${$who}{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[${$who}{gua}][1]が暴\走する!";
				${$who.'_at'} = int(${$who.'_at'} * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin(${$who.'_at'}) : &_attack_normal(${$who.'_at'}, ${$temp_y.'_df'});
			${$who.'_at'} = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if (${$temp_y.'_is_counter'}) {
				$mes .= "攻撃を返され $v のﾀﾞﾒｰｼﾞをうけました<br>";
				${$who}{hp} -= $v;
			}
			elsif (${$temp_y.'_is_stanch'}) {
				$mes .= "ｽﾀﾝで動けない!<br>";
			}
			else {
				$mes .= "$v のﾀﾞﾒｰｼﾞを";
				$mes .= $who eq 'm' ? 'あたえました<br>' : 'うけました<br>';
				if ($who eq 'm' && $m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wnameは壊れてしまった<br>" if $m{wea_c} == 0;
				}
				${$temp_y}{hp} -= $v;
			}
		}
	}
	$hit_damage -= ${$temp_y}{hp};

	# 送電服は受けたダメージで回復すると思ってたけど与えたダメージで回復する 分けて書いてあることから仕様と思われる
	# ｸﾜﾊﾞﾗは消費MP半減だから無効技連打でも恩恵受けられるが、送電服は与えたダメージに依存するのでｸﾜﾊﾞﾗほど恩恵受けないと思われる
	# 高魅力がｿｰﾗﾝ撃って運が良ければｸﾜﾊﾞﾗよりも効率は良いが…20から18,15とかにするのは？
	if ($guas[${$who}{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "あたえたﾀﾞﾒｰｼﾞから MP を $v 吸収しました<br>";
		${$who}{mp} += $v;
		${$who}{mp} = ${$who}{max_mp} if ${$who}{mp} > ${$who}{max_mp};
	}

	if (${$temp_y.'_gua_relief'} && $hit_damage) {
		my $v = int($hit_damage / 10);
		$mes .= "$v のﾀﾞﾒｰｼﾞを";
		$mes .= $who eq 'm' ? '防がれました<br>' : '防ぎました<br>';
		${$temp_y}{hp} += $v;
	}
	elsif (${$temp_y.'_gua_remain'} && $hit_damage && ${$temp_y}{hp} <= 0) {
		$mes .= "$guas[${$temp_y}{gua}][1]に攻撃が当たり奇跡的に致命傷を";
		$mes .= $who eq 'm' ? 'まぬがれられた<br>' : 'まぬがれた<br>';
		${$temp_y}{hp} = 1;
	}
	elsif (${$temp_y.'_gua_half_damage'} && $hit_damage) {
		$mes .= "$guas[${$temp_y}{gua}][1]がﾀﾞﾒｰｼﾞを半減させました<br>";
		${$temp_y}{hp} += int($hit_damage / 2);
	}
}

#=================================================
# 攻撃・防御ﾌﾗｸﾞ
#=================================================
sub get_battle_flags { # $who で切り替え $who = 'm' or $who = 'y'
	return if ($guas[${$who}{gua}][0] eq '21') && ($who ne 'm' || !$pikorin); # 狂戦士の鎧は攻撃強制 閃いてるなら狂戦士の鎧でも必殺技
	&{ ${$who.'_s'}->[6] } if defined(${$who.'_s'}); # 必殺技のﾌﾗｸﾞ
	&{ $guas[ ${$who}{gua} ]->[6] } if ${$who}{gua}; # 防具のﾌﾗｸﾞ
}

#=================================================
# 会心、通常攻撃
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>会心の一撃!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# 新技習得(すでに覚えている技でも発動) 習得で1、未習得で0
#=================================================
sub _learning {
	if (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		# 覚えられる属性のものを全て@linesに入れる
		my @lines = ();
		for my $i (1 .. $#skills) {
			push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
		}

		if (@lines) {
			my $no = $lines[int(rand(@lines))];
			# 覚えていない技なら追加
			my $is_learning = 1;
			for my $m_skill (@m_skills) {
				if ($m_skill eq $no) {
					$is_learning = 0;
					last;
				}
			}
			$m{skills} .= "$no," if $is_learning;
			@m_skills = split /,/, $m{skills};
			$m_s = $skills[ $no ];
			return 1;
		}
		else { # 例外処理：覚えられるものがない
			$m_mes = '閃めきそうで閃けない…';
		}
	}
	return 0;
}

#=================================================
# 戦闘用メニュー
#=================================================
sub battle_menu {
	if($is_smart){
		$menu_cmd .= qq|<table boder=0 cols=5 width=90 height=90>|;

		$menu_cmd .= qq|<tr><td><form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="submit" value="攻撃" class="button1s"><input type="hidden" name="cmd" value="0">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|</form>|;
		$menu_cmd .= qq|</td>|;

		for my $i (1 .. $#m_skills+1) {
			if($i % 5 == 0){
				$menu_cmd .= qq|<tr>|;
			}
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			my $mline;
			if(length($skills[ $m_skills[$i-1] ][1])>20){
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10,10). "\n" . substr($skills[ $m_skills[$i-1] ][1],20);
			}elsif(length($skills[ $m_skills[$i-1] ][1])>10) {
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10);
			}else{
				$mline = $skills[ $m_skills[$i-1] ][1];
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 5 == 4){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#m_skills % 5 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;
	}else{
		$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		$menu_cmd .= qq|<option value="0">攻撃</option>|;
		for my $i (1 .. $#m_skills+1) { # ｺﾏﾝﾄﾞ位置 配列要素位置は -1
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
		}
		$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|<input type="submit" value="決 定" class="button1"></form>|;
	}
}

#=================================================
# 勝利
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}を倒しました<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('battle');
	}

	$result = 'win';
}

#=================================================
# 敗北
#=================================================
sub lose {
	if ($m{name} eq 'nanamie' || $m{name} eq 'QE') {
#		&win;
#		return;
	}

	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}はやられてしまった…<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;

	$result = 'lose';
}

#=================================================
# 武器により特攻がつくかどうか
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}

#=================================================
# 防具が有効かどうか
#=================================================
sub is_gua_valid {
	my($gua, $wea) = @_;
	return $guas[$gua][2] eq $weas[$wea][2];
}

#=================================================
# MPがあるかどうか
#=================================================
sub m_mp_check {
	my $m_s = shift;
	return ($m{mp} >= $m_s->[3] || ($guas[$m{gua}][0] eq '6' && $m{mp} >= int($m_s->[3] / 2)));
}
sub y_mp_check {
	my $y_s = shift;
	return ($y{mp} >= $y_s->[3] || ($guas[$y{gua}][0] eq '6' && $y{mp} >= int($y_s->[3] / 2))); # 戦闘行動では効いてないがこっちはｸﾜﾊﾞﾗ効いてる
}

1; # 削除不可
