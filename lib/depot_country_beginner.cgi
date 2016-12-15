my $this_file = "$logdir/$m{country}/depot_b.cgi";
my $this_log = "$logdir/$m{country}/depot_b_log.cgi";
#=================================================
# 新規用国庫
#=================================================

# 最大保存数
my $max_depot = 10;

# 預けられないｱｲﾃﾑ
my %taboo_items = (
	wea => [32,], # 武器
	egg => [], # ﾀﾏｺﾞ
	pet => [127,138,188], # ﾍﾟｯﾄ
	gua => [], # 防具
);

sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}
#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "ここは新規用国庫です。$max_depot個まで預けることができます<br>";
		$mes .= "どうしますか?<br>";
	}
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_fileが開けません");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_logが開けません");
		close $fh;
	}
	&menu('やめる', '引出す', '預ける', '整理する','履歴確認');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# 引出す
#=================================================
sub tp_100 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot;

	$mes .= "どれを引出しますか? [ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .=  $is_mobile ? qq|<p><input type="submit" value="引出す" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="引出す" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $flag = 1;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				
				if ($kind eq '1' && $m{wea}) {
					$mes .= "既に武器を所持しています";
					$flag = 0;
				}
				elsif ($kind eq '2' && $m{egg}) {
					$mes .= "既に卵を所持しています";
					$flag = 0;
				}
				elsif($kind eq '3' && $m{pet}) {
					$mes .= "既にﾍﾟｯﾄを所持しています";
					$flag = 0;
				}
				elsif($kind eq '4' && $m{gua}) {
					$mes .= "既に防具を所持しています";
					$flag = 0;
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line && $flag) {
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			if ($kind eq '1') {
				$m{wea}    = $item_no;
				$m{wea_c}  = $item_c;
				$m{wea_lv} = $item_lv;
				$mes .= "$weas[$m{wea}][1]を引出しました<br>";
			}
			elsif ($kind eq '2') {
				$m{egg}    = $item_no;
				$m{egg_c}  = $item_c;
				$mes .= "$eggs[$m{egg}][1]を引出しました<br>";
			}
			elsif ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]★$m{pet_c}を引出しました<br>";

				&get_icon_pet;
			}
			elsif ($kind eq '4') {
				$m{gua}    = $item_no;
				$mes .= "$guas[$m{gua}][1]を引出しました<br>";
			}

			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_fileが開けません");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>0<>\n";
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;

			# 引出すﾀｲﾐﾝｸﾞで新しいｱｲﾃﾑがあればｺﾚｸｼｮﾝに追加
			require './lib/add_collection.cgi';
			&add_collection;
		}
		else {
			close $fh;
		}
	}
	&begin;
}

#=================================================
# 預ける
#=================================================
sub tp_200 {
	$mes .= 'どれを預けますか?';
	
	my @menus = ('やめる');
	push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
	push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
	push @menus, $m{pet} > 0 ? $pets[$m{pet}][1] : '';
	push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
	
	&menu(@menus);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..4);
	if ($cmd eq '1' && $m{wea_name}) {
		$mes .= "唯一無二の武器を預けることはできません<br>";
		&begin;
		return;
	}
	my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
	for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
		if ($taboo_item eq $m{ $kinds[$cmd] }) {
			my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
							: $cmd eq '2' ? $eggs[$m{egg}][1]
							: $cmd eq '3' ? $pets[$m{pet}][1]
							:               $guas[$m{gua}][1]
							;
			$mes .= "$t_item_nameは預けることはできません<br>";
			&begin;
			return;
		}
	}
	my $line;
	my $sub_line;
	if ($cmd eq '1' && $m{wea}) {
		$line = "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
		$sub_line = "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '2' && $m{egg}) {
		$line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>\n";
		$sub_line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '3' && $m{pet} > 0) {
		$line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>\n";
		$sub_line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '4' && $m{gua}) {
		$line = "$cmd<>$m{gua}<>0<>0<>\n";
		$sub_line = "$cmd<>$m{gua}<>0<>0<>$m{name}<>1<>\n";
	}
	else {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	push @lines, $_ while <$fh>;
	
	if (@lines >= $max_depot) {
		close $fh;
		$mes .= 'これ以上預けることができません<br>';
	}
	else {
		push @lines, $line;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if ($cmd eq '1') {
			if($m{wea_name}){
				$m{wea} = 32;
				$m{wea_c} = 0;
				$m{wea_lv} = 0;
				$mes .= "持ち主の手を離れた途端$m{wea_name}はただの$weas[$m{wea}][1]になってしまった";
				$m{wea_name} = "";
			}
			$mes .= "$weas[$m{wea}][1]を預けました<br>";
			$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		}
		elsif ($cmd eq '2') {
			$mes .= "$eggs[$m{egg}][1]を預けました<br>";
			$m{egg} = $m{egg_c} = 0;
		}
		elsif ($cmd eq '3') {
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}を預けました<br>";
			&remove_pet;
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]を預けました<br>";
			$m{gua} = 0;
		}
		
			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_fileが開けません");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, $sub_line;
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;
	}
	&begin;
}

#=================================================
# 整理
#=================================================
sub tp_300 {
	my @lines = ();
	my $n_egg = 0;
	my $n_man = 0;
	my $n_hero = 0;	
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>){
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if($kind == 2 && $item_no == 53){
			$line = "2<>42<>$item_c<>$item_lv<>\n";
			$n_egg++;
		}
		if($kind == 3 && $item_no == 180){
			$line = "3<>76<>$item_c<>$item_lv<>\n";
			$n_man++;
		}
		if($kind == 3 && $item_no == 181){
			$line = "3<>77<>$item_c<>$item_lv<>\n";
			$n_hero++;
		}
		push @lines, $line;
	}
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] }
					map { [$_, split /<>/ ] } @lines;
	while($n_egg>0 || $n_man>0 || $n_hero>0){
		my $line_i = rand(@lines);
		my $o_line = $lines[$line_i];
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $o_line;
		if($kind == 2 && $item_no == 42 && $n_egg > 0){
			$o_line = "2<>53<>$item_c<>$item_lv<>\n";
			$n_egg--;
		}
		if($kind == 3 && $item_no == 76 && $n_man > 0){
			$o_line = "3<>180<>$item_c<>$item_lv<>\n";
			$n_man--;
		}
		if($kind == 3 && $item_no == 77 && $n_hero > 0){
			$o_line = "3<>181<>$item_c<>$item_lv<>\n";
			$n_hero--;
		}
		$lines[$line_i] = $o_line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "預けているものを整理しました<br>";
	&begin;
}

#=================================================
# ログ確認
#=================================================
sub tp_400 {
	my @lines = ();
	open my $fh, "< $this_log" or &error("$this_logが開けません");
	while (my $line = <$fh>){
		my($kind, $item_no, $item_c, $item_lv, $name, $type) = split /<>/, $line;
		$mes .= "$name が";
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$mes .= "を";
		$mes .= $type eq '1' ? "預けました<br>":
					$type eq '0' ? "引き出しました<br>":
								"奪いました<br>";
	}
	close $fh;
	&begin;
}

#=================================================
# <input type="radio" 付の預かり所の物
#=================================================
sub radio_my_depot {
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_fileが開けません");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_logが開けません");
		close $fh;
	}
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$sub_mes .= qq|<input type="radio" id="$count" name="cmd" value="$count">|;
		$sub_mes .= qq|<label for="$count">| unless $is_mobile;
		$sub_mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	return $count, $sub_mes;
}

1; # 削除不可
