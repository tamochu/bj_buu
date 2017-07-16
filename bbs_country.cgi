#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbsc.cgi';
#=================================================
# 国掲示板 Created by Merino
#=================================================
&get_data;
#&error("$cs{name}[0]の方はご利用できません") if $m{country} eq '0';
&error("牢獄中は作戦会議室には入れません") if $m{lib} eq 'prison';

# 会議室のﾃﾞﾌｫﾙﾄ名：○○作戦会議室
# country_config.cgi で直打ち利用されてるのでﾃﾞﾌｫﾙﾄ変える場合はそちらも要変更…
$this_title  = $cs{bbs_name}[$m{country}] eq '' ? "$cs{name}[$m{country}]作戦会議室" : $cs{bbs_name}[$m{country}];
$this_file   = "$logdir/$m{country}/bbs";
$this_script = 'bbs_country.cgi';

# その国の人しか書き込まないので文字色をﾃﾞﾌｫﾙﾄ色(色付がいい場合は↓一行削除)
$cs{color}[$m{country}] = $cs{color}[0];

#=================================================
&run;
&footer;
exit;
