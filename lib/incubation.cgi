
#================================================
# 孵化（スイッチありの時の処理）
#================================================
sub begin {
	&tp_1;
}
sub tp_1  {
	if ($m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "持っていた$eggs[$m{egg}][1]が光だしました!<br>";
		
		# ﾊｽﾞﾚｴｯｸﾞ専用処理
		if ( $eggs[$m{egg}][1] eq 'ﾊｽﾞﾚｴｯｸﾞ' && rand(7) > 1 && $m{egg} != 53) {
			if (rand(6) > 1) {
				$mes .= "なんと、$eggs[$m{egg}][1]の中から $eggs[$m{egg}][1]が産まれました<br>";
			}
			else {
				$mes .= "なんと、$eggs[$m{egg}][1]の中は空っぽでした…<br>";
				$m{egg} = 0;
			}
		}
		# ﾀｷｵﾝｴｯｸﾞ
		elsif ($eggs[$m{egg}][1] eq 'ﾀｷｵﾝｴｯｸﾞ') {
			$m{egg_c} = 0;
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			if (rand(3) < 1) {
				$m{egg} = 0;
			} else {
				$mes .= "$eggs[$m{egg}][1]が時を逆行した<br>";
			}
		}
		# ｱﾋﾞﾘﾃｨｴｯｸﾞ専用処理(曜日により変わる)
		elsif ( $eggs[$m{egg}][1] eq 'ｱﾋﾞﾘﾃｨｴｯｸﾞ' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : 'おいすー';
			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]＜$pet_mes<br><br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# 孵化をロギング
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('incubation');
		}
	}
	$mes .= "戻ります";
	&refresh;
	&n_menu;
}

1; # 削除不可
