#================================================
# index.cgiﾃﾝﾌﾟﾚｰﾄ(PC) Created by Merino
#================================================

#================================================
sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;
	
	my @lines = &get_countries_mes();

	my $country_html;
	$country_html .= qq|ﾛｸﾞｲﾝ中 $cs_c{all}人 [<font color="$cs{color}[0]">$cs{name}[0]</font> $cs_c{0}人]<br>|;
	$country_html .= qq|<table cellpadding="4" class="table2">|;
	for my $i (1 .. $w{country}) {
		my $c_count = defined $cs_c{$i} ? $cs_c{$i} : 0;
		
		my($country_mes, $country_mark) = split /<>/, $lines[$i];
		$country_mark = 'non_mark.gif' if $country_mark eq '';
		$country_html .= qq|<tr><td><img src="$icondir/$country_mark"></td></td><td style="color: #333; background-color: $cs{color}[$i]; text-align: right;" nowrap><b>$cs{name}[$i]</b><br>$c_count人<br>$cs{ceo}[$i]<br></td><td style="width:100%;">$country_mes<br></td></tr>\n|;
	}
	$country_html .= qq|</table>|;
	my $title_html = $title_img ? qq|<img src="$title_img">| : qq|<h1>$title</h1>|;

	my $login_html = '';
	if ($cs_c{all} >= $max_login) {
		$login_box_html .= qq|<br><p style="font-size: 16px; color: #FF0; font-weight: bold;">ﾛｸﾞｲﾝ規制中</p><p>ﾛｸﾞｲﾝ人数が減るまでしばらくお待ちください。携帯からのﾛｸﾞｲﾝは可能\です。</p><br>|;
	}
	else {
		$login_box_html .= qq|<form method="$method" action="login.cgi" style="margin: 0; padding: 0;"><table class="table1">|;
		$login_box_html .= qq|<tr><th><tt>ﾌﾟﾚｲﾔｰ名:</tt></th><td><input type="text" name="login_name" value="$cook_name" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><th><tt>ﾊﾟｽﾜｰﾄﾞ:</tt></th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><td colspan="2"><input type="checkbox" name="is_cookie" value="1" $checked> <tt>次回から入力省略</tt></th></tr>|;
		$login_box_html .= qq|</table><p><input type="submit" value="[> ログイン" class="button_login"></p></form>|;
	}
	
	print <<"EOM";
<style type="text/css">
<!--
body { margin: 0; padding: 0; }
form { margin: 0; padding: 7px; }
-->
</style>
<div align="center">
<table width="840" border="0" cellpading="0" cellspacing="0" class="top_box">
<tr>
	<td valign="top">
		<div class="login_list">
			$login_list
		</div>
		<br>$country_html<br>
	</td>
	<td valign="top" align="center">
		<div class="login_box">
			Chromeのデータセーバーを無効にしないとアクセスできません
			$login_box_html
		</div>
		<div align="left" style="padding: 0.2em 2em;">
			<p><a href="readme.html" class="link1">[> Readme　</a></p>
			<p><a href="http://www13.atwiki.jp/blindjustice/" class="link1">[> 説明書　</a></p>
			<p><a href="http://www43.atwiki.jp/bjkurobutasaba/" class="link1">[> wiki　</a></p>
			<p class="text_small">質問する前に必ず読むこと!</p>
			<p><a href="new_entry.cgi" class="link1">[> 新規登録</a></p>
			<p class="text_small">登録前に説明書必読!</p>
		</div>
		
		<hr style="border: 1px dashed #CCC;">
		<form action="./html/0.html">
			<input type="submit" value="ﾌﾟﾚｲﾔｰ一覧" class="button1">
			<br><span class="text_small">数日ごとに更新</span>
		</form>
		<form method="$method" action="legend.cgi">
			<input type="submit" value="悠久の石碑" class="button1">
			<br><span class="text_small">$world_name大陸の歴史</span>
		</form>
		<form method="$method" action="contest.cgi">
			<input type="submit" value="ｺﾝﾃｽﾄ会場" class="button1">
			<br><span class="text_small">才能\の卵</span>
		</form>
		<form method="$method" action="sales_ranking.cgi">
			<input type="submit" value="売上ﾗﾝｷﾝｸﾞ" class="button1">
			<br><span class="text_small">$sales_ranking_cycle_day日ごとに更新</span>
		</form>
		<form method="$method" action="player_ranking.cgi">
			<input type="submit" value="廃人ﾗﾝｷﾝｸﾞ" class="button1">
			<br><span class="text_small">1日ごとに更新</span>
		</form>
		<form method="$method" action="main_player.cgi">
			<input type="submit" value="主力表\ " class="button1">
		</form>
		<form method="$method" action="main_player2.cgi">
			<input type="submit" value="主力表\2 " class="button1">
		</form>
		<form method="$method" action="year_player_ranking.cgi">
			<input type="submit" value="一年ﾗﾝｷﾝｸﾞ" class="button1">
			<br><span class="text_small">1年ごとに更新</span>
		</form>
		<form method="$method" action="year_player_ranking_country.cgi">
			<input type="submit" value="国別ﾗﾝｷﾝｸﾞ" class="button1">
			<br><span class="text_small">1年ごとに更新</span>
		</form>
		<form method="$method" action="pop_ranking_gold.cgi">
			<input type="submit" value="人気ﾗﾝｷﾝｸﾞ(金)" class="button1">
		</form>
		<form method="$method" action="pop_ranking_middle.cgi">
			<input type="submit" value="人気ﾗﾝｷﾝｸﾞ(銀)" class="button1">
		</form>
		<form method="$method" action="./news.cgi">
			<input type="submit" value="過去の栄光" class="button1">
			<br><span class="text_small">最近の出来事</span>
		</form>
		<form method="$method" action="library.cgi">
			<input type="submit" value="図書館" class="button1">
			<br><span class="text_small">先人の知恵</span>
		</form>
		<form method="$method" action="shop_big_data.cgi">
			<input type="submit" value="相場" class="button1">
			<br><span class="text_small">アイテム価格の推移</span>
		</form>
		<a href="https://github.com/tamochu/bj_buu">source github（大事なことは無し、入ってたら連絡ください）</a>
<br>
		<hr style="border: 1px dashed #CCC;">
		<form action="$home">
			<input type="submit" value="ＨＯＭＥ" class="button1">
		</form>
		<form method="$method" action="reset_player.cgi">
			<input type="submit" name="name" value="ﾘｾｯﾄ処理" class="button_s">
		</form>
		<form method="$method" action="search_player.cgi">
			<input type="text" name="search_name" value=""><input type="submit" value="..." class="button_s">
		</form>
	</td>
</tr>
<tr>
	<td colspan="2">
		<div class="footer">
			定員[ $w{player}/$max_entry人 ]　ﾌﾟﾚｲﾔｰ保存期間 $auto_delete_day日(1世代目Lv.1は1日)<br>
			基本拘束時間 $GWT分　給与 $salary_hour時間毎　君主の任期 $reset_ceo_cycle_year年周期
		</div>
	</td>
</tr>
<tr>
	<td colspan="2">
		<div class="footer">
			全携帯機種対応：携帯からPCと同じURLにｱｸｾｽするだけ。<br>
			ﾌﾟﾚｲﾔｰが作成した画像・ﾃｷｽﾄ等は、著作権・肖像権等について法令上の義務に従い、ﾌﾟﾚｲﾔｰの自己責任において登録・掲載されるものとします。<br>
		</div>
	</td>
</tr>
</table>

</div>
EOM
}



1; # 削除不可
