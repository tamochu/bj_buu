use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# �Ղ��̊J�n�E�I���Ŏg���郂�W���[��
# ��ȌĂяo����
# ./lib/reset.cgi
#================================================
# �g�� ����� �n���x�ޯ����� ����ݍs�� �n���xؽı
# �O���u ����� �n���x�ޯ����� ����ݍs�� �n���xؽı
# �ّ� ����� ����ݍs��
# ���� ����� ����ݍs��

#================================================
# �Ղ����ɒǉ�����鍑�̐��E���́E�����E���F�̒�`
#================================================

use constant FESTIVAL_COUNTRY_PROPERTY => {
#		'kouhaku' => [2, 1, ["���̂��̎R", "�����̂��̗�"], ["#ffffff", "#ff0000"]],
#		'sangokusi' => [3, 1, ["�", "��", "�"], ["#4444ff", "#ff4444", "#44ff44"]]
	'kouhaku' => [2,["���̂��̎R", "�����̂��̗�"], ["#ffffff", "#ff0000"]],
	'sangokusi' => [3, ["�", "��", "�"], ["#4444ff", "#ff4444", "#44ff44"]]
};

#================================================
# �Ղ��J�n���̍�����ݒ肵�Ďn�߂�
#================================================
sub begin_festival_world {
	# �Ղ��J�n���̊��������ׂĂ̍����ƌN��t�@�C����������
	# ����ق���Ǝ��ۂɂ��郁���o�[�Ɨ����E���[�f�[�^�Ƃ��ꗂ�������
	for my $i (0 .. $w{country}) {
		$cs{old_ceo}[$i] = $cs{ceo}[$i] if $w{year} % 40 == 0 || $w{year} % 40 == 20; # �g���E�O���u�̂� $cs{old_ceo} �ɑޔ����Ă���
		$cs{ceo}[$i] = '';
		for my $key (qw/war dom mil pro/) {
			$cs{$key}[$i] = '';
			$cs{$key.'_c'}[$i] = 0;
		}
		$cs{member}[$i] = 0;
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		close $fh;
		open my $fh2, "> $logdir/$i/leader.cgi" or &error("$logdir/$i/leader.cgi̧�ق��J���܂���");
		close $fh2;
	}
	&write_cs;

	if ($w{year} % 40 == 0){ # �s��ՓV
		$w{world} = $#world_states-2;
		$w{game_lv} = 99;
		&run_kouhaku(1);
	} elsif ($w{year} % 40 == 20) { # �O���u
		$w{world} = $#world_states-3;
		$w{game_lv} = 99;
		&run_sangokusi(1);
	} elsif ($w{year} % 40 == 10) { # �ّ�
		$w{world} = $#world_states-5;
		$w{game_lv} = 99;
		$w{win_countries} = '';
		$w{reset_time} = $time; # $config_test ? $time: $time + 3600 * 12; # �I�����
		$w{limit_time} = $config_test ? $time: $time + 3600 * 24; # �������
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i]  = 5000;
			$cs{tax}[$i]     = 99;
			$cs{state}[$i]   = 5;
			$cs{food}[$i]    = 999999;
			$cs{money}[$i]   = 999999;
			$cs{soldier}[$i] = 999999;
		}
		&run_sessoku(1);
	} else { # ����
		$w{world} = $#world_states-1;
		&run_konran(1);
	}
}

#================================================
# �Ղ����������ďI����
#================================================
sub end_festival_world {
	if ($w{year} % 40 == 0){ # �s��ՓV
		&run_kouhaku(0);
	} elsif ($w{year} % 40 == 20) { # �O���u
		&run_sangokusi(0);
	} else {
		if ($w{year} % 40 == 10) { # �ّ�
			&run_sessoku(0);
		} else { # ����
			&run_konran(0);
		}
		# �g���E�O���u�͊J�n���ɏ�������������΍ςނ��A
		# �ّ��E�����͌N��f�[�^�Ȃǂ�����̂ŏI�����ɂ�������
		for my $i (1 .. $w{country}) {
			$cs{ceo}[$i] = '';
			for my $key (qw/war dom mil pro/) {
				$cs{$key}[$i] = '';
				$cs{$key.'_c'}[$i] = 0;
			}
			$cs{member}[$i] = 0;
			open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
			close $fh;
			open my $fh2, "> $logdir/$i/leader.cgi" or &error("$logdir/$i/leader.cgi̧�ق��J���܂���");
			close $fh2;
		}
	}
}

#================================================
# �g���̊J�n(1)�ƏI��(0)
#================================================
sub run_kouhaku {
	$is_start = shift;

#	require "./lib/move_player.cgi";
	if ($is_start) { # �g���J�n���̏���	
		&add_festival_country('kouhaku');
		&player_shuffle($w{country}-1..$w{country});
	}
	else { # �g���I�����̏���
		&end_kouhaku_sangokusi('kouhaku');
	}
}

#================================================
# �O���u�̊J�n(1)�ƏI��(0)
#================================================
sub run_sangokusi {
	$is_start = shift;

	require "./lib/move_player.cgi";
	if ($is_start) { # �O���u�J�n���̏���
		&add_festival_country('sangokusi');
		&player_shuffle($w{country}-2..$w{country});
	}
	else { # �O���u�I�����̏���
		&end_kouhaku_sangokusi('sangokusi');
	}
}

# �g�����O���u���I�����̏�������
sub end_kouhaku_sangokusi {
	my $festival_name = shift;

	require "./lib/shopping_offertory_box.cgi";
	my($c1, $c2) = split /,/, $w{win_countries};
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		next unless &you_exists($pid, 1);
		my %you_datas = &get_you_datas($pid, 1);

		if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
			for my $k (qw/war dom pro mil ceo/) {
				if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
					&send_god_item(5, $cs{$k}[$you_datas{country}]);
				}
			}
			open my $fh, ">> $userdir/$pid/ex_c.cgi";
			print $fh "fes_c<>1<>\n";
			close $fh;

			&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
		}

		&move_player2($you_datas{name}, 0);
		# ���ꂵ���L�������s�픻��ɂȂ�󂪂Ȃ��̂Ŕs�픻��͏ȗ�
		if ($you_datas{name} eq $m{name}) { # �Ώۂ����L�����Ȃ��
			$m{country} = 0; # �������̏�������
			$y{country} = 0;
			$m{vote} = ''; # �����E���[�f�[�^�̏�����

			# ��\�n���x��ؽı
			for my $k (qw/war dom pro mil/) {
				$m{"${k}_c"} = $m{"${k}_c_t"};
				$m{"${k}_c_t"} = 0;
			}
			&write_user;
		}
		else { # �Ώۂ����L�����Ȃ��
			my @data = (
				['country', 0],
				['y_country', 0],
				['vote', ''],
			);

			unless ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				my @data2 = (
					['shogo', "$cs{name}[$you_datas{country}](��)"],
					['trick_time', $time + 3600 * 24 * 3],
					['shogo_t', ''] # �̍��Œ�ͱ�ּ���炢�H
				);
				push @data, @data2;
			}

			for my $k (qw/war dom pro mil/) {
				my @data3 = (
					["${k}_c", $you_datas{"${k}_c_t"}],
					["${k}_c_t", 0]
				);
				push @data, @data3;
			}

			&regist_you_array($you_datas{name}, @data);
		}
	}
	closedir $dh;

	# �Ղ�p�̍��������Ēʏ��������ؽı���Ă��܂����� write_cs ��ɂ���� cs_data_repair ���K�v
	&remove_festival_country($festival_name);
	&write_cs;
	&cs_data_repair;
}

#================================================
# �ّ��̊J�n(1)�ƏI��(0)
#================================================
sub run_sessoku {
	$is_start = shift;

	if ($is_start) { # �ّ��J�n���̏���
		&player_shuffle(1..$w{country});
=pod
		����ق��Ȃ��p
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);

			&wt_c_reset(\%m, \%you_datas); # �ғ����ݷݸނ̍X�V��ؾ��	
		}
		closedir $dh;
=cut
	} # �ّ��J�n���̏���
	else { # �ّ��I�����̏���
		require './lib/shopping_offertory_box.cgi';
		require "./lib/move_player.cgi";
		# 1�ʍ��ɂ͓���{�[�i�X�ƍՂ��V
		# (int(����/2)+1)�ʂɂ͓���{�[�i�X
		my @strong_rank = &get_strong_ranking;
		$w{win_countries} = "$strong_rank[0],$strong_rank[1]";

		&write_world_news("<b>$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strong_rank[0]]��$cs{name}[$strong_rank[1]]�̏����ɂȂ�܂���</b>");
		&write_legend('touitu', "$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strong_rank[0]]��$cs{name}[$strong_rank[1]]�̏����ɂȂ�܂���");

#		$cs{strong}[$strong_rank[2]] = 0;
#		$cs{is_die}[$strong_rank[2]] = 3;

		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);

			# �Ղ�n��
			if ($strong_rank[0] eq $you_datas{country} || $strong_rank[1] eq $you_datas{country}) {
				# 1�ʍ��̑�\�ɂ͍Ղ��V
				if ($$strong_rank[0] eq $you_datas{country}) {
					for my $k (qw/war dom pro mil ceo/) {
						if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
							&send_god_item(5, $cs{$k}[$you_datas{country}]);
						}
					}
					&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
			}

			# �l�o��������
			&move_player2($you_datas{name}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$m{vote} = '';
				# ��\�n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					$m{"${k}_c"} = $m{"${k}_c_t"};
					$m{"${k}_c_t"} = 0;
				}
				&write_user;
			} else {
				my @data = (
					['country', 0],
					['vote', '']
				);
				for my $k (qw/war dom pro mil/) {
					my @data2 = (
						["${k}_c", $you_datas{"${k}_c_t"}],
						["${k}_c_t", 0]
					);
					push @data, @data2;
				}
				&regist_you_array($you_datas{name}, @data);
			}

			# �����Ŏg���̂Ŏc���Ă����Ă�������
			# �r���̍��ɂ���v���C���[�͓K���d��
			#elsif ($strong_rank[2] eq $p{country}) {
				#my $to_country = 0;
				#do {
					#$to_country = int(rand($w{country}) + 1);
				#} while ($cs{is_die}[$to_country] > 1);

				#&move_player($p{name}, $p{country}, $to_country);
				#if ($p{name} eq $m{name}){
					#$m{country} = $to_country;
					#&write_user;
				#} else {
					#&regist_you_data($p{name}, 'country', $to_country);
				#}
			#}
		}
	} # �ّ��I�����̏���
}

#================================================
# �����̊J�n(1)�ƏI��(0)
#================================================
sub run_konran {
	$is_start = shift;

#	require "./lib/move_player.cgi";
	if ($is_start) { # �����J�n���̏���
		&player_shuffle(1..$w{country});
	} # �����J�n���̏���
	else { # �����I�����̏���
		my($c1, $c2) = split /,/, $w{win_countries}; # ���ꍑ�̎擾
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless -f "$userdir/$pid/user.cgi";
			my %you_datas = &get_you_datas($pid, 1);

			&move_player2($you_datas{name}, 0);
			if ($you_datas{name} eq $m{name}) { # �Ώۂ����L�����Ȃ��
				$m{country} = 0; # �������̏�������
				$m{vote} = ''; # �����E���[�f�[�^�̏�����
				&write_user;
			}
			else { # �Ώۂ����L�����Ȃ��
				my @data = (
					['country', 0],
					['vote', '']
				);
				&regist_you_array($you_datas{name}, @data);
			}

			# ���ꍑ�ɂ����l�ɗ�
			if ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}
		}
		closedir $dh;
		&write_cs;
	} # �����I�����̏���
}

#================================================
# �w�肳�ꂽ�Ղ��p�̍���ǉ����A����ȊO�̍����ޯ�����
# �ǉ�����鍑�̏��� FESTIVAL_COUNTRY_PROPERTY �Œ�`���Ă���
#================================================
sub add_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	$w{country} += $country_num;
	my $max_c = int($w{player} / $country_num) + 3;
	require './lib/_rampart.cgi';
	for my $i ($w{country}-($country_num-1)..$w{country}){
		mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot_log patrol prison prison_member prisoner violator leader member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
#			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		# ���ɂ�1�s�ڂ��ݒ�Ȃ̂ŗ\�ߏ�������ł����Ȃ��ƍ��ɂɂԂ�����1�ڂ̃A�C�e�����������Ă��܂�
		my $output_file = "$logdir/$i/depot.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		print $fh "1<>1<>1����Lv1�ȏオ���p�ł��܂�<>\n";
		close $fh;
		chmod $chmod, $output_file;

		&add_npc_data($i);
		# create union file
		for my $j (1 .. $i-1) {
			my $file_name = "$logdir/union/${j}_${i}";
			$w{ "f_${j}_${i}" } = -99;
			$w{ "p_${j}_${i}" } = 2;
			next if -f "$file_name.cgi";
			open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
			close $fh;
			chmod $chmod, "$file_name.cgi";
			open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
			close $fh2;
			chmod $chmod, "${file_name}_log.cgi";
			open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
			close $fh3;
			chmod $chmod, "${file_name}_member.cgi";
		}
		unless (-f "$htmldir/$i.html") {
			open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
			close $fh_h;
		}

		my $num = $i-($w{country}+1-$country_num);
		$cs{name}[$i]        = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[1][$num];
		$cs{color}[$i]       = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[2][$num];
		$cs{prison_name}[$i] = '�S��';
		$cs{member}[$i]      = 0;
		$cs{win_c}[$i]       = 999;
		$cs{tax}[$i]         = 99;
		$cs{strong}[$i]      = $max_c * 500; # �d����� * 500
		$cs{food}[$i]        = $config_test ? 999999 : 0;
		$cs{money}[$i]       = $config_test ? 999999 : 0;
		$cs{soldier}[$i]     = $config_test ? 999999 : 0;
		$cs{state}[$i]       = 0;
		$cs{capacity}[$i]    = $max_c;
		$cs{is_die}[$i]      = 0;
		$cs{barrier}[$i]     = &get_init_barrier;
	}

	for my $i (1 .. $w{country}-$country_num) {
		$cs{strong}[$i]   = 0;
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = 0;
		$cs{is_die}[$i]   = 1;

		for my $j ($i+1 .. $w{country}-$country_num) {
			$w{ "f_${i}_${j}" } = -99;
			$w{ "p_${i}_${j}" } = 2;
		}
	}

	my @lines = &get_countries_mes();
	if ($w{country} > @lines) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "<>non_mark.gif<>\n" for 1..$country_num;
		close $fh9;
	}

	# �o�b�N�A�b�v�쐬
	for my $i (0 .. $w{country} - $country_num) {
		my $from = "$logdir/$i";
		my $backup = $from . "_backup";
		rcopy($from, $backup);
	}
	my $from = "$logdir/countries.cgi";
	my $backup = "$logdir/countries_backup.cgi";
	rcopy($from, $backup);
}

#================================================
# �w�肳�ꂽ�Ղ��p�̍����폜���A����ȊO�̍���ؽı
# �폜����鍑�̏��� FESTIVAL_COUNTRY_PROPERTY �Œ�`���Ă���
#================================================
sub remove_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	# ���t�H���_�폜
	for (my $i = $w{country}; $i > $w{country}+1-$country_num; $i--) { # ������+�Í�-�Ղ荑
		my $from = "$logdir/$i";
		my $num = rmtree($from);
	}
	$w{country} -= $country_num;

	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	pop @lines while @lines > $w{country} + 1;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	# ���f�[�^����
	for my $i (0 .. $w{country}) {
		my $from = "$logdir/$i";
		my $backup = $from . "_backup";
		my $num = rmtree($from);
		rcopy($backup, $from);
	}

	my $i = 1;
	open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
	my $world_line = <$fh>;
	while (my $line = <$fh>) {
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
				$cs{$k}[$i] = $v;
			}
		}
		++$i;
	}
	close $fh;
}

#================================================
# �ғ����ݷݸނ̍X�V��ؾ�āi�Ղ�˓�����10�N���j
#================================================
sub wt_c_reset {
	my ($m, $you_datas) = @_;
	if ($$you_datas{name} eq $$m{name}){
		$$m{wt_c_latest} = $$m{wt_c};
		$$m{wt_c} = 0;
		&write_user;
	} else {
		my @data = (
			['wt_c_latest', $$you_datas{wt_c}],
			['wt_c', 0]
		);
		&regist_you_array($$you_datas{name}, @data);
	}
}

#================================================
# �v���[���[�V���b�t��
# �ғ��������ƂɐU�蕪����B
#================================================
sub player_shuffle {
	my @countries = @_;
	
	for my $i (0..$#countries){
		my $j = int(rand(@countries));
		my $temp = $countries[$i];
 		$countries[$i] = $countries[$j];
 		$countries[$j] = $temp;
	}
	
	my %country_num = ();
	for my $c ($countries) {
		$country_num{$c} = 0;
	}
	
	# ���[�U�[�ꗗ�擾
	my @player_line = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		next unless &you_exists($pid, 1);
		my %you_datas = &get_you_datas($pid, 1);

		&wt_c_reset(\%m, \%you_datas); # �ғ����ݷݸނ̍X�V��ؾ��

		# �������V���b�t������Ȃ��� true
		# �g���E�O���u�͊֌W�Ȃ��̂ŏ������Ȃ�
		# �V���b�t������Ȃ��ŋ��c���Ă�l���v���X���� player_line �ɑ����Ȃ�
		if ($you_datas{shuffle} && $w{world} == $#world_states-1) {
			# member.cgi�����������Ă���̂ŃV���b�t���O�̍��ɍēx��΂��Ȃ��ƃf�[�^�̕s��v���N����
			&move_player2($you_datas{name}, $you_datas{country});
			if ($you_datas{country}) { # �d�����Ă����Ȃ�
				$country_num{$you_datas{country}}++;
				next;
			}
#			my $c_find = 0;
#			if ($you_datas{country}) { # �d�����Ă���Ȃ�
#				for my $c (@countries) {
#					if ($c eq $you_datas{country}) {
#						$country_num{$c}++;
#						$c_find = 1;
#					}
#				}
#			}
#			if ($c_find) {
#				next;
#			}
		}
		
		push @player_line, "$you_datas{name}<>$you_datas{wt_c_latest}<>\n";
	}
	closedir $dh;
	
	@player_line = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ] } @player_line;
	
	my $updown = 1;
	my $index = 0;
	my $round = 0;
	my @new_line = ();
	my $mc = @countries;
	for my $pl (@player_line) {
		my $c = $countries[$index];
		my($pname, $pw) = split /<>/, $pl;
		push @new_line, "$pname<>$c<>\n";
		$country_num{$c}++;
		while (1) {
			$index += $updown;
			if ($index < 0) {
				$index = 0;
				$updown = 1;
				$round++;
			} elsif ($index >= $mc) {
				$index = $mc - 1;
				$updown = -1;
				$round++;
			}
			if ($country_num{$countries[$index]} <= $round) {
				last;
			}
		}
	}

	# �U�蕪��
	for my $nl (@new_line) {
		my($nname, $nc) = split /<>/, $nl;
		my $pid = unpack 'H*', $nname;
		my %you_datas = &get_you_datas($pid, 1);

		&move_player2($you_datas{name}, $nc);
		# �Ώۂ����L�����Ȃ��
		if ($you_datas{name} eq $m{name}) {
			$m{country} = $nc; # �������̏�������
			$m{vote} = ''; # �����E���[�f�[�^�̏�����

			# ������łȂ���Α�\�n���x���ޯ�����
			if ($w{world} != $#world_states-1) {
				for my $k (qw/war dom pro mil/) {
					$m{"${k}_c_t"} = $m{"${k}_c"};
					$m{"${k}_c"} = 0;
				}
			}
			&write_user;
		}
		# �Ώۂ����L�����Ȃ��
		else {
			my @data = (
				['country', $nc],
				['vote', '']
			);

			# ������łȂ���Α�\�n���x�̏�������
			if ($w{world} != $#world_states-1) {
				for my $k (qw/war dom pro mil/) {
					my @data2 = (
						["${k}_c_t", $you_datas{"${k}_c"}],
						["${k}_c", 0]
					);
					push @data, @data2;
				}
			}
			&regist_you_array($you_datas{name}, @data);
		}
	}
	&write_cs;
}

#================================================
# �Ղ��p�̃v���C���[�ړ��֐�
# �ʏ�ł���Έړ����E�ړ���̃����o�[�t�@�C���◧���E���[�f�[�^�Ȃǂ��C�����邪�A
# �������������X�̃`�F�b�N���K�v�Ȃ����߃����o�[�t�@�C���ɒǋL���邾��
#================================================
sub move_player2 {
	my($name, $to_country) = @_;

	open my $fh9, ">> $logdir/$to_country/member.cgi" or &error("$logdir/$to_country/member.cgi̧�ق��J���܂���");
	print $fh9 "$name\n";
	close $fh9;
	++$cs{member}[$to_country];
}

=pod
#================================================
# �ꊇ regist_you_data ���鎞�ɍŒ���K�v�ȃf�[�^���쐬���Ԃ�
# ��P������ get_you_datas �̖߂�l�������|�C���^
# ��Q������ user.cgi ��1�s��
# ��R�����͎d����̍��i���o�[
# ��S�����͑�\�n���Ɋւ���t���O 0 �ޯ����� 1 ؽı
# ���ӁI �����̏��O�����������ł���Ă���̂ŕύX���鎞�͂�����ύX
#================================================
sub create_you_data {
	my($you_datas, $user_line , $to_country, $daihyo_flag) = @_;

	# �������̏�������
	if (index($user_line, "<>country;") >= 0) { $user_line =~ s/<>(country;).*?<>/<>${1}$to_country<>/; }
	else { $user_line = "country;$to_country<>" . $user_line; }

	# �����E���[�f�[�^�̏�����
	if (index($user_line, "<>vote;") >= 0) { $user_line =~ s/<>(vote;).*?<>/<>$1<>/; }
	else { $user_line = "vote;<>" . $user_line; }

	# ������łȂ���Α�\�n���x�̏�������
	if ($w{world} != $#world_states-1) {
		for my $k (qw/war dom pro mil/) {
			my $k1 = $daihyo_flag == 0 ? "${k}_c_t" : "${k}_c"; # �ޯ����߁Eؽı�ŎQ�Ɛ悪�t
			my $k2 = $daihyo_flag == 0 ? "${k}_c" : "${k}_c_t" ; # �ޯ����߁Eؽı�ŎQ�Ɛ悪�t
			if (index($user_line, "<>$k1;") >= 0) { $user_line =~ s/<>($k1;).*?<>/<>$1$$you_datas{$k2}<>/; }
			else { $user_line = "$k1;$$you_datas{$k2}<>" . $user_line; }
			if (index($user_line, "<>$k2;") >= 0) { $user_line =~ s/<>($k2;).*?<>/<>${1}0<>/; }
			else { $user_line = "$k2;0<>" . $user_line; }
		}
	}

	return $user_line;
}

#================================================
# �ꊇ regist_you_data ���鎞�ɕK�v�ȕ����̍��Ȃǂ̃f�[�^��ǉ����ĕԂ�
# ��P������ get_you_datas �̖߂�l�������|�C���^
# ��Q������ user.cgi ��1�s��
#================================================
sub add_you_penalty_data {
	my($you_datas, $user_line) = @_;

	if (index($line, "<>shogo;") >= 0) { $line =~ s/<>(shogo;).*?<>/<>${1}$cs{name}[$$you_datas{country}](��)<>/; }
	else { $line = "shogo;$cs{name}[$$you_datas{country}](��)<>" . $line; }

	my $t = $time + 3600 * 24 * 3;
	if (index($line, "<>trick_time;") >= 0) { $line =~ s/<>(trick_time;).*?<>/<>${1}$t<>/; }
	else { $line = "trick_time;$t<>" . $line; }

	if (index($line, "<>shogo_t;") >= 0) { $line =~ s/<>(shogo_t;).*?<>/<>${1}$datas{shogo}<>/; }
	else { $line = "shogo_t;$datas{shogo}<>" . $line; }

	return $user_line;
}
=cut
#================================================
# 1�� (int(����/2)+1)�� ������ �̍��͏��ʂ�z��ŕԂ�
# �ّ��p�����ǂȂ񂩎g�������邩���H
#================================================
sub get_strong_ranking {
	# lstrcpy �Ƃ� memcpy �ŃK�b�Ƃ��悤�ɂ����ƊȒP�ɃR�s�y�ł����������Ǖ�����񂿂�
	my %tmp_cs;
	for my $i (1 .. $w{country}) {
		$tmp_cs{$i-1} = $cs{strong}[$i];
	}

	# ���͂ɒ��ڂ��č~���\�[�g
	my @strong_rank = ();
	foreach(sort {$tmp_cs{$b} <=> $tmp_cs{$a}} keys %tmp_cs){
		push(@strong_rank, [$_, $tmp_cs{$_}]);
	}

	my $_country = $w{country} - 1; # ����݂���������
	my $center = int($_country / 2);

	# top center bottom �̃_�u�萔�Ɛ擪�C���f�b�N�X�̎擾
	my @data = ([0,-1], [0,-1], [0,-1]);
	for my $i (0 .. $_country) {
		if ($strong_rank[$i][1] == $strong_rank[0][1]) {
			$data[0][0]++;
			$data[0][1] = $i if $data[0][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$center][1]) {
			$data[1][0]++;
			$data[1][1] = $i if $data[1][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$c][1]) {
			$data[2][0]++;
			$data[2][1] = $i if $data[2][1] < 0;
		}
	}

	# ���ꍑ�͂�����Ȃ�d�����Ȃ��悤�� rand �I��
	# �d�����Ȃ��l�������܂� while rand ���������������H
	my @result = ();
	for my $i (0 .. $#data) {
		my $j = int(rand($data[$i][0])+$data[$i][1]); # �_�u��̐擪�C���f�b�N�X����_�u�萔-1�̗���
		push (@result, @{splice(@strong_rank, $j, 1)}[0] + 1 ); # rand�I�����ꂽ������₩�甲�� 0 ������݂Ȃ̂� +1
		# �_�u�萔��擪�C���f�b�N�X�̏C��
		for my $k ($i+1 .. $#data) {
			if ($j > $data[$k][1]) {
				$data[$k][0]--;
			}
			elsif ($j < $data[$k][1]) {
				$data[$k][1]--;
			}
			else {
				$data[$k][0]--;
				$data[$k][1]--;
			}
		}
	}
	return @result;
}

=pod
# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0 ���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

sub player_migrate {
	my $type = shift;

	if ($type == &festival_type('kouhaku', 1)) { # �s��ՓV�ݒ�
	}
	elsif ($type == &festival_type('kouhaku', 0)) { # �s��ՓV����
	}
	elsif ($type == &festival_type('sangokusi', 1)) { # �O���u�ݒ�
	}
	elsif ($type == &festival_type('sangokusi', 0)) { # �O���u����
		require "./lib/move_player.cgi";
	}
#	elsif ($type == &festival_type('konran', 1) || $type == &festival_type('sessoku', 1)) { # �����ݒ�
	elsif ($type == &festival_type('konran', 1)) { # �����ݒ�
	}
#	elsif ($type == &festival_type('konran', 0) || $type == &festival_type('sessoku', 0)) { #��������
	elsif ($type == &festival_type('konran', 0)) { #��������
	}
	elsif ($type == &festival_type('sessoku', 1)) { # �ّ��J�n
#		&write_cs;
	}
	elsif ($type == &festival_type('sessoku', 0)) { # �ّ��I��
#		&cs_data_repair;
#		&write_cs;
	}
	elsif ($type == &festival_type('dokuritu', 1)) { # �Ɨ��ݒ�
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
	}
	elsif ($type == &festival_type('dokuritu', 0)) { # �Ɨ�����
		require "./lib/move_player.cgi";
		for my $i (1..$w{country}) {
			my @names = &get_country_members($i);
			for my $name (@names) {
				$name =~ tr/\x0D\x0A//d;
				if($name eq $m{name}){
					&move_player($m{name}, $i, 0);
					$m{country} = 0;
					&write_user;
				}
				my %you_datas = &get_you_datas($name);
				&move_player($name, $i, 0);
				&regist_you_data($name, 'country', 0);

				my($c1, $c2) = split /,/, $w{win_countries};
				if ($c1 eq $i || $c2 eq $i) {
					require './lib/shopping_offertory_box.cgi';
					if ($cs{ceo}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(7, $cs{ceo}[$you_datas{country}]) for (1..2);
					}
					my $n_id = unpack 'H*', $name;
					open my $fh, ">> $userdir/$n_id/ex_c.cgi";
					print $fh "fes_c<>1<>\n";
					close $fh;
					
					&send_item($name, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
			}
		}
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			$w{country} = $i;
			++$i;
		}
		close $fh;
		
		&cs_data_repair;# ???
	}
}
=cut
1;