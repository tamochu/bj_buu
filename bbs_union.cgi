#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# “¯–¿Œf¦”Â Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]‚Ì•û‚Í‚²—˜—p‚Å‚«‚Ü‚¹‚ñ") if $m{country} eq '0';
&error("‘¼‚Ì‘‚Æ“¯–¿‚ğ‘g‚ñ‚Å‚¢‚Ü‚¹‚ñ") unless $union;
&error("˜S–’†‚Í“¯–¿‰ï‹cº‚É‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{lib} eq 'prison';
my $u = &union($m{country}, $union);

$this_title  = "$cs{name}[$m{country}]+$cs{name}[$union] “¯–¿‰ï‹cº";
$this_file   = "$logdir/union/$u";
$this_script = 'bbs_union.cgi';

#=================================================
&run;
&footer;
exit;
