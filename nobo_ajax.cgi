#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/_nobo_common.cgi';
use lib './lib';
use JSON;

&decode;
&read_user;
&access_check;
&read_cs;

if ($in{log}) {
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	&log_run;
} else {
	print "Content-type: applecation/json; charset=utf-8\n\n";
	&run;
}

sub run {
	my $nobo = &getNobO($id);
	
	my $coder = JSON->new->utf8->convert_blessed;
	print $coder->encode($nobo);
}

sub log_run {
	my $this_file = "$userdir/$id/nobo_letter.cgi";
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_file Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		close $fh;
	}
	open my $fh, "< $this_file" or &error("$this_file Ì§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	my $i = 0;
	while (my $line = <$fh>) {
		$i++;
		if ($i > 5) {
			last;
		}
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		print qq|$bcomment <font size="1">($bdate)</font><hr size="1">\n|;
	}
	close $fh;
}

exit;
