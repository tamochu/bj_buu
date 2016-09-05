#================================================
# 10秒当てゲーム
#================================================
require './lib/_casino_funcs.cgi';

sub header2 {
	my $auto_loader_head = '';
	if ($is_mobile) {
		print qq|</head><body $body><a name="top"></a>|;
	}
	else {
		if ($files[$m{c_type}][3]) {
			$auto_loader_head = &auto_loader($this_file, 1);
		}
		print <<"EOM";
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">
<link rel="stylesheet" type="text/css" href="$htmldir/themes/green/style.css">

<script language="JavaScript">
<!--
myButton = 0;
function myCheck() {
	if (myButton == 0) {
		myStart = Date.now();
		myButton = 1;
		document.form.startButton.value = "Stop";
		myInterval = setInterval("myDisp()",10);
	}
	else {
		clearInterval( myInterval );
		myDisp(true);

		myButton = 0;
		document.form.startButton.value = "Start";
	}
}
function myDisp(result) {
	myStop=Date.now();
	myTime = myStop - myStart;

	var milli_sec = myTime % 1000;
	myTime = (myTime - milli_sec) / 1000;
	var sec = myTime % 60;
	milli_sec = (((milli_sec < 100) ? "0" : "") + ((milli_sec < 10) ? "0" : "") + milli_sec).slice(0, 2);

	if (result) {
		milli_sec += "秒";
	}
	if (sec < 5 || result) {
		document.form.comment.value = sec + "." + milli_sec;
	}
	else {
		document.form.comment.value = "";
	}
}

function textset(text){
	document.form.comment.value = document.form.comment.value + text;
}
function textfocus() {
	document.form.comment.focus();
	return true;
}
-->
</script>
<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js"></script>
$auto_loader_head
<script type="text/javascript" src="$htmldir/enchant.js"></script>
$enchant_game
</head>
<body $body>
EOM
	}
}

sub run {
	unless (-f "$this_file.cgi") {
		open my $fh, "> $this_file.cgi";
		close $fh;
	}
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&write_comment if ($in{mode} eq "write") && $in{comment};
	}

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b" readonly="readonly"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="button" value="Start" name="startButton" onclick="myCheck()" class="button_s">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;
	my($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember, $number_log) = &get_member;

	unless ($is_mobile) {
		print qq|自動ﾘﾛｰﾄﾞ<select name="reload_time" class="select1"><option value="0">なし|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]秒| : qq|<option value="$i">$reload_times[$i]秒|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c人:$member</font><br>|;

	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;


}

sub get_member {
    my $is_find = 0;
    my $member  = '';
    my @members = ();
    my %sames   = ();

	unless (-f "${this_file}_member.cgi") {
		open my $fh, "> ${this_file}_member.cgi";
		close $fh;
	}
    open my $fh, "+< ${this_file}_member.cgi"
        or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
    eval { flock $fh, 2; };
    while (my $line = <$fh>) {
        my ($mtime, $mname, $maddr) = split /<>/, $line;
        next if $time - $limit_member_time > $mtime;
        next if $sames{$mname}++;                      # 同じ人なら次

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
    seek $fh, 0, 0;
    truncate $fh, 0;
    print $fh @members;
    close $fh;

    my $member_c = @members;

    return ($member_c, $member);
}

1;