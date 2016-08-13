my $this_file = "$logdir/$m{country}/depot.cgi";
my $this_log = "$logdir/$m{country}/depot_log.cgi";
#=================================================
# ‘ŒÉ
#=================================================

# Å‘å•Û‘¶”
my $max_depot = 30;

# —˜—p‰Â”\‚ÈÚÍŞÙ(‚½‚¾‚µ1¢‘ã‚Ì‚İ)
my($need_lv, $need_sedai, $top_message) = &status_check;

$need_lv ||= 5;

# —˜—p‰Â”\‚È¢‘ã
$need_sedai ||= 1;

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
	$mes .= "—˜—p‰Â”\\¢‘ãF$need_sedai ƒŒƒxƒ‹F$need_lv<br>$top_message<br>";
	if ($m{tp} > 1) {
		$mes .= "‘¼‚É‰½‚©‚µ‚Ü‚·‚©?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "‚±‚±‚Í‘ŒÉ‚Å‚·B$max_depotŒÂ‚Ü‚Å—a‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
		$mes .= "‚Ç‚¤‚µ‚Ü‚·‚©?<br>";
	}
	&menu('‚â‚ß‚é', 'ˆøo‚·', '—a‚¯‚é', '®—‚·‚é','—š—ğŠm”F', 'V‹K—p');
#	&menu('‚â‚ß‚é', 'ˆøo‚·', '—a‚¯‚é', '®—‚·‚é','—š—ğŠm”F','—ª’D');
}
sub tp_1 {
#	return if &is_ng_cmd(1..5);
	return if &is_ng_cmd(1..5);
	
	if ($cmd eq '5') {
		$m{lib} = 'depot_country_beginner';
		$mes .= "‚±‚±‚ÍV‹K—p‘ŒÉ‚Å‚·B10ŒÂ‚Ü‚Å—a‚¯‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
		$mes .= "‚Ç‚¤‚µ‚Ü‚·‚©?<br>";
		&menu('‚â‚ß‚é', 'ˆøo‚·', '—a‚¯‚é', '®—‚·‚é','—š—ğŠm”F');
	} else {
		$m{tp} = $cmd * 100;
		&{ 'tp_'. $m{tp} };
	}
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
	if ($m{sedai} < $need_sedai || ($m{sedai} == $need_sedai && $m{lv} < $need_lv)) {
		$mes .= "$need_sedai ¢‘ãÚÍŞÙ$need_lv–¢–‚Ìl‚Íg‚¤‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
	} else {
		if ($cmd) {
			my $count = 0;
			my $new_line = '';
			my $flag = 1;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $fh, 2; };
			my $head_line = <$fh>;
			push @lines, $head_line;
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
	
	if (@lines >= $max_depot+1) {
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
	my $head_line = <$fh>;
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
	unshift @lines, $head_line;
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
# —ª’D
#=================================================
sub tp_600 {
	$mes .= "‚Ç‚Ì‘‚Ì‘ŒÉ‚ğPŒ‚‚µ‚Ü‚·‚©?($GWT•ª)<br>";
	&menu('‚â‚ß‚é', @countries);
	$m{tp} += 10;
}

sub tp_610 {
	return if &is_ng_cmd(1..$w{country});
	
	if ($m{country} eq $cmd) {
		$mes .= '©‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '“¯–¿‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd] ne '1') {
		$mes .= '–Å–S‚µ‚Ä‚¢‚È‚¢‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;
		
		$mes .= "$cs{name}[$y{country}]‚ÉŒü‚©‚¢‚Ü‚µ‚½<br>";
		$mes .= "$GWT•ªŒã‚É“’…‚·‚é—\\’è‚Å‚·<br>";
		
		&wait;
	}
}

sub tp_620 {
	$mes .= "$c_y‚É“’…‚µ‚Ü‚µ‚½<br>";
	$m{tp} += 10;
	$m{value} = int(rand(20))+5;
	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "“G•º‚Ì‹C”zy $m{value}% z<br>";
	$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
	&menu('—ª’D‚·‚é','ˆø‚«‚ ‚°‚é');
	$m{value} += int(rand(10)+1);
}

sub loop_menu {
	$mes .= "“G•º‚Ì‹C”zy $m{value}% z<br>";
	$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?';
	&menu('‘±‚¯‚é', '‚â‚ß‚é');
}

sub tp_630 {
	if ($cmd eq '0') { # Às
		if ( $m{value} > rand(110)+35 ) { # ¸”s ’Pƒ‚Érand(100)‚É‚·‚é‚Æ30%‚­‚ç‚¢‚ÅŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚¤‚Ì‚Å rand(110)+30‚É•ÏX
			$mes .= "“G•º‚ÉŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚Á‚½!!<br>";
			
			$m{tp} = 560;
			&n_menu;
		}
		else { # ¬Œ÷
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			&loop_menu;
			$m{tp} -= 10;
		}
		$m{value} += int(rand(10)+1);
	}
	elsif ($cmd eq '1') { # ‘Ş‹p
		$mes .= 'ˆø‚«ã‚°‚é‚±‚Æ‚É‚µ‚Ü‚·<br>';
		
		if ($m{turn} <= 0) { # ‰½‚à‚µ‚È‚¢‚Åˆø‚«ã‚°
			&refresh;
			&n_menu;
		}
		else {
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 570;
			&n_menu;
		}
	}
	else {
		&loop_menu;
	}
}


sub tp_640{
	$mes .= "‘ŒÉ‚ğ’T‚è‚Ü‚µ‚½!<br>[ ˜A‘±$m{turn}‰ñ¬Œ÷]<br>";
}

sub tp_650 {
	if(int(rand(1)) < $m{turn}) {
		my $count = 0;
		my $new_line = '';
		my @lines = ();
		my $number = int(rand(100));
		open my $fh, "+< $logdir/$y{country}/depot.cgi" or &error("$logdir/$y{country}/depot.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		my $head_line = <$fh>;
		push @lines, $head_line;
		while (my $line = <$fh>) {
			++$count;
			if (!$new_line && $number eq $count) {
				$new_line = $line;
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line) {
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			$mes .= &get_item_name($kind, $item_no);
			$mes .= "‚ğ’D‚¢‚Ü‚µ‚½<br>";

			my @log_lines = ();
			open my $lfh, "+< $logdir/$y{country}/depot_log.cgi" or &error("$logdir/$y{country}/depot_log.cgi‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>2<>\n";
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;

			my @mlines = ();
			open my $mfh, "+< $this_file" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $mfh, 2; };
			push @mlines, $_ while <$mfh>;
	
			push @mlines, $new_line;
			seek  $mfh, 0, 0;
			truncate $mfh, 0;
			print $mfh @mlines;
			close $mfh;

			my @mlog_lines = ();
			open my $lmfh, "+< $this_log" or &error("$this_file‚ªŠJ‚¯‚Ü‚¹‚ñ");
			eval { flock $lmfh, 2; };
			my $mlog_count = 0;
			while (my $mlog_line = <$lmfh>){ 
			      push @mlog_lines, $mlog_line;
			      $mlog_count++;
			      last if $mlog_count > 30;
			}
			unshift @mlog_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>1<>\n";
			seek  $lmfh, 0, 0;
			truncate $lmfh, 0;
			print $lmfh @mlog_lines;
			close $lmfh;
		}
		else {
			$mes .= "‰½‚à’D‚¦‚Ü‚¹‚ñ‚Å‚µ‚½<br>";
			close $fh;
		}
	}else {
		$mes .= "‰½‚à’D‚¦‚Ü‚¹‚ñ‚Å‚µ‚½<br>";
	}
	$m{tp} = 570;
	&n_menu;
	&write_cs;
}

sub tp_660 {
	$m{act} += $m{turn};

	# À²°Î
	&refresh;
	&write_world_news("$c_m‚Ì$m{name}‚ª‘ŒÉ—ª’D‚É¸”s‚µ$c_y‚Ì˜S–‚É—H•Â‚³‚ê‚Ü‚µ‚½");
	&add_prisoner;
	my $v = int( (rand(4)+1) );
	$m{exp} += $v;
	$m{rank_exp}-= int(rand(6)+5);
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
}

sub tp_670 {
	$m{act} += $m{turn};

	my $v = int( rand(2) * $m{turn} );
	$m{exp} += $v;
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	$m{egg_c} += int(rand($m{turn})+$m{turn}) if $m{egg};

	if ($m{turn} >= 10) {
		$mes .= "”C–±‚É‘å¬Œ÷!$m{name}‚É‘Î‚·‚é•]‰¿‚ª‘å‚«‚­ã‚ª‚è‚Ü‚µ‚½<br>";
		$m{rank_exp} += $m{turn} * 3;
	}
	else {
		$mes .= "”C–±‚É¬Œ÷!$m{name}‚É‘Î‚·‚é•]‰¿‚ªã‚ª‚è‚Ü‚µ‚½<br>";
		$m{rank_exp} += int($m{turn} * 1.5);
	}

	&write_cs;
	&refresh;
	&n_menu;
}

#=================================================
# <input type="radio" •t‚Ì—a‚©‚èŠ‚Ì•¨
#=================================================
sub radio_my_depot {
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">‚â‚ß‚é</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
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


sub status_check {
	open my $fh, "< $this_file" or &error("$this_file ‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $head_line = <$fh>;
	my($lv_s,$sedai_s,$message_s) = split /<>/, $head_line;
	close $fh;
	
	return $lv_s,$sedai_s,$message_s;
}

1; # íœ•s‰Â
