#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# Æ­°½•\¦ Created by Merino
#================================================

# •\¦‚·‚é‚à‚Ì(./log/‚É‚ ‚é‚à‚Ì)@’Ç‰Áíœ•À‚×‘Ö‚¦‰Â”\
my @files = (
#	['À²ÄÙ',		'Û¸ŞÌ§²Ù–¼'],
	['‰ß‹‚Ì‰hŒõ',	'world_news',		],
	['¢ŠEî¨',	'world_big_news',	],
	['•¨—¬î•ñ',	'send_news',		],
	['“¬‹Zê‚Ì‹OÕ','colosseum_news',	],
	['V’…ÌŞÛ¸Ş',	'blog_news',		],
	['VìŠG‰æ',	'picture_news',		],
	['Vì–{',		'book_news',		],
	['Q“üƒƒO',	'entry_news',		],
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
		if ($is_appli) {
			&show_page_switcher;
		}
		else {
			print qq|<div style="margin-bottom: 14px;">|;
			print qq|<form method="$method" action="$script" style="display: inline;">|;
			print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
			print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
			&show_wait;
			print qq|</div>|;
		}
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	}
	
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="./amida.cgi?id=$in{id}&pass=$in{pass}">±ĞÀŞ¸¼Ş</a> / |;

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	print qq|<font size="1">¦‰æ‘œ‚ª•\\¦‚³‚ê‚Ä‚¢‚È‚¢‚à‚Ì‚ÍA‚»‚Ìl‚ÌÏ²Ëß¸Á¬‚©‚ç‚È‚­‚È‚Á‚½‚à‚Ì‚Å‚·</font><br>| if $files[$in{no}][1] eq 'picture_news';
	
	open my $fh, "< $logdir/$files[$in{no}][1].cgi" or &error("$logdir/$files[$in{no}][1].cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}

sub show_wait {
	&read_user;
#	my %p = get_you_datas($in{id}, 1);
	my $state = '';
	if ($m{lib} eq 'domestic') {
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "”_‹Æ’†‚Å‚·";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "¤‹Æ’†‚Å‚·";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "’¥•º’†‚Å‚·";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}elsif($m{turn} eq '4'){
				$state = "’´‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "’·Šú“à­’†‚Å‚·";
		}
	}elsif($m{lib} eq 'military'){
		$state = "ˆÚ“®’†‚Å‚·";
		if($m{tp} eq '110'){
			$state .= "(‹­’D)";
		}elsif($m{tp} eq '210'){
			$state .= "(’³•ñ)";
		}elsif($m{tp} eq '310'){
			$state .= "(ô”])";
		}elsif($m{tp} eq '410'){
			$state .= "(’ã@)";
		}elsif($m{tp} eq '510'){
			$state .= "(‹UŒv)";
		}elsif($m{tp} eq '610'){
			$state .= "(Ué)";
		}elsif($m{tp} eq '710'){
			if($m{value} eq 'military_ambush'){
				$state = "ŒR–";
			}else{
				$state = "iŒR";
			}
			$state .= "‘Ò‚¿•š‚¹’†‚Å‚·";
		}elsif($m{tp} eq '810'){
			$state .= "(’·Šú‹­’D)";
		}elsif($m{tp} eq '910'){
			$state .= "(’·Šú’³•ñ)";
		}elsif($m{tp} eq '1010'){
			$state .= "(’·Šúô”])";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{prison_name}[$y{country}]‚Å—H•Â’†‚Å‚·";
	}elsif($m{lib} eq 'promise'){
		$state = "ˆÚ“®’†‚Å‚·";
		if($m{tp} eq '110'){
			$state .= "(—FD)";
		}elsif($m{tp} eq '210'){
			$state .= "(’âí)";
		}elsif($m{tp} eq '310'){
			$state .= "(éí•z)";
		}elsif($m{tp} eq '410'){
			$state .= "(“¯–¿ŒğÂ)";
		}elsif($m{tp} eq '510'){
			$state .= "(“¯–¿”jŠü)";
		}elsif($m{tp} eq '610'){
			$state .= "(H—¿—A‘—)";
		}elsif($m{tp} eq '710'){
			$state .= "(‘‹à—A‘—)";
		}elsif($m{tp} eq '810'){
			$state .= "(•ºm—A‘—)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "ˆÚ“®’†‚Å‚·";
		if($m{value} eq '0.5'){
			$state .= "(­”iŒR)";
		}elsif($m{value} eq '1'){
			$state .= "(iŒR)";
		}elsif($m{value} eq '1.5'){
			$state .= "(’·Šú‰“ª)";
		}
	}

	if ($state) {
		my $next_time_mes = sprintf("%d•ª%02d•b", int($m{wt} / 60), int($m{wt} % 60) );
		print qq| $state|;
		print qq| <span id="nokori_time">$next_time_mes</span>| if 0 < $m{wt};
	}
}
