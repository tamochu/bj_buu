#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_comment_tag.cgi';
require "$datadir/casino.cgi";

#require 'lib/casino_mahjang_base.cgi';

&decode;
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
&access_check;
&read_user;
&read_cs;

$limit_member_time = 60;

$this_file = "$logdir/chat_casino$files[$m{c_type}][2]";
require "./lib/casino_$files[$m{c_type}][1].cgi";#run,get_member,etc
&member_reload;
&print_cards_app;
exit;
sub print_cards_app{
	my $view_point = 0;
	my @up_hand;
	my @right_hand;
	my @left_hand;
	my @down_hand;
	my @up_trash;
	my @right_trash;
	my @left_trash;
	my @down_trash;
	my $is_player = 0;
	
	open my $fh, "< ${this_file}_member.cgi" or &error("ﾒﾝﾊﾞｰﾌｧｲﾙが開けません"); 
	my $head_line = <$fh>;
	my($turn, $rate, $e_player, $s_player, $w_player, $n_player, $trash_e, $trash_s, $trash_w, $trash_n, $hands_e, $hands_s, $hands_w, $hands_n, $bonus, $rest) = split /<>/, $head_line;
	close $fh;
	if($m{name} eq $e_player){
		$view_point = 1;
		$is_player = 1;
	}elsif($m{name} eq $s_player){
		$view_point = 2;
		$is_player = 1;
	}elsif($m{name} eq $w_player){
		$view_point = 3;
		$is_player = 1;
	}elsif($m{name} eq $n_player){
		$view_point = 4;
		$is_player = 1;
	}

	if($view_point == 0){
		$up_hand = $hands_w;
		$right_hand = $hands_s;
		$left_hand = $hands_n;
		$down_hand = $hands_e;
		$up_trash = $trash_w;
		$right_trash = $trash_s;
		$left_trash = $trash_n;
		$down_trash = $trash_e;
	}elsif($view_point == 1){
		$up_hand = $hands_w;
		$right_hand = $hands_s;
		$left_hand = $hands_n;
		$down_hand = $hands_e;
		$up_trash = $trash_w;
		$right_trash = $trash_s;
		$left_trash = $trash_n;
		$down_trash = $trash_e;
	}elsif($view_point == 2){
		$up_hand = $hands_n;
		$right_hand = $hands_w;
		$left_hand = $hands_e;
		$down_hand = $hands_s;
		$up_trash = $trash_n;
		$right_trash = $trash_w;
		$left_trash = $trash_e;
		$down_trash = $trash_s;
	}elsif($view_point == 3){
		$up_hand = $hands_e;
		$right_hand = $hands_n;
		$left_hand = $hands_s;
		$down_hand = $hands_w;
		$up_trash = $trash_e;
		$right_trash = $trash_n;
		$left_trash = $trash_s;
		$down_trash = $trash_w;
	}elsif($view_point == 4){
		$up_hand = $hands_s;
		$right_hand = $hands_e;
		$left_hand = $hands_w;
		$down_hand = $hands_n;
		$up_trash = $trash_s;
		$right_trash = $trash_e;
		$left_trash = $trash_w;
		$down_trash = $trash_n;
	}else {
		$up_hand = $hands_w;
		$right_hand = $hands_s;
		$left_hand = $hands_n;
		$down_hand = $hands_e;
		$up_trash = $trash_w;
		$right_trash = $trash_s;
		$left_trash = $trash_n;
		$down_trash = $trash_e;
	}
	@bonus_cards = split / / , $bonus;
	
	my($up_raw, @up_eat) = split / /, $up_hand;
	my($right_raw, @right_eat) = split / /, $right_hand;
	my($left_raw, @left_eat) = split / /, $left_hand;
	my($down_raw, @down_eat) = split / /, $down_hand;
	
	if($turn){
		my $no_hands = 1;
		my @up_raws = split //, $up_raw;
		for my $i (0..18){
			if($up_raws[$i*2] eq ''){
				last;
			}
			$no_hands = 0;
			
			print "ura,";
		}
		if($no_hands){
			print "-1";
		}
		@eat_hands = @up_eat;
		for my $eat (@eat_hands){
			my @eat_str = split //, $eat;
			if($eat_str[0] eq '-' && $eat_str[-1] ne '-'){
				print "y$eat_str[1]$eat_str[2],";
				print "$eat_str[3]$eat_str[4],";
				print "$eat_str[5]$eat_str[6],";
				print "$eat_str[7]$eat_str[8]," if $eat_str[7];
			}
			elsif($eat_str[0] eq '-' && $eat_str[-1] eq '-'){
				print "$eat_str[1]$eat_str[2],";
				print "y$eat_str[3]$eat_str[4],";
				print "$eat_str[5]$eat_str[6],";
				print "$eat_str[7]$eat_str[8]," if ($eat_str[7] && $eat_str[7] ne '-');
			}
			elsif($eat_str[0] ne '-' && $eat_str[-1] eq '-'){
				print "$eat_str[0]$eat_str[1],";
				print "$eat_str[2]$eat_str[3],";
				if($eat_str[6] ne '-'){
					print "$eat_str[4]$eat_str[5],";
					print "y$eat_str[6]$eat_str[7],";
				}else{
					print "y$eat_str[4]$eat_str[5],";
				}
			}else{
				print "ura,";
				print "$eat_str[2]$eat_str[3],";
				print "$eat_str[4]$eat_str[5],";
				print "ura,";
			}
		}
		print "<>";
		$no_hands = 1;
		my @left_raws = split //, $left_raw;
		for my $i (0..18){
			if($left_raws[$i*2] eq ''){
				last;
			}
			$no_hands = 0;
			
			print "yura,";
		}
		if($no_hands){
			print "-1";
		}
		@eat_hands = @left_eat;
		for my $eat (@eat_hands){
			my @eat_str = split //, $eat;
			if($eat_str[0] eq '-' && $eat_str[-1] ne '-'){
				print "$eat_str[1]$eat_str[2],";
				print "y$eat_str[3]$eat_str[4],";
				print "y$eat_str[5]$eat_str[6],";
				print "y$eat_str[7]$eat_str[8]," if $eat_str[7];
			}
			elsif($eat_str[0] eq '-' && $eat_str[-1] eq '-'){
				print "y$eat_str[1]$eat_str[2],";
				print "$eat_str[3]$eat_str[4],";
				print "y$eat_str[5]$eat_str[6],";
				print "y$eat_str[7]$eat_str[8]," if ($eat_str[7] && $eat_str[7] ne '-');
			}
			elsif($eat_str[0] ne '-' && $eat_str[-1] eq '-'){
				print "y$eat_str[0]$eat_str[1],";
				print "y$eat_str[2]$eat_str[3],";
				if($eat_str[6] ne '-'){
					print "y$eat_str[4]$eat_str[5],";
					print "$eat_str[6]$eat_str[7],";
				}else{
					print "$eat_str[4]$eat_str[5],";
				}
			}else{
				print "yura,";
				print "y$eat_str[2]$eat_str[3],";
				print "y$eat_str[4]$eat_str[5],";
				print "yura,";
			}
		}
		print "<>";
		$no_hands = 1;
		my @right_raws = split //, $right_raw;
		for my $i (0..18){
			if($right_raws[$i*2] eq ''){
				last;
			}
			$no_hands = 0;
			
			print "yura,";
		}
		if($no_hands){
			print "-1";
		}
		@eat_hands = @right_eat;
		for my $eat (@eat_hands){
			my @eat_str = split //, $eat;
			if($eat_str[0] eq '-' && $eat_str[-1] ne '-'){
				print "$eat_str[1]$eat_str[2],";
				print "y$eat_str[3]$eat_str[4],";
				print "y$eat_str[5]$eat_str[6],";
				print "y$eat_str[7]$eat_str[8]," if $eat_str[7];
			}
			elsif($eat_str[0] eq '-' && $eat_str[-1] eq '-'){
				print "y$eat_str[1]$eat_str[2],";
				print "$eat_str[3]$eat_str[4],";
				print "y$eat_str[5]$eat_str[6],";
				print "y$eat_str[7]$eat_str[8]," if ($eat_str[7] && $eat_str[7] ne '-');
			}
			elsif($eat_str[0] ne '-' && $eat_str[-1] eq '-'){
				print "y$eat_str[0]$eat_str[1],";
				print "y$eat_str[2]$eat_str[3],";
				if($eat_str[6] ne '-'){
					print "y$eat_str[4]$eat_str[5],";
					print "$eat_str[6]$eat_str[7],";
				}else{
					print "$eat_str[4]$eat_str[5],";
				}
			}else{
				print "yura,";
				print "y$eat_str[2]$eat_str[3],";
				print "y$eat_str[4]$eat_str[5],";
				print "yura,";
			}
		}
		print "<>";
		$no_hands = 1;
		@raw_hands = split //, $down_raw;
		for my $j (0..18){
			if($raw_hands[$j*2] eq ''){
				last;
			}
			$no_hands = 0;
			
			if($view_point == 0){
				print 'ura,';
			}else{
				print "$raw_hands[$j*2]$raw_hands[$j*2+1],";
			}
		}
		if($no_hands){
			print "-1";
		}
		@eat_hands = @down_eat;
		for my $eat (@eat_hands){
			print ",";
			my @eat_str = split //, $eat;
			if($eat_str[0] eq '-' && $eat_str[-1] ne '-'){
				print "y$eat_str[1]$eat_str[2],";
				print "$eat_str[3]$eat_str[4],";
				print "$eat_str[5]$eat_str[6],";
				print "$eat_str[7]$eat_str[8]," if $eat_str[7];
			}
			elsif($eat_str[0] eq '-' && $eat_str[-1] eq '-'){
				print "$eat_str[1]$eat_str[2],";
				print "y$eat_str[3]$eat_str[4],";
				print "$eat_str[5]$eat_str[6],";
				print "$eat_str[7]$eat_str[8]," if ($eat_str[7] && $eat_str[7] ne '-');
			}
			elsif($eat_str[0] ne '-' && $eat_str[-1] eq '-'){
				print "$eat_str[0]$eat_str[1],";
				print "$eat_str[2]$eat_str[3],";
				if($eat_str[6] ne '-'){
					print "$eat_str[4]$eat_str[5],";
					print "y$eat_str[6]$eat_str[7],";
				}else{
					print "y$eat_str[4]$eat_str[5],";
				}
			}else{
				print "ura,";
				print "$eat_str[2]$eat_str[3],";
				print "$eat_str[4]$eat_str[5],";
				print "ura,";
			}
		}
		$notrush = 1;
		print "<>";
		my $reach_flag = 0;
		@trashs = split //, $up_trash;
		my $i_t = 0;
		for my $i (0..24){
			last if($trashs[$i_t] eq '');
			if($trashs[$i_t] eq '-'){
				$reach_flag = 1;
				$i_t++;
			}
			
			if($reach_flag){
				print "y$trashs[$i_t]$trashs[$i_t+1],";
				$reach_flag = 0;
			}else{
				print "$trashs[$i_t]$trashs[$i_t+1],";
			}
			$notrush = 0;
			$i_t += 2;
		}
		if($notrush){
			print "-1";
		}
		$notrush = 1;
		print "<>";
		$reach_flag = 0;
		@trashs = split //, $left_trash;
		$i_t = 0;
		for my $i (0..24){
			last if($trashs[$i_t] eq '');
			if($trashs[$i_t] eq '-'){
				$reach_flag = 1;
				$i_t++;
			}
			
			if($reach_flag){
				print "$trashs[$i_t]$trashs[$i_t+1],";
				$reach_flag = 0;
			}else{
				print "y$trashs[$i_t]$trashs[$i_t+1],";
			}
			$notrush = 0;
			$i_t += 2;
		}
		if($notrush){
			print "-1";
		}
		$notrush = 1;
		print "<>";
		$reach_flag = 0;
		@trashs = split //, $right_trash;
		$i_t = 0;
		for my $i (0..24){
			last if($trashs[$i_t] eq '');
			if($trashs[$i_t] eq '-'){
				$reach_flag = 1;
				$i_t++;
			}
			
			if($reach_flag){
				print "$trashs[$i_t]$trashs[$i_t+1],";
				$reach_flag = 0;
			}else{
				print "y$trashs[$i_t]$trashs[$i_t+1],";
			}
			$notrush = 0;
			$i_t += 2;
		}
		if($notrush){
			print "-1";
		}
		$notrush = 1;
		print "<>";
		$reach_flag = 0;
		@trashs = split //, $down_trash;
		$i_t = 0;
		for my $i (0..24){
			last if($trashs[$i_t] eq '');
			if($trashs[$i_t] eq '-'){
				$reach_flag = 1;
				$i_t++;
			}
			
			if($reach_flag){
				print "y$trashs[$i_t]$trashs[$i_t+1],";
				$reach_flag = 0;
			}else{
				print "$trashs[$i_t]$trashs[$i_t+1],";
			}
			$notrush = 0;
			$i_t += 2;
		}
		if($notrush){
			print "-1";
		}
		$notrush = 1;
		print "<>";

		my $no_bonus = 1;
		for my $i (0..4){
			last if($bonus_cards[$i] eq '');
			$card = $bonus_cards[$i];
			print "$card,";
			$no_bonus = 0;
		}
		if($no_bonus){
			print "-1"
		}
		print "<>";
		
		my $nomatch_flag = 1;
		my $cut_flag = 0;
		my $t_card = 0;
		if($turn == 1){
			@new_trash = split // , $trash_e;
			if($m{name} eq $s_player){
				$cut_flag = 1;
			}
		}elsif($turn == 2){
			@new_trash = split // , $trash_s;
			if($m{name} eq $w_player){
				$cut_flag = 1;
			}
		}elsif($turn == 3 || ($three && $turn == 4)){
			@new_trash = split // , $trash_w;
			if($m{name} eq $n_player){
				$cut_flag = 1;
			}
		}elsif($turn == 4){
			@new_trash = split // , $trash_n;
			if($m{name} eq $e_player){
				$cut_flag = 1;
			}
		}
		$t_num = pop @new_trash;
		$t_var = pop @new_trash;
		if($e_player eq $m{name}){
			$t_hands = $hands_e;
		}elsif($s_player eq $m{name}){
			$t_hands = $hands_s;
		}elsif($w_player eq $m{name}){
			$t_hands = $hands_w;
		}elsif($n_player eq $m{name}){
			$t_hands = $hands_n;
		}
		my($t_raw, @t_eat) = split / /, $t_hands;
		my @pm_cards = (0,0,0,0,0);
		if($t_var eq 'z'){
			my $c_num = $t_num;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[2]++;
				$t_raw =~ s/$t_var$c_num//;
			}
		}else{
			my $c_num = $t_num - 2;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[0]++;
				$t_raw =~ s/$t_var$c_num//;
			}
			$c_num = $t_num - 1;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[1]++;
				$t_raw =~ s/$t_var$c_num//;
			}
			$c_num = $t_num;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[2]++;
				$t_raw =~ s/$t_var$c_num//;
			}
			$c_num = $t_num + 1;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[3]++;
				$t_raw =~ s/$t_var$c_num//;
			}
			$c_num = $t_num + 2;
			for (0..14){
				last if($t_raw !~ /$t_var$c_num/);
				$pm_cards[4]++;
				$t_raw =~ s/$t_var$c_num//;
			}
		}
		if($turn >= 1 && $turn <= 4 && $m{c_value} == 0 && 
			(($m{name} eq $e_player && $turn != 1) ||
			($m{name} eq $s_player && $turn != 2) ||
			($m{name} eq $w_player && $turn != 3) ||
			($m{name} eq $n_player && $turn != 4))){
			if($pm_cards[0] && $pm_cards[1] && $cut_flag){
				my $temp = $t_num - 2;
				my $card1 = $t_var . $temp;
				$temp = $t_num - 1;
				my $card2 = $t_var . $temp;
				print "1,$card1,$card2,";
				$nomatch_flag = 0;
			}
			if($pm_cards[1] && $pm_cards[3] && $cut_flag){
				my $temp = $t_num - 1;
				my $card1 = $t_var . $temp;
				$temp = $t_num + 1;
				my $card2 = $t_var . $temp;
				print "2,$card1,$card2,";
				$nomatch_flag = 0;
			}
			if($pm_cards[3] && $pm_cards[4] && $cut_flag){
				my $temp = $t_num + 1;
				my $card1 = $t_var . $temp;
				$temp = $t_num + 2;
				my $card2 = $t_var . $temp;
				print "3,$card1,$card2,";
				$nomatch_flag = 0;
			}
			if($pm_cards[2] >= 2){
				my $card1 = $t_var . $t_num;
				print "4,$card1,$card1,";
				$nomatch_flag = 0;
			}
		}
		if($nomatch_flag){
			print "-1,-1,-1";
		}
		print "<>";
		
		if( ($turn == 5 && $m{name} eq $e_player) || 
			($turn == 6 && $m{name} eq $s_player) || 
			($turn == 7 && $m{name} eq $w_player) || 
			($turn == 8 && $m{name} eq $n_player)){
			my $ret_t = &is_tenpai;
			if($m{c_value} == 0 && $ret_t){
				print "1";
			}else{
				print "0";
			}
		}else{
			print "0";
		}
		print "<>";

		my $no_kan_flag = 1;
		if( ($turn == 5 && $m{name} eq $e_player) || 
			($turn == 6 && $m{name} eq $s_player) || 
			($turn == 7 && $m{name} eq $w_player) || 
			($turn == 8 && $m{name} eq $n_player)){
			my @m_num = (0,0,0,0,0,0,0,0,0);
			my @s_num = (0,0,0,0,0,0,0,0,0);
			my @p_num = (0,0,0,0,0,0,0,0,0);
			my @t_num = (0,0,0,0,0,0,0);
			my($k_raw, @k_eat) = split / /, $t_hands;
			
			for my $i (1..9){
				for (0..14){
					last if ($k_raw !~ /m$i/);
					$k_raw =~ s/m$i//;
					$m_num[$i-1]++;
				}
				for (0..14){
					last if ($k_raw !~ /s$i/);
					$k_raw =~ s/s$i//;
					$s_num[$i-1]++;
				}
				for (0..14){
					last if ($k_raw !~ /p$i/);
					$k_raw =~ s/p$i//;
					$p_num[$i-1]++;
				}
				for (0..14){
					last if ($k_raw !~ /z$i/);
					$k_raw =~ s/z$i//;
					$t_num[$i-1]++;
				}
			}
			for my $eat (@k_eat){
				if($eat =~ /(m([1-9]))\1{2}/){
					$m_num[$2 - 1] += 3;
				}elsif($eat =~ /(s([1-9]))\1{2}/){
					$s_num[$2 - 1] += 3;
				}elsif($eat =~ /(p([1-9]))\1{2}/){
					$p_num[$2 - 1] += 3;
				}elsif($eat =~ /(z([1-7]))\1{2}/){
					$t_num[$2 - 1] += 3;
				}
			}
			
			for my $i (0..8){
				if($m_num[$i] == 4){
					my $card = $i+1;
					print "m$card,";
					$no_kan_flag = 0;
				}
				if($s_num[$i] == 4){
					my $card = $i+1;
					print "s$card,";
					$no_kan_flag = 0;
				}
				if($p_num[$i] == 4){
					my $card = $i+1;
					print "p$card,";
					$no_kan_flag = 0;
				}
			}
			for my $i (0..6){
				if($t_num[$i] == 4){
					my $card = $i+1;
					print "z$card,";
					$no_kan_flag = 0;
				}
			}
		}
		if($no_kan_flag){
			print "-1";
		}
		print "<>";
		my $ret;
		my $base;
		my $doubled;
		my $ret_str;
		if($turn >= 1 && $turn <= 4 &&
			(($m{name} eq $e_player && $turn != 1) ||
			($m{name} eq $s_player && $turn != 2) ||
			($m{name} eq $w_player && $turn != 3) ||
			($m{name} eq $n_player && $turn != 4))){
			$ret = &is_finish_r;
			my $ret2 = &is_furiten;
			if($ret && $ret2 == 0){
				print "1";
			}else{
				print "0";
			}
		}elsif( ($turn == 5 && $m{name} eq $e_player) || 
				($turn == 6 && $m{name} eq $s_player) || 
				($turn == 7 && $m{name} eq $w_player) || 
				($turn == 8 && $m{name} eq $n_player)){
			$ret = &is_finish_t;
			if($ret){
				print "1";
			}else{
				print "0";
			}
		}
		print "<>";
		
		if( ($turn == 4 && $m{name} eq $e_player) || 
			($turn == 1 && $m{name} eq $s_player) || 
			($turn == 2 && $m{name} eq $w_player) || 
			($turn == 3 && $m{name} eq $n_player)){
			print "1";
		}else{
			print "0";
		}
		print "<>";
		
		$ret_str = 'blank';
		unless ($ret_str){
			$ret_str = '役無し';
		}
		my $rest_num = int(length($rest)/2);
		print "-1<>-1<>$ret_str<>0<>$turn<>$rest_num<>";
	}else{
		print "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>1<>0<>0<>"
	}
}

sub num_to_card{
	my $i = shift;
	my $ret;
	my $y_flag = 0;
	if($i >= 1000){
		$y_flag = 1;
		$i -= 1000;
	}
	if($i <= -1000){
		$y_flag = 1;
		$i += 1000;
	}
	
	if($i >= 0 && $i < 100){
		$ret = int($i / 10) - 1;
	}elsif($i >= 100 && $i < 200){
		$ret = int($i / 10) - 2;
	}elsif($i >= 200 && $i < 300){
		$ret = int($i / 10) - 3;
	}elsif($i >= 300 && $i < 400){
		$ret = int($i / 10) - 4;
	}elsif($i == -1){
		$ret = -1;
	}else{
		$ret = 34;
	}
	if($y_flag){
		$ret += 100
	}
	return $ret;
}

sub member_reload {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $auto_draw_p = 0;
	my $auto_play_p = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('1ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($turn, $rate, $e_player, $s_player, $w_player, $n_player, $trash_e, $trash_s, $trash_w, $trash_n, $hands_e, $hands_s, $hands_w, $hands_n, $bonus, $rest) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn >= 2){
				#自動ツモ、ツモ切り
				if($mname eq $e_player && $turn == 4){
					$mtime = $time - $limit_member_time + 2;
					$auto_draw_p = 1;
				}elsif($mname eq $s_player && $turn == 1){
					$mtime = $time - $limit_member_time + 2;
					$auto_draw_p = 2;
				}elsif($mname eq $w_player && $turn == 2){
					$mtime = $time - $limit_member_time + 2;
					$auto_draw_p = 3;
				}elsif($mname eq $n_player && $turn == 3){
					$mtime = $time - $limit_member_time + 2;
					$auto_draw_p = 4;
				}elsif($mname eq $e_player && $turn == 5){
					$mtime = $time - $limit_member_time + 2;
					$auto_play_p = 1;
				}elsif($mname eq $s_player && $turn == 6){
					$mtime = $time - $limit_member_time + 2;
					$auto_play_p = 2;
				}elsif($mname eq $w_player && $turn == 7){
					$mtime = $time - $limit_member_time + 2;
					$auto_play_p = 3;
				}elsif($mname eq $n_player && $turn == 8){
					$mtime = $time - $limit_member_time + 2;
					$auto_play_p = 4;
				}
			}elsif($mturn == 0) {
				next;
			}
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
	}
	unshift @members, "$turn<>$rate<>$e_player<>$s_player<>$w_player<>$n_player<>$trash_e<>$trash_s<>$trash_w<>$trash_n<>$hands_e<>$hands_s<>$hands_w<>$hands_n<>$bonus<>$rest<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if($auto_draw_p){
		&auto_draw($auto_draw_p);
	}elsif($auto_play_p){
		&auto_play($auto_play_p);
	}
}
