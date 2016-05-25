require './lib/_comment_tag.cgi';
require 'lib/_write_tag.cgi';
#================================================
# BBS2 Arranged by Oiiuii
#================================================

# ˜A‘±‘‚«‚İ‹Ö~ŠÔ(•b)
$bad_time    = 10;

# Å‘åÛ¸Ş•Û‘¶Œ”
$max_log     = 50;

# Å‘åÛ¸Ş•Û‘¶ŠúŠÔ
$max_time     = 5 * 24 * 3600;

# Å‘åºÒİÄ”(”¼Šp)
$max_comment = 400;
$rmax_comment = 30;

# ÒİÊŞ°‚É•\¦‚³‚ê‚éŠÔ(•b)
$limit_member_time = 60 * 4;

my @menus = ([999, '‚»‚Ì‘¼'], [1000, '‹à'], @weas, @eggs, @pets);


#================================================
sub run {
	if ($in{mode} eq "write" && $in{ad_type} ne '2' && ($in{comment} || $in{is_del} eq '1' || ($in{want} ne '0' || $in{pay} ne '0'))) {
		&write_comment;
	}
	if ($in{mode} eq "write_res") {
		if($in{is_letter}){
			$in{comment} .= "<hr>yé“`Œ¾”Â‚Ö‚ÌƒŒƒXz";
			&send_letter($in{res_name}, 1);
		}else {
			&write_res;
		}
	}
	
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;
	
	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<br><textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="‘‚«‚Ş" class="button_s">|;
	print qq|<input type="checkbox" name="is_del" value="1">L‚ğæ‚è‰º‚°‚é<br>|;
#	print qq|<input type="radio" name="ad_type" value="0">’Êí<br>|;
	print qq|<input type="radio" name="ad_type" value="1" checked>L<br>|;
	print qq|<input type="radio" name="ad_type" value="2">ŒŸõ<br>|;
	print qq|‹<select name="want" class="menu1">|;
	for my $i (0 .. $#menus) {
		next if $menus[$i][0] eq '0';
		print qq|<option value="$i">$menus[$i][1]</option>|;
	}
	print qq|</select>|;
	print qq|o<select name="pay" class="menu1">|;
	for my $i (0 .. $#menus) {
		next if $menus[$i][0] eq '0';
		print qq|<option value="$i">$menus[$i][1]</option>|;
	}
	print qq|</select></form><br>|;

	print qq|<font size="2">$member_cl:$member</font><hr>|;

	my @lines;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	@lines = <$fh>;
	while (my $line = shift @lines) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bwant,$bpay,$btype,$bres1,$bres2,$bres3,$bres4,$bres5) = split /<>/, $line;
		if($in{ad_type} eq '2'){
				next if $bwant ne $in{want} && $bpay ne $in{pay};
		}
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bcomment = &comment_change($bcomment, 0);
		my $reses = "----<br>";
		$reses .= "$bres1<br>" if $bres1;
		$reses .= "$bres2<br>" if $bres2;
		$reses .= "$bres3<br>" if $bres3;
		$reses .= "$bres4<br>" if $bres4;
		$reses .= "$bres5<br>" if $bres5;
		if($in{mode} eq "res" && $in{res_name} eq $bname){
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write_res"><input type="hidden" name="res_name" value="$bname">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<br><textarea name="comment" cols="30" rows="1" wrap="soft" class="textarea1"></textarea><br>|;
			print qq|<input type="checkbox" name="is_letter" value="1">è†‚Å‘—‚é<br>|;
			print qq|<input type="submit" value="ƒŒƒX" class="button_s">|;
			print qq|</form><br>|;
		}else{
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="res"><input type="hidden" name="res_name" value="$bname">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="ƒŒƒX" class="button_s"></form><br>|;
		}
		$bname = &name_link($bname);
		$bname .= "[$bshogo]" if $bshogo;
		if ($is_mobile) {
			print qq|<div>$bicon<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font>$reses</div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br>$reses</td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}

sub write_res{
	&error('–{•¶‚É‰½‚à‘‚©‚ê‚Ä‚¢‚Ü‚¹‚ñ') if $in{comment} eq '';
	&error("–{•¶‚ª’·‚·‚¬‚Ü‚·(”¼Šp$rmax_comment•¶š‚Ü‚Å)") if length $in{comment} > $rmax_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	
	# µ°ÄØİ¸
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"

	while (my $line = <$fh>) {
		my($otime,$odate,$oname,$ocountry,$oshogo,$oaddr,$ocomment,$oicon,$owant,$opay,$otype,$ores1,$ores2,$ores3,$ores4,$ores5) = split /<>/, $line;
		if ($oname eq $in{res_name}){
			push @lines, "$otime<>$odate<>$oname<>$ocountry<>$oshogo<>$oaddr<>$ocomment<>$oicon<>$owant<>$opay<>$otype<>$in{comment}($m{name})<>$ores1<>$ores2<>$ores3<>$ores4<>\n";
		}else{
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

sub write_comment {
	&error('–{•¶‚É‰½‚à‘‚©‚ê‚Ä‚¢‚Ü‚¹‚ñ') if $in{comment} eq '' && $in{is_del} ne '1' && ($in{want} eq '0' && $in{pay} eq '0');
	&error("–{•¶‚ª’·‚·‚¬‚Ü‚·(”¼Šp$max_comment•¶š‚Ü‚Å)") if length $in{comment} > $max_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	if($in{want} ne '0'){
		     $in{comment} = "‹)$menus[$in{want}][1]<br>" . $in{comment};
	}
	if($in{pay} ne '0'){
		     $in{comment} = "o)$menus[$in{pay}][1]<br>" . $in{comment};
	}
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment,$htype) = (split /<>/, $head_line)[0,2,6,10];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bwant,$bpay,$btype) = split /<>/, $line;
	return 0 if $in{comment} eq $hcomment;
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("˜A‘±“Še‚Í‹Ö~‚µ‚Ä‚¢‚Ü‚·B<br>‚µ‚Î‚ç‚­‘Ò‚Á‚Ä‚©‚ç‘‚«‚ñ‚Å‚­‚¾‚³‚¢");
	}
	push @lines, $head_line unless $hname eq $m{name} && $htype eq '1' && ($in{ad_type} eq '1' || $in{is_del} eq '1');

	while (my $line = <$fh>) {
		my ($otime,$oname,$ocomment,$otype) = (split /<>/, $line)[0,2,6,10];
		next if $oname eq $m{name} && $otype eq '1' && ($in{ad_type} eq '1' || $in{is_del} eq '1');
		if ($otype == 0){
		   next if @lines >= $max_log - 1;
		}else {
		      next if $otime + $max_time < $time;
		}
		push @lines, $line;
	}
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>$in{want}<>$in{pay}<>1<>ˆÈ~‚ÌƒŒƒX‚Í‚ ‚è‚Ü‚¹‚ñ<><><><><>\n" unless $in{is_del} eq '1';

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ÒİÊŞ°Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # “¯‚¶l‚È‚çŸ
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

1; # íœ•s‰Â
