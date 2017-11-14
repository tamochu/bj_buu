#=================================================
# ���� Created by Merino
#=================================================

# �ŗ��F����70�̐����𑝂₷�Ɠ�Փx���ȒP�ɁA���炷�Ɠ�Փx������Ȃ��
sub tax { ($cs{tax}[$m{country}] + 70) * 0.01 };

# ���K�͂̎���
my $GWT_s = int($GWT * 0.6);

# ��K�͂̎���
my $GWT_b = int($GWT * 2);

# ���K�͂̎���
my $GWT_l = int($GWT * 4);

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		if ($m{act} >= 100) {
			$mes .= "�x�����Ƃ�܂�<br>���ɍs���ł���̂� $GWT����ł�";
			$m{act} = 0;
			&refresh;
			&wait;
			return 0;
		}
		else {
			$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
			&refresh;
			&n_menu;
			return 0;
		}
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ����s���܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= '�������s�������̎����𑝂₵�܂�<br>�ǂ���s���܂���?<br>';
	}
	if ($m{tutorial_switch}) {
		require './lib/tutorial.cgi';
		&show_tutorial_message('�����ɂ���Đ푈������̂ɕK�v�ȕ����𒙂߂邱�Ƃ��ł����I<br>�_�ƁE���ƁE�����̂����ꂩ�̏n���x�� 50 �ɂȂ�x�ɕ񏧋����Ⴆ�邩��A�܂��͂����_���Ă݂悤');
	}
	
	&menu('��߂�','�_��','����','����','��������');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);

	if    ($cmd eq '1') { $mes .= "�������̎悵�č���$e2j{food}�𑝂₵�܂�<br>"; }
	elsif ($cmd eq '2') { $mes .= "�������炨���𒥐ł�����$e2j{money}�𑝂₵�܂�<br>"; }
	elsif ($cmd eq '3') { $mes .= "���m���W���č���$e2j{soldier}�𑝂₵�܂�<br>��1�l�ɂ�1G<br>"; }
	elsif ($cmd eq '4') { $mes .= "�_��,����,�������܂Ƃ߂čs���܂�<br>"; $GWT_s *= 3; $GWT_b *= 3; $GWT *= 3; $GWT_l *= 3; }

	$m{tp} = $cmd * 100;
	$mes .= '�ǂ̂��炢�s���܂���?<br>';

	my @size = ('��߂�', "���K��    ($GWT_s��)", "���K��    ($GWT��)", "��K��    ($GWT_b��)", "���K��    ($GWT_l��)");
	&menu(@size);
}

#=================================================
# ����
#=================================================
sub tp_100 { &exe1('�������̎悵�܂�<br>') }
sub tp_200 { &exe1('�����𒥐ł��܂�<br>') }
sub tp_300 { &exe1('���m���ٗp���܂�<br>') }
sub tp_400 { &exe1('�܂Ƃ߂ē������s���܂�<br>') }
sub exe1 {
	return if &is_ng_cmd(1..4);
	my $i = 1;
	if ($m{tp} == 400) { # ��������
		unless ($m{nou_c} >= 5 && $m{sho_c} >= 5 && $m{hei_c} >= 5) {
			$mes .= "�����������s���ɂ́A�_��,����,�����̏n���x��5��ȏ�łȂ��Ƃł��܂���<br>";
			&begin;
			return;
		}
		$i = 3; # ���� 3 ��
	}

	$GWT =  $cmd eq '1' ? $GWT_s * $i
			: $cmd eq '3' ? $GWT_b * $i
			: $cmd eq '4' ? $GWT_l * $i
			:               $GWT   * $i
			;

	$m{tp} += 10;
	$m{turn} = $cmd;
	$mes .= "$_[0]���ʂ�$GWT����<br>";
	&before_action('icon_pet_exp', $GWT);
	&wait;
}

#=================================================
# �������ʗʃ{�[�i�X�ix�{�␳ ��萔�ʃ{�[�i�X��t�������Ȃ�Έʒu�ɒ��Ӂj
#=================================================
sub multi_bonus {
	my ($k, $v) = @_;

	# �������͓�����1.1�{
	$v *= 1.1 if $cs{dom}[$m{country}] eq $m{name};

	# �N��͓�����1.05�{�A�\�N���Ȃ��1.2�{
	$v *= ( ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05 ) if $cs{ceo}[$m{country}] eq $m{name};

	# �y���͓�����1.1�{
	$v *= 1.1 if $m{unit} eq '16';

	# ���ݒ�␳
	$v *= &get_modify('dom');

	# �푰�␳
	$v = &seed_bonus($k, $v);
	$v = &seed_bonus('red_moon', $v);

	return $v;
}

#=================================================
# �_�ƌ���
#=================================================
sub tp_110 {
	my $v = ($m{nou_c} + $m{mat}) * $m{turn} * 10;
	$v  = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '1') {
		$v *= 1.5; # �L��
	}
	elsif ($cs{state}[$m{country}] eq '3') {
		$v *= 0.5; # �\��
	}
	
	$v = &multi_bonus('nou', $v);
	$v = &use_pet('nou', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '28');
	$v = int($v);
	
	$cs{food}[$m{country}] += $v;
	$mes .= "������ $v �̎悵�܂���<br>";
	
	&c_up('nou_c') for (1..$m{turn});
	&write_yran('nou', $v, 1);
	
	return if $m{tp} eq '410';

	&after1;
	$m{turn} = 5 if $m{turn} eq '4';
	&after2;
}
#=================================================
# ���ƌ���
#=================================================
sub tp_210 {
	my $v = ($m{sho_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '2') {
		$v *= 1.5; # �i�C
	}
	elsif ($cs{state}[$m{country}] eq '4') {
		$v *= 0.5; # �s��
	}
	
	$v = &multi_bonus('sho', $v);
	$v = &use_pet('sho', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '29');
	$v = int($v);

	$cs{money}[$m{country}] += $v;
	$mes .= "������ $v ���ł��܂���<br>";

	&c_up('sho_c') for (1..$m{turn});
	&write_yran('sho', $v, 1);

	return if $m{tp} eq '410';

	&after1;
	$m{turn} = 5 if $m{turn} eq '4';
	&after2;
}
#=================================================
# ��������
#=================================================
sub tp_310 {
	my $v = ($m{hei_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '5') {
		$v *= 0.5; # �Q�[
	}
	
	$v = &multi_bonus('hei', $v);
	if ($v < $m{money}){
		$v = &use_pet('hei', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '30');
	}
	$v = int($v);

	$v = $m{money} if $v > $m{money};
	$v = 0 if 0 > $m{money};
	$m{money} -= $v;

	$cs{soldier}[$m{country}] += $v;
	$mes .= "���m�� $v �l�ٗp���܂���<br>";

	if (0 < $v && 0 < $m{money}){
		&c_up('hei_c') for (1..$m{turn});
		&write_yran('hei', $v, 1);
	}

	return if $m{tp} eq '410';

	&after1;
	# �����͂�����������̂ŁA�o���l�ƕ]�������������׽
	$m{turn} = 5 if $m{turn} eq '4';
	$m{turn} += 2 if 0 < $v && 0 < $m{money};
	&after2;
}
#=================================================
# ������������
#=================================================
sub tp_410 {
	&tp_110;
	&tp_210;
	&tp_310;

	&after1;
	$m{turn} = 5 if $m{turn} eq '4';
	$m{turn} *= 4;
	&after2;
}

#=================================================
# �I������
#=================================================
sub after1 { # $m{turn} ����S�����Ԃ�����o����Ō�̃^�C�~���O�ŌĂ΂��
	require './lib/_rampart.cgi'; # ���
	my $i = $m{tp} == 410 ? 3 : 1; # ���� 3 ��F���� 1 ��
	my $g = $m{turn} eq '1' ? $GWT_s * $i
			: $m{turn} eq '3' ? $GWT_b * $i
			: $m{turn} eq '4' ? $GWT_l * $i
			:                   $GWT   * $i
			;
	&gain_dom_barrier($g);

	# �S�����ԂŌ��ʗʕς�邩������Ȃ��̂ł����ɒ�`
	if ($w{world} eq $#world_states - 5 && int(rand(24)) < 1 && $w{reset_time} < $time) { # �ّ����ɊJ�킵�Ă��� 1/24 ��
		my $v = int(rand(50)+1) * 10;
		$cs{strong}[$m{country}] += $v;
		&mes_and_world_news("<b>$c_m��$e2j{strong}��$v�������܂���</b>");
	}
}
sub after2 {
	my $v = int( (rand(3)+4) * $m{turn} );
	$v = &use_pet('domestic', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '160');
	$m{exp} += $v;
	$m{rank_exp} += int( (rand($m{turn}) + $m{turn}) * 2);
	$m{egg_c} += int(rand(3)+3) if $m{egg};
	
	$mes .= "$m{name}�ɑ΂���]�����オ��܂���<br>";
	$mes .= "$v ��$e2j{exp}����ɓ���܂���<br>";

	# ��J��
	$m{act} = 0;
	$mes .= '��J���񕜂��܂���<br>';
	
	&special_money if ($w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1'));

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('domestic');
	}
	
	&daihyo_c_up('dom_c'); # ��\�n���x
	&run_tutorial_quest('tutorial_dom_1');

	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# ���J��
#=================================================
sub special_money { # �����̏I�����������������Ă΂��
	my $v = int($m{rank} * 150 * $m{turn});
	$m{money} += $v;
	$mes .= "���܂ł̌��т��F�߂�� $v G�̌��J������������ꂽ<br>";
}

1; # �폜�s��
