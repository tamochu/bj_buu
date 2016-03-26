#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# お絵描きCGI(PC専用) Created by Merino
#================================================
# 【しぃ堂 Shi-dow】http://shichan.jp/ から
# ・PaintBBSをﾀﾞｳﾝﾛｰﾄﾞして「PaintBBS.jar」を同階層に置いてね
# ・しぃペインター通常(sptr1114.zip)をﾀﾞｳﾝﾛｰﾄﾞして「spainter.jar、res(フォルダ)」を同階層に置いてね

# 画像の横幅
my $image_width = 48;

# 画像の縦幅
my $image_height = 48;

# お絵描きﾀｲﾌﾟ ◎追加/変更/削除/並び換え可能
# 一番上のものがﾃﾞﾌｫﾙﾄになります
# 使いたくないお絵描きは先頭に(#をつけると選択できなくなります)
# ------------------
# 例＞Paint BBSだけにしたい場合
# ['paint_bbs',		'Paint BBS'],
# #['shi_painter',		'しぃペインター'],
# #['shi_painter_pro',	'しぃペインターPro'],
# ------------------
my @types = (
	# ｻﾌﾞﾙｰﾁﾝ名,		'ﾀｲﾄﾙ'
	['paint_bbs',		'Paint BBS'],
	['shi_painter',		'しぃペインター'],
	['shi_painter_pro',	'しぃペインターPro'],
);

# ﾃﾞﾌｫﾙﾄの出力(0:JPEG,1:PNG)
$in{is_wish_png} ||= 0;


# ----------------------------
# 荒らし/手抜き対策

# 画像作成時の最低ｱｸｼｮﾝ数
my $security_click = 10;

# 画像作成時の最低時間(秒)
my $security_timer = 20;


#================================================
&decode;
&header;
&read_user;

my $goods_c = &my_goods_count("$userdir/$id/picture");
&error("$max_my_picture個以上絵を所有することができません") if $goods_c >= $max_my_picture + $m{sedai} * 3;

$in{type} ||= 0;
$in{type} = 0 if $in{type} !~ /\d/ || $in{type} < 0 || $in{type} > $#types;
my $image_size = 1;

&header_myroom;
&run;
&footer;
exit;

#================================================
sub run {
	for my $i (0..$#types) {
		print $in{type} eq $i && !$in{is_wish_png} ? qq|$types[$i][1](JPEG) / | : qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=$i&is_wish_png=0">$types[$i][1](JPEG)</a> / |;
		print $in{type} eq $i &&  $in{is_wish_png} ? qq|$types[$i][1](PNG) / | : qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=$i&is_wish_png=1">$types[$i][1](PNG)</a> / |;
	}
	
	my $sub_title = '(JPEG出力)';
	if (!$is_force_jpeg && $in{is_wish_png}) {
		$image_size = 60;
		print qq|<p>基本はPNGで出力されますが、圧縮の関係により稀にJPEGになる場合もあります。</p>|;
		$sub_title = '(PNG出力)';
	}
	print qq|<h3>$types[$in{type}][1] $sub_title</h3>|;

	&{ $types[$in{type}][0] };
	&_common_param;
	&read_me;
}


#================================================
# 共通param
#================================================
sub _common_param {
	print <<"EOM";
	<param name="image_width" value="$image_width">
	<param name="image_height" value="$image_height">
	<param name="image_size" value="$image_size">
	<param name="image_jpeg" value="true">
	<param name="image_bkcolor" value="#ffffff">

	<param name="compress_level" value="15">
	<param name="undo" value="60">
	<param name="undo_in_mg" value="15">
	<param name="scriptable" value="true">	

	<param name="color_text"value="#505078">
	<param name="color_bk" value="#9999bb">
	<param name="color_bk2" value="#8888aa">
	<param name="color_icon" value="#ccccff">

	<param name="color_bar" value="#6f6fae">
	<param name="color_bar_hl" value="#ffffff">
	<param name="color_bar_frame_hl" value="#eeeeff">
	<param name="color_bar_frame_shadow" value="#aaaaaa">

	<param name="send_language" value="sjis">
	<param name="send_advance" value="true">
	<param name="send_header" value="id=$id&pass=$pass&time=$time;">
	<param name="send_header_image_type" value="true">

	<param name="security_click" value="$security_click">
	<param name="security_timer" value="$security_timer">
	<param name="security_url" value="$htmldir/security_url.html">
	<param name="security_post" value="false">
	<param name="url_save" value="oekaki_save.cgi">
	<param name="url_exit" value="oekaki_exit.cgi?id=$id&pass=$pass&time=$time">
</applet>
EOM
}

#================================================
# Paint BBS param
#================================================
sub paint_bbs {
	print <<"EOM";
<applet code="pbbs.PaintBBS.class" name="paintbbs" archive="PaintBBS.jar" width="90%" height="90%" align="center" MAYSCRIPT>
	<param name="bar_size" value="20">
	<param name="tool_advance" value="true">
	<param name="poo" value="false">
	
	<param name="thumbnail_width" value="100%">
	<param name="thumbnail_height" value="100%">
EOM
}


#================================================
# しぃペインター param
#================================================
sub shi_painter {
	print <<"EOM";
<applet code="c.ShiPainter.class" name="paintbbs" archive="spainter.jar,res/normal.zip" width="90%" height="90%" MAYSCRIPT>
	<param name="MAYSCRIPT" value="true">
	
	<param name="dir_resource" value="./res/">
	<param name="tt.zip" value="./res/tt.zip">
	<param name="res.zip" value="./res/res_normal.zip">
	<param name="tools" value="normal">
	<param name="layer_count" value="3">
	<param name="quality" value="1">

	<param name="tool_color_bk" value="#aabbcc">
	<param name="tool_color_button" value="#ddeeff">
	<param name="tool_color_button_hl" value="#9900ff">
	<param name="tool_color_button_dk" value="#ff0099">
	
	<param name="tool_color_button2" value="#ffffff">
	<param name="tool_color_text" value="0">
	<param name="tool_color_bar" value="#00ff00">
	<param name="tool_color_frame" value="#ff0000">
EOM
	&_common_param_shi;
}

#================================================
# しぃペインターPro param
#================================================
sub shi_painter_pro {
	print <<"EOM";
<applet code="c.ShiPainter.class" name="paintbbs" archive="spainter.jar,res/pro.zip" WIDTH="90%" height="100%">
	<param name="dir_resource" value="./res/">
	<param name="tt.zip" value="./res/tt.zip">
	<param name="res.zip" value="./res/res_pro.zip">
	<param name="tools" value="pro">
	<param name="layer_count" value="3">
	<param name="quality" value="2">
EOM
	&_common_param_shi;
}


#================================================
# しぃペインター共通param
#================================================
sub _common_param_shi {
	print <<"EOM";
	<param name="color_frame" value="0xff">
	<param name="color_iconselect" value="#112233">
	<param name="color_bar_shadow" value="#778899"> 

	<param name="pro_menu_color_text" value="#FFFFFF">
	<param name="pro_menu_color_off" value="#222233">
	<param name="pro_menu_color_off_hl" value="#333344">
	<param name="pro_menu_color_off_dk" value="0">
	<param name="pro_menu_color_on" value="#ff0000">
	<param name="pro_menu_color_on_hl" value="#ff8888">
	<param name="pro_menu_color_on_dk" value="#660000">
	
	<param name="bar_color_bk" value="#ffffff">
	<param name="bar_color_frame" value="#ffffff">
	<param name="bar_color_off" value="#ffffff">
	<param name="bar_color_off_hl" value="#ffffff">
	<param name="bar_color_off_dk" value="#ffffff">
	<param name="bar_color_on" value="#777777">
	<param name="bar_color_on_hl" value="#ffffff">
	<param name="bar_color_on_dk" value="#ffffff">
	<param name="bar_color_text" value="0">
	
	<!--ウインドウ関係の設定-->
	<param name="window_color_text" value="#ff0000">
	<param name="window_color_frame" value="#ffff00">
	<param name="window_color_bk" value="#000000">
	<param name="window_color_bar" value="#777777">
	<param name="window_color_bar_hl" value="#888888">
	<param name="window_color_bar_text" value="#000000">
	
	<!--確認ウインドウの設定-->
	<param name="dlg_color_bk" value="#ccccff">
	<param name="dlg_color_text" value="0">
	
	<!--アプレットの背景の設定-->
	<param name=color_bk value="#9999CC">
	<param name=color_bk2 value="#888888">
	
	<!--レイヤーのメーターカラーの設定-->
	<param name=l_m_color value="#ffffff">
	<param name=l_m_color_text value="#0000ff">
EOM
}


sub read_me {
	print <<"EOM";
<table cellpadding="2" cellspacing="2" border="0">
<tbody>
	<tr valign="Top">
		<td valign="Top">
		
		<div class="mes">
		<div align="center">注意事項</div>
		<ul>
			<li>作成した画像については、著作権・肖像権等について法令上の義務に従い、<br>作成したプレイヤーの自己責任において登録・掲載されるものとします。
			<li>わいせつな表\現、差別的な表\現、残虐的な表\現など、公共の一般常識から外れた投稿は自粛してください。
			<li>某マウスやダック、ゲームKHのキャラクターなどは著作権が厳しいので注意！
		</ul>
		</div><br>

		<div style="color:#00CC00">ミスしてページを変えたりウインドウを消してしまったりした場合は落ちついて同じキャンバスの幅で<br>
		編集ページを開きなおしてみて下さい。大抵は残っています。<br>
		（WinIEやネスケ6.1の短縮起動機能\が使えないブラウザは閉じると消えます）<br><br></div>

			<div style="color: rgb(0,102,0); ">基本の動作(恐らくこれだけは覚えておいた方が良い機能\)</div>
			
			<div style="font-size: 80%; ">
				<span style="color: rgb(80,144,120); ">&lt;基本&gt;</span><br>
				
				PaintBBSでは右クリック,ctrl+クリック,alt+クリックは同じ動作をします。<br>
				基本的に操作は一回のクリックか右クリックで動作が完了します。(ベジエやコピー使用時を除く)<br>
				<br>
				
				<span style="color: rgb(80,144,120); ">&lt;ツールバー&gt;</span><br>
				ツールバーの殆どのボタンは複数回クリックして機能\を切り替える事が出来ます。<br>
				右クリックで逆周り。その他パレットの色,マスクの色,一字保存ツールに現在の状態を登録,<BR>
				レイヤ表\示非表\示切り替え等全て右クリックです。<br>
				逆にクリックでパレットの色と一時保存ツールに保存しておいた状態を取り出せます。<br>
				<br>
				
				<span style="color: rgb(80,144,120); ">&lt;キャンバス部分&gt;</span><br>
				右クリックで色をスポイトします<br>
				ベジエやコピー等の処理の途中で右クリックを押すとリセットします。
			</div>
			
			<br>
			
			<div style="color: rgb(0,102,0); ">特殊動作(使う必要は無いが慣れれば便利な機能\)</div>
				
				<div style="font-size: 80%; ">
					<span style="color: rgb(80,144,120); ">&lt;ツールバー&gt;</span><br>
					
				値を変更するバーはドラッグ時バーの外に出した場合変化が緩やかになりますので<br>
				それを利用して細かく変更する事が出来ます。<br>
				パレットはShift+クリックで色をデフォルトの状態に戻します。<br><br>
				<span style="color: rgb(80,144,120); ">&lt;キーボードのショートカット&gt;</span>
				<br>
				+で拡大-で縮小。 <br>
				Ctrl+ZかCtrl+Uで元に戻す、Ctrl+Alt+ZかCtrl+Yでやり直し。<br>
				Escでコピーやベジエのリセット。（右クリックでも同じ） <br>
				スペースキーを押しながらキャンバスをドラッグするとスクロールの自由移動。<br>
				Ctrl+Alt+ドラッグで線の幅を変更。<br><br>
				<span style="color: rgb(80,144,120);">&lt;コピーツールの特殊な利用方法&gt;</span>
				<br>
				レイヤー間の移動は現時点ではコピーとレイヤー結合のみです。コピーでの移動方法は、<br>
				まず移動したいレイヤ上の長方形を選択後、移動させたいレイヤを選択後に通常のコピーの作業を<br>
				続けます。そうする事によりレイヤ間の移動が可能\になります。<br>
				
			</div>
				<br>
			
			<div style="color: rgb(0,102,0); ">ツールバーのボタンと特殊な機能\の簡単な説明</div>
			<div style="font-size: 80%; ">

			<ul type="Circle">
				<li>ペン先(通常ペン,水彩ペン,テキスト)<br><span style="color: #CCFFFF; ">
						メインのフリーライン系のペンとテキスト</span><br><br></li>
						
				<li>ペン先2(トーン,ぼかし,他)<br><span style="color: #CCFFFF; ">
						特殊な効果を出すフリーライン系のペン</span><br><br></li>
						
				<li>図形(円や長方形)<br><span style="color: #CCFFFF; ">
						長方形や円等の図形</span><br><br></li>
						
				<li>特殊(コピーやレイヤー結合,反転等)<br><span style="color: #CCFFFF; ">
						コピーは一度選択後、ドラッグして移動、コピーさせるツールです。</span><br><br></li>
						
				<li>マスクモード指定(通常,マスク,逆マスク）<br><span style="color: #CCFFFF; ">
						マスクで登録されている色を描写不可にします。逆マスクはその逆。<br>
						通常でマスク無し。また右クリックでマスクカラーの変更が可能\。<br><br></span></li>
						
				<li>消しゴム(消しペン,消し四角,全消し)<BR><span style="color: #CCFFFF">
						透過レイヤー上を白で塗り潰した場合、下のレイヤーが見えなくなりますので<BR>
						上位レイヤーの線を消す時にはこのツールで消す様にして下さい。全消しはすべてを透過ピクセル化させるツールです。<br>
						全けしを利用する場合はこのツールを選択後キャンバスをクリックでOK。<br><br></span></li>
						
				<li>描写方法の指定。(手書き,直線,ベジエ曲線)<br><span style="color: #CCFFFF; ">
						ペン先,描写機能\指定ではありません。<br>
						また適用されるのはフリーライン系のツールのみです。</span><br><br></li>
						
				<li>カラーパレット郡<br><span style="color: #CCFFFF; ">
						クリックで色取得。右クリックで色の登録。Shift+クリックでデフォルト値。</span><br><br></li>
						
				<li>RGBバーとalphaバー<br><span style="color: #CCFFFF; ">
						細かい色の変更と透過度の変更。Rは赤,Gは緑,Bは青,Aは透過度を指します。<br>
						トーンはAlphaバーで値を変更する事で密度の変更が可能\です。</span><br><br></li>
						
				<li>線幅変更ツール<br><span style="color: #CCFFFF; ">
						水彩ペンを選択時に線幅を変更した時、デフォルトの値がalpha値に代入されます。</span><br><br></li>
				
				<li>線一時保存ツール<br><span style="color: #CCFFFF; ">
						クリックでデータ取得。右クリックでデータの登録。(マスク値は登録しません)</span><br><br></li>
				
				<li>レイヤーツール<br><span style="color: #CCFFFF; ">
				PaintBBSは透明なキャンバスを二枚重ねたような構造になっています。<br>
				つまり主線を上に書き、色を下に描くと言う事も可能\になるツールです。<br>
				通常レイヤーと言う種類の物ですので鉛筆で描いたような線もキッチリ透過します。<br>
				クリックでレイヤー入れ替え。右クリックで選択されているレイヤの表\示、非表\示切り替え。</span><br><br></li>	
			</ul>
			
			</div>
			<span style="color: rgb(0,102,0); ">投稿に関して：</span>
			<div style="font-size: 80%; ">
				絵が完成したら投稿ボタンで投稿します。<br>
				絵の投稿が成功した場合は指定されたURLへジャンプします。<br>
				失敗した場合は失敗したと報告するのみでどこにも飛びません。<br>
				単に重かっただけである場合少し間を置いた後、再度投稿を試みて下さい。<br>
				この際二重で投稿される場合があるかもしれませんが、それは<br>
				WebサーバーかCGI側の処理ですのであしからず。
			</div>
		</td>
	</tr>
</tbody>
</table>
EOM
}

