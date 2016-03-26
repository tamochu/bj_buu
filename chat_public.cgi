#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/chat.cgi';
#=================================================
# ‹¤’ÊÁ¬¯Ä Created by Merino
#=================================================
&get_data;

$this_file   = "$logdir/chat_public";
$this_title  = "Œğ—¬Lê";
$this_script = 'chat_public.cgi';

&header2;
#=================================================
&run;
&footer;
exit;
