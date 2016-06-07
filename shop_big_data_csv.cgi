#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

my @lines = &get_sale_data_log(0, 0);

print "Content-Type: text/csv\n";
print "Content-Disposition: attachment; filename=data.csv\n\n";

for my $line (@lines) {
	my ($kind, $item_no, $item_c, $item_lv, $price, $place, $i_time) = split /<>/, $line;
	my $item_mes = &get_item_name($kind, $item_no, $item_c, $item_lv);
	print "$kind,$item_no,$item_c,$item_lv,$price,$place,$i_time,$item_mes\n";
}

exit;