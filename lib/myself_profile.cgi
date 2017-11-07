require "$datadir/profile.cgi";
#================================================
# ﾌﾟﾛﾌｨｰﾙ設定 Created by Merino
#================================================

my @mail_alarm_names = ('日記', '改造案');
my @mail_alarm_types = ('diary', 'kaizou');

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
			$mes .= qq|<hr>$profile->[1] 入力例：2000/01/01<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
		else {
			$mes .= qq|<hr>$profile->[1]<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
	}
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		my $boch_pet = $m{sex} eq '1' ? '脳内嫁' : 'ﾏｽｺｯﾄｷｬﾗ';
		$mes .= qq|<hr>$boch_pet<br><input type="text" name="boch_pet" value="$m{boch_pet}" class="text_box_b"><br>|; 
	}
	# 日記・改造案 system.cgi も要修正
	my @mail_datas = split /,/, $m{mail_address}; # [0]ﾒｰﾙｱﾄﾞﾚｽ [1]日記 [2]改造案
	$mes .= qq|<hr>メールアドレス（手紙の受信通知に利用）<br><input type="text" name="mail_address" value="$mail_datas[0]" class="text_box_b"><br>|; 

	for my $i (0 .. $#mail_alarm_types) {
		my $checked = $mail_datas[$i+1] ? ' checked' : '';
		$mes .= qq|<input type="checkbox" name="mail_alarm_$mail_alarm_types[$i]" value="1"$checked>$mail_alarm_names[$i] |;
	}
	$mes .= '※個人宛は必ず通知されます';

#	if ($w{world} eq $#world_states-4) {
#		require './lib/fate.cgi';
#		$mes .= &regist_mes(0);
#	}
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
				} elsif (!($datas{$profile->[0]} =~ /(\d{4})\/(\d{2})\/(\d{2})/)) {
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

		my @mail_datas = split /,/, $m{mail_address};
		unless ($in{mail_address} eq $mail_datas[0] && $mail_datas[1] eq $in{mail_alarm_diary} && $mail_datas[2] eq $in{mail_alarm_kaizou}) {
			if ($in{mail_address} =~ /^[^@]+@[^.]+\..+/) {
				for my $i (0 .. $#mail_alarm_types) {
					$in{mail_address} .= qq|,$in{"mail_alarm_$mail_alarm_types[$i]"}|;
				}
				$m{mail_address} = $in{mail_address};
				$mes .= 'メールアドレスを設定しました<br>';
			}
			elsif ($in{mail_address} eq '') {
				$m{mail_address} = '';
				$mes .= 'メールアドレスを削除しました<br>';
			}
			else {
				&error("入力されたメールアドレスが正しくありません");
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
