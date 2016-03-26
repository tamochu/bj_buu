#!/usr/local/bin/perl --
package NobOArmySoldier;
use strict;
use warnings;
use JSON qw/decode_json/;

sub new {
	my $clazz = shift;
	my $self = {
		ArmyID => 0,
		Amount => 0
	};
	return bless $self, $clazz;
}

sub armyId {
	my $self = shift;
	if (@_) {
		$self->{ArmyID} = shift;
	}
	return $self->{ArmyID};
}

sub amount {
	my $self = shift;
	if (@_) {
		$self->{Amount} = shift;
	}
	return $self->{Amount};
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
		$self->{$key} = ${${$data}{NobOArmySoldier}}{$key};
	}
}

1;