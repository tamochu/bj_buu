#!/usr/local/bin/perl --
require './lib/system.cgi';
#================================================
# ‚¨ŠG•`‚«Œãˆ—(url_exit) Created by Merino
#================================================
&decode;

my $name = pack 'H*', $in{id};

my $image_type = -f "./user/$in{id}/picture/_$in{time}.png" ? 'png' : 'jpeg';
$mes .= qq|<img src="./user/$in{id}/picture/_$in{time}.$image_type"><br>ŠG‚ğ$name‚ÌÏ²Ëß¸Á¬‚É•Û‘¶‚µ‚Ü‚µ‚½<br>|;
require 'bj.cgi';
exit;

