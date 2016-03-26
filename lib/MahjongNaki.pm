#!/usr/local/bin/perl --
package MahjongNaki;
use strict;
use warnings;
use MahjongPai;

sub new {
	my $clazz = shift;
	my $self = {
		PaiNaki => MahjongPai->new(),
		Pai1 => MahjongPai->new(),
		Pai2 => MahjongPai->new(),
		KanFlag => 0,
		NakiFrom => 3,
	};
	return bless $self, $clazz;
}

sub clone {
	my $self = shift;
	my $clone =  MahjongNaki->new();
	$clone->paiNaki()->str($self->paiNaki()->str());
	$clone->pai1()->str($self->pai1()->str());
	$clone->pai2()->str($self->pai2()->str());
	$clone->kanFlag($self->kanFlag());
	$clone->nakiFrom($self->nakiFrom());
	return $clone;
}

sub paiNaki {
	my $self = shift;
	return $self->{PaiNaki};
}

sub pai1 {
	my $self = shift;
	return $self->{Pai1};
}

sub pai2 {
	my $self = shift;
	return $self->{Pai2};
}

sub kanFlag {
	my $self = shift;
	if (@_) {
		$self->{KanFlag} = shift;
	}
	return $self->{KanFlag};
}

sub nakiFrom {
	my $self = shift;
	if (@_) {
		$self->{NakiFrom} = shift;
	}
	return $self->{NakiFrom};
}

sub setPai {
	my $self = shift;
	my $str = shift;
	my @split_str = split //, $str;
	if ($split_str[0] eq '-') {
		if ($split_str[-1] eq '-') {
			# 対面ポン
			$self->{Pai1}->str($split_str[1] . $split_str[2]);
			$self->{PaiNaki}->str($split_str[3] . $split_str[4]);
			$self->{Pai2}->str($split_str[5] . $split_str[6]);
			if (@split_str == 10) {
				$self->{KanFlag} = 1;
			}
			$self->{NakiFrom} = 2;
		} else {
			# 上家ポンチー
			$self->{PaiNaki}->str($split_str[1] . $split_str[2]);
			$self->{Pai1}->str($split_str[3] . $split_str[4]);
			$self->{Pai2}->str($split_str[5] . $split_str[6]);
			if (@split_str == 9) {
				$self->{KanFlag} = 1;
			}
			$self->{NakiFrom} = 3;
		}
	} else {
		if ($split_str[-1] eq '-') {
			# 下家ポン
			$self->{Pai1}->str($split_str[0] . $split_str[1]);
			$self->{Pai2}->str($split_str[2] . $split_str[3]);
			$self->{PaiNaki}->str($split_str[4] . $split_str[5]);
			if (@split_str == 9) {
				$self->{KanFlag} = 1;
			}
			$self->{NakiFrom} = 1;
		} else {
			# 暗槓
			$self->{Pai1}->str($split_str[0] . $split_str[1]);
			$self->{Pai2}->str($split_str[2] . $split_str[3]);
			$self->{PaiNaki}->str($split_str[4] . $split_str[5]);
			$self->{KanFlag} = 2;
			$self->{NakiFrom} = 0;
		}
	}
}

sub setMentsu {
	my $self = shift;
	my $str = shift;
	my @split_str = split //, $str;
	$self->{Pai1}->str($split_str[0] . $split_str[1]);
	$self->{Pai2}->str($split_str[2] . $split_str[3]);
	$self->{PaiNaki}->str($split_str[4] . $split_str[5]);
	$self->{KanFlag} = -1;
	$self->{NakiFrom} = 0;
}

sub toString {
	my $self = shift;
	my $ret_str = '';
	if ($self->kanFlag() == 2) {
		for my $i (0..3) {
			$ret_str .= $self->paiNaki()->str();
		}
	} else {
		if ($self->kanFlag() != -1) {
			if ($self->nakiFrom() == 2 || $self->nakiFrom() == 3) {
				$ret_str .= '-';
			}
		}
		$ret_str .= $self->paiNaki()->str() . $self->pai1()->str() . $self->pai2()->str();
		if ($self->kanFlag() == 1) {
			$ret_str .= $self->paiNaki()->str();
		}
		if ($self->kanFlag() != -1) {
			if ($self->nakiFrom() == 1 || $self->nakiFrom() == 2) {
				$ret_str .= '-';
			}
		}
	}
	return $ret_str;
}

sub isShuntsu {
	my $self = shift;
	return ($self->pai1()->str() ne $self->pai2()->str());
}

sub isKotsu {
	my $self = shift;
	return !$self->isShuntsu();
}

sub isPon {
	my $self = shift;
	return ($self->isKotsu() && $self->kanFlag() == 0);
}

sub isAnko {
	my $self = shift;
	return ($self->isKotsu() && $self->kanFlag() == -1);
}

sub isMinkan {
	my $self = shift;
	return ($self->isKotsu() && $self->kanFlag() == 1);
}

sub isAnkan {
	my $self = shift;
	return ($self->isKotsu() && $self->kanFlag() == 2);
}

sub isIku {
	my $self = shift;
	if ($self->pai1()->isIku()) {
		return 1;
	}
	if ($self->pai2()->isIku()) {
		return 1;
	}
	if ($self->paiNaki()->isIku()) {
		return 1;
	}
	return 0;
}

sub isTsu {
	my $self = shift;
	if ($self->pai1()->isTsu()) {
		return 1;
	}
	if ($self->pai2()->isTsu()) {
		return 1;
	}
	if ($self->paiNaki()->isTsu()) {
		return 1;
	}
	return 0;
}

sub isYaochu {
	my $self = shift;
	return ($self->isIku() || $self->isTsu());
}

sub getMinPaiStr {
	my $self = shift;
	my $min_pai_str = $self->pai1()->str();
	my $min_num = $self->pai1()->getNum();
	if ($min_num > $self->pai2()->getNum()) {
		$min_pai_str = $self->pai2()->str();
		$min_num = $self->pai2()->getNum();
	}
	if ($min_num > $self->paiNaki()->getNum()) {
		$min_pai_str = $self->paiNaki()->str();
		$min_num = $self->paiNaki()->getNum();
	}
	return $min_pai_str;
}

sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'PaiNaki' => $self->paiNaki(),
		'Pai1' => $self->pai1(),
		'Pai2' => $self->pai2(),
		'KanFlag' => $self->kanFlag(),
		'NakiFrom' => $self->nakiFrom()
	);
	return {%self_hash};
}

1;