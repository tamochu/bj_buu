#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/bbs2.cgi';
#=================================================
# 宣伝用掲示板 Created by Merino
#=================================================
&get_data;

$this_title  = "広告看板";
$this_file   = "$logdir/bbs_ad2";
$this_script = 'bbs_ad2.cgi';
$this_sub_title = "アイテムの交換募集など";

#=================================================
&run;
&footer;
exit;
