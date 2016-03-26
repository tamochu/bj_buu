#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_write_tag.cgi';
require "$datadir/casino.cgi";
#require 'lib/casino_mahjang_base.cgi';

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

$this_file = "$logdir/chat_casino$files[$m{c_type}][2]";
require "./lib/casino_$files[$m{c_type}][1].cgi";#run,get_member,etc

print "$in{mode}";
if ($in{mode} eq "play") {
	$in{comment} = &play_card;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "draw") {
	$in{comment} = &draw_card;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "eat") {
	$in{comment} = &eat_card;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "kan") {
	$in{comment} = &kan_card;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "peh") {
	$in{comment} = &peh_card;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "finish_r") {
	$in{comment} = &finish_r($in{target});
	$in{comment} .= $yaku;
	&write_comment if $in{comment};
}
elsif ($in{mode} eq "finish_t") {
	$in{comment} = &finish_t;
	$in{comment} .= $yaku;
	&write_comment if $in{comment};
}
exit;
sub write_comment {
	&error('–{•¶‚É‰½‚à‘‚©‚ê‚Ä‚¢‚Ü‚¹‚ñ') if $in{comment} eq '';
	&error("–{•¶‚ª’·‚·‚¬‚Ü‚·(”¼Šp$max_comment•¶Žš‚Ü‚Å)") if length $in{comment} > $max_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	
	# µ°ÄØÝ¸
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 1);

	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	push @lines, $head_line;

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}
