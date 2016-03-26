#!/usr/local/bin/perl --
package NobOOwner;
use strict;
use warnings;
use JSON qw/decode_json/;

sub new {
	my $clazz = shift;
	my $self = {
		TerritoryID => 0,
		OwnerName => 'no user',
		Capital => 1
	};
	return bless $self, $clazz;
}

sub territoryId {
	my $self = shift;
	if (@_) {
		$self->{TerritoryID} = shift;
	}
	return $self->{TerritoryID};
}

sub ownerName {
	my $self = shift;
	if (@_) {
		$self->{OwnerName} = shift;
	}
	return $self->{OwnerName};
}

sub capital {
	my $self = shift;
	if (@_) {
		$self->{Capital} = shift;
	}
	return $self->{Capital};
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
		$self->{$key} = ${${$data}{NobOOwner}}{$key};
	}
	
	return $self;
}

1;