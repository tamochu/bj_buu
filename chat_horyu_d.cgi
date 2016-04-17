#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# 改造案討論所詳細
#=================================================
&get_data;

$this_title  = "改造案投票所";
$this_list   = "$logdir/chat_horyu_list";
$this_dir    = "$logdir/kaizou";
$this_script = 'chat_horyu_d.cgi';
$headline_script = 'chat_horyu.cgi';

# 連続書き込み禁止時間(秒)
$bad_time    = 5;

# 最大ﾛｸﾞ保存件数
$max_log     = 50;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 2000;

# 催促時間
$remind_time = 3 * 24 * 3600;

# 催促無し
@no_remind = ($admin_name, $admin_sub_name);

# 君主以外の締め切り権限者
@deletable_member = ($admin_name, $admin_sub_name);

#=================================================
&run;
&footer;
exit;

#=================================================
sub run {
	&write_comment if ($in{mode} eq "write") && $in{comment};
	&good_comment if ($in{mode} eq "good");
	&bad_comment if ($in{mode} eq "bad");
	&no_comment if ($in{mode} eq "no");
	&close_line if ($in{mode} eq "close");

	print qq|<form method="$method" action="$headline_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	my $rows = $is_mobile ? 2 : 5;
	open my $fh2, "< $this_dir/$in{line}.cgi" or &error("$this_dir/$in{line}.cgi ﾌｧｲﾙが開けません");
	my $head_linet = <$fh2>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
	my @goods = split /,/, $bgood;
	my $goodn = @goods;
	my @bads = split /,/, $bbad;
	my $badn = @bads;
	if ($hidden) {
		$bgood = "匿名";
		$bbad = "匿名";
	}
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="line" value="$in{line}"><input type="hidden" name="target" value="$in{line}">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="書き込む" class="button_s"><input type="checkbox" name="tokumei" value="1">匿名<br>|;
	print qq|<input type="radio" name="mode" value="write" checked>書き込み|;
	if ($limit > $time + 7 * 24 * 3600) {
		print qq|<input type="radio" name="mode" value="close">議論を締め切る<br>|;
		print qq|<select name="limit">|;
		print qq|<option value="1">期限一日</option>|;
		print qq|<option value="3">期限三日</option>|;
		print qq|<option value="7" selected>期限七日</option>|;
		print qq|</select><br>|;
	}
	print qq|<input type="radio" name="mode" value="good">賛成<input type="radio" name="mode" value="bad">反対<input type="radio" name="mode" value="no">棄権<br>|;
	print qq|<hr size="1">|;
	if($limit > $time + 7 * 24 * 3600){
		print qq|議論段階<br>実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad<br>\n|;
	}elsif($limit > $time){
		print qq|この議題に書き込む<br>実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad<br>\n|;
	}else{
		if($goodn > $badn){
			print qq|<font size="5"><font color="blue">実装希望者 $goodn 人:$bgood</font> 実装反対者 $badn 人:$bbad この議題は期間を過ぎてます</font><br>\n|;
		}elsif($goodn < $badn){
			print qq|<font size="5">実装希望者 $goodn 人:$bgood <font color="red">実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
		}else{
			print qq|<font size="5"><font color="yellow">実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
		}
	}
	my $last_write_time;
	while (my $linet = <$fh2>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
		$bname .= "[$bshogo]" if ($bshogo && $bname ne '名無しさん@黒豚鯖');
		$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
		if ($hidden) {
			$bname = "匿名";
			$bicon = $default_icon;
			$bcountry = 0;
		}
		$bcomment = &comment_change($bcomment, 1);
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		$last_write_time = $btime;
	}
	close $fh2;
	print qq|</form>|;
	if ($last_write_time + $remind_time < $time) {
		&remind($in{line});
	}
}

#=================================================
# 書き込み処理
#=================================================
sub write_comment {
	&error('本文に何も書かれていません') if $in{comment} eq '';
	&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("ファイル名が異常です") if ($target =~ /[^0-9]/);
	&error("$target.cgiというファイルが存在しません") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, ">> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ﾌｧｲﾙが開けません");

	# ｵｰﾄﾘﾝｸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"

	my $wname = $in{tokumei} ? '名無しさん@黒豚鯖' : $m{name};
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	print $fh "$time<>$date<>$wname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	close $fh;
	return 1;
}

#=================================================
# 良評価
#=================================================
sub good_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("ファイル名が異常です") if ($target =~ /[^0-9]/);
	&error("$target.cgiというファイルが存在しません") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;
	my @goods = split /,/, $bgood;
	my @bads = split /,/, $bbad;
	$bgood = "";
	for my $gname (@goods){
		unless($gname eq $m{name}){
			if($bgood eq ""){
				$bgood .= "$gname";
			}else{
				$bgood .= ",$gname";
			}
		}
	}
	$bbad = "";
	for my $bname (@bads){
		unless($bname eq $m{name}){
			if($bbad eq ""){
				$bbad .= "$bname";
			}else{
				$bbad .= ",$bname";
			}
		}
	}
	if($bgood eq ""){
		$bgood .= "$m{name}";
	}else{
		$bgood .= ",$m{name}";
	}
	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# 悪評価
#=================================================
sub bad_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("ファイル名が異常です") if ($target =~ /[^0-9]/);
	&error("$target.cgiというファイルが存在しません") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;
	my @goods = split /,/, $bgood;
	my @bads = split /,/, $bbad;
	$bgood = "";
	for my $gname (@goods){
		unless($gname eq $m{name}){
			if($bgood eq ""){
				$bgood .= "$gname";
			}else{
				$bgood .= ",$gname";
			}
		}
	}
	$bbad = "";
	for my $bname (@bads){
		unless($bname eq $m{name}){
			if($bbad eq ""){
				$bbad .= "$bname";
			}else{
				$bbad .= ",$bname";
			}
		}
	}
	if($bbad eq ""){
		$bbad .= "$m{name}";
	}else{
		$bbad .= ",$m{name}";
	}
	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# 無評価
#=================================================
sub no_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("ファイル名が異常です") if ($target =~ /[^0-9]/);
	&error("$target.cgiというファイルが存在しません") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;
	my @goods = split /,/, $bgood;
	my @bads = split /,/, $bbad;
	$bgood = "";
	for my $gname (@goods){
		unless($gname eq $m{name}){
			if($bgood eq ""){
				$bgood .= "$gname";
			}else{
				$bgood .= ",$gname";
			}
		}
	}
	$bbad = "";
	for my $bname (@bads){
		unless($bname eq $m{name}){
			if($bbad eq ""){
				$bbad .= "$bname";
			}else{
				$bbad .= ",$bname";
			}
		}
	}
	
	push @lines, "$bgood<>$bbad<>$limit<>$hidden<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# 議論を締め切る
#=================================================
sub close_line {
	my $target = $in{target};
	my @voter = ();

	return 1 if ($target eq "no_write");
	return 1 if ($m{name} ne $cs{ceo}[$m{country}] && !&delete_check);
	&error("ファイル名が異常です") if ($target =~ /[^0-9]/);
	&error("$target.cgiというファイルが存在しません") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_line;
	
	my @goods = split /,/, $bgood;
	for my $name (@goods) {
		push @voter, $name;
	}
	my @bads = split /,/, $bbad;
	for my $name (@bads) {
		push @voter, $name;
	}
	
	$limit = $time + $in{limit} * 24 * 3600;
	push @lines, "<><>$limit<>$hidden<>\n";
	$line = <$fh>;
	my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $line;
	my ($lmin, $lhour, $lday, $lmon) = (localtime($limit))[1, 2, 3, 4];
	$lmon += 1;
	$vcomment = $bcomment . "の期限が$lmon月$lday日$lhour時$lmin分に設定されました。";
	$bcomment .= "<br>議論期限:$lmon月$lday日$lhour時$lmin分";
	push @lines, "$btime<>$bdate<>$bname<>$bcountry<>$bshogo<>$baddr<>$bcomment<>$bicon<>\n";
	
	for my $vname (@voter) {
		&system_letter($vname, $vcomment);
	}
	
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# 催促
#=================================================
sub remind {
	$target = shift;
	open my $fh2, "< $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ﾌｧｲﾙが開けません");
	my $head_linet = <$fh2>;
	my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
	my $head_linea = <$fh2>;
	my($atime,$adate,$aname,$acountry,$ashogo,$aaddr,$acomment,$aicon,$aid) = split /<>/, $head_linea;
	close $fh2;
	
	if ($limit < $time + 7 * 24 * 3600) {
		return;
	}
	
	$aname =~ s/さん提出<br>議題//g;
	
	for my $name (@no_remind) {
		if ($name eq $aname) {
			return;
		}
	}
	
	if (&system_letter($aname, "あなたの発議した議論<br>$acomment<br>が3日間進んでません。")) {
		open my $fh3, ">> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ﾌｧｲﾙが開けません");
		print $fh3 "$time<>$date<>システム<>0<><><>発議者に催促状を出しました<><>\n";
		close $fh3;
	}
}

sub system_letter {
	my $aname = shift;
	my $content = shift;

	my $send_id = unpack 'H*', $aname;
	local $this_file = "$userdir/$send_id/letter";
	if (-f "$this_file.cgi") {
		$in{comment} = $content;
		$mname = $m{name};
		$m{name} = 'システム';
		$mcountry = $m{country};
		$m{country} = 0;
		$micon = $m{icon};
		$m{icon} = '';
		$mshogo = $m{shogo};
		$m{shogo} = '';
		&send_letter($aname, 0);

		$in{comment} = "";
		$m{name} = $mname;
		$m{country} = $mcountry;
		$m{icon} = $micon;
		$m{shogo} = $mshogo;
		return 1;
	}
	
	return 0;
}

#=================================================
# 締切者チェック
#=================================================
sub delete_check {
	for my $name (@deletable_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}

