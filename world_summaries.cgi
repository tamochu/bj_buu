#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# 世界情勢表示 Created by nanamie
#================================================

@world_summaries = (
	# 平和
	'終戦期間がいつもより長いです。<br>'.
	'以下省略',
	# 繁栄
	'一部の行動に対して功労金が貰えます。<br>'.
	'以下省略',
	# 革命
	'革命',
	# 略奪
	'略奪',
	# 暴君
	'暴君',
	# 混沌
	'混沌',
	# 結束
	'結束',
	# 鉄壁
	'鉄壁',
	# 不仲
	'不仲',
	# 絶望
	'戦争勝利時に復興フラグが立ちません。<br>'.
	'終焉と違い同盟可、統一国力を超えたら通常通り統一できます。<br>'.
	'以下省略',
	# 深遠
	'深淵',
	# 監禁
	'監禁',
	# 厄年
	'厄年',
	# 終焉
	'終焉',
	# 大殺界
	'大殺界',
	# 迷走
	'迷走',
	# 匿名
	'匿名',
	# 白兵
	'白兵',
	# 殺伐
	'殺伐',
	# 謎
	'謎',
	# 花火
	'花火',
	# 拙速
	'拙速',
	# 英雄
	'英雄',
	# 三国志
	'三国に分かれて統一戦をします。<br>'.
	'以下省略',
	# 不倶戴天
	'二国に分かれて統一戦をします。<br>'.
	'以下省略',
	# 混乱
	'プレイヤーがあちこちの国に飛ばされそれぞれ統一戦をします。<br>'.
	'以下省略',
	# 暗黒
	'封印国とNPC国とに分かれて統一戦をします。<br>'.
	'以下省略'
);

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{world} ||= 0;
	$in{world} = 0 if $in{world} >= @world_states;

	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="ＴＯＰ" class="button1"></form>|;
	}

	print "<h1>$world_states[$in{world}]</h1>";
	print "<p>誰か書きたい人おらんかね～</p>";
	print "$world_states[$in{world}]は、$world_summaries[$in{world}]";
}