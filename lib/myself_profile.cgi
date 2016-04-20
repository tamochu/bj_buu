require "$datadir/profile.cgi";
#================================================
# ﾌﾟﾛﾌｨｰﾙ設定 Created by Merino
#================================================

#================================================
sub begin {
	$layout = 2;

	my %datas = ();
	open my $fh, "< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgiﾌｧｲﾙが開けません");
	my $line = <$fh>;
	close $fh;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$datas{$k} = $v;
	}

	$mes .= qq|$m{name}のﾌﾟﾛﾌｨｰﾙ：全角80文字(半角160)まで<br>|;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="mode" value="write">|;
	for my $profile (@profiles) {
		if ($profile->[1] eq "誕生日") {
			$mes .= qq|<hr>$profile->[1] 入力例：2000/01/01 生年月日を入力した場合には二度と変更できません<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
		else {
			$mes .= qq|<hr>$profile->[1]<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
	}
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		my $boch_pet = $m{sex} eq '1' ? '脳内嫁' : 'ﾏｽｺｯﾄｷｬﾗ';
		$mes .= qq|<hr>$boch_pet<br><input type="text" name="boch_pet" value="$m{boch_pet}" class="text_box_b"><br>|; 
	}
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="変更する" class="button1"></p></form>|;
	&n_menu;
}

sub tp_1 {
	if ($in{mode} eq 'write') {
		my %datas = ();
		open my $fh, "+< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		my $line = <$fh>;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$datas{$k} = $v;
		}
		
		my $is_rewrite = 0;
		for my $profile (@profiles) {
			unless ($in{$profile->[0]} eq $datas{$profile->[0]}) {
				&error("$profile->[1] に不正な文字( ,\'\"\;<> )が含まれています")	if $in{$profile->[0]} =~ /[;<>]/;
				&error("$profile->[1] は全角80(半角160)文字以内です")		if length($in{$profile->[0]}) > 160;
				if ($profile->[0] ne 'birthday') {
					$datas{$profile->[0]} = $in{$profile->[0]};
					$is_rewrite = 1;
				} elsif (!$datas{$profile->[0]} =~ /(\d{4})\/(\d{2})\/(\d{2})/) {
#					&error("$profile->[1] が不正です(2000/01/01)の形式で入力してください。") if &valid_date($in{$profile->[0]});
					$datas{$profile->[0]} = $in{$profile->[0]};
					$is_rewrite = 1;
				}
			}
		}
		if ($is_rewrite) {
			my $new_line = '';
			while ( my($k, $v) = each %datas ) {
				$new_line .= "$k;$v<>";
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh $new_line;
			close $fh;
			
			$mes .= 'ﾌﾟﾛﾌｨｰﾙを変更しました<br>';
			&n_menu;
		}
		else {
			close $fh;
			$mes .= 'やめました<br>';
		}
		if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
			unless ($in{boch_pet} eq $m{boch_pet}){
				&error("ﾍﾟｯﾄ名は全角10(半角20)文字以内です") if length($in{boch_pet}) > 20;
			}
			$m{boch_pet} = $in{boch_pet};
			$mes .= $m{sex} eq '1' ? '脳内嫁に名前を付けました<br>':'ﾏｽｺｯﾄｷｬﾗに名前を付けました<br>';
		}
		if ($w{world} eq $#world_states-4) {
			if ($in{voice}) {
				require './lib/fate.cgi';
				if (&regist_attack($in{trigger}, $in{timing}, $in{demerit}, $in{max_count}, $in{effect}, $in{voice}, $in{random})) {
					$mes .= '必殺技を設定しました。';
				}
			}
		}
	}
	else {
		$mes .= 'やめました<br>';
	}

	&refresh;
	&n_menu;
}

sub valid_date {
	my $date = shift;
	if ($date =~ /(\d{4})\/(\d{2})\/(\d{2})/) {
		my $year = $1;
		my $month = $2;
		my $day = $3;
		my(@mlast) = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
		
		if ($month < 1 || 12 < $month) { return 1; }
		
		if ($month == 2) {
			if ( (($year % 4 == 0) && ($year % 100 != 0)) || ($year % 400 == 0) ) {
				$mlast[1]++;
			}
		}
		
		if ($day < 1 || $mlast[$month-1] < $day) { return 1; }
		
		return 0;
	}
	return 1;
}

1; # 削除不可
