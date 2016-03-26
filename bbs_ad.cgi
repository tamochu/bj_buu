#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#require './lib/bbs.cgi';
require './lib/bbs2.cgi';
#=================================================
# é“`—pŒf¦”Â Created by Merino
#=================================================
&get_data;

$this_title  = "é“`Œ¾”Â";
#$this_file   = "$logdir/bbs_ad";
$this_file   = "$logdir/bbs_ad2";
#$this_script = 'bbs_ad.cgi';
$this_script = 'bbs_ad2.cgi';
$this_sub_title = "±²ÃÑŒğŠ·,Œ‹¥‘Šè•åW,‚¨“X‚ÌĞ‰î‚È‚Ç";

#=================================================
&run;
&footer;
exit;
