#!/usr/local/bin/perl --
package MahjongTehai;
use strict;
use warnings;
use MahjongPai;
use MahjongNaki;
use MahjongMentsuSeparatedTehai;

sub new {
	my $clazz = shift;
	my $self = {
		Tehai => [],
		Naki => [],
		Position => 0,
		Mine => 1,
		TsumoFlag => 0,
		ChankanFlag => 0,
		TenhoFlag => 0,
		ChihoFlag => 0,
		ReachFlag => 0,
		DoubleReachFlag => 0,
		IppatsuFlag => 0,
		RinshanFlag => 0,
		HaiteiFlag => 0,
		Doras => [],
		AgariHai => MahjongPai->new(),
		LastAddPai => MahjongPai->new(),
	};
	return bless $self, $clazz;
}

sub clone {
	my $self = shift;
	my $clone = MahjongTehai->new();
	$clone->setAll($self->toString());
	return $clone;
}

sub tehai {
	my $self = shift;
	return $self->{Tehai};
}

sub naki {
	my $self = shift;
	return $self->{Naki};
}

sub position {
	my $self = shift;
	if (@_) {
		$self->{Position} = shift;
	}
	return $self->{Position};
}
sub mine {
	my $self = shift;
	if (@_) {
		$self->{Mine} = shift;
	}
	return $self->{Mine};
}
sub tsumoFlag {
	my $self = shift;
	if (@_) {
		$self->{TsumoFlag} = shift;
	}
	return $self->{TsumoFlag};
}
sub chankanFlag {
	my $self = shift;
	if (@_) {
		$self->{ChankanFlag} = shift;
	}
	return $self->{ChankanFlag};
}
sub tenhoFlag {
	my $self = shift;
	if (@_) {
		$self->{TenhoFlag} = shift;
	}
	return $self->{TenhoFlag};
}
sub chihoFlag {
	my $self = shift;
	if (@_) {
		$self->{ChihoFlag} = shift;
	}
	return $self->{ChihoFlag};
}
sub reachFlag {
	my $self = shift;
	if (@_) {
		$self->{ReachFlag} = shift;
	}
	return $self->{ReachFlag};
}
sub doubleReachFlag {
	my $self = shift;
	if (@_) {
		$self->{DoubleReachFlag} = shift;
	}
	return $self->{DoubleReachFlag};
}
sub ippatsuFlag {
	my $self = shift;
	if (@_) {
		$self->{IppatsuFlag} = shift;
	}
	return $self->{IppatsuFlag};
}
sub rinshanFlag {
	my $self = shift;
	if (@_) {
		$self->{RinshanFlag} = shift;
	}
	return $self->{RinshanFlag};
}
sub haiteiFlag {
	my $self = shift;
	if (@_) {
		$self->{HaiteiFlag} = shift;
	}
	return $self->{HaiteiFlag};
}
sub doras {
	my $self = shift;
	return $self->{Doras};
}
sub setDoras {
	my $self = shift;
	my @doras = @_;
	@{$self->doras()} = ();
	for my $dora (@doras) {
		push @{$self->doras()}, $dora;
	}
}
sub agariHai {
	my $self = shift;
	return $self->{AgariHai};
}
sub lastAddPai {
	my $self = shift;
	return $self->{LastAddPai};
}

sub setTehai {
	my $self = shift;
	my $str = shift;
	my @split_str = split //, $str;
	my $i = 0;
	while ($i < @split_str) {
		if ($split_str[$i] eq ' ') {
			last;
		}
		my $pai = MahjongPai->new();
		$pai->str($split_str[$i] . $split_str[$i+1]);
		$self->add($pai);
		$i += 2;
	}
}

sub setAll {
	my $self = shift;
	my $str = shift;
	my @split_str = split / /, $str;
	my $first = 1;
	for my $ss (@split_str) {
		if ($first) {
			$self->setTehai($ss);
			$first = 0;
		} else {
			my $huro = MahjongNaki->new();
			$huro->setPai($ss);
			push @{$self->naki()}, $huro;
		}
	}
}

sub add {
	my $self = shift;
	my $pai = shift;
	push @{$self->tehai()}, $pai;
	$self->lastAddPai()->str($pai->str());
}

sub chi {
	my $self = shift;
	my $pai = shift;
	my $type = shift;
	my $pai_num = $pai->getNum();
	my $pai1_str = $pai->getType() . ($pai_num - 1);
	my $pai2_str = $pai->getType() . ($pai_num + 1);
	if ($type == -1) {
		$pai1_str = $pai->getType() . ($pai_num - 2);
		$pai2_str = $pai->getType() . ($pai_num - 1);
	} elsif ($type == 1) {
		$pai1_str = $pai->getType() . ($pai_num + 1);
		$pai2_str = $pai->getType() . ($pai_num + 2);
	}
	my @hist = $self->toHistogram();
	if ($hist[MahjongPai::strToNum($pai1_str)] > 0 && $hist[MahjongPai::strToNum($pai2_str)] > 0) {
		my $t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai1_str) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai2_str) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		my $naki = MahjongNaki->new();
		$naki->setPai('-' . $pai->str() . $pai1_str . $pai2_str);
		push @{$self->naki()}, $naki;
		
		return 1;
	}
	return 0;
}

sub pon {
	my $self = shift;
	my $pai = shift;
	my $from = shift;
	my @hist = $self->toHistogram();
	if ($hist[MahjongPai::strToNum($pai->str())] >= 2) {
		my $t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		my $naki = MahjongNaki->new();
		my $naki_str = $pai->str() . $pai->str() . $pai->str();
		if ($from == 3) {
			$naki_str = '-' . $naki_str;
		} elsif ($from == 2) {
			$naki_str = '-' . $naki_str . '-';
		} elsif ($from == 1) {
			$naki_str = $naki_str . '-';
		}
		$naki->setPai($naki_str);
		push @{$self->naki()}, $naki;
		
		return 1;
	}
	return 0;
}

sub minkan {
	my $self = shift;
	my $pai = shift;
	my $from = shift;
	my @hist = $self->toHistogram();
	if ($hist[MahjongPai::strToNum($pai->str())] >= 3) {
		my $t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		my $naki = MahjongNaki->new();
		my $naki_str = $pai->str() . $pai->str() . $pai->str() . $pai->str();
		if ($from == 3) {
			$naki_str = '-' . $naki_str;
		} elsif ($from == 2) {
			$naki_str = '-' . $naki_str . '-';
		} elsif ($from == 1) {
			$naki_str = $naki_str . '-';
		}
		$naki->setPai($naki_str);
		push @{$self->naki()}, $naki;
		
		return 1;
	}
	return 0;
}

sub ankan {
	my $self = shift;
	my $pai = shift;
	my @hist = $self->toHistogram();
	if ($hist[MahjongPai::strToNum($pai->str())] == 4) {
		my $t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		$t_i = 0;
		for my $t_pai (@{$self->tehai()}) {
			if ($t_pai->str() eq $pai->str()) {
				splice @{$self->tehai()}, $t_i, 1;
				last;
			}
			$t_i++;
		}
		my $naki = MahjongNaki->new();
		my $naki_str = $pai->str() . $pai->str() . $pai->str() . $pai->str();
		$naki->setPai($naki_str);
		push @{$self->naki()}, $naki;
		
		return 1;
	}
	return 0;
}

sub kakan {
	my $self = shift;
	my $pai = shift;
	
	my $naki_index = -1;
	my $i = 0;
	for my $naki (@{$self->naki()}) {
		if ($naki->pai1()->str() eq $pai->str() && $naki->isPon()) {
			$naki_index = $i;
			last;
		}
		$i++;
	}
	
	my $tehai_index = -1;
	$i = 0;
	for my $tehai (@{$self->tehai()}) {
		if ($tehai->str() eq $pai->str()) {
			$tehai_index = $i;
			last;
		}
		$i++;
	}
	
	if ($naki_index != -1 && $tehai_index != -1) {
		splice @{$self->tehai()}, $tehai_index, 1;
		my @naki = @{$self->naki()};
		$naki[$naki_index]->kanFlag(1);
		@{$self->naki()} = @naki;
		return 1;
	}
	return 0;
}

sub getKanable  {
	my $self = shift;
	my @kanable = ();
	my @hist = $self->toHistogram();
	for my $i (0..33) {
		if ($hist[$i] == 4) {
			my $pai = MahjongPai->new();
			$pai->str(MahjongPai::numToStr($i));
			push @kanable, $pai;
		}
	}
	for my $naki (@{$self->naki()}) {
		if ($naki->isPon() && $hist[MahjongPai::strToNum($naki->pai1()->str())] == 1) {
			my $pai = MahjongPai->new();
			$pai->str($naki->pai1()->str());
			push @kanable, $pai;
		}
	}
	return @kanable;
}

sub drop {
	my $self = shift;
	my $index = shift;
	if (!$self->isKiriban()) {
		return undef;
	}
	if ($index >= 0 && $index < @{$self->tehai()}) {
		my $pai = splice @{$self->tehai()}, $index, 1;
		
		$self->sortTehai();
		
		return $pai;
	}
	return undef;
}

sub toString {
	my $self = shift;
	my $force = shift;
	my $ret_str = '';
	for my $tehai (@{$self->tehai()}) {
		if ($force || $self->mine()) {
			$ret_str .= $tehai->str();
		}
	}
	for my $naki (@{$self->naki()}) {
		$ret_str .= ' ';
		$ret_str .= $naki->toString();
	}
	return $ret_str;
}

sub toHistogram {
	my $self = shift;
	my @hist = ();
	for my $i (0..33) {
		push @hist, 0;
	}
	for my $tehai (@{$self->tehai()}) {
		if (MahjongPai::strToNum($tehai->str()) != -1) {
			$hist[MahjongPai::strToNum($tehai->str())]++;
		}
	}
	return @hist;
}

sub toHistogramAll {
	my $self = shift;
	my @hist = ();
	for my $i (0..33) {
		push @hist, 0;
	}
	for my $tehai (@{$self->tehai()}) {
		if (MahjongPai::strToNum($tehai->str()) != -1) {
			$hist[MahjongPai::strToNum($tehai->str())]++;
		}
	}
	for my $naki (@{$self->naki()}) {
		$hist[MahjongPai::strToNum($naki->pai1()->str())]++;
		$hist[MahjongPai::strToNum($naki->pai2()->str())]++;
		$hist[MahjongPai::strToNum($naki->paiNaki()->str())]++;
		if ($naki->kanFlag() > 0) {
			$hist[MahjongPai::strToNum($naki->paiNaki()->str())]++;
		}
	}
	return @hist;
}

sub sortTehai {
	my $self = shift;
	@{$self->tehai()} = sort { MahjongPai::strToNum($a->str()) <=> MahjongPai::strToNum($b->str()) } @{$self->tehai()};
}

sub calcShanten {
	my $self = shift;
	my $c = $self->calcChitoitsuShanten();
	my $k = $self->calcKokushiShanten();
	my $b = $self->calcBaseShanten();
	my $min = 13;
	if ($c < $min) {
		$min = $c;
	}
	if ($k < $min) {
		$min = $k;
	}
	if ($b < $min) {
		$min = $b;
	}
	
	return $min;
}

sub calcChitoitsuShanten {
	my $self = shift;
	if (@{$self->naki()} > 0) {
		return 13;
	}
	my @hist = $self->toHistogram();
	my $toitsu = 0;
	my $seed = 0;
	for my $i (0..33) {
		if ($hist[$i] > 0) {
			$seed++;
		}
		if ($hist[$i] >= 2) {
			$toitsu++;
		}
	}
	if ($seed > 7) {
		$seed = 7;
	}
	return (13 - $toitsu - $seed);
}

sub calcKokushiShanten {
	my $self = shift;
	if (@{$self->naki()} > 0) {
		return 13;
	}
	my @hist = $self->toHistogram();
	my $yaochu = 0;
	my $janto = 0;
	my @yaochu_index = (0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33);
	for my $i (@yaochu_index) {
		if ($hist[$i] > 0) {
			$yaochu++;
		}
		if ($janto == 0 && $hist[$i] >= 2) {
			$janto++;
		}
	}
	
	return (13 - $yaochu - $janto);
}

sub calcBaseShanten {
	my $self = shift;
	my @hist = $self->toHistogram();
	
	for my $i (0..33) {
		if ($hist[$i] == 1) {
			if ($i >= 27) {
				$hist[$i] = 0;
			} else {
				my $num = ($i % 9) + 1;
				if ($num == 1) {
					if ($hist[$i + 1] + $hist[$i + 2] == 0) {
						$hist[$i] = 0;
					}
				} elsif ($num == 9) {
					if ($hist[$i - 2] + $hist[$i - 1] == 0) {
						$hist[$i] = 0;
					}
				} elsif ($num == 2) {
					if ($hist[$i - 1] + $hist[$i + 1] + $hist[$i + 2] == 0) {
						$hist[$i] = 0;
					}
				} elsif ($num == 8) {
					if ($hist[$i - 2] + $hist[$i - 1] + $hist[$i + 1] == 0) {
						$hist[$i] = 0;
					}
				} else {
					if ($hist[$i - 2] + $hist[$i - 1] + $hist[$i + 1] + $hist[$i + 2] == 0) {
						$hist[$i] = 0;
					}
				}
			}
		}
	}
	
	my $naki_length = @{$self->naki()};
	
	my $ch = [map {$_} @hist];
	my $min = &mentsuCalc(0, $naki_length, @$ch);
	for my $i (0..33) {
		if ($hist[$i] >= 2) {
			my $chj = [map {$_} @hist];
			$$chj[$i] -= 2;
			my $js = &mentsuCalc(0, $naki_length, @$chj) - 1;
			if ($min > $js) {
				$min = $js;
			}
		}
	}
	return $min;
}

sub tatsuCalc {
	my $index = shift;
	my @h = @_;
	while ($index < 34) {
		if ($h[$index] != 0) {
			last;
		}
		$index++;
	}
	if ($index >= 34) {
		return 0;
	}
	
	# 対子
	if ($h[$index] >= 2) {
		$h[$index] -= 2;
		return (&tatsuCalc($index, @h) + 1);
	}
	
	# 順子
	if ($index >= 27) {
		return &tatsuCalc($index + 1, @h);
	}
	my $num = ($index % 9) + 1;
	# 辺張、両面
	if ($num < 9) {
		if ($h[$index + 1] > 0) {
			$h[$index]--;
			$h[$index + 1]--;
			return (&tatsuCalc($index, @h) + 1);
		}
	}
	# 嵌張
	if ($num < 8) {
		if ($h[$index + 2] > 0) {
			$h[$index]--;
			$h[$index + 2]--;
			return (&tatsuCalc($index, @h) + 1);
		}
	}
	return &tatsuCalc($index + 1, @h);
}

sub mentsuCalc {
	my $index = shift;
	my $mentsu = shift;
	my @h = @_;
	while ($index < 34) {
		if ($h[$index] != 0) {
			last;
		}
		$index++;
	}
	if ($index >= 34) {
		my $tatsu = &tatsuCalc(0, @h);
		if ($mentsu + $tatsu > 4) {
			$tatsu = 4 - $mentsu;
		}
		return (8 - $mentsu * 2 - $tatsu);
	}
	
	if ($index >= 27) {
		if ($h[$index] >= 3) {
			$h[$index] -= 3;
			return &mentsuCalc($index + 1, $mentsu + 1, @h);
		}
	} else {
		my $num = ($index % 9) + 1;
		my $skipClone = [map {$_} @h];
		my $shanten = &mentsuCalc($index + 1, $mentsu, @$skipClone);
		if ($num < 8 && $h[$index + 1] > 0 && $h[$index + 2] > 0) {
			# 順子が取れる場合
			if ($h[$index] >= 3) {
				# さらに刻子も取れる場合
				my $shuntsuClone = [map {$_} @h];
				$$shuntsuClone[$index]--;
				$$shuntsuClone[$index + 1]--;
				$$shuntsuClone[$index + 2]--;
				my $shuntsuShanten = &mentsuCalc($index, $mentsu + 1, @$shuntsuClone);
				
				my $kotsuClone = [map {$_} @h];
				$$kotsuClone[$index] -= 3;
				my $kotsuShanten = &mentsuCalc($index, $mentsu + 1, @$kotsuClone);
				
				if ($shuntsuShanten < $shanten) {
					$shanten = $shuntsuShanten;
				}
				if ($kotsuShanten < $shanten) {
					$shanten = $kotsuShanten;
				}
			} else {
				$h[$index]--;
				$h[$index + 1]--;
				$h[$index + 2]--;
				my $shuntsuShanten = &mentsuCalc($index, $mentsu + 1, @h);
				if ($shuntsuShanten < $shanten) {
					$shanten = $shuntsuShanten;
				}
			}
		} else {
			if ($h[$index] >= 3) {
				$h[$index] -= 3;
				my $kotsuShanten = &mentsuCalc($index, $mentsu + 1, @h);
				if ($kotsuShanten < $shanten) {
					$shanten = $kotsuShanten;
				}
			}
		}
		return $shanten;
	}
	return &mentsuCalc($index + 1, $mentsu, @h);
}

sub getMachi {
	my $self = shift;
	if ($self->calcShanten() == 0) {
		return $self->getYuko();
	}
	return ();
}

sub getYuko {
	my $self = shift;
	if ($self->isTsumoban()) {
		my @yukohais = ();
		my $nowShanten = $self->calcShanten();
		for my $i (0..33) {
			my $pai = MahjongPai->new();
			$pai->str(MahjongPai::numToStr($i));
			my $clone = $self->clone();
			$clone->add($pai);
			if ($clone->calcShanten() == $nowShanten - 1) {
				push @yukohais, $pai;
			}
		}
		return @yukohais;
	}
	return ();
}

sub isTsumoban {
	my $self = shift;
	return (@{$self->tehai()} % 3 == 1);
}

sub isKiriban {
	my $self = shift;
	return (@{$self->tehai()} % 3 == 2);
}

sub isShoupai {
	my $self = shift;
	return (@{$self->tehai()} % 3 == 0);
}

sub calcPoint {
	my $self = shift;
	my $ba = shift;
	my $kaze = shift;
	
	if ($self->calcShanten() == -1) {
		if ($self->calcChitoitsuShanten() == -1 && !$self->isRyanpeikou() ) {
			my $mst = MahjongMentsuSeparatedTehai->new();
			$mst->setTehai($self);
			my ($fan, $yaku) = $mst->calcFan($ba, $kaze);
			return MahjongMentsuSeparatedTehai::calcPointFromHuAndFan($self->tsumoFlag(), $kaze eq 'z1', 25, 2 + $fan, '七対子,' . $yaku);
		} elsif ($self->calcKokushiShanten() == -1) {
			return MahjongMentsuSeparatedTehai::calcPointFromHuAndFan($self->tsumoFlag(), $kaze eq 'z1', 20, 13, '国士無双');
		} else {
			my @max_point = (0, 0, 'チョンボ', '');
			my @sml = $self->splitMentsu();
			for my $sm (@sml) {
				my @point = $sm->calcPoint($ba, $kaze);
				if ($max_point[1] < $point[1]) {
					@max_point = @point;
				}
			}
			return @max_point;
		}
	}
	return (0, 0, 'チョンボ', '');
}

sub splitMentsu {
	my $self = shift;
	my @list = ();
	my @hist = $self->toHistogram();
	my $split_tehai = MahjongMentsuSeparatedTehai->new();
	$split_tehai->setTehai($self);
	
	for my $i (0..33) {
		if ($hist[$i] >= 2) {
			my $clone_h = [map {$_} @hist];
			${$clone_h}[$i] -= 2;
			$split_tehai->setJanto(MahjongPai::numToStr($i));
			@list = &removeMentsu($split_tehai, $clone_h, @list);
		}
	}

	@list = &machiSet($self->lastAddPai(), @list);
	return @list;
}

sub removeMentsu {
	my $s = shift;
	my $h_ref = shift;
	my @h = @{$h_ref};
	my @l = @_;
	
	my $rest_find = 0;
	for my $i (0..33) {
		my $removed = 0;
		if ($h[$i] > 0) {
			$rest_find = 1;
			my $num = ($i % 9) + 1;
			if ($i < 27) {
				if ($num < 8) {
					if ($h[$i] > 0 && $h[$i + 1] > 0 && $h[$i + 2] > 0) {
						my $shuntsuH = [map {$_} @h];
						my $shuntsuS = $s->clone();
						${$shuntsuH}[$i]--;
						${$shuntsuH}[$i + 1]--;
						${$shuntsuH}[$i + 2]--;
						my $shuntsu = MahjongNaki->new();
						$shuntsu->setMentsu(MahjongPai::numToStr($i) . MahjongPai::numToStr($i + 1) . MahjongPai::numToStr($i + 2));
						$shuntsuS->addMentsu($shuntsu);
						@l = &removeMentsu($shuntsuS, $shuntsuH, @l);
						$removed = 1;
					}
				}
			}
			if ($h[$i] >= 3) {
				my $kotsuH = [map {$_} @h];
				my $kotsuS = $s->clone();
				${$kotsuH}[$i] -= 3;
				my $kotsu = MahjongNaki->new();
				$kotsu->setMentsu(MahjongPai::numToStr($i) . MahjongPai::numToStr($i) . MahjongPai::numToStr($i));
				$kotsuS->addMentsu($kotsu);
				@l = &removeMentsu($kotsuS, $kotsuH, @l);
				$removed = 1;
			}
		}
		if ($removed) {
			last;
		}
	}
	if (!$rest_find) {
		push @l, $s;
	}
	return @l;
}

sub machiSet {
	my $finish_pai = shift;
	my @list = @_;
	
	my @machi_list = ();
	for my $s (@list) {
		# 両面
		for my $mentsu (@{$s->mentsu()}) {
			if ($mentsu->kanFlag() == -1 && $mentsu->isShuntsu()) {
				if ($mentsu->paiNaki()->str() eq $finish_pai->str() && $finish_pai->getNum() != 7) {
					my $clone = $s->clone();
					$clone->finishShape(0);
					push @machi_list, $clone;
				} elsif ($mentsu->pai2()->str() eq $finish_pai->str() && $finish_pai->getNum() != 3) {
					my $clone = $s->clone();
					$clone->finishShape(0);
					push @machi_list, $clone;
				}
			}
		}
		# シャボ
		for my $mentsu (@{$s->mentsu()}) {
			if ($mentsu->kanFlag() == -1 && $mentsu->isKotsu()) {
				if ($mentsu->paiNaki()->str() eq $finish_pai->str()) {
					my $clone = $s->clone();
					$clone->finishShape(1);
					push @machi_list, $clone;
				}
			}
		}
		# 嵌張
		for my $mentsu (@{$s->mentsu()}) {
			if ($mentsu->kanFlag() == -1 && $mentsu->isShuntsu()) {
				if ($mentsu->pai1()->str() eq $finish_pai->str()) {
					my $clone = $s->clone();
					$clone->finishShape(2);
					push @machi_list, $clone;
				}
			}
		}
		# 辺張
		for my $mentsu (@{$s->mentsu()}) {
			if ($mentsu->kanFlag() == -1 && $mentsu->isShuntsu()) {
				if ($mentsu->paiNaki()->str() eq $finish_pai->str() && $finish_pai->getNum() == 7) {
					my $clone = $s->clone();
					$clone->finishShape(3);
					push @machi_list, $clone;
				} elsif ($mentsu->pai2()->str() eq $finish_pai->str() && $finish_pai->getNum() == 3) {
					my $clone = $s->clone();
					$clone->finishShape(3);
					push @machi_list, $clone;
				}
			}
		}
		if ($s->janto()->str() eq $finish_pai->str()) {
			my $clone = $s->clone();
			$clone->finishShape(4);
			push @machi_list, $clone;
		}
	}
	return @machi_list;
}

sub isRyanpeikou {
	my $self = shift;
	if (@{$self->naki()} == 0) {
		my @hist = $self->toHistogram();
		my $peikou = 0;
		my $janto = 0;
		for my $j (0..1) {
			for my $i (0..6) {
				if ($hist[$i] >= 2 && $hist[$i + 1] >= 2 && $hist[$i + 2] >= 2) {
					$hist[$i] -= 2;
					$hist[$i + 1] -= 2;
					$hist[$i + 2] -= 2;
					$peikou++;
				}
			}
			for my $i (9..15) {
				if ($hist[$i] >= 2 && $hist[$i + 1] >= 2 && $hist[$i + 2] >= 2) {
					$hist[$i] -= 2;
					$hist[$i + 1] -= 2;
					$hist[$i + 2] -= 2;
					$peikou++;
				}
			}
			for my $i (18..24) {
				if ($hist[$i] >= 2 && $hist[$i + 1] >= 2 && $hist[$i + 2] >= 2) {
					$hist[$i] -= 2;
					$hist[$i + 1] -= 2;
					$hist[$i + 2] -= 2;
					$peikou++;
				}
			}
		}
		for my $i (0..33) {
			if ($hist[$i] >= 2) {
				$janto = 1;
			}
		}
		if ($peikou == 2 && $janto) {
			return 1;
		}
	}
	return 0;
}

sub hide {
	my $self = shift;
	my $ret = $self->clone();
	for my $i (0..$#{$ret->tehai()}) {
		${$ret->tehai()}[$i]->str('u0');
	}
	return $ret;
}

sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Tehai' => $self->toString(),
	);
	return {%self_hash};
}

1;