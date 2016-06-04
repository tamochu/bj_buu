#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require "$datadir/seed_templates.cgi";
#================================================
# í‘°Ú×
#================================================

&decode;
&header;
&header_profile;
&read_cs;

my $table_class = $is_smart ? "table2" : "table1" ;

&seed_detail;

&footer;
exit;

#================================================
# Ú×
#================================================
sub seed_detail {
	print qq|<table class="$table_class" cellpadding="3">| unless $is_mobile;
	
	for my $i (0..$#seed_templates) {
		next if $datas{$profile->[0]} eq '';
		
		print $is_mobile ? qq|<hr><h2>$profile->[1]</h2><br>$datas{$profile->[0]}<br>|
			: qq|<tr><th align="left">$profile->[1]</th></tr><tr><td>$datas{$profile->[0]}</td></tr>|;
	}
	print qq|</table>| unless $is_mobile;
}
