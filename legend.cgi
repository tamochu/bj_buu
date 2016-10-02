#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# Î”è Created by Merino
#================================================

# •\Ž¦‚·‚é‚à‚Ì(./log/legend/‚É‚ ‚é‚à‚Ì)@’Ç‰Áíœ•À‚×‘Ö‚¦‰Â”\
my @files = (
#	['À²ÄÙ',				'Û¸ÞÌ§²Ù–¼'],
	['—ð‘ã‚Ì‘å—¤”eŽÒ',		'touitu'	],
	['õ‰i‰“‚ÌØõ',		'comp_shogo'],
	['½·ÙÏ½À°',				'comp_skill'],
	['³ªÎßÝÏ½À°',			'comp_wea'	],
	['±°Ï°Ï½À°',			'comp_gua'	],
	['´¯¸ÞÏ½À°',			'comp_egg'	],
	['Íß¯ÄÏ½À°',			'comp_pet'	],
	['ËßÖËßÖ—ð‘ã‹­‰¤ŽÒ',	'champ_0'	],
	['ËÞ·ÞÅ°—ð‘ã‹­‰¤ŽÒ',	'champ_1'	],
	['ÍÞÃ×Ý—ð‘ã‹­‰¤ŽÒ',		'champ_2'	],
	['Ï¼Þ¼¬Ý—ð‘ã‹­‰¤ŽÒ',	'champ_3'	],
	['¿Ù¼Þ¬°—ð‘ã‹­‰¤ŽÒ',	'champ_4'	],
	['Á¬ÝËßµÝ—ð‘ã‹­‰¤ŽÒ',	'champ_5'	],
);


#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	}

	for my $i (0 .. $#files) {
		next unless -s "$logdir/legend/$files[$i][1].cgi";
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	
	open my $fh, "< $logdir/legend/$files[$in{no}][1].cgi" or &error("$logdir/legend/$files[$in{no}][1].cgiÌ§²Ù‚ª“Ç‚Ýž‚ß‚Ü‚¹‚ñ");
	print qq|<li>$_</li><hr>\n| while <$fh>;
	close $fh;
}
