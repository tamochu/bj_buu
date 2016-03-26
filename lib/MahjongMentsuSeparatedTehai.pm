#!/usr/local/bin/perl --
package MahjongMentsuSeparatedTehai;
use strict;
use warnings;
use MahjongPai;
use MahjongNaki;
use MahjongYaku;
use MahjongTehai;

sub new {
	my $clazz = shift;
	my $self = {
		Mentsu => [],
		Janto => MahjongPai->new(),
		FinishShape => 0,
		Tehai => MahjongTehai->new(),
	};
	return bless $self, $clazz;
}

sub clone {
	my $self = shift;
	my $clone = MahjongMentsuSeparatedTehai->new();
	for my $m (@{$self->mentsu()}) {
		push @{$clone->mentsu()}, $m->clone();
	}
	$clone->janto()->str($self->janto()->str());
	$clone->finishShape($self->finishShape());
	$clone->tehai($self->tehai());
	return $clone;
}

sub mentsu {
	my $self = shift;
	return $self->{Mentsu};
}

sub janto {
	my $self = shift;
	return $self->{Janto};
}

sub finishShape {
	my $self = shift;
	if (@_) {
		$self->{FinishShape} = shift;
	}
	return $self->{FinishShape};
}

sub tehai {
	my $self = shift;
	if (@_) {
		$self->{Tehai} = shift;
	}
	return $self->{Tehai};
}

sub addMentsu {
	my $self = shift;
	my $naki = shift;
	push @{$self->{Mentsu}}, $naki;
}

sub setJanto {
	my $self = shift;
	my $str = shift;
	$self->{Janto}->str($str);
}

sub setTehai {
	my $self = shift;
	my $tehai = shift;
	$self->{Tehai} = $tehai;
	for my $naki (@{$tehai->naki()}) {
		$self->addMentsu($naki);
	}
}

sub countShuntsu {
	my $self = shift;
	my $count = 0;
	for my $mentsu (@{$self->mentsu()}) {
		if ($mentsu->isShuntsu()) {
			$count++;
		}
	}
	return $count;
}

sub countKotsu {
	my $self = shift;
	my $count = 0;
	for my $mentsu (@{$self->mentsu()}) {
		if ($mentsu->isKotsu()) {
			$count++;
		}
	}
	return $count;
}

sub is4Mentsu {
	my $self = shift;
	return (($self->countShuntsu() + $self->countKotsu()) == 4);
}

sub countAnko {
	my $self = shift;
	my $count = 0;
	for my $mentsu (@{$self->mentsu()}) {
		if ($mentsu->isAnko() || $mentsu->isAnkan()) {
			$count++;
		}
	}
	return $count;
}

sub countKan {
	my $self = shift;
	my $count = 0;
	for my $mentsu (@{$self->mentsu()}) {
		if ($mentsu->isMinkan() || $mentsu->isAnkan()) {
			$count++;
		}
	}
	return $count;
}

sub isMenzen {
	my $self = shift;
	my $count = 0;
	for my $mentsu (@{$self->mentsu()}) {
		if ($mentsu->kanFlag() != -1 && $mentsu->kanFlag() != 2) {
			return 0;
		}
	}
	return 1;
}

sub calcHu {
	my $self = shift;
	my $ba = shift;
	my $kaze = shift;
	
	my $hu = 20;
	if ($self->janto()->str() eq $ba) {
		$hu += 2;
	}
	if ($self->janto()->str() eq $kaze) {
		$hu += 2;
	}
	if ($self->finishShape() == 2 || $self->finishShape() == 3 || $self->finishShape() == 4) {
		$hu += 2;
	}
	
	for my $mentsu (@{$self->mentsu()}) {
		my $addHu = 0;
		if ($mentsu->isPon()) {
			$addHu = 2;
		} elsif ($mentsu->isAnko()) {
			if ($self->finishShape() == 1 && $mentsu->pai1()->str() eq $self->tehai()->lastAddPai()->str()) {
				$addHu = 2;
			} else {
				$addHu = 4;
			}
		} elsif ($mentsu->isMinkan()) {
			$addHu = 8;
		} elsif ($mentsu->isAnkan()) {
			$addHu = 16;
		}
		if ($mentsu->isYaochu()) {
			$addHu *= 2;
		}
		$hu += $addHu;
	}
	
	if ($hu % 10 > 0) {
		$hu += 10 - ($hu % 10);
	}
	return $hu;
}

sub calcFan {
	my $self = shift;
	my $ba = shift;
	my $kaze = shift;
	
	my $fan = 0;
	my @yaku_arr = ();
	my @yaku_list = ();
	
	for my $rule (&MahjongYaku::getRules) {
		my $yaku = $rule->yaku->($self, $ba, $kaze);
		if ($yaku->fan() > 0) {
			push @yaku_list, $yaku;
		}
	}
	
	my $is_yakuman = 0;
	for my $yaku (@yaku_list) {
		if ($yaku->fan() >= 13) {
			$is_yakuman = 1;
		}
	}
	
	for my $yaku (@yaku_list) {
		if (!$is_yakuman || $yaku->fan() >= 13) {
			$fan += $yaku->fan();
			push @yaku_arr, $yaku->yaku();
		}
	}
	
	if ($fan > 0) {
		my $dora_num = 0;
		my @hist = $self->tehai()->toHistogramAll();
		for my $dora_h (@{$self->tehai()->doras()}) {
			my $dora = MahjongPai::getDoraNextStr($dora_h);
			$dora_num += $hist[MahjongPai::strToNum($dora)];
		}
		if ($dora_num > 0) {
			$fan += $dora_num;
			push @yaku_arr, 'ƒhƒ‰' . $dora_num;
		}
	}
	
	my $yaku_str = join ',', @yaku_arr;
	
	return ($fan, $yaku_str);
}

sub calcPoint {
	my $self = shift;
	my $ba = shift;
	my $kaze = shift;
	
	my $hu = $self->calcHu($ba, $kaze);
	my ($fan, $yaku) = $self->calcFan($ba, $kaze);
	return &calcPointFromHuAndFan($self->tehai()->tsumoFlag(), $kaze eq 'z1', $hu, $fan, $yaku);
}

sub calcPointFromHuAndFan {
	my $tsumoFlag = shift;
	my $oyaFlag = shift;
	my $hu = shift;
	my $fan = shift;
	my $yaku = shift;
	
	my $hu_fan_str = $hu . '•„' . $fan . 'ãÊ';
	if ($fan == 0) {
		return (0, 0, '–ð–³‚µ', '');
	}
	my $base_point = $hu * 2 * 2;
	for my $i (1..$fan) {
		$base_point *= 2;
	}
	
	if ($base_point >= 2000) {
		if ($fan >= 13) {
			my $yakuman_doubled = int($fan / 13);
			$base_point = 8000 * $yakuman_doubled;
			if ($yakuman_doubled == 1) {
				$hu_fan_str .= '–ð–ž';
			} elsif ($yakuman_doubled == 2) {
				$hu_fan_str .= 'ƒ_ƒuƒ‹–ð–ž';
			} elsif ($yakuman_doubled == 3) {
				$hu_fan_str .= 'ƒgƒŠƒvƒ‹–ð–ž';
			} else {
				$hu_fan_str .= $yakuman_doubled . '”{–ð–ž';
			}
		} elsif ($fan >= 11) {
			$base_point = 6000;
			$hu_fan_str .= 'ŽO”{–ž';
		} elsif ($fan >= 8) {
			$base_point = 4000;
			$hu_fan_str .= '”{–ž';
		} elsif ($fan >= 6) {
			$base_point = 3000;
			$hu_fan_str .= '’µ–ž';
		} else {
			$base_point = 2000;
			$hu_fan_str .= '–žŠÑ';
		}
	}
	if ($tsumoFlag) {
		my $oya_point = $base_point * 2;
		if ($oya_point % 100 > 0) {
			$oya_point = $oya_point + 100 - ($oya_point % 100);
		}
		my $ko_point = $base_point;
		if ($ko_point % 100 > 0) {
			$ko_point = $ko_point + 100 - ($ko_point % 100);
		}
		if ($oyaFlag) {
			return ($oya_point, $oya_point, $yaku, $hu_fan_str, ($fan >= 13));
		} else {
			return ($ko_point, $oya_point, $yaku, $hu_fan_str, ($fan >= 13));
		}
	} else {
		my $ron_point = $base_point;
		if ($oyaFlag) {
			$ron_point *= 6;
		} else {
			$ron_point *= 4;
		}
		if ($ron_point % 100 > 0) {
			$ron_point = $ron_point + 100 - ($ron_point % 100);
		}
		return (0, $ron_point, $yaku, $hu_fan_str, ($fan >= 13));
	}
}
1;