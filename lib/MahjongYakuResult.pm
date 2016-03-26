#!/usr/local/bin/perl --
package MahjongYakuResult;
use strict;
use warnings;

sub new {
	my $clazz = shift;
	my $self = {
		Fan => 0,
		Yaku => '',
		@_,
	};
	return bless $self, $clazz;
}

sub fan {
	my $self = shift;
	if (@_) {
		$self->{Fan} = shift;
	}
	return $self->{Fan};
}

sub yaku {
	my $self = shift;
	if (@_) {
		$self->{Yaku} = shift;
	}
	return $self->{Yaku};
}

1;