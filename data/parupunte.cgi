#=================================================
# ﾊﾟﾙﾌﾟﾝﾃ
#=================================================
# ◎追加/削除/変更/並び替え可
@effects = (
	#処理
	sub{
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使う声が空しく響いた</b>");
	},
	sub{
		$y{country} = int(rand($w{country}));
		&add_prisoner;
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使い、現れた魔物によって連れ去られた</b>");
	},
	sub{
		if($w{world} eq $#world_states - 5 || $w{world} eq $#world_states - 4 || $w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || $w{world} eq $#world_states - 1 || $w{world} eq $#world_states){
			&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使う声が空しく響いた</b>");
		}else {
			$w{world} = int(rand(@world_states-6));
			&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使い、世界情勢が変化した</b>");
			&write_cs;
		}
	},
	sub{
	 	my %sames;
		for my $country (0..$w{country}){
			open my $fh, "< $logdir/$country/member.cgi";
			while (my $player = <$fh>) {
				$player =~ tr/\x0D\x0A//d;
 
				# 同じ名前の人が複数いる場合
				next if ++$sames{$player} > 1;
 
				&regist_you_data($player,'silent_time',$time+600);
				&regist_you_data($player,'silent_kind',0);
			}
			close $fh;
		}
		$m{silent_time} = $time+600;
		$m{silent_kind} = 0;
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うとどこからともなく寡黙な魔人現れた</b>");
	},
	sub{
		require './lib/shopping_offertory_box.cgi';
		&get_god_item(0);
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うと笑いながら神様が現れた</b>");
	},
	sub{
		my %sames;
		open my $fh, "< $logdir/$m{country}/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;
 
			# 同じ名前の人が複数いる場合
			next if ++$sames{$player} > 1;
 
			&regist_you_data($player,'silent_time',$time+600);
			&regist_you_data($player,'silent_kind',int(rand(3)+1));
		}
		close $fh;
		$m{silent_time} = $time+600;
		$m{silent_kind} = int(rand(3)+1);
		&mes_and_world_news("<b>ﾏｲｺｫ！＠$cs{name}[$m{country}]</b>");
	},
	sub{
		for my $i (1..$w{country}){
			for my $k ('food','money','soldier'){
				$cs{$k}[$i] += int($cs{$k}[$i] * (-0.2+rand(0.4)));
			}
		}
		&write_cs;
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うと死霊の騎士が全国の資源をめちゃくちゃにしていった</b>");
	},
	sub{
		my $n = int(rand(5)+2);
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うと地中から邪神の大群が現れた</b>");
		&disaster for 0..$n;
		&write_cs;
	},
	sub{
		my %sames;
		for my $i (0..$w{country}) {
			open my $fh, "< $logdir/$i/member.cgi";
			while (my $player = <$fh>) {
				$player =~ tr/\x0D\x0A//d;
 
				# 同じ名前の人が複数いる場合
				next if ++$sames{$player} > 1;
 
				&regist_you_data($player,'silent_time',$time+600);
				&regist_you_data($player,'silent_kind',int(rand(3)+1));
			}
			close $fh;
		}
		$m{silent_time} = $time+600;
		$m{silent_kind} = int(rand(3)+1);
		&mes_and_world_news("<b>We are the WORLD!!!!</b>");
	},
	sub{
		my @rest_days = (1, 3, 7, 10);
		my $n = $rest_days[int(rand(@rest_days))];
		$w{limit_time} = $time + 3600 * 24 * $n;
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うと毎日がエブリデイになった（統一期限残り$n日）</b>");
		&write_cs;
	},
	sub{
		my @item_list = ();
		my $roulette = 0;
		open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
		while (my $line = <$fh>) {
			my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;

			# 商品がない店は非表示
			my $shop_id = unpack 'H*', $name;
			next unless -s "$userdir/$shop_id/shop.cgi";

			if (-s "$userdir/$shop_id/shop.cgi") {
				open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_nameの商品が読み込めません");
				while (my $iline = <$ifh>) {
					my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
					$roulette += $price;
					push @item_list, "$no<>$roulette<>$name<>\n";
				}
				close $ifh;
			}
		}
		close $fh;
		
		my $target = int(rand($roulette));
		my $tline;
		for my $item_line (@item_list){
			my($no, $roulette, $name) = split /<>/, $item_line;
			if($target <= $roulette){
				$tline = $item_line;
				last;
			}
		}
		
		my($t_no, $roulette, $name) = split /<>/, $tline;
		my $shop_id = unpack 'H*', $name;
		if (-f "$userdir/$shop_id/shop.cgi") {
			my $is_find    = 0;
			my $is_rewrite = 0;
			my @lines = ();
			open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("商品ﾘｽﾄが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
				
				if ($no eq $t_no) {
					my $sell_id = int(rand(1000)+1);
					
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, $sell_id);
					$is_rewrite = 1;
				}
				else {
					push @lines, $line;
				}
			}
			if ($is_rewrite) {
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
			}
			close $fh;
		}
		
 		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うとあわてんぼうのサンタクロースが現れた</b>");
 	},
	sub{
		my %sames;
		for my $country (0..$w{country}){
			open my $fh, "< $logdir/$country/member.cgi";
			while (my $player = <$fh>) {
				$player =~ tr/\x0D\x0A//d;
 
				# 同じ名前の人が複数いる場合
				next if ++$sames{$player} > 1;
 
				my %datas = &get_you_datas($player);
				if ($datas{shogo} && $datas{shogo_t} eq ''){
					my $t_shogo = $datas{shogo};
					$t_shogo .= '(笑)';
					&regist_you_data($player,'shogo',$t_shogo);
					&regist_you_data($player,'shogo_t',$datas{shogo});
					&regist_you_data($player,'trick_time',$time + 3600);
				}
			}
			close $fh;
		}
		&mes_and_world_news("<b>ｗｗｗｗｗ$pets[$m{pet}][1]★$m{pet_c}をｗｗ使うとブフォｗｗｗｗｗｗ</b>");
	},
	sub{
		if($m{country}){
			my %sames;
			open my $fh, "< $logdir/$m{country}/member.cgi";
			while (my $player = <$fh>) {
				$player =~ tr/\x0D\x0A//d;
				# 同じ名前の人が複数いる場合
				next if ++$sames{$player} > 1;
				&regist_you_data($player,'next_salary',$time);
			}
			close $fh;
			$m{next_salary} = $time;
			&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使い$cs{name}[$m{country}]の国民はボーナスをもらった</b>");
		}else {
			&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使う声が空しく響いた</b>");
		}
	},
	sub{
		my %sames;
		for my $country (0..$w{country}){
			open my $fh, "< $logdir/$country/member.cgi";
			while (my $player = <$fh>) {
				$player =~ tr/\x0D\x0A//d;
 
				# 同じ名前の人が複数いる場合
				next if ++$sames{$player} > 1;
 
#				my %datas = &get_you_datas($player);
#				&regist_you_data($player,'lib','');
#				&regist_you_data($player,'wt',0);
#				&regist_you_data($player,'tp',0);
#				&regist_you_data($player,'turn',0);
#				&regist_you_data($player,'stock',0);
#				&regist_you_data($player,'value',0);
				my @data = (
					['lib', ''],
					['wt', 0],
					['tp', 0],
					['turn', 0],
					['stock', 0],
					['value', 0]
				);
				&regist_you_array($player, @data);
			}
			close $fh;
		}
		for my $i (1..$w{country}){
			$cs{is_die}[$i] = 0 if $cs{is_die}[$i] < 2;
			$cs{state}[$i] = 0;
			$cs{tax}[$i] = 1;
			for my $j ($i+1..$w{country}){
				my $p_c_c = "p_${i}_${j}";
				$w{$p_c_c} = 0;
				my $f_c_c = "f_${i}_${j}";
				$w{$f_c_c} = 50;
			}
			open my $fh, "+< $logdir/$i/patrol.cgi" or &error("$logdir/$i/patrol.cgiﾌｧｲﾙが開けません");
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;

		}
		&mes_and_world_news("<b>$pets[$m{pet}][1]★$m{pet_c}を使うと$m{name}のゆびさきからいてつくはどうがほとばしる!!</b>");
		&write_cs;
	},
);


1; # 削除不可
