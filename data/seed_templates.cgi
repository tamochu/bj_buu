@seed_templates = (
	[0, '繁殖力上昇',
		{
			'fecundity' => 10
		},
		1
	],
	[1, '繁殖力低下',
		{
			'fecundity' => -5
		},
		-1
	],
	[2, '鍛冶屋',
		{
			'smith' => <<'EOM'
		,'smith' => sub {
			$v = shift;
			++$m{wea_lv} if ($m{wea_lv} < 30 && rand(2) < 1);
			return 0;
		}
EOM
		},
		2
	],
	[3, '商売下手',
		{
			'sho' => <<'EOM'
		,'sho' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[4, '商売上手',
		{
			'sho' => <<'EOM'
		,'sho' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[5, '農業下手',
		{
			'nou' => <<'EOM'
		,'nou' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[6, '農業上手',
		{
			'nou' => <<'EOM'
		,'nou' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[7, '戦争嫌い',
		{
			'hei' => <<'EOM'
		,'hei' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-3
	],
	[8, '兵法家',
		{
			'hei' => <<'EOM'
		,'hei' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		4
	],
	[9, '短命',
		{
			'sedai_lv' => <<'EOM'
		,'sedai_lv' => sub {
			$v = shift;
			$v -= 10;
			return $v;
		}
EOM
		},
		-2
	],
	[10, '長命',
		{
			'sedai_lv' => <<'EOM'
		,'sedai_lv' => sub {
			$v = shift;
			$v += 10;
			return $v;
		}
EOM
		},
		4
	],
	[11, '敗者を襲う',
		{
			'war_win' => <<'EOM'
		,'war_win' => sub {
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
EOM
		},
		2
	],
	[12, '強欲',
		{
			'gou' => <<'EOM'
		,'gou' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[13, '取りこぼし',
		{
			'gou' => <<'EOM'
		,'gou' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[14, '007',
		{
			'cho' => <<'EOM'
		,'cho' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[15, '悪目立ち',
		{
			'cho' => <<'EOM'
		,'cho' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[16, 'ナンパ',
		{
			'sen' => <<'EOM'
		,'sen' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[17, '口下手',
		{
			'sen' => <<'EOM'
		,'sen' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[18, '紅き月',
		{
			'red_moon' => <<'EOM'
		,'red_moon' => sub {
			$v = shift;
			my $mday = (localtime($time))[3];
			if ($mday eq '1' || $mday eq '15') {
				$v = int($v * 1.1);
			}
			return $v;
		}
EOM
		},
		5
	],
	[19, '二枚舌',
		{
			'gik' => <<'EOM'
		,'gik' => sub {
			$v = shift;
			$v += 2;
			return $v;
		}
EOM
		},
		4
	],
);

1;
