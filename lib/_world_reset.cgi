#================================================
# 世界情勢や国ﾃﾞｰﾀのﾘｾｯﾄで使われるモジュール
# 祭り情勢に関するものが多いが全体的にもっとシンプルにできそうなので _world_reset としておく
# world reset vs_npc が使う add_npc_data はさらに外部に置いた方が良さそう
#================================================

#================================================
# 主な呼び出し元
# ./lib/world.cgi
# ./lib/reset.cgi
# 戦争勝利時の統一や統一期限が切れた時に必要になる
#================================================

#================================================
# 情勢全般
#================================================

# 来年の情勢リストを渡すと直近11年の情勢と重複するものを除外した情勢リストが返ってくる
sub unique_worlds {
	my @new_worlds = @_;
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my @old_worlds = split /<>/, <$fh>;
	close $fh;
	my @next_worlds;
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
	return @next_worlds;
}

#================================================
# 特殊情勢 暗黒を含む祭り情勢の意
#================================================

# 渡された情勢ナンバーを渡すと祭り情勢か判断して返す
sub is_festival_world {
	my $world_no = shift;
	if ($#world_states-5 <= $world_no && $world_no < $#world_states) {
#		require './lib/_festival_world.cgi'; # 祭り情勢ならば自動的にロード
		return 1;
	}
	else {
		return 0;
	}
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

1;