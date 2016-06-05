@default_seeds = (
	[0, 'human',
		['Ë­°Ïİ',
			{
				'default' => sub {
					$v = shift;
					return $v;
				}
			},
		100,
		'–³‚µ']
	],
	[1, 'dwarf',
		['ÄŞÜ°Ì',
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
		50,
		'’b–è‰®,¤”„‰ºè']
	],
	[2, 'hobbit',
		['ÎËŞ¯Ä',
			{
				'nou' => sub {
					$v = shift;
					$v = int($v * 1.05);
					return $v;
				},
				'hei' => sub {
					$v = shift;
					$v = int($v * 0.95);
					return $v;
				}
			},
		50,
		'”_‹Æãè,í‘ˆŒ™‚¢']
	],
	[3, 'elf',
		['´ÙÌ',
			{
				'sedai_lv' => sub {
					$v = shift;
					$v += 10;
					return $v;
				}
			},
		50,
		'’·–½']
	],
	[4, 'ork',
		['µ°¸',
			{
				'war_win' => sub {
					$v = shift;
					if (&you_exists($y{name})) {
						%datas = &get_you_datas($y{name});
						if ($datas{sex} ne $m{sex}) {
							my $marriage_file_man = "$logdir/marriage_man.cgi";
							my $marriage_file_woman = "$logdir/marriage_woman.cgi";
							my $is_find = 0;

							open my $fh, "< $marriage_file_man" or &error("$marriage_file_manÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
							while (my $line = <$fh>) {
								my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
								if ($name eq $datas{name}) {
									$is_find = 1;
								}
							}
							close $fh;

							open my $fh2, "< $marriage_file_woman" or &error("$marriage_file_womanÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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

								&write_world_news(qq|<font color="#740A00">ƒ™:ß*'ö‚©‚è¥'*ß:™„$m{name}‚Æ$datas{name}‚ªŒ‹¥‚µ‚Ü‚µ‚½</font>|);

								my @lines = ();
								open my $fh3, "+< $marriage_file_woman" or &error("$marriage_file_womanÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
								open my $fh4, "+< $marriage_file_woman" or &error("$marriage_file_womanÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
		50,
		'”sÒ‚ğP‚¤']
	],
);

1;
