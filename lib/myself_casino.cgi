my $this_file       = "$userdir/$id/shop_casino.cgi";
my $this_pool_file  = "$userdir/$id/casino_pool.cgi";
my $shop_list_file  = "$logdir/shop_list_casino.cgi";
require "$datadir/slots.cgi";
#================================================
# ��@����
#================================================

# ���ݔ�p
my $build_money = 100000;


if ($m{coin} > 2500000) {
	$m{coin} = 2500000;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����̶��ɂ̐ݒ�����܂�<br>";
		$mes .= "��$sales_ranking_cycle_day���Ԃ��X�̔��オ�Ȃ��Ƃ��X�͎����I�ɕX�ɂȂ�܂�<br>";
	}
	&menu('��߂�','��{��', '��ǉ�', '���X�̏Љ�', '���X�����Ă�', '��݂��߰ق���');
}

sub tp_1 {
	return if &is_ng_cmd(1..5);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '���l') {
			$mes .= "�E�Ƃ����l�łȂ��Ƃ��X�����Ă邱�Ƃ��ł��܂���<br>";
			&begin;
		}
		else {
			$mes .= "���X�����Ă�ɂ� $build_money G������܂�<br>";
			$mes .= "�����l�̂��X�ݷݸނ̍X�V���߂����Ɍ��Ă�Ƃ����ɕX���Ă��܂��܂�<br>";
			&menu('��߂�','���Ă�');
		}
	}
	elsif (!-f $this_file) {
		$mes .= '�܂��́A���X�����Ă�K�v������܂�<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# ����
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('���X�����Ă�̂Ɏ��s���܂���');
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_casino.cgi" or &error('��ٽ̧�ق��J���܂���');
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_casino.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
			print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
			close $fh3;
			
			open my $fh4, "> $this_pool_file" or &error('�v�[��̧�ق��J���܂���');
			print $fh4 "0<>0<>0<>";
			close $fh4;
			chmod $chmod, "$this_pool_file";
	
			&mes_and_send_news("<b>�l���ɂ����Ă܂���</b>", 1);
			$mes .= '<br>�����������X�ɐV�����ׂ܂��傤<br>';
			$m{money} -= $build_money;
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}

#=================================================
# ��{��
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;

	$mes .= '���j�����܂���?<br>';
	$mes .= '���X�̑�ꗗ<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>�䖼</th><th>���[�g</th><th>���v��</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="checkbox" name="cmd_$no" value="1">$slots[$slot_no][1]</td><td align="right">$ratio ���</td><td align="right">$profit</td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>���[�g�F<input type="text" name="ratio" value="1" class="text_box1" style="text-align:right">���</p>|;
	$mes .= qq|<p>���v���F<input type="text" name="profit" value="-100" class="text_box1" style="text-align:right">%</p>|;
	$mes .= qq|<p>�j��<input type="checkbox" name="delete" value="1"></p>|;
	$mes .= qq|<p><input type="submit" value="�ύX" class="button1"></p></form>|;
	
	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	my $checked = 0;
	
	if ($in{ratio} =~ /[^0-9]/ || $in{ratio} < 0 || $in{ratio} > 2500000) {
		$mes .= '���[�g���s���ł��B';
		&begin;
		return;
	}
	if ($in{profit} !~ /^-?[0-9]+$/ || $in{profit} > 100 || $in{profit} < -100) {
		$mes .= '���v�����s���ł��B';
		&begin;
		return;
	}
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
		
		if ($in{"cmd_$no"} && $in{ratio} ne '0') {
			$checked = 1;
			if ($in{delete} eq '1') {
				$mes .= "$slot_name��j�����܂���<br>";
			} else {
				if ($slots[$slot_no][5]) {
					$profit = $in{profit} / 100.0;
				}
				push @lines, "$no<>$slot_no<>$in{ratio}<>$profit<>\n";
			}
		} else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if($checked){
		&tp_100;
	}else{
		&begin;
	}
}

#=================================================
# �V��ǉ�
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;
	
	$mes .= '�ǂ��ǉ����܂���?<br>';
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	for my $i (1..$#slots) {
		$profit = $slots[$i][5] ? qq|<input type="text" name="profit_$i" value="0" class="text_box1" style="text-align:right">%| : $slots[$i][2];
		$mes .= qq|<input type="radio" name="cmd" value="$i">$slots[$i][1] ���v��:$profit ������:$slots[$i][3]<br>|;
	}
	
	$mes .= qq|<p>���[�g�F<input type="text" name="ratio" value="1" class="text_box1" style="text-align:right">���</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�V��ǉ�" class="button1"></p></form>|;
	
	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	if ($cmd && $m{money} >= $slots[$cmd][3]) {
		my @shop_items = ();
		open my $in, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		push @shop_items, $_ while <$in>;
		close $in;
		
		if ($in{ratio} =~ /[^0-9]/ || $in{ratio} <= 0 || $in{ratio} > 2500000) {
			$mes .= '���[�g�� 1 ��� �ȏ� 250��0000 ��݈ȓ��ɂ���K�v������܂�<br>';
			&begin;
			return;
		}
		$profit = $slots[$cmd][2];
		if ($slots[$cmd][5]) {
			if ($in{"profit_$cmd"} !~ /^-?[0-9]+$/ || $in{"profit_$cmd"} > 100 || $in{"profit_$cmd"} < -100) {
				$mes .= '���v���� -100�ȏ� 100�ȉ��ɂ���K�v������܂�<br>';
				&begin;
				return;
			}
			$profit = $in{"profit_$cmd"} / 100.0;
		}
		
		my($last_no) = (split /<>/, $shop_items[-1])[0];
		++$last_no;
		
		open my $fh2, ">> $this_file" or &error("$this_file���J���܂���");
		print $fh2 "$last_no<>$slots[$cmd][0]<>$in{ratio}<>$profit<>\n";
		close $fh2;
		
		$m{money} -= $slots[$cmd][3];
		
		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# ���X�̐ݒ�
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('���XؽĂ��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|�O��̔���F$sale_c�� $sale_money G<br>|;
			$mes .= qq|<hr>���X�̖��O[�S�p8(���p16)�����܂�]�F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|�Љ[�S�p20(���p40)�����܂�]�F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# ���X������̂�ؽĂɂȂ��̂͂��������̂ł�����x�ǉ�
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
		print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
		close $fh3;
	}
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= '��߂܂���';
		&begin;
		return;
	}
	
	&error('���X�̖��O���������܂��B�S�p8(���p16)�����܂�') if length $in{name} > 16;
	&error('�Љ���������܂��B�S�p20(���p40)�����܂�') if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	my %names = ();
	open my $fh, "+< $shop_list_file" or &error('���XؽĂ��J���܂���');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		next if $names{$name}++;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "���X�̖��O�� $in{name} �ɕς��܂���<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "�Љ�� $in{message} �ɕς��܂���<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}
			
			if ($is_rewrite) {
				unless ($m{guild_number}){
					$m{guild_number} = 0;
				}
				$guild_number = $m{guild_number};
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("���łɓ������O�̂��X�����݂��܂�");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#=================================================
# ��݃v�[��
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_pool_file" or &error("$this_pool_file���J���܂���");
	my $pool, $this_term_gain, $slot_runs;
	while (my $line = <$fh>){
		($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
	}
	close $fh;

	$mes .= qq|�����o���ۂɂ�1��݈ȏ�c���Ă�������|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���݂̃v�[����ݐ��F$pool���<br>|;
	$mes .= qq|<input type="radio" name="multiple" value="1" checked>�v�[������<br>|;
	$mes .= qq|<input type="radio" name="multiple" value="-1">�����o��<br>|;
	$mes .= qq|<input type="text" name="pool" value="0" class="text_box_b"> ���<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�v�[������" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_510 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	unless (-f $this_pool_file) {
		&begin;
		return;
	}
	
	$push = $in{multiple} * $in{pool};

	if ($m{coin} < $push) {
		$push = $m{coin};
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "+< $this_pool_file" or &error("$this_pool_file���J���܂���");
	eval { flock $fh, 2; };
	
	while (my $line = <$fh>){
		my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
		if ($pool + $push > 0) {
			$pool += $push;
			$m{coin} -= $push;
		}
		push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
	}
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "��݂��v�[�����܂���<br>";
	&begin;
}

1; # �폜�s��
