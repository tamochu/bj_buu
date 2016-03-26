#!/usr/local/bin/perl --
package DiplomacyOrder;
use strict;
use warnings;

sub new {
	my $clazz = shift;
	my $self = {
		Kind => 'F',
		Start => '',
		End => 'Holds',
		Support => '',
		SupportAt => '',
		ComboyStart => '',
		ComboyEnd => '',
		Country => '',
		Lose => '',
		Erase => 0,
		Add => 0
	};
	return bless $self, $clazz;
}

sub kind {
	my $self = shift;
	if (@_) {
		$self->{Kind} = shift;
	}
	return $self->{Kind};
}

sub start {
	my $self = shift;
	if (@_) {
		$self->{Start} = shift;
	}
	return $self->{Start};
}

sub end {
	my $self = shift;
	if (@_) {
		$self->{End} = shift;
	}
	return $self->{End};
}

sub support {
	my $self = shift;
	if (@_) {
		$self->{Support} = shift;
	}
	return $self->{Support};
}

sub supportAt {
	my $self = shift;
	if (@_) {
		$self->{SupportAt} = shift;
	}
	return $self->{SupportAt};
}

sub comboyStart {
	my $self = shift;
	if (@_) {
		$self->{ComboyStart} = shift;
	}
	return $self->{ComboyStart};
}

sub comboyEnd {
	my $self = shift;
	if (@_) {
		$self->{ComboyEnd} = shift;
	}
	return $self->{ComboyEnd};
}

sub country {
	my $self = shift;
	if (@_) {
		$self->{Country} = shift;
	}
	return $self->{Country};
}

sub lose {
	my $self = shift;
	if (@_) {
		$self->{Lose} = shift;
	}
	return $self->{Lose};
}

sub erase {
	my $self = shift;
	if (@_) {
		$self->{Erase} = shift;
	}
	return $self->{Erase};
}

sub add {
	my $self = shift;
	if (@_) {
		$self->{Add} = shift;
	}
	return $self->{Add};
}

sub resetOrder {
	my $self = shift;
	my $start = shift;
	$self->kind('F');
	$self->start($start);
	$self->end('Holds');
	$self->support('');
	$self->supportAt('');
	$self->comboyStart('');
	$self->comboyEnd('');
	$self->country('');
	$self->lose('');
	$self->erase(0);
	$self->add(0);
}

# 移行publicメソッド
sub hold {
	my $self = shift;
	my $start = shift;
	$self->resetOrder($start);
}

sub move {
	my $self = shift;
	my $start = shift;
	my $end = shift;
	$self->resetOrder($start);
	$self->end($end);
}

sub setSupport {
	my $self = shift;
	my $start = shift;
	my $support = shift;
	my $supportAt = shift;
	$self->resetOrder($start);
	$self->support($support);
	$self->supportAt($supportAt);
}

sub comboy {
	my $self = shift;
	my $start = shift;
	my $comboy = shift;
	my $comboyEnd = shift;
	$self->resetOrder($start);
	$self->kind('N');
	$self->comboyStart($comboy);
	$self->comboyEnd($comboyEnd);
}

sub moveTo {
	my $self = shift;
	if ($self->end() eq 'Holds') {
		return $self->start();
	} else {
		return $self->end();
	}
}

sub TO_JSON {
	my $self = shift;
	my %h_self = map { $_ => $self->{$_} } keys(%$self);

	return { ref($self) => \%h_self };
}

1;