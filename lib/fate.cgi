use List::Util;
my $this_file = "$userdir/$id/super.cgi";
#=================================================
# 英雄
#=================================================
# 冷却期間
# 6時間から3時間に短縮 空打ちの時間だけを短縮したり 0 にするのは発動してない云々抜きに隠し必殺技狙いやすくなるだけ
# 単純に間隔短くした方がまだマシ 全体的に必殺技が大人しくなった気がしないでもないので倍撃てても問題ない気もするので半分に
$coolhour = $config_test ? 0 : 3;
$cooldown_time = $coolhour * 3600;
# トリガー
@triggers = (
#	[0]No	[1]名前			[2]type			[3]倍率	[4]選択可能	[5]発動率(%)
	[0,		'ﾏｲﾙｰﾑ',		'myroom',		0.1,	1,			100],
	[1,		'戦争勝利',		'war',			0.5,	1,			100],
	[2,		'軍事成功',		'military',		0.4,	1,			60],
	[3,		'偽計決裂',		'breakdown',	1,		0,			100],
	[4,		'外交成功',		'promise',		0.4,	1,			60],
	[5,		'宣戦布告',		'declaration',	0.8,	0,			80],
	[6,		'停戦条約',		'cessation',	0.6,	0,			80],
	[7,		'内政',			'domestic',		0.4,	1,			50],
	[8,		'戦闘勝利',		'battle',		0.3,	0,			20],
	[9,		'修行',			'training',		0.4,	0,			30],
	[10,	'討伐',			'hunting',		0.4,	0,			30],
	[11,	'闘技場',		'colosseum',	0.4,	0,			80],
	[12,	'一騎打ち',		'single',		1,		0,			100],
	[13,	'ｶｼﾞﾉ',			'casino',		0.2,	0,			1],
	[14,	'発言',			'voice',		0.2,	0,			10],
	[15,	'孵化',			'incubation',	0.3,	0,			100],
	[16,	'脱獄',			'prison',		0.5,	0,			100],
	[17,	'救出',			'rescue',		0.7,	0,			70],
	[18,	'闘技場優勝',	'colosseum_top',1,		0,			100],
	[19,	'ボス討伐',		'boss',			1,		0,			100],
	[20,	'暴発',			'random',		1,		0,			100],
);

=pod
# 無条件に発動できるようにしてトリガーの発動率をイジるなど 試してない
# トリガー
@triggers = (
#	[0]No	[1]名前			[2]type			[3]倍率	[4]選択可能	[5]発動率(%)
	[0,		'ﾏｲﾙｰﾑ',		'myroom',		0.1,	1,			100],
	[1,		'戦争勝利',		'war',			0.5,	1,			20],
	[2,		'軍事成功',		'military',		0.4,	1,			15],
	[3,		'偽計決裂',		'breakdown',	1,		0,			100],
	[4,		'外交成功',		'promise',		0.4,	1,			12],
	[5,		'宣戦布告',		'declaration',	0.8,	0,			30], # 停戦と違って能動的に布告できるから低め もっと低くても良さそうだけど適当で当たるから
	[6,		'停戦条約',		'cessation',	0.6,	0,			60], # 布告と違って受動的だから布告より高め
	[7,		'内政',			'domestic',		0.4,	1,			10],
	[8,		'戦闘勝利',		'battle',		0.3,	0,			20],
	[9,		'修行',			'training',		0.4,	0,			30],
	[10,	'討伐',			'hunting',		0.4,	0,			30],
	[11,	'闘技場',		'colosseum',	0.4,	0,			80],
	[12,	'一騎打ち',		'single',		1,		0,			100],
	[13,	'ｶｼﾞﾉ',			'casino',		0.2,	0,			1],
	[14,	'発言',			'voice',		0.2,	0,			10],
	[15,	'孵化',			'incubation',	0.3,	0,			100],
	[16,	'脱獄',			'prison',		0.5,	0,			100],
	[17,	'救出',			'rescue',		0.7,	0,			70],
	[18,	'闘技場優勝',	'colosseum_top',1,		0,			100],
	[19,	'ボス討伐',		'boss',			1,		0,			100],
	[20,	'暴発',			'random',		1,		0,			100],
);
=cut

=pod
# 黒豚鯖での仕様
# タイミング
@timings = (
#	[0]No	[1]名前							[2]条件		[3]倍率		[4]選択可能
	[0,		'任意',							sub{ return 1; },	0.1,	1],
	[1,		'滅亡時',						sub{ return $cs{is_die}[$m{country}]; },	0.5,	1],
	[1,		'ぼっちの時',						sub{ return !$union; },	0.12,	1], # ぼっち国は延々全国民が恩恵受ける訳だから倍率高くするとたぶん逆に一方的有利になりすぎる
	[2,		'国力ﾄｯﾌﾟ',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return 0; } } return 1; },	0.7,	0],
	[3,		'資源がすべて100000未満の時',	sub{ return ($cs{food}[$m{country}] < 100000 && $cs{money}[$m{country}] < 100000 && $cs{soldier}[$m{country}] < 100000); },	0.4,	1],
	[4,		'兵士が20000未満の時',			sub{ return $cs{soldier}[$m{country}] < 20000; },	0.6,	0],
	[5,		'兵士が999999の時',				sub{ return $cs{soldier}[$m{country}] >= 999999; },	0.8,	0],
	[6,		'代表の時',						sub{ return &is_daihyo; },	0.3,	1],
);
=cut

=pod
全体的に終盤泥沼化しそうな気がする

シナジー
同盟組む→同盟国がある時
ｴｸｽｶﾘﾊﾟｰ(ﾉｱ)→滅亡時
国力0滅亡→滅亡時・国力0時→ｴｸｽｶﾘﾊﾟｰ(国力+1)→国力1時
国力0滅亡→滅亡時・国力0時→ｳﾛﾎﾞ覚醒着弾・ﾍﾟｯﾄのｳﾛﾎﾞ→国力ｿﾞﾛ目時
国力0滅亡→滅亡時・国力0時→ｲｰｽﾀｰ→国力ｿﾞﾛ目時（国力+0～100なので11・22・33・44・55・66・77・88・99が当たるかもしれない）
ｳﾛﾎﾞ→ｳﾛﾎﾞ覚醒中
ｴｸｽｶﾘﾊﾟｰ(国力+1)→国力%5・国力ｿﾞﾛ目
ｴｸｽｶﾘﾊﾟｰ(難易度+1)→統難%5
ｾﾞｳｽ→国力%3・統国%4
ﾌｪﾝﾘﾙ→国力%3
ﾊﾞﾙﾑﾝｸ→前期統一時
ﾛﾌﾟﾄ(物資減少)→FMS<10万
ﾛﾌﾟﾄ(統一難易度-1)→統難%5
ｴｸｽｶﾘﾊﾞｰ(与滅亡)→滅亡時
ｴｸｽｶﾘﾊﾞｰ(国力0)→国力0時
ｴｸｽｶﾘﾊﾞｰ(状態変更)→暴風・不況時
ｴｸｽｶﾘﾊﾞｰ(難易度上昇)→統難%5

効果量
統国ｿﾞﾛ目		4			選択可
国力ｿﾞﾛ目		3			選択不可		意図してるとはいえｲｽﾀとｴｸｽｶﾘﾊﾟｰとか終盤意外と狙える 倍率4から3に減らして選択不可に変更 代わりに統一国力ｿﾞﾛ目を追加
国力1				2			選択可		国力1が機能しすぎると三国志みたいに泥沼になりそうな予感がするので倍率3から2に減らした
ぼっち			1.25		選択不可
ウロボ			1.2		選択可		ｳﾛﾎﾞ自体が強いからさらに条件に加えると凶悪？
回数>20			1.02		選択不可
国力0				1			選択不可
トップ			0.7		選択不可
回数%11			0.62		選択可		ここら辺の倍率でも選択可が欲しいと思って非効率な感じで定義 前期から連続を溜めておけるがそんぐらい良いか
SOL<2万			0.6		選択不可
SOL満				0.6		選択不可
統国%3			0.6		選択不可
回数>9			0.56		選択不可
統難%5			0.43		選択可
FMS<10万			0.4		選択可
前期統一			0.38		選択不可
滅亡時			0.35		選択可
国力%50			0.35		選択不可
ビリ				0.34		選択可
代表時			0.32		選択可
回数>4			0.28		選択可
独身時			0.27		選択可
暴・不			0.26		選択可
国力%12			0.25		選択可
回数%3			0.22		選択不可
同盟時			0.212		選択可
=cut

# コピペなので要らないデータ持ってるけどまだ仕様が決まってないので放置
# コンセプトとして国関係を条件に限定してるっぽいけど発動させにくいってことで緩和して国に関係ない条件もかなり追加した（独身の時や連続回数やレベルなど）
# タイミング
$timing_base = 0; # 0.2 # 無条件で発生なら 0 を超える数値 その数値が無条件発動時のベース倍率となる
@timings = (
#	[0]No	[1]名前							[2]条件		[3]倍率		[4]選択可能
#	[0,		'任意',							sub{ return 0.1; },	0.1,	1],
	[0,		'滅亡時',						sub{ return $cs{is_die}[$m{country}] ? 0.35 : $timing_base; },	0.5,	1],
	[1,		'同盟国がある時',						sub{ return $union ? 0.212 : $timing_base; },	0.12,	1], # ぼっちと同盟国の仕様逆さまにした 何もしないで済む「同盟を組まない」に向けるよりも「同盟組もう」にバイアス掛ける
	[2,		'ぼっちの時',						sub{ return !$union ? 1.25 : $timing_base; },	0.12,	0], # 元は選択可の0.212だったけど隠しにして効果高く
	[3,		'国力ﾄｯﾌﾟの時',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return $timing_base; } } return 0.7; },	0.7,	0], # 同盟有無の条件と同じで逆さまにした方が良いかも？ ﾌｪﾝﾘﾙは自国食らわないしトップ側は維持簡単だろうからトップ2発ﾌｪﾝﾘﾙ食らうでバランス取ってると思われる
	[4,		'国力ﾋﾞﾘの時',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] < $cs{strong}[$m{country}]) { return $timing_base; } } return 0.34; },	0.7,	0], # ビリ目指して戦争しないよりもトップ目指して戦争する方が健全っぽ
	[5,		'国力ｿﾞﾛ目の時',					sub{ return ($cs{strong}[$m{country}] > 1 && $cs{strong}[$m{country}] =~ /^(\d)\1+$/) ? 3 : $timing_base; },	0.7,	0],
	[6,		'国力1の時',					sub{ return ($cs{strong}[$m{country}] == 1) ? 2 : $timing_base; },	0.7,	1],
	[7,		'国力0の時',					sub{ return ($cs{strong}[$m{country}] == 0) ? 1 : $timing_base; },	0.7,	0],
	[8,		'国力が 12 の倍数の時',					sub{ return $cs{strong}[$m{country}] > 0 && (($cs{strong}[$m{country}] % 12) == 0) ? 0.25 : $timing_base; },	0.7,	1],
	[9,		'国力が 50 の倍数の時',					sub{ return $cs{strong}[$m{country}] > 0 && (($cs{strong}[$m{country}] % 50) == 0) ? 0.35 : $timing_base; },	0.7,	0], # 初期国力が必ず 50 の倍数なので隠しに
	[10,		'暴風・不況の時',					sub{ return ($cs{state}[$m{country}] == 3 || $cs{state}[$m{country}] == 4) ? 0.26 : $timing_base; },	0.7,	1],
	[11,		'ｳﾛﾎﾞﾛｽ覚醒中',					sub{ return ($cs{extra}[$m{country}] > 0 && $cs{extra_limit}[$m{country}] >= $time) ? 1.2 : $timing_base; },	0.7,	1],
	[12,		'資源がすべて100000未満の時',	sub{ return ($cs{food}[$m{country}] < 100000 && $cs{money}[$m{country}] < 100000 && $cs{soldier}[$m{country}] < 100000) ? 0.4 : $timing_base; },	0.4,	1],
	[13,		'兵士が20000未満の時',			sub{ return $cs{soldier}[$m{country}] < 20000 ? 0.6 : $timing_base; },	0.6,	0],
	[14,		'兵士が999999の時',				sub{ return $cs{soldier}[$m{country}] >= 999999 ? 0.6 : $timing_base; },	0.8,	0],
	[15,		'代表の時',						sub{ return &is_daihyo ? 0.32 : $timing_base; },	0.3,	1],
	[16,		'独身の時',						sub{ return $m{marriage} ? $timing_base : 0.27; },	0.3,	1],
	[17,		'連続回数が 3 の倍数の時',						sub{ return ($m{renzoku_c} > 0 && ($m{renzoku_c} % 2) == 0) ? 0.22 : $timing_base; },	0.3,	0],
	[18,		'連続5回以上の時',						sub{ if ($m{renzoku_c} > 4) { $m{renzoku_c} = 0; return 0.28; } else { return $timing_base; } },	0.3,	1],
	[19,		'連続10回以上の時',						sub{ if ($m{renzoku_c} > 9) { $m{renzoku_c} = 0; return 0.56; } else { return $timing_base; } },	0.3,	0],
	[20,		'連続20回以上の時',						sub{ if ($m{renzoku_c} > 29) { $m{renzoku_c} = 0; return 1.12; } else { return $timing_base; } },	0.3,	0],
	[21,		'連続数が 11 の倍数の時',						sub{ if ($m{renzoku_c} > 0 && (($m{renzoku_c} % 11) == 0)) { $m{renzoku_c} = 0; return 0.62; } else { return $timing_base; } },	0.3,	1],
	[22,		'統一国力が 3 の倍数の時',						sub{ return ($touitu_strong % 3) == 0 ? 0.6 : $timing_base; },	0.3,	0], # 3 だと当たりやす過ぎ？ 4 とか 6 ぐらいにしてもそもそもﾌｪﾝﾘﾙ・ｾﾞｳｽでガクガク動く 微妙
	[23,		'統一国力がｿﾞﾛ目の時',					sub{ return ($touitu_strong > 1 && $touitu_strong =~ /^(\d)\1+$/) ? 4 : $timing_base; },	0.7,	1],
	[24,		'統一難易度が 5 の倍数の時',						sub{ return ($w{game_lv} % 5) == 0 ? 0.43 : $timing_base; },	0.3,	1],
	[25,		'前期統一国の時',						sub{ my($c1, $c2) = split /,/, $w{win_countries}; return ($c1 == $m{country} || $c2 == $m{country}) ? 0.38 : $timing_base; },	0.3,	0],

# 変動しづらいのでイマイチ
#	[16,		'仕官数トップ',					sub{ for my $i (1..$w{country}) { if ($cs{member}[$i] > $cs{member}[$m{country}]) { return 0.2; } } return 0.5; },	0.7,	1],
#	[17,		'仕官数ビリ',					sub{ for my $i (1..$w{country}) { if ($cs{member}[$i] < $cs{member}[$m{country}]) { return 0.2; } } return 0.5; },	0.7,	1],
);


=pod
個人的には所持金・ｺｲﾝデメリットみたくユーザーがデメリットの強弱を変えられる項目がもっと欲しい
ブーストかけたいやつはかければ良いし、デメリットが嫌ならブーストさせなければ良いしみたいな
問題は効率が悪そうなことか こういう計算にしたらっていうのあったら誰か教えて欲しい
ﾍﾟｯﾄデメリットはほとんど試してないけどとんでもないことになるかも

効果量
世代交代		3
ﾍﾟｯﾄﾚﾍﾞﾙ		効果量はコード				★7ぶち込んで2.6
給料			2.3
no1熟練		2.2							減って増えてもほとんど問題がない上に上がりにくい熟練なのでうってつけ
ｽﾃﾀﾞｳﾝ		2
離婚			1.6							これもﾃﾞﾒﾘｯﾄじゃなくなる可能性もあるけど大したことないか？
武器ﾚﾍﾞﾙ		1.6							ﾃﾞﾒﾘｯﾄじゃないとも言えるしｼﾞｬﾝｸでゴミ武器買って鍛えて使ってがうまいけど当たりってことで
勲章			1.2
孵化値		1.2
拘束			1
貢献値		1
所持金2		0.7
ｺｲﾝ2			0.6
所持金		0.5～3.249？				所持金多いほどブースト
ｺｲﾝ			0.5～1.9？					ｺｲﾝ多いほどブースト
孵化値		0.5～孵化値 * 0.006		育て屋のﾊｽﾞﾚｴｯｸﾞぶち込む用 孵化ﾀｷｵﾝぶち込んで 59.99400 修正だね！
なし			0.5
=cut
# その他デメリット
$demerit_base = 0.5; # 無条件で発生なら 0 を超える数値 その数値が無条件発動時のベース倍率となる
@demerits = (
#	[0]No	[1]名前				[2]デメリット		[3]倍率		[4]選択可能
	[0,		'なし',				sub{ return $demerit_base; },		0.5,	0],
	[1,		'基本拘束',			sub{ &wait; return 1; },	1,	1],
	[2,		'世代交代',			sub{ $m{lv} = 99; $m{exp} = 100; return 3; },	1.2,	0],
	[3,		'ｽﾃｰﾀｽﾀﾞｳﾝ',	sub{ @st = (qw/max_hp max_mp at df mat mdf ag cha lea/); $k = $st[int(rand(@st))]; $m{$k} -= int(rand(20)); $m{$k} = $m{$k} <= 0 ? int(rand(20)):$m{$k}; return 2; },	1.2,	0],
	[4,		'貢献値100減少',		sub{ $m{rank_exp} -= 100; return 1; },	1,	1],
#	[5,		'貢献値100減少(弱)',		sub{ $m{rank_exp} -= 100; return 0.8; },	0.8,	0],
	[5,		'所持金10%消費',		sub{ if ($m{money} > 49999999) { my $vv = 4999999 * 0.0000005; $m{money} -= int(4999999 * 0.1); return $vv > 0 ? $vv + 0.75 : $demerit_base; } else { my $vv = $m{money} * 0.0000005; $m{money} = int($m{money} * 0.9); return $vv > 0 ? $vv + 0.75 : $demerit_base; } },	0.7,	1], # ｻﾏｰｼﾞｬﾝﾎﾞｾﾞｳｽで一発で終わるからあとで考える
	[6,		'所持金10000消費',		sub{ $m{money} -= 10000; return 0.7; },	0.7,	0],
	[7,		'勲章3個返上',		sub{ $m{medal} -= 3; return 1.2; },	1.5,	1],
#	[8,		'勲章10個返上(弱)',		sub{ $m{medal} -= 10; return 1; },	1,	0],
	[8,		'ｺｲﾝ10%減少',		sub{ my $vv = $m{coin} * 0.0000005; $m{coin} = int($m{coin} * 0.9); return $vv > 0 ? $vv + 0.65 : $demerit_base ; },	0.8,	1],
	[9,		'ｺｲﾝ10000減少',		sub{ if ($m{coin} > 9999) { $m{coin} -= 10000; return 0.6; } else { return $demerit_base; } },	0.5,	0],
	[10,		'給与+6時間',		sub{ $m{next_salary} += int( 3600 * 6 ); return 2.3; },	1.4,	1],
#	[11,		'孵化値ﾘｾｯﾄ',		sub{ my $vv = $m{egg_c} * 0.006; $m{egg_c} = 0; return $vv + 0.5; },	0.6,	1], # 却下
	[11,		'孵化値100消費',		sub{ if ($m{egg_c} > 99) { $m{egg_c} -= 100; return 1.2; } else { return 0.5; } },	0.6,	1], # ↑の修正 固定にして大人しく
	[12,		'武器ﾚﾍﾞﾙ-1',		sub{ if ($m{wea_lv} > 0) { $m{wea_lv} -= 1; return 1.6 } else { return 0.5; } },	0.6,	0],
	[13,		'ﾍﾟｯﾄﾚﾍﾞﾙ-1',		sub{ if ($m{pet_c} > 0) { my @fib_rets = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 2000, 5000, 10000, 20000, 50000, 100000); my $vv = $m{pet_c}; $m{pet_c}--; return 0.1 * $fib_rets[$vv] + 0.5; } else { return 0.5; } },	0.6,	0],
	[14,		'no1熟練-1',		sub{ if ($m{no1_c} > 0) { my $vv = $m{no1_c}; $m{no1_c} -= 1; return 2.2; } else { return 0.5; } },	0.6,	1],
	[15,		'ゴミクズ',			sub{ if ($m{shogo} ne $shogos[1][0]) { $m{shogo} = $shogos[1][0]; return 4; } else { return 0.5; } },	2.0,	0], # 2.6万～260万消費 100世代まで上がり続ける弊害で落差激しいからゴミクズの仕様を元に戻すとかしたい
	[16,		'離婚',			sub{ if ($m{marriage} ne '') { $m{marriage} = ''; return 1.6; } else { return 0.5; } },	1.5,	0], # 
);

# 回数
@max_counts = (
#	[0]No	[1]回数	[2]倍率	[3]選択可能
	[0,		1,		1,		1],
	[1,		2,		0.4,		0],
	[2,		3,		0.2,		0],
);

# 乱数のブレ幅が大きいとブレ幅の小さい倍率に対して乱数が計算結果の多くを占めてしまう（倍率の意義が薄まる）
# 明示的にglobalしてないけど配列内の関数のグローバル変数に外からアクセスできない（配列が定義されて関数を呼び出すまで関数も定義されずグローバル変数として機能しないみたいな？）
# 参照できないから関数内でメッセージを返すように仕様変更
# 効果
@effects = (
#	[0]No	[1]名前				[2]効果			[3]選択可能	[4]メッセージ
	[0,		'ﾌｪﾝﾘﾙ',			sub{
		$v = shift;
		$c = &get_most_strong_country;
		my ($attack_name, $attack_value) = get_attack_level(400);
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			next if $cs{strong}[$i] == 0; # ｴｸｽｶﾘﾊﾟｰで国力1に持って行きたいので国力0の国はスルー
#			$cs{strong}[$i] -= int((rand(16000)+2000) * $v);
#			$cs{strong}[$i] -= int((rand(16000)+2000) * $v) if ($i eq $c);
			$cs{strong}[$i] -= int((rand($attack_value)+100) * $v);
			$cs{strong}[$i] -= int((rand($attack_value)+100) * $v) if ($i eq $c); # 国力トップにはﾌｪﾝﾘﾙ2発
			if ($cs{strong}[$i] < 0) {
				$cs{strong}[$i] = int(rand(10)) * 100; # 国力マイナスになったら国力を 0～900 に
			}
		};
		&write_cs;
		return "$v倍$attack_nameﾌｪﾝﾘﾙによって各国の国力が減少した";
	},	1,	'ﾌｪﾝﾘﾙによって各国の国力が減少した'],
	[1,		'ｾﾞｳｽ',				sub{
		$v = shift;
		# 国数と難易度にもよるがﾌｪﾝﾘﾙvsｾﾞｳｽだと基本ﾌｪﾝﾘﾙのが使い勝手良さそう？
		# ﾌｪﾝﾘﾙゲーもどうかと思うのでｾﾞｳｽも底上げするか何か他にメリット持たせても良さそう
#		$v *= 1.5;
		my ($attack_name, $attack_value) = get_attack_level(1000);
#		$cs{strong}[$m{country}] += int((10000 + rand(10000)) * $v);
		$cs{strong}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v倍$attack_nameｾﾞｳｽによって$c_mの国力が増加した";
	},	1,	'自国の国力が増加した'],
	[2,		'ﾛﾌﾟﾄ（大地震）',				sub{
		$v = shift;
		$v *= 0.4;
#		my ($attack_name, $attack_value) = get_attack_level(100000);
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{soldier}[$i] -= int((rand(600000)+200000) * $v);
#			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
			$cs{soldier}[$i] = int($cs{soldier}[$i] * 0.5 ** $v);
			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v倍ﾛﾌﾟﾄによって全国の兵士が激減した";
	},	0,	'全国の兵士が激減した'], # 0
	[3,		'ﾛﾌﾟﾄ（自然災害）',				sub{
		$v = shift;
		$v *= 0.4;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{food}[$i] -= int((rand(600000)+200000) * $v);
			$cs{food}[$i] = int($cs{food}[$i] * 0.5 ** $v);
			$cs{food}[$i] = 0 if $cs{food}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v倍ﾛﾌﾟﾄによって全国の$e2j{food}が激減した";
	},	0,	'全国の食糧が激減した'], # 0
	[4,		'ﾛﾌﾟﾄ（経済破綻）',				sub{
		$v = shift;
		$v *= 0.4;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{money}[$i] -= int((rand(600000)+200000) * $v);
			$cs{money}[$i] = int($cs{money}[$i] * 0.5 ** $v);
			$cs{money}[$i] = 0 if $cs{money}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v倍ﾛﾌﾟﾄによって全国の$e2j{money}が激減した";
	},	0,	'全国の資金が激減した'], # 0
	[5,		'ｱﾙｶﾄﾗｽﾞ',				sub{
		# ｱﾙｶﾄﾗｽﾞすげーテスト中 黒豚鯖仕様のがたぶん弱いんだと思う
		# 倍率表示からの倍率と実際の効果量が違うからの倍率イジった関係で新しい仕様にしようかと
		$v = shift;
		my @ks = (qw/ceo war dom pro mil/);

=pod
		my @ks = (qw/war dom pro mil/);
		@ks = List::Util::shuffle(@ks);
		unshift @ks, 'ceo';
=cut

		my @ks2 = ();
		my $vv = $v - int($v);
		for my $i (0 .. int($v)) {
			my $k = $ks[int(rand(@ks))];
			next if int(rand(2)) < 1;
			if ((int($v)-$i) >= 1 || rand(1) < $vv) {
				push @ks2, $k;
			}
		}

		my %cnt;
		@ks2 = grep {!$cnt{$_}++} @ks2;

		unless (@ks2) {
			&write_cs;
			return "$v倍ｱﾙｶﾄﾗｽﾞは不発に終わった";
		}

		my $daihyo = '';
		for my $k (@ks2) {
			$daihyo .= "$e2j{$k}";
		 	for my $i (1 .. $w{country}) {
	 			next if $cs{$k}[$i] eq '';
	 			next if $i eq $m{country};
#	 			next if rand(0.1) > $v;

	 			&regist_you_data($cs{$k}[$i], 'lib', 'prison');
	 			&regist_you_data($cs{$k}[$i], 'tp', 100);
	 			&regist_you_data($cs{$k}[$i], 'y_country',  $m{country});
	 			&regist_you_data($cs{$k}[$i], 'wt', $GWT * 60);
	 			&regist_you_data($cs{$k}[$i], 'act', 0);

	 			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi が開けません");
	 			print $fh "$cs{$k}[$i]<>$i<>\n";
	 			close $fh;
	 		}
		};
		&write_cs;
		return "$v倍ｱﾙｶﾄﾗｽﾞによって全国の$daihyoが監禁された";
	},	1,	'全国の代表が監禁された'],
	[6,		'ｱﾙｶﾄﾗｽﾞ(裏)',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my @names = &get_country_members($c);
	 	for my $name (@names) {
			$name =~ tr/\x0D\x0A//d;
		
			&regist_you_data($name, 'lib', 'prison');
			&regist_you_data($name, 'tp', 100);
			&regist_you_data($name, 'y_country',  $m{country});
			&regist_you_data($name, 'wt', $GWT * 60);
			&regist_you_data($name, 'act', 0);
		
			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi が開けません");
			print $fh "$name<>$c<>\n";
			close $fh;
		};
		&write_cs;
		return "$cs{name}[$c]の国民が監禁された";
	},	0,	"$cs{name}[$c]の国民が監禁された"], # 0
	# 必殺ﾛﾌﾟﾄと滅亡着弾ﾍﾟﾅﾙﾃｨで物資吹き飛びまくる気がする
	# ﾛﾌﾟﾄ弱体化させて物資増加効果を上げても良い気もするがﾛﾌﾟﾄは適当限定に対してこっちは選択可だし微妙なとこ
	[7,		'ｸｯｷｰ',				sub{
		$v = shift;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{food}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{food}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v倍$attack_nameｸｯｷｰによって$c_mの食糧が増加した";
	},	1,	'自国の食糧が増加した'],
	[8,		'ｴﾋﾞｽ',				sub{
		$v = shift;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{money}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{money}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v倍$attack_nameｴﾋﾞｽによって$c_mの資金が増加した";
	},	1,	'自国の資金が増加した'],
	[9,		'ﾏﾙｽ',				sub{
		$v = shift;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{soldier}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{soldier}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v倍$attack_nameﾏﾙｽによって$c_mの兵士が増加した";
	},	1,	'自国の兵士が増加した'],
	# 1時間固定に戻した方が良いかも？
	# ｳﾛﾎﾞ強い指摘あったから1時間1倍から30分1倍に調整、さらに15分ベースにして様子見
	# ｳﾛﾎﾞ覚醒中は上書きできないようになっていたが発生しても効果なしだと寂しいので常に上書き
	# 長時間を引いた後に短時間を引くと効果短縮だけど強い指摘もあったしそれぐらいでちょうど良いかも？
	[10,	'ｳﾛﾎﾞﾛｽ',				sub{
		$v = shift;
		my $vv = int(15 * $v);
#		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 60 * $vv;
			$cs{extra}[$m{country}] = 1;
#		}
		&write_cs;
		return "$c_mの奪国力が$vv分増加する";
	},	0,	'自国の奪国力が増加する'], # 0
	[11,	'ｳﾛﾎﾞﾛｽ(軍事)',				sub{
		$v = shift;
		my $vv = int(15 * $v);
#		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 60 * $vv;
			$cs{extra}[$m{country}] = 2;
#		}
		&write_cs;
		return "$c_mの軍事力が$vv分増加する";
	},	0,	'自国の軍事力が増加する'], # 0
	[12,	'ｲｰｽﾀｰ',				sub{
		$v = shift;
		# 統一難易度の下がるｲｰｽﾀｰ
		# 選択可能のｴｸｽｶﾘﾊﾟｰを導入したのでｲｰｽﾀｰを撃つべき状況は増えたが国力5000以上で滅亡してることもあってｲｽﾀ撃つ前に勝手に復興しそう
		# 他に何かメリット持たせた方が良さそうな感じ（滅亡国の国力+0～100効果を足したのは国力1条件を満たした滅亡国の邪魔をするとか国力0滅亡した時に打ち返したらｿﾞﾛ目になる可能性があるため）
		for my $i (1..$w{country}) {
			if ($cs{is_die}[$i]) {
				$cs{strong}[$i] += int(rand(101));
				$cs{is_die}[$i] = 0;
				--$w{game_lv};
			}
		};
		&write_cs;
		return "全国が復興しました";
	},	1,	'全国が復興しました'],
	[13,	'ﾘｳﾞｧｲｱｻﾝ',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my ($attack_name, $attack_value) = get_attack_level(2000);
#		my $vv = int((20000 + rand(20000)) * $v);
		my $vv = int($attack_value * (rand(0.1)+0.95) * $v);
		if ($cs{strong}[$c] < $vv) {
			$vv = $cs{strong}[$c];
		}
		$cs{strong}[$c] -= $vv;
		$cs{strong}[$m{country}] += int($vv / 3);
		&write_cs;
		return "$v倍$attack_nameﾘｳﾞｧｲｱｻﾝによって$cs{name}[$c]の国力を奪った";
	},	0,	"$cs{name}[$c]の国力を奪った"], # 0
	[13,	'ｴｸｽｶﾘﾊﾞｰ',				sub{
		$v = shift;
		# 一国がﾌｪﾝﾘﾙ集中砲火される必殺技
		# その対象国の国力によってﾌｪﾝﾘﾙ何十発分にもなって統一国力が激減
		# 本来は自国を除く国力トップに当たる訳だけど減る統一国力が基本最高値を叩き出すので1～4発ぐらい撃つだけでゲームが終わる（英雄一回で一発撃てるかどうかで想定してるはず）
		# もっと撃ちやすくして欲しいということで、基本常時最高値を叩き出さないように自国を除くランダムセレクトに変更
		# さらにすぐに終わりすぎないように統一難易度を上げるようにしたので統一難易度の倍数条件を満たしたりするかもしれない
		# （そもそも復興で難易度下がるので難易度上げる処理入れないと統一国力も統一難易度もガンガン下がり続けてしまう）
		# 暴風・不況条件があるのでイリーガルな滅亡方法を作ると状態変更回数がそれだけ減ってしまい条件満たしにくくなったり条件満たしたままになるので状態変更も再現させる
		# ｴｸｽｶﾘﾊﾟｰの方は国力が0になる（本当に滅亡した）訳じゃないから再現しなくて良い やるとしたら全国飢饉とか一層必殺技ﾍﾟｽﾄ追加した方が良さそう
		my @cs2 = (1 .. $w{country});
		splice(@cs2, $m{country}-1, 1);
		$c = $cs2[int(rand(@cs2))]; # &get_most_strong_country;
		$w{game_lv} += int($cs{strong}[$c]*0.0002); # 対象国の国力5000毎に難易度+1
		$cs{strong}[$c] = 0;
		$cs{is_die}[$c] = 1;
		$cs{state}[$_] = int(rand(@country_states)) for (1 .. $w{country});
		&write_cs;
		return "$cs{name}[$c]に聖剣を放った";
	},	0,	"$cs{name}[$c]に聖剣を放った"], # 0
	[14,	'ｴｸｽｶﾘﾊﾟｰ',				sub{
		$v = shift;
		# 偽ｴｸｽｶﾘﾊﾞｰ、ｴｸｽｶﾘﾊﾞｰからﾌｪﾝﾘﾙ効果を除いてみたがこれだと要は敵国にﾉｱを張る効果になってしまう（さらに滅亡条件も満たさせる）
		# もうちょっと自国に有利になるように確率でﾉｱを張りつつ滅亡条件も満たすように変更
		# 統一難易度についてはｴｸｽｶﾘﾊﾞｰと同様
		# ﾉｱ効果よりも滅亡条件＋国力1条件＋統一難易度条件を操作するために使ったりするのを想定

		$c = rand(100) < 60 ? $m{country} : # 基本自国効果だが自分で選べる必殺技で使い勝手良すぎるので、
				int(rand($w{country})+1); # 敵国に効果を与えるデメリットになることもあるように

		$cs{is_die}[$c] = 1 if int(rand(3)) < 1; # 1/3 の確率でﾉｱ効果

		++$cs{strong}[$m{country}]; # 国力+1 国力0で滅亡した時に撃ち返せば国力1条件を満たせる 運が良ければ国力ゾロ目も有り得る

		# 必ず上がるだと難易度がうなぎ上りだろうから50%ぐらいで 複数の条件に絡む技だし
		# 必ずﾉｱ効果が発生する訳じゃないのでまだ上がりすぎかも
		++$w{game_lv} if $cs{is_die}[$c] && int(rand(2)) < 1;
		&write_cs;
		return "$cs{name}[$c]が眩い光に包まれた";
	},	1,	"$cs{name}[$c]に聖剣を放った"],
	[15,	'ﾊﾞﾙﾑﾝｸ',				sub{
		$v = shift;
		# 前期統一国を自国にする必殺技 給料美味しいです！ 孵化値美味しいです！ 前期統一条件を満たす
		$w{win_countries} = $m{country};
		&write_cs;
		return "$cs{name}[$m{country}]が財宝を独り占めにする";
	},	0,	"$cs{name}[$c]に聖剣を放った"],
	[16,	'ﾄﾞﾗｳﾌﾟﾆﾙ',				sub{
		$v = shift;
		# 自国民の疲労回復 or 給料時間短縮
		# ﾊﾞﾙﾑﾝｸ撃っとけば給料美味しいです！ 孵化値美味しいです！ 給料+6時間デメリットの打ち消し
		# 凶悪であれば各国民確率で効果発生とか回復値・短縮値を倍率に任せるとか、ハズレ要素として賽銭時間短縮も追加するとか自国民孵化値+100とか（孵化値消費デメリットの弱埋め合わせ）
		my $f = int(rand(3)) < 1; # 0 = 疲労(2/3), 1 = 給料(1/3)
		my %sames;
		open my $fh, "< $logdir/$m{country}/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;
			# 同じ名前の人が複数いる場合
			next if ++$sames{$player} > 1;
			unless ($f) {
				&regist_you_data($player,'act', 0);
			}
			else {
				&regist_you_data($player,'next_salary', $time);
			}
		}
		close $fh;

		unless ($f) {
			$m{act} = 0;
		}
		else {
			$m{next_salary} = $time;
		}

		return "滴る恵みに$cs{name}[$m{country}]の国民が狂喜乱舞する";
	},	0,	"$cs{name}[$c]に聖剣を放った"],
);
#=================================================
# 登録メッセージ
#=================================================
sub regist_mes {
	$force = shift;
	$tm = qq|【必殺技】|;
	my $attack = &get_attack;
	my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack;
	my $is_count = &count_check($a_max_count, $a_count, $a_last_attack);
	$attack = &get_attack;# ？？？
	if ($attack eq '' || $force) {
		$tm .= qq|<form method="$method" action="$script">|;

		$tm .= qq|<select name="trigger" class="menu1">|;
		for my $i (0..$#triggers) {
			next if !$triggers[$i][4];
			$tm .= qq|<option value="$i">$triggers[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="timing" class="menu1">|;
		for my $i (0..$#timings) {
			next if !$timings[$i][4];
			$tm .= qq|<option value="$i">$timings[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="demerit" class="menu1">|;
		for my $i (0..$#demerits) {
			next if !$demerits[$i][4];
			$tm .= qq|<option value="$i">$demerits[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="max_count" class="menu1">|;
		for my $i (0..$#max_counts) {
			next if !$max_counts[$i][3];
			$tm .= qq|<option value="$i">$max_counts[$i][1]回</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="effect" class="menu1">|;
		for my $i (0..$#effects) {
			next if !$effects[$i][3];
			$tm .= qq|<option value="$i">$effects[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><input type="text" name="voice" class="text_box_b"/>|;
		$tm .= qq|<br><br><input type="checkbox" name="random" value="1"/>適当|;
		$tm .= qq|<input type="hidden" name="regist_attack"/>|;
		$tm .= qq|<input type="hidden" name="mode" value="regist_attack">|;
		$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$tm .= qq|<input type="submit" value="必殺技を設定する" class="button1"></form>|;

	} else {
		my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $random, $last_attack) = split /<>/, $attack;
		unless ($is_count) {
	#		my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack_set;
	
			unless ($is_mobile) {
				$tm .= qq|<table class="table1" cellpadding="3">|;
				$tm .= qq|<tr><th>行動</th><td>$triggers[$trigger][1]</td></tr>|;
				$tm .= qq|<tr><th>条件</th><td>$timings[$timing][1]</td></tr>|;
				$tm .= qq|<tr><th>デメリット</th><td>$demerits[$demerit][1]</td></tr>|;
				$tm .= qq|<tr><th>回数</th><td>$max_counts[$max_count][1]回</td></tr>|;
				$tm .= qq|<tr><th>効果</th><td>$effects[$effect][1]</td></tr>|;
				$tm .= qq|<tr><th>ｾﾘﾌ</th><td>「$voice」</td></tr>|;
				$tm .= qq|</table>|;
			}
			else {
				$tm .= qq|<br>$triggers[$trigger][1]|;
				$tm .= qq|<br>$timings[$timing][1]|;
				$tm .= qq|<br>$demerits[$demerit][1]|;
				$tm .= qq|<br>$max_counts[$max_count][1]回|;
				$tm .= qq|<br>$effects[$effect][1]|;
				$tm .= qq|<br>セリフ「$voice」|;
			}

#			$tm .= qq|<br>次の必殺技発動まで <font color="#FF0000"><b>ＯＫ！</b></font>|;

			$tm .= qq|<br><form method="$method" action="$script">|;
			$tm .= qq|<input type="hidden" name="mode" value="use_attack">|;
			$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$tm .= qq|<input type="checkbox" name="luxury" value="1">空打ち|;
			$tm .= qq|<input type="submit" value="必殺技を使用する" class="button1"></form>|;
		}
		else {
			my $nokori_time = ($last_attack + $cooldown_time) - $time;
			my $nokori_time_mes = '';
			$nokori_time_mes = sprintf("約<b>%d</b>時<b>%02d</b>分後", $nokori_time / 3600, $nokori_time % 3600 / 60);
			$tm .= qq|<br>必殺技の再設定まで $nokori_time_mes|;
		}
	}

	return $tm;
}
#=================================================
# 必殺技登録
#=================================================
sub regist_attack {
	my ($trigger, $timing, $demerit, $max_count, $effect, $voice, $random) = @_;
	my $attack = &get_attack;

	if ($attack ne '') {
		&del_attack;
		return 0;
	}
	if ($random) {
		my @triggers_s = ();
		for my $i (0..$#triggers) {
			if ($triggers[$i][4]) {
				push @triggers_s, $i;
			}
		}
		if (rand(5) < 1) {
			$trigger = int(rand(@triggers));
		} else {
			$trigger = $triggers_s[int(rand(@triggers_s))];
		}
		
		my @timings_s = ();
		for my $i (0..$#timings) {
			if ($timings[$i][4]) {
				push @timings_s, $i;
			}
		}
		if (rand(5) < 1) {
			$timing = int(rand(@timings));
		} else {
			$timing = $timings_s[int(rand(@timings_s))];
		}
		
		my @demerits_s = ();
		for my $i (0..$#demerits) {
			if ($demerits[$i][4]) {
				push @demerits_s, $i;
			}
		}
		if (rand(5) < 1) {
			$demerit = int(rand(@demerits));
		} else {
			$demerit = $demerits_s[int(rand(@demerits_s))];
		}
		
		my @max_counts_s = ();
		for my $i (0..$#max_counts) {
			if ($max_counts[$i][3]) {
				push @max_counts_s, $i;
			}
		}
		if (rand(10) < 1) {
			$max_count = int(rand(@max_counts));
		} else {
			$max_count = $max_counts_s[int(rand(@max_counts_s))];
		}
		
		my @effects_s = ();
		if (rand(3) < 1) {
			for my $i (0..$#effects) {
				if ($effects[$i][3]) {
					push @effects_s, $i if int(rand(100)) < 70;
				}
				else {
					push @effects_s, $i;
				}
			}
			$effect = $effects_s[int(rand(@effects_s))];
#			$effect = int(rand(@effects));
		} else {
			for my $i (0..$#effects) {
				if ($effects[$i][3]) {
					push @effects_s, $i;
				}
			}
			$effect = $effects_s[int(rand(@effects_s))];
		}
	} else {
		if (!$triggers[$trigger][4]) {
			return 0;
		}
		if (!$timings[$timing][4]) {
			return 0;
		}
		if (!$demerits[$demerit][4]) {
			return 0;
		}
		if (!$max_counts[$max_count][3]) {
			return 0;
		}
		if (!$effects[$effect][3]) {
			return 0;
		}
	}
	open my $fh, ">> $this_file" or &error("$this_fileに書き込めません");
	if ($config_test) {
		print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$triggers[$trigger][1]・$timings[$timing][1]・$demerits[$demerit][1]・$max_counts[$max_count][1]・$effects[$effect][1]<>0<>$time<>\n";
	}
	else {
		print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>0<>$time<>\n";
	}
	close $fh;
	
	return 1;
}
#=================================================
# 必殺技取得
#=================================================
sub get_attack {
	if (-f "$this_file") {
		open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				close $fh;
				return $line;
			}
		}
		close $fh;
	}
	return '';
}
#=================================================
# 必殺技削除
#=================================================
sub del_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				next;
			}
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# 必殺技解除
#=================================================
sub cancel_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>0<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# 必殺技使用
#=================================================
sub use_count_up {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが読み込めません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# 必殺技回数チェック
#=================================================
sub count_check {
	my ($max_count, $count, $last_attack) = @_;
	if ($max_counts[$max_count][1] > $count) {
		return 0;
	} elsif ($last_attack + $cooldown_time < $time) {
		&del_attack;
		return 1;
	} else {
		return 1;
	}
}
#=================================================
# 必殺技発動
#=================================================
sub super_attack {
	my $key = shift;
	unless ($m{country}) {
		return;
	}
	if ($time < $w{reset_time}) {
		return;
	}
	my $attack = &get_attack;
	if ($attack eq '') {
		return;
	}
	my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $attack;
	if ($key eq 'luxury') {
		&cancel_attack;
	}
	if ($key ne $triggers[$trigger][2] || rand(100) > $triggers[$trigger][5]) {
		return;
	}
#	$attackable = &{$timings[$timing][2]};
#	if (!$attackable) {
#		return;
#	}
	my $timing_v = &{$timings[$timing][2]};
	return unless $timing_v;
	if (&count_check($max_count, $count, $last_attack)) {
		return;
	}

	my $demerit_v = &{$demerits[$demerit][2]};
	return unless $demerit_v > 0;
#	return unless &{$demerits[$demerit][2]};
#	my $mem = &modified_member($m{country});
	$e_mes = $effects[$effect][2]->($triggers[$trigger][3]
#							* &{$timings[$timing][2]}
							* $timing_v
#							* $demerits[$demerit][3]
							* $demerit_v
							* $max_counts[$max_count][2]
#							* 11.2);
							* (10 + ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 0.1));
# 仕官上限数が技の強弱に与える影響が大きい 人が少ない鯖と多い鯖とでかなりの差が出る上に少ないと弱く多いと強くで終わりにくいすぐ終わるの極端な感じ
#							* (1 + ($cs{capacity}[$m{country}] - $mem) * 0.1)); # 仕官上限数に新規ちゃん多いほど弱体化？ たぶん逆になってる
#	$e_mes = $effects[$effect][4];
	&use_count_up;
	&mes_and_world_news("必殺技を開放し、$e_mes。<br><b>$m{name}「$voice」</b>", 1);
}

#=================================================
# 必殺技の基本効果量を渡すと必殺技の強さが配列で返る($1, $2)
# $1：ﾚﾍﾞﾙ文字（通常・メガ・ギガ）
# $2：効果量（1倍・1.2倍・1.5倍）→(1倍・1.1倍・1.3倍)
#=================================================
sub get_attack_level {
	my $attack_value = shift;
	my @level_names = ('', 'ﾒｶﾞ', 'ｷﾞｶﾞ');
	my @level_values = (1, 1.1, 1.3);
	my $level = rand(100) < 10 ? 2 :
					rand(100) < 25 ? 1 :
					0;
	return ($level_names[$level], $attack_value*$level_values[$level]);
}

#=================================================
# 修正後所属人数
#=================================================
sub modified_member {
	my $count_country = shift;
	my $count = 0;
	my @members = &get_country_members($count_country);
	for my $member (@members) {
		$member =~ tr/\x0D\x0A//d; # = chomp 余分な改行削除
		my $member_id = unpack 'H*', $member;
		my %datas = &get_you_datas($member_id, 1);
		unless ($datas{sedai} == 1) {
			$count++;
		}
	}
	return $count;
}

1;