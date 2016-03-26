#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# 改造案討論所保存ログ
#=================================================
&get_data;

$this_title  = "投票済み議案";
$this_list   = "$logdir/chat_horyu_list_s";
$this_dir    = "$logdir/kaizou2";
$this_script = 'chat_horyu_s.cgi';

@del_member = ('黒豚', 'おいいういい');
#=================================================
&run;
&footer;
exit;

#=================================================
sub run {
	&del_thread if ($in{mode} eq "delete" && &del_check);
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ﾌｧｲﾙが開けません");
	my @rev_line;
	while (my $line = <$fh>) {
		unshift @rev_line, $line
	}
	for my $line (@rev_line) {
		chomp($line);
		open my $fh2, "< $this_dir/$line.cgi" or &error("$this_dir/$line.cgi ﾌｧｲﾙが開けません");
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
		print qq|<hr size="1">|;
		if($goodn > $badn){
			print qq|<font size="5"><font color="blue">実装希望者 $goodn 人:$bgood</font> 実装反対者 $badn 人:$bbad この議題は期間を過ぎてます</font><br>\n|;
		}elsif($goodn < $badn){
			print qq|<font size="5">実装希望者 $goodn 人:$bgood <font color="red">実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
		}else{
			print qq|<font size="5"><font color="yellow">実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
		}
		
		if(&del_check){
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="delete">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="削除" class="button_s">|;
			print qq|<input type="hidden" name="target" value="$line"></form>|;
		}
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
		}
		close $fh2;
		print qq|<hr size="5">\n|;
	}
	close $fh;
	print qq|</form>|;
}
#=================================================
# 議題消去
#=================================================
sub del_thread {
	my @lines;
	my %sames = ();
	open my $fh, "+< $this_list.cgi" or &error("$this_list.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		chomp($line);
		if($line != $in{target}){
			next if $sames{$line}++;
			push @lines, "$line\n";
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	unlink "$this_dir/$in{target}.cgi" or &error("$this_dir/$in{target}.cgi ﾌｧｲﾙが削除できません");

	return 1;
}

#=================================================
# 著作者チェック
#=================================================
sub del_check {
	for my $name (@del_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}
