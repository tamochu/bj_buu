#!/usr/local/bin/perl --
package NobOArmy;
use strict;
use warnings;
use JSON qw/decode_json/;

sub new {
	my $clazz = shift;
	my $self = {
		ID => 0,
		TargetTerritoryID => 0,
		LeaderName => 'no user',
		X => 0,
		Y => 0,
		Speed => 0.1,
		Civilization => 0,
		Trade => 0
	};
	return bless $self, $clazz;
}

sub id {
	my $self = shift;
	if (@_) {
		$self->{ID} = shift;
	}
	return $self->{ID};
}

sub targetTerritoryId {
	my $self = shift;
	if (@_) {
		$self->{TargetTerritoryID} = shift;
	}
	return $self->{TargetTerritoryID};
}

sub leaderName {
	my $self = shift;
	if (@_) {
		$self->{LeaderName} = shift;
	}
	return $self->{LeaderName};
}

sub x {
	my $self = shift;
	if (@_) {
		$self->{X} = shift;
	}
	return $self->{X};
}

sub y {
	my $self = shift;
	if (@_) {
		$self->{Y} = shift;
	}
	return $self->{Y};
}

sub speed {
	my $self = shift;
	if (@_) {
		$self->{Speed} = shift;
	}
	return $self->{Speed};
}

sub civilization {
	my $self = shift;
	if (@_) {
		$self->{Civilization} = shift;
	}
	return $self->{Civilization};
}

sub trade {
	my $self = shift;
	if (@_) {
		$self->{Trade} = shift;
	}
	return $self->{Trade};
}

# accessor ‚±‚±‚Ü‚Å

sub setPosition {
	my $self = shift;
	my $from = shift;
	my $to = shift;

	$self->x($from->x());
	$self->y($from->y());
	$self->targetTerritoryId($to->id());
	$self->civilization($from->civilization());
}

sub move {
	my $self = shift;
	my $diff = shift;
	my $targetTerritory = shift;
	
	my $targetX = $targetTerritory->x();
	my $targetY = $targetTerritory->y();
	
	my $distance = sqrt((($targetX - $self->x()) ** 2) + (($targetY - $self->y()) ** 2));
	if ($distance < $self->speed() * $diff) {
		$self->x($targetX);
		$self->y($targetY);
		return 1;
	} else {
		my $p = $self->speed() * $diff / $distance;
		$self->x($targetX * $p + $self->x() * (1.0 - $p));
		$self->y($targetY * $p + $self->y() * (1.0 - $p));
		return 0;
	}
}

sub TO_JSON {
	my $self = shift;
	my %h_self = map { $_ => $self->{$_} } keys(%$self);

	return { ref($self) => \%h_self };
}

sub FROM_JSON {
	my $self = shift;
	my $json = shift;
	
	my $data = decode_json($json);
	for my $key (keys(%$self)) {
		$self->{$key} = ${${$data}{NobOArmy}}{$key};
	}
}

1;