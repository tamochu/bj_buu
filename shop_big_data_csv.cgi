#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

my @lines = &get_sale_data_log(0, 0);

print "Content-Type: text/csv\n";
print "Content-Disposition: attachment; filename=data.csv\n\n";

for my $line (@lines) {
	my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
	my $item_mes = $kind eq '1' ? qq|[$weas[$item_no][2]]$weas[$item_no][1]Åö$item_lv($item_c/$weas[$item_no][4])|
			  : $kind eq '2' ? qq|[óë]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])|
			  : $kind eq '3' ? qq|[Çÿ]$pets[$item_no][1]Åö$item_c|
			  :			       qq|[$guas[$item_no][2]]$guas[$item_no][1]|
			  ;
	print "$kind,$item_no,$item_c,$item_lv,$price,$place,$i_time,$item_mes\n";
}

exit;