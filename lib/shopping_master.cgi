my $this_file = "$logdir/master.cgi";
#================================================
# 道場
#================================================
# 世代制限:この世代以上か未満で弟子か師匠に分かれる
my $need_sedai = 2;

my %exp_to_name = (
	"nou_c"=>"農業",
	"sho_c"=>"商業",
	"hei_c"=>"徴兵",
	"gai_c"=>"外交",
	"gou_c"=>"強奪",
	"cho_c"=>"諜報",
	"sen_c"=>"洗脳",
	"gik_c"=>"偽計",
	"tei_c"=>"偵察",
	"mat_c"=>"待伏",
	"tou_c"=>"討伐",
	"shu_c"=>"修行",
	"win_c"=>"武功",
	"lose_c"=>"不屈",
);

my %exp_to_needs = (
	"nou_c"=>5000,
	"sho_c"=>5000,
	"hei_c"=>5000,
	"gai_c"=>2000,
	"gou_c"=>5000,
	"cho_c"=>5000,
	"sen_c"=>5000,
	"gik_c"=>5000,
	"tei_c"=>5000,
	"mat_c"=>5000,
	"tou_c"=>20000,
	"shu_c"=>20000,
	"win_c"=>2000,
	"lose_c"=>500,
);

my $need_money = 0;
#================================================
# 利用条件
#================================================
sub is_satisfy {
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ここは道場だ<br>';
		$mes .= '今日はなんの用だ?<br>';
	}
	
	&menu('やめる','師匠を探す','師匠登録する','破門する','推薦する');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# 師匠を探す
#================================================
sub tp_100 {
	if($m{sedai} > $need_sedai){
		$mes .= "弟子になれるのは$need_sedai 世代までだ<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "すでに師匠がいるぞ<br>";
		&begin;
		return;
	}
	$layout = 1;
	$mes .= 'これが、師匠のﾘｽﾄだ<br>';
	$mes .= '習いたい熟練度の師匠を選べ?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>世代</th><th>熟練度</th><th>メッセージ</th><th>推薦者<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/世代$sedai/熟練度$exp_to_name{$expert}/メッセージ$message/推薦者$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$message</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="入門する" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
# ------------------
sub tp_110 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	my $exp_c;
	open my $fh, "< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			$exp_c = $expert;
			last;
		}
	}
	close $fh;

	my $y_id = unpack 'H*', $send_to;
	unless ($send_to) {
		$mes .= '登録者ﾘｽﾄに登録されていない人には入門できません<br>';
		&begin;
		return;
	}
	unless (-f "$userdir/$y_id/user.cgi") {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file が開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
			unless ($cmd eq $no) {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		$mes .= "アイツはもう消した！";
		&begin;
		return;
	}
	my %you_datas = &get_you_datas($send_to);
	$mes .= "$exp_to_name{$exp_c}：$you_datas{$exp_c}<br>";
	
	if(-f "$userdir/$y_id/recommendation.cgi"){
		open my $fh, "< $userdir/$y_id/recommendation.cgi" or &error("推薦書ﾌｧｲﾙが開けません");
		while (my $line = <$fh>){
			my($name, $message) = split /<>/, $line;
			$mes .= "$nameさんの推薦：<br>$message<br>";
		}
		close $fh;
	}
	
	$mes .= "この人の弟子になりますか？<br>";
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0">やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>入門<br>|;
	$mes .= qq|<input type="hidden" name="no" value="$cmd"><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="OK" class="button1"></p></form>|;	
	$m{tp} += 10;
}
# ------------------
sub tp_120 {
	return if &is_ng_cmd(1);
	
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file が開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($in{no} eq $no) {
			&regist_you_data($name, 'master', $m{name});
			$m{master} = $name;
			$m{master_c} = $expert;
			&write_world_news(qq|$m{name}が$nameに弟子入りしました|);
			&system_letter($name, "$m{name}が弟子になりました")
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#================================================
# 登録
#================================================
sub tp_200 {
	$layout = 2;
	if($m{sedai} <= $need_sedai){
		$mes .= "もっと修行してからこい<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "すでに弟子がいる<br>";
		&begin;
		return;
	}
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>熟練度</th></tr>| unless $is_mobile;

	for my $exp_c (keys %exp_to_name) {
		next if($exp_to_needs{$exp_c} > $m{$exp_c});
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}</td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="message" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="登録する" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_210 {
	unless ($cmd){
		&begin;
		return;
	}
	my $exp_find = 0;
	for my $exp_c (keys %exp_to_name){
		if($exp_c eq $cmd){
			$exp_find= 1;
		}
	}
	unless ($exp_find){
		&begin;
		return;
	}
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		unless ($name eq $m{name}) {
			push @lines, $line;
		}
	}
	if ($m{money} < $need_money) {
		close $fh;
		$mes .= "登録するお金が足りません<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{sedai}<>$cmd<>$m{shogo}<>$cs{name}[$m{country}]<>$in{message}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "$m{name}が師匠として登録されました<br>";
		$m{money} -= $need_money;
	}
	
	&begin;
}

#================================================
# 破門する
#================================================
sub tp_300 {
	unless($m{master}){
		$mes .= "弟子がいません<br>";
		&begin;
		return;
	}
	$mes .= "本当に弟子を破門しますか？<br>";
	
	&menu('やめる','破門する');
	$m{tp} += 10;
}

sub tp_310 {
	return if &is_ng_cmd(1);
	&regist_you_data($m{master}, 'master', '');
	&regist_you_data($m{master}, 'master_c', '');
	$m{master} = '';
	
	$mes .= "弟子を破門しました<br>";
	&begin;
}

#================================================
# 推薦する
#================================================
sub tp_400 {
	$layout = 1;
	$mes .= 'これが、師匠のﾘｽﾄだ<br>';
	$mes .= '推薦する師匠を選べ?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>名前</th><th>$e2j{name}</th><th>登録日</th><th>世代</th><th>熟練度</th><th>推薦者<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/登録日$mdate/世代$sedai/熟練度$exp_to_name{$expert}/推薦者$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="推薦する" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_410 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	my $y_id;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file が開けません");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			$y_id = unpack 'H*', $send_to;
			if($in{comment}){
				push @lines, "$no<>$mdate<>$name<>$country<>$sedai<>$expert<>$shogo<>$recommendation,$m{name}<>$message<>\n";
				open my $fh2, ">> $userdir/$y_id/recommendation.cgi" or &error("推薦書ﾌｧｲﾙが開けません");
				print $fh2 "$m{name}<>$in{comment}<>\n";
				close $fh2;
			}else{
				push @lines, "$no<>$mdate<>$name<>$country<>$sedai<>$expert<>$shogo<>$recommendation<>$message<>\n";
			}
		}else{
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	if ($send_to) {
		if(-f "$userdir/$y_id/recommendation.cgi"){
			open my $fh2, "< $userdir/$y_id/recommendation.cgi" or &error("推薦書ﾌｧｲﾙが開けません");
			while (my $line = <$fh2>){
				my($name, $message) = split /<>/, $line;
				$mes .= "$nameさんの推薦：<br>$message<br>";
			}
			close $fh2;
		}
	}else{
		$mes .= '登録者ﾘｽﾄに登録されていない人には推薦できません<br>';
	}

	&begin;
}

sub system_letter {
	my $aname = shift;
	my $content = shift;

	my $send_id = unpack 'H*', $aname;
	my $letter_file = "$userdir/$send_id/letter";
	if (-f "$letter_file.cgi") {
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

1; # 削除不可
