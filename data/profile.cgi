#=================================================
# ﾌﾟﾛﾌｨｰﾙ設定 Created by Merino
#=================================================
# ◎追加/削除/変更/並び替え可
# ﾌﾟﾛﾌｨｰﾙで表示するもの。左の英字は同じじゃなければ何でも良い
@profiles = (
	['name',		'名前'],
	['sex',			'性別'],
	['blood',		'血液型'],
	['birthday',	'誕生日'],
	['age',			'年齢'],
	['job',			'職業'],
	['address',		'住んでいる所'],
	['hobby',		'趣味'],
	['boom',		'ﾏｲﾌﾞｰﾑ'],
	['site',		'ｵｽｽﾒｻｲﾄ'],
	['dream',		'夢/目標'],
	['motto',		'座右の銘'],
	['character',	'性格・特徴'],
	['like',		'好きなもの'],
	['dislike',		'嫌いなもの'],
	['login',		'ﾛｸﾞｲﾝ時間'],
	['work',		'主な活動/役割'],
	['ceo',			'君主になったら'],
	['boast',		'自慢'],
	['reference',	'このｻｲﾄを知ったきっかけ'],
	['message',		'何か一言'],
);


#=================================================
# ﾌﾟﾛﾌｨｰﾙﾍｯﾀﾞｰ
#=================================================
sub header_profile {
	&error('そのようなﾌﾟﾚｲﾔｰが存在しません') unless -d "$userdir/$in{id}";
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	if ($is_mobile) {
		print qq|<form method="$method" action="players.cgi"><input type="submit" value="ﾌﾟﾚｲﾔｰ一覧" class="button1"></form>|
	}
	else {
		print -f "$htmldir/$in{country}.html"
			? qq|<form action="$htmldir/$in{country}.html"><input type="submit" value="ﾌﾟﾚｲﾔｰ一覧" class="button1"></form>|
			: qq|<form action="$htmldir/0.html"><input type="submit" value="ﾌﾟﾚｲﾔｰ一覧" class="button1"></form>|
			;
	}
	
	my $name = pack 'H*', $in{id};
	print qq|<h1>$name$in{title}</h1>|;
	
	print qq|<a href="profile.cgi?id=$in{id}&country=$in{country}&mode=status&title=Status">ｽﾃｰﾀｽ</a>/|;
	print qq|<a href="profile.cgi?id=$in{id}&country=$in{country}&mode=profile&title=Profile">ﾌﾟﾛﾌｨｰﾙ</a>/| if -s "$userdir/$in{id}/profile.cgi";
	print qq|<a href="blog.cgi?id=$in{id}&country=$in{country}&title=Blog">日記</a>/| if -s "$userdir/$in{id}/blog.cgi";
	print qq|<a href="memory.cgi?id=$in{id}&country=$in{country}&title=Memory">戦歴</a>/|;
	print qq|<hr><br>|;
}


1; # 削除不可
