#=================================================
# ﾌﾟﾛﾌｨｰﾙ設定 Created by Merino
#=================================================
# ◎追加/削除/変更/並び替え可
# ﾌﾟﾛﾌｨｰﾙで表示するもの。左の英字は同じじゃなければ何でも良い

my @files = (
	['手紙',	'letter'],
	['日記',	'blog'],
	['お絵描き','oekaki'],
	['本作成',	'book'],
);


#=================================================
# ﾌﾟﾛﾌｨｰﾙﾍｯﾀﾞｰ
#=================================================
sub header_myroom {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;

	for my $i (0 .. $#files) {
		next if $is_mobile && $files[$i][1] eq 'oekaki';
		print $in{no} eq $i ? qq| $files[$i][0] /| : qq| <a href="$files[$i][1].cgi?id=$id&pass=$pass&no=$i">$files[$i][0]</a> /|;
	}
	print qq|<h1>$files[$in{no}][0]</h1>|;
}


1; # 削除不可
