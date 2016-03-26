#!/usr/local/bin/perl --
package MahjongHo;
use strict;
use warnings;
use MahjongPai;

sub new {
	my $clazz = shift;
	my $self = {
		Ho => [],
		ReachAt => -1,
		Position => 0,
		Eaten => [],
	};
	return bless $self, $clazz;
}

sub ho {
	my $self = shift;
	return $self->{Ho};
}

sub clearHo {
	my $self = shift;
	$self->{Ho} = [];;
}

sub reachAt {
	my $self = shift;
	if (@_) {
		$self->{ReachAt} = shift;
	}
	return $self->{ReachAt};
}

sub position {
	my $self = shift;
	if (@_) {
		$self->{Position} = shift;
	}
	return $self->{Position};
}

sub eaten {
	my $self = shift;
	if (@_) {
		$self->{Eaten} = @_;
	}
	return $self->{Eaten};
}

sub clearEaten {
	my $self = shift;
	$self->{Eaten} = [];
}

sub addHo {
	my $self = shift;
	my $str = shift;
	my $pai = MahjongPai->new();
	$pai->str($str);
	push @{$self->ho()}, $pai;
}

sub reach {
	my $self = shift;
	if ($self->reachAt() == -1) {
		my @ho = @{$self->ho()};
		if (@ho > 0) {
			$self->reachAt($#ho);
		}
	}
}

sub eat {
	my $self = shift;
	my @ho = @{$self->ho()};
	if (@ho > 0) {
		push @{$self->eaten()}, $#ho;
	}
}

sub toString {
	my $self = shift;
	my $ret_str = '';
	my $i = 0;
	for my $pai (@{$self->ho()}) {
		$ret_str .= $pai->str();
		if ($i == $self->reachAt()) {
			$ret_str .= 'r';
		}
		if (grep {$_ eq $i} @{$self->eaten()}) {
			$ret_str .= 'e';
		}
		$i++;
	}
	return $ret_str;
}

sub setAll {
	my $self = shift;
	my $str = shift;
	$self->clearHo();
	$self->reachAt(-1);
	$self->clearEaten();
	my @split_str = split //, $str;
	my $i = 0;
	while ($i < @split_str) {
		my $c = $split_str[$i];
		if ($c eq 'r') {
			$self->reach();
		} elsif ($c eq 'e') {
			$self->eat();
		} elsif ($c eq 'm' || $c eq 's' || $c eq 'p' || $c eq 'z') {
			my $num = $split_str[$i + 1];
			$self->addHo($c . $num);
			$i++;
		}
		$i++;
	}
}

sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Ho' => $self->toString(),
	);
	return {%self_hash};
}

1;