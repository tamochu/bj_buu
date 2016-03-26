#!/usr/local/bin/perl --
package MahjongAi;
use strict;
use warnings;
use MahjongTehai;
use MahjongHo;
use MahjongPai;

sub new {
	my $clazz = shift;
	my $self = {
		Name => 'MahjongTestAI',
		Tehais => [],
		Hos => [],
		Points => [],
		Yama => undef,
		Round => -1,
		Continuous => -1,
		Turn => -1,
		Phase => -1,
		RoundSet => 0,
		LatestDrop => undef,
		DropPos => -1,
		Kyotaku => 0,
	};
	return bless $self, $clazz;
}

sub name {
	my $self = shift;
	return $self->{Name};
}

sub tehais {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Tehais}}[$i];
		}
		${$self->{Tehais}}[$i] = $x;
	}
	return $self->{Tehais};
}

sub hos {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Hos}}[$i];
		}
		${$self->{Hos}}[$i] = $x;
	}
	return $self->{Hos};
}

sub points {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Points}}[$i];
		}
		${$self->{Points}}[$i] = $x;
	}
	return $self->{Points};
}

sub yama {
	my $self = shift;
	if (@_) {
		$self->{Yama} = shift;
	}
	return $self->{Yama};
}

sub round {
	my $self = shift;
	if (@_) {
		$self->{Round} = shift;
	}
	return $self->{Round};
}

sub continuous {
	my $self = shift;
	if (@_) {
		$self->{Continuous} = shift;
	}
	return $self->{Continuous};
}

sub turn {
	my $self = shift;
	if (@_) {
		$self->{Turn} = shift;
	}
	return $self->{Turn};
}

sub phase {
	my $self = shift;
	if (@_) {
		$self->{Phase} = shift;
	}
	return $self->{Phase};
}

sub roundSets {
	my $self = shift;
	if (@_) {
		$self->{RoundSets} = shift;
	}
	return $self->{RoundSets};
}

sub latestDrop {
	my $self = shift;
	if (@_) {
		$self->{LatestDrop} = shift;
	}
	return $self->{LatestDrop};
}

sub dropPos {
	my $self = shift;
	if (@_) {
		$self->{DropPos} = shift;
	}
	return $self->{DropPos};
}

sub kyotaku {
	my $self = shift;
	if (@_) {
		$self->{Kyotaku} = shift;
	}
	return $self->{Kyotaku};
}

sub allShownHistogram {
	my $self = shift;
	my @hist = ();
	for my $i (0..33) {
		push @hist, 0;
	}
	if ($self->round() != -1) {
		for my $i (0..3) {
			my $tehaiStr = $self->tehais($i);
			my $tehai = MahjongTehai->new();
			$tehai->setAll($tehaiStr);
			my @th = $tehai->toHistogramAll();
			for my $j (0..33) {
				$hist[$j] += $th[$j];
			}
			
			my $hoStr = $self->hos($i);
			my $ho = MahjongHo->new();
			$ho->setAll($hoStr);
			for my $hp (@{$ho->ho()}) {
				$hist[MahjongPai::strToNum($hp->str())]++;
			}
		}
	}
	
	return @hist;
}

sub restHistogram {
	my $self = shift;
	my @hist = ();
	my @h = $self->allShownHistogram();
	for my $i (0..33) {
		push @hist, (4 - $h[$i]);
	}
	
	return @hist;
}

sub getMyTehai {
	my $self = shift;
	my $tehai = MahjongTehai->new();
	my $tehaiStr = $self->tehais(0);
	$tehai->setAll($tehaiStr);
	return $tehai;
}

sub getMyHo {
	my $self = shift;
	my $hoStr = $self->hos(0);
	my $ho = MahjongHo->new();
	$ho->setAll($hoStr);
	return $ho;
}


sub playIndex {
	my $self = shift;
	my $tehai = $self->getMyTehai();
	my @hist = $tehai->toHistogram();
	my @shantenIndex = ();
	my @restHist = $self->restHistogram();
	my @restIndex = ();
	
	for my $i (0..$#{$self->getMyTehai()->tehai()}) {
		my $tehai = $self->getMyTehai();
		$tehai->drop($i);
		push @shantenIndex, $tehai->calcShanten();
		my @yukohais = $tehai->getYuko();
		my $yukoRest = 0;
		for my $yuko (@yukohais) {
			$yukoRest += $restHist[MahjongPai::strToNum($yuko->str())];
		}
		push @restIndex, $yukoRest;
	}
	
	my $minShanten = 13;
	for my $shanten (@shantenIndex) {
		if ($shanten < $minShanten) {
			$minShanten = $shanten;
		}
	}
	
	my $index = -1;
	my $maxYuko = -1;
	for my $i (0..$#shantenIndex) {
		if ($shantenIndex[$i] == $minShanten) {
			if ($maxYuko < $restIndex[$i]) {
				$index = $i;
				$maxYuko = $restIndex[$i];
			}
		}
	}
	
	return $index;
}

sub selectEat {
	my $self = shift;
	return -3;
}

sub isReach {
	my $self = shift;
	return ($self->getMyHo()->reachAt() == -1 && $self->getMyTehai()->calcShanten() == 0);
}

sub isRon {
	my $self = shift;
	my $tehai = $self->getMyTehai();
	$tehai->add($self->latestDrop());
	return ($tehai->calcShanten() == -1);
}

sub isTsumo {
	my $self = shift;
	return ($self->getMyTehai()->calcShanten() == -1);
}

sub getKan {
	my $self = shift;
=pod
	my @hist = $self->getMyTehai()->toHistogram();
	for my $i (0..33) {
		if ($hist[$i] == 4) {
			my $pai = MahjongPai->new();
			$pai->str(MahjongPai::numToStr($i));
			return $pai;
		}
	}
=cut
	return undef;
}


sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Name' => $self->name(),
	);
	return {%self_hash};
}
1;