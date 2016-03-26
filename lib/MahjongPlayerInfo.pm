#!/usr/local/bin/perl --
package MahjongPlayerInfo;
use strict;
use warnings;
use Encode::Guess qw/shift-jis/;

sub new {
	my $clazz = shift;
	my $self = {
		Name => 'player',
		Point => 25000,
		Position => 0,
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

sub pname {
	my $self = shift;
	my $pname = $self->name();
	if ($self->name() !~ /dummy/) {
		$pname = pack 'H*', $pname; 
		my $decoder = Encode::Guess->guess($pname);
		ref($decoder) || die "Can't guess: " . $decoder;
		$pname = $decoder->decode($pname);
	}
	return $pname;
}

sub point {
	my $self = shift;
	if (@_) {
		$self->{Point} = shift;
	}
	return $self->{Point};
}

sub pointAdd {
	my $self = shift;
	my $point = shift;
	$self->{Point} += $point;
}

sub position {
	my $self = shift;
	if (@_) {
		$self->{Position} = shift;
	}
	return $self->{Position};
}

sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Name' => $self->name(),
		'PName' => $self->pname(),
		'Point' => $self->point(),
		'Position' => $self->position(),
	);
	return {%self_hash};
}

sub toString {
	my $self = shift;
	my $ret = '';
	$ret .= $self->name() . ':' . $self->point();
	return $ret;
}

sub setAll {
	my $self = shift;
	my $str = shift;
	chomp $str;
	my ($name, $point) = split /:/, $str;
	$self->name($name);
	$self->point($point);
}

1;