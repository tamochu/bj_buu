#================================================
# ｶｼﾞﾉ共用関数
#================================================

use constant GAME_RESET => 1; # ｹﾞｰﾑの更新が止まっている
use constant LEAVE_PLAYER => 2; # 参加者が非ｱｸﾃｨﾌﾞになっている

$limit_think_time = 60 * 10; # 10分放置でﾌﾟﾚｲﾔｰ除外
$limit_game_time = 60 * 20; # 30分放置でｹﾞｰﾑﾘｾｯﾄ

#================================================
# 対人ｶｼﾞﾉの基本的なﾒｲﾝ画面
#================================================
sub _default_run {
#	my $_default = $_; # ﾁｬｯﾄ部分の有無
	$in{comment} = &{$in{mode}} if $in{mode} && $in{mode} ne 'write'; # 各ｺﾏﾝﾄﾞに対応する関数へのﾛｰﾀﾞｰ
	&write_comment if $in{comment};

	my @datas = ();

	my($member_c, $member, @datas) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}

	print qq|<h2>$this_title</h2>|;
	print qq|$mes|;
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;
	unless ($is_mobile) {
		print qq|自動ﾘﾛｰﾄﾞ<select name="reload_time" class="select1"><option value="0">なし|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]秒| : qq|<option value="$i">$reload_times[$i]秒|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c人:$member</font><br>|;

	&show_game_info(@datas);

	print qq|<hr>|;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

#================================================
# ｺｲﾝの増減
#================================================
sub coin_move{
	my ($m_coin, $name, $no_system_comment) = @_;
	my $ret_v;
	
	my $player_id = unpack 'H*', $name;

	# 存在しない場合はスキップ
	unless (-f "$userdir/$player_id/user.cgi") {
		return $ret_v;
	}
	if($name eq $m{name}){
		if ($m{coin} + $m_coin < 0){
			$ret_v = -1 * $m{coin};
		}else {
			$ret_v = $m_coin;
		}
		
		$m{coin} += $ret_v;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $m_coin;

		if ($temp < 0){
			$temp = 0;
			$ret_v = -1 * $datas1{coin};
		} else {
			if ($temp > 2500000) {
				$temp = 2500000;
			}
			$ret_v = $m_coin;
		}
		&regist_you_data($name,'coin',$temp);
	}

	unless ($no_system_comment) {
		if($ret_v > 0){
			&system_comment("$name は $ret_v ｺｲﾝ得ました");
		}else{
			my $temp = -1 * $ret_v;
			&system_comment("$name は $temp ｺｲﾝ払いました");
		}
	}
	
	if ($m_coin < $ret_v) {
		my $diff = ($ret_v - $m_coin) * 10;
			
		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_fileが開けません");
			eval { flock $fh, 2; };
			
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff;
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	
	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# 存在しない場合はスキップ
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name は $mes_as として $prize を獲得しました");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name が $mes_news</font>|);
	}
}

sub system_comment{
	my $s_mes = shift;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };

	# ｵｰﾄﾘﾝｸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>システムメッセージ<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# 対人ｶｼﾞﾉ関係の変数を初期化
#================================================
sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

#================================================
# 対人ｶｼﾞﾉ関係の変数を初期化(複数ﾕｰｻﾞｰ)
#================================================
sub you_lot_c_reset {
	my @names = @_;

	my @data = (
		['c_turn', 0],
		['c_value', 0],
		['c_stock', 0],
	);

	for $name (@names) {
		if ($name eq $m{name}) {
			$m{c_turn} = $m{c_value} = $m{c_stock} = 0;
			&write_user;
		}
		else {
			&regist_you_array($datas{name}, @data);
		}
	}
}

1;#削除不可
