#!/usr/local/bin/perl --

#┌─────────────────────────────────
#│ Perl Checker v2.21 (2002/09/07)
#│ Copyright(C) Kent Web 2002
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'PerlChecker v2.21';
#┌─────────────────────────────────
#│ [使用方法]
#│   1. このスクリプト (pcheck.cgi) をCGI実行可能なディレクトリに
#│      置いて、パーミッションを 755 に設定します。
#│   2. ブラウザで直接アクセスするとチェックフォームが現れますので、
#│      フォーム内にチェックしたいCGIスクリプトのファイル名を入力
#│      します。（別ディレクトリにある場合にはパス付きで指定）
#│
#│	▼例(1) 同一ディレクトリ内の test.cgi をチェック
#│
#│		→  test.cgi と入力
#│
#│	▼例(2) 平行の位置にある testディレクトリ内の test.cgi を
#│             チェック
#│
#│		→  ../test/test.cgi と入力
#│
#│   3. チェックするCGIスクリプトの拡張子は .cgi .pl .xcg の3種
#│      のみです。
#│
#│ [留意事項]
#│   1. このプログラムはフリーソフトです。
#│   2. このプログラムを使用したいかなる損害に対して作者は一切の
#│      責任を負いません。
#└─────────────────────────────────

#------------#
#  基本設定  #
#------------#

# パスワード
# → 英数字でパスワードを指定すると、このプログラムの実行には
#    パスワードが必須となります。(英数字で8文字以内で指定)
$pass = '';

#------------#
#  設定完了  #
#------------#

print "Content-type: text/html\n\n";
print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size:13px; }
.red { color:#DD0000; }
.silver { background:#e0e0e0; }
A:link    { text-decoration:none; }
A:visited { text-decoration:none; }
A:active  { text-decoration:none; }
A:hover   { text-decoration:underline; color:#DD0000; }
-->
</STYLE>
<title>$ver</title></head>
<body bgcolor="white" text="black" link="blue" vlink="blue">
<center><hr width=400>
EOM

if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
}
@buf = split(/&/, $buf);
foreach (@buf) {
	($key, $val) = split(/=/);
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$val =~ s/\0//g;
	$val =~ s/\+//g;
	$val =~ s/&//g;
	$val =~ s/"//g;
	$val =~ s/>//g;
	$val =~ s/<//g;

	$in{$key} = $val;
}
$file = $in{'file'};

# パスチェック
if ($pass ne '') {
	if ($in{'pass'} eq '') {
		print "<P>パスワードを入力してください\n";
		print "<form action=\"pcheck.cgi\" method=\"POST\">\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=\" 認証 \"></form>\n";
		print "<hr width=400></center>\n</body></html>\n";
		exit;
	}
	elsif ($in{'pass'} ne $pass) {
		&error('<pre>パスワードが違います');
	}
}

print <<"EOM";
<h3>Perl文法チェッカー</h3>
<table><tr><td>
<UL>
<LI>フォーム内にチェックするファイル名を入力してください。
<LI>拡張子は <tt>.cgi .pl .xcg</tt> のみ有効です。
<P>syntax OK →　文法上正しい<br>
syntax error →　文法エラー
</UL>
</td></tr></table>
<form action="pcheck.cgi" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=text name=file size=35 value="$file">
<input type=submit value="チェック">
<P>
EOM

if ($in{'file'}) {

	print "<span class=silver><b>- 診断結果 -</b></span><br><br>\n";

	# ファイルチェック
	if ($file !~ /^[\.\/\w\-]+\.(cgi|pl|xcg)$/) {
		&error("ファイル名が不正です → $file");
	}
	unless (-e $file) { &error('ファイルが存在しません'); }

	# 先頭行読み取り
	open(IN,"$file");
	$top = <IN>;
	close(IN);

	print "<table border=1 cellpadding=8 cellspacing=1>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>改行形式</font></td>";
	print "<td bgcolor='#FFFFCC'>";

	# 改行判定
	if ($top =~ /(.*)\x0D\x0A$/) { print "CR+LF (Win形式)"; $ppath = $1; }
	elsif ($top =~ /(.*)\x0D$/) { print "CR（Mac形式)"; $ppath = $1; }
	elsif ($top =~ /(.*)\x0A$/) { print "LF (UNIX形式)"; $ppath = $1; }
	else { print "不明"; $ppath = '不明'; }
	print "</td></tr>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>Perlのパス</font></td>\n";
	print "<td bgcolor='#FFFFCC'><TT>$ppath</TT></td></tr>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>サーバのPerl<br>とのチェック</font></td>";
	print "<td bgcolor='#FFFFCC'>";

	# パスチェック
	$ppath =~ s/^\#\!\s*//g;
	if (-e $ppath) { print "合っています<br><TT>$ppath</TT></td></tr>\n"; }
	else { print "パスが不正のようです<br><TT>$ppath</TT></td></tr>\n"; }

	# パーミッション
	print "<tr><td bgcolor='#0000DD'><font color='white'>パーミッション</font></td>";
	print "<td bgcolor='#FFFFCC'>";
	if (-x $file) { print "実行権あり</td></tr>\n"; }
	else { print "実行権がありません</td></tr>\n"; }

	# 文法チェック
	print "<tr><td bgcolor='#0000DD'><font color='white'>文法チェック</font></td>";
	print "<td bgcolor='#FFFFCC'>";
	print "<PRE CLASS=red>\n";

	# チェック実行
	open(PROC,"perl -c $file 2>&1 |");
	print <PROC>;
	close(PROC);

	print "</PRE></td></tr></table>\n";
}

print <<"EOM";
<P><hr width=400>
<P><span style="font-family:verdana;font-size:11px;"><b>$ver</b><br>
<!-- 著作権表\記：削除禁止 -->
Copyright (C)
<a href='http://www.kent-web.com/'>Kent Web</a>
 2002
</span></center>
</body>
</html>
EOM
exit;

## エラー処理
sub error {
	print <<"EOM";
<P>$_[0]
</PRE>
<P><hr width=400></center>
</body>
</html>
EOM
	exit;
}

__END__

