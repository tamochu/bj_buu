use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_world_reset.cgi';
#================================================
# 国ﾘｾｯﾄ Created by Merino
#================================================

# 統一難易度：[難しい 60 ～ 40 簡単]
my $game_lv = $config_test ? int(rand(6) + 5) : int( rand(11) + 40 );

# 統一期限(日)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# 期日が過ぎた場合
#================================================
sub time_limit {
	$w{win_countries} = '';
	if (&is_festival_world) { # 祭り情勢時に期限切れ
		&time_limit_festival;
		&write_cs;
	}
	else { # 暗黒・通常情勢で期限切れ
		&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
		&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");

		# 特殊情勢前期でもなく暗黒終了時でもないなら
		# 特殊情勢で上書きされるので計算するだけ無駄
		unless ($w{year} =~ /5$/ || $w{year} =~ /6$/ || $w{year} =~ /9$/) {
			my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
			my @next_worlds = &unique_worlds(@new_worlds);
			$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		}
	}

	&reset; # ここまで今期期限切れ時の処理

	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

	&opening_common;

	$w{game_lv} = 0;

	&write_cs;
}

#================================================
# 国ﾃﾞｰﾀﾘｾｯﾄ処理
# 統一と期限切れで呼ばれるので抽象的とする
# reset後に情勢が確定するため、ここを通ってから情勢を表示すること
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});

	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000 if $cs{is_die}[$i] != 2;
	}

	# 終了処理
	if (&is_special_world) { # 特殊情勢終了
		if ($w{year} =~ /6$/) { # 暗黒・英雄終了
			unless ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 暗黒終了
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# 英雄終了処理は特になし
		}
		else { # 祭り情勢終了
			require './lib/_festival_world.cgi';
			my $migrate_type = &ending_festival;
			&player_migrate($migrate_type);
		}
		$w{world} = int(rand($#world_states-5));
	}

	# 仕官できる人数
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);

	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
#	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{limit_time} = $config_test ? $time: $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;

	# set countries
	my($c1, $c2) = split /,/, $w{win_countries};
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

	# 特殊情勢開始処理
	if (&is_special_world) { # 特殊情勢開始
		if ($w{year} =~ /6$/) { # 暗黒・英雄開始
			# おそらく6年と16年で暗黒が続く
			# $w{year} =~ /^6$/ || とでも加える？
			if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 英雄開始
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
			else { # 暗黒開始
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
		}
		else { # 祭り情勢開始
			require './lib/_festival_world.cgi';
			my $migrate_type = &opening_festival;
			&wt_c_reset;
			&player_migrate($migrate_type);
		}
	}

	# 1000年デフォルト
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
}

1; # 削除不可