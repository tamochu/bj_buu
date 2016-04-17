#!/usr/local/bin/perl --
require 'config.cgi';
#require './lib/chat.cgi';
require './lib/bbs.cgi';
#=================================================
# ã§í ¡¨Øƒ Created by Merino
#=================================================
&get_data;

$this_file   = "$logdir/chat_admin";
$this_title  = "â^âcãcò_èÍ";
$this_script = 'chat_admin.cgi';

#&header2;
#=================================================
&run;
&footer;
exit;
