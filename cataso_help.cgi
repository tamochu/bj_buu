#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

sub header2 {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	
print << "HTML";
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="$htmldir/css/cataso.css?$jstime" />
<title>HELP</title>
</head>
<body>
HTML
}

sub run {
	print qq|<ul>|;
	print qq|<li>「/reset」:リセット</li>|;
	print qq|<li>ルール：持ち点が10点になり勝利宣言をすれば勝利</li>|;
	print qq|<li>点数：<ul><li>家：1個1点</li><li>街：1個2点</li><li>道王（一筆書きで一番長い道を作った人）：2点</li><li>騎士王（騎士カードを一番多く使った人）：2点</li><li>得点カード：1枚1点</li></ul></li>|;
	print qq|<li>資源は左から<span class="sand">土</span><span class="wool">羊</span><span class="iron">鉄</span><span class="wheat">麦</span><span class="tree">木</span></li>|;
	print qq|<li>街道:<span class="sand">土1</span><span class="tree">木1</span></li>|;
	print qq|<li>家：<span class="sand">土1</span><span class="wool">羊1</span><span class="wheat">麦1</span><span class="tree">木1</span></li>|;
	print qq|<li>街：<span class="iron">鉄3</span><span class="wheat">麦2</span></li>|;
	print qq|<li>カード：<span class="wool">羊1</span><span class="iron">鉄1</span><span class="wheat">麦1</span></li>|;
	print qq|</ul>|;
}

sub footer2 {
	print qq|</body></html>|;
}

&header2;
&run;
&footer2;
exit;
