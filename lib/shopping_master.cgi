my $this_file = "$logdir/master.cgi";
#================================================
# “¹ê
#================================================
# ¢‘ã§ŒÀ:‚±‚Ì¢‘ãˆÈã‚©–¢–‚Å’íq‚©t ‚É•ª‚©‚ê‚é
my $need_sedai = 2;

my %exp_to_name = (
	"nou_c"=>"”_‹Æ",
	"sho_c"=>"¤‹Æ",
	"hei_c"=>"’¥•º",
	"gai_c"=>"ŠOŒğ",
	"gou_c"=>"‹­’D",
	"cho_c"=>"’³•ñ",
	"sen_c"=>"ô”]",
	"gik_c"=>"‹UŒv",
	"tei_c"=>"’ã@",
	"mat_c"=>"‘Ò•š",
	"tou_c"=>"“¢”°",
	"shu_c"=>"Cs",
	"win_c"=>"•Œ÷",
	"lose_c"=>"•s‹ü",
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
# —˜—pğŒ
#================================================
sub is_satisfy {
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚ ‚è‚Ü‚·‚©?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '‚±‚±‚Í“¹ê‚¾<br>';
		$mes .= '¡“ú‚Í‚È‚ñ‚Ì—p‚¾?<br>';
	}
	
	&menu('‚â‚ß‚é','t ‚ğ’T‚·','t “o˜^‚·‚é','”j–å‚·‚é','„‘E‚·‚é');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# t ‚ğ’T‚·
#================================================
sub tp_100 {
	if($m{sedai} > $need_sedai){
		$mes .= "’íq‚É‚È‚ê‚é‚Ì‚Í$need_sedai ¢‘ã‚Ü‚Å‚¾<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "‚·‚Å‚Ét ‚ª‚¢‚é‚¼<br>";
		&begin;
		return;
	}
	$layout = 1;
	$mes .= '‚±‚ê‚ªAt ‚ÌØ½Ä‚¾<br>';
	$mes .= 'K‚¢‚½‚¢n—û“x‚Ìt ‚ğ‘I‚×?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>¢‘ã</th><th>n—û“x</th><th>ƒƒbƒZ[ƒW</th><th>„‘EÒ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/¢‘ã$sedai/n—û“x$exp_to_name{$expert}/ƒƒbƒZ[ƒW$message/„‘EÒ$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$message</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="“ü–å‚·‚é" class="button1"></p></form>|;
	
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
	open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
		$mes .= '“o˜^ÒØ½Ä‚É“o˜^‚³‚ê‚Ä‚¢‚È‚¢l‚É‚Í“ü–å‚Å‚«‚Ü‚¹‚ñ<br>';
		&begin;
		return;
	}
	unless (-f "$userdir/$y_id/user.cgi") {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
		
		$mes .= "ƒAƒCƒc‚Í‚à‚¤Á‚µ‚½I";
		&begin;
		return;
	}
	my %you_datas = &get_you_datas($send_to);
	$mes .= "$exp_to_name{$exp_c}F$you_datas{$exp_c}<br>";
	
	if(-f "$userdir/$y_id/recommendation.cgi"){
		open my $fh, "< $userdir/$y_id/recommendation.cgi" or &error("„‘E‘Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		while (my $line = <$fh>){
			my($name, $message) = split /<>/, $line;
			$mes .= "$name‚³‚ñ‚Ì„‘EF<br>$message<br>";
		}
		close $fh;
	}
	
	$mes .= "‚±‚Ìl‚Ì’íq‚É‚È‚è‚Ü‚·‚©H<br>";
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0">‚â‚ß‚é<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>“ü–å<br>|;
	$mes .= qq|<input type="hidden" name="no" value="$cmd"><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="OK" class="button1"></p></form>|;	
	$m{tp} += 10;
}
# ------------------
sub tp_120 {
	return if &is_ng_cmd(1);
	
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($in{no} eq $no) {
			&regist_you_data($name, 'master', $m{name});
			$m{master} = $name;
			$m{master_c} = $expert;
			&write_world_news(qq|$m{name}‚ª$name‚É’íq“ü‚è‚µ‚Ü‚µ‚½|);
			&system_letter($name, "$m{name}‚ª’íq‚É‚È‚è‚Ü‚µ‚½")
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
# “o˜^
#================================================
sub tp_200 {
	$layout = 2;
	if($m{sedai} <= $need_sedai){
		$mes .= "‚à‚Á‚ÆCs‚µ‚Ä‚©‚ç‚±‚¢<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "‚·‚Å‚É’íq‚ª‚¢‚é<br>";
		&begin;
		return;
	}
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>n—û“x</th></tr>| unless $is_mobile;

	for my $exp_c (keys %exp_to_name) {
		next if($exp_to_needs{$exp_c} > $m{$exp_c});
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}</td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="message" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="“o˜^‚·‚é" class="button1"></p></form>|;

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
	open my $fh, "+< $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		unless ($name eq $m{name}) {
			push @lines, $line;
		}
	}
	if ($m{money} < $need_money) {
		close $fh;
		$mes .= "“o˜^‚·‚é‚¨‹à‚ª‘«‚è‚Ü‚¹‚ñ<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{sedai}<>$cmd<>$m{shogo}<>$cs{name}[$m{country}]<>$in{message}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "$m{name}‚ªt ‚Æ‚µ‚Ä“o˜^‚³‚ê‚Ü‚µ‚½<br>";
		$m{money} -= $need_money;
	}
	
	&begin;
}

#================================================
# ”j–å‚·‚é
#================================================
sub tp_300 {
	unless($m{master}){
		$mes .= "’íq‚ª‚¢‚Ü‚¹‚ñ<br>";
		&begin;
		return;
	}
	$mes .= "–{“–‚É’íq‚ğ”j–å‚µ‚Ü‚·‚©H<br>";
	
	&menu('‚â‚ß‚é','”j–å‚·‚é');
	$m{tp} += 10;
}

sub tp_310 {
	return if &is_ng_cmd(1);
	&regist_you_data($m{master}, 'master', '');
	&regist_you_data($m{master}, 'master_c', '');
	$m{master} = '';
	
	$mes .= "’íq‚ğ”j–å‚µ‚Ü‚µ‚½<br>";
	&begin;
}

#================================================
# „‘E‚·‚é
#================================================
sub tp_400 {
	$layout = 1;
	$mes .= '‚±‚ê‚ªAt ‚ÌØ½Ä‚¾<br>';
	$mes .= '„‘E‚·‚ét ‚ğ‘I‚×?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br>|;
	$mes .= qq|<table class="table1"><tr><th>–¼‘O</th><th>$e2j{name}</th><th>“o˜^“ú</th><th>¢‘ã</th><th>n—û“x</th><th>„‘EÒ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/“o˜^“ú$mdate/¢‘ã$sedai/n—û“x$exp_to_name{$expert}/„‘EÒ$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="„‘E‚·‚é" class="button1"></p></form>|;
	
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
	open my $fh, "+< $this_file" or &error("$this_file ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			$y_id = unpack 'H*', $send_to;
			if($in{comment}){
				push @lines, "$no<>$mdate<>$name<>$country<>$sedai<>$expert<>$shogo<>$recommendation,$m{name}<>$message<>\n";
				open my $fh2, ">> $userdir/$y_id/recommendation.cgi" or &error("„‘E‘Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
			open my $fh2, "< $userdir/$y_id/recommendation.cgi" or &error("„‘E‘Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
			while (my $line = <$fh2>){
				my($name, $message) = split /<>/, $line;
				$mes .= "$name‚³‚ñ‚Ì„‘EF<br>$message<br>";
			}
			close $fh2;
		}
	}else{
		$mes .= '“o˜^ÒØ½Ä‚É“o˜^‚³‚ê‚Ä‚¢‚È‚¢l‚É‚Í„‘E‚Å‚«‚Ü‚¹‚ñ<br>';
	}

	&begin;
}

sub system_letter {
	my $aname = shift;
	my $content = shift;

	my $send_id = unpack 'H*', $aname;
	local $this_file = "$userdir/$send_id/letter";
	if (-f "$this_file.cgi") {
		$in{comment} = $content;
		$mname = $m{name};
		$m{name} = 'ƒVƒXƒeƒ€';
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

1; # íœ•s‰Â
