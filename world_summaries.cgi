#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ¢ŠEî¨•\¦ Created by nanamie
#================================================


@world_summaries = (
	# •½˜a
	'•½˜a',
	# ”É‰h
	'”É‰h',
	# Šv–½
	'Šv–½',
	# —ª’D
	'—ª’D',
	# –\ŒN
	'–\ŒN',
	# ¬“×
	'¬“×',
	# Œ‹‘©
	'Œ‹‘©',
	# “S•Ç
	'“S•Ç',
	# •s’‡
	'•s’‡',
	# â–]
	'â–]',
	# [‰“
	'[•£',
	# ŠÄ‹Ö
	'ŠÄ‹Ö',
	# –ï”N
	'–ï”N',
	# Ià
	'Ià',
	# ‘åEŠE
	'‘åEŠE',
	# –À‘–
	'–À‘–',
	# “½–¼
	'“½–¼',
	# ”’•º
	'”’•º',
	# E”°
	'E”°',
	# “ä
	'“ä',
	# ‰Ô‰Î
	'‰Ô‰Î',
	# Ù‘¬
	'Ù‘¬',
	# ‰p—Y
	'‰p—Y',
	# O‘u
	'O‘u',
	# •s‹ä‘Õ“V
	'•s‹ä‘Õ“V',
	# ¬—
	'¬—',
	# ˆÃ•
	'ˆÃ•‚Å‚ÍA••ˆó‘‚ÆNPC‘‚Æ‚É•ª‚©‚ê‚Ä“ˆêí‚ğ‚µ‚Ü‚·B<br>'.
	'ˆÈ‰ºÈ—ª'
);

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

	print "<h1>$world_states[$in{world}]</h1>";
	print "$world_summaries[$in{world}]";
}