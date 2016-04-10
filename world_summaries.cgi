#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ¢ŠEî¨•\¦ Created by nanamie
#================================================


@world_summaries = (
	# •½˜a
	'•½˜a', '”É‰h','Šv–½','—ª’D','–\ŒN','¬“×','Œ‹‘©','“S•Ç','•s’‡','â–]','[•£','ŠÄ‹Ö','–ï”N','Ià','‘åEŠE','–À‘–','“½–¼','”’•º','E”°','“ä','‰Ô‰Î','Ù‘¬','‰p—Y','O‘u','•s‹ä‘Õ“V','¬—',   'ˆÃ•');

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

	print qq|<h1>$world_states[$in{world}]</h1><hr>|;
	print "Œ»İ‚Ì¢ŠEî¨‚Í $world_states[$in{world}] ‚Å‚·B<br>";
	print "$world_summaries[$in{world}]";
}