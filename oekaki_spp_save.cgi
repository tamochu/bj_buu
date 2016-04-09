#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

use CGI;
#================================================
# ‚¨ŠG•`‚«•Û‘¶(url_save) Powered by nanamie
#================================================

$cgi = CGI->new;

# “Še‚Å‚«‚éÅ‘å»²½Ş
$max_data_size = 5000;

#================================================
&save_img();
exit;

#================================================
sub save_img {
	my $file = $cgi->param("file");
	
	my $fid = $cgi->param("id");
	my $fpass = $cgi->param("pass");
	
	my $image_type = $file eq '_temp.jpeg' ? "jpeg" : "png";
	
	&error_oekaki("no user dir") unless -d "$userdir/$fid";
	my %datas = &get_you_datas($fid, 1);
	&error_oekaki("wrong password") unless $datas{pass} eq $fpass;
	
	open my $fh, "> $userdir/$fid/picture/_$time.$image_type" or &error_oekaki("save failed");
	binmode $fh;
	while (read($file, $buffer, 1024)) {
		print $fh $buffer;
	}
	close $fh;
	close $file;
	
	print "Content-type: text/plain\n\n";
}

#================================================
# ‚¨ŠG•`‚«‘¤‚É´×°o—Í
sub error_oekaki {
	my $error_message = shift;
	print "Content-type: text/plain\n\nerror\n";
	print "$error_message\n";
	exit;
}

