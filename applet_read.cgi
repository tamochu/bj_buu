#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_comment_tag.cgi';

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

open my $fh, "< $this_file.cgi" or &error("$this_file.cgi Ãß≤ŸÇ™äJÇØÇ‹ÇπÇÒ");
while (my $line = <$fh>) {
	my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	unless ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$bname .= "[$bshogo]" if $bshogo;
	}
	$bcomment = &comment_change($bcomment, 1);

	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|$bnameÅF$bcomment (ìΩñºÇ»Ç§: $bdate)\n|;
	}else{
		print qq|$bnameÅF$bcomment ($cs{name}[$bcountry] : $bdate)\n|;
	}
}
close $fh;

exit;
