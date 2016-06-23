#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use Time::HiRes qw(gettimeofday tv_interval);
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
#			my $from_c;
			if($rank_status[$no][0] eq 'strong'){
				$id_name =~ s/ .*?から最も奪う//;
#				$from_c = $name;
#				$from_c =~ s/.*?( .*?から最も奪う)/\1/g;
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
	my $t0 = [gettimeofday];

	my @line = ();
	my $last_year = $w{year} - 1;

	push @line, "$last_year\n";
	$country = $in{no};

	my %sames = ();
	my @p_ranks = ();
	for my $no (0 .. $#rank_status) {
		push(@{$p_ranks[$no]}, [0, 0]);
	}

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

				# ﾗﾝｷﾝｸﾞに自分のﾃﾞｰﾀを挿入ｿｰﾄ、ﾗﾝｸ外に出たﾃﾞｰﾀを削除
				my $rank_size = $#{$p_ranks[$no]};
				for my $rank (0 .. $rank_size) {
					if ($ydata{$status} > $p_ranks[$no][$rank][0]) {
						splice(@{$p_ranks[$no]}, $rank, 0, [$ydata{$status}, "$player$from"]);
						if ($#{$p_ranks[$no]} > $max_ranking) {
							splice(@{$p_ranks[$no]}, $#{$p_ranks[$no]}-1, 1);
						}
						last;
					}
				}
			}

		}
		close $fh;
	}
	close $cfh;

	for my $no (0 .. $#rank_status) {
=pod
		# 高速化のために sort を使わずﾗﾝｸｲﾝﾌﾟﾚｲﾔｰの上位者を抜き出す
		my $count = 0;
		my $old_max_value = 0;
		my @ranking = (0, 0); # 順位, ダブリ
		while ($max_ranking > $ranking[0]) {
			last unless @{$p_ranks[$no]};
	
			# sort の代わりにトップを順次抜き出す
			my $max_value = 0;
			my $max_index = 0;
			for my $index (0 .. $#{$p_ranks[$no]}) {
				if ($p_ranks[$no][$index][0] > $max_value) {
					$max_value = $p_ranks[$no][$index][0];
					$max_index = $index;
				}
			}
	
			# 2位以下が上位と同じ数値ならダブリ数うｐ、違うならダブリ数リセット
			$ranking[1] = $old_max_value > $max_value ? 0 : $ranking[1]+1 if $count > 0;
			$ranking[0] = $count+1 - $ranking[1]; # (インデックス+1) - ダブリ数 = 順位
=cut

			for my $rank (0 .. $max_ranking-1) {
				push(@line, "$p_ranks[$no][$rank][0]<>$p_ranks[$no][$rank][1]<>\n");
			}
#			push(@line, join('<>', @{splice(@{$p_ranks[$no]}, $max_index, 1)})."<>\n");
#			$count++;
#			$old_max_value = $max_value;
		}
		push @line, "0<><>\n";
	}

#	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
#	print $fh @line;
#	close $fh;

	my $timer = tv_interval($t0);
	print "$timer ms<br>";
}
