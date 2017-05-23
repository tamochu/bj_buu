my $depot_file = "$userdir/$id/depot.cgi";
my $this_lock_file = "$userdir/$id/depot_lock.cgi";
#================================================
# 賽銭箱
#=================================================
# 糞ﾍﾟｯﾄ
my @bad_pets = (126,197);

# レアﾍﾟｯﾄ
my @good_pets = (3,7,8,17,18,19,20,21,58,59,60,63,127,150,151,183);

# 強化限界
my $max_mix = 20;

# 過去の栄光に表示される最低値
my $dragon_nest = 10;

# 最大保存数
my $max_depot = $m{sedai} > 7 ? 50 : $m{sedai} * 5 + 15;
$max_depot += $m{depot_bonus} if $m{depot_bonus};

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何をするの?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ドラクエ？知らんな<br>';
		$mes .= '装備中のペットと預り所にあるﾍﾟｯﾄを合成できるよ！よ！<br>';
	}
	
	&menu('やめる','ﾍﾟｯﾄを合成する','まとめて合成', '生け贄の羊を祭壇に', '合成可能ペットを確認');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	if ($cmd ne '4') {
		if($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]){
			$mes .= "$shogos[1][0]は合成できない。残念<br>";
			&begin;
			return;
		}
		if ($m{pet} < 0) {
			$mes .= "借りたﾍﾟｯﾄをキメラ化するなんてとんでもない！<br>";
			&begin;
			return;
		}
		unless ($pets[$m{pet}][5]) {
			$mes .= "君が今持ってるﾍﾟｯﾄは合成できないんだ。ごめんね<br>";
			&begin;
			return;
		}
		if ($pets[$m{pet}][0] eq '9' && $m{pet_c} >= 15) { # ﾌｧﾝﾄﾑ☆15で強化限界
			$mes .= "$pets[$m{pet}][1]はもう合成できないんだ。ごめんね<br>";
			&begin;
			return;
		}
		if ($cmd eq '1' && $m{is_full}) {
			$mes .= "預り所がいっぱいで合成したﾍﾟｯﾄが入らないよ<br>";
			&begin;
			return;
		}
	}
	
	$layout = 2;
	if($cmd eq '1'){
		$mes .= "どれと合成しますか?<br>";
		$mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
	
		my %lock = &get_lock_item;
		open my $fh, "< $depot_file" or &error("$depot_file が読み込めません");
		my $count = 0;
		while (my $line = <$fh>) {
			++$count;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

			if($kind eq '3' && $lock{"$kind<>$item_no<>"} < 1){
				my $good_bad = 'normal';
				for my $bpet (@bad_pets){
					if($bpet == $item_no){
						$good_bad = 'bad';
						last;
					}
				}
				for my $gpet (@good_pets){
					if($gpet == $item_no){
						$good_bad = 'good';
						last;
					}
				}

				$mes .= qq|<label class="$good_bad">| unless $is_mobile;
				$mes .= qq|<input type="radio" name="cmd" value="$count">|;
				$mes .= qq|[ぺ]$pets[$item_no][1]★$item_c|;
				$mes .= qq|</label>| unless $is_mobile;
				$mes .= qq|<br>|;
			}
		}
		close $fh;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= $is_mobile ? qq|<p><input type="submit" value="合成する" class="button1" accesskey="#"></p></form>|:
			qq|<p><input type="submit" value="合成する" class="button1"></p></form>|;
	} elsif ($cmd eq '4') {
		$mes .= "今合成可能\なのは<br>";
		my $line_i = 0;
		for my $pi (1..$#pets) {
			if ($pets[$pi][5] && $pi ne'180' && $pi ne'181') {
				$mes .= $pets[$pi][1] . ", ";
				$line_i++;
				if ($line_i > 5) {
					$mes .= "<br>";
					$line_i = 0;
				}
			}
		}
		$mes .= "<br>だよ。<br>";
		&begin;
		return;
	}else{
		$mes .= "どれと合成しますか?<br>";
		$mes .= qq|<form method="$method" action="$script">|;
	
		my %lock = &get_lock_item;
		open my $fh, "< $depot_file" or &error("$depot_file が読み込めません");
		my $count = 0;
		while (my $line = <$fh>) {
			++$count;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

			if($kind eq '3' && $lock{"$kind<>$item_no<>"} < 1){
				my $good_bad = 'normal';
				for my $bpet (@bad_pets){
					if($bpet == $item_no){
						$good_bad = 'bad';
						last;
					}
				}
				for my $gpet (@good_pets){
					if($gpet == $item_no){
						$good_bad = 'good';
						last;
					}
				}

				my $checked = '';
				if ($cmd eq '3' && $item_no == 126) {
					$checked = ' checked';
				}
				$mes .= qq|<label class="$good_bad">| unless $is_mobile;
				$mes .= qq|<input type="checkbox" name="pet_$count" value="1"$checked>|;
#				$mes .= qq|<label for="$count">| unless $is_mobile;
				$mes .= qq|[ぺ]$pets[$item_no][1]★$item_c|;
				$mes .= qq|</label>| unless $is_mobile;
				$mes .= qq|<br>|;
			}
		}
		close $fh;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= $is_mobile ? qq|<p><input type="submit" value="合成する" class="button1" accesskey="#"></p></form>|:
			qq|<p><input type="submit" value="合成する" class="button1"></p></form>|;
		$cmd = 2;
	}
	$m{tp} = $cmd * 100;
}

#=================================================
# 合成
#=================================================
sub tp_100 {
	if ($cmd) {
		my $count = 0;
		my $pet_no;
		my $pet_c;
		my @lines = ();
		open my $fh, "+< $depot_file" or &error("$depot_fileが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			++$count;
			if ($cmd eq $count) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				if($kind eq '3' && &mix($item_no, 0) == -1){
					push @lines, $line;
				}
			}
			else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;
		close $fh;
		
	}
	&begin;
}

#=================================================
# 一括合成
#=================================================
sub tp_200 {
	
	open my $fh, "< $depot_file" or &error("$depot_file が読み込めません");
	my $count = 0;
	my $rest = 0;
	while (my $line = <$fh>) {
		++$count;
		 $rest++ unless $in{"pet_$count"};
		# ここから消しても良さそう
#		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
#		unless($in{"pet_$count"}){
#			$rest++;
#		}
	}
	close $fh;
	if($rest > $max_depot){
		$mes .= "預り所がいっぱいで合成したﾍﾟｯﾄが入らないよ<br>";
		&begin;
		return;
	}
	
	$count = 0;
	my @lines = ();
	my %duplication = ();
	open my $fh, "+< $depot_file" or &error("$depot_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($in{"pet_$count"}) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			$no_logging = $duplication{$item_no};
			$duplication{$item_no}++;
			if(&mix($item_no, $no_logging) == -1){
				push @lines, $line;
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0; 
	print $fh @lines;
	close $fh;

	&begin;
}

sub mix{
	my $pet_no = shift;
	my $no_logging = shift;
	
	if($m{pet_c} >= $max_mix || $pets[$m{pet}][0] eq '9' && $m{pet_c} >= 15){ # ☆20以上かﾌｧﾝﾄﾑ☆15以上で強化限界
		$mes .= "そのﾍﾟｯﾄはこれ以上合成できないよ<br>";
		&begin;
		return -1;
	}
	if (!$no_logging) {
		&sale_data_log(3, $pet_no, 0, 0, 500, 5);
	}
	
	my $good_bad = 1;
	for my $bpet (@bad_pets){
		if($bpet == $pet_no){
			$good_bad = 1.5;
			last;
		}
	}
	for my $gpet (@good_pets){
		if($gpet == $pet_no){
			$good_bad = 0.5;
			last;
		}
	}
	
	if(rand(&fib($m{pet_c}))*$good_bad < 1){
		$m{pet_c}++;
		$mes .= "合成に成功したよ君のﾍﾟｯﾄは$pets[$m{pet}][1]★$m{pet_c}になったよ<br>";
		if($m{pet_c} >= $dragon_nest){
			&mes_and_world_news("$pets[$m{pet}][1]★$m{pet_c}の合成に成功しました。", 1);
		}
	}else{
		$mes .= "残念合成に失敗したよ<br>";
	}
}

sub fib{
	my $x = shift;
	my @fib_rets = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765);
	return $fib_rets[$x];
}

#=================================================
# ロックアイテムの取得
#=================================================
sub get_lock_item {
	my %lock = ();
	open my $lfh, "< $this_lock_file" or &error("$this_lock_fileが開けません");
	while (my $line = <$lfh>){
		chomp $line;
		$lock{$line}++;
	}
	close $lfh;

	return %lock;
}

1; # 削除不可
