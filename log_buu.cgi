#!/usr/local/bin/perl

#===========================================================
# jinro: Version 1 maziro  過去ログ参照専用
#===========================================================

require './lib/jcode.pl';
require './config.cgi';
require './douke/lib_jinro.cgi';

#-[ 設定開始 ]-----------------------------------------------------------

# ゲーム名
$sys_title = "道化の預言";
# 画像フォルダ
$imgpath = "./douke/img2/";
#CGI パスファイル名
$cgi_path = "log_buu.cgi";
# プレイヤーデータディレクトリ
$dat_dir = "./douke/playlog/";
# プレイヤーデータ パスファイル名 (拡張子無し)
$dat_path = "./douke/playlog/dat_buu";
# ログデータ パスファイル名 (拡張子無し)
$log_path = "./douke/playlog/log_buu";
# 戻りパス
$return_url = "chat_casino.cgi";
# ロックファイル パス
$lock_path = "./douke/lock/jinro.loc";
# ID & PASSWORD
$sys_ID[1] = 'arum';
$sys_ID[2] = 'amam';
$sys_ID[3] = 'tott';
$sys_ID[4] = '0004';
$sys_ID[5] = '0005';
$sys_ID[6] = '0006';

$sys_pass[1] = 'pass';
$sys_pass[2] = '2222';
$sys_pass[3] = '3333';
$sys_pass[4] = '4444';
$sys_pass[5] = '5555';
$sys_pass[6] = '6666';

$sys_name[1] = '亜留間　次郎';
$sys_name[2] = '雨宮';
$sys_name[3] = 'とっとと';
$sys_name[4] = '管理者４番';
$sys_name[5] = '管理者５番';
$sys_name[6] = '管理者６番';

#キャラクター
$chr_hum = '村　人';
$chr_wlf = '人　狼';
$chr_ura = '占い師';
$chr_nec = '霊能者';
$chr_mad = '狂　人';
$chr_fre = '共有者';
$chr_bgd = '狩　人';
$chr_fox = '妖　孤';
$chr_rol = '猫　又';

#-[ 設定終了 ]-----------------------------------------------------------

$ENV{'TZ'} = "JST-9";

$wk_color[1] = "#DDDDDD";
$wk_color[2] = "#999999";
$wk_color[3] = "#FFFF33";
$wk_color[4] = "#FF9900";
$wk_color[5] = "#FF0000";
$wk_color[6] = "#99CCFF";
$wk_color[7] = "#0066FF";
$wk_color[8] = "#00EE00";
$wk_color[9] = "#CC00CC";
$wk_color[10] = "#FF9999";


# Japanese KANJI code
if (-f "jcode.pl") {
	$jflag = 1;
	require "jcode.pl";
	$code = ord(substr("漢", 0, 1));
	if ($code == 0xb4) {
		$ccode = "euc";
	} elsif ($code == 0x1b) {
		$ccode = "jis";
	} else {
		$ccode = "sjis";
	}
}

&decode;
&read_user;
&read_cs;
$return_url .= "?id=$id&pass=$pass";

# File lock
foreach $i ( 1, 2, 3, 4, 5, 6 ) {
		if (mkdir($lock_path, 0755)) {
				last;
		} elsif ($i == 1) {
				($mtime) = (stat($lock_path))[9];
				if ($mtime < time() - 600) {
						rmdir($lock_path);
				}
		} elsif ($i < 6) {
				sleep(2);
		} else {
				&disp_head1;
				print "<H1>ファイルロック</H1>\n";
				print "再度アクセスお願いします。<BR>\n";
				print "<A href='javascript:window.history.back()'>戻る</A>\n";
				&disp_foot;
				exit(1);
		}
}

# Remove lockfile when terminated by signal
sub sigexit { rmdir($lock_path); exit(0); }
$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = "sigexit";

# Write current message. EDATA
($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime(time);
	$date = sprintf("%02d/%02d-%02d:%02d",$mon + 1, $mday, $hour, $min);

$sys_loginflg = $in{'TXTLOGIN'};
$sys_plyerno  = 0;
if ($in{'TXTPNO'} ne ''){
	$sys_plyerno  = $in{'TXTPNO'};
}
$sys_village = $in{'VILLAGENO'};
$sys_logviewflg = 0;
$sys_storytype = $in{'STORYTYPE'};

# FileName
$cnt = sprintf("%06d",$sys_village);
$file_pdata = $dat_path.$cnt.".bak";
$tmp_pdata  = $dat_path.$cnt.".tmp";
$file_log   = $log_path.$cnt.".bak";
$tmp_log    = $log_path.$cnt.".tmp";

#cookie
if ($in{'COMMAND'} eq 'ENTER') {
	print &setCookie('SELECTROOM', $in{'VILLAGENO'});
}
if ($in{'COMMAND'} eq 'LOGIN') {
	print &setCookie('PLAYERNO'.$sys_village, $in{'CMBPLAYER'});
	print &setCookie('PASSWORD'.$sys_village, $in{'TXTPASS'});
}

print "Content-type: text/html\n";
print "\n";

# ***************************************************************** ログイン有無
if ($in{'TXTLOGIN'} ne '') {
	#--------------------------------------------------------------------- ログ閲覧
	if ($in{'COMMAND'} eq 'LOGVIEW') {
		$sys_loginflg = '2';
		$sys_plyerno = 60;
		$sys_logviewflg = 1;
	}
	#=================================================================== ログインＯＫ
	if ($sys_loginflg eq '2') {
		# 現在の状態を確認
		if( open(IN, $file_pdata)){
			$wk_count = 0;
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				$wk_count++;
				if ($wk_count == 1){
					@data_vildata = split(/,/, $value);
				}else{
					@wk_player = split(/,/, $value);
					for ($i = 0; $i <= 14; $i++) {
						$data_player[$wk_count-1][$i] = $wk_player[$i];
					}
				}
			}
		}else{
			print "<TR><TD>◆ファイルオープンエラー：$file_pdata</TD></TR>\n";
		}
		close(IN);
		
		
		# [ HEAD ]
		&disp_head2;

		# [ PLAYER LIST ]
		&disp_players;

		# [ MY DATA ]
		&disp_mydata;
		
		if ($sys_logviewflg != 1 || $sys_storytype != "2"){
			print "<TR><TD class=\"CLSTD01\">◆ 出来事</TD></TR>\n";
			print "<TR><TD>\n";
			# [ 日付 ]
			&disp_time(@data_vildata);
			print "<BR>\n";
			# [ コメント ]
			&disp_msg;
			print "</TD></TR>\n";
		}
		
		# [ 行動設定 ]
		&disp_command;
		
		# [ コメントdead ]
		&disp_msgdead;
		
		# [ ログ ]
		&disp_msgall;
		
	}
	
	print "</TD></TR>\n";
	print "<TR><TD class=\"CLSTD01\"><A href=\"$return_url\">戻る</A>\n";
	print "<INPUT type=\"hidden\" name=\"TXTPNO\" value=\"$sys_plyerno\">";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"2\">";
	$wk_rnd = int(rand(1000000)) + 1;
	print "<INPUT type=\"hidden\" name=\"FORMID\" value=\"$wk_rnd\">";
	print "</TD></TR>\n";
} else {
	# ***************************************************************** ログインなし
	
	&disp_head1;
	
	#参照するログを選択する画面へ
	&disp_logview_back;
}

# [ FOOT ]
&disp_foot;

# Lock解除
rmdir($lock_path);
