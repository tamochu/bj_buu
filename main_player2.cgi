#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 廃人ﾗﾝｷﾝｸﾞ Created by oiiiuiiii
#=================================================

my $max_ranking = 100;

my %calc_name = (
	rank => "階級",
	lea => "統率",
	nou_c => "農業",
	sho_c => "商業",
	hei_c => "徴兵",
	mil5_sum => "軍事5種合計",
	mil3_sum => "軍事3種合計",
	str => "強さ",
	win_c => "戦争勝利数",
	win_par => "勝率",
	gai_c => "外交",
	gou_c => "強奪",
	cho_c => "諜報",
	sen_c => "洗脳",
	gik_c => "偽計",
	kou_c => "攻城",
	tei_c => "偵察",
	mat_c => "待伏",
	year_strong => "一年奪国力",
	year_nou => "一年農業",
	year_sho => "一年商業",
	year_hei => "一年徴兵",
	year_gou => "一年強奪",
	year_cho => "一年諜報",
	year_sen => "一年洗脳",
	year_gou_t => "一年強奪(累計)",
	year_cho_t => "一年諜報(累計)",
	year_sen_t => "一年洗脳(累計)",
	year_gik => "一年偽計",
	year_res => "一年救出",
	year_esc => "一年脱獄",
	year_tei => "一年偵察",
	year_stop => "一年停戦",
	year_pro => "一年友好",
	year_dai => "一年国畜"
);

#=================================================
&decode;
&header_main_player;
&read_cs;

my $this_file = "$logdir/main_player2.cgi";
my $this_script = 'main_player2.cgi';

my $default_calc = "rank:8:1::lea:300:1:::nou_c:500:1::sho_c:500:1:::nou_c:500:1::sho_c:500:1::hei_c:500:1:::mil5_sum:2500:1:::mil5_sum:5000:1:::gai_c:350:1:::win_c:200:1::win_par:75:1:::win_c:400:1::win_par:80:1";
#my $default_calc = "rank:15:1::lea:900:1:::nou_c:1000:1::sho_c:1000:1:::nou_c:1000:1::sho_c:1000:1::hei_c:1000:1:::mil5_sum:7000:1:::mil5_sum:10000:1:::gai_c:1400:1:::win_c:800:1::win_par:75:1:::win_c:1000:1::win_par:80:1";

&update_main_player if $in{calc};
&run;
&footer;
exit;


#================================================
# header
#================================================
sub header_main_player {
	print "Content-type: text/html; charset=Shift_JIS\n";
	if ($gzip ne '' && $ENV{HTTP_ACCEPT_ENCODING} =~ /gzip/){  
		if ($ENV{HTTP_ACCEPT_ENCODING} =~ /x-gzip/) {
			print "Content-encoding: x-gzip\n\n";
		}
		else{
			print "Content-encoding: gzip\n\n";
		}
		open STDOUT, "| $gzip -1 -c";
	}
	else {
		print "\n";
	}
	
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	unless ($is_mobile) {
		print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
		print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">|;
		print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/bj.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/jquery.add-input-area.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/main_player.js?$jstime"></script>\n|;
	} else {
		# ガラケーで外部CSSの読み込みはNG
		# HTMLファイルを読み込んだ後にCSSファイルを読み込むため、
		# 素のHTMLが表示された後にCSSが適用され画面がチラつくなどの問題がある
		print qq|<style type="text/css"><!-- a.clickable_name {color: inherit; text-decoration: none;} --></style>|;
	}
	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
	print qq|</head><body $body><a name="top"></a>|;
}
#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	print qq|<h1>主力表\</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞは出力される度にﾘｾｯﾄされ更新されます</ul></div><br>|;
	print qq|<form action="$this_script">|;
	if ($is_mobile) {
		print qq|算出式<textarea name="calc">$default_calc</textarea><br>|;
	} else {
		print qq|<ul id="make_calc_list">|;
		print qq|<li class="make_calc_list_var">|;
		print qq|グループ<input type="text" name="make_calc_list_group_0" class="text_box1 changable group"/>|;
		print qq|<select name="make_calc_list_type_0" class="changable type"/>|;
		for my $tk (keys(%calc_name)) {
			print qq|<option value="$tk">$calc_name{$tk}</option>|;
		}
		print qq|</select>|;
		print qq|が<input type="text" name="make_calc_list_value_0" class="text_box_s changable value"/>以上|;
		print qq|<input type="button" class="make_calc_list_del button1" value="削除"/>|;
		print qq|</li>|;
		print qq|</ul>|;
		print qq|<input type="button" value="追加" class="make_calc_list_add button1"/>|;
		print qq|階級は|;
		for my $r (0..$#ranks) {
			print qq|$ranks[$r]:$r,|;
		}
		print qq|となります。<br>|;
		print qq|<input type="hidden" name="calc" value="$default_calc" id="calc"/><br>|;
	}
	print qq|閾値<input type="text" name="min" value="1" class="text_box1"><br>|;
	print qq|<input type="submit" value="出力" class="button1">|;
	print qq|</form>|;

	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	$head_line = <$fh>;
	my($output_time, $calc_def, $calc_min) = split /<>/, $head_line;
	
	my($min,$hour,$mday,$mon,$year) = (localtime($output_time))[1..4];
	my $output_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
	
	my $calc_table = &calc_to_table($calc_def);
	print qq|<h2>出力日:$output_date<br>算出式:$calc_table<br>閾値:$calc_min</h2>|;
	
	my $pre_number = 0;
	my $d_rank;

	print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th><th>評価</th></tr>| unless $is_mobile;
	
	my @lines = ();
	while ($line = <$fh>) {
		push @lines, $line;
		my($number,$name,$country,$type) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
		print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
	
	
	for my $country_i(0..$w{country}) {
		$rank = 1;
		print qq|<h3>$cs{name}[$country_i]の主力</h3>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>数値</th><th>名前</th><th>所属国</th><th>評価</th></tr>| unless $is_mobile;
		
		for my $line (@lines) {
			my($number,$name,$country,$type) = split /<>/, $line;
			next if $country != $country_i;
			my $player_id =  unpack 'H*', $name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>位/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rank位</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				;
			++$rank;
		}
		close $fh;
		
		print qq|</table>| unless $is_mobile;
	}
}

#=================================================
# 主力表を更新
#=================================================
sub update_main_player  {

	my %sames = ();
	my @line = ();
	my @p_ranks = (1,'','','');
	my @calcs = split /:::/, $in{calc};

	for my $country (0 .. $w{country}) {

		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");

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
				open my $yfh, "< $userdir/$player_id/year_ranking.cgi" or &error("$player のyear_ranking.cgiﾌｧｲﾙが開けません");
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
						$p{type} .= "(高階級)";
					} #
					elsif ($calc_line eq "nou_c:500:1::sho_c:500:1") { # || $calc_line eq "nou_c:500:1::sho_c:500:1::hei_c:500:1")) {
						$p{type} .= "(内政屋)";
					} #
					elsif ($calc_line eq "mil5_sum:2500:1") { # || $calc_line eq "mil5_sum:5000:1")) {
						$p{type} .= "(軍事屋)";
					}
					elsif ($calc_line eq "gai_c:350:1") {
						$p{type} .= "(外交屋)";
					}
					elsif ($calc_line eq "gai_c:350:1") {
						$p{type} .= "(外交屋)";
					}
					elsif ($calc_line eq "win_c:200:1::win_par:75:1") { # || $calc_line eq "win_c:400:1::win_par:80:1") {
						$p{type} .= "(戦争屋)";
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
	open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

#=================================================
# 算出式テーブル化
#=================================================
sub calc_to_table  {
	my $calc = shift;
	
	my $ret_table = qq|<table class="table1"><tr><th>条件</th><th>加算値</th></tr>|;
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
			$condition_data .= qq|$calc_name{$calc_status}:$calc_min以上|;
			$plus = $calc_plus;
		}
		$ret_table .= qq|<tr><td>$condition_data</td><td>$plus</td></tr>|;
	}
	
	return $ret_table;
}