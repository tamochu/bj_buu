#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/chat.cgi';
#=================================================
# ˜S–Á¬¯Ä Created by Merino
#=================================================
&get_data;

if ($m{lib} eq 'prison') {
	$this_title = "$cs{name}[$y{country}]‚Ì˜S–";
	$this_file  = "$logdir/$y{country}/prison";
}
else {
	$this_title = "$cs{name}[$m{country}]‚Ì˜S–";
	$this_file  = "$logdir/$m{country}/prison";
}
$this_script = 'chat_prison.cgi';
&header2;
#=================================================
&run;
&footer;
exit;
