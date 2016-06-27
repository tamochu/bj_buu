#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#use Time::HiRes qw(gettimeofday tv_interval);
#=================================================
# 廃人ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

my @rank_status = (
#変数,表示名,最低値
	['strong','奪国力',500],
	['gou','強奪',3000],
	['cho','諜報',3000],
	['sen','洗脳',3000],
	['nou','農業',50000],
	['sho','商業',50000],
	['hei','徴兵',50000],
	['sal','給料',10000],
);


#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = int($in{no});
$in{no} = 0 if $in{no} > $w{country};
my $this_file = "$logdir/year_player_ranking_country_$in{no}.cgi";

my $max_ranking = $in{rank_num} ? $in{rank_num} : ($in{no} == 0 ? 3 : 10);

&update_player_ranking if $in{renew};
#&update_player_ranking; #すぐに更新したい場合はここのコメントアウトを外す（ただし処理が重くなるので速やかに戻すこと）
&run;
&footer;
exit;


#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	for my $i (0 .. $w{country}) {
		print $i eq $in{no} ? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / | : qq|<a href="?no=$i">$cs{name}[$i]</a> / |;
	}
	unless(-f "$this_file"){
		open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
		print $fh "1";
		close $fh;
	}
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $year = <$fh>;
	close $fh;
	&update_player_ranking if ($w{year} > $year+1);

	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $year = <$fh>;
	for my $no (0..$#rank_status){
		my $rank = 1;
		print qq|<h1>$year年$rank_status[$no][1]年間ﾗﾝｷﾝｸﾞ</h1>|;

		print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th></tr>| unless $is_mobile;
	
		my $pre_number = 0;
		my $d_rank;
		while ($line = <$fh>) {
			my($number,$name) = split /<>/, $line;
			last if($number == 0);
			my $id_name = $name;
			if($rank_status[$no][0] eq 'strong'){
				$id_name =~ s/ .*?から最も奪う//;
			}
			my $player_id =  unpack 'H*', $id_name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a>/$cs{name}[$in{no}]/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a></td><td>$cs{name}[$in{no}]<br></td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a></td><td>$cs{name}[$in{no}]<br></td></tr>\n|
				;
			++$rank;
		}
		print qq|</table>| unless $is_mobile;
	}
	close $fh;
}

#=================================================
# 廃人ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_player_ranking  {
#	my $t0 = [gettimeofday];
	my @line = ();
	my $last_year = $w{year} - 1;
	push @line, "$last_year\n";
	$country = $in{no};

	my @p_ranks = ();
	for my $no (0 .. $#rank_status) {
		push(@{$p_ranks[$no]}, [0, 0]);
	}

	my %sames = ();
	open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");
	while (my $player = <$cfh>) {
		$player =~ tr/\x0D\x0A//d;
		next if ++$sames{$player} > 1;
		my $player_id = unpack 'H*', $player;
		unless (-f "$userdir/$player_id/year_ranking.cgi") {
			next;
		}

		open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgiﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			next if index($line, "year;$last_year", 0) < 0; # 前年以外のデータは無意味なので解析しない

			# 前年の一年ﾗﾝｷﾝｸﾞﾃﾞｰﾀの取り出し
			my %ydata;
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				$ydata{$k} = $v;
			}

			for my $no (0 .. $#rank_status) {
				my $status = $rank_status[$no][0];
				next if $ydata{$status} < $rank_status[$no][2];
				# ﾗﾝｷﾝｸﾞが埋まっていて最下位より小さければﾗﾝｸｲﾝする訳がない
				next if ($#{$p_ranks[$no]} >= $max_ranking) && ($p_ranks[$no][$#{$p_ranks[$no]}-1][0] > $ydata{$status});

				my $from = '';
				if ($status eq 'strong') {
					my $strong_c;
					my $strong_v = 0;
					for my $from_c (1 .. $w{country}){
						if($strong_v < $ydata{"strong_".$from_c}){
							$strong_v = $ydata{"strong_".$from_c};
							$strong_c = $from_c;
						}
					}
					$from = " $cs{name}[$strong_c]から最も奪う";
				}

				# 各ﾌﾟﾚｲﾔｰを挿入ｿｰﾄしながらﾗﾝｸ付けし、ﾗﾝｸ外になった順位は削除
				my $is_insert = 0; # 挿入しているか
				my @count = (1, 0); # 総数, 通過数
				my ($prev_rank, $prev_value) = (0, 0); # 1つ上位の順位と値
				for my $j (0 .. $#{$p_ranks[$no]}) {
					# 挿入ｿｰﾄでﾌﾟﾚｲﾔｰを大きい順に並べる
					# 同時に順位も計算するので挿入は一回のみ
					if ($ydata{$status} > $p_ranks[$no][$j][0] && !$is_insert) {
						splice(@{$p_ranks[$no]}, $j, 0, [$ydata{$status}, $player.$from]);
						$is_insert = 1;
					}
	
					# ﾗﾝｷﾝｸﾞから出たﾌﾟﾚｲﾔｰを除外
					# 同順位があるので1人ではなく全員削除
					$count[1] = $prev_value == $p_ranks[$no][$j][0] ? $count[1]+1 : 0;
					my $rank = $count[0] - $count[1]; # 回数 - ダブり数 = 順位
					if ($rank > $prev_rank && $prev_rank >= $max_ranking) {
						splice(@{$p_ranks[$no]}, $j, 1) while $p_ranks[$no][$j][0];
						last; # 全員削除したので次の要素はない
					}
	
					# 次の要素がﾗﾝｸ外かどうか判定するのに順位と値が必要
					($prev_rank, $prev_value) = ($rank, $p_ranks[$no][$j][0]);
					$count[0]++;
				}
=pod
				# ﾗﾝｷﾝｸﾞに自分のﾃﾞｰﾀを挿入ｿｰﾄ、ﾗﾝｸ外に出たﾃﾞｰﾀを削除
				# 同位の考慮はしなくてもええんでね
				for my $rank (0 .. $#{$p_ranks[$no]}) {
					if ($ydata{$status} > $p_ranks[$no][$rank][0]) {
						splice(@{$p_ranks[$no]}, $rank, 0, [$ydata{$status}, "$player$from"]);
						splice(@{$p_ranks[$no]}, $#{$p_ranks[$no]}-1, 1) if $#{$p_ranks[$no]} > $max_ranking; # ﾀﾞﾐｰﾃﾞｰﾀが1個あるから$#
						last;
					}
				}
=cut
			}
		}
		close $fh;
	}
	close $cfh;

	# 各種ﾗﾝｷﾝｸﾞの10位以内のﾌﾟﾚｲﾔｰを追加
	for my $no (0 .. $#rank_status) {
		for my $rank (0 .. $#{$p_ranks[$no]}-1) {
			push(@line, "$p_ranks[$no][$rank][0]<>$p_ranks[$no][$rank][1]<>\n");
		}
		push @line, "0<><>\n";
	}
	undef(@p_ranks);

	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	print $fh @line;
	close $fh;

#	my $timer = tv_interval($t0);
#	print "$timer ms<br>";
}
