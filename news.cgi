#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# ﾆｭｰｽ表示 Created by Merino
#================================================

# 表示するもの(./log/にあるもの)　追加削除並べ替え可能
my @files = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名'],
	['過去の栄光',	'world_news',		],
	['世界情勢',	'world_big_news',	],
	['物流情報',	'send_news',		],
	['闘技場の軌跡','colosseum_news',	],
	['新着ﾌﾞﾛｸﾞ',	'blog_news',		],
	['新作絵画',	'picture_news',		],
	['新作本',		'book_news',		],
);

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="ＴＯＰ" class="button1"></form>|;
	}
	
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="./amida.cgi?id=$in{id}&pass=$in{pass}">ｱﾐﾀﾞｸｼﾞ</a> / |;

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	print qq|<font size="1">※画像が表\示されていないものは、その人のﾏｲﾋﾟｸﾁｬからなくなったものです</font><br>| if $files[$in{no}][1] eq 'picture_news';
	
	open my $fh, "< $logdir/$files[$in{no}][1].cgi" or &error("$logdir/$files[$in{no}][1].cgiﾌｧｲﾙが読み込めません");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}
