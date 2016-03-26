#!/usr/local/bin/perl --
package MahjongPai;
use strict;
use warnings;

sub new {
	my $clazz = shift;
	my $self = {
		Str => 'u0',
		UraFlag => 0,
	};
	return bless $self, $clazz;
}

sub str {
	my $self = shift;
	if (@_) {
		$self->{Str} = shift;
	}
	return $self->{Str};
}

sub uraFlag {
	my $self = shift;
	if (@_) {
		$self->{UraFlag} = shift;
	}
	return $self->{UraFlag};
}

sub getType {
	my $self = shift;
	return substr($self->str(), 0, 1);
}

sub getNum {
	my $self = shift;
	return int(substr($self->str(), 1, 1));
}

sub isTsu {
	my $self = shift;
	return ($self->getType() eq 'z');
}

sub isIku {
	my $self = shift;
	my $num = $self->getNum();
	return (!$self->isTsu() && ($num == 1 || $num == 9));
}

sub isYaochu {
	my $self = shift;
	return ($self->isTsu() || $self->isIku());
}

sub getDoraNextStr {
	my $self = shift;
	my $type = $self->getType();
	my $num = $self->getNum() + 1;
	if ($type eq 'z') {
		if ($num == 5) {
			$num = 1;
		} elsif ($num == 8) {
			$num = 5;
		}
	} else {
		if ($num == 10) {
			$num = 1;
		}
	}
	return ($type . $num);
}


sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Str' => $self->uraFlag() ? 'u0' : $self->str(), 
	);
	return {%self_hash};
}

sub strToNum {
	my $str = shift;
	my $type = substr($str, 0, 1);
	my $num = int(substr($str, 1, 1));
	if ($type eq 'm') {
		if ($num >= 1  && $num <= 9) {
			return ($num - 1);
		}
	} elsif ($type eq 's') {
		if ($num >= 1  && $num <= 9) {
			return ($num + 8);
		}
	} elsif ($type eq 'p') {
		if ($num >= 1  && $num <= 9) {
			return ($num + 17);
		}
	} elsif ($type eq 'z') {
		if ($num >= 1  && $num <= 7) {
			return ($num + 26);
		}
	}
	return -1;
}

sub numToStr {
	my $num = shift;
	my $type = int($num / 9);
	my $numStr = ($num % 9) + 1;
	my $typeStr = 'u';
	if ($type == 0) {
		$typeStr = 'm';
	} elsif ($type == 1) {
		$typeStr = 's';
	} elsif ($type == 2) {
		$typeStr = 'p';
	} elsif ($type == 3) {
		$typeStr = 'z';
	} else {
		return 'u0';
	}
	return ($typeStr . $numStr);
}

1;