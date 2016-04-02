#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ‹¤’ÊŒf¦”Â Created by Merino
#=================================================
&get_data;

$this_title  = "$titleŒf¦”Â";
$this_file   = "$logdir/bbs_public";
$this_script = 'bbs_public.cgi';
$this_sub_title = qq|<br>‘‚«‚İŒ ŒÀ‚Ì‚ ‚él‚µ‚©‘‚«‚ß‚Ü‚¹‚ñB<br>ƒoƒO•ñ‚Í<a href="letter.cgi?id=$id&pass=$pass&send_name=‚¨‚¢‚¢‚¤‚¢‚¢">‚±‚¿‚ç</a>‚Ö<br>ˆ¥A‚ÍŒğ—¬‚Ö|;
@writer_member = ($admin_name, $admin_sub_name, $admin_support_name);

#=================================================
&run;
&footer;
exit;
