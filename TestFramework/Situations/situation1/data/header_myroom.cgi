#=================================================
# ÌßÛÌ¨°Ùİ’è Created by Merino
#=================================================
# ’Ç‰Á/íœ/•ÏX/•À‚Ñ‘Ö‚¦‰Â
# ÌßÛÌ¨°Ù‚Å•\¦‚·‚é‚à‚ÌB¶‚Ì‰pš‚Í“¯‚¶‚¶‚á‚È‚¯‚ê‚Î‰½‚Å‚à—Ç‚¢

my @files = (
	['è†',	'letter'],
	['“ú‹L',	'blog'],
	['‚¨ŠG•`‚«','oekaki'],
	['–{ì¬',	'book'],
	['‚¨ŠG•`‚«(¼°Êß¯Êß)','oekaki_spp'],
);


#=================================================
# ÌßÛÌ¨°ÙÍ¯ÀŞ°
#=================================================
sub header_myroom {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;

	for my $i (0 .. $#files) {
		next if ($is_mobile || $is_smart) && $files[$i][1] eq 'oekaki';
		next if $is_mobile && $files[$i][1] eq 'oekaki_spp';
		print $in{no} eq $i ? qq| $files[$i][0] /| : qq| <a href="$files[$i][1].cgi?id=$id&pass=$pass&no=$i">$files[$i][0]</a> /|;
	}
	print qq|<h1>$files[$in{no}][0]</h1>|;
}


1; # íœ•s‰Â
