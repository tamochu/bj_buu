#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# }‘ŠÙ
#================================================

#================================================
&decode;
my $this_dir = "$logdir/library";

&header;
&header_library;

&run;

&footer;
exit;

#================================================
# header
#================================================
sub header_library {
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="–ß‚é" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	}
	print qq|<hr>|;
}


#================================================
# ˆê——•\¦
#================================================
sub run {
	$layout = 2;
	my $count = 0;
	my $sub_mes .= qq|<hr>|;
	opendir my $dh, $this_dir or &error("$this_dirÃŞ¨Ú¸ÄØ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;

		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<li><a href="$this_dir/$file_name" target="_blank">$file_title</a>|;
				  ;
		++$count;
	}
	closedir $dh;
	
	print qq|Š‘ ” $count û<br>|;
	print qq|$sub_mes<hr>|;
}
