my $this_file = "$logdir/$m{country}/depot_b.cgi";
my $this_log = "$logdir/$m{country}/depot_b_log.cgi";
#=================================================
# V‹K—p‘ŒÉ
#=================================================

# Å‘å•Û‘¶”
my $max_depot = 10;

# —a‚¯‚ç‚ê‚È‚¢±²ÃÑ
my %taboo_items = (
	wea => [32,], # •Ší
	egg => [], # ÀÏºŞ
	pet => [127,138,188], # Íß¯Ä
	gua => [], # –h‹ï
);

sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '‘‚É‘®‚µ‚Ä‚È‚¢‚Æs‚¤‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}
#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "‘¼‚É‰½‚©‚µ‚Ü‚·‚©?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "‚±‚±‚ÍV‹K—p‘ŒÉ‚Å‚·B$max_depotŒÂ‚Ü‚Å—a‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
		$mes .= "‚Ç‚¤‚µ‚Ü‚·‚©?<br>";
	}
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_log‚ªŠJ‚¯‚Ü‚¹‚ñ");
		close $fh;
	}
	&menu('‚â‚ß‚é', 'ˆøo‚·', '—a‚¯‚é', '®—‚·‚é','—š—ğŠm”F');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ˆøo‚·
#=================================================
sub tp_100 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot;

	$mes .= "‚Ç‚ê‚ğˆøo‚µ‚Ü‚·‚©? [ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .=  $is_mobile ? qq|<p><input type="submit" value="ˆøo‚·" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="ˆøo‚·" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $flag = 1;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				
				if ($kind eq '1' && $m{wea}) {
					$mes .= "Šù‚É•Ší‚ğŠ‚µ‚Ä‚¢‚Ü‚·";
					$flag = 0;
				}
				elsif ($kind eq '2' && $m{egg}) {
					$mes .= "Šù‚É—‘‚ğŠ‚µ‚Ä‚¢‚Ü‚·";
					$flag = 0;
				}
				elsif($kind eq '3' && $m{pet}) {
					$mes .= "Šù‚ÉÍß¯Ä‚ğŠ‚µ‚Ä‚¢‚Ü‚·";
					$flag = 0;
				}
				elsif($kind eq '4' && $m{gua}) {
					$mes .= "Šù‚É–h‹ï‚ğŠ‚µ‚Ä‚¢‚Ü‚·";
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
				$mes .= "$weas[$m{wea}][1]‚ğˆøo‚µ‚Ü‚µ‚½<br>";
			}
			elsif ($kind eq '2') {
				$m{egg}    = $item_no;
				$m{egg_c}  = $item_c;
				$mes .= "$eggs[$m{egg}][1]‚ğˆøo‚µ‚Ü‚µ‚½<br>";
			}
			elsif ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚ğˆøo‚µ‚Ü‚µ‚½<br>";

				if (-f "$userdir/$id/pet_icon.cgi") {
					open my $ifh, "< $userdir/$id/pet_icon.cgi";
					my $line = <$ifh>;
					close $ifh;
					if (index($line, "<>$m{pet}_") >= 0) {
						$line =~ s/.*<>($m{pet}_.*?)<>.*/$1/;
						$m{icon_pet} = $line;
					}
					else {
						$m{icon_pet} = '';
					}
				}
			}
			elsif ($kind eq '4') {
				$m{gua}    = $item_no;
				$mes .= "$guas[$m{gua}][1]‚ğˆøo‚µ‚Ü‚µ‚½<br>";
			}

			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
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

			# ˆøo‚·À²Ğİ¸Ş‚ÅV‚µ‚¢±²ÃÑ‚ª‚ ‚ê‚ÎºÚ¸¼®İ‚É’Ç‰Á
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
# —a‚¯‚é
#=================================================
sub tp_200 {
	$mes .= '‚Ç‚ê‚ğ—a‚¯‚Ü‚·‚©?';
	
	my @menus = ('‚â‚ß‚é');
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
		$mes .= "—Bˆê–³“ñ‚Ì•Ší‚ğ—a‚¯‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
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
			$mes .= "$t_item_name‚Í—a‚¯‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
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
	open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	push @lines, $_ while <$fh>;
	
	if (@lines >= $max_depot) {
		close $fh;
		$mes .= '‚±‚êˆÈã—a‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>';
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
				$mes .= "‚¿å‚Ìè‚ğ—£‚ê‚½“r’[$m{wea_name}‚Í‚½‚¾‚Ì$weas[$m{wea}][1]‚É‚È‚Á‚Ä‚µ‚Ü‚Á‚½";
				$m{wea_name} = "";
			}
			$mes .= "$weas[$m{wea}][1]‚ğ—a‚¯‚Ü‚µ‚½<br>";
			$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		}
		elsif ($cmd eq '2') {
			$mes .= "$eggs[$m{egg}][1]‚ğ—a‚¯‚Ü‚µ‚½<br>";
			$m{egg} = $m{egg_c} = 0;
		}
		elsif ($cmd eq '3') {
			$mes .= "$pets[$m{pet}][1]š$m{pet_c}‚ğ—a‚¯‚Ü‚µ‚½<br>";
			$m{pet} = 0;
			$m{icon_pet} = '';
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]‚ğ—a‚¯‚Ü‚µ‚½<br>";
			$m{gua} = 0;
		}
		
			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
# ®—
#=================================================
sub tp_300 {
	my @lines = ();
	my $n_egg = 0;
	my $n_man = 0;
	my $n_hero = 0;	
	open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
	
	$mes .= "—a‚¯‚Ä‚¢‚é‚à‚Ì‚ğ®—‚µ‚Ü‚µ‚½<br>";
	&begin;
}

#=================================================
# ƒƒOŠm”F
#=================================================
sub tp_400 {
	my @lines = ();
	open my $fh, "< $this_log" or &error("$this_log‚ªŠJ‚¯‚Ü‚¹‚ñ");
	while (my $line = <$fh>){
		my($kind, $item_no, $item_c, $item_lv, $name, $type) = split /<>/, $line;
		$mes .= "$name ‚ª";
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$mes .= "‚ğ";
		$mes .= $type eq '1' ? "—a‚¯‚Ü‚µ‚½<br>":
					$type eq '0' ? "ˆø‚«o‚µ‚Ü‚µ‚½<br>":
								"’D‚¢‚Ü‚µ‚½<br>";
	}
	close $fh;
	&begin;
}

#=================================================
# <input type="radio" •t‚Ì—a‚©‚èŠ‚Ì•¨
#=================================================
sub radio_my_depot {
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_log‚ªŠJ‚¯‚Ü‚¹‚ñ");
		close $fh;
	}
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">‚â‚ß‚é</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
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

1; # íœ•s‰Â
