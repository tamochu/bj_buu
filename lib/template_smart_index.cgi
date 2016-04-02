#================================================

# index.cgiﾃﾝﾌﾟﾚｰﾄ(スマホ) Created by Merino

#================================================



#================================================

sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;

	print <<"EOM";
<h1>$title</h1>
<form method="$method" action="login.cgi">
<div>ﾌﾟﾚｲﾔｰ名:<input type="text" name="login_name" value="$cook_name"></div>
<div>ﾊﾟｽﾜｰﾄﾞ:<input type="password" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>次回から入力省略(Cookie対応携帯のみ)</div>
<div><input type="submit" value="ﾛｸﾞｲﾝ"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
<ol>
<li><a href="http://buu.pandora.nu/cgi-bin/bj/user/8d9593d8/book/526561646d65208dec3a8d9593d8.html">Readme</a>
<li><a href="http://www13.atwiki.jp/blindjustice/">説明書</a>
<li><a href="http://www43.atwiki.jp/bjkurobutasaba/">Wiki</a>
<li><a href="new_entry.cgi">新規登録</a>
<li><a href="players.cgi">ﾌﾟﾚｲﾔｰ一覧</a>
<li><a href="legend.cgi">悠久の石碑</a>
<li><a href="sales_ranking.cgi">商人ﾗﾝｷﾝｸﾞ</a>
<li><a href="contest.cgi">ｺﾝﾃｽﾄ会場</a>
<li><a href="news.cgi">過去の栄光</a>
<li><a href="$home_m">HOME</a>
<li><a href="reset_player.cgi">ﾘｾｯﾄ処理</a>
<li><a href="player_ranking.cgi">廃人ﾗﾝｷﾝｸﾞ</a>
<li><a href="main_player.cgi">主力表\</a>
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
(1世代目1ﾚﾍﾞﾙは5日)<br>
基本拘束時間 $GWT分<br>
給与 $salary_hour時間毎<br>
君主の任期 $reset_ceo_cycle_year年周期
<hr>
EOM
}


1; # 削除不可
