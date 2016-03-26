#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/profile.cgi";
#================================================
# í—ğ•\¦ Created by Merino
#================================================
&decode;
&header;
&header_profile;
&run;
&footer;
exit;
#================================================
sub run {
	open my $fh, "< $userdir/$in{id}/memory.cgi" or &error("$userdir/$in{id}/memory.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}
