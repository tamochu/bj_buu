#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# お絵描きCGI(SP用) powered by nanamie
#================================================

# 画像の横幅
my $image_width = 48;

# 画像の縦幅
my $image_height = 48;

# ﾃﾞﾌｫﾙﾄの出力(0:JPEG,1:PNG)
$in{is_wish_png} ||= 0;

#================================================
&decode;
&spp_header;
&read_user;

my $goods_c = &my_goods_count("$userdir/$id/picture");
&error("$max_my_picture個以上絵を所有することができません") if $goods_c >= $max_my_picture + $m{sedai} * 3;

my $image_size = 5000;

&header_myroom;
&run;
&footer;
exit;

#================================================
sub run {
	print !$in{is_wish_png} ? qq|JPEG / | : qq|<a href="?id=$id&pass=$pass&is_wish_png=0">JPEG</a> / |;
	print $in{is_wish_png} ? qq|PNG / | : qq|<a href="?id=$id&pass=$pass&is_wish_png=1">PNG</a> / |;
	
	my $sub_title = '(JPEG出力)';
	if (!$is_force_jpeg && $in{is_wish_png}) {
		print qq|<p>基本はPNGで出力されますが、圧縮の関係により稀にJPEGになる場合もあります。</p>|;
		$sub_title = '(PNG出力)';
	}
	print qq|<h3>SPPainter $sub_title</h3>|;

	&spp;
	&_common_param;
	&read_me;
}


#================================================
# 共通param
#================================================
sub _common_param {
	print <<"EOM";
	<datalist id="colors">
		<option value="#000000"></option>
		<option value="#808080"></option>
		<option value="#c0c0c0"></option>
		<option value="#ffffff"></option>
		<option value="#0000ff"></option>
		<option value="#000080"></option>
		<option value="#008080"></option>
		<option value="#008000"></option>
		<option value="#00ff00"></option>
		<option value="#00ffff"></option>
		<option value="#ffff00"></option>
		<option value="#ff0000"></option>
		<option value="#ff00ff"></option>
		<option value="#808000"></option>
		<option value="#800080"></option>
		<option value="#800000"></option>
	</datalist>
	<param name="image_width" id="image_width" value="$image_width">
	<param name="image_height" id="image_height" value="$image_height">
	<param name="image_size" id="image_size" value="$image_size">
	<param name="send_header" id="send_header" value="id=$id&pass=$pass&time=$time;">
	<param name="url_save" id="url_save" value="oekaki_spp_save.cgi">
	<param name="id" id="id" value="$id">
	<param name="pass" id="pass" value="$pass">
</applet>
EOM
}

sub spp {
	print <<"EOM";
<div>ブラウザ依存がどうにもならないのでページ下部を参照し対応しているブラウザを利用してください。</div>

<form>
	<table id="canvas">
		<tr>
			<td>
				<canvas id="cv" width="480px" height="480px" style="background-color:#ffffff;"></canvas>
			</td>
			<td>
				<table id="tools">
					<tr>
						<td><button type="button" id="pen" value="pen" class="on">〆</button>
						<td><button type="button" id="line" value="line" class="off">ー</button></td>
						<td><button type="button" id="dropper" value="dropper" class="off">♀</button></td>
					</tr>
					<tr>
						<td><button type="button" id="fillrect" value="fillrect" class="off">■</button></td>
						<td><button type="button" id="rect" value="rect" class="off">□</button></td>
						<td><button type="button" id="paint" value="paint" class="off">※</button></td>
					<tr>
						<td><button type="button" id="fillarc" value="fillarc" class="off">●</button></td>
						<td><button type="button" id="arc" value="arc" class="off">○</button></td>
						<td><button type="button" id="cutrect" value="cutrect" class="off">cut</button></td>
					</tr>
					<tr>
						<td>R：<span id="_r">0</span></td>
						<td colspan="2">
							<input type="range" name="r" min="0" max="255" value="0" id="r">
						</td>
					</tr>
					<tr>
						<td>G：<span id="_g">0</span></td>
						<td colspan="2">
							<input type="range" name="g" min="0" max="255" value="0" id="g">
						</td>
					</tr>
					<tr>
						<td>B：<span id="_b">0</span></td>
						<td colspan="2">
							<input type="range" name="b" min="0" max="255" value="0" id="b">
						</td>
					</tr>
					<tr>
						<td>色：</td>
						<td colspan="2"><input type="color" list="colors" value="#000000" id ="color" style="width:100%;"></td>
					</tr>
					<tr>
						<td>背景色：</td>
						<td colspan="2"><input type="color" name="backcolor" value="#ffffff" list="colors" id="backcolor" style="width:100%;"></td>
					</tr>
					<tr>
						<td>太さ：<span id="_weight">12</span></td>
						<td colspan="2">
							<input type="range" name="weight" min="12" max="32" value="12" id="weight">
						</td>
					</tr>
					<tr>
						<td>透度：<span id="_alpha">0</span></td>
						<td colspan="2">
							<input type="range" name="alpha" min="0" max="10" value="0" id="alpha">
						</td>
					</tr>
					<tr>
						<td><img id="newImg" style="border:1px solid #000000;width:48px;height:48px;"></td>
						<td colspan="2"><span id="ext"></span><br><span id="size"></span>B</td>
					</tr>
				</table>
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<table id="func">
					<tr>
						<td><label for="undo">undo<input type="button" id="undo" value="undo" style="display:none;"></label></td>
						<td><label for="redo">redo<input type="button" id="redo" value="redo" style="display:none;"></label></td>
						<td><label for="clear">消去<input type="button" id="clear" value="clear" style="display:none;"></label></td>
						<td><label for="file">取込<input type="file" id="file" style="display:none;"></label></td>
						<td><label for="convert">作成<input type="button" id="convert" value="convert" style="display:none;"></label></td>
						<td><label id="_send" for="send" class="disable">投稿<input type="button" id="send" style="display:none;"></label></td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
</form>
EOM
}

sub read_me {
	print qq|<a href="$htmldir/spp_table.html" target="_blank">対応ブラウザ</a>|;
}

sub spp_header {
	print "Content-type: text/html; charset=Shift_JIS\n";
	if ($gzip ne '' && $ENV{HTTP_ACCEPT_ENCODING} =~ /gzip/){  
		if ($ENV{HTTP_ACCEPT_ENCODING} =~ /x-gzip/) {
			print "Content-encoding: x-gzip\n\n";
		}
		else{
			print "Content-encoding: gzip\n\n";
		}
		open STDOUT, "| $gzip -1 -c";
	}
	else {
		print "\n";
	}
	
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
	print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
	print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">|;
	print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
	print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
	print qq|<script type="text/javascript" src="$htmldir/js/SPPainter.js?$jstime"></script>|;
	print qq|<script type="text/javascript" src="$htmldir/js/CanvasFillAlgorithm.js?$jstime"></script>|;
	print qq|<script type="text/javascript" src="$htmldir/js/b64utils.js?$jstime"></script>|;
	print qq|<link rel="stylesheet" type="text/css" href="$htmldir/css/SPPainter.css?$jstime">|;
	print qq|</head><body $body><a name="top"></a>|;
}