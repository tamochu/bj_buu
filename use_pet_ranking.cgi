#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/_use_pet_log.cgi';
#=================================================
# 国ﾍﾟ廃人ﾗﾝｷﾝｸﾞ Created by nanamie
#=================================================

my $max_ranking = 10;

#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @country_pets;
require './lib/_use_pet_log.cgi' if $rank_status[$in{no}][0] eq 'use_pet';
my $type = $country_pets[$in{no}] > 0 ? "$in{no}" : ''; # ﾌｧｲﾙ名の語末はﾍﾟｯﾄ番号と一致しない 0～n

my $this_file = "$logdir/use_pet_ranking_${type}.cgi";
my $use_pet_ranking_cycle_day = 1;

#unless (-f "$this_file") {
#	open my $fh1, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
#	close $fh1;
#	chmod $chmod, $this_file;
#}

&update_use_pet_ranking if -M $this_file > $use_pet_ranking_cycle_day;
#&update_use_pet_ranking; #すぐに更新したい場合はここのコメントアウトを外す（ただし処理が重くなるので速やかに戻すこと）
&run;
&footer;
exit;


#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	for my $i (0 .. $#country_pets) {
		print $i eq $in{no} ? qq|$pets[$country_pets[$i]][1] / | : qq|<a href="?no=$i">$pets[$country_pets[$i]][1]</a> / |;
	}
	print qq|<a href="player_ranking.cgi?no=0">廃人ﾗﾝｷﾝｸﾞ</a> / |;

	print qq|<h1>$country_pets[$in{no}][1]廃人ﾗﾝｷﾝｸﾞ</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞは$use_pet_ranking_cycle_day日ごとにﾘｾｯﾄされ更新されます</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th></tr>| unless $is_mobile;

	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		if($rank_status[$in{no}][0] eq 'rank'){
			my $tempn = $number;
			my $sran = 0;
			while ($tempn =~ /★/){
				$tempn =~ s/★//;
				$sran++;
			}
			if($sran){
				$d_rank = $rank if ($pre_number != $sran);
				$pre_number = $sran;
			}else {
				$d_rank = $rank if ($pre_number ne $number);
				$pre_number = $number;
			}
		}else {
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
		}
		print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;

	print qq|</table>| unless $is_mobile;
}

#=================================================
# 廃人ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_use_pet_ranking  {
	my %sames = ();
	my @line = ();
	my @p_ranks = ();

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			my $c = &read_use_pet_log($player_id, $country_pets[$in{no}]);

			# ﾗﾝｷﾝｸﾞが埋まっていて最下位より小さければﾗﾝｸｲﾝする訳がない
			next if (@p_ranks > $max_ranking) && ($p_ranks[$#p_ranks][1] >= $c);

			if (0 < $c) {
				# 各ﾌﾟﾚｲﾔｰを挿入ｿｰﾄしながらﾗﾝｸ付けし、ﾗﾝｸ外になった順位は削除
				my $is_insert = 0; # 挿入しているか
				my @count = (1, 0); # 総数, 通過数
				my ($prev_rank, $prev_value) = (0, 0); # 1つ上位の順位と値
				for my $i (0 .. @p_ranks) {
					# 挿入ｿｰﾄでﾌﾟﾚｲﾔｰを大きい順に並べる
					# 同時に順位も計算するので挿入は一回のみ
					if ($c >= $p_ranks[$i][0] && !$is_insert) {
						splice(@p_ranks, $i, 0, [$c, $player]);
						$is_insert = 1;
					}

					# ﾗﾝｷﾝｸﾞから出たﾌﾟﾚｲﾔｰを除外
					# 同順位があるので1人ではなく全員削除
					$count[1] = $prev_value == $p_ranks[$i][0] ? $count[1]+1 : 0;
					my $rank = $count[0] - $count[1]; # 回数 - ダブり数 = 順位
					if ($rank > $prev_rank && $prev_rank >= $max_ranking) {
						splice(@p_ranks, $i, 1) while $p_ranks[$i][1];
						last; # 全員削除したので次の要素はない
					}

					# 次の要素がﾗﾝｸ外かどうか判定するのに順位と値が必要
					($prev_rank, $prev_value) = ($rank, $p_ranks[$i][0]);
					$count[0]++;
				}
			}
		}
		close $cfh;
	}

	# 整形＋末尾のダミー削除
	for my $rank (0 .. $#p_ranks - 1) {
		push(@line, "$p_ranks[$rank][0]<>$p_ranks[$rank][1]<>\n");
	}
	undef(@p_ranks);

	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}
