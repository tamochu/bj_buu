#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# ”pl×İ·İ¸Ş Created by oiiiuiiii
#=================================================

my $max_ranking = 100;

my %calc_name = (
	rank => "ŠK‹‰",
	lea => "“—¦",
	nou_c => "”_‹Æ",
	sho_c => "¤‹Æ",
	hei_c => "’¥•º",
	mil5_sum => "ŒR–5í‡Œv",
	mil3_sum => "ŒR–3í‡Œv",
	str => "‹­‚³",
	win_c => "í‘ˆŸ—˜”",
	win_par => "Ÿ—¦",
	gai_c => "ŠOŒğ",
	gou_c => "‹­’D",
	cho_c => "’³•ñ",
	sen_c => "ô”]",
	gik_c => "‹UŒv",
	tei_c => "’ã@",
	mat_c => "‘Ò•š",
	year_strong => "ˆê”N’D‘—Í",
	year_nou => "ˆê”N”_‹Æ",
	year_sho => "ˆê”N¤‹Æ",
	year_hei => "ˆê”N’¥•º",
	year_gou => "ˆê”N‹­’D",
	year_cho => "ˆê”N’³•ñ",
	year_sen => "ˆê”Nô”]",
	year_gou_t => "ˆê”N‹­’D(—İŒv)",
	year_cho_t => "ˆê”N’³•ñ(—İŒv)",
	year_sen_t => "ˆê”Nô”](—İŒv)",
	year_gik => "ˆê”N‹UŒv",
	year_res => "ˆê”N‹~o",
	year_esc => "ˆê”N’E–",
	year_tei => "ˆê”N’ã@",
	year_stop => "ˆê”N’âí",
	year_pro => "ˆê”N—FD",
	year_dai => "ˆê”N‘’{"
);

#=================================================
&decode;
&header;
&read_cs;

my $this_file = "$logdir/main_player.cgi";
my $this_script = 'main_player.cgi';

my $default_calc = "rank:8:1::lea:300:1:::nou_c:500:1::sho_c:500:1:::nou_c:500:1::sho_c:500:1::hei_c:500:1:::mil5_sum:2500:1:::mil5_sum:5000:1:::gai_c:350:1:::win_c:200:1::win_par:75:1:::win_c:400:1::win_par:80:1";
#my $default_calc = "rank:15:1::lea:900:1:::nou_c:1000:1::sho_c:1000:1:::nou_c:1000:1::sho_c:1000:1::hei_c:1000:1:::mil5_sum:7000:1:::mil5_sum:10000:1:::gai_c:1400:1:::win_c:800:1::win_par:75:1:::win_c:1000:1::win_par:80:1";

&update_main_player if $in{calc};
&run;
&footer;
exit;


#=================================================
# ×İ·İ¸Ş‰æ–Ê
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	print qq|<h1>å—Í•\\</h1>|;
	print qq|<div class="mes"><ul><li>×İ·İ¸Ş‚Ío—Í‚³‚ê‚é“x‚ÉØ¾¯Ä‚³‚êXV‚³‚ê‚Ü‚·</ul></div><br>|;
	print qq|<form action="$this_script">|;
	print qq|Zo®<textarea name="calc" cols="60" rows="8" class="textarea1">$default_calc</textarea><br>|;
	print qq|è‡’l<input type="text" name="min" value="1" class="text_box1"><br>|; # value="4"
	print qq|<input type="submit" value="o—Í" class="button1">|;
	print qq|</form>|;

	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	$head_line = <$fh>;
	my($output_time, $calc_def, $calc_min) = split /<>/, $head_line;
	
	my($min,$hour,$mday,$mon,$year) = (localtime($output_time))[1..4];
	my $output_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
	
	my $calc_table = &calc_to_table($calc_def);
	print qq|<h2>o—Í“ú:$output_date<br>Zo®:$calc_table<br>è‡’l:$calc_min</h2>|;
	
	my $pre_number = 0;
	my $d_rank;

	print qq|<table class="table1" cellpadding="2"><tr><th>‡ˆÊ</th><th>”’l</th><th>–¼‘O</th><th>Š‘®‘</th><th>•]‰¿</th></tr>| unless $is_mobile;
	
	my @lines = ();
	while ($line = <$fh>) {
		push @lines, $line;
		my($number,$name,$country,$type) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
		print $is_mobile     ? qq|<hr><b>$d_rank</b>ˆÊ/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
	
	
	for my $country_i(0..$w{country}) {
		$rank = 1;
		print qq|<h3>$cs{name}[$country_i]‚Ìå—Í</h3>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>‡ˆÊ</th><th>”’l</th><th>–¼‘O</th><th>Š‘®‘</th><th>•]‰¿</th></tr>| unless $is_mobile;
		
		for my $line (@lines) {
			my($number,$name,$country,$type) = split /<>/, $line;
			next if $country != $country_i;
			my $player_id =  unpack 'H*', $name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>ˆÊ/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				;
			++$rank;
		}
		close $fh;
		
		print qq|</table>| unless $is_mobile;
	}
}

#=================================================
# å—Í•\‚ğXV
#=================================================
sub update_main_player  {

	my %sames = ();
	my @line = ();
	my @p_ranks = (1,'','','');
	my @calcs = split /:::/, $in{calc};

	for my $country (0 .. $w{country}) {

		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");

		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/user.cgi") {
				next;
			}
			my %p = &get_you_datas($player_id, 1);

			$p{str} = int($p{max_hp} + $p{max_mp} + $p{at} + $p{df} + $p{mat} + $p{mdf} + $p{ag} + $p{cha} * 0.5);
			$p{mil3_sum} = $p{gou_c} + $p{cho_c} + $p{sen_c};
			$p{mil5_sum} = $p{gou_c} + $p{cho_c} + $p{sen_c} + $p{gik_c} + $p{tei_c};
			if ($p{win_c} + $p{lose_c} + $p{draw_c} > 0) {
				$p{win_par} = int($p{win_c} / ($p{win_c} + $p{lose_c} + $p{draw_c}) * 100);
			} else {
				$p{win_par} = 0;
			}
			
			my $last_year = $w{year} - 1;
			if (-f "$userdir/$player_id/year_ranking.cgi") {
				open my $yfh, "< $userdir/$player_id/year_ranking.cgi" or &error("$player ‚Ìyear_ranking.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
				while (my $line = <$yfh>) {
					my %yyear;
					for my $hash (split /<>/, $line) {
						my($k, $v) = split /;/, $hash;
						$yyear{$k} = $v;
						if($k eq 'year'){
							if($v != $last_year){
								next;
							}
						}
					}
					if($yyear{year} == $last_year){
						foreach my $key (keys(%yyear)){
							$p{'year_' . $key} = $yyear{$key};
						}
					}
				}
				close $yfh;
			}
			
			$p{calc} = 0;

			for my $calc_line (@calcs) {
				my @and_calc = split /::/, $calc_line;
				my $and_all_clear = 1;
				my $plus;
				for my $calc_and_line (@and_calc) {
					my ($calc_status, $calc_min, $calc_plus) = split /:/, $calc_and_line;
					if (!$calc_name{$calc_status}) {
						next;
					}
					if ($p{$calc_status} < $calc_min) {
						$and_all_clear = 0;
					}
					if ($calc_plus eq 'score') {
						$plus = $p{$calc_status};
					} else {
						$plus = $calc_plus;
					}
				}
				if ($and_all_clear) {
					$p{calc} += $plus;
					if ($calc_line eq "rank:8:1::lea:300:1") {
						$p{type} .= "(‚ŠK‹‰)";
					} #
					elsif ($calc_line eq "nou_c:500:1::sho_c:500:1") { # || $calc_line eq "nou_c:500:1::sho_c:500:1::hei_c:500:1")) {
						$p{type} .= "(“à­‰®)";
					} #
					elsif ($calc_line eq "mil5_sum:2500:1") { # || $calc_line eq "mil5_sum:5000:1")) {
						$p{type} .= "(ŒR–‰®)";
					}
					elsif ($calc_line eq "gai_c:350:1") {
						$p{type} .= "(ŠOŒğ‰®)";
					}
					elsif ($calc_line eq "gai_c:350:1") {
						$p{type} .= "(ŠOŒğ‰®)";
					}
					elsif ($calc_line eq "win_c:200:1::win_par:75:1") { # || $calc_line eq "win_c:400:1::win_par:80:1") {
						$p{type} .= "(í‘ˆ‰®)";
					}
				}
			}
			next if $p{calc} < $in{min};

			my @datas = ();
			my @rdata = ();
			my $i = 1;

			while ($i <= $max_ranking){
				$rdata[0] = shift @p_ranks;
				$rdata[1] = shift @p_ranks;
				$rdata[2] = shift @p_ranks;
				$rdata[3] = shift @p_ranks;
				if ($rdata[0] <= $p{calc}) {
					push @datas, $p{calc}, $p{name}, $p{country}, $p{type};
					push @datas, $rdata[0], $rdata[1], $rdata[2], $rdata[3] unless $i >= $max_ranking && $p{calc} != $rdata[0];
					$i++;
					my $last_number = $datas[-4];
					while($i <= $max_ranking || $last_number == $p_ranks[0]){
						my $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$last_number = $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						last if $cash eq '';
						$i++;
					}
				}else {
					push @datas, $rdata[0], $rdata[1], $rdata[2], $rdata[3];
					$i++;
				}
				last if $rdata[1] eq '';
			}
			@p_ranks = ();
			push @p_ranks, @datas;
		}
		close $cfh;
	}
	while ($p_ranks[1] ne '') {
		my @data;
		for my $j (0..3){
			$data[$j] = shift @p_ranks;
		}
		push @line, "$data[0]<>$data[1]<>$data[2]<>$data[3]\n";
	}
	unshift @line, "$time<>$in{calc}<>$in{min}\n";
	open my $fh, "> $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

#=================================================
# Zo®ƒe[ƒuƒ‹‰»
#=================================================
sub calc_to_table  {
	my $calc = shift;
	
	my $ret_table = qq|<table class="table1"><tr><th>ğŒ</th><th>‰ÁZ’l</th></tr>|;
	my @calcs = split /:::/, $calc;
	
	for my $calc_line (@calcs) {
		my @and_calc = split /::/, $calc_line;
		my $condition_data = "";
		my $plus;
		for my $calc_and_line (@and_calc) {
			my ($calc_status, $calc_min, $calc_plus) = split /:/, $calc_and_line;
			if (!$calc_name{$calc_status}) {
				next;
			}
			$condition_data .= qq|$calc_name{$calc_status}:$calc_minˆÈã|;
			$plus = $calc_plus;
		}
		$ret_table .= qq|<tr><td>$condition_data</td><td>$plus</td></tr>|;
	}
	
	return $ret_table;
}
