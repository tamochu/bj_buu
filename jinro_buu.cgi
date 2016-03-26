#!/usr/local/bin/perl --

#================================================================================
# jinro: Version 1 maziro
# 道化 = clowning
# 預言 = prophecy
# 2005/03/14      村人登録抹消機能を追加
# 2005/03/19      データとログファイルの保存先を変更
#                 ファイル名に付ける番号を前ゼロ付き６桁に変更
#                 村一覧の取得方法をディレクトリのファイル一覧から取得する方法に変更
# 2005/03/20      人狼の勝利時に生き残っている村人を殺すように修正
#                 アイコンを追加
# 2005/04/03      死亡者は全員無条件で敗者とする
# 2005/06/12      初日の生贄キャラを追加、最大参加数を２３人へ
#                 アイコンと管理者の一覧をファイル化
#================================================================================

require './lib/jcode.pl';
require './config.cgi';
require './douke/lib_jinro.cgi';

#-[ 設定開始 ]-----------------------------------------------------------

# ゲーム名
$sys_title = "道化の預言";
# 画像フォルダ
$imgpath = "./douke/img2/";
#CGI パスファイル名
$cgi_path = "jinro_buu.cgi";

# プレイヤーデータディレクトリ
$dat_dir = "./douke/playdata/";
# プレイヤーデータ パスファイル名 (拡張子無し)
$dat_path = "./douke/playdata/dat_buu";
# ログデータ パスファイル名 (拡張子無し)
$log_path = "./douke/playdata/log_buu";
# バックアップ パスファイル名 (拡張子無し)
$dat_path_bak = "./douke/playlog/dat_buu";
$log_path_bak = "./douke/playlog/log_buu";
#管理者情報ファイル
$sys_path_bak = "./douke/sys_id.dat";
#アイコン情報ファイル
$ico_path_bak = "./douke/icon.dat";
# 戻りパス
$return_url = "chat_casino.cgi";
# ロックファイル パス
$lock_path = "./douke/lock/jinro.loc";

#キャラクター
$chr_hum = '村　人';
$chr_wlf = '人　狼';
$chr_ura = '占い師';
$chr_nec = '霊能者';
$chr_mad = '狂　人';
$chr_fre = '共有者';
$chr_bgd = '狩　人';
$chr_fox = '妖　狐';
$chr_rol = '猫　又';
$chr_bwl = '大　狼';
$chr_cfx = '子　狐';

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

$data_vildata_sum = 20;
$data_player_sum = 14;


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
$sys_plyerid  = '';
if ($in{'TXTPID'} ne ''){
	$sys_plyerid  = $in{'TXTPID'};
}
$sys_village = $in{'VILLAGENO'};
$sys_logviewflg = 0;
$sys_storytype = $in{'STORYTYPE'};

# FileName
$wak_village =  sprintf("%06d",$sys_village);
$file_pdata = $dat_path.$wak_village.".dat";
$tmp_pdata  = $dat_path.$wak_village.".tmp";
$file_log	= $log_path.$wak_village.".dat";
$tmp_log	= $log_path.$wak_village.".tmp";

#cookie
if ($in{'COMMAND'} eq 'ENTER') {
	print &setCookie('SELECTROOM', $in{'VILLAGENO'});
}
if ($in{'COMMAND'} eq 'LOGIN') {
	print &setCookie('PLAYERNO'.$sys_village, $in{'CMBPLAYER'});
	print &setCookie('PASSWORD'.$sys_village, $in{'TXTPASS'});
}
if ($in{'COMMAND'} eq 'ENTRY') {
	print &setCookie('HN', $in{'TXTHN'});
	print &setCookie('MAILADRES', $in{'TXTMAIL'});
}
print "Content-type: text/html\n";
print "\n";

$sys_plyerno  = 0;
if ($sys_plyerid){
	if($sys_plyerid == -60){
		$sys_plyerno = 60;
	}elsif($sys_plyerid == -99){
		$sys_plyerno = 50;
	}else{
		open(IN, $file_pdata);
		$wk_count = 0;
		while (<IN>) {
			$wk_count++;
			$value = $_;
			$value =~ s/\n//g;
			@wk_player = split(/,/, $value);
			if ($wk_count > 1 && $wk_player[12] == $sys_plyerid){
				$sys_plyerno = $wk_player[0];
				last;
			}
		}
		close(IN);
	}
}




# ***************************************************************** ログイン有無
if ($in{'TXTLOGIN'} ne '') {
	# =================================================================== 未ログイン 
	if ($sys_loginflg eq '1') {
		#--------------------------------------------------------------------- エントリー処理 
		if ($in{'COMMAND'} eq 'ENTRY') {
			$wk_entryflg = 0;
			if ($in{'TXTNAME'} ne '' && $in{'CMBICON'} ne '') {
				# 登録した村人の情報をデータファイルへ書き込む
				open(IN, $file_pdata);
				$wk_count = 0;
				while (<IN>) {
					$value = $_;
					$value =~ s/\n//g;
					$wk_count++;
					if ($wk_count == 1){
						@data_vildata = split(/,/, $value);
						$data_no = $data_vildata[1];
					}else{
						$data_player[$wk_count-1] = $value;
					}
				}
				close(IN);

				if ($data_vildata[0] >= 1) {
					$wk_entryflg = 2;
				}elsif ($data_vildata[1] >= $data_vildata[13]){
					$wk_entryflg = 3;
				}else{
					#WRITE
					$data_no++;
					$wk_id = int(rand(1000000)) + 1;
					# 0:NO , 1:ALIVE/DEAD , 2:VOTE , 3:JOB , 4:JOBwk , 5:WinLose , 6:COLOR , 7:NAME , 8:HN , 9:silent , 10:date, 11:ICON, 12:ID, 13:FOR DEATHNOTE, 14:CFOX
					$data_player[$data_no] = $data_no.',A,0,NON,0,-,'.$in{'CMBCOLOR'}.','.$in{'TXTNAME'}.','.$m{name}.',0,'.$date.','.$in{'CMBICON'}.','.$wk_id.',0';
					open(OUT, "> ".$file_pdata);
					$data_vildata[1] = $data_no;
					# 0:GAMESTART , 1:PLAYERNO , 2:DATE , 3:FAZE , 4:TIME , 5:VILNAME , 6:FORMID , 7:管理者ＩＤ , 8:RULE , 9:PASTTIME , 10:GM , 11:BET, 12:MASSACRE, 13:MAXPLAYER, 14:FANATIC, 15:DEATH NOTE, 16:BWLF, 17:CFOX, 18:SIXVIL, 19:CONFIGMODE, 20:ALL NUMBERS
					for my $i (0..$data_vildata_sum){
						print OUT "$data_vildata[$i],";
					}
					print OUT "\n";
					for ($i = 1; $i <= $data_no; $i++) {
						print OUT "$data_player[$i]\n";
					}
					close(OUT);
					&msg_write(0, 1, 31,"「<b>$in{'TXTNAME'}</b>さん」が村へやってきました。");
					$wk_entryflg = 1;
				}
			}
			# Print HTML document
			&disp_head1;
			print "<TR><TD>\n";
			if($wk_entryflg == 1){
				print "アナタは$data_no人目の村民として登録が完了しました。\n";
				$in{'COMMAND'} = 'LOGIN';
				$in{'CMBPLAYER'} = $data_no;
				$sys_plyerid = $wk_id;
			}elsif($wk_entryflg == 2){
				print "申\し訳ありません。既にゲームが開始しています。\n";
			}elsif($wk_entryflg == 3){
				print "申\し訳ありません。既に定員いっぱい登録されています。\n";
			}else{
				print "入力項目が正しくありません。\n";
			}
			print "</TD></TR>\n";
		}
		#--------------------------------------------------------------------- ログイン処理
		if ($in{'COMMAND'} eq 'LOGIN') {
			$wk_loginflg = 0;
			$wk_count = 0;
			$user_no = 1;
			if ($in{'CMBPLAYER'} == 0){
				#旅人の村へログイン処理
				$wk_loginflg = 1;
				$sys_loginflg = '2';
				$sys_plyerno = 60;
				$sys_plyerid = -60;
			}elsif ($in{'CMBPLAYER'} <= 23){
				#プレイヤーの村へログイン処理
				open(IN, $file_pdata);
				while (<IN>) {
					$wk_count++;
					$value = $_;
					$value =~ s/\n//g;
					@wk_player = split(/,/, $value);
					if ($wk_count > 1){
						if ($wk_player[0] == $in{'CMBPLAYER'}){
							if ($wk_player[8] eq $m{name}){
								$wk_loginflg = 1;
								$sys_loginflg = '2';
								$sys_plyerno = $in{'CMBPLAYER'};
								$sys_plyerid = $wk_player[12];
							}else{
								$wk_loginflg = 9;
							}
						}
					}
				}
				close(IN);
			}elsif ($in{'CMBPLAYER'} == 99){
				#村へ管理者ログイン
				open(IN, $file_pdata);
				while (<IN>) {
					$wk_count++;
					$value = $_;
					$value =~ s/\n//g;
					@wk_player = split(/,/, $value);
					if ($wk_count == 1){
						$user_no = @wk_player[7];
					}
				}
				close(IN);
				
				&sysadoin;
				if ($m{name} eq $sys_ID[$user_no]) {
					$wk_loginflg = 1;
					$sys_loginflg = '2';
					$sys_plyerno = 50;
					$sys_plyerid = -99;
				}else{
					$wk_loginflg = 9;
				}
			}
			# Print HTML document
			if($wk_loginflg != 1){
				&disp_head1;
				if ($user_no == 0){
					print "$data_vildata[7]が設定されていません。\n";
				}
				print "パスワードが正しくありません。\n";
			}
		}
		#--------------------------------------------------------------------- ログ閲覧
		if ($in{'COMMAND'} eq 'LOGVIEW') {
			$sys_loginflg = '2';
			$sys_plyerno = 60;
			$sys_plyerid = -60;
			$sys_logviewflg = 1;
		}
	}
	#=================================================================== ログインＯＫ
	if ($sys_loginflg eq '2') {

		# 現在の状態を確認
		open(IN, $file_pdata);
		$wk_count = 0;
		while (<IN>) {
			$value = $_;
			$value =~ s/\n//g;
			$wk_count++;
			if ($wk_count == 1){
				@data_vildata = split(/,/, $value);
			}else{
				@wk_player = split(/,/, $value);
				for ($i = 0; $i <= $data_player_sum; $i++) {
					$data_player[$wk_count-1][$i] = $wk_player[$i];
				}
			}
		}
		close(IN);
		
		$wk_txtmsg1 = '';
		$wk_txtmsg2 = '';
		$wk_txtmsglen = 0;
		if ($in{'comment'} ne '') {
#			$in{'comment'} =~ s/\r*\x00/\x00/g;
#			$in{'comment'} =~ s/\n*\x00//g;
			$in{'comment'} =~ s/,//g;
			$wk_txtmsg1 = $in{'comment'};
			$wk_txtmsg2 = $in{'comment'};
			$wk_txtmsg2 =~ s/[\n\r]/<br>/g;
			$wk_txtmsglen = length($in{'comment'});
		}

		$data_player[$sys_plyerno][10] = $date;

		#2重投稿防止
		if ($data_vildata[6] == $in{'FORMID'}) {
			$in{'COMMAND'} = '';
		}
		$data_vildata[6] = $in{'FORMID'};
		
		#=================================================================== 開始前
		if($data_vildata[0]==0){
			#--------------------------------------------------------------------- 開始
			my $cmd_start = 0;
			if($in{'COMMAND'} eq 'START' || $in{'COMMAND'} eq 'STARTF' || $in{'COMMAND'} eq 'STARTFF'){
				$cmd_start = 1;
			}
			my $teiin_check = 0;
			if($data_vildata[19]){
				if($data_vildata[1] == $data_vildata[13]){
					$teiin_check = 1;
				}
			}else{
				if($data_vildata[1] >= 8 || ($data_vildata[18] && $data_vildata[1] >= 6)){
					$teiin_check = 1;
				}
			}
			if($data_vildata[12]){
				$teiin_check = 1;
			}
			if ($cmd_start && $teiin_check) {
				if($data_vildata[12]){
					for($i = $data_vildata[1] + 1; $i <= $data_vildata[13]; $i++){
						$data_player[$i][0] =  1;
						$data_player[$i][1] =  'D';
						$data_player[$i][2] =  0;
						$data_player[$i][3] =  'NON';
						$data_player[$i][4] =  0;
						$data_player[$i][5] =  '-';
						$data_player[$i][6] =  '#DDDDDD';
						$data_player[$i][7] =  '初日犠牲者';
						$data_player[$i][8] =  '管理者';
						$data_player[$i][9] =  0;
						$data_player[$i][10] =  $date;
						$data_player[$i][11] =  26;# icon
						$data_player[$i][12] =  1;
						$data_player[$i][13] =  0;
					}
					$data_vildata[1] = $data_vildata[13];
					$data_vildata[11] = 0;
				}
				#WRITE
				for ($i = 1; $i <= $data_vildata[13]; $i++) {
					$wk_charactor[$i] = 'HUM';
				}
				@wk_rnd = &randomarr($data_vildata[1]);
				if($data_vildata[18]){ # 六人村
					$wk_charactor[$wk_rnd[1]] = 'WLF';
					$wk_charactor[$wk_rnd[2]] = 'BGD';
					$wk_charactor[$wk_rnd[3]] = 'URA';
					for ($i = 4; $i <= $data_vildata[1]; $i++) {
						$wk_charactor[$wk_rnd[$i]] = 'MAD';
					}
				}elsif($data_vildata[19]){ # 配役規定
					my @haiyaku = split /:/, $data_vildata[20];
					my $counter = 1;
					for(1..$haiyaku[1]){
						$wk_charactor[$wk_rnd[$counter]] = 'WLF';
						$counter++;
					}
					for(1..$haiyaku[2]){
						$wk_charactor[$wk_rnd[$counter]] = 'URA';
						$counter++;
					}
					for(1..$haiyaku[3]){
						$wk_charactor[$wk_rnd[$counter]] = 'NEC';
						$counter++;
					}
					for(1..$haiyaku[4]){
						$wk_charactor[$wk_rnd[$counter]] = 'MAD';
						$counter++;
					}
					for(1..$haiyaku[5]){
						$wk_charactor[$wk_rnd[$counter]] = 'FRE';
						$counter++;
					}
					for(1..$haiyaku[6]){
						$wk_charactor[$wk_rnd[$counter]] = 'BGD';
						$counter++;
					}
					for(1..$haiyaku[7]){
						$wk_charactor[$wk_rnd[$counter]] = 'FOX';
						$counter++;
					}
					for(1..$haiyaku[8]){
						$wk_charactor[$wk_rnd[$counter]] = 'ROL';
						$counter++;
					}
				}else{
					$wk_charactor[$wk_rnd[2]] = 'WLF';
					$wk_charactor[$wk_rnd[3]] = 'WLF';
					$wk_charactor[$wk_rnd[4]] = 'URA';
					if($data_vildata[1] >= 16){
						$wk_charactor[$wk_rnd[15]] = 'WLF';
					}
					if($data_vildata[1] >= 9){
						$wk_charactor[$wk_rnd[8]] = 'NEC';
					}
					if($data_vildata[1] >= 10){
						$wk_charactor[$wk_rnd[9]] = 'MAD';
					}
					if($data_vildata[1] >= 11){
						$wk_charactor[$wk_rnd[10]] = 'BGD';
					}
					if($data_vildata[1] >= 13){
						$wk_charactor[$wk_rnd[11]] = 'FRE';
						$wk_charactor[$wk_rnd[12]] = 'FRE';
					}
					if($data_vildata[1] >= 18){
						$wk_charactor[$wk_rnd[16]] = 'WLF';
						$wk_charactor[$wk_rnd[17]] = 'ROL';
					}
					if($data_vildata[1] >= 15 && $in{'COMMAND'} eq 'STARTF'){
						$wk_charactor[$wk_rnd[14]] = 'FOX';
					}
					if($in{'COMMAND'} eq 'STARTFF'){
						if($data_vildata[1] >= 8){
							$wk_charactor[$wk_rnd[7]] = 'FOX';
						}
						if($data_vildata[1] >= 16){
							$wk_charactor[$wk_rnd[14]] = 'FOX';
						}
					}
				}
				
				if($wk_charactor[1] eq 'WLF' || $wk_charactor[1] eq 'FOX'){ # 初日犠牲者を狼、狐から外す処理
					@wk_rnd2 = &randomarr($data_vildata[1]);
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if($wk_charactor[$wk_rnd2[$i]] eq 'WLF' || $wk_charactor[$wk_rnd2[$i]] eq 'FOX'){
							next;
						}else{
							my $temp_charactor = $wk_charactor[1];
							$wk_charactor[1] = $wk_charactor[$wk_rnd2[$i]];
							$wk_charactor[$wk_rnd2[$i]] = $temp_charactor;
							last;
						}
					}
				}
				if($data_vildata[1] >= 20 && $data_vildata[16]){ # 大狼
					$wlf_sum = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if($wk_charactor[$i] eq 'WLF'){
							$wlf_sum++;
						}
					}
					$bwl_num = int(rand($wlf_sum));
					$wlf_sum = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if($wk_charactor[$i] eq 'WLF'){
							if($wlf_sum == $bwl_num){
								$wk_charactor[$i] = 'BWL';
								last;
							}
							$wlf_sum++;
						}
					}
				}
				if($data_vildata[1] >= 20 && $data_vildata[17]){ # 子狐
					$fox_sum = 0;
					$hum_sum = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if($wk_charactor[$i] eq 'FOX'){
							$fox_sum++;
						}
						if($wk_charactor[$i] eq 'HUM'){
							$hum_sum++;
						}
					}
					if($fox_sum >= 2){
						$cfx_num = int(rand($fox_sum));
						$fox_sum = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if($wk_charactor[$i] eq 'FOX'){
								if($fox_sum == $cfx_num){
									$wk_charactor[$i] = 'CFX';
									last;
								}
								$fox_sum++;
							}
						}
					}else{
						$cfx_num = int(rand($hum_sum));
						$hum_sum = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if($wk_charactor[$i] eq 'HUM'){
								if($hum_sum == $cfx_num){
									$wk_charactor[$i] = 'CFX';
									last;
								}
								$hum_sum++;
							}
						}
					}
				}
				
				@wk_rnd3 = &randomarr($data_vildata[1]);
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					$data_player[$i][3] = $wk_charactor[$i];
					$data_player[$i][13] = $wk_rnd3[$i];
				}
				
				@sub_data = @data_player;
				for($i = 1; $i <= $data_vildata[1]; $i++){
					for($j = 1; $j <= $data_vildata[1]; $j++){
						if($sub_data[$j][13] == $i){
							$data_player[$i] = $sub_data[$j];
							$data_player[$i][0] = $i;
							$data_player[$i][13] = 0;
						}
					}
				}
				for($i = 1; $i <= $data_vildata[1]; $i++){
					if ($data_player[$i][12] == $sys_plyerid){
						$sys_plyerno = $data_player[$i][0];
						last;
					}
				}
				if($data_vildata[15]){
					for($i = 1; $i <= $data_vildata[1]; $i++){
						if ($data_player[$i][12] == 1){
							$data_vildata[15] = $i;
							last;
						}
					}
				}
				$data_vildata[0] = 1;
				$data_vildata[2] = 1;
				$data_vildata[3] = 2;
				$data_vildata[4] = 0;
				$data_vildata[9] = $time;
	
				# Print HTML document
				&msg_write(1, 50, 32,"<FONT size=\"+1\">１日目の夜となりました。</FONT>");
				
				$numhum = 0;
				$numwlf = 0;
				$numura = 0;
				$numnec = 0;
				$nummad = 0;
				$numbgd = 0;
				$numfre = 0;
				$numcat = 0;
				$numfox = 0;
				$numbwl = 0;
				$numcfx = 0;
				
				for ($i = 1; $i <= 23; $i++) {
					if($data_player[$i][3] eq 'HUM'){
						$numhum++;
					}
					if($data_player[$i][3] eq 'WLF'){
						$numwlf++;
					}
					if($data_player[$i][3] eq 'URA'){
						$numura++;
					}
					if($data_player[$i][3] eq 'NEC'){
						$numnec++;
					}
					if($data_player[$i][3] eq 'MAD'){
						$nummad++;
					}
					if($data_player[$i][3] eq 'BGD'){
						$numbgd++;
					}
					if($data_player[$i][3] eq 'FRE'){
						$numfre++;
					}
					if($data_player[$i][3] eq 'ROL'){
						$numcat++;
					}
					if($data_player[$i][3] eq 'FOX'){
						$numfox++;
					}
					if($data_player[$i][3] eq 'BWL'){
						$numbwl++;
					}
					if($data_player[$i][3] eq 'CFX'){
						$numcfx++;
					}
				}
				$haiyaku = "配役：";
				$haiyaku .= $numhum > 0 ? "村人 $numhum 人 ":"";
				$haiyaku .= $numwlf > 0 ? "人狼 $numwlf 人 ":"";
				$haiyaku .= $numbwl > 0 ? "大狼 $numbwl 人 ":"";
				$haiyaku .= $numura > 0 ? "占い $numura 人 ":"";
				$haiyaku .= $numnec > 0 ? "霊能\ $numnec 人 ":"";
				$haiyaku .= $nummad > 0 ? "狂人 $nummad 人 ":"";
				$haiyaku .= $numbgd > 0 ? "狩人 $numbgd 人 ":"";
				$haiyaku .= $numfre > 0 ? "共有 $numfre 人 ":"";
				$haiyaku .= $numcat > 0 ? "猫又 $numcat 人 ":"";
				$haiyaku .= $numfox > 0 ? "妖狐 $numfox 人 ":"";
				$haiyaku .= $numcfx > 0 ? "子狐 $numcfx 人 ":"";
				&msg_write(1, 50, 32,$haiyaku);
			}
			#--------------------------------------------------------------------- メッセージ
			if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '') {
				$wk_fonttag1 = "";
				$wk_fonttag2 = "";

				# [ msg write ]
				if ($in{'COMMAND'} eq 'MSG2'){
					$wk_fonttag1 = "<FONT size=\"+1\">";
					$wk_fonttag2 = "</FONT>";
				}
				if ($in{'COMMAND'} eq 'MSG3'){
					$wk_fonttag1 = "<FONT size=\"-1\">";
					$wk_fonttag2 = "</FONT>";
				}
				&msg_write(0, 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
			}
			#--------------------------------------------------------------------- 名前変更
			if ($in{'COMMAND'} eq 'NAMECHG' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsglen <= 20){
					$data_player[$sys_plyerno][7] = $wk_txtmsg1;
				}
			}
			#--------------------------------------------------------------------- 村名変更
			if ($in{'COMMAND'} eq 'VILNAME' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsglen <= 16){
					$data_vildata[5] = $wk_txtmsg1;
				}
			}
			#--------------------------------------------------------------------- ルール変更
			if ($in{'COMMAND'} eq 'VILRULE' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsg1 =~ /^[0-9]$/){
					$rule_number = int($wk_txtmsg1);
					$data_vildata[8] = $rule_number if ($rule_number >= 0 && $rule_number < @limit_times);
				}
			}
			#--------------------------------------------------------------------- 賭け変更
			if ($in{'COMMAND'} eq 'VILBET' && $wk_txtmsg1 ne '') {
				$data_vildata[11] = 0;
				$data_vildata[11] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- 大量殺戮変更
			if ($in{'COMMAND'} eq 'VILMASSACRE' && $wk_txtmsg1 ne '') {
				$data_vildata[12] = 0;
				$data_vildata[12] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- 定員変更
			if ($in{'COMMAND'} eq 'VILMAX' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsg1 =~ /^[0-9]+$/){
					$max_number = int($wk_txtmsg1);
					my $min = $data_vildata[19] ? 4:
								$data_vildata[18] ? 6 : 8;
					if ($max_number >= $min && $max_number <= 23 && $max_number >= $data_vildata[1]){
						$data_vildata[13] = $max_number;
						$max_mura = $data_vildata[13] - 1;
						$data_vildata[20] = "$max_mura:1:0:0:0:0:0:0:0";
					}
				}
			}
			#--------------------------------------------------------------------- 狂信者変更
			if ($in{'COMMAND'} eq 'FANATIC' && $wk_txtmsg1 ne '') {
				$data_vildata[14] = 0;
				$data_vildata[14] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- デスノ変更
			if ($in{'COMMAND'} eq 'DEATHNOTE' && $wk_txtmsg1 ne '') {
				$data_vildata[15] = 0;
				$data_vildata[15] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- 大狼変更
			if ($in{'COMMAND'} eq 'BWLF' && $wk_txtmsg1 ne '') {
				$data_vildata[16] = 0;
				$data_vildata[16] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- 子狐変更
			if ($in{'COMMAND'} eq 'CFOX' && $wk_txtmsg1 ne '') {
				$data_vildata[17] = 0;
				$data_vildata[17] = 1 if $wk_txtmsg1;
			}
			#--------------------------------------------------------------------- 六人村変更
			if ($in{'COMMAND'} eq 'SIXVIL' && $wk_txtmsg1 ne '') {
				$data_vildata[18] = 0;
				if($wk_txtmsg1){
					$data_vildata[13] = 6;
					$data_vildata[18] = 1;
					$data_vildata[19] = 0;
					$max_mura = $data_vildata[13] - 1;
					$data_vildata[20] = "$max_mura:1:0:0:0:0:0:0:0";
				}
			}
			#--------------------------------------------------------------------- 配役規定
			if ($in{'COMMAND'} eq 'CHAVIL' && $wk_txtmsg1 ne '') {
				$data_vildata[19] = 0;
				$data_vildata[13] = 23;
				if($wk_txtmsg1){
					$data_vildata[18] = 0;
					$data_vildata[19] = 1;
					$max_mura = $data_vildata[13] - 1;
					$data_vildata[20] = "$max_mura:1:0:0:0:0:0:0:0";
				}
			}
			#--------------------------------------------------------------------- 配役数変更
			if ($in{'COMMAND'} =~ /^NUM(.*)$/ && $wk_txtmsg1 ne '') {
				my $num_yaku = $1;
				if ($wk_txtmsg1 =~ /^[0-9]+$/){
					$cha_number = int($wk_txtmsg1);
					my @haiyaku = split /:/, $data_vildata[20];
					if($num_yaku eq 'WLF' && $cha_number >= 1){
						$haiyaku[1] = $cha_number;
					}elsif($num_yaku eq 'URA'){
						$haiyaku[2] = $cha_number;
					}elsif($num_yaku eq 'NEC'){
						$haiyaku[3] = $cha_number;
					}elsif($num_yaku eq 'MAD'){
						$haiyaku[4] = $cha_number;
					}elsif($num_yaku eq 'FRE'){
						$haiyaku[5] = $cha_number;
					}elsif($num_yaku eq 'BGD'){
						$haiyaku[6] = $cha_number;
					}elsif($num_yaku eq 'FOX'){
						$haiyaku[7] = $cha_number;
					}elsif($num_yaku eq 'ROL'){
						$haiyaku[8] = $cha_number;
					}
					my $sum_cha = 0;
					for my $i (1..8){
						if($haiyaku[$i]){
							$sum_cha += $haiyaku[$i];
						}else{
							$haiyaku[$i] = 0;
						}
					}
					my $rest_cha = $data_vildata[13] - $sum_cha;
					if($rest_cha < 0){
						$haiyaku[1] = 1;
						for my $i (2..8){
							$haiyaku[$i] = 0;
						}
						$rest_cha = $data_vildata[13] - 1;
					}
					$haiyaku[0] = $rest_cha;
					$data_vildata[20] = join ':', @haiyaku;
				}
			}
			#--------------------------------------------------------------------- 管理者メッセージ
			if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
				# [ msg write ]
				&msg_write(0, 1, 24, $wk_txtmsg2);
			}
			#--------------------------------------------------------------------- 村人登録抹消処理
			if ($in{'COMMAND'} eq 'PLEYERDEL') {
				open(IN, $file_pdata);
				$wk_count = 0;
				while (<IN>) {
					$value = $_;
					$value =~ s/\n//g;
					$wk_count++;
					if ($wk_count == 1){
						@data_vildata = split(/,/, $value);
					}else{
						@wk_player = split(/,/, $value);
						if ($in{'CMBPLAYER'} == $wk_player[0]){
							#削除する村人の行を飛ばす
							$wk_CMBPLAYER = $data_player[$in{'CMBPLAYER'}][7];
							$wk_count--;
						}else{
							$data_player[$wk_count-1][0] = $wk_count - 1;
							for ($i = 1; $i <= $data_player_sum; $i++) {
								 $data_player[$wk_count-1][$i] = $wk_player[$i];
							}
						}
					}
				}
				close(IN);
				#村人の人数を一人減らす
				$data_vildata[1] = $data_vildata[1] - 1;
				&data_write;
				&msg_write($data_vildata[2], 2, 34,"<b>$wk_CMBPLAYER</b>さんは<FONT color=\"#ff0000\">村人の登録を抹消されました。</FONT>");
			}
		}
		#=================================================================== ＯＮＰＬＡＹ！
		if($data_vildata[0]==1){# ゲーム中フラグ
			if($data_vildata[8] != 0){
				$data_vildata[4] += $time - $data_vildata[9];
				$data_vildata[9] = $time;
			}
			#--------------------------------------------------------------------- [ 昼 ]
			if($data_vildata[3] == 1){# 昼
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][0]){
						$data_vildata[4] = 0;
						$data_vildata[3] = 3
					}
				}
				#--------------------------------------------------------------------- メッセージ
				if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '' && $data_vildata[4] < $limit_times[$data_vildata[8]][0]) {
					if($data_vildata[8] == 0){
						if ($wk_txtmsglen <= 100){
							$data_vildata[4] += 15;
						}elsif ($wk_txtmsglen <= 200){
							$data_vildata[4] += 30;
						}elsif ($wk_txtmsglen <= 300){
							$data_vildata[4] += 45;
						}elsif ($wk_txtmsglen <= 400){
							$data_vildata[4] += 60;
						}elsif ($wk_txtmsglen <= 500){
							$data_vildata[4] += 75;
						}elsif ($wk_txtmsglen <= 600){
							$data_vildata[4] += 90;
						}elsif ($wk_txtmsglen <= 700){
							$data_vildata[4] += 105;
						}else{
							$data_vildata[4] += 120;
						}
						if ($data_vildata[4] >= $limit_times[0][0]){
							$data_vildata[4] = $limit_times[0][0];
						}
					}

					$wk_fonttag1 = "";
					$wk_fonttag2 = "";
					# [ msg write ]
					if ($in{'COMMAND'} eq 'MSG2'){
						$wk_fonttag1 = "<FONT size=\"+1\">";
						$wk_fonttag2 = "</FONT>";
					}
					if ($in{'COMMAND'} eq 'MSG3'){
						$wk_fonttag1 = "<FONT size=\"-1\">";
						$wk_fonttag2 = "</FONT>";
					}
					&msg_write($data_vildata[2], 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
				}
				#--------------------------------------------------------------------- 霊 話
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 沈黙
				if ($in{'COMMAND'} eq 'SILENT') {
					$data_player[$sys_plyerno][9] = 1;
					# 判定
					$wk_cnt_live	= 0;
					$wk_cnt_silent = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A'){
							$wk_cnt_live++;
							if ($data_player[$i][9] == 1) {
								$wk_cnt_silent++;
							}
						}
					}
					# 半数 判定
					if(int($wk_cnt_live / 2) < $wk_cnt_silent){
						$data_vildata[4] += 60;
						if ($data_vildata[4] >= $limit_times[$data_vildata[8]][0]){
							$data_vildata[4] = $limit_times[$data_vildata[8]][0];
						}
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							$data_player[$i][9] = 0;
						}
						&msg_write($data_vildata[2], 1, 25, '「・・・・・・。」１分間ほどの沈黙が続いた。');
					}
				}
				#--------------------------------------------------------------------- 投票
				if (($in{'COMMAND'} eq 'VOTE' && $data_player[$sys_plyerno][2] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') || $in{'COMMAND'} eq 'VOTECHK') {
					if ($in{'COMMAND'} eq 'VOTE'){
						$data_player[$sys_plyerno][2] = $in{'CMBPLAYER'};
					}
					# 投票判定
					$wk_voteflg = 1;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$wk_votecount[$i] = 0;
					}
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][2] != 0 && $data_player[$i][1] eq 'A'){
							$wk_votecount[$data_player[$i][2]]++;
						}
						if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
							$wk_voteflg = 0;
						}
					}

					if ($wk_voteflg == 1){
						$wk_topvote = 1;
						$wk_votetable = "<TABLE>";
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A'){
								$wk_votetable = $wk_votetable."<TR><TD><b>$data_player[$i][7]</b>さん</TD><TD>$wk_votecount[$i] 票</TD><TD>投票先 → <b>$data_player[$data_player[$i][2]][7]</b>さん</TD></TR>";
								if ($wk_votecount[$wk_topvote] < $wk_votecount[$i]){
									$wk_topvote = $i;
								}
							}
						}
						$wk_votetable = $wk_votetable."</TABLE>";
						&msg_write($data_vildata[2], 2, 0,"$wk_votetable");
						&msg_write($data_vildata[2], 2, 0,"<BR><FONT size=\"+1\">$data_vildata[2]日目 投票結果。</FONT>");
						$wk_topvotecheck = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($wk_votecount[$wk_topvote] == $wk_votecount[$i]){
								$wk_topvotecheck++;
							}
						}
						if ($wk_topvotecheck == 1){
							# 投票終了、一番の人を処刑する
							$data_vildata[3] = 2;
							$data_vildata[4] = 24;
							$data_vildata[9] = $time;
							$data_player[$wk_topvote][1] = 'D';
							# 猫又の道連れ
							if ($data_player[$wk_topvote][3] eq 'ROL') {
								#生きている人から一人選ぶ  *無作為じゃなくね？
								for ($i = 1; $i <= $data_vildata[1]; $i++) {
									 if ($data_player[$i][1] eq 'A') {
										 $wk_targezibaku = $i;
									 }
								}
								$data_player[$wk_targezibaku][1] = 'D';
							}else{
								$wk_targezibaku = 99;
							}
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
								$data_player[$i][9] = 0;
								$data_player[$i][13] = 0;
								if ($data_player[$i][3] eq 'NEC' && $data_player[$i][1] eq 'A' && $data_vildata[2]>=2) {
									$data_player[$i][4] = $wk_topvote;
								}
								if ($data_player[$i][3] eq 'URA') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'CFX') {
									$data_player[$i][4] = 0;
								}
							}
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 2, 33,"<b>$data_player[$wk_topvote][7]</b>さんは村民協議の結果<FONT color=\"#ff0000\">処刑されました・・・。</FONT>");
								if ($wk_targezibaku != 99) {
									&msg_write($data_vildata[2], 2, 35,"<b>$data_player[$wk_targezibaku][7]</b>さんは猫又に道連れにされて<FONT color=\"#ff0000\">死亡しました・・・。</FONT>");
								}
							}
							
							# [ 勝利判定 ]
							&sub_judge;
							
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]日目の夜となりました。</FONT>");
							}
						}else{
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
							}
							&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">再投票となりました。</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
				}
				#--------------------------------------------------------------------- 再投票
				if ($in{'COMMAND'} eq 'REVOTE') {
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$data_player[$i][2] = 0;
					}
					$data_vildata[4] = 0;
					&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">再投票となりました。</FONT>");
				}
			}
			#--------------------------------------------------------------------- [ 昼 投票待ち ]
			if($data_vildata[3] == 3){# 昼
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][2]){
						$data_vildata[4] = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A' && $data_player[$i][2] == 0) {
								$data_player[$i][1] = 'D';
								&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
							}
						}
						$in{'COMMAND'} = 'VOTECHK';
					}
				}
				#--------------------------------------------------------------------- 霊 話
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 投票
				if (($in{'COMMAND'} eq 'VOTE' && $data_player[$sys_plyerno][2] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') || $in{'COMMAND'} eq 'VOTECHK') {
					if ($in{'COMMAND'} eq 'VOTE'){
						$data_player[$sys_plyerno][2] = $in{'CMBPLAYER'};
					}
					# 投票判定
					$wk_voteflg = 1;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$wk_votecount[$i] = 0;
					}
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][2] != 0 && $data_player[$i][1] eq 'A'){
							$wk_votecount[$data_player[$i][2]]++;
						}
						if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
							$wk_voteflg = 0;
						}
					}

					if ($wk_voteflg == 1){
						$wk_topvote = 1;
						$wk_votetable = "<TABLE>";
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A'){
								$wk_votetable = $wk_votetable."<TR><TD><b>$data_player[$i][7]</b>さん</TD><TD>$wk_votecount[$i] 票</TD><TD>投票先 → <b>$data_player[$data_player[$i][2]][7]</b>さん</TD></TR>";
								if ($wk_votecount[$wk_topvote] < $wk_votecount[$i]){
									$wk_topvote = $i;
								}
							}
						}
						$wk_votetable = $wk_votetable."</TABLE>";
						&msg_write($data_vildata[2], 2, 0,"$wk_votetable");
						&msg_write($data_vildata[2], 2, 0,"<BR><FONT size=\"+1\">$data_vildata[2]日目 投票結果。</FONT>");
						$wk_topvotecheck = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($wk_votecount[$wk_topvote] == $wk_votecount[$i]){
								$wk_topvotecheck++;
							}
						}
						if ($wk_topvotecheck == 1){
							# 投票終了、一番の人を処刑する
							$data_vildata[3] = 2;
							$data_vildata[4] = 24;
							$data_vildata[9] = $time;
							$data_player[$wk_topvote][1] = 'D';
							# 猫又の道連れ
							if ($data_player[$wk_topvote][3] eq 'ROL') {
								#生きている人から一人選ぶ  *無作為じゃなくね？
								for ($i = 1; $i <= $data_vildata[1]; $i++) {
									 if ($data_player[$i][1] eq 'A') {
										 $wk_targezibaku = $i;
									 }
								}
								$data_player[$wk_targezibaku][1] = 'D';
							}else{
								$wk_targezibaku = 99;
							}
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
								$data_player[$i][9] = 0;
								$data_player[$i][13] = 0;
								if ($data_player[$i][3] eq 'NEC' && $data_player[$i][1] eq 'A' && $data_vildata[2]>=2) {
									$data_player[$i][4] = $wk_topvote;
								}
								if ($data_player[$i][3] eq 'URA') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'CFX') {
									$data_player[$i][4] = 0;
								}
							}
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 2, 33,"<b>$data_player[$wk_topvote][7]</b>さんは村民協議の結果<FONT color=\"#ff0000\">処刑されました・・・。</FONT>");
								if ($wk_targezibaku != 99) {
									&msg_write($data_vildata[2], 2, 35,"<b>$data_player[$wk_targezibaku][7]</b>さんは猫又に道連れにされて<FONT color=\"#ff0000\">死亡しました・・・。</FONT>");
								}
							}
							
							# [ 勝利判定 ]
							&sub_judge;
							
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]日目の夜となりました。</FONT>");
							}
						}else{
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
							}
							$data_vildata[4] = 0;
							&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">再投票となりました。</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
				}
				#--------------------------------------------------------------------- 再投票
				if ($in{'COMMAND'} eq 'REVOTE') {
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$data_player[$i][2] = 0;
					}
					$data_vildata[4] = 0;
					&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">再投票となりました。</FONT>");
				}
			}
			#--------------------------------------------------------------------- [ 夜 ]
			if($data_vildata[3] == 2){# 夜の時間調整
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][1]){
						$data_vildata[4] = 0;
						$data_vildata[3] = 4;
					}
				}
				#-------------------------- 遠吠え
				if ($in{'COMMAND'} eq 'MSGWLF' && $wk_txtmsg1 ne '' && $data_vildata[4] < $limit_times[$data_vildata[8]][1]) {
					if($data_vildata[8] == 0){
						if ($wk_txtmsglen <= 100){
							$data_vildata[4] += 15;
						}elsif ($wk_txtmsglen <= 200){
							$data_vildata[4] += 30;
						}elsif ($wk_txtmsglen <= 300){
							$data_vildata[4] += 45;
						}else{
							$data_vildata[4] += 60;
						}
						if ($data_vildata[4] >= $limit_times[0][0]){
							$data_vildata[4] = $limit_times[0][0];
						}
					}
					# [ msg write ]
					&msg_write($data_vildata[2], 3, $sys_plyerno, $wk_txtmsg2);
				}
				#-------------------------- 殺害予告
				if($data_vildata[2] >= 2){
					if ($in{'COMMAND'} eq 'KILL' && ($data_player[$in{'CMBPLAYER'}][3] ne 'WLF' || $data_player[$in{'CMBPLAYER'}][3] ne 'BWL') && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを狙います。");
					}
				}else{
					if ($in{'COMMAND'} eq 'KILL' && ($data_player[$in{'CMBPLAYER'}][3] ne 'WLF' || $data_player[$in{'CMBPLAYER'}][3] ne 'BWL') && $data_player[$in{'CMBPLAYER'}][1] eq 'A' && $data_player[$in{'CMBPLAYER'}][12] == 1) {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを狙います。");
					}
				}
				#-------------------------- 占い師
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを占います。");
				}
				#-------------------------- 狩人
				if ($in{'COMMAND'} eq 'GUARD' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 13, 44,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを護衛します。");
				}
				#--------------------------- 共有会話
				if ($in{'COMMAND'} eq 'MSGFRE' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 6, $sys_plyerno, $wk_txtmsg2);
				}
				#-------------------------- 子狐
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					$data_player[$sys_plyerno][14] = int(rand(2));
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを占います。");
				}
				#-------------------------- デスノ
				if ($in{'COMMAND'} eq 'DEATHNOTE' && $data_player[$sys_plyerno][13] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					unless(($data_player[$sys_plyerno][3] eq 'WLF' || $data_player[$sys_plyerno][3] eq 'WLF') && ($data_player[$in{'CMBPLAYER'}][3] eq 'WLF' || $data_player[$in{'CMBPLAYER'}][3] eq 'WLF')){
						$data_player[$sys_plyerno][13] = $in{'CMBPLAYER'};
						&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんの名前をノートに書きました。");
					}
				}
				
				#--------------------------- 独り言
				if ($in{'COMMAND'} eq 'MSG1' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 5, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- 霊 話
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 2, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 夜終了判定
				if ($in{'COMMAND'} ne '') {
					$wk_nightend = 1;
					$wk_targetwlf = 0;
					$wk_targetura = 0;
					$wk_targetbgd = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A') {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
								$wk_targetwlf = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'URA' && $data_player[$i][8] ne '管理者') {
								$wk_targetura = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'CFX' && $data_player[$i][8] ne '管理者') {
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
								$wk_targetbgd = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
						}
					}
					if ($wk_nightend == 1) {
						@wk_mes = ();
						# 護衛なしで妖狐以外なら人狼に殺害される
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] ne 'FOX') {
							$data_player[$wk_targetwlf][1] = 'D';
							push @wk_mes, "<b>$data_player[$wk_targetwlf][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>";
						}
						# 妖狐が占いされたか判定
						if ($data_player[$wk_targetura][3] eq 'FOX') {
							$data_player[$wk_targetura][1] = 'D';
							push @wk_mes, "<b>$data_player[$wk_targetura][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>";
						}
						@rand_i = ();
						for my $i (0..$#wk_mes){
							push @rand_i, $i;
						}
						for my $i (0..$#wk_mes){
							$j = int(rand(@wk_mes));
							my $temp = $rand_i[$j];
							$rand_i[$j] = $rand_i[$i];
							$rand_i[$i] = $temp;
						}
						for my $i(@rand_i){
							&msg_write($data_vildata[2], 4, 34,$wk_mes[$i]);
						}
						# デスノ
						$wk_targetdeathnote = $data_player[$data_vildata[15]][13];
						if ($wk_targetdeathnote) {
							if($data_player[$wk_targetdeathnote][1] eq 'A'){
								$data_player[$wk_targetdeathnote][1] = 'D';
								&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetdeathnote][7]</b>さんは翌日に<FONT color=\"#ff0000\">死体で発見された・・・。</FONT>");
							}
						}
						
						#猫又が人狼を道連れ
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] eq 'ROL') {
							#生きている人狼の中から一人を選ぶ *わかめて鯖と違う
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][1] eq 'A'){
									if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
										$wk_targezibaku = $i;
									}
								}
							}
							$data_player[$wk_targezibaku][1] = 'D';
							&msg_write($data_vildata[2], 4, 35,"<b>$data_player[$wk_targezibaku][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>");
						}
						# [ 勝利判定 ]
						&sub_judge;
						
						if ($data_vildata[0] == 1) {
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'BGD') {
									$data_player[$i][4] = 0;
								}
							}
							$data_vildata[2]++;
							$data_vildata[3] = 1;
							$data_vildata[4] = 0;
							$data_vildata[9] = $time;
							&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]日目の朝となりました。</FONT>");
						}
						if($data_vildata[15]){
							$data_vildata[15] = int(rand($data_vildata[1])) + 1;
						}
					}
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
				}
			}
			
			#--------------------------------------------------------------------- [ 夜 能力実行待ち]
			if($data_vildata[3] == 4){# 夜の時間調整
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][1]){
						$data_vildata[4] = 0;
						$kill_wlf = 1;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A') {
								if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
									if ($data_player[$i][4] == 0 && $kill_wlf) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
									}
									$kill_wlf = 0;
								}
								if ($data_player[$i][3] eq 'URA') {
									if ($data_player[$i][4] == 0) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
									}
								}
								if ($data_player[$i][3] eq 'CFX') {
									if ($data_player[$i][4] == 0) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
									}
								}
								if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
									if ($data_player[$i][4] == 0) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
									}
								}
							}
						}
					}
				}
				#-------------------------- 殺害予告
				if($data_vildata[2] >= 2){
					if ($in{'COMMAND'} eq 'KILL' && ($data_player[$in{'CMBPLAYER'}][3] ne 'WLF' || $data_player[$in{'CMBPLAYER'}][3] ne 'BWL') && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを狙います。");
					}
				}else{
					if ($in{'COMMAND'} eq 'KILL' && ($data_player[$in{'CMBPLAYER'}][3] ne 'WLF' || $data_player[$in{'CMBPLAYER'}][3] ne 'BWL') && $data_player[$in{'CMBPLAYER'}][1] eq 'A' && $data_player[$in{'CMBPLAYER'}][12] == 1) {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを狙います。");
					}
				}
				#-------------------------- 占い師
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを占います。");
				}
				#-------------------------- 狩人
				if ($in{'COMMAND'} eq 'GUARD' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 13, 44,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを護衛します。");
				}
				#--------------------------- 共有会話
				if ($in{'COMMAND'} eq 'MSGFRE' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 6, $sys_plyerno, $wk_txtmsg2);
				}
				#-------------------------- 子狐
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					$data_player[$sys_plyerno][14] = int(rand(2));
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんを占います。");
				}
				#-------------------------- デスノ
				if ($in{'COMMAND'} eq 'DEATHNOTE' && $data_player[$sys_plyerno][13] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					unless(($data_player[$sys_plyerno][3] eq 'WLF' || $data_player[$sys_plyerno][3] eq 'WLF') && ($data_player[$in{'CMBPLAYER'}][3] eq 'WLF' || $data_player[$in{'CMBPLAYER'}][3] eq 'WLF')){
						$data_player[$sys_plyerno][13] = $in{'CMBPLAYER'};
						&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>さんの名前をノートに書きました。");
					}
				}
				
				#--------------------------- 独り言
				if ($in{'COMMAND'} eq 'MSG1' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 5, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- 霊 話
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 2, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 24, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- 夜終了判定
				if ($in{'COMMAND'} ne '') {
					$wk_nightend = 1;
					$wk_targetwlf = 0;
					$wk_targetura = 0;
					$wk_targetbgd = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A') {
							if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
								$wk_targetwlf = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'URA' && $data_player[$i][8] ne '管理者') {
								$wk_targetura = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'CFX' && $data_player[$i][8] ne '管理者') {
								$wk_targetura = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
								$wk_targetbgd = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
						}
					}
					if ($wk_nightend == 1) {
						@wk_mes = ();
						# 護衛なしで妖狐以外なら人狼に殺害される
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] ne 'FOX') {
							$data_player[$wk_targetwlf][1] = 'D';
							push @wk_mes, "<b>$data_player[$wk_targetwlf][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>";
						}
						# 妖狐が占いされたか判定
						if ($data_player[$wk_targetura][3] eq 'FOX') {
							$data_player[$wk_targetura][1] = 'D';
							push @wk_mes, "<b>$data_player[$wk_targetura][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>";
						}
						@rand_i = ();
						for my $i (0..$#wk_mes){
							push @rand_i, $i;
						}
						for my $i (0..$#wk_mes){
							$j = int(rand(@wk_mes));
							my $temp = $rand_i[$j];
							$rand_i[$j] = $rand_i[$i];
							$rand_i[$i] = $temp;
						}
						for my $i(@rand_i){
							&msg_write($data_vildata[2], 4, 34,$wk_mes[$i]);
						}
						
						$wk_targetdeathnote = $data_player[$data_vildata[15]][13];
						# デスノ
						if ($wk_targetdeathnote) {
							if($data_player[$wk_targetdeathnote][1] eq 'A' ){
								$data_player[$wk_targetdeathnote][1] = 'D';
								&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetdeathnote][7]</b>さんは翌日に<FONT color=\"#ff0000\">死体で発見された・・・。</FONT>");
							}
						}
						#猫又が人狼を道連れ
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] eq 'ROL') {
							#生きている人狼の中から一人を選ぶ *わかめて鯖と違う
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][1] eq 'A'){
									if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
										$wk_targezibaku = $i;
									}
								}
							}
							$data_player[$wk_targezibaku][1] = 'D';
							&msg_write($data_vildata[2], 4, 35,"<b>$data_player[$wk_targezibaku][7]</b>さんは翌日<FONT color=\"#ff0000\">無残な姿で発見された・・・。</FONT>");
						}
						# [ 勝利判定 ]
						&sub_judge;
						
						if ($data_vildata[0] == 1) {
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'BGD') {
									$data_player[$i][4] = 0;
								}
							}
							$data_vildata[2]++;
							$data_vildata[3] = 1;
							$data_vildata[4] = 0;
							$data_vildata[9] = $time;
							&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]日目の朝となりました。</FONT>");
						}
						if($data_vildata[15]){
							$data_vildata[15] = int(rand($data_vildata[1])) + 1;
						}
					}
				}
				#--------------------------------------------------------------------- 管理者メッセージ
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>さんは都合により<FONT color=\"#ff0000\">突然死しました・・・。</FONT>");
				}
			}
		}
		#=================================================================== ゲーム終了
		if($data_vildata[0]==2){
			#--------------------------------------------------------------------- メッセージ
			if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '') {
				$wk_fonttag1 = "";
				$wk_fonttag2 = "";
				# [ msg write ]
				if ($in{'COMMAND'} eq 'MSG2'){
					$wk_fonttag1 = "<FONT size=\"+1\">";
					$wk_fonttag2 = "</FONT>";
				}
				if ($in{'COMMAND'} eq 'MSG3'){
					$wk_fonttag1 = "<FONT size=\"-1\">";
					$wk_fonttag2 = "</FONT>";
				}
				&msg_write($data_vildata[2], 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
			}
			#--------------------------------------------------------------------- 管理者メッセージ
			if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
				# [ msg write ]
				&msg_write($data_vildata[2], 50, 24,$wk_txtmsg2);
			}
		}

		# 0:GAMESTART , 1:PLAYERNO , 2:DATE , 3:FAZE , 4:TIME , 5:FORMID , 7:管理者ＩＤ
		# 0:NO , 1:ALIVE/DEAD , 2:VOTE , 3:JOB , 4:JOBwk , 5:wk1 , 6:wk2 , 7:PASSWORD , 8:NAME , 9:PROFILE 
		
		# [ HEAD ]
		&disp_head2;
		
		if ($sys_logviewflg != 1 || $sys_storytype != "2"){
			print "<TR><TD ><OPTION value=\"\"><INPUT type=\"submit\" value=\"更新\"></TD></TR>\n";
		}

		# [ PLAYER LIST ]
		&disp_players;

		# [ MY DATA ]
		&disp_mydata;
		
		if ($sys_logviewflg != 1 || $sys_storytype != "2"){
			print "<TR><TD class=\"CLSTD01\">◆ 出来事</TD></TR>\n";
			if($data_vildata[0]!=2){
			}
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

		
		#データ書きこみ
		if($sys_plyerno <= 50){
			&data_write;
		}
	}
	
	print "</TD></TR>\n";
	print "<TR><TD>\n";
	print "<INPUT type=\"hidden\" name=\"TXTPID\" value=\"$sys_plyerid\">";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"2\">";
	$wk_rnd = int(rand(1000000)) + 1;
	print "<INPUT type=\"hidden\" name=\"FORMID\" value=\"$wk_rnd\">";
	print "</TD></TR>\n";
}
# ***************************************************************** ログインなし
else{
	&disp_head1;
	#ユーザーＩＤの存在検査
	&sysadoin;
	$user_no = 0;
	for ($i = 1; $i <= $sys_ID_COUNT; $i++) {# 管理ユーザーチェック
		if ($m{name} eq $sys_ID[$i]) {
			$user_no = $i;
		}
	}
	
	if($user_no == 0 && $in{'TXTPASS'} eq $pass){# 新規管理ユーザー
		open(IN, $sys_path_bak);
		$wk_count_s = 1;
		$sys_ID_COUNT = 0;
		while (<IN>) {
			$value = $_;
			$value =~ s/\n//g;
			
			@wk_player = split(/,/, $value);
			$sys_ID[$wk_count_s] = $wk_player[0];
			$sys_pass[$wk_count_s] = $wk_player[1];
			$sys_name[$wk_count_s] = $wk_player[2];
			$wk_count_s++;
			$sys_ID_COUNT++;
			}
		close(IN);
		
		$sys_ID[$wk_count_s] = $m{name};
		$sys_pass[$wk_count_s] = $m{pass};
		$sys_name[$wk_count_s] = $m{name};
		
		open(OUT, "> ".$sys_path_bak);
		for(1..$wk_count_s){
			print OUT "$sys_ID[$_],$sys_pass[$_],$sys_name[$_]\n";
		}
		close(OUT);
		$user_no = $wk_count_s;
		$in{'TXTPASS'} = $sys_pass[$user_no];
	}
	
	if ($in{'TXTPASS'} eq $sys_pass[$user_no] && $user_no != 0) {
		if ($in{'COMMAND'} eq 'NEWVILLAGE' && $in{'TXTMURA'} ne '') {
			#新規作成した村の情報をファイルへ書き込む
			#最後の村番号を取得する
			opendir(INDIR, $dat_dir) || die $!;
			@files = sort readdir(INDIR);
			closedir(INDIR);
			foreach (@files){
			if(/dat_buu(.*)\.(dat)$/){
				$filename = $_;
				if(open(IN, $dat_dir.$filename)){
				  @wk_vildata = split(/,/,<IN>);
				  #ファイル名から村番号を取得
				  @wk_filename = unpack 'a7a6a4', $filename; # unpack
				  $wk_fileno = $wk_filename[1];
				  
				  close(IN);
				  }
				}
			}
			$wk_fileno++;
			$wk_txtmsg1 = '';
			$wk_txtmsglen = 0;
			if ($in{'TXTMURA'} ne '') {
				$in{'TXTMURA'} =~ s/\r*$//g;
				$in{'TXTMURA'} =~ s/\n//g;
				$in{'TXTMURA'} =~ s/,//g;
				$wk_txtmsg1 = $in{'TXTMURA'};
				$wk_txtmsg2 = $in{'TXTMURA'};
				$wk_txtmsg2 =~ s/\r/<BR>/g;
				$wk_txtmsglen = length($in{'TXTMURA'});
			}
			#６桁に補正
			$cnt = sprintf("%06d",$wk_fileno);
			#データファイル＆ログファイルへ書き込み
			$file_pdata = $dat_path.$cnt.".dat";
			$file_log   = $log_path.$cnt.".dat";
			@data_vildata = (0,1,0,1,0,'');
			if ($wk_txtmsglen <= 16){
				$data_vildata[5] = $wk_txtmsg1;
			}
			$data_vildata[7] = $user_no;
			$data_vildata[8] = 1;
			$data_vildata[9] = $time;
			if($in{'GM'} eq 'NOGM'){
				$data_vildata[10] = 1;
			}else{
				$data_vildata[10] = 0;
			}
			if($in{'BET'} eq 'NOBET'){
				$data_vildata[11] = 0;
			}else{
				$data_vildata[11] = 1;
			}
			$data_vildata[12] = 0;
			$data_vildata[13] = $in{MAXMEMBER}; #定員数
			$data_vildata[14] = $in{FANATIC} ? 1:0;
			$data_vildata[15] = $in{DEATHNOTE} ? 1:0;
			$data_vildata[16] = $in{BWLF} ? 1:0;
			$data_vildata[17] = $in{CFOX} ? 1:0;
			$data_vildata[18] = $in{SIXVIL} ? 1:0;
			#村の作成と同時に初日犠牲者を作成する
			$data_player[1][0] =  1;
			$data_player[1][1] =  'A';
			$data_player[1][2] =  0;
			$data_player[1][3] =  'NON';
			$data_player[1][4] =  0;
			$data_player[1][5] =  '-';
			$data_player[1][6] =  '#DDDDDD';
			$data_player[1][7] =  '初日犠牲者';
			$data_player[1][8] =  '管理者';
			$data_player[1][9] =  0;
			$data_player[1][10] =  $date;
			$data_player[1][11] =  26;# icon
			$data_player[1][12] =  1;
			
			&data_write;
			open(OUT, "> ".$file_log);
			close(OUT);
		
			print "<TR><TD align=\"center\">新規に作成しました。</TD></TR>\n";
		} elsif ($in{'COMMAND'} eq 'DELVILLAGE') {
			$wak_village =  sprintf("%06d",$sys_village);
			open(IN, $dat_path.$wak_village.".dat");
			@wk_vildata = split(/,/,<IN>);
			close(IN);
			if ($wk_vildata[0] == 2) {# 終了してる村
				#バックアップ番号を取得
				if( open( FH, "douke/count.dat" ) ){
					$cnt = <FH>;
					close(FH);
					#カウントアップ
					$cnt++;
					#カウンタ書き込み
					if( open( FH, ">douke/count.dat" ) ){
						print FH $cnt;
						close(FH);
					} else {
						print "ファイル書き込オープンに失敗しました。\n";
					}
					#６桁に補正
					$cnt = sprintf("%06d",$cnt);
				} else {
					print "ファイル読み込オープンに失敗しました。\n";
				}
				#プレイヤーデータをバックアップ
				$file_pdata = $dat_path.$wak_village.".dat";
				$file_bakup = $dat_path_bak.$cnt.".bak";
				$ret = rename  $file_pdata , $file_bakup;
				if ($ret == 0) {
					printf "ファイル名変更に失敗(%s => %s)\n", $file_pdata, $file_bakup;
					printf "エラー(%d:%s)\n", $!, $!;
				}
				#ログデータをバックアップ
				$file_log	= $log_path.$wak_village.".dat";
				$file_bakup = $log_path_bak.$cnt.".bak";
				$ret = rename  $file_log , $file_bakup;
				if ($ret == 0) {
					printf "ファイル名変更に失敗(%s => %s)\n", $file_pdata, $file_bakup;
					printf "エラー(%d:%s)\n", $!, $!;
				}
				print "<TR><TD align=\"center\">村 $sys_village番を削除しました。</TD></TR>\n";
			} else {
				print "<TR><TD align=\"center\">ゲームを終了してから削除してください。</TD></TR>\n";
			}
		} elsif ($in{'COMMAND'} eq 'ENDVILLAGE') {
			open(IN, $file_pdata);
			$wk_count = 0;
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				$wk_count++;
				if ($wk_count == 1){
					@data_vildata = split(/,/, $value);
				}else{
					@wk_player = split(/,/, $value);
					for ($i = 0; $i <= $data_player_sum; $i++) {
						$data_player[$wk_count-1][$i] = $wk_player[$i];
					}
				}
			}
			close(IN);
			
			$data_vildata[0] = 2;
			&data_write;
			print "<TR><TD align=\"center\">村 $sys_village番ゲームを強制終了しました。</TD></TR>\n";
		} elsif ($in{'COMMAND'} eq 'VILLAGEBAN') {
			unlink  $file_pdata;
			print "<TR><TD align=\"center\">村 $sys_village番を廃村にしました。</TD></TR>\n";
		}
		&disp_admin;
	} else {
		if ($in{'COMMAND'} eq 'ENTER') {
			&disp_login;
		}else{
			if ($in{subf} eq "room") {
				&disp_room;
			}
			elsif ($in{subf} eq "entry") {
				&disp_entry;
			}
			elsif ($in{subf} eq "log") {
				&disp_logview;
			}
			elsif ($in{subf} eq "master") {
				&disp_admin;
			}
			else {
				print "<TR><TD align=\"center\">正しい入り口からどうぞ。</TD></TR>\n";
			}
		}
	}
}

# [ FOOT ]
&disp_foot;

# Lock解除
rmdir($lock_path);
