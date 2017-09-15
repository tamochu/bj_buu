#=================================================
# 黒十字病院 Created by Merino
#=================================================

# ------------------
# 整形手術のｱｲｺﾝ表示
# [PC]一覧表示の折り返し数
my $tr = 10;

# [携帯]１ﾍﾟｰｼﾞの表示数
my $max_mobile_icon = 30;

# ------------------
# ﾍﾞｰｽとなる金額
my $base_price = $m{sedai} > 8 ? 400 + ($m{lv} * 10) : ($m{sedai} * 50) + ($m{lv} * 10);

# ﾒﾆｭｰ
my @menus = (
	# ﾒﾆｭｰ名,		値段
	['やめる',		0],
	['治癒',		$base_price * 20],
	['性転換手術',	$base_price * 50],
	['ﾛﾎﾞﾄﾐｰ手術',	500000],
	['整形手術',	1000], # ｱｲｺﾝを使わない場合はこの行と sub tp_400以降を削除してOK
	['首輪交換',	1000], # ｱｲｺﾝを使わない場合はこの行と sub tp_400以降を削除してOK
	['符牒更新',	10000], # ｱｲｺﾝを使わない場合はこの行と sub tp_400以降を削除してOK
);


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますかぁ?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '黒十字病院へようこそぉ<br>本日はどのようなご用件でしょぅかぁ?';
	}
	
	&menu(map { $_->[0] } @menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# 治癒
#================================================
sub tp_100 {
	$mes .= "$menus[1][0]わぁ、貴方の傷を癒すことができるわよぉ<br>";
	$mes .= "ただしぃ、$menus[1][1] Gのお金がかかるのぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[1][0]する");
}
sub tp_110 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[1][1]) {
		$mes .= "西洋の神秘の力を使って貴方の体を癒すわよぉ<br>";
		$mes .= "そぉれ、ﾊｯｽﾙｩ～ﾊｯｽﾙｩ～♪元気になったでしょ<br>";
		$mes .= "あたしが必要になったらまた来てね<br>";
		$m{hp} = $m{max_hp};
		$m{mp} = $m{max_mp};
		$m{money} -= &use_pet('hospital',$menus[1][1]);
		&run_tutorial_quest('tutorial_hospital_1');
		&refresh;
		&n_menu;
	}
	else {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
	}
}

#================================================
# 性転換
#================================================
sub tp_200 {
	$mes .= "$menus[2][0]をすると、$sexes[$m{sex}]じゃなくなっちゃうけどいいのかしらぁ?<br>";
	$mes .= "手術をするには、$menus[2][1] Gと手術時間$GWT分必要よぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[2][0]する");
}
sub tp_210 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[2][1]) {
		$mes .= '麻酔を打って手術を始めるわね<br>';
		$mes .= '次に目覚めたときにわぁ別人となっているわよぉ<br>';
		$m{sex} = $m{sex} eq '1' ? 2 : 1;
		$m{hp}  = $m{max_hp};
		$m{mp}  = $m{max_mp};
		$m{act} = 0;
		$m{money} -= $menus[2][1];
		if ($m{job} eq '22' || $m{job} eq '23') {
			$m{job} = 0;
		}
		&refresh;
		&wait;
		&write_memory("意を決して $sexes[$m{sex}] に性転換手術をしました");
	}
	else {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
	}
}

#================================================
# ﾛﾎﾞﾄﾐｰ手術
#================================================
sub tp_300 {
	$mes .= "$menus[3][0]をするとぉ、貴方のお名前やﾊﾟｽﾜｰﾄﾞを変えることができるわぁ<br>";
	$mes .= "ただしﾄ･ｸ･ﾍﾞ･ﾂな大手術だからぁ、$cs{name}[0]の方しかすることができないのぉ<br>" if $m{country};
	$mes .= "手術をするには、$menus[3][1] Gと手術時間$GWT分必要よぉ<br>";
	$mes .= "手術をするとぉ、現在利用している銀行のお金はなくなってしまうわよぉ<br>" if $m{bank};
	$mes .= "どぉするぅ？";
	if (&on_summer) {
		$mes .= qq|<hr><font color="red">※イベント中に改名すると不具合が起きる可能性があります(名前で管理していることがあるため)</font>|;
	}
	else {
		$mes .= "<br>";
	}

	$m{tp} += 10;
	&menu("やめる", "$menus[3][0]する");
}
sub tp_310 {
	return if &is_ng_cmd(1);
	if ($m{country}) {
		$mes .= "$cs{name}[0]になってからぁ、また来てね<br>";
		&begin;
		return;
	}

	my $auction_file = "$logdir/auction.cgi";
	my $is_entry = 0;
	open my $fh, "< $auction_file" or &error("$auction_fileが読み込めません");
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
		$is_entry = 1 if $m{name} eq $to_name;
	}
	close $fh;
	if ($is_entry) {
		$mes .= "ｵｰｸｼｮﾝで入札中の方はぁ、それが済んでから来てね<br>";
		&begin;
		return;
	}


	$mes .= qq|それでわぁ、新しいお名前とﾊﾟｽﾜｰﾄﾞを教えてね<br>|;
	$mes .= qq|<form method="GET" action="$script"><table class="table1">|;
	$mes .= qq|<tr><td><tt>ﾌﾟﾚｲﾔ-名：</tt></td><td><input type="text" name="new_name" value="$m{name}" class="text_box1"><br></td></tr>|;
	$mes .= qq|<tr><td><tt>ﾊﾟｽﾜｰﾄﾞ ：</tt></td><td><input type="text" name="new_pass" value="$m{pass}" class="text_box1"><br></td></tr>|;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="確定" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_320 {
	if ($m{country}) {
		$mes .= "$cs{name}[0]になってからぁ、また来てね<br>";
		&begin;
		return;
	}
	elsif ($m{money} < $menus[3][1]) {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
		return;
	}
	elsif (!$in{new_name} && $in{new_pass} eq '') {
		&begin;
		return;
	}
	elsif ($in{new_name} eq $m{name} && $in{new_pass} eq $m{pass}) {
		&begin;
		return;
	}

	&error('ﾌﾟﾚｲﾔ-名が入力されていません')	unless $in{new_name};
	&error('ﾊﾟｽﾜｰﾄﾞが入力されていません')	if $in{new_pass} eq '';

	&error('ﾌﾟﾚｲﾔ-名に不正な文字( ,;\"\'&<>\\\/ )が含まれています')	if $in{new_name} =~ /[,;\"\'&<>\\\/]/;#"
	&error('ﾌﾟﾚｲﾔ-名に不正な空白が含まれています')				if $in{new_name} =~ /　/ || $in{new_name} =~ /\s/;
	&error('ﾌﾟﾚｲﾔ-名は全角6(半角12)文字以内です')				if length($in{new_name}) > 12;
	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字で入力して下さい')				if $in{new_pass} =~ m/[^0-9a-zA-Z]/;
	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字4～12文字です')					if length $in{new_pass} < 4 || length $in{new_pass} > 12;
	&error('ﾌﾟﾚｲﾔ-名とﾊﾟｽﾜｰﾄﾞが同一文字列です')					if $in{new_name} eq $in{new_pass};

	unless ($m{name} eq $in{new_name}) {
		my $new_id = unpack 'H*', $in{new_name};
		&error('その名前はすでに使われています') if -d "$userdir/$new_id";
		&write_world_news("$m{name} が $in{new_name} と改名をしました", 1);

		rename "$userdir/$id", "$userdir/$new_id" or &error('名前の変換に失敗しました');

		my @lines = ();
		open my $fh, "+< $logdir/0/member.cgi" or &error("$cs{name}[0]のﾒﾝﾊﾞｰﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			next if $line eq $m{name};
			push @lines, "$line\n";
		}
		push @lines, "$in{new_name}\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		# 夏イベ中はラヂオ体操のログも書き換える(他はとりあえず知らん)
		if (&on_summer) {
			my $this_radio_dir = "$logdir/summer_radio";
			for my $d (1..31) {
				if (-f "$this_radio_dir/$d.cgi") {
					my @members = ();
					open my $fh, "+< $this_radio_dir/$d.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
					eval { flock $fh, 2; };
					while (my $line = <$fh>) {
						my ($mname, $mtime) = split /<>/, $line;
						if ($mname eq $m{name}) {
							push @members, "$in{new_name}<>$mtime<>\n";
						}
						else {
							push @members, "$mname<>$mtime<>\n";
						}
					}
					seek  $fh, 0, 0;
					truncate $fh, 0;
					print $fh @members;
					close $fh;
				}
			}
		}

		$id = $new_id;
		$m{name} = $in{new_name};
		$mes .= qq|<font color="#FF0000">新ﾌﾟﾚｲﾔｰ名:$in{new_name}</font><br>|;
	}

	unless ($m{pass} eq $in{new_pass}) {
		$m{pass} = $in{new_pass};
		$pass    = $in{new_pass};
		$mes .= qq|<font color="#FF0000">新ﾊﾟｽﾜｰﾄﾞ:$in{new_pass}</font><br>|;
	}
	
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
	$m{act} = 0;
	$m{bank} = '';
	$m{money} -= $menus[3][1];
	&refresh;
	&wait;
	
	$mes .= qq|昔の貴方はもう存在しないわぁ<br><font color="#FF0000"><b>新しい名前とﾊﾟｽﾜｰﾄﾞを忘れないようにね</b></font><br>|;
	$mes .= qq|[次回から入力省略]にﾁｪｯｸを入れいている人わぁ、一度ﾛｸﾞｲﾝし直した方がいいわよぉ<br>| unless $is_mobile;
}

#================================================
# 整形
#================================================
sub tp_400 {
	if ($default_icon eq '') {
		$mes .= 'ごめんなさぁい。この病院には整形のﾄﾞｸﾀｰがいないのぉ<br>';
		&begin;
		return;
	}
	if ($m{icon_t} ne '') {
		$mes .= 'そんないい顔変えちゃうなんてもったいないわぁ<br>';
		&begin;
		return;
	}
	$mes .= "$menus[4][0]は、貴方の顔をまったくの別人にしちゃうわよぉ<br>";
#	$mes .= "今使用している顔ｶﾀﾛｸﾞは、ﾏｲﾋﾟｸﾁｬに戻るわよぉ<br>" if -f "$icondir/$m{icon}";
	$mes .= "手術をするには、$menus[4][1] Gと手術時間$GWT分かかりますけどぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "自分のｱｲｺﾝに$menus[4][0]する", "ﾃﾞﾌｫﾙﾄｱｲｺﾝに$menus[4][0]する");
}
sub tp_410 {
	return if &is_ng_cmd(1..2);
	if ($default_icon eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	$mes .= 'どのようなお顔にしますぅ?<br>ｶﾀﾛｸﾞからお選びくださぁい<br>';
	unless ($m{icon} eq $default_icon) {
		my $file_title = &get_goods_title($m{icon});
		$mes .= "現在の顔ｱｲｺﾝﾀｲﾄﾙ『$file_title』<br>";
	}

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> やめる<hr>|;
	
	if($cmd eq '1'){
		opendir my $dh, "$userdir/$id/picture" or &error('ﾏｲﾋﾟｸﾁｬが開けません');
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /^_/;
			next if $file_name =~ /\.html$/;

			my $file_title = &get_goods_title($file_name);
			$mes .= qq|<input type="radio" name="icon" value="$file_name"><img src="$userdir/$id/picture/$file_name" $mobile_icon_size> $file_title<hr>|;
		}
		closedir $dh;
	}
	
	$mes .= qq|<input type="radio" name="icon" value="$default_icon"><img src="$icondir/$default_icon" $mobile_icon_size> ﾃﾞﾌｫﾙﾄ<hr>|;

	if($cmd eq '2'){
		my %add_num = ();
		open my $fh, "< $logdir/add_icon_number.cgi" or &error('ｱｲｺﾝﾘｽﾄが開けません');
		while (my $line = <$fh>) {
			my($i_name, $number) = split /<>/, $line;
			$add_num{$i_name} = $number;
		}
		close $fh;

		my $icon_no;
		$icon_no = 0;
		opendir my $dh_d, "$icondir" or &error('ﾃﾞﾌｫﾙﾄﾋﾟｸﾁｬが開けません');
		while (my $file_name_d = readdir $dh_d) {
			next if $file_name_d =~ /^\./;
			next if $file_name_d =~ /\.html$/;

			if ($file_name_d =~ /^_add/){
				my $file_title_d = "No.$icon_no";
				$file_title_d .= ":$add_num{$file_name_d}人";
				$mes .= qq|<input type="radio" name="icon" value="$file_name_d"><img src="$icondir/$file_name_d" $mobile_icon_size> $file_title_d<hr>|;
				$icon_no++;
			}
		}
		closedir $dh_d;
	}


	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="決定" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_420 {
	if ($default_icon eq '') {
		&begin;
		return;
	}

	if ($in{icon} && ($in{icon} eq $default_icon || -f "$icondir/$in{icon}" || -f "$userdir/$id/picture/$in{icon}") ) {
		if ($m{money} >= $menus[4][1]) {
			# 自作ｱｲｺﾝ
			unless ($in{icon} eq $default_icon || $in{icon} =~ /^_add/) {
				&error("$non_titleのものは整形することができません") if $in{icon} =~ /^_/;
				&error("同じﾀｲﾄﾙのものがすでに使われています") if -f "$icondir/$in{icon}";
				
				rename "$userdir/$id/picture/$in{icon}", "$icondir/$in{icon}"  or &error("あらやだ、整形に失敗しちゃったわぁ");
			}

			# 変更前のｱｲｺﾝが自作ｱｲｺﾝならﾏｲﾋﾟｸﾁｬに戻す
			if($m{icon} =~ /^_add/){
				my %add_num = ();
				my @lines = ();
				my $new = 1;
				open my $fh, "+< $logdir/add_icon_number.cgi" or &error('ｱｲｺﾝﾘｽﾄが開けません');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($i_name, $number) = split /<>/, $line;
					if($i_name eq $in{icon}){
						$number--;
						$number = 0 if $number < 0;
						$new = 0;
					}
					push @lines, "$i_name<>$number<>\n";
				}
				if($new){
					push @lines, "$in{icon}<>0<>\n";
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}elsif ($m{icon} ne $default_icon && -f "$icondir/$m{icon}") {
				if (-f "$userdir/$id/picture/$m{icon}") {
					$mes .= "同じﾀｲﾄﾙの絵がﾏｲﾋﾟｸﾁｬにあったため、変更前の顔ｶﾀﾛｸﾞは消滅しました<br>";
				}
				else {
					rename "$icondir/$m{icon}", "$userdir/$id/picture/$m{icon}" or &error("あらやだ、整形に失敗しちゃったわぁ");
					my $file_title = &get_goods_title($m{icon});
					$mes .= "変更前に使用していた『$file_title』がﾏｲﾋﾟｸﾁｬに戻りました<br>";
				}
			}


			$m{icon} = $in{icon};

			$mes .= '麻酔を打って手術を始めるわね<br>';
			$mes .= '次に目覚めたときにわぁ別人となっているわよぉ<br>';
			
			$m{hp}  = $m{max_hp};
			$m{mp}  = $m{max_mp};
			$m{act} = 0;
			$m{money} -= $menus[4][1];
			if($in{icon} =~ /^_add_/){
				my $img_name = $in{icon};
				$img_name =~ s/^_add_//;
				my $img_title = &get_goods_title($img_name);
				$img_title =~ s/.*作://;
				&send_money($img_title,'印税収入として黒十字病院',$menus[4][1]*0.3);
				my @lines = ();
				my $new = 1;
				open my $fh, "+< $logdir/add_icon_number.cgi" or &error('ｱｲｺﾝﾘｽﾄが開けません');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($i_name, $number) = split /<>/, $line;
					if($i_name eq $in{icon}){
						$number++;
						$new = 0;
					}
					push @lines, "$i_name<>$number<>\n";
				}
				if($new){
					push @lines, "$in{icon}<>1<>\n";
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}
			&refresh;
			&wait;
		}
		else {
			$mes .= 'あらぁ、お金が足りませんわぁ<br>';
			&begin;
		}
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#================================================
# 首輪
#================================================
sub tp_500 {
	if ($default_icon eq '') {
		$mes .= 'ごめんなさぁい。この病院には獣医がいないのぉ<br>';
		&begin;
		return;
	}
	elsif ($pets[$m{pet}][0] == 0) {
		$mes .= 'ごめんなさぁい。まずはﾍﾟｯﾄを連れてきてね<br>';
		&begin;
		return;
	}
	elsif ($pets[$m{pet}][0] < 0) {
		$mes .= 'ごめんなさぁい。そのﾍﾟｯﾄには首輪は似合わないわぁ<br>';
		&begin;
		return;
	}
	$mes .= "$menus[5][0]は、貴方のﾍﾟｯﾄの個性をチョイアゲ↑しちゃうわよぉ<br>";
	$mes .= "首輪を交換するには、$menus[5][1] Gかかりますけどぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[5][0]する");
}
sub tp_510 {
	return if &is_ng_cmd(1);
	if ($default_icon eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	$mes .= 'どのような首輪にしますぅ?<br>ｶﾀﾛｸﾞからお選びくださぁい<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> やめる<hr>|;

	$mes .= qq|<input type="radio" name="icon" value="1">首輪を外す<hr>|;

	if($cmd eq '1'){
		opendir my $dh, "$icondir/pet" or &error('ﾍﾟｯﾄﾌｫﾙﾀﾞが開けません');
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /\.html$/;
			# ﾀﾞｯﾁﾜｲﾌじゃないなら手持ちのﾍﾟｯﾄのｱｲｺﾝのみ ﾀﾞｯﾁﾜｲﾌならすべてのﾍﾟｯﾄのｱｲｺﾝ
			unless (($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24') && ($m{boch_pet} && $m{pet})) {
				next unless $file_name =~ /^$m{pet}_/;
			}

			my $checked = " checked=\"checked\"" if $file_name eq $m{icon_pet};

			# ちょっと行き当たりばったりの強引
			my $name = $file_name;
			my $pet_n = $file_name;
			$pet_n =~ s/^(\d+)_.*/\1/;
			my $petname = ($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24') && ($m{boch_pet} && $m{pet}) ? $pets[$pet_n][1] : '';
			$name =~ s/^\d+_//;
			my $file_title = &get_goods_title($name);
			$file_title =~ s/.*?\s//;
			$mes .= qq|<input type="radio" name="icon" value="$file_name"$checked><img src="$icondir/pet/$file_name" $mobile_icon_size>$petname $file_title<hr>|;
		}
		closedir $dh;
	}

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="決定" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_520 {
	if ($default_icon eq '') {
		&begin;
		return;
	}

	if ($in{icon} && ($in{icon} == 1)) {
		$m{icon_pet} = '';
		$m{icon_pet_lv} = 0;
		$m{icon_pet_exp} = 0;
		$mes .= '外した首輪はこっちで回収しておくわね<br>';

		my $id = unpack 'H*', $m{name};
		my $this_file = "$userdir/$id/pet_icon.cgi";
		if (-f "$this_file") {
			open my $fh, "+< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			my $line = <$fh>;
			if(index($line, "<>$m{pet};") >= 0){
				$line =~ s/<>($m{pet});.*?;(.*?);(.*?)<>/<>$1;$m{icon_pet};$2;$3<>/;
			}else{
				$line = $line . "$m{pet};$m{icon_pet};1;22<>";
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh $line;
			close $fh;
		}

		&refresh;
		&n_menu;
	}
	elsif ($in{icon} && ($in{icon} eq $m{icon_pet})) {
		$mes .= 'やめました<br>';
		&begin;
	}
	elsif ($in{icon} && (-f "$icondir/pet/$in{icon}") ) {
		if ($m{money} >= $menus[5][1]) {
			$m{icon_pet} = $in{icon};

			$mes .= 'これであなたのﾍﾟｯﾄもイケイケ↑よぉ<br>';

			$m{money} -= $menus[5][1];

			# ちょっと行き当たりばったりの強引
			my $file_name = $in{icon};
			$file_name =~ s/^\d+_//;
			my $name = &get_goods_title($file_name);
			$name =~ s/.*作://; # 作者名
			&send_money($name,'印税収入として黒十字病院',$menus[5][1]*0.3);

			my $id = unpack 'H*', $m{name};
			my $this_file = "$userdir/$id/pet_icon.cgi";
			if (-f "$this_file") {
				open my $fh, "+< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
				eval { flock $fh, 2; };
				my $line = <$fh>;
				if(index($line, "<>$m{pet};") >= 0){
					$line =~ s/<>($m{pet});.*?;(.*?);(.*?)<>/<>$1;$m{icon_pet};$2;$3<>/;
					$m{icon_pet_lv} = $2;
					$m{icon_pet_exp} = $3;
				}else{
					$line = $line . "$m{pet};$m{icon_pet};1;22<>";
					$m{icon_pet_lv} = 1;
					$m{icon_pet_exp} = 22;
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
				close $fh;
			}
			else {
				open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
				print $fh "<>$m{pet};$m{icon_pet};1;22<>";
				close $fh;
				$m{icon_pet_lv} = 1;
				$m{icon_pet_exp} = 22;
			}

			&refresh;
			&n_menu;
		}
		else {
			$mes .= 'あらぁ、お金が足りませんわぁ<br>';
			&begin;
		}
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#================================================
# 符牒更新
#================================================
sub tp_600 {
	$mes .= "$menus[6][0]をするとぉ、貴方のﾊﾟｽﾜｰﾄﾞを変えることができるわぁ<br>";
	$mes .= "変更をするには、$menus[6][1] G必要よぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[6][0]する");
}
sub tp_610 {
	return if &is_ng_cmd(1);

	$mes .= qq|それでわぁ、新しいお名前とﾊﾟｽﾜｰﾄﾞを教えてね<br>|;
	$mes .= qq|<form method="GET" action="$script"><table class="table1">|;
	$mes .= qq|<tr><td><tt>ﾊﾟｽﾜｰﾄﾞ ：</tt></td><td><input type="text" name="new_pass" value="$m{pass}" class="text_box1"><br></td></tr>|;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="確定" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_620 {
	if ($m{money} < $menus[6][1]) {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
		return;
	}
	elsif ($in{new_pass} eq '') {
		&begin;
		return;
	}
	elsif ($in{new_pass} eq $m{pass}) {
		&begin;
		return;
	}

	&error('ﾊﾟｽﾜｰﾄﾞが入力されていません')	if $in{new_pass} eq '';

	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字で入力して下さい')				if $in{new_pass} =~ m/[^0-9a-zA-Z]/;
	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字4～12文字です')					if length $in{new_pass} < 4 || length $in{new_pass} > 12;
	&error('ﾌﾟﾚｲﾔ-名とﾊﾟｽﾜｰﾄﾞが同一文字列です')					if $m{name} eq $in{new_pass};

	unless ($m{pass} eq $in{new_pass}) {
		$m{pass} = $in{new_pass};
		$pass    = $in{new_pass};
		$mes .= qq|<font color="#FF0000">新ﾊﾟｽﾜｰﾄﾞ:$in{new_pass}</font><br>|;
	}
	
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
#	$m{act} = 0;
	$m{money} -= $menus[6][1];
	&refresh;
	&n_menu;

	$mes .= qq|昔のﾊﾟｽﾜｰﾄﾞではもうログインできないないわぁ<br><font color="#FF0000"><b>新しいﾊﾟｽﾜｰﾄﾞを忘れないようにね</b></font><br>|;
	$mes .= qq|[次回から入力省略]にﾁｪｯｸを入れいている人わぁ、一度ﾛｸﾞｲﾝし直した方がいいわよぉ<br>| unless $is_mobile;
}

1; # 削除不可
