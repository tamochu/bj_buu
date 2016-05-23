@twitter_bots = (
	sub {
		# もしもbot
		return "よぉ、、、、";
	},
	sub {
		# 宣伝
		return "にゃあ鯖Blind Justice\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# 宣伝2
		my $job_name = $jobs[int(rand(@jobs))][1];
		return "【急募】$job_name\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# 宣伝3
		return "このゲームで最強の国つくろうず\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		require "$datadir/hunting.cgi";
		my $place = int(rand(@places));
		my $filename =  "$logdir/monster/$places[$place][0].cgi";
		
		my $all_skills = 0;
		my $all_self_burning = 0;
		open my $fh, "< $filename" or &error("$filenameﾌｧｲﾙが開けません");
		while (my $line = <$fh>) {
			my @datas = split /<>/, $line;
			my $i = 0;
			my %y = ();
			for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
				$y{$k} = $datas[$i];
				++$i;
			}
			my $skill_st = 0;
			my $si = 0;
			my $skill_str = '';
			for my $skill (split /,/, $y{skills}) {
				$si++;
				if ($skills[$skill][2] eq $weas[$y{wea}][2]) {
					$skill_st += $skills[$skill][7];
					if ($skill eq '32') {
						$all_self_burning++;
					}
				} else {
					$skill_st += $skills[0][7];
				}
			}
			for (my $j = $si; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			$all_skills += 5;
		}
		close $fh;
		
		my $sp = int((10 * $all_self_burning / $all_skills) + rand(4) - 2) * 10;
		return "アリア＜セルバ予\想ー☆ミ\n現在の$places[$place][2]は$sp％のセルバ確率です";
	},
	sub {
		# 仕官人数bot
		my $i = 0;
		for my $j (1 .. $w{country}) {
			$i += $cs{member}[$j];
		}
		return "現在の仕官数は$i人です";
	},
	sub {
		# 説明書bot
		@strs = (
			"経営者の所持金がマイナス、総預金額が100万G未満、顧客の預けた回数が5回未満で銀行が潰れます",
			"ﾎﾟｯﾎﾟを君主が持つと特殊効果を発動できるようになります",
			);
		return $strs[int(rand(@strs))];
	},
);

1;
