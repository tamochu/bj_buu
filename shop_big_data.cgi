#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 相場
#=================================================
my $this_script = 'shop_big_data.cgi';
my $csv_script = 'shop_big_data_csv.cgi';
my $update_day = 2 * 3600;

#=================================================
&decode;
&header;

my ($kind, $no) = split /_/, $in{item}; 
$kind ||= 1;
$no ||= 1;
$kind = 1 if $kind < 1 || $kind > 4;

my $this_file = "$htmldir/item_${kind}_${no}.html";
my $html_file = "html/item_${kind}_${no}.html";

if (-e $this_file) {
	if ((stat $filename)[9] + $update_day < $time) {
		&create_sale_data_chart($kind, $no);
	}
} else {
	&create_sale_data_chart($kind, $no);
}
&run;
&footer;
exit;

#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	print qq|<form action="$csv_script"><input type="submit" value="全データCSV取得" class="button1"></form>|;
	print qq|<hr>種類,アイテム番号,アイテム変数1,アイテム変数2,値段,種別(1:商人のお店,2:ｵｰｸｼｮﾝ,3:ｵｰｸｼｮﾝ即決,4:ｼﾞｬﾝｸｼｮｯﾌﾟ,5:破棄等),時間（UNIX時間）,アイテム名<hr>|;

	if (-e $this_file) {
		print qq|<a href="$html_file" target="_blank">相場</a>|;
	} else {
		print qq|参考データがありません。|;
	}
	print qq|<hr>|;
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#weas) {
		if ($i ne '0') {
			print qq|<option value="1_$i">[$weas[$i][2]]$weas[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="武器" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#eggs) {
		if ($i ne '53') {
			print qq|<option value="2_$i">$eggs[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="卵" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#pets) {
		if ($i ne '180' && $i ne '181' && $pets[$i][0] > 0) {
			print qq|<option value="3_$i">$pets[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="ﾍﾟｯﾄ" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#guas) {
		if ($guas[$i][1] !~ /未実装/) {
			print qq|<option value="4_$i">[$guas[$i][2]]$guas[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="防具" class="button1">|;
	print qq|</form>|;

}
