require './lib/move_player.cgi';
my $this_file = "$logdir/$m{country}/violator.cgi";
#=================================================
# ���ݒ� Created by Merino
#=================================================

# �Ǖ�����[(����\�҂�5�l)
my $need_vote_violator = 2;

# �ꊇ���M�ɕK�v�Ȕ�p
my $need_money = 3000;

# �Ǖ��S������
my $violator_penalty = 3 * 24 * 3600;
# ���O�ދ��S������
my $deportation_penalty = 12 * 3600;

# ��t�z
my $investment_money = 1000000;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!&is_daihyo) {
		$mes .= '���̑�\\�҂łȂ��ƍs�����Ƃ��ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ����s���܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '���̺���ނ́A���̑�\\�҂̂ݍs�����Ƃ��ł��܂�<br>';
		$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="��\\�]�c��" class="button1"></form>|;
	}
	
	&menu('��߂�', '��\\�]�c��', '�����ꊇ���M', '�ŗ�����', '�Ǖ��ҋc��', '�Ǖ��Ґ\\��', '����\\�����C','���Ɋ�t', '��ĕ\�쐬');
}
sub tp_1 {
	return if &is_ng_cmd(1..8);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}


#=================================================
# �]�c������
#=================================================
sub tp_100 {
	$mes .= qq|�e���̑�\\�҂̂ݓ������邱�Ƃ��ł��܂�<br>|;
	$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��\\�]�c��" class="button1"></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	&begin;
}

#=================================================
# �ꊇ���M
#=================================================
sub tp_200 {
	$mes .= "���̍��ɏ���������ڲ԰�S���Ɏ莆�𑗂邱�Ƃ��ł��܂�<br>";
	$mes .= "�P��̑��M�� $need_money G������܂�<br>";

	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ꊇ���M/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	if ($in{comment}) {
		&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;

		if ($m{money} >= $need_money) {
			$in{comment} .= "<hr>�y$cs{name}[$m{country}]�S���ɑ��M�z";
			
			open my $fh_m, "< $logdir/$m{country}/member.cgi";
			while (my $line_m = <$fh_m>) {
				$line_m =~ tr/\x0D\x0A//d;
				
				my $y_id = unpack 'H*', $line_m;
				next unless -f "$userdir/$y_id/letter.cgi";
				
				my @lines = ();
				open my $fh, "+< $userdir/$y_id/letter.cgi" or &error('�ꊇ���M�Ɏ��s���܂���');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					push @lines, $line;
					last if @lines >= $max_log-1;
				}
				unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$in{comment}<>$m{icon}<>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				# �莆��������׸ނ����Ă�
				&set_letter_flag($y_id, 2);
=pod
				my $letters = 0;
				if(-f "$userdir/$send_id/letter_flag.cgi"){
					open my $fh9, "< $userdir/$y_id/letter_flag.cgi";
					my $line = <$fh9>;
					($letters) = split /<>/, $line;
					close $fh9;
				}
				$letters++;
				
				open my $fh9, "> $userdir/$y_id/letter_flag.cgi";
				print $fh9 "$letters<>";
				close $fh9;
=cut
			}
			close $fh_m;
			
			$m{money} -= $need_money;
			$mes .= "$need_money G�x�����A$cs{name}[$m{country}]�S���Ɏ莆�𑗐M���܂���<br>";
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# �ŗ��ύX
#=================================================
sub tp_300 {
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{tax} [1%�`99%]�F<input type="text" name="tax" value="" class="text_box_s" style="text-align:right">% ���݁F$cs{tax}[$m{country}]%<br>|; # ���l����
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;

	$mes .= qq|<div>|;
	$mes .= qq|<label>| unless $is_moble;
	$mes .= qq|<input type="radio" name="mode" value="0" checked="checked">���l����<br>|;
	$mes .= qq|</label>| unless $is_moble;
	$mes .= qq|<label>| unless $is_moble;
	$mes .= qq|<input type="radio" name="mode" value="1">1% �ɕύX����<br>|;
	$mes .= qq|</label>| unless $is_moble;
	$mes .= qq|<label>| unless $is_moble;
	$mes .= qq|<input type="radio" name="mode" value="2">99% �ɕύX����|;
	$mes .= qq|</label>| unless $is_moble;
	$mes .= qq|</div>|;

	$mes .= qq|<br><input type="submit" value="�ύX����" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	if ($in{mode} < 1 && $in{tax} && $cs{tax}[$m{country}] ne $in{tax}) {
		&error("$e2j{tax}�𔼊p�����ŋL�����Ă�������") if $in{tax} eq '' || $in{tax} =~ /[^0-9]/;
		&error("$e2j{tax}��1% �` 99%�܂łł�") if $in{tax} < 1 || $in{tax} > 99;

		$mes .= "$e2j{tax}�� $in{tax} %�ɕύX���܂���<br>";
		$cs{tax}[$m{country}] = $in{tax};
		&write_cs;
	}
	elsif ($in{mode} == 1 && $cs{tax}[$m{country}] != 1) {
		$mes .= "$e2j{tax}�� 1 %�ɕύX���܂���<br>";
		$cs{tax}[$m{country}] = 1;
		&write_cs;
	}
	elsif ($in{mode} == 2 && $cs{tax}[$m{country}] != 99) {
		$mes .= "$e2j{tax}�� 99 %�ɕύX���܂���<br>";
		$cs{tax}[$m{country}] = 99;
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# �Ǖ��ҋc��
#=================================================
sub tp_400 {
	$layout = 1;

	my $vote_disagree = 5 - $need_vote_violator;
	my $find = 0;

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��߂�" class="button1"></form>|;
	
	$mes .= "�c���ɂ��r�炵�⍑�̕��j�ɏ]��Ȃ��҂���������Ǖ����邱�Ƃ��ł��܂�<br>";
	$mes .= "�^����$need_vote_violator�[�ȏ�F�Ǖ��҂���������Ǖ�<br>";
	$mes .= "���΂�$vote_disagree�[�ȏ�F�\\��������\\�҂�������Ǖ�<br>";
	$mes .= "<hr>�Ǖ���ؽ�<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $w_span) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		my $type_mes = $w_span == 1 ? '�w�Ǖ��x' : '�w���O�ދ��x������';
		
#		$mes .= qq|<hr><input type="hidden" name="cmd" value="$no">|;
		$mes .= qq|<hr>|;
		$mes .= qq|�w$message�x�𗝗R�Ɂw$violator�x��$type_mes���ׂ���$name���\\��<br>|;
#		$mes .= qq|���R�F<br>|;
		$mes .= qq|<input type="radio" name="answer_$no" value="1" checked>�^�� $yes_c�[�F$yess<br>|;
		$mes .= qq|<input type="radio" name="answer_$no" value="2">���� $no_c�[�F$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="checkbox" name="$no" value="1">���[|;
		$find = 1;
	}
	close $fh;
	$mes .= qq|<hr><input type="submit" value="���[" class="button_s"></form>| if $find;

	$m{tp} += 10;
}
sub tp_410 {
#	if (!$in{answer} || $in{answer} =~ /[^12]/) {
#		$mes .= '��߂܂���<br>';
#		&begin;
#		return;
#	}

	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $w_span) = split /<>/, $line;

#		if ($cmd eq $no) {
		if ($in{$no}) {
			my $answer = $in{"answer_$no"};
			# �\�������̂������Ŕ��΂Ȃ�\�������
			if ($m{name} eq $name && $answer eq '2') {
				$mes .= "$violator�̒Ǖ��\\��������܂���<br>";
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("�����̕]�c�ɂ͓��[���邱�Ƃ��ł��܂���");
			}

			my $v_id = unpack 'H*', $violator;
			# �����폜�Ȃǂŏ����Ă����ꍇ�͏��O
			if (!-f "$userdir/$v_id/user.cgi") {
				$mes .= "$violator�Ƃ�����ڲ԰�����݂��܂���<br>";
				next;
			}
			# �����ɂ��Ȃ��ꍇ�͏��O
			elsif ( !&is_my_country($violator) ) {
				$mes .= "$violator�Ƃ�����ڲ԰��$cs{name}[$m{country}]�ɏ������Ă���܂���<br>";
				next;
			}

			# ���łɎ������ǂ��炩�ɓ���Ă����ꍇ�̂��߂ɁA��񔒎��ɂ���
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{name} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{name} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($answer eq '1') {
				$new_yess .= "$m{name},";
				$mes .= "$violator�̒Ǖ��Ɏ^�����܂�<br>";
			}
			elsif ($answer eq '2') {
				$new_nos .= "$m{name},";
				$mes .= "$violator�̒Ǖ��ɔ��΂��܂�<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_cn = @yes_c;
			my $no_cn  = @no_c;
			my $penalty_time = $w_span == 1 ? $violator_penalty : $deportation_penalty;
			
			my $vote_disagree = 5 - $need_vote_violator;
			
			if ($yes_cn >= $need_vote_violator) {
				my %datas = &get_you_datas($v_id, 1);
				&move_player($violator, $datas{country}, 0);

				my @data = (
					['wt', $penalty_time],
					['country', 0],
					['lib', ''],
					['tp', 0],
				);
				&regist_you_array($violator, @data);
#				&regist_you_data($violator, 'wt', $penalty_time);
#				&regist_you_data($violator, 'country', 0);
#				&regist_you_data($violator, 'lib', '');
#				&regist_you_data($violator, 'tp', 0);
				if($w_span == 2){
					# ��\�߲�Ĕ���
					my @data2 = (
						['war_c', 0],
						['dom_c', 0],
						['mil_c', 0],
						['pro_c', 0],
					);
					&regist_you_array($violator, @data2);
#					for my $k (qw/war dom mil pro/) {
#						my $kc = $k . "_c";
#						&regist_you_data($violator, $kc, 0); # ��������Ȃ��� 0 �H
#					}
				}

				&write_world_news("�y�c���z$cs{name}[$m{country}]�̑�\\�ҒB�̕]�c�ɂ��A$violator�����O�Ǖ��ƂȂ�܂���", 1, $violator);
				$mes .= "�^����$need_vote_violator�[�ȏ�ɂȂ����̂�$violator���Ǖ�����܂���<br>";
			}
			elsif ($no_cn >= $vote_disagree) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # �\�������l�������Ă����ꍇ
				&move_player($name, $country, 0);

				my @data = (
					['wt', $penalty_time],
					['country', 0],
					['lib', ''],
					['tp', 0],
				);
				&regist_you_array($name, @data);
#				&regist_you_data($name, 'wt', $penalty_time);
#				&regist_you_data($name, 'country', 0);
#				&regist_you_data($name, 'lib', '');
#				&regist_you_data($name, 'tp', 0);
				if($w_span == 2){
					# ��\�߲�Ĕ���
					my @data2 = (
						['war_c', 0],
						['dom_c', 0],
						['mil_c', 0],
						['pro_c', 0],
					);
					&regist_you_array($name, @data2);
#					for my $k (qw/war dom mil pro/) {
#						my $kc = $k . "_c";
#						&regist_you_data($name, $kc, 0);
#					}
				}

				&write_world_news("�y�c���z$cs{name}[$m{country}]�̑�\\�ҒB�̕]�c�ɂ��A$name�����O�Ǖ��ƂȂ�܂���", 1, $name);
				$mes .= "���΂�$vote_desagree�[�ȏ�ɂȂ����̂�$name���Ǖ�����܂���<br>";
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>$w_span\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#=================================================
# �Ǖ��Ґ\��
#=================================================
sub tp_500 {
	$mes .= qq|�����̑�\\�ҒB�̋c���ɂ�莩������ڲ԰��Ǖ����邱�Ƃ��ł��܂�<br>|;
	$mes .= qq|�������\\�������̂�����ꍇ�́A�Ǖ��ҋc���Ŕ��΂ɓ���Ă�������<br>|;
	$mes .= qq|<hr>�Ǖ��Ґ\\��<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���O�F<input type="text" name="violator" class="text_box1"><br>|;
	$mes .= qq|���R[�S�p40(���p80)�����܂�]�F<br><input type="text" name="message" class="text_box_b">|;
	$mes .= qq|<br><input type="radio" name="w_span" value="1" checked>�Ǖ�<br>|;
	$mes .= qq|<input type="radio" name="w_span" value="2">���O�ދ�<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�\\������" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_510 {
	if ($in{violator} && $in{message}) {
		&error('���������������܂��S�p40(���p80)�����܂�') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
			if ( &is_my_country($in{violator}) ) {
				my @lines = ();
				open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
				eval { flock $fh, 2; };
				push @lines, $_ while <$fh>;
				my($last_no) = (split /<>/, $lines[$#lines])[0];
				++$last_no;
				push @lines, "$last_no<>$m{name}<>$m{country}<>$in{violator}<>$in{message}<>$m{name},<><>$in{w_span}<>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				$mes .= "$in{violator}��$in{message}�̗��R�ŒǕ��҂Ƃ��Đ\\�����܂���<br>";
			}
			else {
				$mes .= "$cs{name}[$m{country}]��$in{violator}�Ƃ�����ڲ԰���������Ă��܂���<br>";
			}
		}
		else {
			$mes .= "$in{violator}�Ƃ�����ڲ԰�����݂��܂���<br>";
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# ���̑�\���C
#=================================================
sub tp_600 {
	$mes .= "���ݑ�\\�ƂȂ��Ă����\\�߲�Ă�����ؾ�Ă���܂�<br>";
	$mes .= "$e2j{ceo}�̎��C��$e2j���[���玫�C���Ă�������<br>";
	$mes .= "���̑�\\�҂����C���܂���?<br>";
	&menu('��߂�', '���C����');

	$m{tp} += 10;
}
sub tp_610 {
	return if &is_ng_cmd(1);

	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$mes .= "$e2j{ceo}�̎��C��$e2j{ceo}���[�ōs���Ă�������<br>";
		&begin;
		return;
	}

	for my $k (qw/war pro dom mil/) {
		if ($cs{$k}[$m{country}] eq $m{name}) {
			$cs{$k}[$m{country}] = '';
			$cs{$k.'_c'}[$m{country}] = 0;
			&write_cs;
			
			$m{$k.'_c'} = 0;
			&mes_and_world_news("$e2j{$k}�����C���܂���", 1);
			last;
		}
	}
	
	&begin;
}

#=================================================
# ���Ɋ�t
#=================================================
sub tp_700 {
	$mes .= "���� $investment_money G��t���č����������܂�<br>";
	$mes .= "���Ɋ�t���܂���?<br>";
	&menu('��߂�', '��t����');

	$m{tp} += 10;
}
sub tp_710 {
	return if &is_ng_cmd(1);

	if ($m{money} < $investment_money) {
		$mes .= "����������܂���<br>";
		&begin;
		return;
	}
	
	unless (-f "$logdir/$m{country}/additional_investment.cgi") {
		open my $fh, "> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi ���ǂݍ��߂܂���");
		close $fh;
	}
	open my $fh, ">> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi ���ǂݍ��߂܂���");
	print $fh "$w{year}<>$m{name}<>\n";
	close $fh;
	
	$m{money} -= $investment_money;
	
	&begin;
}

#=================================================
# ��ĕ\�쐬
#=================================================
sub wl {
	my ($hour, $min, $min2) = @_;
	$min += $min2;
	if ($min >= 60) {
		# ���� 60 �ȏ�Ȃ玞�𑝂₵�ĕ��� 60 ������
		$hour += int($min / 60);
		$min = $min % 60;
	}
	return sprintf("%02d:%02d", $hour, $min);

}
sub tp_800 {
	$layout = 2;

	# ��ĕ\�e���v���[�g�̓ǂݍ���
	# �t�@�C�����Ȃ���΃f�t�H���g�e���v���[�g
	my @templates = ();
	my $p_id = unpack 'H*', $m{name};
	if (!(-e "$userdir/$p_id/isseihyo.cgi") || (-s "$userdir/$p_id/isseihyo.cgi") < 1) {
		push(@templates, "�ʏ�^(�����e���v��)<>0;������<>15;�ʏ픭<>23;�{����<>25;�z���E��픭<>45;��ē�<>47;��풅<>\n");
		open my $fh, "> $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ̧�ق��ǂݍ��߂܂���");
		print $fh $templates[0];
		close $fh;
	}
	else {
		open my $fh, "< $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ̧�ق��ǂݍ��߂܂���");
		while (my $l = <$fh>) {
			push(@templates, $l) if $l ne "\n";
		}
		close $fh;
	}

	my @wars_type = ();
	my @text = ();
	for my $i (0 .. $#templates) {
		my @line = split("<>", $templates[$i]);
		push(@wars_type, $line[0]); # �e���v���̖��O���擾
		$templates[$i] =~ s|<>|<>\n|g; # ���[�U�[���ҏW���₷���悤�ɉ��s
	}

	my ($min, $hour) = (localtime($time))[1 .. 2];
	my $now = sprintf("%02d:%02d", $hour, $min);

	# ���������ň�ԋ߂� 5 �� 0 �Ɋۂ߂������20����
	my $min_low = $min - int(($min * 0.1)) * 10;
	$min += $min_low < 5 ? 25 - $min_low : 30 - $min_low;
	if ($min >= 60) {
		# ���� 60 �ȏ�Ȃ玞�𑝂₵�ĕ��� 60 ������
		$hour += int($min / 60);
		$min = $min % 60;
	}

	my $ttime = sprintf("%02d:%02d", $hour, $min);

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|�J�n�����F<input type="text" name="time" value="$ttime" class="text_box_s"> ���݁F$now<br><br>|;

	$mes .= qq|�ڕW�F<select name="target">|;
	for my $target (1 .. $w{country}) {
		$mes .= qq|<option value="$target" label="$cs{name}[$target]">$cs{name}[$target]</option>|;
	}
	$mes .= qq|</select><br><br>|;

	$mes .= qq|�e���v���F<select name="type">|;
	for my $type (0 .. $#wars_type) {
		$mes .= qq|<option value="$type" label="$wars_type[$type]">$wars_type[$type]</option>|;
	}
	$mes .= qq|</select><br><br>|;

	$mes .= qq|�z���l���F<input type="text" name="hukoku" value="$m{name}" class="text_box_s"><br><br>|;
	$mes .= qq|���l���F<input type="text" name="teisen" value="" class="text_box_s"><br><br>|;

	$mes .= qq|���āF<select name="text">|;
	$mes .= qq|<option value="" label="----">���ɂȂ�</option>|;
	$mes .= qq|<option value="�����W��" label="�����W��">�����W��</option>|;
	$mes .= qq|</select><br><br>|;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�쐬����" class="button1"><br><br>|;
	$mes .= qq|<hr>�e�s���ɂ͕K��&lt;&gt;����������<br>1�s�ڂ���ĕ\\�̖���<br>�Z�~�R�����̍����ɊJ�n��������ɂ���n������w��A<br>�Z�~�R�����̉E���ɂ��̎����̍s��������<br>|;

	for my $i (0 .. 4) {
		$mes .= qq|<textarea name="text_$i" rows="10" cols="25">$templates[$i]</textarea><br>|;
	}
	$mes .= qq|</form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_810 {
	if ($in{time}) {
		my @templates = ();
		my $p_id = unpack 'H*', $m{name};
		open my $fh, "> $userdir/$p_id/isseihyo.cgi" or &error("$userdir/$p_id/isseihyo.cgi ̧�ق��ǂݍ��߂܂���");
		for my $i (0 .. 4) {
			$in{"text_$i"} =~ s|&lt;&gt;|<>|g;
			$in{"text_$i"} =~ s|&#59||g;
			print $fh qq/$in{"text_$i"}\n/;
			push(@templates, $in{"text_$i"});
		}
		close $fh;

		my ($hour, $min) = split(/:/, $in{time});
		my $sub_mes = "�ڕW�F$cs{name}[$in{target}]\n\n";
		my @line = split( /<>/, $templates[$in{type}] );
		for my $i (1 .. $#line) {
			my @array = split( /;/, $line[$i]);
			$sub_mes .= &wl($hour, $min, $array[0])." $array[1]\n";
		}
		$sub_mes .= "\n�z���F$in{hukoku}\n";
		$sub_mes .= "���F$in{teisen}";
		$sub_mes .= "\n\n$in{text}" if $in{text};

		$mes .= qq|<textarea name="text_$i" rows="15" cols="35">$sub_mes</textarea><br>|;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#=================================================
# �Ǖ����悤�Ƃ��Ă���l�͎����̐l? 1(true) or 0(false)
#=================================================
sub is_my_country {
	my $name = shift;
	open my $fh, "< $logdir/$m{country}/member.cgi" or &error("$logdir/$m{country}/member.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		return 1 if $line eq $name;
	}
	close $fh;
	return 0;
}


1; # �폜�s��
