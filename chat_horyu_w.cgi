#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# 改造案討論所スレ建て
#=================================================
use File::Copy;

&get_data;

$this_title  = "改造案議題作成";
$this_list   = "$logdir/chat_horyu_list";
$save_list   = "$logdir/chat_horyu_list_s";
$this_dir    = "$logdir/kaizou";
$save_dir    = "$logdir/kaizou2";
$this_script = 'chat_horyu_w.cgi';
$this_return = 'chat_horyu_w';

@deletable_member = ($admin_name, $admin_sub_name);

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 2000;

#=================================================
&run;
&footer;
exit;

#=================================================
sub run {

	&write_comment if ($in{mode} eq "write" && $in{target} eq "new" && $in{comment});
	&del_comment if ($in{mode} eq "write" && $in{target} ne "new" && &delete_check);

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="hidden" name="limit" value="365">|;
#	print qq|<select name="limit">|;
#	print qq|<option value="1">期限一日</option>|;
#	print qq|<option value="3">期限三日</option>|;
#	print qq|<option value="7" selected>期限七日</option>|;
#	print qq|<option value="365" selected>たたき台</option>|;
#	print qq|</select>|;
	print qq|<input type="submit" value="作成" class="button_s"><br>|;
	print qq|<input type="radio" name="target" value="new" checked>議題を作成<br><hr size="5"><br>|;
	print qq|<input type="checkbox" name="save" value="1" checked>終了議案を保存<br>|;
	
	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
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
		if($limit > $time){
			print qq|実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad\n|;
		}else{
			if($goodn > $badn){
				print qq|<font size="5"><font color="blue">実装希望者 $goodn 人:$bgood</font> 実装反対者 $badn 人:$bbad この議題は期間を過ぎてます</font><br>\n|;
			}elsif($goodn < $badn){
				print qq|<font size="5">実装希望者 $goodn 人:$bgood <font color="red">実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
			}else{
				print qq|<font size="5"><font color="yellow">実装希望者 $goodn 人:$bgood 実装反対者 $badn 人:$bbad</font> この議題は期間を過ぎてます</font><br>\n|;
			}
		}
		print qq|<input type="radio" name="target" value="$line">この議題を消去<br>|;
		 $linet = <$fh2>;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
		if ($hidden) {
			$bname = "匿名";
			$bicon = $default_icon;
			$bcountry = 0;
		}
		$bcomment = &comment_change($bcomment, 1);
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		close $fh2;
		print qq|<hr size="5">\n|;
	}
	close $fh;
	print qq|</form>|;
}

#=================================================
# 書き込み処理
#=================================================
sub write_comment {
	&error('本文に何も書かれていません') if $in{comment} eq '';
	&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;
	my $max = 1;
	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		chomp($line);
		if($line > $max){
			$max = $line;
		}
	}
	close $fh;
	my $target = $max+1;

	open my $fhw, ">> $this_list.cgi" or &error("$this_list.cgi ﾌｧｲﾙが開けません");
	print $fhw "$target\n";
	close $fhw;

	open my $fh2, "> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ﾌｧｲﾙが開けません");

	# ｵｰﾄﾘﾝｸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	
	my $limit = $in{limit} * 24 * 3600;
	my $limit_time = $time + $limit;
	my ($lmin, $lhour, $lday, $lmon) = (localtime($limit_time))[1, 2, 3, 4];
	$lmon += 1;
	if ($in{limit} <= 7) {
		$in{comment} .= "<br>議論期限:$lmon月$lday日$lhour時$lmin分";
	}

	print $fh2 "<><>$limit_time<>0<>\n";
	print $fh2 "$time<>$date<>$m{name}さん提出<br>議題<>0<><>$addr<>$in{comment}<>$m{icon}<>\n";
	close $fh2;

	$in{comment} = "$m{name}さんが改造案を作成しました<hr>【改造案から送信】";
	my $mname = $m{name};
	$m{name} = 'システム';
	my $mcountry = $m{country};
	$m{country} = 0;
	my $micon = $m{icon};
	$m{icon} = '';
	my $mshogo = $m{shogo};
	$m{shogo} = '';
	&send_group('all');

	$in{comment} = "";
	$m{name} = $mname;
	$m{country} = $mcountry;
	$m{icon} = $micon;
	$m{shogo} = $mshogo;

	return 1;
}

#=================================================
# 議題消去
#=================================================
sub del_comment {
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

	if($in{save}){
		open my $fh2, ">> $save_list.cgi" or &error("$save_list.cgi ﾌｧｲﾙが開けません");
		print $fh2 "$in{target}\n";
		close $fh2;
		copy("$this_dir/$in{target}.cgi", "$save_dir/$in{target}.cgi");
		&doubled_save_clean;
	}
	
	unlink "$this_dir/$in{target}.cgi" or &error("$this_dir/$in{target}.cgi ﾌｧｲﾙが削除できません");

	return 1;
}

#=================================================
# 保存リスト修正
#=================================================
sub doubled_save_clean {
	my @lines;
	my %sames = ();
	open my $fh, "+< $save_list.cgi" or &error("$save_list.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		chomp($line);
		next if $sames{$line}++;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#=================================================
# 削除者チェック
#=================================================
sub delete_check {
	for my $name (@deletable_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}

