#!/usr/local/bin/perl --
package MahjongYama;
use strict;
use warnings;
use MahjongPai;

sub new {
	my $clazz = shift;
	my $self = {
		Yama => [],
		KanNum => 1,
		TedumiRest => [],
		TedumiYamas => [],
		Round => -1,
		Tsumikomi => [0, 0, 0, 0],
	};
	return bless $self, $clazz;
}

sub yama {
	my $self = shift;
	return $self->{Yama};
}

sub clearYama {
	my $self = shift;
	$self->{Yama} = [];
}

sub pushYama {
	my $self = shift;
	my $pai = shift;
	push @{$self->{Yama}}, $pai;
}

sub kanNum {
	my $self = shift;
	if (@_) {
		$self->{KanNum} = shift;
	}
	return $self->{KanNum};
}

sub getRest {
	my $self = shift;
	return (@{$self->yama()} - 14);
}

sub getDoraStrs {
	my $self = shift;
	my @ret = ();
	for my $i (1..$self->kanNum()) {
		my $dora = ${$self->yama()}[-2 * $i - 4];
		if (defined($dora)) {
			push @ret, $dora->str();
		}
	}
	return @ret;
}

sub getAllDora {
	my $self = shift;
	my $reach = shift;
	my @doras = ();
	for my $i (1..$self->kanNum()) {
		my $dora = ${$self->yama()}[-2 * $i - 4];
		push @doras, $dora;
	}
	if ($reach) {
		for my $i (1..$self->kanNum()) {
			my $ura = ${$self->yama()}[-2 * $i - 3];
			push @doras, $ura;
		}
	}
	
	return @doras;
}

sub isEnd {
	my $self = shift;
	return $self->getRest() <= 0 || $self->kanNum() > 4;
}

sub setDefault {
	my $self = shift;
	$self->clearYama();
	my @supai_type = ('m', 's', 'p');
	for my $type (@supai_type) {
		for my $num (1..9) {
			for my $j (0..3) {
				my $supai = MahjongPai->new();
				$supai->str($type . $num);
				$self->pushYama($supai);
			}
		}
	}
	for my $num (1..7) {
		for my $j (0..3) {
			my $tsupai = MahjongPai->new();
			$tsupai->str('z' . $num);
			$self->pushYama($tsupai);
		}
	}
	$self->shuffle();
}

sub shuffle {
	my $self = shift;
	my $i = @{$self->yama()};
	while ($i) {
		my $j = int(rand($i));
		my $t = ${$self->yama()}[--$i];
		${$self->yama()}[$i] = ${$self->yama()}[$j];
		${$self->yama()}[$j] = $t;
	}
=pod
	my @str = qw/m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 m9 m9 m9 m9/;
	my @indexes = (1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4);
	
	for my $j (0..13) {
		my $pi = 0;
		for my $y (0..$#{$self->yama()}) {
			my $t = ${$self->yama()}[$y];
			if ($t->str() eq $str[$j]) {
				$pi++;
			}
			if ($pi == $indexes[$j]) {
				${$self->yama()}[$y] = ${$self->yama()}[$j];
				${$self->yama()}[$j] = $t;
				last;
			}
		}
	}
	
	$i = 0;
	for my $ton (0..2) {
		for my $hai (0..3) {
			my $j = $ton * 16 + $hai;
			my $t = ${$self->yama()}[$i];
			${$self->yama()}[$i] = ${$self->yama()}[$j];
			${$self->yama()}[$j] = $t;
			$i++;
		}
	}
	for my $chonchon (48, 52) {
		my $j = $chonchon;
		my $t = ${$self->yama()}[$i];
		${$self->yama()}[$i] = ${$self->yama()}[$j];
		${$self->yama()}[$j] = $t;
		$i++;
	}
=cut
}

sub kan {
	my $self = shift;
	$self->kanNum($self->kanNum() + 1);
	my @yama = $self->yama();
	my $index_wan = @yama - 9;
	my $pai = splice @{$self->yama()}, $index_wan, 1;
	return $pai;
}

sub draw {
	my $self = shift;
	my $pai = shift @{$self->yama()};
	return $pai;
}

sub tedumiRest {
	my $self = shift;
	return $self->{TedumiRest};
}

sub tedumiYamas {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if ($i < 0 || $i >= @{$self->{TedumiYamas}}) {
			return undef;
		}
		if (!defined($x)) {
			return ${$self->{TedumiYamas}}[$i];
		}
		${$self->{TedumiYamas}}[$i] = $x;
	}
	return $self->{TedumiYamas};
}

sub clearTedumi {
	my $self = shift;
	$self->{TedumiRest} = [];
	$self->{TedumiYamas} = [[], [], [], []];
	$self->{Tsumikomi} = [0, 0, 0, 0];
}

sub beginTedumi {
	my $self = shift;
	my $round = shift;
	$self->round($round);
	$self->clearTedumi();
	my @supai_type = ('m', 's', 'p');
	for my $type (@supai_type) {
		for my $num (1..9) {
			for my $j (0..3) {
				push @{$self->tedumiRest()}, ($type . $num . $j);
			}
		}
	}
	for my $num (1..7) {
		for my $j (0..3) {
			push @{$self->tedumiRest()}, ('z' . $num . $j);
		}
	}
}

sub isTedumiEnd {
	my $self = shift;
	return @{$self->tedumiRest()} == 0;
}

sub isRemain {
	my $self = shift;
	my $str = shift;
	for my $r (@{$self->tedumiRest()}) {
		if ($str eq $r) {
			return 1;
		}
	}
	return 0;
}

sub restToYama {
	my $self = shift;
	my $position = shift;
	my $str = shift;
	
	if (!defined($position)) {
		return;
	}
	if ($position < 0 || $position >= 4) {
		return;
	}
	if (!defined(${$self->tedumiYamas}[$position])) {
		${$self->tedumiYamas}[$position] = [];
		push @{${$self->tedumiYamas}[$position]}, 'u0' for (0..33);
	}
	my $pushable = 0;
	for my $p (@{${$self->tedumiYamas}[$position]}) {
		if ($p eq 'u0') {
			$pushable = 1;
			last;
		}
	}
	if ($pushable == 0) {
		return;
	}
	if (!$self->isRemain($str)) {
		return;
	}
	my @order = $self->tsumikomiOrder($position);
	
	for my $i (0..$#{$self->tedumiRest()}) {
		if ($str eq ${$self->tedumiRest()}[$i]) {
			my $pStr = splice @{$self->tedumiRest()}, $i, 1;
			for my $j (@order) {
				if (${${$self->tedumiYamas}[$position]}[$j] eq 'u0') {
					${${$self->tedumiYamas}[$position]}[$j] = $pStr;
					last;
				}
			}
			last;
		}
	}
}

sub tsumikomiOrder {
	my $self = shift;
	my $position = shift;

	my @order = ();
	
	for my $i (0..33) {
		push @order, $i;
	}
	
	my $dir = (8 + $position - $self->round()) % 4;
	if ($self->tsumikomi($position) == 2) {
		# å≥ò\êœÇ›
		@order = ();
		
		for my $i (0..33) {
			push @order, -1;
		}
		my $tsumiPos = (2 + $dir) % 4;
		my $ii = 0;
		for my $i (0..33) {
			if (($i % 4) == $tsumiPos) {
				$order[$ii] = $i;
				$ii++;
			}
		}
		while ($ii < 34) {
			my $j = 0;
			while ($j < 34) {
				my $find = 0;
				for my $o (@order) {
					if ($o == $j) {
						$find = 1;
					}
				}
				if ($find == 0) {
					last;
				}
				$j++;
			}
			$order[$ii] = $j;
			$ii++;
		}
	} elsif ($self->tsumikomi($position) == 3) {
		# îöíeêœÇ›
		@order = ();
		
		for my $i (0..33) {
			push @order, -1;
		}
		my $firstPos;
		if ($dir == 0) {
			$order[0] = 4;
			$order[1] = 5;
			$firstPos = 10;
		} elsif ($dir == 1) {
			$firstPos = 8;
		} elsif ($dir == 2) {
			$firstPos = 14;
		} elsif ($dir == 3) {
			$firstPos = 20;
		}
		my $ii = 2;
		my $i = $firstPos;
		my $block = 1;
		while ($i < 34) {
			$order[$ii] = $i;
			$ii++;
			if ($block < 4) {
				$i++;
				$block++;
			} else {
				$i += 13;
				$block = 1;
			}
		}
		while ($ii < 34) {
			my $j = 0;
			while ($j < 34) {
				my $find = 0;
				for my $o (@order) {
					if ($o == $j) {
						$find = 1;
					}
				}
				if ($find == 0) {
					last;
				}
				$j++;
			}
			$order[$ii] = $j;
			$ii++;
		}
	}
	return @order;
}

sub randomGet {
	my $self = shift;
	my $position = shift;
	my $str = ${$self->tedumiRest()}[int(rand(@{$self->tedumiRest()}))];
	$self->restToYama($position, $str);
}

sub tedumiTerminate {
	my $self = shift;
	my $oyaPos = shift;
	$self->clearYama();
	for my $i (0..3) {
		my $pos = ($oyaPos - $i + 4) % 4;
		my $yama = ${$self->tedumiYamas()}[$pos];
		for my $pStr (@{$yama}) {
			my @ps = split //, $pStr;
			my $pai = MahjongPai->new();
			$pai->str($ps[0] . $ps[1]);
			$self->pushYama($pai);
		}
	}
	$self->clearTedumi();
}

sub diceOffset {
	my $self = shift;
	my $offset = shift;
	my @offsetCut = splice @{$self->{Yama}}, 0, $offset;
	push @{$self->{Yama}}, @offsetCut;
}

sub round {
	my $self = shift;
	if (@_) {
		$self->{Round} = shift;
	}
	return $self->{Round};
}

sub tsumikomi {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if ($i < 0 || $i >= @{$self->{Tsumikomi}}) {
			return undef;
		}
		if (!defined($x)) {
			return ${$self->{Tsumikomi}}[$i];
		}
		${$self->{Tsumikomi}}[$i] = $x;
	}
	return $self->{Tsumikomi};
}

sub toString {
	my $self = shift;
	my $ret = $self->kanNum() . ':';
	$ret .= join "", (map { $_->str() } @{$self->yama()});
	$ret .= ':' . join "&", @{$self->tedumiRest()};
	$ret .= ':' . join "<>", (map { defined($_) ? join "&", @{$_} : "" } @{$self->tedumiYamas()});
	$ret .= ':' . $self->round();
	$ret .= ':' . join "&", @{$self->tsumikomi()};
	return $ret;
}

sub setAll {
	my $self = shift;
	my $str = shift;
	chomp $str;
	my ($kanNum, $yamaStr, $tedumiRest, $tedumiYamas, $round, $tsumikomi) = split /:/, $str;
	my @split_str = split //, $yamaStr;
	$self->kanNum($kanNum);
	$self->clearYama();
	my $i = 0;
	while ($i < @split_str) {
		my $pai = MahjongPai->new();
		$pai->str($split_str[$i] . $split_str[$i+1]);
		$self->pushYama($pai);
		$i += 2;
	}
	@{$self->tedumiRest()} = split /&/, $tedumiRest;
	@{$self->tedumiYamas()} = map { [split /&/, $_] } split /<>/, $tedumiYamas;
	$self->round($round);
	@{$self->tsumikomi()} = split /&/, $tsumikomi;
}

# @deprecated
sub TO_JSON {
	my $self = shift;
	my @doras = $self->getDoraStrs();
	my %self_hash = (
		'Dora' => \@doras,
		'RestNum' => $self->getRest(),
		'KanNum' => $self->kanNum(),
		'TedumiRest' => $self->tedumiRest(),
		'TedumiYamas' => $self->tedumiYamas(),
		'Round' => $self->round(),
		'Tsumikomi' => $self->tsumikomi()
	);
	return {%self_hash};
}

1;