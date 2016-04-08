require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
#================================================
# BBS Created by Merino
#================================================

# 連続書き込み禁止時間(秒)
$bad_time    = 10;

# 最大ﾛｸﾞ保存件数
$max_log     = 50;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 2000;

# ﾒﾝﾊﾞｰに表示される時間(秒)
$limit_member_time = 60 * 4;

# 最大過去ﾛｸﾞ保存件数
$max_bbs_past_log = 50;


#================================================
sub run {
	if ($in{mode} eq "write" && $in{comment} && (&is_daihyo || &is_sabakan)) {
		&write_comment;
		
		# 保存ﾛｸﾞ用
		if ($in{is_save_log}) {
			my $sub_this_file = $this_file;
			$this_file .= "_log";
			$max_log = $max_bbs_past_log;
			&write_comment;
			$this_file = $sub_this_file;
			$mes .= "書き込みをﾛｸﾞ保存しました<br>";
		}
	}
	
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;

	my $this_script_p = $this_script;
	$this_script_p =~ s/\.cgi//;
	print qq|<form method="$method" action="past_log.cgi"><input type="hidden" name="this_title" value="$this_title">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="this_file" value="$this_file"><input type="hidden" name="this_script" value="$this_script_p">|;
	print qq|<input type="submit" value="過去ﾛｸﾞ" class="button_s"></form>|;
	
	if(&is_daihyo || &is_sabakan){
		my $rows = $is_mobile ? 2 : 5;
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
		print qq|<input type="submit" value="書き込む" class="button_s">|;
		print qq|　 <input type="checkbox" name="is_save_log" value="1">ﾛｸﾞ保存</form><br>|;
	}
	print qq|<font size="2">$member_c人:$member</font><hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname = &name_link($bname);
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bcomment = &comment_change($bcomment, 0);
		if ($is_mobile) {
			print qq|<div>$bicon<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font></div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br></td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}


1; # 削除不可
