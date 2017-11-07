use Time::HiRes;
my $this_file = "$userdir/$id/depot.cgi";
my $this_log = "$userdir/$id/depot_log.cgi";
my $this_lock_file = "$userdir/$id/depot_lock.cgi";
#=================================================
# 預かり所 Created by Merino
#=================================================

# 最大保存数
my $max_depot = $m{sedai} > 7 ? 50 : $m{sedai} * 5 + 15;
$max_depot += $m{depot_bonus} if $m{depot_bonus};

# 各処理の開始時に倉庫の擦り切りを行うと処理の隙間で倉庫ﾃﾞｰﾀが書き換えられていた場合に意図せぬｱｲﾃﾑの消失が起きるため、擦り切り処理を開始時ではなく直前に変更
# 例：引き出す画面を開いた後に荷物が届いた場合、ﾕｰｻﾞｰはｱｲﾃﾑを交換したつもりでも持っていたﾍﾟｯﾄが消失し届いた荷物が末尾に追加される
# 擦り切り処理が走るのは引き出した時と整理をした時　先に売るか捨てるかして倉庫を開ければ擦り切り対象のｱｲﾃﾑを入荷できる
# 擦り切り対象のｱｲﾃﾑはロックを無視して売ったり捨てたりできる
my $lost_depot = $max_depot * 2;

# 相手に送るときの手数料(同国)
my $need_money = 100;

# 相手に送るときの手数料(他国)
my $need_money_other = 1000;

# 売る値段
my $sall_price = 100;

# 満杯を超えた時のﾍﾟﾅﾙﾃｨ金(引出し、売る時に減らされる)
my $penalty_money = $m{sedai} > 10 ? 3000 : $m{sedai} * 300;

# 相手に送る時に必要なﾚﾍﾞﾙ(ただし1世代時のみ)
my $need_lv = 10;

# 相手に送るの禁止なｱｲﾃﾑ
my %taboo_items = (
	wea => [32,], # 武器
	egg => [], # ﾀﾏｺﾞ
	pet => [127,188], # ﾍﾟｯﾄ
	gua => [], # 防具
);

my @magic_words = ('a'..'z', 'A'..'Z', 0..9);

#================================================
sub begin {

	local $magic_word = '';
	$magic_word .= $magic_words[int(rand($#magic_words+1))] for (0 .. 12);
	$m{magic_word} = $magic_word;

	if (-f "$userdir/$id/depot_flag.cgi") {
		unlink "$userdir/$id/depot_flag.cgi";
	}
	unless (-f $this_lock_file) {
		open my $lfh, "> $this_lock_file" or &error("$this_lock_fileが開けません");
		close $lfh;
	}
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "ここは預かり所です。$max_depot個まで預けることができます<br>";
		$mes .= "$max_depot個を超えている場合は、$penalty_money Gの罰金を支払ってもらいます<br>";
		$mes .= "どうしますか?<br>";
	}
	&menu('やめる', '引出す', '預ける', '整理する', '相手に送る', '一括売却', '捨てる', 'ロックをかける', '履歴');
}
sub tp_1 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "不正な処理により倉庫の操作を中断しました<br>";
		&begin;
		return;
	}
	return if &is_ng_cmd(1..8);

	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# 引出す
#=================================================
sub tp_100 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "不正な処理により倉庫の操作を中断しました<br>";
		&begin;
		return;
	}

	my $no = $_[0];
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot($no);

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "どれを引出しますか? [ $count / $max_depot$lost_mes ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="magic_word" value="$in{magic_word}">|; # 多窓させないための一時キー
	$mes .= $is_mobile ? qq|<p><input type="submit" value="引出す" class="button1" accesskey="#"></p>|:
		qq|<p><input type="submit" value="引出す" class="button1"></p>|;
	$mes .= qq|<label><input type="checkbox" id="pet_summary" name="show_summary" value="1">ﾍﾟｯﾄの効果を確認する</label></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "不正な処理により倉庫の操作を中断しました<br>";
		&begin;
		return;
	}
	else { # ここでキーが変わった瞬間からあとに続く呼び出しが弾かれるが、キーが変わる瞬間に入られるとおそらく結局同時処理されそうな気がする
		my $magic_word = '';
		$magic_word .= $magic_words[int(rand($#magic_words+1))] for (0 .. 12);
		$in{magic_word} = $magic_word;
		$m{magic_word} = $magic_word;
		&write_user;
	}
	if ($in{show_summary} && $cmd && $cmd <= $lost_depot) { # ﾍﾟｯﾄの説明ﾓｰﾄﾞかつ非表示ﾃﾞｰﾀにアクセスしてない
		require './data/pet.cgi';
		my $count = 0;
		my $new_line = '';
		open my $fh, "< $this_file" or &error("$this_fileが開けません");
		while (my $line = <$fh>) {
			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				my $item_name = &get_item_name($kind, $item_no);
				if($kind eq '3' && $item_no > 0) {
					$mes .= "$item_name：$pet_effects[$item_no]<br>";
					last;
				}
				else {
					$mes .= "$item_nameはﾍﾟｯﾄではありません<br>";
					last;
				}
			}
		}
		close $fh;

		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} }($cmd);
		return;
	}
	else { # 引き出しﾓｰﾄﾞ
		if ($cmd && $cmd <= $lost_depot) { # 非表示ﾃﾞｰﾀにアクセスしてない
			my $count = 0;
			my $new_line = '';
			my $add_line = '';
			my $depot_line = '';
			my @lines = ();
			my $l_mes = "";
			open my $fh, "+< $this_file" or &error("$this_fileが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				if ($in{magic_word} ne $m{magic_word}) { # ここで弾くと効果テキメンらしい 不具合らしい謎の効き目
					$mes = "不正な処理により倉庫の操作を中断しました<br>";
					close $fh;
					&begin;
					return;
				}
				my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
				$depot_line .= "$rkind,$ritem_no,$ritem_c,$ritem_lv<>";
				++$count;
				if (!$new_line && $cmd eq $count) {
					$new_line = $line;
					my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
					$depot_line .= "$kind,$item_no,$item_c,$item_lv<>";
					if ($kind eq '1' && $m{wea}) {
						if($m{wea_name}){
							$m{wea} = 32;
							$m{wea_c} = 0;
							$m{wea_lv} = 0;
							$mes .= "持ち主の手を離れた途端$m{wea_name}はただの$weas[$m{wea}][1]になってしまった<br>";
							$m{wea_name} = "";
						}
						$add_line = "$kind<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
						$mes .= $l_mes = "$weas[$m{wea}][1]を預け";
					}
					elsif ($kind eq '2' && $m{egg}) {
						$add_line = "$kind<>$m{egg}<>$m{egg_c}<>0<>\n";
						$mes .= $l_mes = "$eggs[$m{egg}][1]を預け";
					}
					elsif($kind eq '3' && $m{pet} > 0) {
						$add_line = "$kind<>$m{pet}<>$m{pet_c}<>0<>\n";
						$mes .= $l_mes = "$pets[$m{pet}][1]★$m{pet_c}を預け";
					}
					elsif($kind eq '4' && $m{gua}) {
						$add_line = "$kind<>$m{gua}<>0<>0<>\n";
						$mes .= $l_mes = "$guas[$m{gua}][1]を預け";
					}
				}
				elsif ($count <= $lost_depot) { # 擦り切り処理
					push @lines, $line;
				}
			}
			if ($in{magic_word} ne $m{magic_word}) { # ここたぶん要らない？ 念のため
				$mes = "不正な処理により倉庫の操作を中断しました<br>";
				close $fh;
				&begin;
				return;
			}
			elsif ($new_line) {
				push @lines, $add_line if $add_line;
				seek  $fh, 0, 0;
				truncate $fh, 0; 
				print $fh @lines;
				close $fh;

				my $s_mes;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
				if ($kind eq '1') {
					$m{wea}    = $item_no;
					$m{wea_c}  = $item_c;
					$m{wea_lv} = $item_lv;
					$mes .= "$weas[$m{wea}][1]を引出しました<br>";
					$l_mes .= $s_mes = "$weas[$m{wea}][1]";
				}
				elsif ($kind eq '2') {
					$m{egg}    = $item_no;
					$m{egg_c}  = $item_c;
					$mes .= "$eggs[$m{egg}][1]を引出しました<br>";
					$l_mes .= $s_mes = "$eggs[$m{egg}][1]";
				}
				elsif ($kind eq '3') {
					$m{pet}    = $item_no;
					$m{pet_c}  = $item_c;
					$mes .= "$pets[$m{pet}][1]★$m{pet_c}を引出しました<br>";
					$l_mes .= $s_mes = "$pets[$m{pet}][1]★$m{pet_c}";

					&get_icon_pet;
				}
				elsif ($kind eq '4') {
					$m{gua}    = $item_no;
					$mes .= "$guas[$m{gua}][1]を引出しました<br>";
					$l_mes .= $s_mes = "$guas[$m{gua}][1]";
				}
				my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
				$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
				$s_mes .= "引出し ($tdate)";
				if(-f "$userdir/$id/depot_watch.cgi"){
					open my $wfh, ">> $userdir/$id/depot_watch.cgi";
					print $wfh "$s_mes<>$depot_line\n";
					close $wfh;
				}
				&penalty_depot($count);
	
				&add_log("引出", $l_mes);
	
				# 引出すﾀｲﾐﾝｸﾞで新しいｱｲﾃﾑがあればｺﾚｸｼｮﾝに追加
				require './lib/add_collection.cgi';
				&add_collection;


#				Time::HiRes::sleep(2.5);
			}
			else {
				close $fh;
			}
		}
		&begin;
	}
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

	my $line;
	if ($cmd eq '1' && $m{wea}) {
		# ここでオリ武器用に自データを書き換えてはいけない
		# 爆発処理で意図せず return する可能性がある
		$line = $m{wea_name} ? "$cmd<>32<>0<>0<>\n" : "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
	}
	elsif ($cmd eq '2' && $m{egg}) {
		$line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>\n";
	}
	elsif ($cmd eq '3' && $m{pet}) {
		$line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>\n";
	}
	elsif ($cmd eq '4' && $m{gua}) {
		$line = "$cmd<>$m{gua}<>0<>0<>\n";
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
		$m{is_full} = 1;
	}
	else {
		my $l_mes = "";
		push @lines, $line;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if ($cmd eq '1') {
			if($m{wea_name}){
				$m{wea} = 32;
				$mes .= "持ち主の手を離れた途端$m{wea_name}はただの$weas[$m{wea}][1]になってしまった<br>";
				$m{wea_name} = "";
			}
			$mes .= "$weas[$m{wea}][1]を預けました<br>";
			$l_mes = "$weas[$m{wea}][1]";
			$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		}
		elsif ($cmd eq '2') {
			$mes .= "$eggs[$m{egg}][1]を預けました<br>";
			$l_mes = "$eggs[$m{egg}][1]";
			$m{egg} = $m{egg_c} = 0;
		}
		elsif ($cmd eq '3') {
			$mes .= "$pets[$m{pet}][1]★$m{pet_c}を預けました<br>";
			$l_mes = "$pets[$m{pet}][1]★$m{pet_c}";
			&remove_pet;
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]を預けました<br>";
			$l_mes = "$guas[$m{gua}][1]";
			$m{gua} = 0;
		}
		
		$m{is_full} = 1 if @lines >= $max_depot;

		&add_log("預入", $l_mes);
	}
	&begin;
}

#=================================================
# 整理
#=================================================
sub tp_300 {
	my @lines = ();
	my @sub_lines = ();
	my $count = 0;
	my $n_egg = 0;
	my $n_man = 0;
	my $n_hero = 0;	
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>){
		++$count;
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
		push @lines, $line if $count <= $lost_depot; # 擦り切り処理
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
# 相手に送る
#=================================================
sub tp_400 {
	$layout = 1;
	$mes .= "誰に何を送りますか?<br>国内手数料：$need_money G<br>国外手数料：$need_money_other G<br>";
	$mes .= 'お金を送る場合は金額を入力してください<br>';

	$mes .= qq|<form method="$method" action="$script"><p>送信先：<input type="text" name="send_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">[$weas[$m{wea}][2]]$weas[$m{wea}][1]★$m{wea_lv}($m{wea_c}/$weas[$m{wea}][4])<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">[卵]$eggs[$m{egg}][1]($m{egg_c}/$eggs[$m{egg}][2])<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">[ペ]$pets[$m{pet}][1]★$m{pet_c}<br>| if $m{pet} > 0;
	$mes .= qq|<input type="radio" name="cmd" value="4">[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>| if $m{gua};
	$mes .= qq|<input type="radio" name="cmd" value="5">お金<input type="text" name="send_money" value="0" class="text_box1" style="text-align:right">G<br>| if $m{money} > 0;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="送る" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_410 {
	return if &is_ng_cmd(1..5);
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方は送ることができません<br>";
		&begin;
		return;
	}
	elsif ($in{send_name} eq '') {
		$mes .= '送り先が記入されていません<br>';
		&begin;
		return;
	}
	elsif ($m{sedai} <= 1 && $m{lv} < $need_lv) {
		$mes .= "1世代目でﾚﾍﾞﾙ$need_lv未満の人は送ることができません<br>";
		&begin;
		return;
	}
	elsif ($cmd eq '1' && $m{wea_name}) {
		$mes .= "唯一無二の武器を送ることはできません<br>";
		&begin;
		return;
	}

	my $send_id = unpack 'H*', $in{send_name};
	my %datas = &get_you_datas($send_id, 1);
	
	# ここの処理を変えるところから
	if ($datas{is_full} && $cmd ne '5' && !&is_sabakan) {
		$mes .= "$in{send_name}の預かり所が満杯で送ることができません<br>";
		&begin;
		return;
	}
	
	my $pay = $datas{country} eq $m{country} ? $need_money : $need_money_other;
	
	if ($m{money} < $pay) {
		$mes .= "郵送手数料( $pay G)が足りません<br>";
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
			$mes .= "$t_item_nameは他の人に送ることはできません<br>";
			&begin;
			return;
		}
	}
	
	my %lock = &get_lock_item;
	my $check_line = $cmd eq '1' ? "$cmd<>$m{wea}<>"
					: $cmd eq '2' ? "$cmd<>$m{egg}<>"
					: $cmd eq '3' ? "$cmd<>$m{pet}<>"
					:               "$cmd<>$m{gua}<>"
					;
	if ($lock{$check_line}) {
			$mes .= "ロックされているアイテムは他の人に送ることはできません<br>";
			&begin;
			return;
	}
	
	if ($cmd eq '1' && $m{wea}) {
		&send_item($in{send_name}, $cmd, $m{wea}, $m{wea_c}, $m{wea_lv}, &is_sabakan);
		&mes_and_send_news("$in{send_name}に$weas[$m{wea}][1]を送りました");
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '2' && $m{egg}) {
		&send_item($in{send_name}, $cmd, $m{egg}, $m{egg_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}に$eggs[$m{egg}][1]を送りました");
		$m{egg} = $m{egg_c} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '3' && $m{pet}) {
		&send_item($in{send_name}, $cmd, $m{pet}, $m{pet_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}に$pets[$m{pet}][1]★$m{pet_c}を送りました");
		&remove_pet;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '4' && $m{gua}) {
		&send_item($in{send_name}, $cmd, $m{gua}, 0, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}に$guas[$m{gua}][1]を送りました");
		$m{gua} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '5' && $in{send_money} > 0 && $in{send_money} !~ /[^0-9]/) {
		if ($m{money} + $pay > $in{send_money}) {
			&send_money($in{send_name}, $m{name}, $in{send_money});
			&mes_and_send_news("$in{send_name}に $in{send_money} Gを送りました");
			$m{money} -= $in{send_money} + $pay;
		}
		else {
			$mes .= "手数料代も含めてお金が足りません<br>";
		}
	}
	&begin;
}

#=================================================
# ｼﾞｬﾝｸｼｮｯﾌﾟに売る
#=================================================
sub tp_500 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot;

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "どれを売りますか? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "どれを売りますか?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="売る" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_510 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}
	my($maxcount, $sub_mes) = &checkbox_my_depot;
	my $count = 0;
	my $is_rewrite = 0;
	my @junk = ();
	my @junk_log = ();
	my @depot_log = ();
	my %lock = &get_lock_item;
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($in{$count} eq '1') {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($count <= $lost_depot && $lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else { # 擦り切り対象のｱｲﾃﾑはロック無視
				$is_rewrite = 1;

				# ﾍﾟｯﾄだけ★情報追記 他は名前だけ
				my $l_mes = &get_item_name($kind, $item_no, $item_c);
				push @depot_log, "$l_mes";
				$mes .= "$l_mesを売りました<br>";
				$item_c = 0 if $kind eq '3'; # ｼﾞｬﾝｸにﾍﾟｯﾄを流す時はレベルを初期化
				$m{money} += $sall_price;

				# 大量に一括売却するとその数だけﾌｧｲﾙｵｰﾌﾟﾝするので1回で済むように変更
#				if (rand(2) < 1) {
					push @junk, "$kind<>$item_no<>$item_c<>\n";
#				}
				push @junk_log, "$kind<>$item_no<>$item_c<>$m{name}<>$time<>0<>\n";
				&penalty_depot($maxcount);
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		# 自分の倉庫の書き込み
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;
		close $fh;

		# ｼﾞｬﾝｸに書き込み
		open my $fh2, ">> $logdir/junk_shop.cgi" or &error("$logdir/junk_shop.cgiﾌｧｲﾙが開けません");
		print $fh2 @junk;
		close $fh2;

		# ｼﾞｬﾝｸﾛｸﾞに書き込み
		open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgiﾌｧｲﾙが開けません");
		print $fh3 @junk_log;
		close $fh3;
	}
	else {
		close $fh;
	}

	if ($is_rewrite) { # 繰り返しになるが、flock中のflockを回避するため
		&add_log("売却", @depot_log);
		&run_tutorial_quest('tutorial_junk_shop_sell_1');
	}

	&begin;
}

#=================================================
# 捨てる
#=================================================
sub tp_600 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot(0, 1);

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "どれを捨てますか? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "どれを捨てますか?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="捨てる" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_610 {
	my($maxcount, $sub_mes) = &radio_my_depot(0, 1);
	my $count = 0;
	my $is_rewrite = 0;
	my %lock = &get_lock_item;
	my $l_mes = "";
	open my $fh, "+< $this_file" or &error("$this_fileが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($cmd eq $count) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($count <= $lost_depot && $lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else { # 擦り切り対象のｱｲﾃﾑはロック無視
				$is_rewrite = 1;

				# ﾍﾟｯﾄだけ★情報追記 他は名前だけ
				$l_mes = &get_item_name($kind, $item_no, $item_c);
				$mes .= "$l_mesを捨てました<br>";
			}
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
	&add_log("破棄", $l_mes) if $is_rewrite;
	&begin;
}

#=================================================
# ロック
#=================================================
sub tp_700 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot_lock_checked;

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "どれをロックしますか? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "どれをロックしますか?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ロック" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_710 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}

	my %lock = (); # ロック情報

	# 倉庫内に存在しないのかアンロックしたのかの判断ができないとアンロックできない状態になりうる
	# 倉庫内でロック指定→以前からロック→ロック（正しい）
	# 倉庫内に存在しない→以前からロック→ロック（一見正しいがアンロックと判別しないとアンロックしてもされない）
	# 倉庫内でアンロック指定→以前からロック→アンロック（正しい）

	# ロック指定されたアイテムの取得
	open my $fh, "< $this_file" or &error("$this_fileが開けません");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if ($in{$count} eq '1' && $lock{"$kind<>$item_no<>"} == 0) {
			$lock{"$kind<>$item_no<>"} = 1; # ロック
		}
		elsif ($in{$count} == 0 && $lock{"$kind<>$item_no<>"} == 0) {
			$lock{"$kind<>$item_no<>"} = -1; # アンロック
		}
		# 倉庫内に存在しないアイテムについては従来のロック情報を利用↓
	}
	close $fh;

	# 従来のロック情報を取得しつつ更新
	open my $lfh, "+< $this_lock_file" or &error("$this_lock_fileが開けません");
	eval { flock $lfh, 2; };
	while (my $line = <$lfh>){
		chomp $line;
		$lock{$line} = 1 if $lock{$line} > -1; # アンロック指定されてないなら引き続きロック
	}

	seek  $lfh, 0, 0;
	truncate $lfh, 0;
	foreach my $line(keys(%lock)){
		if ($lock{$line} > 0) {
			print $lfh "$line\n";
		}
	}
	close $lfh;
	&begin;
}

#=================================================
# 履歴
#=================================================
sub tp_800 {
	if (-f "$this_log") {
		my @lines = ();
		open my $fh, "< $this_log" or &error("$this_logが開けません");
		while (my $line = <$fh>){
			$mes .= "$line<br>";
		}
		close $fh;
	}
	&begin;
}

#=================================================
# 罰金処理
#=================================================
sub penalty_depot {
	my $count = shift;
	return if $count eq '';

	if ($count > $max_depot) {
		$m{is_full} = 1;
		$mes .= "罰金 $penalty_money Gを支払いました<br>";
		$m{money} -= $penalty_money;
	}
	else {
		$m{is_full} = 0;
	}
}


#=================================================
# <input type="radio" 付の預かり所の物
#=================================================
sub radio_my_depot {
	my $no = shift; # 選択状態にするｱｲﾃﾑ番号 0 で「やめる」
	my $is_show = shift; # 溢れているｱｲﾑﾃを表示するかどうか
	my $count = 0;
	my %lock = &get_lock_item;
	my $sub_mes = qq|<form method="$method" action="$script">|;
	my $checked = " checked" unless $no;
	$sub_mes .= qq|<label><input type="radio" name="cmd" value="0"$checked>やめる</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if (!$is_show && $count > $lost_depot) {
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
		}
		else {
			$checked = $no == $count ? " checked" : "" ;
			$sub_mes .= qq|<label>| unless $is_mobile;
			$sub_mes .= qq|<input type="radio" name="cmd" value="$count"$checked>|;
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
			$sub_mes .= qq|</label>| unless $is_mobile;
			$sub_mes .= qq|<br>|;
		}
	}
	close $fh;

	$m{is_full} = $count >= $max_depot ? 1 : 0;

	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" 付の預かり所の物
#=================================================
sub checkbox_my_depot {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="チェックを外す" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="チェックを外す" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$sub_mes .= qq|<label>| unless $is_mobile;
		$sub_mes .= qq|<input type="checkbox" name="$count" value="1">|;
		my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
		$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" 付の預かり所の物
#=================================================
sub checkbox_my_depot_lock_checked {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="チェックを外す" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="チェックを外す" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	my %sames = ();
	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		# 重複するアイテムは最初の一個目だけ表示
		unless ($sames{"$kind<>$item_no<>"}) {
			$sub_mes .= qq|<label>| unless $is_mobile;
			$sub_mes .= qq|<input type="checkbox" name="$count" value="1"|;
			$sub_mes .= qq| checked| if $lock{"$kind<>$item_no<>"};
			$sub_mes .= qq|>|;
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
			$sub_mes .= qq|</label>| unless $is_mobile;
			$sub_mes .= qq|<br>|;
		}
		$sames{"$kind<>$item_no<>"}++;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
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

#=================================================
# 倉庫ﾛｸﾞ
# add_log("売りました", "item1"[, "item2", "item3"])
#=================================================
sub add_log {
	my $type = shift;
	my @items = @_;

	my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
	$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
	my $s_mes = "";
	for my $item (@items) {
		$s_mes .= "$item";
		$s_mes .= "," if @items > 1;
	}
	$s_mes = substr($s_mes, 0,  -1) if @items > 1;
	$s_mes .= "を$type($tdate)";

	if (-f $this_log) {
		open my $wfh, "+< $this_log";
		eval { flock $wfh, 2; };
		my @log_lines = ();
		my $log_count = 0;
		while (my $log_line = <$wfh>){ 
			push @log_lines, $log_line;
			$log_count++;
			last if $log_count > 30;
		}
		unshift @log_lines, "$s_mes\n";
		seek  $wfh, 0, 0;
		truncate $wfh, 0;
		print $wfh @log_lines;
		close $wfh;
	}
	else {
		open my $wfh, "> $this_log";
		print $wfh "$s_mes\n";
		close $wfh;
	}
}

#=================================================
# アイテムデータの表示
#=================================================
sub show_item_datas {
	my ($item_name, $is_lock, $is_over) = @_;
	my $item_datas = '';
	$item_datas .= $item_name;
	$item_datas .= qq|<img src="$icondir/emoji/1f512.png" width="14px" height="14px">| if $is_lock;
	$item_datas .= ' 溢れてます' if $is_over;
	return $item_datas;
}

1; # 削除不可
