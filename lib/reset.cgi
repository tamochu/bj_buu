use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# 国ﾘｾｯﾄ Created by Merino
#================================================

# 統一難易度：[難しい 60 ～ 40 簡単]
#my $game_lv = $config_test ? int(rand(6) + 55) : int( rand(11) + 40 );
my $game_lv = $config_test ? int( rand(11) + 45 ) : int( rand(11) + 45 );

# 統一期限(日)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# 期日が過ぎた場合
#================================================
sub time_limit {
	$w{win_countries} = '';
	unless ($w{world} eq $#world_states-5) { # 拙速以外の情勢で期限切れ
		&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
		&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");

		# 特殊情勢前期でもなく暗黒終了時でもないなら
		# 特殊情勢で上書きされるので計算するだけ無駄
		unless ($w{year} =~ /5$/ || $w{year} =~ /6$/ || $w{year} =~ /9$/) {
			($w{world}, $w{world_sub}) = &choice_unique_world(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
	}

	&reset; # ここまで今期期限切れ時の処理

	if ($w{world} eq '0') { # 平和
		&write_world_news("<i>世界は $world_states[$w{world}] になりました</i>");
		&send_twitter("世界は $world_states[$w{world}] になりました");
	}
	elsif ($w{world} eq '18') { # 殺伐
		&write_world_news("<i>世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました</i>");
		&send_twitter("世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました");
	}
	else {
		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
		&send_twitter("世界は $world_states[$w{world}] となりました");
	}

	&add_world_log($w{world});
	&begin_common_world;

	&write_cs;
}

#================================================
# 国ﾃﾞｰﾀﾘｾｯﾄ処理（情勢は含まれないっぽい）
# 統一と期限切れで呼ばれるので抽象的とする
# 基本的にここで $w{world} を書き換えてはいけない（特殊情勢は統一者が情勢を選ばない限り情勢なしになるのを回避するため？）
# reset後に情勢が確定するため、ここを通ってから情勢を表示すること
# reset 前後に $w{world} を変える処理があるので情勢を決める関数として使うものではないと思われる
#================================================
sub reset {
	$this_file = "$logdir/chat_casino_toto";
	require './lib/casino_toto.cgi';
	&pay_back($w{year});
	$this_file = "$logdir/chat_casino_e";
	require './lib/casino_espoir.cgi';
	&game_end_espoir($w{year});

	# 特殊情勢終了処理
	if (&is_special_world) { # 特殊情勢終了
		if ($w{year} =~ /6$/) { # 暗黒・英雄終了
#			if ($w{year} =~ /16$/ || $w{year} =~ /36$/ || $w{year} =~ /56$/ || $w{year} =~ /76$/ || $w{year} =~ /96$/) { # 暗黒終了
			if ($w{year} % 20 > 9) { # 暗黒終了
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# 英雄終了処理は特になし
		}
		else { # 祭り情勢終了
			require './lib/_festival_world.cgi';
			&end_festival_world;
		}
		$w{world} = int(rand($#world_states-5));
	}

	# ここまでが一年の最後の最後
	# ここからは一年の最初の最初

	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 12;
	$w{limit_time} = $config_test ? $time + 3600 * 36 : $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;

	# reset countries
	my $sleep_num = 0;
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
#		$sleep_num++ if $cs{is_die}[$i] > 2;
	}

	# 仕官できる人数
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
#	$country -= $sleep_num if $sleep_num > 0;
	my $ave_c = int($w{player} / $country);
	$ave_c = $ave_c < 2 ? 2 : $ave_c;
#	$ave_c = $config_test ? 11 : $ave_c;

	# set countries
	my($c1, $c2) = split /,/, $w{win_countries};
	for my $i (1 .. $w{country}) {
		# 統一国の場合はNPC弱体
#		$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
		$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(4) + 12) * 1000;
		$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		$cs{food}[$i]     = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
#		if ($cs{is_die}[$i] > 2) {
#			$cs{strong}[$i]   = 0;
#			$cs{capacity}[$i] = 0;
#		}
#		else {
			$cs{is_die}[$i]   = 0;
			$cs{capacity}[$i] = $ave_c;
#		}
		
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
		&send_twitter("各国の$e2j{ceo}の任期が満了となりました");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>各国の代表\者の任期が満了となりました</b>");
		&send_twitter("各国の代表\者の任期が満了となりました");
	}

	# 特殊情勢開始処理
	if (&is_special_world) { # 特殊情勢開始
		if ($w{year} =~ /6$/) { # 暗黒・英雄開始
#			if ($w{year} =~ /16$/ || $w{year} =~ /36$/ || $w{year} =~ /56$/ || $w{year} =~ /76$/ || $w{year} =~ /96$/) { # 暗黒開始
			if ($w{year} % 20 > 9) { # 暗黒開始
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
			else { # 英雄開始
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
		}
		else { # 祭り情勢開始
			require './lib/_festival_world.cgi';
			&begin_festival_world;
		}
	}

	# 1000年デフォルト
	# ｽﾊﾟﾝ長すぎて形骸化してる上に祭り情勢の開始ﾊﾞｯｸｱｯﾌﾟと終了ﾘｽﾄｱに挟まってるから無効化されそう？
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
}

#================================================
# 年数を渡すと特殊情勢か判断して返す
#================================================
sub is_special_world {
	return $w{year} > 0 ? ($w{year} =~ /6$/ || $w{year} =~ /0$/) : 0 ;
}

#================================================
# 年数を渡すと祭り情勢か判断して返す
# 祭り情勢ならばモジュールもロード
#================================================
sub is_festival_world {
	if ($w{year} > 9 && $w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		return 1;
	}
	return 0;
}

#================================================
# 情勢リストを渡すと直近11年の情勢と重複するものを除外した中からランダムで情勢を選んでくれる
# 戻り値は (world, world_sub)
#================================================
sub choice_unique_world {
	my @new_worlds = @_;
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $line = <$fh>;
	close $fh;
	my @old_worlds = split /<>/, $line;
	my @next_worlds = ();
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

	# 重複するものばかりだった場合には「平和」になるようになっていたが「謎」の方が適当かと
	return ( $next_worlds[int(rand(@next_worlds))], int(rand($#world_states-5)) ) if @next_worlds;
	return ( 19, int(rand($#world_states-5)) );
}

#================================================
# 渡された情勢を情勢ログの先頭に挿入する
#================================================
sub add_world_log {
	my $world = shift;
	my $nline = "$world<>";
	my $saved_w = 0;
	open my $fh, "+< $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $line = <$fh>;
	my @old_worlds = split /<>/, $line;
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	seek $fh, 0, 0;
	truncate $fh, 0;
	print $fh "$nline\n";
	close $fh;
}

#================================================
# 通常情勢の設定をする
#================================================
sub begin_common_world {
	my $old_world = $w{world};

	if ($w{world} eq '0') { # 平和
		$w{reset_time} += $config_test ? 0 : 3600 * 12;
#		&write_world_news("<i>世界は $world_states[$w{world}] になりました</i>");
	}
	elsif ($w{world} eq '6') { # 結束
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i] > 2;
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
#		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
	}
	elsif ($w{world} eq '18') { # 殺伐
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
#		&write_world_news("<i>世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました</i>");
	}
	else {
#		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
	}
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.9):$w{game_lv};
}

1; # 削除不可