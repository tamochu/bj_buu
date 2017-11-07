use Time::HiRes;
$load_time = Time::HiRes::time unless $load_time;
require './lib/jcode.pl';
require './lib/summer_system.cgi';
use Time::Local;
&get_date; # 時間と日付は常時必要なので常に取得
use LWP::UserAgent;
use lib q(./lib);
use FlockWrapper(flock => 'mkdir', dir => './lock');
use MIME::Base64;
use Encode;

#================================================
# ﾒｲﾝでよく使う処理 Created by Merino
#================================================

#================================================
# 国 + 世界 データ読み込み countries
#================================================
sub read_cs {
	# -------------------
	# Get %cs
	# 国に属していない場合の国名と色
	%cs = (
		name  => ['ﾈﾊﾞｰﾗﾝﾄﾞ'],
		color => ['#CCCCCC'],
	);
	my $i = 1;
	open my $fh, "< $logdir/countries.cgi" or &error("国ﾃﾞｰﾀが読み込めません");
	my $world_line = <$fh>;
	while (my $line = <$fh>) {
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$cs{$k}[$i] = $v;
		}
		++$i;
	}
	close $fh;
	
	# -------------------
	# Get %w
	%w  = ();
	$union = 0;
	for my $hash (split /<>/, $world_line) {
		my($k, $v) = split /;/, $hash;
		$w{$k} = $v;
		
		# 自分が所属している国に同盟国があるなら $union に set
		if ($k =~ /^p_(\d)_(\d)$/ && $v eq '1') {
			if ($m{country} eq $1) {
				$union = $2;
			}
			elsif ($m{country} eq $2) {
				$union = $1;
			}
		}
	}
	
	# -------------------
	# 統一国力 と 無所属を含まない国名だけの配列作成
	@contries = ();
	my $all_strong = 0;
	for my $i (1 .. $w{country}) {
		$all_strong += $cs{strong}[$i];
		push @countries, $cs{name}[$i];
	}
	$touitu_strong = int($all_strong * $w{game_lv} * 0.01);
	
	# -------------------
	# 自国名と相手国名頻繁に使うので簡単な変数に
	$c_m = $cs{name}[$m{country}];
	$c_y = $cs{name}[$y{country}];
	
	# 空ﾃﾞｰﾀ読み込み制御
	&error("国ﾃﾞｰﾀの読み込みに失敗しました") if $cs{name}[1] eq '';
}

#================================================
# プレイヤーデータ読み込み
#================================================
sub read_user { # Get %m %y
	%m = ();
	%y = ();
	
	$id   = $in{id} || unpack 'H*', $in{login_name};
	$pass = $in{pass};
	
	open my $fh, "< $userdir/$id/user.cgi" or &error("そのような名前$in{login_name}のﾌﾟﾚｲﾔｰが存在しません");
	my $line = <$fh>;
	close $fh;
	
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		
		if ($k =~ /^y_(.+)$/) {
			$y{$1} = $v;
		}
		else {
			$m{$k} = $v;
		}
	}
	&error('ﾊﾟｽﾜｰﾄﾞが違います') unless $m{pass} eq $pass;
	
	# 拘束時間がある場合、経過時間分減らす
	$m{wt} -= ($time - $m{ltime}) if $m{wt} > 0;

#	$m{money_limit} = $m{money};
	
	$m{cha_org} = $m{cha};
	
	$m{debug} = $line;
	
	&read_summer;

	if ($m{tutorial_switch}) {
		require './lib/tutorial.cgi';
		&read_tutorial;
	}
}

#==========================================================
# headerなど一式ｾｯﾄ bj.cgi bbs_xxxx.cgi chat_xxxx.cgiなどで使用
#==========================================================
sub get_data {
	&decode;
	&header;
	&read_user;
	&access_check;
	&read_cs;
}

#================================================
# 自分が鯖管かどうか
#================================================
sub is_sabakan {
	for my $k ($admin_name, $admin_sub_name, $admin_support_name) {
		return 1 if $m{name} eq $k;
	}
	return 0;
}

#================================================
# 自分が国の代表者かどうか
#================================================
sub is_daihyo {
	for my $k (qw/war dom pro mil ceo/) {
		return 1 if $m{name} eq $cs{$k}[$m{country}];
	}
	return 0;
}

#================================================
# 自分が国の君主かどうか
#================================================
sub is_ceo {
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		return 1;
	}
	return &is_sabakan;
}

#==========================================================
# 国の昇順を返す 1_2,1_3とか。(2_1ﾌｧｲﾙは存在しないので)
#==========================================================
# &union(国1,国2); って書くと取得できるよ
sub union {
	my($country_1, $country_2) = @_;
	return $country_1 < $country_2 ? "${country_1}_${country_2}" : "${country_2}_${country_1}";
}

#==========================================================
# 手紙書き込み処理 letter.cgi marriage.cgiで使用
#==========================================================
sub send_letter {
	my($name, $is_save_log) = @_;
	my $letter_type = 1;
	if ($this_file =~ /blog/) {
		$letter_type = 3;
	}
	elsif ($this_script =~ /horyu/) {
		$letter_type = 4;
	}

	if ($name =~ /^&lt;(.*)&gt;$/ && &is_sabakan) {
		&send_group($1);
		return;
	}
	
	&error('送り先の名前がありません') if $name eq '';
	my $send_id = unpack 'H*', $name;
	
	local $this_file = "$userdir/$send_id/letter";
	&error("$nameというﾌﾟﾚｲﾔｰが存在しません") unless -f "$this_file.cgi";

	require './lib/_bbs_chat.cgi';
	local $max_log = 100;
	&write_comment;

	# 手紙があるよﾌﾗｸﾞをたてる
	&set_letter_flag($send_id, $letter_type);

	my %you_datas = &get_you_datas($send_id, 1);
	my @mail_datas = split /,/, $you_datas{mail_address}; # [0]ﾒｰﾙｱﾄﾞﾚｽ [1]日記 [2]改造案

	if ($mail_datas[0] =~ /^[^@]+@[^.]+\..+/ && ($letter_type == 1 || ($mail_datas[1] && $letter_type == 3) || ($mail_datas[2] && $letter_type == 4))) {
		my $sendmail = '/usr/sbin/sendmail';
		my $from = 'Blind Justice にゃあ鯖';
		my $to = $you_datas{mail_address};
		my $cc = '';
		my $subject = '手紙が届きました';
		my $msg = <<"EOS";
手紙が届いています。
----------------------------------------
Blind Justice にゃあ鯖
http://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi

※このメールは手紙の受信通知です。返信しても相手ユーザーには届きません。
※このメールに心当たりがない場合は、お手数ですがこのメールへの返信にてお問い合わせください。
また、今後このメールを受け取らない場合は、ログイン→マイルーム→自己紹介の「メールアドレス（手紙の受信通知に利用）」の項目を空に変更してください。
----------------------------------------
EOS

		$subject = Encode::encode('ISO-2022-JP', Encode::decode('Shift_JIS', $subject));
		$subject = encode_base64($subject, '');
		$subject = "=?ISO-2022-JP?B?$subject?=";
		$from = Encode::encode('ISO-2022-JP', Encode::decode('Shift_JIS', $from));
		$from = encode_base64($from, '');
		$from = "=?ISO-2022-JP?B?$from?= <nyaa\@pandora.nu>";
		$msg = Encode::encode('ISO-2022-JP', Encode::decode('Shift_JIS', $msg));
		
		open(SDML,"| $sendmail -i -f nyaa\@pandora.nu $to") || die 'sendmail error';
		print SDML "From: $from\n";
		print SDML "To: nyaa\@pandora.nu\n";
		print SDML "Cc: $cc\n";
		print SDML "Subject: $subject\n";
		print SDML "MIME-Version: 1.0\n";
		print SDML "Content-Type: text/plain; charset=ISO-2022-JP\n";
		print SDML "Content-Transfer-Encoding: 7bit\n\n";
		print SDML "$msg";
		close(SDML);
	}

	&send_letter_save_log($name) if $is_save_log eq '1';
}
# ------------------
# 送信履歴保存
sub send_letter_save_log {
	my $name = shift;
	my @lines = ();
	open my $fh, "+< $userdir/$id/letter_log.cgi" ;
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>$name<><><>$addr<>$in{comment}<><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

sub send_group {
	$group = shift;
	if ($group eq 'all') {
		my @names = &get_player_name_list;
		for my $name (@names) {
			&send_letter($name, 0);
		}
	} elsif ($group eq 'ceo') {
		for my $i (1..$w{country}) {
			if ($cs{ceo}[$i]) {
				&send_letter($cs{ceo}[$i], 0);
			}
		}
	} elsif ($group eq 'daihyo') {
		for my $i (1..$w{country}) {
			for my $k (qw/war dom pro mil ceo/) {
				if ($cs{$k}[$i]) {
					&send_letter($cs{$k}[$i], 0);
				}
			}
		}
	} else {
		&error("$groupというグループは存在しません");
	}
}

#==========================================================
# 国の方針取得(国の引数を与えるとその国の方針だけ)
#==========================================================
sub get_countries_mes {
	my $country = shift;

	my @lines = ();
	open my $fh, "< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fh;
	return $country ? $lines[$country] : @lines;
}


#================================================
# デコード
#================================================
sub decode {
	local ($k,$v,$buf);
	my $err_flag = 0;

	if ($ENV{REQUEST_METHOD} eq 'POST') {
		&error('投稿量が大きすぎます',1) if $ENV{CONTENT_LENGTH} > 51200;
		read STDIN, $buf, $ENV{CONTENT_LENGTH};
	}
	else {
		&error('投稿量が大きすぎます',1) if length $ENV{QUERY_STRING} > 51200;
		$buf = $ENV{QUERY_STRING};
	}
	
	for my $pair (split /&/, $buf) {
		($k,$v) = split /=/, $pair;
		$v =~ tr/+/ /;
		$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack 'H2', $1/eg;

		# jcode.pl 文字化け防止用
		&jcode'convert(*v, 'sjis', 'sjis');#'

		# 記号置換え
		$v =~ s/&/&amp/g;
		$v =~ s/;/&#59;/g;
		$v =~ s/&amp/&amp;/g;
		$v =~ s/,/&#44;/g;
		$v =~ s/</&lt;/g;
		$v =~ s/>/&gt;/g;
		$v =~ s/"/&quot;/g;#"
		$v =~ s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]//g;
		$v =~ s/\.\.\///g;
		$v =~ s/【ダイス】/(ダイス)/g;
		
		# BBS系の書き込み
		if ($k eq 'comment') {
			$v =~ s/\r\n/<br>/g;
			$v =~ s/\r/<br>/g;
			$v =~ s/\n/<br>/g;
			$v =~ s|ホォシ|<font color="#FFD700">★</font>|g;
			$v =~ s|オゥプ|<font color="#00FA9A">♪</font>|g;
		}
		else {
			$v =~ tr/\x0D\x0A//d; # 改行削除
		}

		$in{$k} = $v;
		
		push @delfiles, $v if $k eq 'delete';
	}
	$cmd = $in{cmd};
}

#================================================
# ｱｸｾｽﾁｪｯｸ Get $addr $host $agent
#================================================
sub access_check {
	$addr = $ENV{REMOTE_ADDR};
	$host = $ENV{REMOTE_HOST};
	
#	if ($gethostbyaddr && ($host eq '' || $host eq $addr)) {
#		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
#	}

	$host = $addr if $host eq '';

	for my $deny (@deny_lists) {
		$deny =~ s/\./\\\./g;
		$deny =~ s/\*/\.\*/g;
		
		if ($is_mobile) {
			&error($deny_message . $agent) if $agent =~ /$deny/;
		}
		else {
			&error($deny_message . $addr) if $addr =~ /^$deny$/i;
			&error($deny_message . $host) if $host =~ /^$deny$/i;
		}
	}
	my $logging = 1;
	for my $nolog (@nolog_lists) {
		$nolog =~ s/\./\\\./g;
		$nolog =~ s/\*/\.\*/g;
		
		if ($is_mobile) {
			$logging = 0 if $agent =~ /$nolog/;
		}
		else {
			$logging = 0 if $addr =~ /^$nolog$/i;
			$logging = 0 if $host =~ /^$nolog$/i;
		}
	}
	
	if ($logging) {
		my $is_find = 0;
		if(-f "$userdir/$id/access_log.cgi"){
			open my $fh, "< $userdir/$id/access_log.cgi" or &error("そのような名前$in{login_name}のﾌﾟﾚｲﾔｰが存在しません");
			while (my $line = <$fh>){
				my($access_addr, $access_host, $access_agent) = split /<>/, $line;
				if($is_mobile){
					if($access_agent eq $agent){
						$is_find = 1;
					}
				}else{
					if($access_addr eq $addr && $access_host eq $host && $access_agent eq $agent){
						$is_find = 1;
					}
				}
			}
			close $fh;
		}
		if(!$is_find && $id){
			open my $fh2, ">> $userdir/$id/access_log.cgi" or &error("そのような名前$in{login_name}のﾌﾟﾚｲﾔｰが存在しません");
			print $fh2 "$addr<>$host<>$agent<>\n";
			close $fh2;
			
		}
	} else {
		$agent = 'admin_agent';
		$addr = '0.0.0.0';
		$host = 'admin_login';
	}
}

#================================================
# 時間取得 Get $time $date
#================================================
sub get_date {
	$time = time();
	my($min,$hour,$mday,$mon,$year) = (localtime($time))[1..4];
	$date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
}

#================================================
# header
#================================================
sub header {
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
	if (!$is_mobile && !$is_appli) {
#	unless ($is_mobile) {
		print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
		print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">|;
		print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/bj.js?$jstime"></script>\n|;
		&load_RWD;
#		if ($is_smart) {
#			print qq|<meta name="viewport" content="width=device-width">|;
#			print qq|<meta name="viewport" content="width=device-width, maximum-scale=1.5, minimum-scale=0.5,user-scalable=yes,initial-scale=0.9" />|;
#			print qq|<link rel="stylesheet" media="screen and (max-width: 480px)" href="$htmldir/smart.css" />|;
#			print qq|<link rel="stylesheet" media="screen and (min-width: 481px)" href="$htmldir/tablet.css" />|;
#			print qq|<link rel="stylesheet" media="screen and (min-width: 481px) and (max-width: 720px)" href="$htmldir/tablet.css?$jstime" />|;
#		}
	}
	elsif ($is_mobile) {
		# ガラケーで外部CSSの読み込みはNG
		# HTMLファイルを読み込んだ後にCSSファイルを読み込むため、
		# 素のHTMLが表示された後にCSSが適用され画面がチラつくなどの問題がある
		print qq|<style type="text/css"><!-- a.clickable_name {color: inherit; text-decoration: none;} --></style>|;
	}
	elsif ($is_appli) {
		print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
#		print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
		print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj_appli.css?$jstime">|;
		print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/bj.js?$jstime"></script>\n|;
=pod
		print qq|<script>|;
		print qq|var pinching = false;|;
		print qq|var d0 = 1;|;
		print qq|var d1 = 1;|;
		print qq|var dx = 0;|;
		print qq|var scale = 1;|;
#		print qq|document.getElementById("body").onscroll = function(){|;
#		print qq|  var $scrollLeft = this.scrollLeft;|;
#		print qq|  document.querySelector("#commands").style.left = $scrollLeft;|;
#		print qq|};|;
		print qq|document.addEventListener("touchmove", function(e){|;
		print qq|  if (e.touches.length == 2) {|;
		print qq|    if (!pinching) {|;
		print qq|      pinching = true;|;
		print qq|      scale = ev.originalEvent.scale;|;
		print qq|      d0 = Math.sqrt(|;
		print qq|        Math.pow(e.touches[1].screenX - e.touches[0].screenX, 2) +|;
		print qq|        Math.pow(e.touches[1].screenY - e.touches[0].screenY, 2)|;
		print qq|      );|;
		print qq|      dx = e.touches[0].screenX;|;
		print qq|    } else {|;
		print qq|      d1 = Math.sqrt(|;
		print qq|        Math.pow(e.touches[1].screenX - e.touches[0].screenX, 2) +|;
		print qq|        Math.pow(e.touches[1].screenY - e.touches[0].screenY, 2)|;
		print qq|      );|;
#		print qq|      document.querySelector("#commands").style.zoom = d1 / d0;|;
		print qq|      document.querySelector("#commands").style.width = window.innerWidth / scale;|;
#		print qq|      document.querySelector("#commands").style.margin-left = dx;|;
		print qq|    }|;
		print qq|  }|;
		print qq|});|;
		print qq|document.addEventListener("touchend", function(e){|;
		print qq|  pinching = false;|;
		print qq|});|;
		print qq|</script>|;
=cut
		print qq|<script type="text/javascript" src="$htmldir/js/appli.js?$jstime"></script>\n|;
	}
#	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	unless ($is_appli) {
		print qq|<title>$title</title>|;
		print qq|</head><body $body><a name="top"></a>|;
	}
	else {
		my $footer = "";
		$footer .= qq|<form method="$method" action="" class="cmd_form">|;
		$footer .= qq|<input type="submit" value="button22" class="button2s">|;
		$footer .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$footer .= qq|</form>|;

		print qq|<title>$title</title>|;
#		print qq|</head><body><div id="container"><div id="header">ヘッダー</div><div id="contents">コンテンツ</div><div id="footer">$footer</div></div></body>|;
#		print qq|</head><body><div id="container"><div id="header">過去の栄光とか</div><div id="contents"></div><div id="footer">$footer</div></div></body>|;
		print qq|</head><body><div id="container"><div id="contents">|;
	}
}
#================================================
# footer
#================================================
sub footer {
	print qq|<p><a href="#top">▲上</a></p>| if $is_mobile;
	print qq|<br><div align="right" style="font-size:11px">|;
	print qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama楽.net</a><br><a href="http://www.game-smartphone.com/simulation/game_387.html">スマートフォンゲームズ</a><br>当サイトでは<a href="https://www.emojione.com/">Emoji One</a>の絵文字を利用しています(<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>)<br>|; # 著作表示:削除・非表示 禁止!!
	print qq|$copyright|;
	printf("%0.10f秒",Time::HiRes::time - $load_time);
	print qq|</div>|;
	print qq|</div>| if $is_appli;
	print qq|</body></html>|;
}

#==========================================================
# エラー画面表示
#==========================================================
sub error {
	my($error_mes, $is_need_header) = @_;
	
	&header if $is_need_header;
	print qq|<div class="mes">$error_mes<br><br></div>\n|;
	print qq|<form action="$script_index"><p><input type="submit" value="ＴＯＰ" class="button1"></p></form>|;
#	&cs_data_repair;
	&log_errors($error_mes);

	&footer;
	exit;
}

#=========================================================
# クッキー取得
#=========================================================
sub get_cookie {
	my $cook = $ENV{HTTP_COOKIE};
	my %cooks;
	my @cooks;

	for my $pair (split /;/, $ENV{HTTP_COOKIE}) {
		my($k, $v) = split /=/, $pair;
		$k =~ s/\s//g;
		$cook{$k} = $v;
	}
	for my $c (split /<>/, $cook{bj}) {
		$c =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack 'H2', $1/eg;
		push @cooks, $c;
	}
	return @cooks;
}

#================================================
# 所持している物の個数
#================================================
sub my_goods_count {
	my $dir_path = shift;
	
	my $count = 0;
	opendir my $dh, $dir_path or &error("$dir_pathﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		++$count;
	}
	closedir $dh;
	
	return $count;
}

#================================================
# 作品のﾀｲﾄﾙ取得
#================================================
sub get_goods_title {
	my $file_name = shift;
	my($file_base) = ($file_name =~ /^(.+)\.[^\.]+$/);
	return $file_base =~ /^_/ || $file_base eq '' ? $non_title : pack 'H*', $file_base;
}

#================================================
# 日付をtimeに(YYYY-MM-DD)
#================================================
sub date_to_time {
	my $date = shift;
	my ($year, $mon, $day) = ($date =~ /(\d{4})\-([01]\d)\-([0-3]\d)/);
	return timelocal(0, 0, 0, $day, $mon - 1, $year);
}

#================================================
# timeを日付に(YYYY-MM-DD)
#================================================
sub time_to_date {
	my $time2 = shift;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($time2);
	$year += 1900;
	$mon++;
	return sprintf("%04d-%02d-%02d",$year,$mon,$mday);
}

#================================================
# ロギング
#================================================
sub log_errors {
	my $text = shift;
	return if $text =~ /そのような名前/;

	my $url = "http://" . $ENV{'HTTP_HOST'} . $ENV{'REQUEST_URI'};
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time());
	$year += 1900;
	$mon++;

	my $time2 = sprintf("%04d-%02d-%02d %02d:%02d.%02d",$year,$mon,$mday,$hour,$min,$sec);
	open my $fh, ">> ./log/error.cgi";
	print $fh "$text $m{name} $time2\n$url\n\n";
	close $fh;
}

#================================================
# ﾌﾟﾚｲﾔｰ名リンク
#================================================
sub name_link {
	my $name = shift;
	if (&you_exists($name)) {
		my $id = unpack("H*", $name);
		my %p = &get_you_datas($id, 1);

		return qq|<a href="profile.cgi?id=$id&country=$p{country}" class="clickable_name">$name</a>|;
	}
	return $name;
}

#================================================
# ﾌﾟﾚｲﾔｰ名置換
#================================================
sub name_replace {
	$text = shift;
	
	my @names = &get_player_name_list;
	
	for my $name (@names) {
		my @pre_links = ();
		while ($text =~ /^(.*?)(<a\s.*?>.*?<\/a>)(.*)$/) {
			$text = $1 . '__a_dummy__' . $3;
			push @pre_links, $2;
		}
		my @pre_tags = ();
		while ($text =~ /^(.*?)(<.*?>)(.*)$/) {
			$text = $1 . "__tag__" . $3;
			push @pre_tags, $2;
		}
		my $text_new = '';
		my $q_name = quotemeta $name;
		while ($text =~ /^(.*?)$q_name(.*)$/) {
			$text_new .= $1 . &name_link($name);
			$text = $2;
		}
		$text = $text_new . $text;
		while ($text =~ /^(.*?)__tag__(.*)$/) {
			my $tag = shift @pre_tags;
			$text = $1 . $tag . $2;
		}
		while ($text =~ /^(.*?)__a_dummy__(.*)$/) {
			my $a_tag = shift @pre_links;
			$text = $1 . $a_tag . $2;
		}
	}
	return $text;
}

#================================================
# ﾌﾟﾚｲﾔｰリスト作成
#================================================
sub make_player_name_list {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		$name = pack 'H*', $id;
		push @lines, "$name\n";
	}
	closedir $dh;
	
	open my $fh, "> $logdir/player_name_list.cgi";
	eval { flock $fh, 2; };
	print $fh @lines;
	close $fh;
}

#================================================
# ﾌﾟﾚｲﾔｰリスト取得
#================================================
sub get_player_name_list {
#	my @names = ();
#	open my $fh, "< $logdir/player_name_list.cgi";
#	while (my $name = <$fh>) {
#		chomp($name);
#		if ($name) {
#			push @names, $name;
#		}
#	}
#	close $fh;
	my @names = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my $name = pack 'H*', $id;
		push @names, $name;
	}
	closedir $dh;
	
	return @names;
}

#================================================
# Twitterに投稿
# 第二引数が 1 で mes_and_world_news ライク
#================================================
sub send_twitter {
	return if $config_test;
	my $message = shift;
	my $flag = shift;

	my $pid = fork;
	die unless defined $pid;
	if ($pid) {
		return;
	}
	close STDOUT;
	close STDIN;
	close STDERR;

	$message = $w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16') ? "$c_mの名無しが$message" : "$c_mの$m{name}が$message" if $flag;
	my $ua = new LWP::UserAgent;
	$ua->agent("AgentName/0.1 " . $ua->agent);
	my %params = (
		pass => $twitter_pass,
		mes => $message
	);
	my $res = $ua->post('http://bj.ecb.mydns.jp/twitter/', [%params]);
	exit;
}

#================================================
# デバッグログ
#================================================
sub debug_log {
	my $message = shift;
	my $tag_disp = shift;
	if (!$config_test) {
		return;
	}
	
	use Data::Dumper;
	my $dmes = Dumper $message;
	$dmes =~ s/\n/<br>/g;
	$dmes =~ s/\s/&nbsp;/g;

	my $tag = unpack 'H*', $tag_disp;
	open my $fh, ">> $logdir/debug_log.cgi";
	print $fh "$m{name}<>$time<>$dmes<>$tag<>\n";
	close $fh;
}

#================================================
# スマートフォン or タブレット端末向けのCSS読み込み
#================================================
sub load_RWD {
	if ($is_smart) {
			print qq|<meta name="viewport" content="width=device-width">|;
			print qq|<link rel="stylesheet" media="screen and (max-width: 480px)" href="$htmldir/smart.css" />|;
			print qq|<link rel="stylesheet" media="screen and (min-width: 481px)" href="$htmldir/tablet.css" />|;
#			print qq|<meta name="viewport" content="width=device-width, maximum-scale=1.5, minimum-scale=0.5,user-scalable=yes,initial-scale=0.9" />|;
#			print qq|<link rel="stylesheet" media="screen and (min-width: 481px) and (max-width: 720px)" href="$htmldir/tablet.css?$jstime" />|;
	}
#	elsif (!$is_mobile) {
#		print qq|<meta name="viewport" content="width=device-width">|;
#	}
}

#================================================
# 専用アプリ向けのページスイッチャー
#================================================
sub show_page_switcher {
	print qq|<div valign="bottom" id="commands">|;

	print qq|<form method="$method" action="news.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="過去の栄光" class="button2s"></form>|;

	print qq|<form method="$method" action="bbs_public.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="掲示板" class="button2s"></form>|;

	print qq|<form method="$method" action="chat_public.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="交流広場" class="button2s"></form>|;

	print qq|<form method="$method" action="chat_horyu.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="改造案投票所" class="button2s"></form>|;

	print qq|<form method="$method" action="bbs_ad.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="宣伝言板" class="button2s"></form>|;

	print qq|<form method="$method" action="chat_prison.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="牢獄" class="button2s"></form>|;

	print qq|<form method="$method" action="bbs_country.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="作戦会議室" class="button2s"></form>|;

	print qq|<br class="cmd_br" />|;

	print qq|<form method="$method" action="bbs_union.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="同盟会議室" class="button2s"></form>|;

	print qq|<form method="$method" action="chat_casino.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="対人ｶｼﾞﾉ" class="button2s"></form>|;

	print qq|<form method="$method" action="bbs_daihyo.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="代表\評議会" class="button2s"></form>|;

	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<input type="submit" value="My ROOM" class="button2s"></form>|;

	print qq|<form method="$method" action="chat_admin.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="運営議論場" class="button2s"></form>|;

	print qq|</div>|;
}

# 手紙があるよﾌﾗｸﾞをたてる
sub set_letter_flag {
	my ($send_id, $type) = @_;
	my $len = 5 - 1; # letter.cgi の受信箱の数 - 1 配列の上限値 system.cgi でも定義 set_letter_flag
	my @letters = (); # 各受信箱の未読数
	my $line = '';

	if (-f "$userdir/$send_id/letter_flag.cgi") {
		open my $fh, "+< $userdir/$send_id/letter_flag.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
		eval { flock $fh, 2; };
		$line = <$fh>;
		@letters = split /<>/, $line;
		$letters[$type]++ if $type; # 専用の受信箱がなく、「すべて」の未読数を増やそうと 0 を指定したとき、「すべて」が2通増えてしまうのを避ける
		$letters[0]++; # 「すべて」を1通増やす
		$line = '';
		$line .= "$letters[$_]<>" for (0 .. $len);
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh $line;
		close $fh;
	}
	else {
		$letters[$_] = 0 for (0 .. $len); # calloc 0 初期化
		$letters[$type]++ if $type; # 専用の受信箱がなく、「すべて」の未読数を増やそうと 0 を指定したとき、「すべて」が2通増えてしまうのを避ける
		$letters[0]++; # 「すべて」を1通増やす
		$line .= "$letters[$_]<>" for (0 .. $len);
		open my $fh, "> $userdir/$send_id/letter_flag.cgi";
		print $fh $line;
		close $fh;
	}
}

1; # 削除不可
