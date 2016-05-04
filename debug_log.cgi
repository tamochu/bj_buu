#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
my $this_script = 'debug_log.cgi';
#=================================================
# デバッグログ
#=================================================

# 並び順名
my %e2j_sorts = (
	name	=> 'プレイヤー別',
	time	=> '時系列順',
);

# ﾃﾞﾌｫﾙﾄの並び順
$in{sort} ||= 'time';


#=================================================
# メイン処理
#=================================================
&header;
&decode;
&top;
&footer;
exit;

#=================================================
# top
#=================================================
sub top {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	
	print qq|<table border="0"><tr>|;
	while (my($k,$v) = each %e2j_sorts) {
		print qq|<td><form method="$method" action="$this_script">\n|;
		print qq|<input type="hidden" name="sort" value="$k"><input type="submit" value="$v" class="button_s"></form></td>\n|;
	}
	print qq|</tr></table>|;

	print qq|<table class="table1"><tr>|;
	for my $k (qw/ﾌﾟﾚｲﾔｰ 時間 デバッグメッセージ タグ/) {
		print qq|<th>$k</th>|;
	}
	print qq|</tr>|;
	
	# デバッグ情報取得
	my @lines = &get_all_messages($in{tag});
	my $count = 0;
	for my $line (@lines) {
		my($name, $ptime, $message, $tag) = split /<>/, $line;
		my $tag_disp = pack 'H*', $tag;
		
		print ++$count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;

		print qq|<td>$name</td>|;
		print qq|<td>$ptime</td>|;
		print qq|<td>$message</td>|;
		print qq|<td><input type="button" class="button_s" value="$tag_disp" onClick="location.href='?tag=$tag';"></td>|;
		print qq|</tr>|;
	}
	print qq|</table>|;
}

#=================================================
# 全ユーザーのデータを取得
#=================================================
sub get_all_messages {
	my $tag = shift;
	my @lines = ();
	
	open my $fh, "< $logdir/debug_log.cgi";
	while (my $line = <$fh>) {
		my($name, $ptime, $message, $ptag) = split /<>/, $line;
		if (!$tag || $tag eq $ptag) {
			push @lines, $line;
		}
	}
	close $fh;
	
	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[1] cmp $b->[1] || $a->[2] <=> $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'time')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	
	return @lines;
}
