#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/contest.cgi";
#================================================
# ºİÃ½Ä Created by Merino
#================================================
# past ‰ß‹, prepare ´İÄØ°ó•t(Ÿ‚ÌºİÃ½Ä), entry Œ»ºİÃ½Ä

# “a“°“ü‚è@’Ç‰Áíœ•À‚×‘Ö‚¦‰Â”\
my @legends = (
#	['À²ÄÙ',		'Û¸ŞÌ§²Ù–¼','í—Ş'	],
	['‹†‹É‚Ì”ü',	'picture',	'img',	],
	['Œ¶‚Ì–¼ì',	'book',		'html'	],
);
# ‚PˆÊ‚É“Š•[‚µ‚½l‚É‘—‚ç‚ê‚éÀÏºŞ
my @egg_nos = (1..34,42..50);


#================================================
&decode;
$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @contests;
my $this_dir = "$logdir/contest/$contests[$in{no}][1]";

&header;
&header_contest;

if    ($in{mode} eq 'past')   { &past; }
elsif ($in{mode} eq 'legend') { &legend; }
elsif ($in{mode} eq 'vote' && $in{vote} && $in{id} && $in{pass}) { &vote; &top; }
else { &top; }

&footer;
exit;

#================================================
# ºİÃ½Ä—pheader
#================================================
sub header_contest {
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	}
	
	for my $i (0 .. $#contests) {
		print $in{mode} ne 'legend' && $i eq $in{no} ? qq|$contests[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$contests[$i][0]</a> / |;
	}

	for my $i (0 .. $#legends) {
		print $in{mode} eq 'legend' && $i eq $in{no} ? qq|$legends[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i&mode=legend">$legends[$i][0]</a> / |;
	}
	print qq|<hr>|;
}


#================================================
# “a“°“ü‚è
#================================================
sub legend {
	print qq|<h1>$legends[$in{no}][0]</h1><hr>|;
	open my $fh, "< $logdir/legend/$legends[$in{no}][1].cgi" or &error("$logdir/legend/$legends[$in{no}][1].cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($round, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
		print $legends[$in{no}][2] eq 'img'  ? qq|<img src="$logdir/legend/$legends[$in{no}][1]/$file_name" style="border: 5px ridge #FC3; vertical-align:middle;"> ‘æ$round‰ñ$contests[$in{no}][0]—DGì•iw$file_titlexì:$name <font size="1">($ldate)</font><hr>|
			: $legends[$in{no}][2] eq 'html' ? qq|‘æ$round‰ñ$contests[$in{no}][0]—DGì•i w<a href="$logdir/legend/$legends[$in{no}][1]/$file_name" target="_blank">$file_title</a>xì:$name <font size="1">($ldate)</font><hr>|
			:                                  qq|‘æ$round‰ñ$contests[$in{no}][0]—DGì•i w$file_titlexì:$name <font size="1">($ldate)</font><hr>|
			;
	}
	close $fh;
}


#================================================
# ‘O‰ñ‚ÌºİÃ½ÄŒ‹‰Ê
#================================================
sub past {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="Œ»İ‚ÌºİÃ½Ä" class="button1"></form>|;

	if (-s "$this_dir/past.cgi") {
		open my $fh, "< $this_dir/past.cgi" or &error("$this_dir/past.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		my $head_line = <$fh>;
		my($etime, $round) = split /<>/, $head_line;
		print qq|<h1>‘æ$round‰ñ$contests[$in{no}][0] Œ‹‰Ê</h1><hr>|;
		while (my $line = <$fh>) {
			my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
			
			print $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> w$file_titlex ì:$name  <b>$vote</b>•[<br>$comment<hr>|
				: $contests[$in{no}][2] eq 'html' ? qq|w<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>x ì:$name  <b>$vote</b>•[<br>$comment<hr>|
				:                                   qq|w$file_titlex ì:$name  <b>$vote</b>•[<br>$comment<hr>|;
				;
		}
		close $fh;
	}
	else {
		print qq|<p>‘O‰ñ‚ÌºİÃ½Ä‚ÍŠJÃ‚³‚ê‚Ä‚¢‚Ü‚¹‚ñ</p>|;
	}
}


#================================================
# top
#================================================
sub top {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="mode" value="past"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="‘O‰ñ‚ÌŒ‹‰Ê" class="button1"></form>|;
	
	my $sub_mes = '<hr>';
	open my $fh, "< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		$sub_mes .= qq|<input type="radio" name="vote" value="$no">| if $in{id} && $in{pass};
		$sub_mes .= $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> No.$now$file_titlex<hr>|
				  : $contests[$in{no}][2] eq 'html' ? qq|No.$now<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>x<hr>|
				  :                                   qq|No.$now$file_titlex<hr>|;
				  ;
		++$count;
	}
	close $fh;
	
	my($min,$hour,$day,$month) = (localtime($etime))[1..4];
	++$month;
	
	# ‰ß‹ºİÃ½Äíœ¨Œ»ºİÃ½Ä‚ğ‰ß‹ºİÃ½Ä¨ŸºİÃ½Ä‚ğŒ»ºİÃ½Ä‚É‚·‚éˆ—
	if ($time > $etime) {
		++$round;
		print qq|<h1>‘æ$round‰ñ$contests[$in{no}][0]</h1>|;
		print qq|<p>cWŒvˆ—’†c</p>|;

		if ($count > 0) {
			&_send_goods_to_creaters if -s "$this_dir/past.cgi";
			&_result_contest;
		}
		&_start_contest;
	}
	elsif ($min_entry_contest > $count) {
		++$round;
		print qq|<h1>‘æ$round‰ñ$contests[$in{no}][0]</h1>|;
		print qq|<p>y“Š•[I—¹“úEŸ‰ñºİÃ½Ä $monthŒ$day“ú$hour$min•ªz</p>|;
		print qq|<p>“o˜^Ò‚ªW‚Ü‚Á‚Ä‚¢‚È‚¢‚½‚ßŠJÃ‰„Šú’†‚Å‚·</p>|;
	}
	elsif ($in{id} && $in{pass}) {
		print qq|<h1>‘æ$round‰ñ$contests[$in{no}][0]</h1>|;
		print qq|<p>y“Š•[I—¹“úEŸ‰ñºİÃ½Ä $monthŒ$day“ú$hour$min•ªz</p>|;
		print qq|<p><font color="#FF9999"><b>$mes</b></font></p>| if $mes;
		print qq|<p>“Š•[‚Íˆêlˆê•[‚Ü‚Å</p>|;
		print qq|<form method="$method" action="contest.cgi">|;
		print qq|<input type="radio" name="vote" value="0" checked>‚â‚ß‚é$sub_mes|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="mode" value="vote"><input type="hidden" name="no" value="$in{no}">|;
		print qq|ºÒİÄ[‘SŠp30(”¼Šp60)•¶š‚Ü‚Å]:<br><input type="text" name="vote_comment" class="text_box_b"><br>|;
		print qq|<input type="submit" value="“Š•[" class="button_s"></form>|;
	}
	else {
		print qq|<h1>‘æ$round‰ñ$contests[$in{no}][0]</h1>|;
		print qq|<p>y“Š•[I—¹“úEŸ‰ñºİÃ½Ä $monthŒ$day“ú$hour$min•ªz</p>|;
		print $sub_mes;
	}
}
# ------------------
# ‰ß‹‚ÌºİÃ½Äì•i‚ğìÒ‚É•Ô•i‚µÌ§²Ù¥Ì«ÙÀŞíœ
sub _send_goods_to_creaters {
	my $count = 0;
	open my $fh, "+< $this_dir/past.cgi" or &error("$this_dir/past.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		++$count;
		next unless -f "$this_dir/$round/$file_name";
		
		my $y_id = unpack 'H*', $name;
		if (-d "$userdir/$y_id/picture") {
			# ì•i‚ğìÒ‚Ö•ÔŠÒ
			rename "$this_dir/$round/$file_name", "$userdir/$y_id/$contests[$in{no}][1]/$file_name" or &error("Cannot rename $this_dir/$round/$file_name to $userdir/$y_id/$contests[$in{no}][1]/$file_name");

			# ì•i‚ª‚ ‚é‚æÌ×¸Ş‚ğ‚½‚Ä‚é
			open my $fh5, "> $userdir/$y_id/goods_flag.cgi";
			close $fh5;
		}
		else {
			unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_nameÌ§²Ù‚ğíœ‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ");
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;
	
	opendir my $dh, "$this_dir/$round" or &error("$this_dir/$roundÃŞ¨Ú¸ÄØ‚ğŠJ‚­‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_nameÌ§²Ù‚ğíœ‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ");
	}
	closedir $dh;
	rmdir "$this_dir/$round" or &error("$this_dir/$roundÃŞ¨Ú¸ÄØ‚ğíœ‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ");
}
# ------------------
# Œ‹‰Ê‚ğWŒv‚µ‚Ä‰ß‹ºİÃ½Ä‚ÉØÈ°Ñ
sub _result_contest {
	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	
	# ‘½‚¢‡‚Ésort
	@lines = map { $_->[0] } sort { $b->[5] <=> $a->[5] } map { [$_, split/<>/] } @lines;
	
	unshift @lines, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	rename "$this_dir/entry.cgi", "$this_dir/past.cgi" or &error("Cannot rename $this_dir/entry.cgi to $this_dir/past.cgi");
	
	# ì•i‚ğºËß°‚µ‚Ä“a“°“ü‚è
	&__copy_goods_to_legend($head_line, $lines[1]) if @lines > $min_entry_contest;
	
	&__send_prize(@lines);
}


# ãˆÊ‚ÉÜ•i‘—‚é
sub __send_prize {
	my @lines = @_;

	require 'config_game.cgi'; # regist_you_data()‚Ì‚½‚ß

	my $head_line = shift @lines;
	my($etime, $round) = split /<>/, $head_line;
	
	my $count = 1;
	for my $line (@lines) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		# 1ˆÊ‚È‚çÌ†
		if ($count eq '1') {
			&regist_you_data($name, 'shogo', $contests[$in{no}][3]);
			
			for my $v_name (split /,/, $vote_names) {
				next unless $v_name;
				my $egg_no = $egg_nos[int(rand(@egg_nos))];
				&send_item($v_name, 2, $egg_no, 0, 0, 1);
			}
			&write_send_news("‘æ$round‰ñ$contests[$in{no}][0]‘æ$countˆÊ‚Ì$name‚É“Š•[‚µ‚½l‚ÉÀÏºŞ‚ª‘—‚ç‚ê‚Ü‚µ‚½");
		}
		
		&send_item($name, 2, $c_prizes[$count-1][0], 0, 0, 1);
		&send_money($name, $contests[$in{no}][0], $c_prizes[$count-1][1]);
		&write_send_news("<b>‘æ$round‰ñ$contests[$in{no}][0]‘æ$countˆÊ‚Ì$name‚É$c_prizes[$count-1][1] G‚Æ $eggs[ $c_prizes[$count-1][0] ][1]‚ª‘—‚ç‚ê‚Ü‚µ‚½</b>", 1, $name);

		last if ++$count > @c_prizes;
	}
}


sub __copy_goods_to_legend {
	my($head_line, $line) = @_;
	my($etime, $round) = split /<>/, $head_line;
	my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
	
	# ‚·‚Å‚É“¯‚¶Ì§²Ù–¼‚ª‘¶İ‚µ‚Ä‚¢‚½‚ç“a“°“ü‚è‚Í‚µ‚È‚¢
	return if -f "$logdir/legend/$contests[$in{no}][1]/$file_name";
	
	# ì•i‚ğ“a“°“ü‚èÌ«ÙÀŞ‚ÉºËß°
	open my $in, "< $this_dir/$round/$file_name";
	binmode $in;
	my @datas = <$in>;
	close $in;

	open my $out, "> $logdir/legend/$contests[$in{no}][1]/$file_name";
	binmode $out;
	print $out @datas;
	close $out;
	
	# “a“°“ü‚èÌ§²Ù‚ÉìÒ‚âÌ§²Ù–¼‚È‚Ç‹L“ü
	my @lines = ();
	open my $fh, "+< $logdir/legend/$contests[$in{no}][1].cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if (@lines > $max_log - 1) {
			my($dround, $dname, $dfile_title, $dfile_name) = split /<>/, $line;
			unlink "$logdir/legend/$contests[$in{no}][1]/$dfile_name" if -f "$logdir/legend/$contests[$in{no}][1]/$dfile_name";
		}
		else {
			push @lines, $line;
		}
	}
	unshift @lines, "$round<>$name<>$file_title<>$file_name<>$date<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# ŸºİÃ½Ä‚ğŒ»ºİÃ½Ä‚ÉØÈ°Ñ
sub _start_contest {
	my $end_time = $time + 24 * 60 * 60 * $contest_cycle_day;

	my @lines = ();
	open my $fh, "+< $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	push @lines, "$end_time<>$round<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	# ´İÄØ°”‚ªÅ’á´İÄØ°”‚ğ’´‚¦‚½ê‡‚ÍŠJÃ
	if ( @lines > $min_entry_contest ) {
		rename "$this_dir/prepare.cgi", "$this_dir/entry.cgi" or &error("Cannot rename $this_dir/prepare.cgi to $this_dir/entry.cgi");
		
		# “Š•[/–¢“Š•[¯•ÊÌ§²Ù‚ğ‰Šú‰»
		open my $fh3, "> $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgiÌ§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
		print $fh3 ",";
		close $fh3;
		
		# ŠJÃéŒ¾
		require 'config_game.cgi'; # write_send_news()‚Ì‚½‚ß
		my($min,$hour,$day,$month) = (localtime($end_time))[1..4];
		++$month;
		&write_world_news("<i>‘æ$round‰ñ$contests[$in{no}][0]‚ªŠJÃ‚³‚ê‚Ü‚µ‚½I“Š•[’÷‚ßØ‚è‚Í$monthŒ$day“ú$hour‚Ü‚Å‚Å‚·</i>");

		# ŸºİÃ½Ä‚ğ‰Šú‰»
		++$round;
	 	open my $fh2, "> $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		print $fh2 "$end_time<>$round<>\n";
		close $fh2;
		mkdir "$this_dir/$round" or &error("$this_dir/$roundÃŞ¨Ú¸ÄØ‚ªì‚ê‚Ü‚¹‚ñ");
	}
	else {
		# ŠÔ‚ğ‰„’·
		--$round;
	 	open my $fh2, "> $this_dir/entry.cgi" or &error("$this_dir/entry.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		print $fh2 "$end_time<>$round<>\n";
		close $fh2;
	}
}

#=================================================
# “Š•[ˆ—
#=================================================
sub vote {
	&read_user;
	&error("ºÒİÄ‚Ì•¶š”µ°ÊŞ°B‘SŠp30[”¼Šp60]•¶š‚Ü‚Å") if length $in{vote_comment} > 60;

	# “Š•[Ï‚İ‚È‚çØÀ°İB–¢“Š•[‚È‚ç–¼‘O‚ğ’Ç‰Á
	if (&add_vote_name) {
		$mes .= "Œ»İs‚í‚ê‚Ä‚¢‚é $contests[$in{no}][0] ‚É‚Í‚·‚Å‚É“Š•[Ï‚İ‚Å‚·<br>";
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		if ($in{vote} eq $no) {
			++$vote;
			if ($in{vote_comment}) {
				$comment .= qq|<b>$m{name}</b>¢$in{vote_comment}£,|;
				$mes .= "$in{vote_comment}‚Æ‚¢‚¤ºÒİÄ‚Å";
			}
			$mes .= "No.$no $file_title‚É“Š•[‚µ‚Ü‚µ‚½<br>";

			$line = "$no<>$name<>$file_title<>$file_name<>$vote<>$comment<>$m{name},$vote_names<>\n";
		}
		
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
# ------------------
sub add_vote_name {
	open my $fh, "+< $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d;
	if ($line =~ /,\Q$m{name}\E,/) {
		close $fh;
		return 1;
	}
	$line .= "$m{name},";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
	return 0;
}

