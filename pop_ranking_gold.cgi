#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 人気ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

#=================================================
&decode;
&header;
&read_cs;

my $this_vote_file = "$logdir/pop_vote2.cgi";
my $this_file = "$logdir/pop_vote2_result.cgi";

my $end_time = &date_to_time('2015-09-01');
if (!(-f "$this_file") || ($time > $end_time && (stat $this_file)[9] < $end_time)) {
	&update_pop_ranking;
}

if ($time > $end_time) {
	&run;
} else {
	&preparing;
}
&footer;
exit;


#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	print qq|<h1>人気投票(金)ﾗﾝｷﾝｸﾞ結果発表\</h1>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th></tr>| unless $is_mobile;
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($name,$number,$country) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
		print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}
#=================================================
# 準備画面
#=================================================
sub preparing {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	print qq|<h1>人気投票(金)ﾗﾝｷﾝｸﾞ結果発表\</h1>|;

	print qq|現在集計中です<br>|;
}

#=================================================
# ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_pop_ranking  {
	my %ranks = ();
	
	open my $fh, "< $this_vote_file" or &error('人気投票ファイルが開けません');
	while (my $line = <$fh>) {
		my($pname, $name) = split /<>/, $line;
		my $p_id = unpack 'H*', $pname;
		if (-f "$userdir/$p_id/user.cgi") {
			$ranks{$pname}++;
		}
	}

	my @lines = ();
	for my $name (keys(%ranks)) {
		my $p_id = unpack 'H*', $name;
		my %p = &get_you_datas($p_id, 1);
		my $rank_name = &get_rank_name($p{rank}, $name);
		push @lines, "$name<>$rank_name<>$p{country}<>\n";
	}
	# 票が多い順に並び替え
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	close $fh;
	
	open my $rfh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;
}
