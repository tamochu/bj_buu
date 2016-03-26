#!/usr/local/bin/perl --
package DiplomacyCountry;
use strict;
use warnings;

sub new {
	my $clazz = shift;
	my $self = {
		Name => 'noname',
		Rank => 0,
		Thinking => 1,
		Army => [],
		Navy => [],
		Order => [],
		Power => 1,
		CapitalInland => [],
		CapitalSeaside => [],
	};
	return bless $self, $clazz;
}

sub name {
	my $self = shift;
	if (@_) {
		$self->{Name} = shift;
	}
	return $self->{Name};
}

sub rank {
	my $self = shift;
	if (@_) {
		$self->{Rank} = shift;
	}
	return $self->{Rank};
}

sub thinking {
	my $self = shift;
	if (@_) {
		$self->{Thinking} = shift;
	}
	return $self->{Thinking};
}

sub army {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Army}}[$i];
		}
		${$self->{Army}}[$i] = $x;
	}
	return $self->{Army};
}

sub navy {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Navy}}[$i];
		}
		${$self->{Navy}}[$i] = $x;
	}
	return $self->{Navy};
}

sub order {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Order}}[$i];
		}
		${$self->{Order}}[$i] = $x;
	}
	return $self->{Order};
}

sub power {
	my $self = shift;
	if (@_) {
		$self->{Power} = shift;
	}
	return $self->{Power};
}

sub capitalInland {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{CapitalInland}}[$i];
		}
		${$self->{CapitalInland}}[$i] = $x;
	}
	return $self->{CapitalInland};
}

sub capitalSeaside {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{CapitalSeaside}}[$i];
		}
		${$self->{CapitalSeaside}}[$i] = $x;
	}
	return $self->{CapitalSeaside};
}

sub addOrder {
	my $self = shift;
	my $order = shift;
	$order->country($self->name());
	push @{$self->order()}, shift;
}

sub delOrder {
	my $self = shift;
	my $order = shift;
	splice @{$self->order()}, $order, 1;
}

sub allOrdered {
	my $self = shift;
	my $o = 0;
	my $a = 0;
	my $n = 0;
	for my $order (@{$self->order()}) {
		$o++;
	}
	for my $army (@{$self->army()}) {
		$a++;
	}
	for my $navy (@{$self->navy()}) {
		$n++;
	}
	return ($o == $a + $n);
}

sub applyOrder {
	my $self = shift;
	my $order = shift;
	# TODO
}

sub applyLose {
	my $self = shift;
	my $order = shift;
	# TODO
}

sub erase {
	my $self = shift;
	my $order = shift;
	# TODO
}

sub addArmy {
	my $self = shift;
	my $capital = shift;
	# TODO
}

sub addNavy {
	my $self = shift;
	my $capital = shift;
	# TODO
}

sub TO_JSON {
	my $self = shift;
	my %h_self = map { $_ => $self->{$_} } keys(%$self);

	return { ref($self) => \%h_self };
}

1;