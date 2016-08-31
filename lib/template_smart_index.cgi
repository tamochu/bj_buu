#================================================

# index.cgiﾃﾝﾌﾟﾚｰﾄ(スマホ) Created by Merino

#================================================



#================================================

sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	my $login_box_html = '';
	if ($cs_c{all} >= $max_login) {
		$login_box_html .= qq|<br><p style="font-size: 16px; color: #FF0; font-weight: bold;">ﾛｸﾞｲﾝ規制中</p><p>ﾛｸﾞｲﾝ人数が減るまでしばらくお待ちください。携帯からのﾛｸﾞｲﾝは可能\です。</p><br>|;
	}
	else {
		$login_box_html .= qq|<form method="$method" action="login.cgi" style="margin: 0 auto; padding: 0;"><table class="table1" style="margin:0 auto;height:68px;">|;
		$login_box_html .= qq|<tr><th style="font-family: monospace;">ﾌﾟﾚｲﾔｰ名:</th><td><input type="text" name="login_name" value="$cook_name" class="text_box1"></td><td rowspan="3"><input type="submit" value="ログイン" class="button_login"></td></tr>|;
		$login_box_html .= qq|<tr><th style="font-family: monospace;">ﾊﾟｽﾜｰﾄﾞ:</th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><td colspan="2" style="text-align:center;"><input type="checkbox" id="cookie" name="is_cookie" value="1" $checked><label for="cookie">次回から入力省略</label></th></tr>|;
#		$login_box_html .= qq|<tr><td colspan="2" style="font-family: monospace;"><input type="submit" value="ログイン" class="button_login"></th></tr>|;
		$login_box_html .= qq|</table></form>|;
	}

	my $entry_box_html = '<div class="entry_box_s">';
		$entry_box_html .= qq|<form action="readme.html">\n<input type="submit" value="Readme" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<form action="http://www13.atwiki.jp/blindjustice/.html">\n<input type="submit" value="説明書" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<form action="http://www43.atwiki.jp/bjkurobutasaba/">\n<input type="submit" value="Wiki" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<br><form action="new_entry.cgi" class="new_entry">\n<input type="submit" value="新規登録" class="navi_button" style="width:100% !important;">\n</form></div>|;


	my @navigator = (
		['Readme', 'readme.html'],
		['説明書', 'http://www13.atwiki.jp/blindjustice/'],
		['Wiki', 'http://www43.atwiki.jp/bjkurobutasaba/'],
		['新規登録', 'new_entry.cgi'],
		['ﾌﾟﾚｲﾔｰ一覧', 'players.cgi'],
		['悠久の石碑', 'legend.cgi'],
		['商人ﾗﾝｷﾝｸﾞ', 'sales_ranking.cgi'],
		['ｺﾝﾃｽﾄ会場', 'contest.cgi'],
		['過去の栄光', 'news.cgi'],
#		['HOME', "$home_m"], # ホームにホームボタン要らなくね？
#		['ﾘｾｯﾄ処理', 'reset_player.cgi'], # 別枠
		['廃人ﾗﾝｷﾝｸﾞ', 'player_ranking.cgi'],
		['主力表\', 'main_player.cgi'],
		['主力表\2', 'main_player2.cgi'],
		['一年ﾗﾝｷﾝｸﾞ', 'year_player_ranking.cgi'],
		['国別ﾗﾝｷﾝｸﾞ', 'year_player_ranking_country.cgi'],
		['人気ﾗﾝｷﾝｸﾞ(金)', 'pop_ranking_gold.cgi'], # データなし
		['人気ﾗﾝｷﾝｸﾞ(銀)', 'pop_ranking_middle.cgi'], # データなし
		['図書館', 'library.cgi'],
		['相場', 'shop_big_data.cgi'],
		['画像掲示板', '../upbbs/imgboard.cgi'],
#		['ｶﾀ~ﾉｱﾌﾟﾘ', 'CatasoApp-release-signed.apk'], # ファイルだからここじゃないとして、まずファイルがない
#		['', ''],
	);

	my $navi_html = '<div class="navi">';
	$navi_html .= qq|<form action="$navigator[0][1]">\n<input type="submit" value="$navigator[0][0]" class="navi_button">\n</form>|;
	$navi_html .= qq|<form action="$navigator[1][1]">\n<input type="submit" value="$navigator[1][0]" class="navi_button">\n</form>|;
	$navi_html .= qq|<form action="$navigator[2][1]">\n<input type="submit" value="$navigator[2][0]" class="navi_button">\n</form><br>|;
	$navi_html .= qq|<form action="$navigator[3][1]" style="width:100% !important;">\n<input type="submit" value="$navigator[3][0]" class="navi_button" style="width:240px;">\n</form><br>|;
	for $i (4 .. $#navigator) {
		$navi_html .= qq|<form action="$navigator[$i][1]">\n<input type="submit" value="$navigator[$i][0]" class="navi_button">\n</form>|;
#		if ($i > 3) {
		if ($i < $#navigator) {
			$navi_html .= qq|<br class="smart_br">| if ($i-3) % 3 == 0;
			$navi_html .= qq|<br class="tablet_br">| if ($i-3) % 5 == 0;
		}
#		}
#		else {
#			$navi_html .= qq|<br>| if $i > 1;
#		}
	}
	$navi_html .= '</div>';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;

	my @lines = &get_countries_mes();

	my $country_html;
	$country_html .= qq|ﾛｸﾞｲﾝ中 $cs_c{all}人 [<font color="$cs{color}[0]">$cs{name}[0]</font> $cs_c{0}人]<br>|;
	$country_html .= qq|<table cellpadding="4" class="blog_letter">|; # blog_letter はそのうち table3 に
	my $c_count = defined $cs_c{0} ? $cs_c{0} : 0;
	$country_html .= qq|<tr><td colspan="2">$c_count人:$cs_c{"0_member"}</td></tr>\n| if $cs_c{"0_member"};
	for my $i (1 .. $w{country}) {
		my $c_count = defined $cs_c{$i} ? $cs_c{$i} : 0;
		my($country_mes, $country_mark) = split /<>/, $lines[$i];
		$country_mark = 'non_mark.gif' if $country_mark eq '';
		$country_html .= qq|<tr><td><img src="$icondir/$country_mark"></td>|;
		$country_html .= qq|<td style="color: #333; background-color: $cs{color}[$i];width:100%;"><b>$cs{name}[$i]</b> $cs{ceo}[$i]<br>$country_mes</td></tr>\n|;
		$country_html .= qq|<tr><td colspan="2">$c_count人:$cs_c{"${i}_member"}</td></tr>\n| if $cs_c{"${i}_member"};
	}
	$country_html .= qq|</table>|;

	print <<"EOM";
$login_box_html
<p style="text-align:center;">
<a href="#attention">アクセス規制について</a>
</p>
<hr>
$navi_html
<hr>
$country_html
<hr>
定員[ $w{player}/$max_entry人 ]<br>
ﾌﾟﾚｲﾔｰ保存期間 $auto_delete_day日(1世代目Lv.1は1日)<br>
基本拘束時間 $GWT分<br>
給与 $salary_hour時間毎 君主の任期 $reset_ceo_cycle_year年周期
<hr>
<ol>
<li><a href="reset_player.cgi">ﾘｾｯﾄ処理</a>
<li><a href="CatasoApp-release-signed.apk">ｶﾀ~ﾉｱﾌﾟﾘ</a>
</ol>
<hr>
<p>
<a name="attention">アクセス規制について</a><br>
複垢作り放題になるためIPアドレスを秘匿する機能\を使ったアクセスは規制しています。以下の例に当てはまる場合には、それぞれの機能\をオフにすることでアクセスできるようになります。
</p>
<ol>
<li>Chrome：データセーバーがオンになっている</li>
<li>Opera：Turbo(オフロード)モードがオンになっている</li>
<li>Mercury：圧縮を有効にしている</li>
<li>Opera Max：使用しているブラウザによるデータ通信を制限している</li>
</ol>
<hr>
<form method="$method" action="login.cgi">
<div>ﾌﾟﾚｲﾔｰ名:<input type="text" name="login_name" value="$cook_name"></div>
<div>ﾊﾟｽﾜｰﾄﾞ:<input type="password" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>次回から入力省略(Cookie対応携帯のみ)</div>
<div><input type="submit" value="ﾛｸﾞｲﾝ"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
EOM
}
=pod
<ol>
<li><a href="readme.html">Readme</a>
<li><a href="http://www13.atwiki.jp/blindjustice/">説明書</a>
<li><a href="http://www43.atwiki.jp/bjkurobutasaba/">Wiki</a>
<li><a href="new_entry.cgi">新規登録</a>
<li><a href="../upbbs/imgboard.cgi">画像掲示板</a>
<li><a href="players.cgi">ﾌﾟﾚｲﾔｰ一覧</a>
<li><a href="legend.cgi">悠久の石碑</a>
<li><a href="sales_ranking.cgi">商人ﾗﾝｷﾝｸﾞ</a>
<li><a href="contest.cgi">ｺﾝﾃｽﾄ会場</a>
<li><a href="news.cgi">過去の栄光</a>
<li><a href="$home_m">HOME</a>
<li><a href="reset_player.cgi">ﾘｾｯﾄ処理</a>
<li><a href="player_ranking.cgi">廃人ﾗﾝｷﾝｸﾞ</a>
<li><a href="main_player.cgi">主力表\</a>
<li><a href="main_player2.cgi">主力表\2</a>
<li><a href="year_player_ranking.cgi">一年ﾗﾝｷﾝｸﾞ</a>
<li><a href="year_player_ranking_country.cgi">国別ﾗﾝｷﾝｸﾞ</a>
<li><a href="pop_ranking_gold.cgi">人気ﾗﾝｷﾝｸﾞ(金)</a>
<li><a href="pop_ranking_middle.cgi">人気ﾗﾝｷﾝｸﾞ(銀)</a>
<li><a href="library.cgi">図書館</a>
<li><a href="shop_big_data.cgi">相場</a>
<li><a href="CatasoApp-release-signed.apk">ｶﾀ~ﾉｱﾌﾟﾘ</a>
</ol>
<hr>
ﾛｸﾞｲﾝ中$cs_c{all}人
<div>$login_list</div>
<hr>
定員 $w{player}/$max_entry人<br>
ﾌﾟﾚｲﾔｰ保存期間 $auto_delete_day日<br>
(1世代目1ﾚﾍﾞﾙは1日)<br>
基本拘束時間 $GWT分<br>
給与 $salary_hour時間毎<br>
君主の任期 $reset_ceo_cycle_year年周期
<hr>
#ここから下は改装中の見本<br>
#スマホ縦画面：<a href="http://www.pandora.nu/nyaa/cgi-bin/upbbs/img-box/img20160620044658.png">img20160620044658.png</a><br>
#スマホ横画面：<a href="http://www.pandora.nu/nyaa/cgi-bin/upbbs/img-box/img20160620044721.png">img20160620044721.png</a><br>
#↑みたくなってなかったらとりあえずリロードしたりブラウザの再起動<br>
#それでもダメなら使ってる端末とブラウザを nanamie に手紙で報告
#<hr>
=cut

1; # 削除不可
