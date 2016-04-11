@seed_templates = (
	[0, '”ÉB—Íã¸',
		{
			'fecundity' => 10
		},
		1
	],
	[1, '”ÉB—Í’á‰º',
		{
			'fecundity' => -5
		},
		-1
	],
	[2, '’b–è‰®',
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
	[3, '¤”„‰ºè',
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
	[4, '¤”„ãè',
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
	[5, '”_‹Æ‰ºè',
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
	[6, '”_‹Æãè',
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
	[7, 'í‘ˆŒ™‚¢',
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
	[8, '•º–@‰Æ',
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
	[9, '’Z–½',
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
	[10, '’·–½',
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
	[11, '”sÒ‚ğP‚¤',
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
EOM
		},
		2
	],
	[12, '‹­—~',
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
	[13, 'æ‚è‚±‚Ú‚µ',
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
	[15, 'ˆ«–Ú—§‚¿',
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
	[16, 'ƒiƒ“ƒp',
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
	[17, 'Œû‰ºè',
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
);

1;
