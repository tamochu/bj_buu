#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# ”pl×İ·İ¸Ş Created by oiiiuiiii
#=================================================

my @rank_status = (
#•Ï”,•\¦–¼,Å’á’l
    ['str','‹­‚³',3000,0],
    ['sedai','¢‘ã',7,0],
    ['rank','ŠK‹‰',15,0],
    ['nou_c','”_‹Æ',300,0],
    ['sho_c','¤‹Æ',300,0],
    ['hei_c','’¥•º',200,0],
    ['gai_c','ŠOŒğ',60,0],
    ['gou_c','‹­’D',300,0],
    ['cho_c','’³•ñ',500,0],
    ['sen_c','ô”]',400,0],
    ['gik_c','‹UŒv',100,0],
    ['tei_c','’ã@',70,0],
    ['mat_c','‘Ò•š',100,0],
    ['cas_c','¶¼ŞÉ',4000,0],
    ['tou_c','“¢”°',4000,0],
    ['shu_c','Cs',5000,0],
    ['col_c','“¬‹Zê',5,0],
    ['mon_c','–‚•¨',5,0],
    ['win_c','•Œ÷',100,0],
    ['hero_c','“ˆê',1,0],
    ['huk_c','•œ‹»',1,0],
    ['met_c','–Å–S',1,0],
    ['esc_c','’E–',5,0],
    ['res_c','‹~o',5,0],
    ['lose_c','•s‹ü',30,0],
    ['fes_c','‚¨Õ‚è–ì˜Y',5,0],
    ['shogo_p','‚â‚è‚±‚İ',70,0],
    ['no1_c','NO.1',10,0],
    ['wt_c_latest','‰Ò“­—¦',100,50],
);

my $max_ranking = 10;

#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @rank_status;
my $type = $rank_status[$in{no}][0] ? "_$rank_status[$in{no}][0]" : '';

my $this_file = "$logdir/player_ranking${type}.cgi";
my $player_ranking_cycle_day = 1;

&update_player_ranking if -M $this_file > $player_ranking_cycle_day;
#&update_player_ranking; #‚·‚®‚ÉXV‚µ‚½‚¢ê‡‚Í‚±‚±‚ÌƒRƒƒ“ƒgƒAƒEƒg‚ğŠO‚·i‚½‚¾‚µˆ—‚ªd‚­‚È‚é‚Ì‚Å‘¬‚â‚©‚É–ß‚·‚±‚Æj
&run;
&footer;
exit;


#=================================================
# ×İ·İ¸Ş‰æ–Ê
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="‚s‚n‚o" class="button1"></form>|;
	for my $i (0 .. $#rank_status) {
		print $i eq $in{no} ? qq|$rank_status[$i][1] / | : qq|<a href="?no=$i">$rank_status[$i][1]</a> / |;
	}
	print qq|<h1>$rank_status[$in{no}][1]”pl×İ·İ¸Ş</h1>|;
	print qq|<div class="mes"><ul><li>×İ·İ¸Ş‚Í$player_ranking_cycle_day“ú‚²‚Æ‚ÉØ¾¯Ä‚³‚êXV‚³‚ê‚Ü‚·</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>‡ˆÊ</th><th>”’l</th><th>–¼‘O</th><th>Š‘®‘</th></tr>| unless $is_mobile;
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		if($rank_status[$in{no}][0] eq 'rank'){
			my $tempn = $number;
			my $sran = 0;
			while ($tempn =~ /š/){
				$tempn =~ s/š//;
				$sran++;
			}
			if($sran){
				$d_rank = $rank if ($pre_number != $sran);
				$pre_number = $sran;
			}else {
				$d_rank = $rank if ($pre_number ne $number);
				$pre_number = $number;
			}
		}else {
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
		}
		print $is_mobile     ? qq|<hr><b>$d_rank</b>ˆÊ/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rankˆÊ</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# ”pl×İ·İ¸Ş‚ğXV
#=================================================
sub update_player_ranking  {

	my %sames = ();
	my @line = ();
	my @p_ranks = (1,'','');
	my $status = $rank_status[$in{no}][0];
	my $rank_min = $rank_status[$in{no}][2];
	if ($rank_status[$in{no}][3]) {
		$max_ranking = $rank_status[$in{no}][3];
	}

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
			if (&get_rank_name($p{rank}, $p{name}) eq 'c’é') {
				$p{rank}++;
			}
			$p{rank} += $p{super_rank};

			my $count = 0;
			for my $i (1 .. $#shogos) {
				my @shk = keys %{ $shogos[$i][1] };
				my $k = $shk[0];
				my $v = $shogos[$i][1]{$k};
				++$count if $p{$k} >= $v;
			}
			my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
			$comp_par = 100 if $comp_par > 100;
			$p{shogo_p} = $comp_par;

			next if $p{$status} < $rank_min;

			my @datas = ();
			my @rdata = ();
			my $i = 1;

			while ($i <= $max_ranking){
				$rdata[0] = shift @p_ranks;
				$rdata[1] = shift @p_ranks;
				$rdata[2] = shift @p_ranks;
				if ($rdata[0] <= $p{$status}) {
					push @datas, $p{$status}, $p{name}, $p{country};
					push @datas, $rdata[0], $rdata[1], $rdata[2] unless $i >= $max_ranking && $p{$status} != $rdata[0];
					$i++;
					my $last_number = $datas[-3];
					while($i <= $max_ranking || $last_number == $p_ranks[0]){
						my $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$last_number = $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						last if $cash eq '';
						$i++;
					}
				}else {
					push @datas, $rdata[0], $rdata[1], $rdata[2];
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
		for my $j (0..2){
			$data[$j] = shift @p_ranks;
		}
		if($status eq 'rank'){
			$data[1] =~ tr/\x0D\x0A//d;
			my $player_id = unpack 'H*', $data[1];
			my %p = &get_you_datas($player_id, 1);
			my $rank_name = &get_rank_name($p{rank}, $p{name});
			if ($p{super_rank}){
				$rank_name = '';
				$rank_name .= 'š' for 1 .. $p{super_rank};
				$rank_name .= $p{rank_name};
			}
			push @line, "$rank_name<>$data[1]<>$data[2]\n";
		}else {
			push @line, "$data[0]<>$data[1]<>$data[2]\n";
		}
	}

	open my $fh, "> $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

