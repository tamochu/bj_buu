##########################################################################################################
# 設定
##########################################################################################################
#---------------------------------------------------------------------
@limit_times = (
#	['昼',	'夜'	'能力使用'],
	[600,	600,	180],
	[270,	180,	180],
);

##########################################################################################################
# サブルーチン
##########################################################################################################
#---------------------------------------------------------------------
sub data_write{
	open(OUT, "> ".$file_pdata);
	for my $i (0..$data_vildata_sum){
		print OUT "$data_vildata[$i],";
	}
	print OUT "\n";
	for ($i9 = 1; $i9 <= $data_vildata[1]; $i9++) {
		for my $i (0..$data_player_sum){
			print OUT "$data_player[$i9][$i],";
		}
		print OUT "\n";
	}
	close(OUT);
}
#---------------------------------------------------------------------
sub msg_write{
	@wk_writedata = @_;
	open(OUT, "> ".$tmp_log);
	open(IN, $file_log);
	print OUT "$wk_writedata[0],$wk_writedata[1],$wk_writedata[2],$wk_writedata[3]\n";
	while (<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);

	# Copy .tmp to .dat
	open(IN, $tmp_log);
	open(OUT, "> ".$file_log);
	$msgs = 0;
	while (<IN>) {
		# if ($msgs++ >= 2000) { last; }
		print OUT;
	}
	close(IN);
	close(OUT);
	unlink($tmp_log);
}
#---------------------------------------------------------------------
sub disp_head1{
	print "<HTML>\n";
	print "<HEAD>\n";
	print '<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">';
	print "<TITLE>$sys_title</TITLE>\n";
	print "</HEAD>\n";
	print "<BODY>\n";
	print "<FORM action=\"$cgi_path\" method=\"POST\">\n";
	print "<TABLE width=\"700\" cellspacing=\"5\"><TBODY>\n";
}
#---------------------------------------------------------------------
#  村に行く（ログイン）
#---------------------------------------------------------------------
sub disp_room{
	# Cookieの値を得る
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	#データファイルの内容を読み出して選択リストを作成する
	print "<TR><TD>村を選択</TD><TD><SELECT name=\"VILLAGENO\">\n";
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			#ファイル名から村番号を取得
			@wk_filename = unpack 'a7a6a4', $filename; # unpack
			$wk_muralist[$wk_fileno] = $wk_filename[1];
			$wk_muralist0[$wk_fileno] = $wk_vildata[0];
			$wk_muralist1[$wk_fileno] = $wk_vildata[1];
			$wk_muralist5[$wk_fileno] = $wk_vildata[5];
			$wk_muralist7[$wk_fileno] = $wk_vildata[7];
			print "<OPTION value=\"$wk_muralist[$wk_fileno]\" ";
			if ($sys_default0 == $wk_filename[1]) {
				print "selected";
			}
			print ">村 住所$wk_muralist[$wk_fileno]番 $wk_vildata[5]村";
			print " 賭けあり" if $wk_vildata[11];
			print "</OPTION>\n";
			$wk_fileno++;
			close(IN);
		}
		}
	}
	print "  </SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"村に行く\"></TD></TR>\n";
	#村の一覧を表示する
	print "<HTML>\n";
	print "<BODY>\n";
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>番号</TH><TH>村の名前</TH><TH>人数</TH><TH>状態</TH><TH>管理者</TH></TR>\n";
	for ($i = 1; $i <= $wk_fileno - 1; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]村</TH><TH>$wk_muralist1[$i]人</TH>";
		if ($wk_muralist0[$i]==0){
			print "<TH>事件前日</TH>";
		}
		if ($wk_muralist0[$i]==1){
			print "<TH>ゲーム開始</TH>";
		}
		if ($wk_muralist0[$i]==2){
			print "<TH>ゲーム終了</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	print "</TABLE>\n";
	print "</BODY>\n";
	print "</HTML>\n";
	
	print "</TABLE>\n";
	#print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"ENTER\">\n";
	print "</TD></TR>\n";
}

#---------------------------------------------------------------------
sub disp_login{
	# Cookieの値を得る
	&getCookie();
	$sys_default1 = $COOKIE{'PLAYERNO'.$sys_village};
	if ($sys_default1 eq "") {
		$sys_default1 = 0;
	}
	$sys_default2 = $COOKIE{'PASSWORD'.$sys_village};
	
	print "<TR><TD>\n";
	print "<TABLE>\n";

	open(IN, $file_pdata);
	@wk_vildata = split(/,/, <IN>);
	print "<TR><TD>村を選択</TD><TD>村 住所$sys_village番 $wk_vildata[5]村</TD></TR>\n";
	print "<TR><TD>名前を選択</TD><TD><SELECT name=\"CMBPLAYER\">\n";
	print "<OPTION value=\"0\">旅　人（観戦）</OPTION>\n";
	while ($value = <IN>) {
		$value =~ s/\n//g;
		@wk_player = split(/,/, $value);
		print "<OPTION value=\"$wk_player[0]\"";
		if ($sys_default1 == $wk_player[0]) {
			print " selected";
		}
		print ">$wk_player[7]</OPTION>\n";
	}
	close(IN);
	if($wk_vildata[10] != 1){
		print "<OPTION value=\"99\"";
		if ($sys_default1 == 99) {
			print " selected";
		}
		print ">管理者：$sys_name[$wk_vildata[7]]</OPTION>\n";
	}
	print "</SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"村に行く\"></TD></TR>\n";
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGIN\">\n";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
#-  管理者ログイン
#---------------------------------------------------------------------
sub disp_admin{
	print "<TR><TD>\n";
	print "<TABLE>\n";
	print "<TR><TD>村を選択</TD><TD><SELECT name=\"VILLAGENO\">\n";
	$wk_fileno = 1;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	#$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			
			@wk_filename = unpack 'a7a6a4', $filename; # unpack
			
			$wk_fileno = $wk_filename[1];
			
			print "<OPTION value=\"$wk_fileno\">村 住所$wk_fileno番 $wk_vildata[5]村</OPTION>\n";
			#$wk_fileno++;
			close(IN);
		}
		}
	}
	$wk_fileno++;
	print "  </SELECT></TD></TR>\n";
	
	print "<TR><TD>新規NO</TD><TD>村NO $wk_fileno</TD></TR>";
	
	print "<TR><TD>処理選択</TD><TD><SELECT name=\"COMMAND\">\n";
	print "  <OPTION value=\"NEWVILLAGE\">村を作成</OPTION>\n";
	print "  <OPTION value=\"DELVILLAGE\">村の削除</OPTION>\n";
	print "  <OPTION value=\"ENDVILLAGE\">ゲームの強制終了</OPTION>\n";
	print "  <OPTION value=\"VILLAGEBAN\">廃村処理</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>GM</TD><TD><SELECT name=\"GM\">\n";
	print "  <OPTION value=\"ONGM\" selected>GMあり</OPTION>\n";
	print "  <OPTION value=\"NOGM\">仮GM</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>GM</TD><TD><SELECT name=\"BET\">\n";
	print "  <OPTION value=\"NOBET\" selected>賭けなし</OPTION>\n";
	print "  <OPTION value=\"BET\">賭けあり</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>定員数</TD><TD><SELECT name=\"MAXMEMBER\">\n";
	print "  <OPTION value=\"23\" selected>23人</OPTION>\n";
	for my $i (1..20){
		my $m = 23 - $i;
		print "  <OPTION value=\"$m\">$m人</OPTION>\n";
	}
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>狂信者</TD><TD><INPUT type=\"checkbox\" name=\"FANATIC\" value=\"1\"></TD></TR>\n";
	print "<TR><TD>死神の手帳</TD><TD><INPUT type=\"checkbox\" name=\"DEATHNOTE\" value=\"1\"></TD></TR>\n";
	print "<TR><TD>大狼</TD><TD><INPUT type=\"checkbox\" name=\"BWLF\" value=\"1\"></TD></TR>\n";
	print "<TR><TD>子狐</TD><TD><INPUT type=\"checkbox\" name=\"CFOX\" value=\"1\"></TD></TR>\n";
	print "<TR><TD>六人村</TD><TD><INPUT type=\"checkbox\" name=\"SIXVIL\" value=\"1\"></TD></TR>\n";
	print "<TR><TD>村の名前(８文字まで)</TD><TD><INPUT size=\"20\" type=\"text\" maxlength=\"16\" name=\"TXTMURA\"></TD></TR>\n";
	print "<TR><TD>パスワード</TD><TD><INPUT type=\"hidden\" name=\"TXTPASS\" value=\"$pass\"></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"処理実行\"></TD></TR>\n";
	print "</TABLE>\n";
	#print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
#  村民登録（プレイヤー登録）
#---------------------------------------------------------------------
sub disp_entry{
	$wk_fileno = 1;
	$wk_entryflg = 0;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			if ($wk_vildata[0] == 0) {
				$wk_entryflg = 1;
				#ファイル名から村番号を取得
				@wk_filename = unpack 'a7a6a4', $filename; # unpack
				$wk_murano[$wk_fileno] = $wk_filename[1];
				$wk_muralist5[$wk_fileno] = $wk_vildata[5];
				$wk_muralist11[$wk_fileno] = $wk_vildata[11];
				$wk_fileno++;
			}
			close(IN);
		}
		}
	}
	print "<TR><TD>\n";
	if ($wk_entryflg == 1) {
		# Cookieの値を得る
		&getCookie();
		$sys_defaultMEIL = $COOKIE{'MAILADRES'};
		$sys_defaultHN = $COOKIE{'HN'};
		print "<CENTER><BR><TABLE border=\"1\" cellspacing=\"4\"><TBODY><TR><TD>";
		print "<TABLE cellpadding=\"4\"><TBODY>";
		
		print "<TR><TD align=\"center\"><B><FONT size=\"+2\">村民登録書</FONT></B></TD></TR>\n";
		print "<TR><TD align=\"center\">◇</TD></TR>\n";
		
		print "<TR><TD align=\"center\">◆村を選択してください。</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"VILLAGENO\">\n";
		for ($i = 1; $i <= $wk_fileno - 1; $i++) {
			print "<OPTION value=\"$wk_murano[$i]\">村 住所$wk_murano[$i]番 $wk_muralist5[$i]村";
			print " 賭けあり" if $wk_muralist11[$i];
			print "</OPTION>\n";
		}
		print "  </SELECT></TD></TR>\n";
		print "<TR><TD align=\"center\">◇</TD></TR>\n";
		
		print "<TR><TD align=\"center\"><INPUT type=\"hidden\" name=\"TXTHN\" value=\"$m{name}\"></TD></TR>\n";
		
		print "<TR><TD align=\"center\">◆アナタのアイコンを選択してください。</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"CMBICON\">\n";
		# アイコンファイルを読み込む
		if(open(IN, $ico_path_bak)){
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				@wk_icon = split(/,/, $value);
				if($wk_icon[0]==26){
					print "<OPTION value=\"$wk_icon[0]\" selected>$wk_icon[1]</OPTION>\n";
				}else{
					print "<OPTION value=\"$wk_icon[0]\">$wk_icon[1]</OPTION>\n";
				}
			}
			close(IN);
		}
		print "</SELECT></TD></TR>\n";
		#print "<TR><TD align=\"center\">◇</TD></TR>\n";
		print "<TR><TD align=\"center\">◇<A href='iconlist.htm' target='_blank'>アイコン一覧</A></TD></TR>\n";
		
		print "<TR><TD align=\"center\">◆アナタの表\示色を選択してください。</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"CMBCOLOR\">\n";
		print "<OPTION value=\"1\" selected>明灰 lightglay</OPTION>\n";
		print "<OPTION value=\"2\">暗灰 darkglay</OPTION>\n";
		print "<OPTION value=\"3\">黄 yellow</OPTION>\n";
		print "<OPTION value=\"4\">橙 orange</OPTION>\n";
		print "<OPTION value=\"5\">赤 red</OPTION>\n";
		print "<OPTION value=\"6\">水 lightblue</OPTION>\n";
		print "<OPTION value=\"7\">青 blue</OPTION>\n";
		print "<OPTION value=\"8\">緑 green</OPTION>\n";
		print "<OPTION value=\"9\">紫 purple</OPTION>\n";
		print "<OPTION value=\"10\">桃 pink</OPTION>\n";
		print "</SELECT></TD></TR>\n";
		print "<TR><TD align=\"center\">◇</TD></TR>\n";

		print "<TR><TD align=\"center\">◆アナタの村人としての名前を入力してください。（10文字）<BR>（例：山田　人郎）<BR><FONT size=\"-1\">プレイ中はこの名前を使用します。HNがばれないものが好ましいです。</FONT></TD></TR>\n";
		print "<TR><TD align=\"center\"><INPUT size=\"20\" maxlength=\"10\" type=\"text\" name=\"TXTNAME\"></TD></TR>\n";
		print "<TR><TD align=\"center\">◇</TD></TR>\n";

		print "<TR><TD align=\"center\">「村民約定」<BR>私は村のため家族のためにそして自分自身のために<BR>もしかしたら、たまたま、いや、なんとなく、現れるかもしれない<BR>「人狼」と戦い抜くことを誓います。</TD></TR>\n";
		print "<TR><TD align=\"center\"><INPUT type=\"submit\" value=\"同意する（登録）\"></TD></TR>\n";
	
		print "</TBODY></TABLE>\n";
		print "</TD></TR></TBODY></TABLE></CENTER>\n";
		print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">";
		print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"ENTRY\">\n";
	} else {
		print "滞在可能\な村がありませんでした。";
	}
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
# 過去ログ表示処理
#---------------------------------------------------------------------
sub disp_logview{
	# Cookieの値を得る
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	
	print "<TR><TD>村を選択</TD><TD><SELECT name=\"VILLAGENO\">\n";
	$wk_fileno = 1;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			if ($wk_vildata[0] == 2) {
				if ($sys_default0 == $wk_fileno) {
					print "selected";
				}
				#ファイル名から村番号を取得
				@wk_filename = unpack 'a7a6a4', $filename; # unpack
				$wk_muralist[$wk_fileno] = $wk_filename[1];
				$wk_muralist0[$wk_fileno] = $wk_vildata[0];
				$wk_muralist1[$wk_fileno] = $wk_vildata[1];
				$wk_muralist2[$wk_fileno] = $wk_vildata[2];
				$wk_muralist3[$wk_fileno] = $wk_vildata[3];
				$wk_muralist4[$wk_fileno] = $wk_vildata[4];
				$wk_muralist5[$wk_fileno] = $wk_vildata[5];
				$wk_muralist6[$wk_fileno] = $wk_vildata[6];
				$wk_muralist7[$wk_fileno] = $wk_vildata[7];
				$wk_muralist8[$wk_fileno] = $wk_vildata[8];
				$wk_muralist9[$wk_fileno] = $wk_vildata[9];
				$wk_muralist10[$wk_fileno] = $wk_vildata[10];
				print "<OPTION value=\"$wk_muralist[$wk_fileno]\" ";
				print ">村 住所$wk_muralist[$wk_fileno]番 $wk_vildata[5]村</OPTION>\n";
				$wk_fileno++;
			}
			close(IN);
		}
		}
	}
	print "  </SELECT></TD></TR>\n";
	print "<TR><TD>話を選択</TD><TD><SELECT name=\"STORYTYPE\">\n";
	print "<OPTION value=\"1\">村人の戦い</OPTION>\n";
	print "<OPTION value=\"2\">霊の談話</OPTION>\n";
	print "<OPTION value=\"3\" selected>全記録</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"記録を見る\"></TD></TR>\n";
	
	#村の一覧を表示する
	print "<HTML>\n";
	print "<BODY>\n";
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>番号</TH><TH>村の名前</TH><TH>人数</TH><TH>　結　果　</TH><TH>管理者</TH></TR>\n";
	for ($i = 1; $i <= $wk_fileno - 1; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]村</TH><TH>$wk_muralist1[$i]人</TH>";
		if ($wk_muralist8[$i]==0){
			print "<TH>未決着</TH>";
		}elsif ($wk_muralist8[$i]==1){
			print "<TH>村人の勝利　</TH>";
		}elsif ($wk_muralist8[$i]==2){
			print "<TH>妖孤の勝利</TH>";
		}elsif ($wk_muralist8[$i]==3){
			print "<TH>人狼の勝利　</TH>";
		}elsif ($wk_muralist8[$i]==4){
			print "<TH>妖孤の勝利</TH>";
		}else{
			print "<TH>　　　　　　</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	print "</TABLE>\n";
	print "</BODY>\n";
	print "</HTML>\n";
	
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGVIEW\">\n";
	print "</TD></TR>\n";
}

sub disp_logview_back{
	# Cookieの値を得る
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	
	print "<TR><TD>村を選択</TD><TD><SELECT name=\"VILLAGENO\">\n";
	#バックアップ番号を取得
	if( open( FH, "./douke/count.dat" ) ){
		$maxcnt = <FH>;
		close(FH);
		for ($i = 1; $i <= $maxcnt; $i++) {
			$cnt = sprintf("%06d",$i);
			if( open(IN, $dat_path.$cnt.".bak") ){
				@wk_vildata = split(/,/,<IN>);
				print "<OPTION value=\"$i\" ";
				if ($sys_default0 == $wk_fileno) {
					print "selected";
				}
				$wk_muralist[$i] = $i;
				$wk_muralist0[$i] = $wk_vildata[0];
				$wk_muralist1[$i] = $wk_vildata[1];
				$wk_muralist5[$i] = $wk_vildata[5];
				$wk_muralist7[$i] = $wk_vildata[7];
				print ">村 住所$wk_fileno番 $wk_vildata[5]村</OPTION>\n";
				close(IN);
			}
		}
	} else {
		print "ファイル読み込オープンに失敗しました。\n";
	}
	print "  </SELECT></TD></TR>\n";
	
	print "<TR><TD>話を選択</TD><TD><SELECT name=\"STORYTYPE\">\n";
	print "<OPTION value=\"1\">村人の戦い</OPTION>\n";
	print "<OPTION value=\"2\">霊の談話</OPTION>\n";
	print "<OPTION value=\"3\" selected>全記録</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"記録を見る\"></TD></TR>\n";
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGVIEW\">\n";
	
	#村の一覧を表示する
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>番号</TH><TH>村の名前</TH><TH>人数</TH><TH>　結　果　</TH><TH>管理者</TH></TR>\n";
	for ($i = 1; $i <= $maxcnt; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]村</TH><TH>$wk_muralist1[$i]人</TH>";
		if ($wk_muralist8[$i]==0){
			print "<TH>未決着</TH>";
		}elsif ($wk_muralist8[$i]==1){
			print "<TH>村人の勝利　</TH>";
		}elsif ($wk_muralist8[$i]==2){
			print "<TH>妖狐の勝利</TH>";
		}elsif ($wk_muralist8[$i]==3){
			print "<TH>人狼の勝利　</TH>";
		}elsif ($wk_muralist8[$i]==4){
			print "<TH>妖狐の勝利</TH>";
		}else{
			print "<TH>　　　　　　</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	
}

#---------------------------------------------------------------------
#---------------------------------------------------------------------
sub disp_head2{
	print "<HTML>\n";
	print "<HEAD>\n";
	print '<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">';
	print "<STYLE type=\"text/css\"><!--\n";
	print "TABLE{ font-size : 11pt; }\n";
	print ".CLSTABLE{ font-size : 10pt; }\n";
	print ".CLSTABLE2{ color : #333333; }\n";
	if ($data_vildata[3] == 1 || $data_vildata[3] == 3) {
		print ".CLSTD01{ color : white; background-color : black; font-weight : bold; }\n";
	}
	if ($data_vildata[3] == 2 || $data_vildata[3] == 4) {
		print ".CLSTD01{ color : black; background-color : white; font-weight : bold; }\n";
	}
	print ".CLSTD02{ background-color : #e3e3e3; }\n";
	print "--></STYLE>\n";
	print qq|<script type="text/javascript" src="$htmldir/nokori_time.js"></script>\n|;
	print "<TITLE>$sys_title</TITLE>\n";
	print "</HEAD>\n";
	if ($data_vildata[3] == 1 || $data_vildata[3] == 3) {
		print "<BODY link=\"#FFCC00\" vlink=\"#FFCC00\" alink=\"#FFCC00\">\n";
	}
	if ($data_vildata[3] == 2 || $data_vildata[3] == 4) {
		print "<BODY bgcolor=\"#000000\" text=\"#ffffff\" link=\"#FF6600\" vlink=\"#FF6600\" alink=\"#FF6600\">\n";
	}
	print "<FORM action=\"$cgi_path\" method=\"POST\">\n";
	print "<TABLE width=\"700\" cellspacing=\"5\"><TBODY>\n";
	print "<TR><TD height=\"20\"><FONT size=\"+1\">$sys_title</FONT></TD></TR>\n";
	if($data_vildata[8] == 0){
		print "<TR><TD>制限時間なし</TD></TR>\n";
	}else{
		print "<TR><TD>制限時間あり</TD></TR>\n";
	}
	if($data_vildata[11] == 1){
		print "<TR><TD>賭けあり</TD></TR>\n";
	}
	if($data_vildata[10] == 1){
		print "<TR><TD>この村は仮GMです。最初に入村した人がゲームを開始してください。</TD></TR>\n";
	}
	if($data_vildata[12] == 1){
		print "<TR><TD>特殊ルール：大量殺戮</TD></TR>\n";
	}
	if($data_vildata[14] == 1){
		print "<TR><TD>追加ルール：狂信者</TD></TR>\n";
	}
	if($data_vildata[15]){
		print "<TR><TD>追加ルール：死神の手帳</TD></TR>\n";
	}
	if($data_vildata[16]){
		print "<TR><TD>追加ルール：大狼</TD></TR>\n";
	}
	if($data_vildata[17]){
		print "<TR><TD>追加ルール：子狐</TD></TR>\n";
	}
	if($data_vildata[18]){
		print "<TR><TD>特殊ルール：六人村</TD></TR>\n";
	}
	if($data_vildata[19]){
		print "<TR><TD>特殊ルール：配役規定</TD></TR>\n";
		my @haiyaku = split /:/, $data_vildata[20];
		
		print "<TR><TD>$chr_hum:$haiyaku[0]人 ";
		print "$chr_wlf:$haiyaku[1]人 ";
		print "$chr_ura:$haiyaku[2]人 " if $haiyaku[2];
		print "$chr_nec:$haiyaku[3]人 " if $haiyaku[3];
		print "$chr_mad:$haiyaku[4]人 " if $haiyaku[4];
		print "$chr_fre:$haiyaku[5]人 " if $haiyaku[5];
		print "$chr_bgd:$haiyaku[6]人 " if $haiyaku[6];
		print "$chr_fox:$haiyaku[7]人 " if $haiyaku[7];
		print "$chr_rol:$haiyaku[8]人 " if $haiyaku[8];
		print "</TD></TR>\n"
	}
}
#---------------------------------------------------------------------
#  画面の一番上に村人の情報を一覧表示する
#---------------------------------------------------------------------
sub disp_players{
	print "<TR><TD class=\"CLSTD01\">◆ 村人たち</TD></TR>\n";
	print "<TR><TD><TABLE class=\"CLSTABLE\"><TBODY>\n";
	$wk_amari = (5 - ($data_vildata[1] % 5)) % 5;
	$wk_iend  = $data_vildata[1] + $wk_amari;
	for ($i = 1; $i <= $wk_iend; $i++) {
		if ($i % 5 == 1){
			print "<TR>";
		}
		if ($i <= $data_vildata[1]){
			if ($data_player[$i][1] eq 'A'){
				#生存中のアイコンを表示
				print "<TD valign=\"top\" bgcolor=\"$wk_color[$data_player[$i][6]]\"><IMG src=\"".$imgpath."alive".$data_player[$i][11].".gif\" title=\"$data_player[$i][7]\" alt=\"$data_player[$i][7]\" width=\"32\" height=\"32\" border=\"0\"></TD>\n";
			}
			if ($data_player[$i][1] eq 'D'){
				#死亡なので墓石のアイコンを表示
				print "<TD valign=\"top\" bgcolor=\"$wk_color[$data_player[$i][6]]\"><IMG src=\"".$imgpath."grave.gif\" title=\"$data_player[$i][7]\" width=\"32\" height=\"32\" border=\"0\"></TD>\n";
			}
			print "<TD>$data_player[$i][7]<BR>";
			if ($data_vildata[0] == 2 || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50) {
				print "<b>$data_player[$i][8]</b>さん<BR>";
				if ($data_player[$i][3] eq 'HUM') {
					print "[$chr_hum]";
				}
				if ($data_player[$i][3] eq 'WLF') {
					print "[$chr_wlf]";
				}
				if ($data_player[$i][3] eq 'URA') {
					print "[$chr_ura]";
				}
				if ($data_player[$i][3] eq 'NEC') {
					print "[$chr_nec]";
				}
				if ($data_player[$i][3] eq 'MAD') {
					print "[$chr_mad]";
				}
				if ($data_player[$i][3] eq 'BGD') {
					print "[$chr_bgd]";
				}
				if ($data_player[$i][3] eq 'FRE') {
					print "[$chr_fre]";
				}
				if ($data_player[$i][3] eq 'FOX') {
					print "[$chr_fox]";
				}
				if ($data_player[$i][3] eq 'ROL') {
					print "[$chr_rol]";
				}
				if ($data_player[$i][3] eq 'BWL') {
					print "[$chr_bwl]";
				}
				if ($data_player[$i][3] eq 'CFX') {
					print "[$chr_cfx]";
				}
				if ($sys_plyerno == 50) {
					if ($data_player[$i][2] != 0) {
						print "<FONT color=\"0000FF\">◆</FONT>";
					}
					if ($data_player[$i][4] != 0) {
						print "<FONT color=\"00FF00\">◆</FONT>";
					}
					print "<BR>$data_player[$i][10]";
				}
				print "<BR>";
			}elsif($data_vildata[10] == 1 && $data_vildata[0] == 0 && $sys_plyerno == 2){
				print "<BR>$data_player[$i][10]<br>";
			
			}
			if ($data_player[$i][1] eq 'A'){
				print "（生存中）</TD>\n";
			}
			if ($data_player[$i][1] eq 'D'){
				print "（死　亡）</TD>\n";
			}
		}else{
			print OUT "<TD></TD><TD></TD>\n";
		}
		if ($i % 5 == 0){
			print "</TR>";
		}
	}
	print "</TBODY></TABLE></TD></TR>\n";
}
#---------------------------------------------------------------------
#  画面の二番目にキャラクターの役目と状況を表示する
#---------------------------------------------------------------------
sub disp_mydata{
	if($data_vildata[0] == 1 && $sys_plyerno <= $data_vildata[13]){
		print "<TR><TD class=\"CLSTD01\">◆ アナタの情報</TD></TR>\n";
		if ($data_player[$sys_plyerno][1] eq 'A') {
			print "<TR><TD><TABLE cellspacing=\"0\"><TBODY>\n";
			if ($data_player[$sys_plyerno][3] eq 'HUM') {
				print "<TR><TD><IMG src=\"".$imgpath."hum.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_hum」です。<BR>";
				print "【能\力】ありません。しかし、アナタの知恵と勇気で村を救うことができるはずです。</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'WLF') {
				print "<TR><TD><IMG src=\"".$imgpath."wlf.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_wlf」です。<BR>";
				print "【能\力】夜の間に他の人狼と協力し村人ひとり殺害できます。アナタはその強力な力で村人を食い殺すのです。</TD></TR>";
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if (($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') && $i != $sys_plyerno) {
						print "<TR><TD colspan=\"2\">【能\力発動】誇り高き人狼の血を引く仲間は<b>$data_player[$i][7]</b>さんです。</TD></TR>";
					}
				}
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】アナタは<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんを殺る予\定です。</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'BWL') {
				print "<TR><TD><IMG src=\"".$imgpath."wlf.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_bwl」です。<BR>";
				print "【能\力】夜の間に他の人狼と協力し村人ひとり殺害できます。アナタはその強力な力で村人を食い殺すのです。</TD></TR>";
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if (($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') && $i != $sys_plyerno) {
						print "<TR><TD colspan=\"2\">【能\力発動】誇り高き人狼の血を引く仲間は<b>$data_player[$i][7]</b>さんです。</TD></TR>";
					}
				}
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】アナタは<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんを殺る予\定です。</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'URA') {
				print "<TR><TD><IMG src=\"".$imgpath."ura.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_ura」です。<BR>";
				print "【能\力】夜の間に村人ひとりを「人」か「狼」か調べることができます。アナタが村人の勝利を握っています。</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】占いの結果、<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんは";
					if ($data_player[$data_player[$sys_plyerno][4]][3] eq 'WLF') {
						print "「$chr_wlf」でした。"
					}else{
						print "「$chr_hum」でした。"
					}
					print "</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'NEC') {
				print "<TR><TD><IMG src=\"".$imgpath."nec.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_nec」です。<BR>";
				print "【能\力】[２日目以降]その日のリンチ死者が「人」か「狼」か調べることができます。地味ですがアナタの努力次第で大きく貢献することも不可能\ではありません。</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】前日処刑された<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんは";
					if ($data_player[$data_player[$sys_plyerno][4]][3] eq 'WLF') {
						print "「$chr_wlf」でした。"
					}elsif($data_player[$data_player[$sys_plyerno][4]][3] eq 'BWL'){
						print "「$chr_bwl」でした。"
					}elsif($data_player[$data_player[$sys_plyerno][4]][3] eq 'CFX'){
						print "「$chr_cfx」でした。"
					}else{
						print "「$chr_hum」でした。"
					}
					print "</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'MAD') {
				print "<TR><TD><IMG src=\"".$imgpath."mad.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_mad」です。<BR>";
				if($data_vildata[14] == 1){
					print "【能\力】人狼の勝利がアナタの勝利となります。アナタはできるかぎり狂って場をかき乱すのです。バカになれ。<BR>狂信者は人狼がだれか把握できます。<br>人狼は";
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if (($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL') && $i != $sys_plyerno) {
							print "<b>$data_player[$i][7]</b>さん";
						}
					}
					print "です。</TD></TR>";
				}else{
					print "【能\力】人狼の勝利がアナタの勝利となります。アナタはできるかぎり狂って場をかき乱すのです。バカになれ。</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'BGD') {
				print "<TR><TD><IMG src=\"".$imgpath."bgd.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_bgd」です。<BR>";
				print "【能\力】[２日目以降]夜の間に村人ひとりを指定し人狼の殺害から護ることができます。人狼のココロを読むのです。</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】アナタは<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんを護衛しています。</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'FRE') {
				print "<TR><TD><IMG src=\"".$imgpath."fre.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_fre」です。<BR>";
				print "【能\力】アナタはもうひとりの$chr_freがだれであるかを知ることができます。生存期間が他に比べ永い能\力です。アナタには推理する時間が与えられたのです。悩みなさい。</TD></TR>";
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if ($data_player[$i][3] eq 'FRE' && $i != $sys_plyerno) {
						print "<TR><TD colspan=\"2\">【能\力発動】もうひとりの$chr_freは<b>$data_player[$i][7]</b>さんです。</TD></TR>";
					}
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'FOX') {
				print "<TR><TD><IMG src=\"".$imgpath."fox.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_fox」です。<BR>";
				print "【能\力】アナタは人狼に殺されることはありません。ただし推理されてしまうと死んでしまいます。村人を騙し、人狼を騙し、村を妖狐のものにするのです。</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'ROL') {
				print "<TR><TD><IMG src=\"".$imgpath."rol.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_rol」です。<BR>";
				print "【能\力】この村に住むただの猫又です。死亡時にアナタを殺した相手を道連れにします。</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'CFX') {
				print "<TR><TD><IMG src=\"".$imgpath."ura.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>アナタの役割は「$chr_cfx」です。<BR>";
				print "【能\力】夜の間に村人ひとりを「人」か「狼」か調べることができます。妖狐とともに勝利を目指すのです</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">【能\力発動】占いの結果、<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>さんは";
					if($data_player[$sys_plyerno][14] == 1){
						if ($data_player[$data_player[$sys_plyerno][4]][3] eq 'WLF') {
							print "「$chr_wlf」ぽい人かな？"
						}else{
							print "「$chr_hum」ぽい人かな？"
						}
					}else{
						print "なんだかとても怪しい人かな？"
					}
					print "</TD></TR>";
				}
			}
			if($data_vildata[15] == $sys_plyerno){
				print "<TR><TD colspan=\"2\">【デスノ】朝起きると家の前に黒いノートが落ちていました。夜中の間に名前を書くことでその人を殺すことができます。";
				if($data_player[$sys_plyerno][13]){
					print "<br>ノートに$data_player[$data_player[$sys_plyerno][13]][7]さんの名前を書きました。";
				}
				print "</TD></TR>";
			}
			if ($data_player[$sys_plyerno][9] == 1) {
				print "<TR><TD colspan=\"2\">【沈　黙】アナタは他の様子を伺いながら沈黙しています。（発言はできます）</TD></TR>";
			}
			if ($data_player[$sys_plyerno][2] != 0) {
				print "<TR><TD colspan=\"2\">【投　票】アナタは<B>$data_player[$data_player[$sys_plyerno][2]][7]</B>さんに投票を行いました。</TD></TR>";
			}
			print "</TBODY></TABLE></TD></TR>\n";
		}else{
			print "<TR><TD>アナタは息絶えました・・・</TD></TR>\n";
		}
	}
	if($data_vildata[0] == 2 && $sys_plyerno <= $data_vildata[13]) {
		print "<TR><TD class=\"CLSTD01\">◆ アナタの情報</TD></TR>\n";
		if ($data_player[$sys_plyerno][5] eq 'W') {
			print "<TR><TD>アナタは<FONT color=\"FF0000\">勝利</FONT>しました。</TD></TR>\n";
		}else{
			print "<TR><TD>アナタは<FONT color=\"0000FF\">敗北</FONT>しました。</TD></TR>\n";
		}
	}
}
#---------------------------------------------------------------------
#  現在の日数と残り時間を表示する
#---------------------------------------------------------------------
sub disp_time{
	$wk_faze[0] = '';
	$wk_faze[1] = 'sun.gif';
	$wk_faze[2] = 'moon.gif';
	if($data_vildata[3] == 1){
		$max_time = $limit_times[$data_vildata[8]][0];
	}elsif($data_vildata[3] == 2){
		$max_time = $limit_times[$data_vildata[8]][1];
	}else {
		$max_time = $limit_times[$data_vildata[8]][2];
	}
	
	$r_time = $max_time - $_[4];
	print "<IMG src=\"".$imgpath."village.gif\" width=\"32\" height=\"32\" border=\"0\"> ";
	print "<FONT size=\"+2\">～ $_[5]村 ～</FONT><BR>";
	print "<IMG src=\"".$imgpath."clock.gif\" width=\"32\" height=\"32\" border=\"0\"> ";
	if($_[2]==0){
		print "<FONT size=\"+2\">事件前日</FONT>定員:$data_vildata[13]人";
	}else{
		print "<FONT size=\"+2\">$_[2]</FONT>日目 ";
		# 昼
		if ($_[3]==1 ||$_[3]==3){
			print "<IMG src=\"".$imgpath.$wk_faze[1]."\" border=\"0\"> ";
			if ($_[3]==1){
				$wk_min = int($r_time / 60);
				$wk_sec = $r_time - 60 * $wk_min;
				print "日没まであと <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>分";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>秒";
				}
				print "</span>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}else{
				# 投票判定
				$wk_nonvotecount = 0;
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
						$wk_nonvotecount++;
					}
				}
				$wk_min = int($r_time / 60);
				$wk_sec = $r_time - 60 * $wk_min;
				print "太陽が西の空に沈みかけています。";
				print "あと <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>分";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>秒";
				}
				print "</span>以内に<FONT size=\"+2\">投票</FONT>を行ってください。<BR>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
				print "あと<FONT size=\"+2\">$wk_nonvotecount</FONT>名の投票待ちとなっています。";
			}
		}
		# 夜
		if ($_[3]==2 ||$_[3]==4){
			print "<IMG src=\"".$imgpath.$wk_faze[2]."\" border=\"0\"> ";
			if ($_[3]==2){
				$wk_min = int(($max_time - $_[4]) / 60);
				$wk_sec = $max_time - 60 * $wk_min - $_[4];
				print "夜明けまであと <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>分";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>秒";
				}
				print "</span>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}else{
				# 投票判定
				$wk_min = int(($max_time - $_[4]) / 60);
				$wk_sec = $max_time - 60 * $wk_min - $_[4];
				print "東の空が白みはじめています。";
				print "あと <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>分";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>秒";
				}
				print "</span>以内に<FONT size=\"+2\">能\力対象</FONT>を決定してください。<BR>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}
		}
		print "<BR>\n";
	}
}
#---------------------------------------------------------------------
sub disp_msg{
	$wk_inputflg = 0;
	print "<TABLE cellpadding=\"0\"><TBODY>";
	open(IN, $file_log);
	while ($wk_inputflg == 0) {
		if ($_ = <IN>){
			$wk_msgwriteflg = 0;
			@wk_logdata = split(/,/, $_);
			# 開始前
			if ($data_vildata[0] == 0){
				$wk_msgwriteflg = 1;
			}
			# ゲーム中、終了後ログイン
			if ($data_vildata[0] == 1 || ($data_vildata[0] == 2 && $sys_logviewflg == 0)){
				# 昼
				if ($data_vildata[3] == 1 || $data_vildata[3] == 3){
					if ($wk_logdata[0] == $data_vildata[2] && ($wk_logdata[1] <= 2 || $wk_logdata[1] == 50)){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[0] == $data_vildata[2] - 1 && ($wk_logdata[1] == 2 || $wk_logdata[1] == 4)){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[0] <= $data_vildata[2] - 2) {
						$wk_inputflg = 9;
					}
				}
				# 夜
				if ($data_vildata[3] == 2 || $data_vildata[3] == 4){
					if ($wk_logdata[0] == $data_vildata[2]){
						if ($wk_logdata[1] == 2 || $wk_logdata[1] == 50) {
							$wk_msgwriteflg = 1;
						}
						if ($wk_logdata[1] == 3) {
							if($sys_plyerno == 60){ #観戦
								$wk_msgwriteflg = 2;
							}else{
								if(($data_player[$sys_plyerno][3] ne 'WLF' && $data_player[$sys_plyerno][3] ne 'BWL') && $data_player[$sys_plyerno][1] eq 'A') {
									$wk_msgwriteflg = 2;
								}else{
									$wk_msgwriteflg = 3;
								}
							}
						}
						if ($wk_logdata[1] == 5 && ($wk_logdata[2] == $sys_plyerno || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
							$wk_msgwriteflg = 4;
						}
						if ($wk_logdata[1] == 6 && ($data_player[$sys_plyerno][3] eq 'FRE' || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
							$wk_msgwriteflg = 5;
						}
					}
					if ($wk_logdata[0] <= $data_vildata[2] - 1) {
						$wk_inputflg = 9;
					}
				}
			}
			# ログ
			if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "1"){
				if ($wk_logdata[0] != 99){
						if ($wk_logdata[1] <= 50 && $wk_logdata[1] != 3){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[1] == 3) {
						$wk_msgwriteflg = 3;
					}
				}
			}
			if ($wk_msgwriteflg == 1){
				print "<TR>";
				if ($wk_logdata[2] == 0) {
					print "<TD colspan=\"2\">$wk_logdata[3]</TD>";
				}
				if ($wk_logdata[2] >= 1 && $wk_logdata[2] <= $data_vildata[13]) {
					print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">◆</FONT><b>$data_player[$wk_logdata[2]][7]</b>さん</TD><TD>「".$wk_logdata[3]."」</TD>";
				}
				if ($wk_logdata[2] == 24) {
					print "<TD valign=\"top\"><FONT color=\"FF9900\">◆<b>ゲームマスター</b></FONT></TD><TD>「".$wk_logdata[3]."」</TD>";
				}
				if ($wk_logdata[2] == 25) {
					print "<TD valign=\"top\">◆<b>村人達</b></TD><TD>".$wk_logdata[3]."</TD>";
				}
				if ($wk_logdata[2] >= 31 && $wk_logdata[2] <= 50) {
					print "<TD colspan=\"2\"><IMG src=\"".$imgpath;
					if ($wk_logdata[2] == 31) {
						print "msg.gif";
					}
					if ($wk_logdata[2] == 32) {
						print "ampm.gif";
					}
					if ($wk_logdata[2] == 33) {
						print "dead1.gif";
					}
					if ($wk_logdata[2] == 34) {
						print "dead2.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "dead3.gif";
					}
					if ($wk_logdata[2] == 41) {
						print "hum.gif";
					}
					if ($wk_logdata[2] == 42) {
						print "wlf.gif";
					}
					if ($wk_logdata[2] == 43) {
						print "ura.gif";
					}
					if ($wk_logdata[2] == 44) {
						print "bgd.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "\" width=\"40\" height=\"40\" border=\"0\"> $wk_logdata[3]</TD>";
					}else{
						print "\" width=\"32\" height=\"32\" border=\"0\"> $wk_logdata[3]</TD>";
					}
				}
				print "</TR>";
			}
			if ($wk_msgwriteflg == 2){
				print "<TR><TD valign=\"top\">◆狼の遠吠え<FONT color=\"#FF0000\"></TD><TD>「アオォーーン・・・」</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 3){
				print "<TR><TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの遠吠え</TD><TD><FONT color=\"#FF0000\">「".$wk_logdata[3]."」</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 4){
				print "<TR><TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの独り言</TD><TD><FONT color=\"#6666AA\">「".$wk_logdata[3]."」</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 5){
				print "<TR><TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの会話</TD><TD><FONT color=\"#33DD33\">「".$wk_logdata[3]."」</FONT></TD></TR>";
			}
		}else{
			$wk_inputflg = 9;
		}
	}
	close(IN);
	print "</TBODY></TABLE>\n";
}
#---------------------------------------------------------------------
# コマンド選択とメッセージ入力画面
#---------------------------------------------------------------------
sub disp_command{
	if($sys_plyerno == 60){
		return();
	}
	print "<TR><TD class=\"CLSTD01\">◆ 行動設定</TD></TR>\n";
	print "<TR><TD>\n";
	print "<TABLE cellpadding=\"0\" cellspacing=\"0\"><TBODY>";
	print "<TR><TD>行動内容：</TD>";
	print "<TD><SELECT name=\"COMMAND\">";
	if ($sys_plyerno <= $data_vildata[13]) {
		if ($data_player[$sys_plyerno][1] eq 'A' || $data_vildata[0]==2) {
			if ($data_vildata[3]==1 || $data_vildata[0]==2){
				print "<OPTION value=\"MSG\">発　言 [発言内容]</OPTION>\n";
				print "<OPTION value=\"MSG2\">強く発言 [発言内容]</OPTION>\n";
				print "<OPTION value=\"MSG3\">弱く発言 [発言内容]</OPTION>\n";
			}
			if ($data_vildata[0]==0) {
				print "<OPTION value=\"NAMECHG\">名前変更(10字以内) [発言内容]</OPTION>\n";
				print "<OPTION value=\"PROFILE\">プロフィール修正(40字以内) [発言内容]</OPTION>\n";
			}
			if ($data_vildata[0]==1) {
				if ($data_vildata[3]==2 || $data_vildata[3]==4) {
					if ($data_player[$sys_plyerno][3] eq 'WLF' || $data_player[$sys_plyerno][3] eq 'BWL'){
						print "<OPTION value=\"MSGWLF\">遠吠え [発言内容]</OPTION>\n";
					}
					if (($data_player[$sys_plyerno][3] eq 'WLF' || $data_player[$sys_plyerno][3] eq 'BWL') && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"KILL\">殺　る [行動対象]</OPTION>\n";
					}
					if (($data_player[$sys_plyerno][3] eq 'URA' || $data_player[$sys_plyerno][3] eq 'CFX') && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"FORTUNE\">占　う [行動対象]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'BGD' && $data_vildata[2] >= 2 && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"GUARD\">護　衛 [行動対象]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'FRE'){
						print "<OPTION value=\"MSGFRE\">会　話 [発言内容]</OPTION>\n";
					}
					if ($sys_plyerno == $data_vildata[15] && $data_player[$sys_plyerno][13] == 0){
						print "<OPTION value=\"DEATHNOTE\">手帳に書く [行動対象]</OPTION>\n";
					}
					print "<OPTION value=\"MSG1\">独り言 [発言内容]</OPTION>\n";
				}
				if (($data_vildata[3]==1 || $data_vildata[3]==3) && $data_player[$sys_plyerno][2] == 0){
					print "<OPTION value=\"VOTE\">投　票 [行動対象]</OPTION>\n";
				}
				if ($data_vildata[3]==1 && $data_player[$sys_plyerno][9] == 0){
					print "<OPTION value=\"SILENT\">沈　黙</OPTION>\n";
				}
			}
		}else{
			print "<OPTION value=\"MSG0\">霊　話 [発言内容]</OPTION>\n";
		}
	}
	# 管理者
	if($data_vildata[10]==0){
		if ($sys_plyerno == 50) {
			print "<OPTION value=\"MSGM0\">管理者霊　話 [発言内容]</OPTION>\n";
			print "<OPTION value=\"MSGM\">管理者メッセージ [発言内容]</OPTION>\n";
			print "<OPTION value=\"VOTECHK\">投票集計</OPTION>\n";
			print "<OPTION value=\"SHOCK\">突然死 [行動対象]</OPTION>\n";
			print "<OPTION value=\"REVOTE\">再投票</OPTION>\n";
			if ($data_vildata[0]==0){
				&print_gmmes;
			}
		}
	}elsif($sys_plyerno == 2 && $data_vildata[0]==0){
		&print_gmmes;
	}
	print "<OPTION value=\"\">更　新</OPTION>\n";
	print "</SELECT></TD>";
	print "<TD width=\"6\"></TD>";
	print "<TD>行動対象：</TD>";
	print "<TD><SELECT name=\"CMBPLAYER\">";
	print "<OPTION value=\"0\">----</OPTION>\n";
	for ($i = 1; $i <= $data_vildata[1]; $i++) {
		if ($i != $sys_plyerno && $data_player[$i][1] eq 'A') {
			print "<OPTION value=\"$data_player[$i][0]\">$data_player[$i][7]</OPTION>\n";
		}
	}
	print "</SELECT></TD></TR>";
	print "</TBODY></TABLE>";
	#print "発言内容：<INPUT type=\"text\" size=\"100\" name=\"TXTMSG\"><BR>\n";
	print "<TABLE cellpadding=\"0\" cellspacing=\"0\"><TBODY><TR>";
	print "<TD valign=\"top\">発言内容：</TD><TD><TEXTAREA rows=\"3\" cols=\"70\" name=\"comment\"></TEXTAREA></TD>\n";
	print "</TR></TBODY></TABLE>";
	print "<INPUT type=\"submit\" value=\"上の内容で行動\">\n";
	print "</TD></TR>\n";
}
sub print_gmmes{
	print "<OPTION value=\"START\">ゲームの開始(妖孤無し)</OPTION>\n";
	print "<OPTION value=\"STARTF\">ゲームの開始(妖孤有り)</OPTION>\n";
	print "<OPTION value=\"STARTFF\">ゲームの開始(妖孤増える)</OPTION>\n";
	print "<OPTION value=\"PLEYERDEL\">村人登録の抹消</OPTION>\n";
	print "<OPTION value=\"VILNAME\">村名変更(8字以内) [発言内容]</OPTION>\n";
	print "<OPTION value=\"VILRULE\">ルール変更(数字) [発言内容]</OPTION>\n";
	print "<OPTION value=\"VILBET\">賭け有無変更(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"VILMASSACRE\">大量殺戮村スイッチ(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"VILMAX\">定員数(数字) [発言内容]</OPTION>\n";
	print "<OPTION value=\"FANATIC\">狂信者スイッチ(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"DEATHNOTE\">死神の手帳(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"BWLF\">大狼(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"CFOX\">子狐(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"SIXVIL\">六人村(0or1) [発言内容]</OPTION>\n";
	print "<OPTION value=\"CHAVIL\">配役規定村(0or1) [発言内容]</OPTION>\n";
	if($data_vildata[19]){
		print "<OPTION value=\"NUMWLF\">人狼数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMURA\">占い数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMNEC\">霊能\数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMMAD\">狂人数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMFRE\">共有数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMBGD\">狩人数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMFOX\">妖狐数(数字) [発言内容]</OPTION>\n";
		print "<OPTION value=\"NUMROL\">猫又数(数字) [発言内容]</OPTION>\n";
	}
}
#---------------------------------------------------------------------
sub disp_msgdead{
	$wk_writeflg = 0;
	if ($data_vildata[0] == 1 && ($data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
		$wk_writeflg = 1;
	}
	if ($data_vildata[0] == 2 && $sys_logviewflg == 0){
		$wk_writeflg = 1;
	}
	if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "2"){
		$wk_writeflg = 2;
	}

	if ($wk_writeflg >= 1){
		print "<TR><TD class=\"CLSTD01\">◆ 幽霊の間</TD></TR>\n";
		print "<TR><TD class=\"CLSTD02\">\n";
		print "<TABLE cellpadding=\"0\" class=\"CLSTABLE2\"><TBODY>";
		open(IN, $file_log);
		$wk_msgcount = 0;
		$wk_inputflg = 0;
		while ($wk_inputflg == 0) {
			if ($_ = <IN>) {
				@wk_logdata = split(/,/, $_);
				if ($wk_logdata[0] == 99){
					$wk_msgcount++;
					print "<TR>\n";
					if ($wk_logdata[2] == 24) {
						print "<TD valign=\"top\"><FONT color=\"FF6600\">◆<b>ゲームマスター</b></FONT></TD><TD>「".$wk_logdata[3]."」</TD>";
					}else{
						print "<TR><TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">◆</FONT><b>$data_player[$wk_logdata[2]][7]</b>さん</TD><TD>「".$wk_logdata[3]."」</TD></TR>";
					}
					print "</TR>\n";
				}
				if ($wk_msgcount >= 20 && $wk_writeflg == 1){
					$wk_inputflg = 9;
				}
			}else{
				$wk_inputflg = 9;
			}
		}
		close(IN);
		print "</TBODY></TABLE>\n";
		print "</TD></TR>\n";
	}
}

sub disp_msgall{
	$wk_inputflg = 0;
	print "<TABLE cellpadding=\"0\"><TBODY>";
	open(IN, $file_log);
	while ($wk_inputflg == 0) {
		if ($_ = <IN>){
			$wk_msgwriteflg = 0;
			@wk_logdata = split(/,/, $_);
			
			# ログ
			if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "3"){
				if ($wk_logdata[0] != 99){
					if ($wk_logdata[1] <= 50 && $wk_logdata[1] != 3){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[1] == 3) {
						$wk_msgwriteflg = 3;
					}
				}else{
					$wk_msgwriteflg = 5;
				}
			}
			if ($wk_msgwriteflg == 1){
				print "<TR>";
				if ($wk_logdata[2] == 0) {
					print "<TD colspan=\"2\">$wk_logdata[3]</TD>";
				}
				if ($wk_logdata[2] >= 1 && $wk_logdata[2] <= $data_vildata[13]) {
					if ($wk_logdata[1] == 5){
						print "<TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの独り言</TD><TD><FONT color=\"#6666AA\">「".$wk_logdata[3]."」</FONT></TD>";
					}elsif ($wk_logdata[1] == 6){
						print "<TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの会話</TD><TD><FONT color=\"#33DD33\">「".$wk_logdata[3]."」</FONT></TD>";
					}else{
						print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">◆</FONT><b>$data_player[$wk_logdata[2]][7]</b>さん</TD><TD>「".$wk_logdata[3]."」</TD>";
					}
				}
				if ($wk_logdata[2] == 24) {
					print "<TD valign=\"top\"><FONT color=\"FF9900\">◆<b>ゲームマスター</b></FONT></TD><TD>「".$wk_logdata[3]."」</TD>";
				}
				if ($wk_logdata[2] == 25) {
					print "<TD valign=\"top\">◆<b>村人達</b></TD><TD>".$wk_logdata[3]."</TD>";
				}
				if ($wk_logdata[2] >= 31 && $wk_logdata[2] <= 50) {
					print "<TD colspan=\"2\"><IMG src=\"".$imgpath;
					if ($wk_logdata[2] == 31) {
						print "msg.gif";
					}
					if ($wk_logdata[2] == 32) {
						print "ampm.gif";
					}
					if ($wk_logdata[2] == 33) {
						print "dead1.gif";
					}
					if ($wk_logdata[2] == 34) {
						print "dead2.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "dead3.gif";
					}
					if ($wk_logdata[2] == 41) {
						print "hum.gif";
					}
					if ($wk_logdata[2] == 42) {
						print "wlf.gif";
					}
					if ($wk_logdata[2] == 43) {
						print "ura.gif";
					}
					if ($wk_logdata[2] == 44) {
						print "bgd.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "\" width=\"40\" height=\"40\" border=\"0\"> $wk_logdata[3]</TD>";
					}else{
						print "\" width=\"32\" height=\"32\" border=\"0\"> $wk_logdata[3]</TD>";
					}
				}
				print "</TR>";
			}
			if ($wk_msgwriteflg == 2){
				print "<TR><TD valign=\"top\">◆狼の遠吠え<FONT color=\"#FF0000\"></TD><TD>「アオォーーン・・・」</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 3){
				print "<TR><TD valign=\"top\" width=\"140\">◆<b>$data_player[$wk_logdata[2]][7]</b>さんの遠吠え</TD><TD><FONT color=\"#FF0000\">「".$wk_logdata[3]."」</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 5){
				print "<TR bgcolor=\"#E3E3E3\">\n";
				if ($wk_logdata[2] == 24) {
					print "<TD valign=\"top\"><FONT color=\"FF6600\">◆<b>ゲームマスター</b></FONT></TD><TD>「".$wk_logdata[3]."」</TD>";
				}else{
					print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">◆</FONT><b>$data_player[$wk_logdata[2]][7]</b>さん</TD><TD>「".$wk_logdata[3]."」</TD>";
				}
				print "</TR>\n";
			}
		}else{
			$wk_inputflg = 9;
		}
	}
	close(IN);
	print "</TBODY></TABLE>\n";
}
#---------------------------------------------------------------------
sub disp_foot{
	print "<TR><TD class=\"CLSTD01\"><A href=\"$return_url\">戻る</A></TD></TR>\n";
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print "</TBODY></TABLE></FORM></BODY>\n";
	print "</HTML>\n";
}
#---------------------------------------------------------------------
# 勝利結果を表示
#---------------------------------------------------------------------
sub sub_judge{
	$wk_alivewlf = 0;
	$wk_alivehum = 0;
	$wk_alivefox = 0;
	for ($i = 1; $i <= $data_vildata[1]; $i++) {
		if ($data_player[$i][1] eq 'A'){
			if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL'){
				$wk_alivewlf++;
			}elsif ($data_player[$i][3] eq 'FOX' || $data_player[$i][3] eq 'CFX'){
				$wk_alivefox++;
			}else{
				$wk_alivehum++;
			}
		}
	}
	if ($wk_alivewlf == 0) {
		if ($wk_alivefox == 0) {
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 1;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				$v = -10000;
				&send_coin($v, $data_player[$i][8], 0);
				if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL' || $data_player[$i][3] eq 'MAD' || $data_player[$i][3] eq 'FOX' || $data_player[$i][3] eq 'CFX'){
					$data_player[$i][5] = 'L';
				}else{
					if ($data_player[$i][1] eq 'D'){
						$data_player[$i][5] = 'W';		#死亡している村人も勝者
					}else{
						$data_player[$i][5] = 'W';		#生存者のみ勝利者とする
						$v = 5000;
						&send_coin($v, $data_player[$i][8], 2);
					}
					$v = 15000;
					&send_coin($v, $data_player[$i][8], 1);
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">人狼の血を根絶することに成功しました！</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">「$chr_hum」の勝利です！</FONT>");
		}else{
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 2;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				$v = -10000;
				&send_coin($v, $data_player[$i][8], 0);
				if ($data_player[$i][3] eq 'FOX' || $data_player[$i][3] eq 'CFX'){
					$data_player[$i][5] = 'W';
					$v = 10000 * $data_vildata[1];
					&send_coin($v, $data_player[$i][8], 1);
				}else{
					$data_player[$i][5] = 'L';
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">人狼がいなくなった今、我の敵などもういない。</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">「$chr_fox」の勝利です！</FONT>");
		}
	}
	if ($wk_alivewlf >= $wk_alivehum) {
		if ($wk_alivefox == 0) {
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 3;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				$v = -10000;
				&send_coin($v, $data_player[$i][8], 0);
				if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'BWL' || $data_player[$i][3] eq 'MAD'){
					if ($data_player[$i][1] eq 'D'){
						$data_player[$i][5] = 'W';		#死亡している人狼も勝者
					}else{
						$data_player[$i][5] = 'W';		#生存者のみ勝利者とする
						$v = 10000;
						&send_coin($v, $data_player[$i][8], 2);
					}
					$v = $data_vildata[1] < 10 ? int(10000 * $data_vildata[1] / 2):
							$data_vildata[1] < 16 ? int(10000 * $data_vildata[1] / 3):
							$data_vildata[1] < 18 ? int(10000 * $data_vildata[1] / 4):
													int(10000 * $data_vildata[1] / 5);
					&send_coin($v, $data_player[$i][8], 1);
				}else{
					$data_player[$i][5] = 'L';
					if($data_player[$i][1] eq 'A'){
						$data_player[$i][1] = 'D';	#敗北した村人は食い殺されて死亡
						&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$i][7]</b>さんは<FONT color=\"#ff0000\">正体を現した人狼に襲われて殺された・・・。</FONT>");
					}
				}
			}
			
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">最後の一人を食い殺すと人狼達は次の獲物を求めて村を後にした・・・。</FONT>");
			&msg_write($data_vildata[2], 1, 42,"<FONT size=\"+2\" color=\"#DD0000\">「$chr_wlf」の勝利です！</FONT>");
		}else{
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 4;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				$v = -10000;
				&send_coin($v, $data_player[$i][8], 0);
				if ($data_player[$i][3] eq 'FOX' || $data_player[$i][3] eq 'CFX'){
					$data_player[$i][5] = 'W';
					$v = 10000 * $data_vildata[1];
					&send_coin($v, $data_player[$i][8], 1);
				}else{
					$data_player[$i][5] = 'L';
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">マヌケな人狼どもを騙すことなど容易いことだ。</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">「$chr_fox」の勝利です！</FONT>");
		}
	}
}
#---------------------------------------------------------------------
# Cookieの値を読み出す
#
sub getCookie {
	local($xx, $name, $value);
	foreach $xx (split(/; */, $ENV{'HTTP_COOKIE'})) {
		($name, $value) = split(/=/, $xx);
		$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
		$COOKIE{$name} = $value;
	}
}

#---------------------------------------------------------------------
# Cookieに値を書き込むためのSet-Cookie:ヘッダを生成する
#
sub setCookie {
	local($tmp, $val);
	$val = $_[1];
	$val =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
	$tmp = "Set-Cookie: ";
	$tmp .= "$_[0]=$val; ";
	$tmp .= "expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
	return($tmp);
}
sub sysadoin{

	open(IN, $sys_path_bak);
	$wk_count = 1;
	$sys_ID_COUNT = 0;
	while (<IN>) {
		$value = $_;
		$value =~ s/\n//g;
		
		@wk_player = split(/,/, $value);
		$sys_ID[$wk_count] = $wk_player[0];
		$sys_pass[$wk_count] = $wk_player[1];
		$sys_name[$wk_count] = $wk_player[2];
		$wk_count++;
		$sys_ID_COUNT++;
		}
	close(IN);
}

sub randomarr{
	$size = shift;
	@rarr = (0);
	
	for my $i (1..$size){
		push @rarr, $i;
	}
	
	for my $i (1..$size){
		my $j = int(rand($size - $i) + $i);
		my $temp = $rarr[$i];
		$rarr[$i] = $rarr[$j];
		$rarr[$j] = $temp;
	}
	
	return @rarr;
}

sub send_coin{
	return unless $data_vildata[11];
	my ($s_coin, $s_name, $s_flag) = @_;
	return if($s_name eq '管理者');
	require './config_game.cgi';
	my %datas = &get_you_datas($s_name);
	my $v_coin = $datas{coin} + $s_coin;
	$v_coin = $vcoin < 0 ? 0 : $v_coin;
	&regist_you_data($s_name, 'coin', $v_coin);
	$g_msg = "$s_nameは";
	if($s_flag == 0){
		$msg_coin = $s_coin * -1;
		$g_msg .= "参加料として $msg_coin ｺｲﾝ払いました";
	}elsif($s_flag == 1){
		$g_msg .= "賞金として $s_coin ｺｲﾝ貰いました";
	}elsif($s_flag == 2){
		$g_msg .= "生存ボーナスとして $s_coin ｺｲﾝ貰いました";
	}
	&msg_write($data_vildata[2], 1, 0,$g_msg);
	return;
}

1;