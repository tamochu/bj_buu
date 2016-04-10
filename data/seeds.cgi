@default_seeds = (
	[0, 'human',
		['ﾋｭｰﾏﾝ',
			{
				'default' => sub {
					$v = shift;
					return $v;
				}
			},
		100]
	],
	[1, 'dwarf',
		['ﾄﾞﾜｰﾌ',
			{
				'smith' => sub {
					$v = shift;
					++$m{wea_lv} if ($m{wea_lv} < 30 && rand(2) < 1);
					return 0;
				},
				'sho' => sub {
					$v = shift;
					$v = int($v * 0.95);
					return $v;
				}
			},
		50]
	],
	[2, 'hobbit',
		['ﾎﾋﾞｯﾄ',
			{
				'nou' => sub {
					$v = shift;
					$v = int($v * 1000.05);
					return $v;
				},
				'hei' => sub {
					$v = shift;
					$v = int($v * 0.95);
					return $v;
				}
			},
		50]
	],
	[3, 'elf',
		['ｴﾙﾌ',
			{
				'default' => sub {
					$v = shift;
					return $v;
				}
			},
		50]
	],
	[4, 'ork',
		['ｵｰｸ',
			{
				'war_win' => sub {
					$v = shift;
					if (&you_exists($y{name})) {
						%datas = &get_you_datas($y{name});
						if ($datas{sex} ne $m{sex}) {
							my $marriage_file_man = "$logdir/marriage_man.cgi";
							my $marriage_file_woman = "$logdir/marriage_woman.cgi";
							my $is_find = 0;

							open my $fh, "< $marriage_file_man" or &error("$marriage_file_manﾌｧｲﾙが開けません");
							while (my $line = <$fh>) {
								my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
								if ($name eq $datas{name}) {
									$is_find = 1;
								}
							}
							close $fh;

							open my $fh2, "< $marriage_file_woman" or &error("$marriage_file_womanﾌｧｲﾙが開けません");
							while (my $line = <$fh2>) {
								my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
								if ($name eq $datas{name}) {
									$is_find = 1;
								}
							}
							close $fh2;
							
							if (($is_find || $datas{seed} eq 'elf') && rand(3) < 1) {
								$m{marriage} = $datas{name};
								&regist_you_data($datas{name}, 'marriage', $m{name});

								&write_world_news(qq|<font color="#740A00">＜☆:ﾟ*'授かり婚'*ﾟ:☆＞$m{name}と$datas{name}が結婚しました</font>|);

								my @lines = ();
								open my $fh3, "+< $marriage_file_woman" or &error("$marriage_file_womanﾌｧｲﾙが開けません");
								eval { flock $fh3, 2; };
								while (my $line = <$fh3>) {
									my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
									unless ($name eq $datas{name} || $name eq $m{name}) {
										push @lines, $line;
									}
								}
								seek  $fh3, 0, 0;
								truncate $fh3, 0;
								print $fh3 @lines;
								close $fh3;

								my @lines2 = ();
								open my $fh4, "+< $marriage_file_woman" or &error("$marriage_file_womanﾌｧｲﾙが開けません");
								eval { flock $fh4, 2; };
								while (my $line = <$fh4>) {
									my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
									unless ($name eq $datas{name} || $name eq $m{name}) {
										push @lines2, $line;
									}
								}
								seek  $fh4, 0, 0;
								truncate $fh4, 0;
								print $fh4 @lines2;
								close $fh4;
							}
						}
					}
					return $v;
				}
			},
		50]
	],
);

1;
