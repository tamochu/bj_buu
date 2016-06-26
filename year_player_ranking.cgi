#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

use File::Copy;
#=================================================
# 一年ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

my @rank_status = (
#変数,表示名,最低値
    ['strong','奪国力',5000],
    ['nou','農業',100000],
    ['sho','商業',100000],
    ['hei','徴兵',100000],
    ['gou','強奪',30000],
    ['cho','諜報',30000],
    ['sen','洗脳',30000],
    ['gou_t','強奪(累計)',3000],
    ['cho_t','諜報(累計)',3000],
    ['sen_t','洗脳(累計)',3000],
    ['gik','偽計',50],
    ['res','救出',3],
    ['esc','脱獄',3],
    ['tei','偵察',30],
    ['win','勝率（20戦以上）',50],
    ['stop','停戦',5],
    ['pro','友好',10],
    ['sal','給料',10000],
    ['dai','国畜',5],
#    ['mil_sum','軍事',1],
);


#=================================================
&decode;
&header;
&read_cs;

my $max_ranking = $in{rank_num} ? $in{rank_num} : 10;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @rank_status;
my $type = $rank_status[$in{no}][0] ? "_$rank_status[$in{no}][0]" : '';

my $this_file = "$logdir/year_player_ranking${type}.cgi";

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
	for my $i (0 .. $#rank_status) {
		print $i eq $in{no} ? qq|$rank_status[$i][1] / | : qq|<a href="?no=$i">$rank_status[$i][1]</a> / |;
	}
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $year = <$fh>;
	close $fh;
	&update_player_ranking if ($w{year} > $year+1);

	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my $year = <$fh>;
	print qq|<h1>$year年$rank_status[$in{no}][1]年間ﾗﾝｷﾝｸﾞ</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞは毎年ごとにﾘｾｯﾄされ更新されます</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th></tr>| unless $is_mobile;
	
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		$id_name = $name;
		if($rank_status[$in{no}][0] eq 'strong'){
			$id_name =~ s/ .*?から最も奪う//g;
		}
		my $player_id =  unpack 'H*', $id_name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
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
sub update_player_ranking  {
	for my $i(1..10){
		my $to_file_name;
		my $old_year = 10 - $i;
		my $old_file_name = $this_file;
		$old_file_name =~ s/\.cgi//;
		$to_file_name = $old_file_name;
		$old_file_name .= "_" . $old_year . ".cgi";
		if($old_year == 0){
			$old_file_name = $this_file;
		}
		my $to_year = $old_year + 1;
		$to_file_name .= "_" . $to_year . ".cgi";
		if(-f "$old_file_name"){
			if($old_year == 9){
				unlink $old_file_name;
			}else{
				move $old_file_name, $to_file_name;
			}
		}
	}

	my %sames = ();
	my @line = ();
	my @p_ranks = ();
	my $status = $rank_status[$in{no}][0];
	my $rank_min = $rank_status[$in{no}][2];
	
	my $last_year = $w{year} - 1;
	push @line, "$last_year\n";

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/year_ranking.cgi") {
				next;
			}

			my $p_status = 0;
			open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgiﾌｧｲﾙが開けません");
			while (my $line = <$fh>) {
				next if (index($line, "year;$last_year", 0) < 0) || # 前年以外のデータは無意味なので解析しない
							(index($line, $status, 0) < 0); # 参照先データを持たない人まで解析しても無意味

				# 前年の一年ﾗﾝｷﾝｸﾞﾃﾞｰﾀの取り出し
				my %ydata;
				for my $hash (split /<>/, $line) {
					my($k, $v) = split /;/, $hash;
					$ydata{$k} = $v;
				}

				if ($status eq 'mil_sum') {
					$ydata{$status} = $ydata{gou};
					if($ydata{cho} > $ydata{$status}){
						$ydata{$status} = $ydata{cho};
					}
					if($ydata{sen} > $ydata{$status}){
						$ydata{$status} = $ydata{sen};
					}
				}
				elsif ($status eq 'strong') {
					my $strong_c;
					my $strong_v = 0;
					for my $from_c (1 .. $w{country}){
						if($strong_v < $ydata{"strong_".$from_c}){
							$strong_v = $ydata{"strong_".$from_c};
							$strong_c = $from_c;
						}
					}
					$player .= " $cs{name}[$strong_c]から最も奪う";
				}
				elsif ($status eq 'win') {
					$ydata{$status} = $ydata{war} > 20 ? 100 * $ydata{$status} / $ydata{war} : 0;
				}
				$p_status = $ydata{$status};
			}
			close $fh;
			next if $p_status < $rank_min;
			push @p_ranks, [$p_status, $player, $country]; # ﾗﾝｸｲﾝﾌﾟﾚｲﾔｰの追加
		}
		close $cfh;
	}

	# ﾗﾝｸｲﾝﾌﾟﾚｲﾔｰのうち上位者を抜き出して1位のプレイヤーにNo.1熟練付与
	# 高速化のために sort を使ってないけど0.08秒ぐらいしか差がない…元のデータが大きければ効果ありそう
	my $count = 0;
	my $old_max_value = 0;
	my @ranking = (0, 0); # 順位, ダブリ
	while ($max_ranking > $ranking[0]) {
		last unless @p_ranks;

		# sort の代わりにトップを順次抜き出す
		my $max_value = 0;
		my $max_index = 0;
		for my $index (0 .. $#p_ranks) {
			if ($p_ranks[$index][0] > $max_value) {
				$max_value = $p_ranks[$index][0];
				$max_index = $index;
			}
		}

		# 2位以下が上位と同じ数値ならダブリ数うｐ、違うならダブリ数リセット
		$ranking[1] = $old_max_value > $max_value ? 0 : $ranking[1]+1 if $count > 0;
		$ranking[0] = $count+1 - $ranking[1]; # (インデックス+1) - ダブリ数 = 順位

		# 給料ﾗﾝｷﾝｸﾞ以外の1位のプレイヤーに No.1 熟練付与
		if ($status ne 'sal' && $ranking[0] == 1) {
			my $no1_name = $p_ranks[$max_index][1];
			$no1_name =~ s/\s.*?から最も奪う$//;
			my $n_id = unpack 'H*', $no1_name;
			open my $ufh, ">> $userdir/$n_id/ex_c.cgi";
			print $ufh "no1_c<>1<>\n";
			close $ufh;
		}

		push(@line, join('<>', @{splice(@p_ranks, $max_index, 1)})."\n");
		$count++;
		$old_max_value = $max_value;
	}

=pod
	if (@p_ranks) {
		# sortで1行にできるけど配列の全要素を操作せずにﾗﾝｸｲﾝするﾌﾟﾚｲﾔｰだけをﾋﾟｯｸする↑の方が速い
		@p_ranks = sort {$b->[0] <=> $a->[0]} @p_ranks;

		# ﾗﾝｷﾝｸﾞﾃﾞｰﾀの書き込み準備
		my @ranking = (0, 0); # 順位, ダブリ
		for my $count (0 .. $#p_ranks) {
			# 2位以下が上位と同じ数値ならダブリ数うｐ、違うならダブリ数リセット
			$ranking[1] = $p_ranks[$count-1][0] > $p_ranks[$count][0] ? 0 : $ranking[1]+1 if $count > 0;
			$ranking[0] = $count+1 - $ranking[1]; # (インデックス+1) - ダブリ数 = 順位

			# 給料ﾗﾝｷﾝｸﾞ以外の1位のプレイヤーに No.1 熟練付与
			if ($status ne 'sal' && $ranking[0] == 1) {
				my $no1_name = $p_ranks[0][1];
				$no1_name =~ s/\s.*?から最も奪う$//;
				my $n_id = unpack 'H*', $no1_name;
				open my $ufh, ">> $userdir/$n_id/ex_c.cgi";
				print $ufh "no1_c<>1<>\n";
				close $ufh;
			}

			push @line, "$p_ranks[$count][0]<>$p_ranks[$count][1]<>$p_ranks[$count][2]\n";
			last if $ranking[0] >= $max_ranking; # 順位が $max_ranking 以上になったらお終い
		}
	}
=cut
	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	print $fh @line;
	close $fh;
}

