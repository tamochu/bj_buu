#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ‚¨ŠG•`‚«•Û‘¶(url_save) Created by Merino
#================================================

# “Še‚Å‚«‚éÅ‘å»²½Ş
$max_data_size = 5000;


#================================================
$ENV{REQUEST_METHOD} =~ tr/a-z/A-Z/;
&error_oekaki("POSTˆÈŠO‚ÌØ¸´½ÄÒ¿¯ÄŞ‚ÍóM‚Å‚«‚Ü‚¹‚ñ") unless $ENV{REQUEST_METHOD} eq 'POST';
&error_oekaki("ÃŞ°À‚ª‘å‚«‚·‚¬‚Ü‚·") if $ENV{CONTENT_LENGTH} > $max_data_size;

my $buf = '';
binmode STDIN;
read(STDIN, $buf, $ENV{CONTENT_LENGTH});

my $header_magic = substr($buf, 0, 1);
if ($header_magic =~ /^[SP]$/) { &save_img($buf); }
else { &error_oekaki('‘Î‰‚µ‚Ä‚¢‚È‚¢¸×²±İÄ‚Å‚·'); }
exit;

#================================================
sub save_img {
	my $buf = shift;
	
	my $header_length      = substr($buf, 1, 8);
	my $send_header_length = index($buf, ";", 1 + 8);
	my $send_header        = substr($buf, 1 + 8, $send_header_length - (1 + 8) );
	my $img_length         = substr($buf, 1 + 8 + $header_length, 8);
	my $img_data           = substr($buf, 1 + 8 + $header_length + 8 + 2, $img_length);
	
	my %p = ();
	for my $pair (split /&/, $send_header) {
		my($k, $v) = split /=/, $pair;
		$p{$k} = $v;
	}
	
	&error_oekaki("ÌßÚ²Ô°“o˜^‚³‚ê‚Ä‚¢‚Ü‚¹‚ñ") unless -d "$userdir/$p{id}";
	my %datas = &get_you_datas($p{id}, 1);
	&error_oekaki("ÌßÚ²Ô°Êß½Ü°ÄŞ‚ªˆá‚¢‚Ü‚·") unless $datas{pass} eq $p{pass};
	
	$p{image_type} =~ tr/A-Z/a-z/;
	&error_oekaki("PNG‚ÆJPEGˆÈŠO‚Ìo—Í‚Í‹–‰Â‚³‚ê‚Ä‚¢‚Ü‚¹‚ñ") unless $p{image_type} eq 'jpeg' || $p{image_type} eq 'png';
	&error_oekaki("JPEGˆÈŠO‚Ìo—Í‚Í‹–‰Â‚³‚ê‚Ä‚¢‚Ü‚¹‚ñ")      if $is_force_jpeg && $p{image_type} ne 'jpeg';
	
	open my $fh, "> $userdir/$p{id}/picture/_$p{time}.$p{image_type}" or &error_oekaki("‰æ‘œ‚Ì•Û‘¶‚É¸”s‚µ‚Ü‚µ‚½");
	binmode $fh;
	print $fh $img_data;
	close $fh;
	
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

