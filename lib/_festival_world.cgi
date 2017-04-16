use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# 祭り情勢の開始・終了で使われるモジュール
# 主な呼び出し元
# ./lib/reset.cgi
#================================================
# 紅白 ｼｬｯﾌﾙ 熟練度ﾊﾞｯｸｱｯﾌﾟ ﾈﾊﾞﾗﾝ行き 熟練度ﾘｽﾄｱ
# 三国志 ｼｬｯﾌﾙ 熟練度ﾊﾞｯｸｱｯﾌﾟ ﾈﾊﾞﾗﾝ行き 熟練度ﾘｽﾄｱ
# 拙速 ﾉｰｼｬｯﾌﾙ ﾈﾊﾞﾗﾝ行き
# 混乱 ｼｬｯﾌﾙ ﾈﾊﾞﾗﾝ行き

#================================================
# 祭り情勢時に追加される国の数・国力・国名・国色の定義
#================================================

if ($config_test) {
	use constant FESTIVAL_COUNTRY_PROPERTY => {
#		'kouhaku' => [2, 1, ["きのこの山", "たけのこの里"], ["#ffffff", "#ff0000"]],
#		'sangokusi' => [3, 1, ["魏", "呉", "蜀"], ["#4444ff", "#ff4444", "#44ff44"]]
		'kouhaku' => [2, 75000, ["きのこの山", "たけのこの里"], ["#ffffff", "#ff0000"]],
		'sangokusi' => [3, 50000, ["魏", "呉", "蜀"], ["#4444ff", "#ff4444", "#44ff44"]]
	};
}

#================================================
# 祭り情勢開始時の国や情勢を設定して始める
#================================================
sub begin_festival_world {
	# 拙速以外の祭り情勢開始時の既存国すべての君主と君主ファイルを初期化
	if ($w{year} % 40 != 10) {
		for my $i (0 .. $w{country}) {
			$cs{old_ceo}[$i] = $cs{ceo}[$i] if $w{year} % 40 != 30; # 紅白・三国志のみ $cs{old_ceo} に退避している
			$cs{ceo}[$i] = '';
			for my $key (qw/war dom mil pro/) {
				$cs{$key}[$i] = '';
				$cs{$key.'_c'}[$i] = 0;
			}
			$cs{member}[$i] = 0;
			open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
			close $fh;
			open my $fh2, "> $logdir/$i/leader.cgi" or &error("$logdir/$i/leader.cgiﾌｧｲﾙが開けません");
			close $fh2;
		}
		&write_cs;
	}

	if ($w{year} % 40 == 0){ # 不倶戴天
		$w{world} = $#world_states-2;
		$w{game_lv} = 99;
		&run_kouhaku(1);
	} elsif ($w{year} % 40 == 20) { # 三国志
		$w{world} = $#world_states-3;
		$w{game_lv} = 99;
		&run_sangokusi(1);
	} elsif ($w{year} % 40 == 10) { # 拙速
		$w{world} = $#world_states-5;
		$w{game_lv} = 99;
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $config_test ? $time: $time + 3600 * 36;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		}
		&run_sessoku(1);
	} else { # 混乱
		$w{world} = $#world_states-1;
		&run_konran(1);
	}
}

#================================================
# 祭り情勢を解除して終える
#================================================
sub end_festival_world {
	if ($w{year} % 40 == 0){ # 不倶戴天
		&run_kouhaku(0);
	} elsif ($w{year} % 40 == 20) { # 三国志
		&run_sangokusi(0);
	} else {
		if ($w{year} % 40 == 10) { # 拙速
			&run_sessoku(0);
		} else { # 混乱
			&run_konran(0);
		}
		# 紅白・三国志は開始時に初期化さえすれば済むが、
		# 拙速・混乱中の君主データなどがあるので終了時にも初期化
		for my $i (1 .. $w{country}) {
			$cs{ceo}[$i] = '';
			for my $key (qw/war dom mil pro/) {
				$cs{$key}[$i] = '';
				$cs{$key.'_c'}[$i] = 0;
			}
			$cs{member}[$i] = 0;
			open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
			close $fh;
			open my $fh2, "> $logdir/$i/leader.cgi" or &error("$logdir/$i/leader.cgiﾌｧｲﾙが開けません");
			close $fh2;
		}
	}
}

#================================================
# 紅白の開始(1)と終了(0)
#================================================
sub run_kouhaku {
	$is_start = shift;

#	require "./lib/move_player.cgi";
	if ($is_start) { # 紅白開始時の処理	
		&add_festival_country('kouhaku');
		&player_shuffle($w{country}-1..$w{country});
	}
	else { # 紅白終了時の処理
		&end_kouhaku_sangokusi('kouhaku');
	}
}

#================================================
# 三国志の開始(1)と終了(0)
#================================================
sub run_sangokusi {
	$is_start = shift;

	require "./lib/move_player.cgi";
	if ($is_start) { # 三国志開始時の処理
		&add_festival_country('sangokusi');
		&player_shuffle($w{country}-2..$w{country});
	}
	else { # 三国志終了時の処理
		&end_kouhaku_sangokusi('sangokusi');
	}
}

# 紅白も三国志も終了時の処理同じ
sub end_kouhaku_sangokusi {
	my $festival_name = shift;

	require "./lib/shopping_offertory_box.cgi";
	my($c1, $c2) = split /,/, $w{win_countries};
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		next unless &you_exists($pid, 1);
		my %you_datas = &get_you_datas($pid, 1);

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
		}

		&move_player2($you_datas{name}, 0);
		# 統一したキャラが敗戦判定になる訳がないので敗戦判定は省略
		if ($you_datas{name} eq $m{name}) { # 対象が自キャラならば
			$m{country} = 0; # 所属国の書き換え
			$y{country} = 0;
			$m{vote} = ''; # 立候補・投票データの初期化

			# 代表熟練度のﾘｽﾄｱ
			for my $k (qw/war dom pro mil/) {
				$m{"${k}_c"} = $m{"${k}_c_t"};
				$m{"${k}_c_t"} = 0;
			}
			&write_user;
		}
		else { # 対象が他キャラならば
			my @data = (
				['country', 0],
				['y_country', 0],
				['vote', ''],
			);

			unless ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				my @data2 = (
					['shogo', "$cs{name}[$you_datas{country}](笑)"],
					['trick_time', $time + 3600 * 24 * 3],
					['shogo_t', ''] # 称号固定はｱﾘﾖｼぐらい？
				);
				push @data, @data2;
			}

			for my $k (qw/war dom pro mil/) {
				my @data3 = (
					["${k}_c", $you_datas{"${k}_c_t"}],
					["${k}_c_t", 0]
				);
				push @data, @data3;
			}

			&regist_you_array($you_datas{name}, @data);
		}
	}
	closedir $dh;

	# 祭り用の国を消して通常既存国をﾘｽﾄｱしてしまうため write_cs 後にさらに cs_data_repair が必要
	&remove_festival_country($festival_name);
	&write_cs;
	&cs_data_repair;
}

#================================================
# 拙速の開始(1)と終了(0)
#================================================
sub run_sessoku {
	$is_start = shift;

	if ($is_start) { # 拙速開始時の処理
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);

			&wt_c_reset(\%m, \%you_datas); # 稼働率ﾗﾝｷﾝｸﾞの更新とﾘｾｯﾄ	
		}
		closedir $dh;
	} # 拙速開始時の処理
	else { # 拙速終了時の処理
		require './lib/shopping_offertory_box.cgi';
		require "./lib/move_player.cgi";
		# 1位国には統一ボーナスと祭り報酬
		# (int(国数/2)+1)位には統一ボーナス
		my @strong_rank = &get_strong_ranking;
		$w{win_countries} = "$strong_rank[0],$strong_rank[1]";

		&write_world_news("<b>$world_name大陸を全土にわたる国力競争は$cs{name}[$strong_rank[0]]と$cs{name}[$strong_rank[1]]の勝利になりました</b>");
		&write_legend('touitu', "$world_name大陸を全土にわたる国力競争は$cs{name}[$strong_rank[0]]と$cs{name}[$strong_rank[1]]の勝利になりました");

#		$cs{strong}[$strong_rank[2]] = 0;
#		$cs{is_die}[$strong_rank[2]] = 3;

		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);

			# 祭り熟練
			if ($strong_rank[0] eq $you_datas{country} || $strong_rank[1] eq $you_datas{country}) {
				# 1位国の代表には祭り報酬
				if ($$strong_rank[0] eq $you_datas{country}) {
					for my $k (qw/war dom pro mil ceo/) {
						if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
							&send_god_item(5, $cs{$k}[$you_datas{country}]);
						}
					}
					&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
			}

			# ネバラン送り
			&move_player2($you_datas{name}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$m{vote} = '';
				&write_user;
			} else {
				my @data = (
					['country', 0],
					['vote', '']
				);
				&regist_you_array($you_datas{name}, @data);
			}

			# 封鎖で使うので残しておいてくだちい
			# ビリの国にいるプレイヤーは適当仕官
			#elsif ($strong_rank[2] eq $p{country}) {
				#my $to_country = 0;
				#do {
					#$to_country = int(rand($w{country}) + 1);
				#} while ($cs{is_die}[$to_country] > 1);

				#&move_player($p{name}, $p{country}, $to_country);
				#if ($p{name} eq $m{name}){
					#$m{country} = $to_country;
					#&write_user;
				#} else {
					#&regist_you_data($p{name}, 'country', $to_country);
				#}
			#}
		}
	} # 拙速終了時の処理
}

#================================================
# 混乱の開始(1)と終了(0)
#================================================
sub run_konran {
	$is_start = shift;

#	require "./lib/move_player.cgi";
	if ($is_start) { # 混乱開始時の処理
		&player_shuffle(1..$w{country});
	} # 混乱開始時の処理
	else { # 混乱終了時の処理
		my($c1, $c2) = split /,/, $w{win_countries}; # 統一国の取得
		opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless -f "$userdir/$pid/user.cgi";
			my %you_datas = &get_you_datas($pid, 1);

			&move_player2($you_datas{name}, 0);
			if ($you_datas{name} eq $m{name}) { # 対象が自キャラならば
				$m{country} = 0; # 所属国の書き換え
				$m{vote} = ''; # 立候補・投票データの初期化
				&write_user;
			}
			else { # 対象が他キャラならば
				my @data = (
					['country', 0],
					['vote', '']
				);
				&regist_you_array($you_datas{name}, @data);
			}

			# 統一国にいた人に卵
			if ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}
		}
		closedir $dh;
		&write_cs;
	} # 混乱終了時の処理
}

#================================================
# 指定された祭り情勢用の国を追加し、それ以外の国をﾊﾞｯｸｱｯﾌﾟ
# 追加される国の情報は FESTIVAL_COUNTRY_PROPERTY で定義しておく
#================================================
sub add_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	$w{country} += $country_num;
	my $max_c = int($w{player} / $country_num) + 3;
	for my $i ($w{country}-($country_num-1)..$w{country}){
		mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot_log patrol prison prison_member prisoner violator leader member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
#			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
			close $fh;
			chmod $chmod, $output_file;
		}
		# 国庫は1行目が設定なので予め書き込んでおかないと国庫にぶち込んだ1個目のアイテムが消失してしまう
		my $output_file = "$logdir/$i/depot.cgi";
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		print $fh "1<>1<>1世代Lv1以上が利用できます<>\n";
		close $fh;
		chmod $chmod, $output_file;

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

		my $num = $i-($w{country}+1-$country_num);
		$cs{name}[$i]     = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[2][$num];
		$cs{color}[$i]    = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[3][$num];
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 999;
		$cs{tax}[$i]      = 99;
		$cs{strong}[$i]   = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[1];
		$cs{food}[$i]     = $config_test ? 999999 : 0;
		$cs{money}[$i]    = $config_test ? 999999 : 0;
		$cs{soldier}[$i]  = $config_test ? 999999 : 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = $max_c;
		$cs{is_die}[$i]   = 0;

		require './lib/_rampart.cgi';
		$cs{barrier}[$i]  = &get_init_barrier;
	}

	for my $i (1 .. $w{country}-$country_num) {
		$cs{strong}[$i]   = 0;
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = 0;
		$cs{is_die}[$i]   = 1;

		for my $j ($i+1 .. $w{country}-$country_num) {
			$w{ "f_${i}_${j}" } = -99;
			$w{ "p_${i}_${j}" } = 2;
		}
	}

	my @lines = &get_countries_mes();
	if ($w{country} > @lines) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "<>non_mark.gif<>\n" for 1..$country_num;
		close $fh9;
	}

	# バックアップ作成
	for my $i (0 .. $w{country} - $country_num) {
		my $from = "$logdir/$i";
		my $backup = $from . "_backup";
		rcopy($from, $backup);
	}
	my $from = "$logdir/countries.cgi";
	my $backup = "$logdir/countries_backup.cgi";
	rcopy($from, $backup);
}

#================================================
# 指定された祭り情勢用の国を削除し、それ以外の国をﾘｽﾄｱ
# 削除される国の情報は FESTIVAL_COUNTRY_PROPERTY で定義しておく
#================================================
sub remove_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	# 国フォルダ削除
	for (my $i = $w{country}; $i > $w{country}+1-$country_num; $i--) { # 既存国+暗黒-祭り国
		my $from = "$logdir/$i";
		my $num = rmtree($from);
	}
	$w{country} -= $country_num;

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

#================================================
# 稼働率ﾗﾝｷﾝｸﾞの更新とﾘｾｯﾄ（祭り突入時の10年毎）
#================================================
sub wt_c_reset {
	my ($m, $you_datas) = @_;
	if ($$you_datas{name} eq $$m{name}){
		$$m{wt_c_latest} = $$m{wt_c};
		$$m{wt_c} = 0;
		&write_user;
	} else {
		my @data = (
			['wt_c_latest', $$you_datas{wt_c}],
			['wt_c', 0]
		);
		&regist_you_array($$you_datas{name}, @data);
	}
}

#================================================
# プレーヤーシャッフル
# 稼働率をもとに振り分ける。
#================================================
sub player_shuffle {
	my @countries = @_;
	
	for my $i (0..$#countries){
		my $j = int(rand(@countries));
		my $temp = $countries[$i];
 		$countries[$i] = $countries[$j];
 		$countries[$j] = $temp;
	}
	
	my %country_num = ();
	for my $c ($countries) {
		$country_num{$c} = 0;
	}
	
	# ユーザー一覧取得
	my @player_line = ();
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		next unless &you_exists($pid, 1);
		my %you_datas = &get_you_datas($pid, 1);

		&wt_c_reset(\%m, \%you_datas); # 稼働率ﾗﾝｷﾝｸﾞの更新とﾘｾｯﾄ

		# 混乱時シャッフルされないで true
		# 紅白・三国志は関係ないので処理しない
		# シャッフルされないで居残ってる人をプラスして player_line に足さない
		if ($you_datas{shuffle} && $w{world} == $#world_states-1) {
			# member.cgiを初期化しているのでシャッフル前の国に再度飛ばさないとデータの不一致が起きる
			&move_player2($you_datas{name}, $you_datas{country});
			if ($you_datas{country}) { # 仕官していたなら
				$country_num{$you_datas{country}}++;
				next;
			}
#			my $c_find = 0;
#			if ($you_datas{country}) { # 仕官しているなら
#				for my $c (@countries) {
#					if ($c eq $you_datas{country}) {
#						$country_num{$c}++;
#						$c_find = 1;
#					}
#				}
#			}
#			if ($c_find) {
#				next;
#			}
		}
		
		push @player_line, "$you_datas{name}<>$you_datas{wt_c_latest}<>\n";
	}
	closedir $dh;
	
	@player_line = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ] } @player_line;
	
	my $updown = 1;
	my $index = 0;
	my $round = 0;
	my @new_line = ();
	my $mc = @countries;
	for my $pl (@player_line) {
		my $c = $countries[$index];
		my($pname, $pw) = split /<>/, $pl;
		push @new_line, "$pname<>$c<>\n";
		$country_num{$c}++;
		while (1) {
			$index += $updown;
			if ($index < 0) {
				$index = 0;
				$updown = 1;
				$round++;
			} elsif ($index >= $mc) {
				$index = $mc - 1;
				$updown = -1;
				$round++;
			}
			if ($country_num{$countries[$index]} <= $round) {
				last;
			}
		}
	}

	# 振り分け
	for my $nl (@new_line) {
		my($nname, $nc) = split /<>/, $nl;
		my $pid = unpack 'H*', $nname;
		my %you_datas = &get_you_datas($pid, 1);

		&move_player2($you_datas{name}, $nc);
		# 対象が自キャラならば
		if ($you_datas{name} eq $m{name}) {
			$m{country} = $nc; # 所属国の書き換え
			$m{vote} = ''; # 立候補・投票データの初期化

			# 混乱情勢でなければ代表熟練度のﾊﾞｯｸｱｯﾌﾟ
			if ($w{world} != $#world_states-1) {
				for my $k (qw/war dom pro mil/) {
					$m{"${k}_c_t"} = $m{"${k}_c"};
					$m{"${k}_c"} = 0;
				}
			}
			&write_user;
		}
		# 対象が他キャラならば
		else {
			my @data = (
				['country', $nc],
				['vote', '']
			);

			# 混乱情勢でなければ代表熟練度の書き換え
			if ($w{world} != $#world_states-1) {
				for my $k (qw/war dom pro mil/) {
					my @data2 = (
						["${k}_c_t", $you_datas{"${k}_c"}],
						["${k}_c", 0]
					);
					push @data, @data2;
				}
			}
			&regist_you_array($you_datas{name}, @data);
		}
	}
	&write_cs;
}

#================================================
# 祭り情勢用のプレイヤー移動関数
# 諸々のチェックが必要ないためメンバーファイルに追記するだけ
#================================================
sub move_player2 {
	my($name, $to_country) = @_;

	open my $fh9, ">> $logdir/$to_country/member.cgi" or &error("$logdir/$to_country/member.cgiﾌｧｲﾙが開けません");
	print $fh9 "$name\n";
	close $fh9;
	++$cs{member}[$to_country];
}

=pod
#================================================
# 一括 regist_you_data する時に最低限必要なデータを作成し返す
# 第１引数は get_you_datas の戻り値を示すポインタ
# 第２引数は user.cgi の1行目
# 第３引数は仕官先の国ナンバー
# 第４引数は代表熟練に関するフラグ 0 ﾊﾞｯｸｱｯﾌﾟ 1 ﾘｽﾄｱ
# 注意！ 混乱の除外処理をここでやっているので変更する時はここを変更
#================================================
sub create_you_data {
	my($you_datas, $user_line , $to_country, $daihyo_flag) = @_;

	# 所属国の書き換え
	if (index($user_line, "<>country;") >= 0) { $user_line =~ s/<>(country;).*?<>/<>${1}$to_country<>/; }
	else { $user_line = "country;$to_country<>" . $user_line; }

	# 立候補・投票データの初期化
	if (index($user_line, "<>vote;") >= 0) { $user_line =~ s/<>(vote;).*?<>/<>$1<>/; }
	else { $user_line = "vote;<>" . $user_line; }

	# 混乱情勢でなければ代表熟練度の書き換え
	if ($w{world} != $#world_states-1) {
		for my $k (qw/war dom pro mil/) {
			my $k1 = $daihyo_flag == 0 ? "${k}_c_t" : "${k}_c"; # ﾊﾞｯｸｱｯﾌﾟ・ﾘｽﾄｱで参照先が逆
			my $k2 = $daihyo_flag == 0 ? "${k}_c" : "${k}_c_t" ; # ﾊﾞｯｸｱｯﾌﾟ・ﾘｽﾄｱで参照先が逆
			if (index($user_line, "<>$k1;") >= 0) { $user_line =~ s/<>($k1;).*?<>/<>$1$$you_datas{$k2}<>/; }
			else { $user_line = "$k1;$$you_datas{$k2}<>" . $user_line; }
			if (index($user_line, "<>$k2;") >= 0) { $user_line =~ s/<>($k2;).*?<>/<>${1}0<>/; }
			else { $user_line = "$k2;0<>" . $user_line; }
		}
	}

	return $user_line;
}

#================================================
# 一括 regist_you_data する時に必要な負け称号などのデータを追加して返す
# 第１引数は get_you_datas の戻り値を示すポインタ
# 第２引数は user.cgi の1行目
#================================================
sub add_you_penalty_data {
	my($you_datas, $user_line) = @_;

	if (index($line, "<>shogo;") >= 0) { $line =~ s/<>(shogo;).*?<>/<>${1}$cs{name}[$$you_datas{country}](笑)<>/; }
	else { $line = "shogo;$cs{name}[$$you_datas{country}](笑)<>" . $line; }

	my $t = $time + 3600 * 24 * 3;
	if (index($line, "<>trick_time;") >= 0) { $line =~ s/<>(trick_time;).*?<>/<>${1}$t<>/; }
	else { $line = "trick_time;$t<>" . $line; }

	if (index($line, "<>shogo_t;") >= 0) { $line =~ s/<>(shogo_t;).*?<>/<>${1}$datas{shogo}<>/; }
	else { $line = "shogo_t;$datas{shogo}<>" . $line; }

	return $user_line;
}
=cut
#================================================
# 1位 (int(国数/2)+1)位 国数位 の国力順位を配列で返す
# 拙速用だけどなんか使い道あるかも？
#================================================
sub get_strong_ranking {
	# lstrcpy とか memcpy でガッとやるようにもっと簡単にコピペできそうだけど分からんちん
	my %tmp_cs;
	for my $i (1 .. $w{country}) {
		$tmp_cs{$i-1} = $cs{strong}[$i];
	}

	# 国力に着目して降順ソート
	my @strong_rank = ();
	foreach(sort {$tmp_cs{$b} <=> $tmp_cs{$a}} keys %tmp_cs){
		push(@strong_rank, [$_, $tmp_cs{$_}]);
	}

	my $_country = $w{country} - 1; # ﾈﾊﾞﾗﾝを除く国数
	my $center = int($_country / 2);

	# top center bottom のダブり数と先頭インデックスの取得
	my @data = ([0,-1], [0,-1], [0,-1]);
	for my $i (0 .. $_country) {
		if ($strong_rank[$i][1] == $strong_rank[0][1]) {
			$data[0][0]++;
			$data[0][1] = $i if $data[0][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$center][1]) {
			$data[1][0]++;
			$data[1][1] = $i if $data[1][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$c][1]) {
			$data[2][0]++;
			$data[2][1] = $i if $data[2][1] < 0;
		}
	}

	# 同一国力があるなら重複しないように rand 選択
	# 重複しない値を引くまで while rand した方が速いか？
	my @result = ();
	for my $i (0 .. $#data) {
		my $j = int(rand($data[$i][0])+$data[$i][1]); # ダブりの先頭インデックスからダブり数-1の乱数
		push (@result, @{splice(@strong_rank, $j, 1)}[0] + 1 ); # rand選択された国を候補から抜く 0 はﾈﾊﾞﾗﾝなので +1
		# ダブり数や先頭インデックスの修正
		for my $k ($i+1 .. $#data) {
			if ($j > $data[$k][1]) {
				$data[$k][0]--;
			}
			elsif ($j < $data[$k][1]) {
				$data[$k][1]--;
			}
			else {
				$data[$k][0]--;
				$data[$k][1]--;
			}
		}
	}
	return @result;
}

=pod
# 祭り情勢の開始と終了に紐づくので 1 ずつ空ける
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# 祭り情勢の名称と、開始時なら 1 終了時 なら 0 を指定する
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

sub player_migrate {
	my $type = shift;

	if ($type == &festival_type('kouhaku', 1)) { # 不倶戴天設定
	}
	elsif ($type == &festival_type('kouhaku', 0)) { # 不倶戴天解除
	}
	elsif ($type == &festival_type('sangokusi', 1)) { # 三国志設定
	}
	elsif ($type == &festival_type('sangokusi', 0)) { # 三国志解除
		require "./lib/move_player.cgi";
	}
#	elsif ($type == &festival_type('konran', 1) || $type == &festival_type('sessoku', 1)) { # 混乱設定
	elsif ($type == &festival_type('konran', 1)) { # 混乱設定
	}
#	elsif ($type == &festival_type('konran', 0) || $type == &festival_type('sessoku', 0)) { #混乱解除
	elsif ($type == &festival_type('konran', 0)) { #混乱解除
	}
	elsif ($type == &festival_type('sessoku', 1)) { # 拙速開始
#		&write_cs;
	}
	elsif ($type == &festival_type('sessoku', 0)) { # 拙速終了
#		&cs_data_repair;
#		&write_cs;
	}
	elsif ($type == &festival_type('dokuritu', 1)) { # 独立設定
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
	}
	elsif ($type == &festival_type('dokuritu', 0)) { # 独立解除
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
		
		&cs_data_repair;# ???
	}
}
=cut
1;