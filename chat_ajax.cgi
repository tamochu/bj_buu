#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_comment_tag.cgi';
require 'lib/_bbs_chat.cgi';
#=================================================
# 共通ﾁｬｯﾄ Created by Merino
#=================================================
&decode;
print "Content-type: text/html; charset=Shift_JIS\n";
print "\n";
&read_user;
&access_check;
&read_cs;

$this_file = $in{file};
$limit_member_time = 30;
my($member_c, $member) = &get_member;
if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
	print qq|</form><font size="2">$member_c人</font><hr>|;
}else{
	print qq|</form><font size="2">$member_c人:$member</font><hr>|;
}
open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
my $i = 0;
while (my $line = <$fh>) {
	$i++;
	if ($in{ten_limit} && $i > 7) {
		last;
	}
	my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	unless ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$bname .= "[$bshogo]" if $bshogo;
	}
	$bcomment = &comment_change($bcomment, 1);

	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|<font color="#ffffff">$bname：$bcomment <font size="1">(匿名なう: $bdate)</font></font><hr size="1">\n|;
	}else{
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
}
close $fh;
#=================================================
exit;
