#!/usr/local/bin/perl --
package MahjongGame;
use strict;
use warnings;
use MahjongYama;
use MahjongPai;
use MahjongTehai;
use MahjongHo;
use MahjongAi;
use MahjongPlayerInfo;
use JSON;
use Digest::MD5 qw(md5_hex);

#====================================
# constructor
#====================================
sub new {
	my $clazz = shift;
	my $self = {
		Tehais => [],
		Hos => [],
		Points => [],
		PlayerNames => [],
		Yama => MahjongYama->new(),
		Round => -1,
		Continuous => 0,
		Turn => 0,
		Phase => 0,
		MemberNum => 4,
		RoundSets => 1,
		LatestDrop => undef,
		KanPai => undef,
		DropPos => -1,
		FinishFlags => [],
		TsumoFlag => 0,
		Kyotaku => 0,
		IppatsuFlag => [0, 0, 0, 0],
		ReachHassei => -1,
		PlayerNoHuro => [0, 0, 0, 0],
		PlayerHuroType => [-2, -2, -2, -2],
		PlayerAutoFinish => [0, 0, 0, 0],
		PlayerIsFinish => [0, 0, 0, 0],
		WaitPlayer => [0, 0, 0, 0],
		MinogashiFlag => [0, 0, 0, 0],
		SpectatorClose => [0, 0, 0, 0],
		ViewPoint => -1,
		Comment => '',
		Tedumi => 1,
	};
	return bless $self, $clazz;
}

#====================================
# accesseor
#====================================
sub tehais {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if ($i < 0 || $i >= @{$self->{Tehais}}) {
			return undef;
		}
		if (!defined($x)) {
			return ${$self->{Tehais}}[$i];
		}
		${$self->{Tehais}}[$i] = $x;
	}
	return $self->{Tehais};
}

sub clearTehais {
	my $self = shift;
	@{$self->{Tehais}} = ();
}

sub hos {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Hos}}[$i];
		}
		${$self->{Hos}}[$i] = $x;
	}
	return $self->{Hos};
}

sub clearHos {
	my $self = shift;
	@{$self->{Hos}} = ();
}

sub points {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Points}}[$i];
		}
		${$self->{Points}}[$i] = $x;
	}
	return $self->{Points};
}

sub playerNames {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{PlayerNames}}[$i];
		}
		${$self->{PlayerNames}}[$i] = $x;
	}
	return $self->{PlayerNames};
}

sub clearPlayerNames {
	my $self = shift;
	@{$self->{PlayerNames}} = ();
}

sub clearPoints {
	my $self = shift;
	@{$self->{Points}} = ();
}

sub yama {
	my $self = shift;
	if (@_) {
		$self->{Yama} = shift;
	}
	return $self->{Yama};
}

sub round {
	my $self = shift;
	if (@_) {
		$self->{Round} = shift;
	}
	return $self->{Round};
}

sub continuous {
	my $self = shift;
	if (@_) {
		$self->{Continuous} = shift;
	}
	return $self->{Continuous};
}

sub turn {
	my $self = shift;
	if (@_) {
		$self->{Turn} = shift;
	}
	return $self->{Turn};
}

sub phase {
	my $self = shift;
	if (@_) {
		$self->{Phase} = shift;
	}
	return $self->{Phase};
}

sub memberNum {
	my $self = shift;
	if (@_) {
		$self->{MemberNum} = shift;
	}
	return $self->{MemberNum};
}

sub roundSets {
	my $self = shift;
	if (@_) {
		$self->{RoundSets} = shift;
	}
	return $self->{RoundSets};
}

sub autoPlayMode {
	my $self = shift;
	if (@_) {
		$self->{AutoPlayMode} = shift;
	}
	return $self->{AutoPlayMode};
}

sub ai {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		$self->{Ai} = shift;
	}
	return $self->{Ai};
}

sub latestDrop {
	my $self = shift;
	if (@_) {
		$self->{LatestDrop} = shift;
	}
	return $self->{LatestDrop};
}

sub kanPai {
	my $self = shift;
	if (@_) {
		$self->{KanPai} = shift;
	}
	return $self->{KanPai};
}

sub dropPos {
	my $self = shift;
	if (@_) {
		$self->{DropPos} = shift;
	}
	return $self->{DropPos};
}

sub finishFlags {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{FinishFlags}}[$i];
		}
		${$self->{FinishFlags}}[$i] = $x;
	}
	return $self->{FinishFlags};
}

sub clearFinishFlags {
	my $self = shift;
	@{$self->{FinishFlags}} = ();
}

sub tsumoFlag {
	my $self = shift;
	if (@_) {
		$self->{TsumoFlag} = shift;
	}
	return $self->{TsumoFlag};
}

sub kyotaku {
	my $self = shift;
	if (@_) {
		$self->{Kyotaku} = shift;
	}
	return $self->{Kyotaku};
}

sub ippatsuFlag {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{IppatsuFlag}}[$i];
		}
		${$self->{IppatsuFlag}}[$i] = $x;
	}
	return $self->{IppatsuFlag};
}

sub reachHassei {
	my $self = shift;
	if (@_) {
		$self->{ReachHassei} = shift;
	}
	return $self->{ReachHassei};
}

sub playerNoHuro {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{PlayerNoHuro}}[$i];
		}
		${$self->{PlayerNoHuro}}[$i] = $x;
	}
	return $self->{PlayerNoHuro};
}

sub playerHuroType {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{PlayerHuroType}}[$i];
		}
		${$self->{PlayerHuroType}}[$i] = $x;
	}
	return $self->{PlayerHuroType};
}

sub isAllNoHuro {
	my $self = shift;
	for my $h (@{$self->{PlayerHuroType}}) {
		if ($h != -3) {
			return 0;
		}
	}
	return 1;
}

sub playerAutoFinish {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{PlayerAutoFinish}}[$i];
		}
		${$self->{PlayerAutoFinish}}[$i] = $x;
	}
	return $self->{PlayerAutoFinish};
}

sub playerIsFinish {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{PlayerIsFinish}}[$i];
		}
		${$self->{PlayerIsFinish}}[$i] = $x;
	}
	return $self->{PlayerIsFinish};
}

sub waitPlayer {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{WaitPlayer}}[$i];
		}
		${$self->{WaitPlayer}}[$i] = $x;
	}
	for my $w (@{$self->{WaitPlayer}}) {
		if ($w) {
			return 1;
		}
	}
	return 0;
}

sub waitCancel {
	my $self = shift;
	@{$self->{WaitPlayer}} = (0, 0, 0, 0);
}

sub minogashiFlag {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{MinogashiFlag}}[$i];
		}
		${$self->{MinogashiFlag}}[$i] = $x;
	}
	return $self->{MinogashiFlag};
}

sub spectorClose {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{SpectorClose}}[$i];
		}
		${$self->{SpectorClose}}[$i] = $x;
	}
	return $self->{SpectorClose};
}

sub md5 {
	my $self = shift;
	my $coder = JSON->new->utf8->convert_blessed;
	return md5_hex($coder->encode($self));
}

sub viewPoint {
	my $self = shift;
	if (@_) {
		$self->{ViewPoint} = shift;
	}
	return $self->{ViewPoint};
}

sub tedumi {
	my $self = shift;
	if (@_) {
		$self->{Tedumi} = shift;
	}
	return $self->{Tedumi};
}

#====================================
# public method
#====================================
sub play {
	my $self = shift;
	my %ret = ();
	$self->waitCancel();
	if ($self->phase() == 0) {
		# 上がりチェック
		for my $tehai (@{$self->tehais()}) {
			$tehai->sortTehai();
		}
		
		for my $i (0..3) {
			my $check_pos = ($self->turn() + $i) % 4;
			my $isRon = $self->isRon($check_pos);
			if ($isRon != -1) {
				if ($isRon == 1) {
					if (!grep {$_ eq $check_pos} @{$self->finishFlags()}) {
						push @{$self->finishFlags()}, $check_pos;
					}
					@{$self->finishFlags()} = keys %{{map {$_ => 1} @{$self->finishFlags()}}};
				}
			} else {
				$self->waitPlayer($check_pos, 2);
			}
		}
		# ツモ前処理
		if (!$self->waitPlayer()) {
			my @finishFlags = @{$self->finishFlags()};
			if ($self->yama()->isEnd() || @finishFlags > 0) {
				%ret = $self->endRound();
			} else {
				if ($self->reachHassei() != -1) {
					$self->hos($self->reachHassei())->reach();
					$self->ippatsuFlag($self->reachHassei(), 1);
					$self->pointAdd($self->reachHassei(), -1000);
					$self->reachHassei(-1);
				}
				for my $i (0..3) {
					my $position = (8 + $self->turn() - 2 - $i) % 4;
					my $isEat = $self->isEat($position);
					if ($isEat != -2) {
						if ($isEat >= -1) {
							for my $j (0..3) {
								$self->ippatsuFlag($i, 0);
							}
						}
					} else {
						$self->waitPlayer($position, 1);
					}
				}
				if (!$self->waitPlayer()) {
					if (!defined($self->latestDrop()) || $self->isAllNoHuro()) {
						$self->phase(1);
					} else {
						for my $i (0..3) {
							if ($self->playerHuroType($i) >= -1) {
								$self->eatPai($i);
							}
						}
					}
				}
			}
		}
	} elsif ($self->phase() == 1) {
		if ($self->minogashiFlag($self->turn()) && $self->hos($self->turn())->reachAt() != -1) {
			$self->minogashiFlag($self->turn(), 0);
		}
		$self->playerTempFlagReset();
		$self->drawPai();
	} elsif ($self->phase() == 2) {
		if (defined($self->kanPai())) {
			my @hist = $self->tehais($self->turn())->toHistogram();
			my $is_ankan = $hist[MahjongPai::strToNum($self->kanPai()->str())] == 4;
			my $is_kakan = 0;
			if ($hist[MahjongPai::strToNum($self->kanPai()->str())] == 1) {
				for my $naki ($self->tehais($self->turn())->naki()) {
					if ($naki->isPon() && $naki->pai1()->str() eq $self->kanPai()->str()) {
						$is_kakan = 1;
					}
				}
			}
			if ($is_ankan) {
				$self->tehais($self->turn())->ankan($self->kanPai());
				my $rinshan = $self->yama()->kan();
				$self->tehais($self->turn())->add($rinshan);
			} elsif ($is_kakan) {
				$self->tehais($self->turn())->kakan($self->kanPai());
				my $rinshan = $self->yama()->kan();
				$self->tehais($self->turn())->add($rinshan);
			}
			$self->kanPai(undef);
		} else {
			if ($self->points($self->turn())->name() =~ /dummy/) {
				%ret = $self->autoPlay();
			}
		}
	}
	return %ret;
}

sub dropPai {
	my $self = shift;
	my $position = shift;
	my $pai_index = shift;
	if (!defined($position)) {
		return;
	}
	if ($position < 0 || $position >= 4) {
		return;
	}
	if (!$self->tehais($position)->isKiriban()) {
		return;
	}
	if ($self->ippatsuFlag($position)) {
		$self->ippatsuFlag($position, 0);
	}
	if ($self->hos($position)->reachAt() != -1) {
		$pai_index = 13;
	}
	my $pai = $self->tehais($position)->drop($pai_index);
	$self->latestDrop($pai);
	$self->dropPos($position);
	$self->hos($position)->addHo($pai->str());
	$self->phase(0);
	my $turn = $self->turn();
	$turn++;
	if ($turn >= 4) {
		$turn = 0;
	}
	$self->turn($turn);
}

sub noEat {
	my $self = shift;
	my $position = shift;
	if (!defined($position)) {
		return;
	}
	$self->eat($position, -3);
}

sub eat {
	my $self = shift;
	my $position = shift;
	my $type = shift;
	if (!defined($position)) {
		return;
	}
	if ($self->turn() != ($position + 1) % 4 && ${$self->playerHuroType()}[$position] == -2) {
		$self->playerHuroType($position, $type);
	}
	$self->waitCancel();
}

sub kan {
	my $self = shift;
	my $position = shift;
	my $index = shift;
	if (!defined($position)) {
		return;
	}
	if ($self->turn() == $position && $self->tehais($position)->isKiriban()) {
		my @kanable = $self->tehais($position)->getKanable();
		if ($index >= 0 && $index < @kanable) {
			$self->kanPai($kanable[$index]);
		}
	}
	$self->waitCancel();
}

sub reach {
	my $self = shift;
	my $position = shift;
	if (!defined($position)) {
		return;
	}
	if ($self->hos($position)->reachAt() == -1) {
		$self->reachHassei($position);
	}
	$self->waitCancel();
}

sub hora {
	my $self = shift;
	my $position = shift;
	if (!defined($position)) {
		return ();
	}
	if ($self->phase() == 2 && $self->turn() == $position) {
		my $tehai = $self->tehais($position)->clone();
		if ($tehai->calcShanten() == -1) {
			$tehai->tsumoFlag(1);
			my @point = $tehai->calcPoint(&roundToBa($self->round()), &roundAndPositionToKaze($self->round(), $position));
			
			if ($point[1] > 0) {
				push @{$self->finishFlags()}, $position;
				$self->tsumoFlag(1);
				$self->waitCancel();
				my %ret = $self->endRound();
				return %ret;
			} else {
				$self->chonbo($position);
				return ('Mes' => 'チョンボ');
			}
		}
	} else {
		$self->playerIsFinish($position, 1);
		$self->waitCancel();
	}
}

sub noHuro {
	my $self = shift;
	my $position = shift;
	if (!defined($position)) {
		return;
	}
	$self->playerNoHuro($position, !$self->playerNoHuro($position));
}

sub startGame {
	my $self = shift;
	my @player_names = @{$self->playerNames()};
	if (@player_names != 4) {
		return;
	}
	$self->round(0);
	$self->continuous(0);
	$self->clearPoints();
	my $position = 0;
	for my $name (@player_names) {
		my $player_info = MahjongPlayerInfo->new();
		$player_info->position($position);
		$player_info->name($name);
		$position++;
		push @{$self->points()}, $player_info;
	}
	$self->startRound();
}

sub participate {
	my $self = shift;
	my $name = shift;
	if (@{$self->playerNames()} < 4) {
		for my $n (@{$self->playerNames()}) {
			if ($n eq $name) {
				return;
			}
		}
		push @{$self->playerNames()}, $name;
	}
}

sub cancelParticipate {
	my $self = shift;
	my $name = shift;
	my $i = 0;
	for my $n (@{$self->playerNames()}) {
		if ($name eq $n) {
			splice @{$self->playerNames()}, $i, 1;
		}
		$i++;
	}
}

sub nameToPosition {
	my $self = shift;
	my $name = shift;
	my $i = 0;
	if ($self->isPlaying()) {
		for my $n (@{$self->points()}) {
			if ($name eq $n->name()) {
				return $i;
			}
			$i++;
		}
	} else {
		for my $n (@{$self->playerNames()}) {
			if ($name eq $n) {
				return $i;
			}
			$i++;
		}
	}
	return undef;
}

sub isReady {
	my $self = shift;
	return (@{$self->playerNames()} == 4 && $self->viewPoint() == 0);
}

sub isPlaying {
	my $self = shift;
	return ($self->round() != -1);
}

sub setObserver {
	my $self = shift;
	my $name = shift;
	my $pos = $self->nameToPosition($name);
	if (defined($pos)) {
		$self->viewPoint($pos);
	} else {
		$self->viewPoint(-1);
	}
}

sub sipaiTedumi {
	my $self = shift;
	my $position = shift;
	my $getStr = shift;
	my %ret = ();
	if ($self->phase() != -1) {
		return %ret;
	}
	if (!defined($position)) {
		return %ret;
	}
	if ($position < 0 || $position >= 4) {
		return %ret;
	}
	
	$self->yama()->restToYama($position, $getStr);
	
	if ($position == 0) {
		for my $i (0..3) {
			if ($self->points($i)->name() =~ /dummy/) {
				$self->yama()->randomGet($i);
			}
		}
	}
	if ($self->yama()->isTedumiEnd()) {
		$self->yama()->tedumiTerminate($self->round() % 4);
		$ret{startDice} = $self->deal();
	}
	
	return %ret;
}

sub tsumikomiSet {
	my $self = shift;
	my $position = shift;
	my $type = shift;
	if ($self->phase() != -1) {
		return;
	}
	if (!defined($position)) {
		return;
	}
	if ($position < 0 || $position >= 4) {
		return;
	}
	
	$self->yama()->tsumikomi($position, $type);
	
	return;
}

#====================================
# private method
#====================================
sub playerTempFlagReset {
	my $self = shift;
	$self->waitCancel();
	for my $i (0..3) {
		$self->playerIsFinish($i, -1);
		$self->playerHuroType($i, -2);
	}
}

sub allFlagReset {
	my $self = shift;
	$self->latestDrop(undef);
	$self->clearFinishFlags();
	$self->dropPos(-1);
	$self->tsumoFlag(0);
	$self->reachHassei(-1);
	$self->kanPai(undef);
	for my $i (0..3) {
		$self->ippatsuFlag($i, 0);
		$self->playerNoHuro($i, 0);
		$self->playerAutoFinish($i, 0);
		$self->minogashiFlag($i, 0);
		$self->spectorClose($i, 0);
	}
	$self->playerTempFlagReset();
}

sub startRound {
	my $self = shift;
	$self->allFlagReset();
	$self->clearTehais();
	$self->clearHos();
	for my $position (0..3) {
		my $tehai = MahjongTehai->new();
		$tehai->position($position);
		push @{$self->tehais()}, $tehai;
		
		my $ho = MahjongHo->new();
		$ho->position($position);
		push @{$self->hos()}, $ho;
	}
	
	$self->yama(MahjongYama->new());
	if ($self->tedumi()) {
		$self->phase(-1);
		$self->yama()->beginTedumi($self->round());
	} else {
		$self->yama()->setDefault();
		
		$self->deal();
	}
}

sub deal {
	my $self = shift;
	
	my $dice = int(rand(6)) + int(rand(6)) + 2;
	my $diceStr = '';
	my $diceOffset = 0;
	
	if ($dice % 4 == 1) {
		$diceStr = '自' . $dice;
		$diceOffset = 0 + $dice * 2;
	} elsif ($dice % 4 == 2) {
		$diceStr = '右' . $dice;
		$diceOffset = 102 + $dice * 2;
	} elsif ($dice % 4 == 3) {
		$diceStr = '対' . $dice;
		$diceOffset = 68 + $dice * 2;
	} else {
		$diceStr = '左' . $dice;
		$diceOffset = 34 + $dice * 2;
	}
	
	$self->yama()->diceOffset($diceOffset);
	
	for my $i (0..2) {
		for my $j (0..3) {
			my $jj = ($self->round() + $j) % 4;
			for my $k (0..3) {
				$self->tehais($jj)->add($self->yama()->draw());
			}
		}
	}
	
	for my $j (0..3) {
		my $jj = ($self->round() + $j) % 4;
		$self->tehais($jj)->add($self->yama()->draw());
	}
	
	$self->phase(2);
	$self->turn($self->round() % 4);
	$self->tehais($self->turn())->add($self->yama()->draw());
	
	for my $i (0..3) {
		$self->tehais($i)->sortTehai();
	}
	
	return $diceStr;
}

sub endRound {
	my $self = shift;
	my %ret = (
		'Mes' => 'dummy',
		'Mes2' => '',
	);
	my @finish_flags = @{$self->finishFlags()};
	if (@finish_flags > 0) {
		if (@finish_flags > 1) {
			my @valid_list = ();
			for my $flag (@finish_flags) {
				my $tehai = $self->tehais($flag)->clone();
				$tehai->reach($self->hos($flag)->reachAt() != -1);
				
				my @point = $tehai->calcPoint(&roundToBa($self->round()), &roundAndPositionToKaze($self->round(), $flag));
				if ($point[1] > 0 && !$self->isFuriten($flag) && !$self->minogashiFlag($flag)) {
					push @valid_list, $flag;
				}
			}
			@finish_flags = @valid_list;
		}
		
		if (@finish_flags == 3) {
			$ret{Mes} = '三家和';
			$self->roundIncrement();
		} elsif (@finish_flags == 2) {
			my $pos1 = ($self->dropPos() + 4 - $finish_flags[0]) % 4;
			my $pos2 = ($self->dropPos() + 4 - $finish_flags[1]) % 4;
			my $finish = $finish_flags[0];
			if ($pos1 < $pos2) {
				$finish = $finish_flags[1];
			}
			my $tehai = $self->tehais($finish);
			$tehai->add($self->latestDrop());
			
			my $reach = $self->hos($finish)->reachAt() != -1;
			$tehai->reachFlag($reach);
			if ($reach) {
				$tehai->doubleReachFlag($self->hos($finish)->reachAt() == 0);
			}
			
			$tehai->setDoras($self->yama()->getAllDora($reach));
			
			$tehai->ippatsuFlag($self->ippatsuFlag($finish));
			
			my @point = $tehai->calcPoint(&roundToBa($self->round()), &roundAndPositionToKaze($self->round(), $finish));
			
			$self->pointAdd($finish, $point[1] + $self->kyotaku());
			$self->pointAdd($self->dropPos(), -1 * $point[1]);
			$self->kyotaku(0);
			
			$ret{Mes} = '頭ハネ &mahjong(' . $tehai->toString() . ')';
			my $dora_str = '';
			for my $dora (@{$tehai->doras()}) {
				$dora_str .= $dora->str();
			}
			$ret{Mes2} = 'ドラ&mahjong(' . $dora_str . ')' . $point[2] . ' ' . $point[3] . $point[1];
			if ($point[4]) {
				$ret{Yakuman} = pack 'H*', $self->points($finish)->name();
			}
			if ($self-round() % 4 != $finish) {
				$self->roundIncrement();
			}
		} else {
			my $finish = ${$self->finishFlags()}[0];
			my $tehai = $self->tehais($finish);
			
			my $reach = $self->hos($finish)->reachAt() != -1;
			$tehai->reachFlag($reach);
			if ($reach) {
				$tehai->doubleReachFlag($self->hos($finish)->reachAt() == 0);
			}
			
			$tehai->setDoras($self->yama()->getAllDora($reach));
			
			$tehai->ippatsuFlag($self->ippatsuFlag($finish));
			
			if ($self->tsumoFlag) {
				$tehai->tsumoFlag(1);
				
				my @point = $tehai->calcPoint(&roundToBa($self->round()), &roundAndPositionToKaze($self->round(), $finish));
				if ($point[1] > 0) {
					if ($self->round() % 4 != $finish) {
						$self->pointAdd($finish, $point[1] + $point[0] * 2 + $self->kyotaku());
						$self->kyotaku(0);
						for my $i (0..3) {
							if ($i != $finish) {
								if ($self->round() % 4 != $i) {
									$self->pointAdd($i, -1 * $point[1]);
								} else {
									$self->pointAdd($i, -1 * $point[0]);
								}
							}
						}
						$ret{Mes} = 'ツモ &mahjong(' . $tehai->toString() . ')';
						$ret{Finish} = $self->points($finish);
						$ret{Drop} = undef;
						my $dora_str = '';
						for my $dora (@{$tehai->doras()}) {
							$dora_str .= $dora->str();
						}
						$ret{Mes2} = 'ドラ&mahjong(' . $dora_str . ')' . $point[2] . ' ' . $point[3] . $point[0] . ' ' . $point[1];
						$self->roundIncrement();
					} else {
						$self->pointAdd($finish, $point[1] * 3 + $self->kyotaku());
						$self->kyotaku(0);
						for my $i (0..3) {
							if ($i != $finish) {
								$self->pointAdd($i, -1 * $point[1]);
							}
						}
						$ret{Mes} = 'ツモ &mahjong(' . $tehai->toString() . ')';
						$ret{Finish} = $self->points($finish);
						$ret{Drop} = undef;
						my $dora_str = '';
						for my $dora (@{$tehai->doras()}) {
							$dora_str .= $dora->str();
						}
						$ret{Mes2} = 'ドラ&mahjong(' . $dora_str . ')' . $point[2] . ' ' . $point[3] . $point[1] . 'オール';
					}
					if ($point[4]) {
						$ret{Yakuman} = pack 'H*', $self->points($finish)->name();
					}
				} else {
					$self->chonbo($finish);
					$ret{Mes} = 'チョンボ';
				}
			} else {
				if ($tehai->isTsumoban()) {
					$tehai->add($self->latestDrop());
				}
				
				my @point = $tehai->calcPoint(&roundToBa($self->round()), &roundAndPositionToKaze($self->round(), $finish));
				
				if ($point[1] > 0 && !$self->isFuriten($finish) && !$self->minogashiFlag($finish)) {
					$self->pointAdd($finish, $point[1] + $self->kyotaku());
					$self->pointAdd($self->dropPos(), -1 * $point[1]);
					
					$ret{Mes} = 'ロン &mahjong(' . $tehai->toString() . ')';
					$ret{Finish} = $self->points($finish);
					$ret{Drop} = $self->points($self->dropPos());
					my $dora_str = '';
					for my $dora (@{$tehai->doras()}) {
						$dora_str .= $dora->str();
					}
					$ret{Mes2} = 'ドラ&mahjong(' . $dora_str . ')' . $point[2] . ' ' . $point[3] . $point[1];
					if ($point[4]) {
						$ret{Yakuman} = pack 'H*', $self->points($finish)->name();
					}
					if ($self->round() % 4 != $finish) {
						$self->roundIncrement();
					}
				} else {
					$self->chonbo($finish);
					$ret{Mes} = 'チョンボ';
				}
			}
		}
	} else {
		my @shantens = ();
		for my $i (0..3) {
			push @shantens, $self->tehais($i)->calcShanten();
		}
		my $tenpais = 0;
		for my $shanten (@shantens) {
			if ($shanten == 0) {
				$tenpais++;
			}
		}
		my $tenpai_point = 0;
		my $no_tenpai_point = 0;
		if ($tenpais == 3) {
			$tenpai_point = 1000;
			$no_tenpai_point = -3000;
		} elsif ($tenpais == 2) {
			$tenpai_point = 1500;
			$no_tenpai_point = -1500;
		} elsif ($tenpais == 1) {
			$tenpai_point = 3000;
			$no_tenpai_point = -1000;
		}
		for my $i (0..3) {
			if ($shantens[$i] == 0) {
				$self->pointAdd($i, $tenpai_point);
			} else {
				$self->pointAdd($i, $no_tenpai_point);
			}
		}
		if ($shantens[$self->round() % 4] != 0) {
			$self->roundIncrement();
		}
		$ret{Mes} = '流局';
	}
	
	my $tobi = 0;
	for my $i (0..3) {
		if ($self->points($i)->point() < 0) {
			$tobi = 1;
		}
	}
	if ($self->round() >= $self->roundSets() * 4 || $tobi) {
		($ret{EndMes}, $ret{Pos0}, $ret{Pos1}, $ret{Pos2}, $ret{Pos3}) = $self->endGame();
	} else {
		$self->startRound();
	}
	return %ret;
}

sub endGame {
	my $self = shift;
	my @ret = ('ゲーム終了', $self->points(0), $self->points(1), $self->points(2), $self->points(3));
	$self->round(-1);
	$self->viewPoint(-1);
	$self->clearPlayerNames();
	return @ret;
}

sub drawPai {
	my $self = shift;
	my $pai = $self->yama()->draw();
	$self->tehais($self->turn())->add($pai);
	$self->phase(2);
}

sub eatPai {
	my $self = shift;
	my $pos = shift;
	my $eat_pos = ($self->turn() + 3) % 4;
	$self->hos($eat_pos)->eat();
	
	if ($self->playerHuroType($pos) < 2) {
		$self->tehais($pos)->chi($self->latestDrop(), $self->playerHuroType($pos));
	} elsif ($self->playerHuroType($pos) == 3) {
		$self->tehais($pos)->minkan($self->latestDrop(), ($eat_pos - $pos + 4) % 4);
		my $rinshan = $self->yama()->kan();
		$self->tehais($pos)->add($rinshan);
	} else {
		$self->tehais($pos)->pon($self->latestDrop(), ($eat_pos - $pos + 4) % 4);
	}
	$self->phase(2);
	$self->turn($pos);
	$self->playerTempFlagReset();
	$self->latestDrop(undef);
}

sub isEat {
	my $self = shift;
	my $pos = shift;
	if ($self->hos($pos)->reachAt() != -1 || $self->playerNoHuro($pos)) {
		$self->playerHuroType($pos, -3);
		return $self->playerHuroType($pos);
	}
	if (($self->turn() + 3) % 4 == $pos) {
		$self->playerHuroType($pos, -3);
		return $self->playerHuroType($pos);
	}
	if ($self->points($pos)->name() !~ /dummy/) {
		my @hist = $self->tehais($pos)->toHistogram();
		my $can_eat = 0;
		if ($self->turn() == $pos && $self->latestDrop()->getType() ne 'z') {
			my $num = $self->latestDrop()->getNum();
			
			my $m2 = $num >= 3 ? MahjongPai::strToNum($self->latestDrop()->getType() . ($num - 2)) : 'u0';
			my $m1 = $num >= 2 ? MahjongPai::strToNum($self->latestDrop()->getType() . ($num - 1)) : 'u0';
			my $p1 = $num <= 8 ? MahjongPai::strToNum($self->latestDrop()->getType() . ($num + 1)) : 'u0';
			my $p2 = $num <= 7 ? MahjongPai::strToNum($self->latestDrop()->getType() . ($num + 2)) : 'u0';
			if ($num >= 3 && $hist[$m2] > 0 && $hist[$m1] > 0) {
				$can_eat = 1;
			}
			if ($num >= 2 && $num <= 8 && $hist[$m1] > 0 && $hist[$p1] > 0) {
				$can_eat = 1;
			}
			if ($num <= 7 && $hist[$p1] > 0 && $hist[$p2] > 0) {
				$can_eat = 1;
			}
		}
		if ($hist[MahjongPai::strToNum($self->latestDrop()->str())] >= 2) {
			$can_eat = 1;
		}
		
		if (!$can_eat) {
			$self->playerHuroType($pos, -3);
		}
		return $self->playerHuroType($pos);
	} else {
		my $ai = $self->getAi($pos);
		$self->playerHuroType($pos, $ai->selectEat());
		return $self->playerHuroType($pos);
	}
}

sub isRon {
	my $self = shift;
	my $pos = shift;
	if ($self->turn() == ($pos + 1) % 4) {
		return 0;
	}
	my $tehai = $self->tehais($pos)->clone();
	$tehai->add($self->latestDrop());
	if ($self->points($pos)->name() !~ /dummy/) {
		$tehai->reachFlag($self->hos($pos)->reachAt() != -1);
		if ($tehai->calcShanten() == -1) {
			if ($self->playerIsFinish($pos) == 0) {
				$self->minogashiFlag($pos, 1);
			}
			return $self->playerIsFinish($pos);
		}
		if ($self->playerIsFinish($pos) != -1) {
			return $self->playerIsFinish($pos);
		}
		return 0;
	} else {
		my $ai = $self->getAi($pos);
		my $result = $ai->isRon();
		
		if ($tehai->calcShanten() == -1 && !$result) {
			$self->minogashiFlag($pos, 1);
		}
		return $result;
	}
}

sub isFuriten {
	my $self = shift;
	my $pos = shift;
	my @ho = $self->hos($pos);
	my @agari = $self->tehais($pos)->getMachi();
	for my $sute (@ho) {
		for my $machi (@agari) {
			if ($sute->str() eq $machi->str()) {
				return 1;
			}
		}
	}
	return 0;
}

sub chonbo {
	my $self = shift;
	my $pos = shift;
	if ($self->round() % 4 == $pos) {
		for my $i (0..3) {
			if ($i == $pos) {
				$self->pointAdd($i, -12000);
			} else {
				$self->pointAdd($i, 4000);
			}
		}
	} else {
		for my $i (0..3) {
			if ($i == $pos) {
				$self->pointAdd($i, -8000);
			} else {
				if ($self->round() % 4 == $i) {
					$self->pointAdd($i, 4000);
				} else {
					$self->pointAdd($i, 2000);
				}
			}
		}
	}
}

sub pointAdd {
	my $self = shift;
	my $pos = shift;
	my $point = shift;
	$self->points($pos)->pointAdd($point);
}

sub roundToBa {
	my $round = shift;
	return MahjongPai::numToStr(27 + int($round / 4));
}

sub roundAndPositionToKaze {
	my $round = shift;
	my $position = shift;
	return MahjongPai::numToStr(27 + ((8 - $round + $position) % 4));
}

sub tehaisJson {
	my $self = shift;
	my $vp = shift;
	if (!defined($vp)) {
		$vp = $self->viewPoint();
	}
	my @tehais = ();
	for my $i (0..3) {
		if ($vp == -1) {
			my $tehai = $self->tehais($i);
			if (defined($tehai) && $self->spectorClose($i)) {
				$tehai = $tehai->hide();
			}
			push @tehais, $tehai;
		} else {
			my $pos = (4 + $i + $vp) % 4;
			my $tehai = $self->tehais($pos);
			if ($i != 0 && defined($tehai)) {
				$tehai = $tehai->hide();
			}
			push @tehais, $tehai;
		}
	}
	return \@tehais;
}

sub hosJson {
	my $self = shift;
	my $vp = shift;
	if (!defined($vp)) {
		$vp = $self->viewPoint();
	}
	my @hos = ();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $ho = $self->hos($pos);
		push @hos, $ho;
	}
	return \@hos;
}

sub playerNamesJson {
	my $self = shift;
	my $vp = shift;
	if (!defined($vp)) {
		$vp = $self->viewPoint();
	}
	my @playerNames = ();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = $self->round() == -1 ? $i : (4 + $i + $vp) % 4;
		my $playerName = $self->playerNames($pos);
		push @playerNames, $playerName;
	}
	return \@playerNames;
}

sub pointsJson {
	my $self = shift;
	my $vp = shift;
	if (!defined($vp)) {
		$vp = $self->viewPoint();
	}
	my @points = ();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $point = $self->points($pos);
		push @points, $point;
	}
	return \@points;
}

sub playerNoHuroJson {
	my $self = shift;
	my @playerNoHuros = ();
	my $vp = $self->viewPoint();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $playerNoHuro = $self->playerNoHuro($pos);
		push @playerNoHuros, $playerNoHuro;
	}
	return \@playerNoHuros;
}

sub playerHuroTypeJson {
	my $self = shift;
	my @playerHuroTypes = ();
	my $vp = $self->viewPoint();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $playerHuroType = $self->playerHuroType($pos);
		push @playerHuroTypes, $playerHuroType;
	}
	return \@playerHuroTypes;
}

sub playerAutoFinishJson {
	my $self = shift;
	my @playerAutoFinishs = ();
	my $vp = $self->viewPoint();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $playerAutoFinish = $self->playerAutoFinish($pos);
		push @playerAutoFinishs, $playerAutoFinish;
	}
	return \@playerAutoFinishs;
}

sub playerIsFinishJson {
	my $self = shift;
	my @playerIsFinishs = ();
	my $vp = $self->viewPoint();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		my $playerIsFinish = $self->playerIsFinish($pos);
		push @playerIsFinishs, $playerIsFinish;
	}
	return \@playerIsFinishs;
}

sub waitPlayerJson {
	my $self = shift;
	my @waitPlayers = ();
	my $vp = $self->viewPoint();
	if ($vp == -1) {
		$vp = 0;
	}
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		push @waitPlayers, $self->waitPlayer($pos);
	}
	return \@waitPlayers;
}

sub yamaJson {
	my $self = shift;
	my $vp = shift;
	if (!defined($vp)) {
		$vp = $self->viewPoint();
	}
	if ($vp == -1) {
		$vp = 0;
	}
	my @tedumiYamas = ();
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		push @tedumiYamas, $self->yama()->tedumiYamas($pos);
	}
	my @tsumikomi = ();
	for my $i (0..3) {
		my $pos = (4 + $i + $vp) % 4;
		push @tsumikomi, $self->yama()->tsumikomi($pos);
	}
	my @doras = $self->yama()->getDoraStrs();
	my %yamaHash = (
		'Dora' => \@doras,
		'RestNum' => $self->yama()->getRest(),
		'KanNum' => $self->yama()->kanNum(),
		'TedumiRest' => $self->yama()->tedumiRest(),
		'TedumiYamas' => \@tedumiYamas,
		'Round' => $self->yama()->round(),
		'Tsumikomi' => \@tsumikomi
	);
	return \%yamaHash;
}

sub roundIncrement {
	my $self = shift;
	
	$self->round($self->round() + 1);
}

sub getAi {
	my $self = shift;
	my $pos = shift;
	my %self_hash = (
		'Tehais' => $self->tehaisJson($pos),
		'Hos' => $self->hosJson($pos),
		'Points' => $self->pointsJson($pos),
		'Yama' => $self->yama(),
		'Round' => $self->round(),
		'Continuous' => $self->continuous(),
		'Turn' => $self->turn(),
		'Phase' => $self->phase(),
		'RoundSets' => $self->roundSets(),
		'LatestDrop' => $self->latestDrop(),
		'DropPos' => $self->dropPos(),
		'Kyotaku' => $self->kyotaku(),
	);
	my $ai = MahjongAi->new();
	for my $tehai (@{$self->tehaisJson($pos)}) {
		push @{$ai->tehais()}, $tehai->toString();
	}
	for my $ho (@{$self->hosJson($pos)}) {
		push @{$ai->hos()}, $ho->toString();
	}
	for my $point (@{$self->pointsJson($pos)}) {
		push @{$ai->points()}, $point;
	}
	$ai->yama($self->yama());
	$ai->round($self->round());
	$ai->continuous($self->continuous());
	$ai->turn($self->turn());
	$ai->phase($self->phase());
	$ai->roundSets($self->roundSets());
	$ai->latestDrop($self->latestDrop());
	$ai->dropPos($self->dropPos());
	$ai->kyotaku($self->kyotaku());
	return $ai;
}

sub autoPlay {
	my $self = shift;
	my %ret = ();
	my $ai = $self->getAi($self->turn());
	
	my $index = $ai->playIndex();
	my $reach = $ai->isReach();
	my $kan = $ai->getKan();
	
	
	if ($ai->isTsumo()) {
		push @{$self->finishFlags()}, $self->turn();
		$self->tsumoFlag(1);
		$self->waitCancel();
		%ret = $self->endRound();
	} elsif (defined($kan)) {
		$self->kanPai($kan);
	} else {
		if ($reach) {
			$self->reach($self->turn());
		}
		$self->dropPai($self->turn(), $index);
	}
	return %ret;
}

sub TO_JSON {
	my $self = shift;
	my %self_hash = (
		'Tehais' => $self->tehaisJson(),
		'Hos' => $self->hosJson(),
		'PlayerNames' => $self->playerNamesJson(),
		'Points' => $self->pointsJson(),
		'Yama' => $self->yamaJson(),
		'Round' => $self->round(),
		'Continuous' => $self->continuous(),
		'Turn' => $self->turn(),
		'Phase' => $self->phase(),
		'RoundSets' => $self->roundSets(),
		'LatestDrop' => $self->latestDrop(),
		'DropPos' => $self->dropPos(),
		'Kyotaku' => $self->kyotaku(),
		'PlayerNoHuro' => $self->playerNoHuroJson(),
		'PlayerHuroType' => $self->playerHuroTypeJson(),
		'PlayerAutoFinish' => $self->playerAutoFinishJson(),
		'PlayerIsFinish' => $self->playerIsFinishJson(),
		'WaitPlayer' => $self->waitPlayerJson(),
		'VP' => $self->viewPoint(),
		'Comment' => $self->{Comment},
	);
	return {%self_hash};
}

sub stateString {
	my $self = shift;
	my $ret = '';
	$ret .= 'isPlaying;';
	$ret .= $self->isPlaying();
	$ret .= "\n";
	$ret .= 'tehais;';
	$ret .= join "<>", (map { $_->toString() } @{$self->tehais()});
	$ret .= "\n";
	$ret .= 'hos;';
	$ret .= join "<>", (map { $_->toString() } @{$self->hos()});
	$ret .= "\n";
	$ret .= 'playerNames;';
	$ret .= join "<>", @{$self->playerNames()};
	$ret .= "\n";
	$ret .= 'points;';
	$ret .= join "<>", (map { $_->toString() } @{$self->points()});
	$ret .= "\n";
	$ret .= 'yama;';
	$ret .= $self->yama()->toString();
	$ret .= "\n";
	$ret .= 'round;';
	$ret .= $self->round();
	$ret .= "\n";
	$ret .= 'continuous;';
	$ret .= $self->continuous();
	$ret .= "\n";
	$ret .= 'turn;';
	$ret .= $self->turn();
	$ret .= "\n";
	$ret .= 'phase;';
	$ret .= $self->phase();
	$ret .= "\n";
	$ret .= 'memberNum;';
	$ret .= $self->memberNum();
	$ret .= "\n";
	$ret .= 'roundSets;';
	$ret .= $self->roundSets();
	$ret .= "\n";
	$ret .= 'latestDrop;';
	if (defined($self->latestDrop())) {
		$ret .= $self->latestDrop()->str();
	}
	$ret .= "\n";
	$ret .= 'kanPai;';
	if (defined($self->kanPai())) {
		$ret .= $self->kanPai()->str();
	}
	$ret .= "\n";
	$ret .= 'dropPos;';
	$ret .= $self->dropPos();
	$ret .= "\n";
	$ret .= 'finishFlags;';
	$ret .= join "<>", @{$self->finishFlags()};
	$ret .= "\n";
	$ret .= 'tsumoFlag;';
	$ret .= $self->tsumoFlag();
	$ret .= "\n";
	$ret .= 'kyotaku;';
	$ret .= $self->kyotaku();
	$ret .= "\n";
	$ret .= 'ippatsuFlag;';
	$ret .= join "<>", @{$self->ippatsuFlag()};
	$ret .= "\n";
	$ret .= 'reachHassei;';
	$ret .= $self->reachHassei();
	$ret .= "\n";
	$ret .= 'playerNoHuro;';
	$ret .= join "<>", @{$self->playerNoHuro()};
	$ret .= "\n";
	$ret .= 'playerHuroType;';
	$ret .= join "<>", @{$self->playerHuroType()};
	$ret .= "\n";
	$ret .= 'playerAutoFinish;';
	$ret .= join "<>", @{$self->playerAutoFinish()};
	$ret .= "\n";
	$ret .= 'playerIsFinish;';
	$ret .= join "<>", @{$self->playerIsFinish()};
	$ret .= "\n";
	$ret .= 'waitPlayer;';
	$ret .= join "<>", @{$self->{WaitPlayer}};
	$ret .= "\n";
	$ret .= 'minogashiFlag;';
	$ret .= join "<>", @{$self->minogashiFlag()};
	$ret .= "\n";
	$ret .= 'comment;';
	$ret .= $self->{Comment};
	$ret .= "\n";
	$ret .= 'tedumi;';
	$ret .= $self->tedumi();
	$ret .= "\n";
	return $ret;
}

sub readState {
	my $self = shift;
	my $str = shift;
	my @lines = split /\n/, $str;
	my $ret = '';
	my $isPlaying = 0;
	for my $line (@lines) {
		my ($key, $value) = split /;/, $line;
		chomp $value;
		if ($key eq 'isPlaying') {
			$isPlaying = $value;
		} elsif (!$isPlaying) {
			if ($key eq 'playerNames') {
				$self->clearPlayerNames();
				my @names = split /<>/, $value;
				for my $name (@names) {
					push @{$self->playerNames()}, $name;
				}
			}
		}elsif ($key eq 'tehais') {
			$self->clearTehais();
			my @tehais = split /<>/, $value;
			for my $i (0..3) {
				my $tehai_str = $tehais[$i];
				my $tehai = MahjongTehai->new();
				$tehai->setAll($tehai_str);
				$tehai->position($i);
				push @{$self->tehais()}, $tehai;
			}
		} elsif ($key eq 'hos') {
			my @hos = split /<>/, $value;
			for my $i (0..3) {
				my $ho_str = $hos[$i];
				my $ho = MahjongHo->new();
				$ho->setAll($ho_str);
				$self->hos($i, $ho);
			}
		} elsif ($key eq 'points') {
			my @points = split /<>/, $value;
			for my $i (0..3) {
				my $point_str = $points[$i];
				my $point = MahjongPlayerInfo->new();
				$point->setAll($point_str);
				$self->points($i, $point);
			}
		} elsif ($key eq 'yama') {
			$self->yama()->setAll($value);
		} elsif ($key eq 'round') {
			$self->round($value);
		} elsif ($key eq 'continuous') {
			$self->continuous($value);
		} elsif ($key eq 'turn') {
			$self->turn($value);
		} elsif ($key eq 'phase') {
			$self->phase($value);
		} elsif ($key eq 'memberNum') {
			$self->memberNum($value);
		} elsif ($key eq 'roundSets') {
			$self->roundSets($value);
		} elsif ($key eq 'latestDrop') {
			if ($value) {
				my $pai = MahjongPai->new();
				$pai->str($value);
				$self->latestDrop($pai);
			}
		} elsif ($key eq 'kanPai') {
			if ($value) {
				my $pai = MahjongPai->new();
				$pai->str($value);
				$self->kanPai($pai);
			}
		} elsif ($key eq 'dropPos') {
			$self->dropPos($value);
		} elsif ($key eq 'finishFlags') {
			my @flags = split /<>/, $value;
			my $i = 0;
			for my $flag (@flags) {
				$self->finishFlags($i, $flag);
				$i++;
			}
		} elsif ($key eq 'tsumoFlag') {
			$self->tsumoFlag($value);
		} elsif ($key eq 'kyotaku') {
			$self->kyotaku($value);
		} elsif ($key eq 'ippatsuFlag') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->ippatsuFlag($i, $flags[$i]);
			}
		} elsif ($key eq 'reachHassei') {
			$self->reachHassei($value);
		} elsif ($key eq 'ippatsuFlag') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->ippatsuFlag($i, $flags[$i]);
			}
		} elsif ($key eq 'playerNoHuro') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->playerNoHuro($i, $flags[$i]);
			}
		} elsif ($key eq 'playerHuroType') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->playerHuroType($i, $flags[$i]);
			}
		} elsif ($key eq 'PlayerAutoFinish') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->playerAutoFinish($i, $flags[$i]);
			}
		} elsif ($key eq 'playerIsFinish') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->playerIsFinish($i, $flags[$i]);
			}
		} elsif ($key eq 'waitPlayer') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->waitPlayer($i, $flags[$i]);
			}
		} elsif ($key eq 'minogashiFlag') {
			my @flags = split /<>/, $value;
			for my $i (0..3) {
				$self->minogashiFlag($i, $flags[$i]);
			}
		} elsif ($key eq 'comment') {
			$self->{Comment} = $value;
		} elsif ($key eq 'tedumi') {
			$self->tedumi($value);
		}
	}
	return $ret;
}
1;