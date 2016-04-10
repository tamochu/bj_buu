#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ¢ŠEî¨•\¦ Created by nanamie
#================================================

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{world} ||= 0;
	$in{world} = 0 if $in{world} >= @world_states;

	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	}

	print "¢ŠEî¨‚Í $world_states[$w{world}] ‚Å‚·B";
}