@twitter_bots = (
	sub {
		# ‚à‚µ‚àbot
		return "‚æ‚§AAAA";
	},
	sub {
		# é“`
		return "‚É‚á‚ IBlind Justice\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# é“`2
		my $job_name = $jobs[int(rand(@jobs))][1];
		return "y‹}•åz$job_name\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# é“`3
		return "‚±‚ÌƒQ[ƒ€‚ÅÅ‹­‚Ì‘‚Â‚­‚ë‚¤‚¸\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		require "$datadir/hunting.cgi";
		my $place = int(rand(@places));
		my $filename =  "$logdir/monster/$places[$place][0].cgi";
		
		my $all_skills = 0;
		my $all_self_burning = 0;
		open my $fh, "< $filename" or &error("$filenameÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
		return "ƒAƒŠƒAƒƒZƒ‹ƒo—\\‘z[™ƒ~\nŒ»İ‚Ì$places[$place][2]‚Í$sp“‚ÌƒZƒ‹ƒoŠm—¦‚Å‚·";
	},
	sub {
		# dŠ¯l”bot
		my $i = 0;
		for my $j (1 .. $w{country}) {
			$i += $cs{member}[$j];
		}
		return "Œ»İ‚ÌdŠ¯”‚Í$il‚Å‚·";
	},
	sub {
		# à–¾‘bot
		@strs = (
			"Œo‰cÒ‚ÌŠ‹à‚ªƒ}ƒCƒiƒXA‘—a‹àŠz‚ª100–œG–¢–AŒÚ‹q‚Ì—a‚¯‚½‰ñ”‚ª5‰ñ–¢–‚Å‹âs‚ª’×‚ê‚Ü‚·",
			"Îß¯Îß‚ğŒNå‚ª‚Â‚Æ“ÁêŒø‰Ê‚ğ”­“®‚Å‚«‚é‚æ‚¤‚É‚È‚è‚Ü‚·",
			"ÀŞ°¸×ËŞ¯Ä‚Íš‚ğã‚°‚é‚ÆÁ–Å‚·‚éŠm—¦‚ª‰º‚ª‚è‚Ü‚·",
			"ˆê•”‚ÌÍß¯Ä‚Í¯~‚è‚Ì‚Ù‚±‚ç‚Å‡¬‚·‚é‚±‚Æ‚É‚æ‚Á‚Ä‹­‰»‚Å‚«‚Ü‚·",
			"—A‘—‚ª¬Œ÷‚µ‚½‚Æ‚«‚É‚Í“¯–¿‘‚Æ‚Ì—FD“x‚ª‘å•‚Éã¸‚µ‚Ü‚·",
			"500–œ‚Å“X‚É’u‚¢‚½ƒAƒCƒeƒ€‚Í¤•iˆê——‚ÉÚ‚è‚Ü‚¹‚ñ",
			"‘qŒÉ‚ª”š”­‚µ‚Ä‚¢‚Ä‚à‡¬I—¹‚É‘qŒÉ‚ª”š”­‚µ‚È‚¢‚Ì‚Å‚ ‚ê‚ÎˆêŠ‡‡¬‚Í‚Å‚«‚Ü‚·",
			"–h‹ï‚ğ‚Á‚Ä‚¢‚é‘Šè‚É‘fè‚Å—§‚¿Œü‚©‚¤‚ÆUŒ‚—Í‚ª3Š„‚É‚È‚è‚Ü‚·OO",
			"©•ª‚Ì•Ší‚Æ‘Šè‚Ì–h‹ï‚Ì‘®«‚ªˆê’v‚µ‚½ê‡‚É‚ÍUŒ‚—Í‚ª”¼Œ¸‚µ‚Ü‚·",
			"–\\ŒNE¬“×‚Í’D‘—Í‚ª2.5”{‚É‚È‚è‚Ü‚·",
			"Šv–½‚Í’D‘—Í‚ªÅ‘å7.5”{‚É‚à‚È‚è‚Ü‚·",
			"”’•º‚Í’D‘—Í‚ª1.2”{‚É‚È‚è‚Ü‚·",
			);
		return $strs[int(rand(@strs))];
	},
	sub {
		# •½‹Ï‘Šêbot
		my $this_file = "./html/item_";
		my $num = 0;
		# ƒ‹[ƒvˆ—‚ªƒLƒVƒ‡‚¢‚¯‚Ç‚Ü‚¾ƒtƒ@ƒCƒ‹‚ª‘µ‚Á‚Ä‚È‚¢‚Ì‚Å‚µ‚á[‚È‚¢
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
		open my $fh, "< $this_file" or &error("$this_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		my $item_name = <$fh>;
		my $header = <$fh>;
		while (my $line = <$fh>) {
			my($itime, $ivalue, $itype) = split /,/, $line;
			if ($itype ne "”jŠü“™" && $ivalue > 500) {
				$item_value += $ivalue;
				$item_count++;
			}
		}
		close $fh;

		chomp($item_name);
		$item_value = int($item_value / $item_count) if $item_count;
		if ($item_value <= 500) {
			return "hinenoyaƒ‰¿Ši’²¸‚Ì•ñ\nŒ»İ‚Ì$item_name‚Íƒ^ƒ_“¯‘R‚©Œv‘ª•s”\\‚Å‚·";
		}
		else {
			return "hinenoyaƒ‰¿Ši’²¸‚Ì•ñ\nŒ»İ‚Ì$item_name‚Ì•½‹Ï‘Šê‚Í${item_value}G‚Å‚·";
		}
	},
	sub {
		# V’…“ú‹Lbot
		my $count = 0;
		my @blogs = ();
		open my $fh, "< $logdir/blog_news.cgi" or &error("$logdir/blog_news.cgiÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
		while (my $line = <$fh>) {
			push @blogs, $line;
			$count++;
			last if $count > 9;
		}
		close $fh;

		my $str = $blogs[int(rand(@blogs))];
		$str =~ s|<.*?>(.*?)<a href="(.*?)">(.*?)<.*?(\(.*?\)).*|$1$3 $4\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/$2|g;
		return $str;
	},
);

1;
