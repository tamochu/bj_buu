#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbsc.cgi';
#=================================================
# 国掲示板 Created by Merino
#=================================================
&get_data;
#&error("$cs{name}[0]の方はご利用できません") if $m{country} eq '0';
&error("牢獄中は作戦会議室には入れません") if $m{lib} eq 'prison';

$this_title  = "$cs{name}[$m{country}]作戦会議室";
$this_file   = "$logdir/$m{country}/bbs";
$this_script = 'bbs_country.cgi';

# その国の人しか書き込まないので文字色をﾃﾞﾌｫﾙﾄ色(色付がいい場合は↓一行削除)
$cs{color}[$m{country}] = $cs{color}[0];

#=================================================
&run;
&footer;
exit;
