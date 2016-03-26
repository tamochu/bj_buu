#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_write_tag.cgi';

&decode;
print "Content-type: text/html; charset=Shift_JIS\n";
if ($gzip ne '' && $ENV{HTTP_ACCEPT_ENCODING} =~ /gzip/){  
	if ($ENV{HTTP_ACCEPT_ENCODING} =~ /x-gzip/) {
		print "Content-encoding: x-gzip\n\n";
	}
	else{
		print "Content-encoding: gzip\n\n";
	}
	open STDOUT, "| $gzip -1 -c";
}
else {
	print "\n";
}
&access_check;
&read_user;
&read_cs;

my $this_file = $in{file_name};

if ($in{comment} && $m{silent_time} > $time) {
	if($m{silent_kind} eq '0'){
		$in{comment} = 'んー！んー！' ;
	}elsif($m{silent_kind} eq '1'){
		$in{comment} = 'ﾌｫｳ！' ;
	}elsif($m{silent_kind} eq '2'){
		$in{comment} = 'ﾎﾟｩ！' ;
	}else{
		$in{comment} .= 'ぽぽぽぽーん' ;
	}
}

&error('本文に何も書かれていません') if $in{comment} eq '';
&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;

my @lines = ();
open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
eval { flock $fh, 2; };

my $mname;
($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);

my $head_line = <$fh>;
my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
return 0 if $in{comment} eq $hcomment;
if ($hname eq $m{name} && $htime + $bad_time > $time) {
	&error("連続投稿は禁止しています。<br>しばらく待ってから書き込んでください");
}
push @lines, $head_line;

while (my $line = <$fh>) {
	push @lines, $line;
	last if @lines >= $max_log-1;
}
if($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')){
	$mname = "名無し";
}
unshift @lines, "$time<>$date<>$mname<>$m{country}<>$m{shogo}<>$addr<>$in{comment}<>$m{icon}<>\n";
seek  $fh, 0, 0;
truncate $fh, 0;
print $fh @lines;
close $fh;
exit;
