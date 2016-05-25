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
			"ﾀﾞｰｸﾗﾋﾞｯﾄは★を上げると消滅する確率が下がります",
			"一部のﾍﾟｯﾄは星降りのほこらで合成することによって強化できます",
			"輸送が成功したときには同盟国との友好度が大幅に上昇します",
			);
		return $strs[int(rand(@strs))];
	},
	sub {
		# 平均相場bot
		my $this_file = "./html/item_";
		my $num = 0;
		# ループ処理がキショいけどまだファイルが揃ってないのでしゃーない
		if (rand(2) < 1) {
			$this_file .= "2_";
			$num = int(rand($#eggs)+1);
			while (!(-e $this_file.$num.".csv")) {
				$num = int(rand($#eggs)+1);
			}
		}
		else {
			$this_file .= "3_";
			$num = int(rand($#pets)+1);
			while (!(-e $this_file.$num.".csv")) {
				$num = int(rand($#pets)+1);
			}
		}
		$this_file .= "$num.csv";

		my $item_value = 0;
		my $item_count = 0;
		open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
		my $item_name = <$fh>;
		my $header = <$fh>;
		while (my $line = <$fh>) {
			my($itime, $ivalue, $itype) = split /,/, $line;
			if ($itype ne "破棄等" && $ivalue > 500) {
				$item_value += $ivalue;
				$item_count++;
			}
		}
		close $fh;

		chomp($item_name);
		$item_value = int($item_value / $item_count) if $item_count;
		if ($item_value <= 500) {
			return "hinenoya＜価格調査の報告\n現在の$item_nameはタダ同然か計測不能\です";
		}
		else {
			return "hinenoya＜価格調査の報告\n現在の$item_nameの平均相場は${item_value}Gです";
		}
	},
);

1;
