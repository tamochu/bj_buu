use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/world_reset.cgi';
#================================================
# 国ﾘｾｯﾄ Created by Merino
#================================================

# 統一難易度：[難しい 60 ～ 40 簡単]
my $game_lv = $config_test ? int(rand(6) + 5) : int( rand(11) + 40 );

# 統一期限(日)
my $limit_touitu_day = int( rand(6)+5 );

# 不倶戴天国名
my $country_name_hug_1 = "たけのこの里";
my $country_name_hug_2 = "きのこの山";

# 三国志国名
my $country_name_san_1 = "魏";
my $country_name_san_2 = "呉";
my $country_name_san_3 = "蜀";

#================================================
# 期日が過ぎた場合
#================================================
sub time_limit  {
	if ($w{world} eq $#world_states-5) {
		my $strongest_country = 0;
		my $max_value = 0;
		for my $i (1 .. $w{country}) {
			if ($cs{strong}[$i] > $max_value) {
				$strongest_country = $i;
				$max_value = $cs{strong}[$i];
			}
		}
		&write_world_news("<b>$world_name大陸を全土にわたる国力競争は$cs{name}[$strongest_country]の勝利になりました</b>");
		&write_legend('touitu', "$world_name大陸を全土にわたる国力競争は$cs{name}[$strongest_country]の勝利になりました");
		$w{win_countries} = $strongest_country;
	} else {
		&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
		&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");
		$w{win_countries} = '';
	}

	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $wline;
	$wline = <$fh>;
	my @old_worlds = split /<>/, $wline;
	close $fh;
	my @next_worlds;
	my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
	for my $new_v (@new_worlds){
		my $old_year = 0;
		my $old_flag = 0;
		for my $o (@old_worlds){
			last if $old_year > 10;
			if ($new_v == $o){
				$old_flag = 1;
				last;
			}
			$old_year++;
		}
		push @next_worlds, $new_v unless $old_flag;
	}
	unless ($w{year} =~ /6$/ || $w{year} =~ /0$/){
		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
	}
	&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>") unless $w{year} =~ /5$/ || $w{year} =~ /9$/;
	my $migrate_type = &reset;
	
	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$nline\n";
	close $fh;
	
	if ($w{world} eq '0') { # 平和
		$w{reset_time} += $config_test ? 0 : 3600 * 12;
	}
	elsif ($w{world} eq '6') { # 結束
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# 奇数の場合は一番国は除く
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	elsif ($w{world} eq '18') { # 殺伐
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states-4) { # 英雄
		$w{game_lv} += 20;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states-2) { # 不倶戴天
		$w{game_lv} = 99;
		if ($cs{name}[$w{country}-1] ne $country_name_hug_1 && $cs{name}[$w{country}] ne $country_name_hug_2) {
			$w{country} += 2;
			my $max_c = int($w{player} / 2) + 3;
			for my $i ($w{country}-1..$w{country}){
				mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
				for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
					my $output_file = "$logdir/$i/$file_name.cgi";
					next if -f $output_file;
					open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
					close $fh;
					chmod $chmod, $output_file;
				}
				for my $file_name (qw/leader member/) {
					my $output_file = "$logdir/$i/$file_name.cgi";
					open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
					close $fh;
					chmod $chmod, $output_file;
				}
				&add_npc_data($i);
				# create union file
				for my $j (1 .. $i-1) {
					my $file_name = "$logdir/union/${j}_${i}";
					$w{ "f_${j}_${i}" } = -99;
					$w{ "p_${j}_${i}" } = 2;

					next if -f "$file_name.cgi";
					open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
					close $fh;
					chmod $chmod, "$file_name.cgi";
					open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
					close $fh2;
					chmod $chmod, "${file_name}_log.cgi";
					open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
					close $fh3;
					chmod $chmod, "${file_name}_member.cgi";
				}
				unless (-f "$htmldir/$i.html") {
					open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
					close $fh_h;
				}
				$cs{name}[$i]     = $i == $w{country} ? $country_name_hug_1 : $country_name_hug_2;
				$cs{color}[$i]    = $i == $w{country} ? '#ff0000':'#ffffff';
				$cs{member}[$i]   = 0;
				$cs{win_c}[$i]    = 999;
				$cs{tax}[$i]      = 99;
				$cs{strong}[$i]   = 75000;
				$cs{food}[$i]     = 0;
				$cs{money}[$i]    = 0;
				$cs{soldier}[$i]  = 0;
				$cs{state}[$i]    = 0;
				$cs{capacity}[$i] = $max_c;
				$cs{is_die}[$i]   = 0;
				my @lines = &get_countries_mes();
				if ($w{country} > @lines - 2) {
					open my $fh9, ">> $logdir/countries_mes.cgi";
					print $fh9 "<>$default_icon<>\n";
					print $fh9 "<>$default_icon<>\n";
					close $fh9;
				}
			}
		}
		$migrate_type = festival_type('kouhaku', 1);

		for my $i (1 .. $w{country}-2) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-2) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	elsif ($w{world} eq $#world_states-3) { # 三国志
		$w{game_lv} = 99;
		if ($cs{name}[$w{country} - 2] ne $country_name_san_1 && $cs{name}[$w{country} - 1] ne $country_name_san_2 && $cs{name}[$w{country}] ne $country_name_san_3) {
			$w{country} += 3;
			my $max_c = int($w{player} / 3) + 3;
			for my $i ($w{country}-2..$w{country}){
				mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
				for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
					my $output_file = "$logdir/$i/$file_name.cgi";
					next if -f $output_file;
					open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
					close $fh;
					chmod $chmod, $output_file;
				}
				for my $file_name (qw/leader member/) {
					my $output_file = "$logdir/$i/$file_name.cgi";
					open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
					close $fh;
					chmod $chmod, $output_file;
				}
				&add_npc_data($i);
				# create union file
				for my $j (1 .. $i-1) {
					my $file_name = "$logdir/union/${j}_${i}";
					$w{ "f_${j}_${i}" } = -99;
					$w{ "p_${j}_${i}" } = 2;

					next if -f "$file_name.cgi";
					open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
					close $fh;
					chmod $chmod, "$file_name.cgi";
					open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
					close $fh2;
					chmod $chmod, "${file_name}_log.cgi";
					open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
					close $fh3;
					chmod $chmod, "${file_name}_member.cgi";
				}
				unless (-f "$htmldir/$i.html") {
					open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
					close $fh_h;
				}
				$cs{name}[$i]     = $i == $w{country}-2 ? $country_name_san_1:
									$i == $w{country}-1 ? $country_name_san_2:
														$country_name_san_3;
				$cs{color}[$i]    = $i == $w{country}-2 ? '#4444ff':
									$i == $w{country}-1 ? '#ff4444':
														'#44ff44';
				$cs{member}[$i]   = 0;
				$cs{win_c}[$i]    = 999;
				$cs{tax}[$i]      = 99;
				$cs{strong}[$i]   = 50000;
				$cs{food}[$i]     = 0;
				$cs{money}[$i]    = 0;
				$cs{soldier}[$i]  = 0;
				$cs{state}[$i]    = 0;
				$cs{capacity}[$i] = $max_c;
				$cs{is_die}[$i]   = 0;
				my @lines = &get_countries_mes();
				if ($w{country} > @lines - 3) {
					open my $fh9, ">> $logdir/countries_mes.cgi";
					print $fh9 "<>$default_icon<>\n";
					print $fh9 "<>$default_icon<>\n";
					print $fh9 "<>$default_icon<>\n";
					close $fh9;
				}
			}
		}
		$migrate_type = festival_type('sangokusi', 1);
		for my $i (1 .. $w{country}-3) {
			$cs{strong}[$i]   = 0;
			$cs{food}[$i]     = 0;
			$cs{money}[$i]    = 0;
			$cs{soldier}[$i]  = 0;
			$cs{state}[$i]    = 0;
			$cs{capacity}[$i] = 0;
			$cs{is_die}[$i]   = 1;

			for my $j ($i+1 .. $w{country}-3) {
				$w{ "f_${i}_${j}" } = -99;
				$w{ "p_${i}_${j}" } = 2;
			}

			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	elsif ($w{world} eq $#world_states-5) { # 拙速
		$migrate_type = festival_type('sessoku', 1);
	}
	elsif ($w{world} eq $#world_states-1) { # 混乱
		$migrate_type = festival_type('konran', 1);
	}
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	&write_cs;
	&player_migrate($migrate_type);
}

#================================================
# 国ﾃﾞｰﾀﾘｾｯﾄ処理
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});
	
	my $migrate_type = 0;
	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
	}
	
	# 世界情勢 暗黒解除
	if ($w{year} =~ /6$/) {
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
			$w{world} = int(rand($#world_states-5));
		} else {
			require './lib/vs_npc.cgi';
			&delete_npc_country;
			$w{world} = int(rand($#world_states-5));
		}
	}
	# 世界情勢 混乱解除
	if ($w{year} =~ /0$/) {
		if($w{year} % 40 == 0){#不倶戴天
			$migrate_type = festival_type('kouhaku', 0);
			$w{country} -= 2;
		}elsif($w{year} % 40 == 20){# 三国志
			$migrate_type = festival_type('sangokusi', 0);
			$w{country} -= 3;
		}elsif($w{year} % 40 == 10){# 拙速
			$migrate_type = festival_type('sessoku', 0);
		}else {#混乱
			$migrate_type = festival_type('konran', 0);
		}
		$w{world} = int(rand($#world_states-5));
	}
	# 仕官できる人数
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);
	
	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;
	if($w{year} % 40 == 10){
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $time + 3600 * 36;
		$w{game_lv} = 99;
	}
	
	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# 統一国の場合はNPC弱体
		if($w{year} % 40 == 10){
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		} else {
			$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
			$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		}
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			if ($cs{ceo}[$i]) {
				my $n_id = unpack 'H*', $cs{ceo}[$i];
				open my $fh, ">> $userdir/$n_id/ex_c.cgi";
				print $fh "ceo_c<>1<>\n";
				close $fh;
			}
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
		
		if ($w{year} % $reset_daihyo_cycle_year == 0) {
			for my $k (qw/war dom pro mil/) {
				my $kc = $k . "_c";
				next if $cs{$k}[$i] eq '';
				my $trick_id = unpack 'H*', $cs{$k}[$i];
				my %datas = &get_you_datas($trick_id, 1);
				&regist_you_data($cs{$k}[$i], $kc, int($datas{$kc} * 0.5));
				
				$cs{$k}[$i] = '';
				$cs{$kc}[$i] = 0;
				
			}
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>各国の$e2j{ceo}の任期が満了となりました</b>");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>各国の代表\者の任期が満了となりました</b>");
	}
	
	# 世界情勢 暗黒突入
	if ($w{year} =~ /6$/) {
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
			$w{world} = $#world_states-4;
		} else {
			require './lib/vs_npc.cgi';
			&add_npc_country;
		}
	}
	# 世界情勢 混乱突入
	if ($w{year} =~ /0$/) {
		if ($w{year} % 40 == 0){ # 不倶戴天
			$w{world} = $#world_states-2;
		} elsif ($w{year} % 40 == 20) { # 三国志
			$w{world} = $#world_states-3;
		} elsif ($w{year} % 40 == 10) { # 拙速
			$w{world} = $#world_states-5;
		} else { # 混乱
			$w{world} = $#world_states-1;
		}
		
		&wt_c_reset;
	}
	
	# 1000年デフォルト
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}
	
	&write_cs;
	return $migrate_type;
}

sub player_migrate {
	my $type = shift;

	if ($type == &festival_type('kouhaku', 0)) {# 不倶戴天解除
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				require './lib/shopping_offertory_box.cgi';
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(笑)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# ネバラン送り
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;
		
		# 国フォルダ削除
		for my $i ($w{country}+2, $w{country}+1) {
			my $from = "$logdir/$i";
			my $num = rmtree($from);
			
			my @lines = ();
			open my $fh, "+< $logdir/countries_mes.cgi";
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
			}
			pop @lines while @lines > $w{country} + 1;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
		
		$w{country} -= 2;
		
		# 国データ復旧
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("国ﾃﾞｰﾀが読み込めません");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			++$i;
		}
		close $fh;
	}
	elsif ($type == &festival_type('sangokusi', 0)){# 三国志解除
		require "./lib/move_player.cgi";
		require "./lib/shopping_offertory_box.cgi";
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(笑)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# ネバラン送り
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;
		
		# 国フォルダ削除
		for my $i ($w{country}+3, $w{country}+2, $w{country}+1) {
			my $from = "$logdir/$i";
			my $num = rmtree($from);
			
			my @lines = ();
			open my $fh, "+< $logdir/countries_mes.cgi";
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
			}
			pop @lines if @lines > $w{country} + 1;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
		
		$w{country} -= 3;
		
		# 国データ復旧
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("国ﾃﾞｰﾀが読み込めません");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			++$i;
		}
		close $fh;
	}
	elsif ($type == &festival_type('konran', 0) || $type == &festival_type('sessoku', 0)) {#混乱解除
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			if($you_datas{name} eq $m{name}){
				&move_player($m{name}, $m{country}, 0);
				$m{country} = 0;
				&write_user;
			}
			&move_player($you_datas{name}, $you_datas{country}, 0);
			&regist_you_data($you_datas{name}, 'country', 0);

			my($c1, $c2) = split /,/, $w{win_countries};
			if ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('konran', 1) || $type == &festival_type('sessoku', 1)) {# 混乱設定
		# 一旦ネバラン送り
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			next if $you_datas{shuffle};
			
			if($you_datas{name} eq $m{name}){
				&move_player($m{name}, $m{country}, 0);
				$m{country} = 0;
				&write_user;
			}
			&move_player($you_datas{name}, $you_datas{country}, 0);
			&regist_you_data($you_datas{name}, 'country', 0);
		}
		closedir $dh;
		
		# 振り分け
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand($w{country}) + 1);
			for my $cj (1..$w{country}) {
				if ($cs{member}[$j] > $cs{member}[$cj] + 2) {
					$j = $cj;
				}
			}
			&move_player($you_datas{name}, $you_datas{country}, $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $j;
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $j);
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('kouhaku', 1)) {# 不倶戴天設定
		# バックアップ作成
		for my $i (0 .. $w{country} - 2) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
		
		require "./lib/move_player.cgi";
		@sedais=([0, 0],[0, 0],[0, 0],[0, 0]);
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand(2));
			my $s;
			if($m{sedai} <= 5){
				$s = 0;
			}elsif($m{sedai} <= 10){
				$s = 1;
			}elsif($m{sedai} <= 15){
				$s = 2;
			}else{
				$s = 3;
			}
			for my $cj (0..1) {
				if ($sedais[$s][$j] > $sedais[$s][$cj] + 2) {
					$j = $cj;
				}
			}
			++$sedais[$s][$j];
			&move_player($you_datas{name}, $you_datas{country}, $w{country} - $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $w{country} - $j;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c_t"} = $m{$k."_c"};
					$m{$k."_c"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $w{country} - $j);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c_t", $you_datas{$k."_c"});
					&regist_you_data($you_datas{name}, $k."_c", 0);
				}
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('sangokusi', 1)) {# 三国志設定
		# バックアップ作成
		for my $i (0 .. $w{country} - 3) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
		
		require "./lib/move_player.cgi";
		@sedais=([0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]);
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand(3));
			my $s;
			if($m{sedai} <= 5){
				$s = 0;
			}elsif($m{sedai} <= 10){
				$s = 1;
			}elsif($m{sedai} <= 15){
				$s = 2;
			}else{
				$s = 3;
			}
			for my $cj (0..2) {
				if ($sedais[$s][$j] > $sedais[$s][$cj] + 2) {
					$j = $cj;
				}
			}
			++$sedais[$s][$j];
			&move_player($you_datas{name}, $you_datas{country}, $w{country} - $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $w{country} - $j;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c_t"} = $m{$k."_c"};
					$m{$k."_c"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $w{country} - $j);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c_t", $you_datas{$k."_c"});
					&regist_you_data($you_datas{name}, $k."_c", 0);
				}
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('dokuritu', 0)) {# 独立解除
		require "./lib/move_player.cgi";
		for my $i (1..$w{country}) {
			my @names = &get_country_members($i);
			for my $name (@names) {
				$name =~ tr/\x0D\x0A//d;
				if($name eq $m{name}){
					&move_player($m{name}, $i, 0);
					$m{country} = 0;
					&write_user;
				}
				my %you_datas = &get_you_datas($name);
				&move_player($name, $i, 0);
				&regist_you_data($name, 'country', 0);

				my($c1, $c2) = split /,/, $w{win_countries};
				if ($c1 eq $i || $c2 eq $i) {
					require './lib/shopping_offertory_box.cgi';
					if ($cs{ceo}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(7, $cs{ceo}[$you_datas{country}]) for (1..2);
					}
					my $n_id = unpack 'H*', $name;
					open my $fh, ">> $userdir/$n_id/ex_c.cgi";
					print $fh "fes_c<>1<>\n";
					close $fh;
					
					&send_item($name, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
			}
		}
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("国ﾃﾞｰﾀが読み込めません");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			$w{country} = $i;
			++$i;
		}
		close $fh;
		
		&cs_data_repair;
	}
	elsif ($type == &festival_type('dokuritu', 1)) {# 独立設定
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
	}
	&cs_data_repair;
}
sub wt_c_reset{
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %you_datas = &get_you_datas($pid, 1);
		
		if ($you_datas{name} eq $m{name}){
			$m{wt_c_latest} = $m{wt_c};
			$m{wt_c} = 0;
			&write_user;
		} else {
			&regist_you_data($you_datas{name}, "wt_c_latest", $you_datas{wt_c});
			&regist_you_data($you_datas{name}, "wt_c", 0);
		}
	}
	closedir $dh;
}

sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]属性[1]武器No	[2]必殺技
		['無', [0],			[61..65],],
		['剣', [1 .. 5],	[1 .. 5],],
		['槍', [6 ..10],	[11..15],],
		['斧', [11..15],	[21..25],],
		['炎', [16..20],	[31..35],],
		['風', [21..25],	[41..45],],
		['雷', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) 亀の家庭医学(NPC) pigure(NPC) ウェル(NPC) vipqiv(NPC) DT(NPC) ハル(NPC) アシュレイ(NPC) ゴミクズ(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}

1; # 削除不可
