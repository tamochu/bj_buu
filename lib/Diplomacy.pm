#!/usr/local/bin/perl --
package Diplomacy;
use strict;
use warnings;
use DiplomacyCountry;
use DiplomacyOrder;

sub new {
	my $clazz = shift;
	my $self = {
		Year => 2000,
		Turn => 0,# 1t–½ 2t“P 3H–½ 4H“P 5H’²
		DipMap => null,
		Countries => [],
		FailProhibit => [],
		FailedOrders => [],
		LoseOrders => [],
	};
	return bless $self, $clazz;
}

sub year {
	my $self = shift;
	if (@_) {
		$self->{Year} = shift;
	}
	return $self->{Year};
}

sub turn {
	my $self = shift;
	if (@_) {
		$self->{Turn} = shift;
	}
	return $self->{Turn};
}

sub dipMap {
	my $self = shift;
	if (@_) {
		$self->{DipMap} = shift;
	}
	return $self->{DipMap};
}

sub countries {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Countries}}[$i];
		}
		${$self->{Countries}}[$i] = $x;
	}
	return $self->{Countries};
}

sub countriesByName {
	my $self = shift;
	my $name = shift;
	for my $country (@{$self->{Countries}}) {
		if ($country->name() eq $name) {
			return $country;
		}
	}
}

sub failProhibit {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{FailProhibit}}[$i];
		}
		${$self->{FailProhibit}}[$i] = $x;
	}
	return $self->{FailProhibit};
}

sub failedOrders {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{FailedOrders}}[$i];
		}
		${$self->{FailedOrders}}[$i] = $x;
	}
	return $self->{FailedOrders};
}

sub loseOrders {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{LoseOrders}}[$i];
		}
		${$self->{LoseOrders}}[$i] = $x;
	}
	return $self->{LoseOrders};
}

# ‚±‚±‚Ü‚Åaccessor

sub getOrders {
	my $self = shift;
	my $c = shift;
	return @{$self->countriesByName($c)->order()};
}

sub addOrder {
	my $self = shift;
	my $c = shift;
	my $order = shift;
	if (!$self->checkOrder($order)) {
		return;
	}
	$self->countriesByName($c)->addOrder($order);
}

sub checkOrder {
	my $self = shift;
	my $order = shift;
	# TODO
	return 1;
}

sub delOrder {
	my $self = shift;
	my $c = shift;
	my $order = shift;
	$self->countriesByName($c)->delOrder($order);
}

sub thinkEnd {
	my $self = shift;
	my $c = shift;
	if ($self->countries($c)->allOrdered()) {
		$self->countries($c)->thinking(0);
		
		if ($self->turn() == 1 || $self->turn() == 3) {
			$self->gmJudgeOrder();
		} elsif ($self->turn() == 5) {
			$self->endAdjust();
		}
	}
}

sub allThinkEnd {
	my $self = shift;
	for my $country (@{$self->countries()}) {
		if ($country->thinking()) {
			return 0;
		}
	}
	return 1;
}

sub gmJudgeOrder {
	my $self = shift;
	if (($self->turn() != 1 && $self->turn() != 3) || !$self->allThinkEnd()) {
		return;
	}
	my @allOrder = ();
	for my $country (@{$self->countries()}) {
		for my $order (@{$country->order()}) {
			push @allOrder, $order;
		}
	}

	my %moveAfter = ();
	my %allSupports = ();
	for my $order (@allOrder) {
		unless ($moveAfter{$order->moveTo()}) {
			$moveAfter{$order->moveTo()} = [];
		}
		push @{$moveAfter{$order->moveTo()}}, $order;
		if ($order->support() ne '') {
			push @{$allSupport{$order->supportAt()}}, $order;
		}
	}
	
	my @successOrder = ();
	my @failOrder = ();
	for my $afterPos (keys(%moveAfter)) {
		if (@{$moveAfter{$afterPos}} > 1) {
			my %posSupport = ();
			for my $support (@{$allSupport{$afterPos}}) {
				$posSupport{$support->support()}++;
			}
			my $maxSupport = -1;
			my $maxPos = 'noSupport';
			for my $support (keys(%posSupport)) {
				if ($maxSupport < $posSupport{$support}) {
					$maxSupport = $posSupport{$support};
					$maxPos = $support;
				} elsif ($maxSupport == $posSupport{$support}) {
					$maxPos = '';
				}
			}
			if ($maxPos ne '') {
				for my $order (@{$moveAfter{$afterPos}}) {
					if ($order->start() eq $maxPos) {
						push @successOrder, $order;
					} else {
						push @failOrder, $order;
					}
				}
			}
		} else {
			push @successOrder, ${$moveAfter{$afterPos}}[0];
		}
	}
	
	@{$self->failProhibit()} = ();
	for my $order (@successOrder) {
		$self->countriesByName($order->country())->applyOrder($order);
		push @{$self->failProhibit()}, $order->start();
		push @{$self->failProhibit()}, $order->end();
	}
	@{$self->failedOrders()} = ();
	for my $order (@failOrder) {
		push @{$self->failedOrders()}, $order;
	}
	
	$self->turnIncrement();
	if (@{$self->failedOrders()} <= 0) {
		$self->turnIncrement();
	}
}

sub addLose {
	my $self = shift;
	my $c = shift;
	my $start = shift;
	my $lose = shift;
	for my $orderI (0..$#{$self->failedOrders()}) {
		my $order = ${$self->failedOrders()}[$orderI];
		if ($order->start() eq $start && $order->country() eq $country) {
			splice @{$self->failedOrders()}, $orderI, 1;
			$order->lose($lose);
			push @{$self->loseOrders()}, $order;
			last;
		}
	}
	if (@{$self->failedOrders()} <= 0) {
		$self->gmJudgeLose();
	}
}

sub gmJudgeLose {
	my $self = shift;
	my %samePos = ();
	for my $order (@{$self->loseOrders()}) {
		$semaPos{$order->lose()}++;
	}
	for my $pos (keys(%samePos)) {
		if ($samePos{$pos} > 1) {
			push @{$self->failProhibit()}, $pos;
		}
	}
	for my $order (@{$self->loseOrders()}) {
		my $apply = 1;
		for my $prohibit (@{$self->failProhibit()}) {
			if ($order->lose() eq $prohibit) {
				$apply = 0;
			}
		}
		if ($apply) {
			$self->countriesByName($order->country())->applyLose($order);
		} else {
			$self->countriesByName($order->country())->erase($order);
		}
	}
	$self->turnIncrement();
}

sub addArmy {
	my $self = shift;
	my $c = shift;
	my $capital = shift;
	$self->countriesByName($c)->addArmy($capital);
}

sub addNavy {
	my $self = shift;
	my $c = shift;
	my $capital = shift;
	$self->countriesByName($c)->addNavy($capital);
}

sub gmJudgeAdjust {
	my $self = shift;
	if ($self->turn() != 5 || !$self->allThinkEnd()) {
		return;
	}
	$self->checkConqure();
	$self->checkPeace();
}

sub endAdjust {
	my $self = shift;
	$self->turnIncrement();
}

sub checkPeace {
	my $self = shift;
	# TODO
}

sub checkConqure {
	my $self = shift;
	# TODO
}

sub gameOver {
	my $self = shift;
	# TODO
}

sub turnIncrement {
	my $self = shift;
	if ($self->turn() == 5) {
		$self->turn(1);
	} else {
		$self->turn($self->turn() + 1);
	}
	if ($self->turn() == 5) {
		$self->gmJudgeAdjust();
	}
	for my $country (@{$self->countries()}) {
		$country->thinking(1);
	}
}

sub TO_JSON {
	my $self = shift;
	my %h_self = map { $_ => $self->{$_} } keys(%$self);

	return { ref($self) => \%h_self };
}

1;