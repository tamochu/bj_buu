#! /usr/local/bin/perl -I./lib
#
# modcheck.cgi
# Perl module check program
# List all Perl modules installed in the server and display them and
# their versions
# Version numbers only display when the packages use $VERSION in it.
#
# サーバーにインストールされているPerlのモジュールをチェックするプログラム
# modcheck.cgiをサーバーにインストールし、ブラウザで表示するとモジュールの
# ファイル名、パッケージ名、バージョンのリストが表示されます。
# バージョンは、$VERSIONをPackage内で使っている場合のみ表示されます。
#
# 1.001 : 2/15/08 : Added dummy mode
# 1.0 : 1/27/08 : Created
#
# http://www.hidekik.com/
# Copyright(c) 2008, Hideki Kanayama All Rights Reserved

use strict;
use CGI::Carp qw(fatalsToBrowser);
use File::Find;

# If include path name into displaying file name, set 1.
# If display only file name, set 0.
# 表示ファイル名にパス名を含む場合は、1, ファイル名のみの場合は、0。
my $include_path = 0;

# サーバーの負担を減らすために実際のモジュールを検索せずにダミーのhtmlを表示するモード
my $dummy_mode = 0;

# ダミーモードのhtmlファイル
my $dummy_html = "modcheck_disp.html";

if ($dummy_mode){
    print "Content-Type: text/html\n\n";
    if (open(HTML, "< $dummy_html")){
	while (<HTML>){
	    print;
	}
	close(HTML);
    } else {
	print "ダミーHTMLファイル$dummy_htmlがオープンできません。\n";
    }
    exit;
}

my $version = "1.0";
my $lastupdatedyear = "2008";
my $mysite = 'http://www.hidekik.com/';

print <<END;
Content-Type: text/html

<html>
<head>
<title>Perl modules</title>
</head>
<body>
<center>
<a href="modcheck.html">Back</a>
<p>
Perl Version : $]<br>
OS Version : $^O<p>
<table cols=4 width=50% border=1>
<tr>
    <th>&nbsp;</th>
<th>File name</th>
<th>Package name</th>
<th>Versoin</th>
</tr>
END

    my @modules;
my $count = 1;

find (\&wanted, @INC);


print <<END;
</table>
</center>
<div align=\"right\"><i>modcheck.cgi $version<br>Copyright(c) $lastupdatedyear, <a href=\"$mysite\" target=\"_blank\">hidekik.com</a></i></div>
<body>
</html>
END

sub wanted {
    my $pmname = $File::Find::name;
    my $pm = $_;
    if ($pmname =~ /\.pm$/){
	if (open (MOD, "< $pmname")){
	    print "<tr align=center>\n";
	    my $hit = 0;
	    my $file = $include_path ? $pmname : $pm;
	    print "<td nowrap>$count</td>\n<td nowrap>$file</td>\n";
	    while (<MOD>){
		if ($hit == 0 and /^\s*package\s+(\S+)\s*;/){
		    print "<td nowrap>$1</td>\n";
		    $hit = 1;
		} elsif ($hit and /VERSION\s*=\s*[\'\"]?\s*([\d\.\w]+)\s*[\'\"]?\s*;/){
		    print "<td nowrap>$1</td>\n";
		    last;
		}
	    }
	    close(MOD);
	    print "</tr>\n";
	}
	$count++;
    }
}

