#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ‹¤’ÊŒf¦”Â Created by Merino
#=================================================
&get_data;
&error("$cs{name}[$w{country}]‚Ì•û‚Í“ü‚ê‚Ü‚¹‚ñ") unless $m{country};
&error("$cs{name}[$w{country}]‚Ì•û‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{country} eq $w{country};
&error("NPC‘‚Æ“¯–¿‚Ì‘‚Í••ˆó‹Rm’c–{•”‚É‚Í“ü‚ê‚Ü‚¹‚ñ") if $w{"p_$m{country}_$w{country}"} eq '1';
&error("˜S–’†‚Í••ˆó‹Rm’c–{•”‚É‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{lib} eq 'prison';

$this_title  = "••ˆó‹Rm’c–{•”";
$this_file   = "$logdir/bbs_vs_npc";
$this_script = 'bbs_vs_npc.cgi';
$this_sub_title = "‘ÎNPC‘ŒR";

#=================================================
&run;
&footer;
exit;
