my $this_file = "$logdir/$m{country}/review.cgi";
#=================================================
# 代表投票 Created by Merino
#=================================================

# 罷免に必要な票
my $need_point = int($cs{member}[$m{country}] * 0.1)+2;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何か行いますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "$c_mの代表\を罷免します<br>";
		$mes .= "罷免になるには$need_point票必要です<br>";
	}
	&menu('やめる', '罷免投票する');
}

sub tp_1 {
	return if &is_ng_cmd(1);
	
	$m{tp} = $cmd * 100;
	&{'tp_' . $m{tp} };
}

#=================================================
# 支持・不支持の選択
#=================================================
sub tp_100 {
	my $dfind = 0;
	for my $k (qw/war dom pro mil/) {
		$dfind = 1 if $cs{$k}[$m{country}] ne '';
	}
	unless($dfind) {
		$mes .= '罷免候補者がいません<br>';
		&begin;
		return;
	}
	
	if (!-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
		for my $k (qw/war dom pro mil/) {
			print $fh "$cs{$k}[$m{country}]<>dummy<>\n";
		}
		close $fh;
	}
	my $sub_mes = '';
	my $is_find = 0;
	open my $fh, "< $this_file" or &error('国リーダーファイルが読み込めません');
	for my $k (qw/war dom pro mil/) {
		my $line = <$fh>;
		next if($cs{$k}[$m{country}] eq '');
		my($name, $vote) = split /<>/, $line;
		my @votes = split /,/, $vote;
		if($cs{$k}[$m{country}] ne $name){
			@votes = ();
		}
		my $vote_num = @votes;
		$sub_mes .= qq|<input type="radio" name="vote" value="$k">$cs{$k}[$m{country}]：$vote_num票<br>|;
	}
	close $fh;
	
	$mes .= '誰を罷免しますか?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="vote" value="">やめる<hr>|;
	$mes .= qq|$sub_mes|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="決 定" class="button1"></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	unless($in{vote}) {
		&begin;
		return;
	}
	
	my $review_name = '';
	my @lines = ();
	open my $fh, "+< $this_file" or &error('国リーダーファイルが開けません');
	eval { flock $fh, 2 };
	for my $k (qw/war dom pro mil/) {
		my $line = <$fh>;
		my($name, $vote) = split /<>/, $line;
		if($k eq $in{vote}){
			$review_name = $cs{$k}[$m{country}];
			if($cs{$k}[$m{country}] ne $name){
				$vote = "$m{name}";
				$name = $cs{$k}[$m{country}];
			}else{
				my @votes = split /,/, $vote;
				my $vote_num = @votes;
				my $vfind = 0;
				for my $vname (@votes){
					$vfind = 1 if($vname eq $m{name});
				}
				unless($vfind){
					$vote .= ",$m{name}";
					$vote_num++;
					if($vote_num >= $need_point){
						$c = $k . '_c';
						my $v_id = unpack 'H*', $name;
						my %datas = &get_you_datas($v_id, 1);
						&regist_you_data($name,$c,int($datas{$c} * 0.75));
						&write_world_news("<b>$nameが$c_mの代表\を罷免になりました</b>", 1, $name);
						$cs{$k}[$m{country}] = '';
						$cs{$c}[$m{country}] = 0;
						$name = '';
						$vote = '';
						&write_cs;
					}
				}
			}
		}
		push @lines, "$name<>$vote<>\n"; # 0票は消える
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= $review_name ? "$review_nameを罷免投票します<br>" : 'やめました<br>';
	
	&begin;
}

1; # 削除不可
