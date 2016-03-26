#!/usr/local/bin/perl --
package NobO;
use strict;
use warnings;
use JSON qw/decode_json encode_json/;
use NobOTerritory;
use NobOOwner;
use NobOArmy;
use NobOArmySoldier;
use NobOLog;
use NobOConfig;


sub new {
	my $clazz = shift;
	my $self = {
		Territories => [],
		Owners => [],
		Armies => [],
		ViewId => '',
		ArmySoldiers => [],
		LastDiffTime => 0,
		Userdir => ''
	};
	return bless $self, $clazz;
}

sub territories {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Territories}}[$i];
		}
		${$self->{Territories}}[$i] = $x;
	}
	return $self->{Territories};
}

sub owners {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Owners}}[$i];
		}
		${$self->{Owners}}[$i] = $x;
	}
	return $self->{Owners};
}

sub armies {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{Armies}}[$i];
		}
		${$self->{Armies}}[$i] = $x;
	}
	return $self->{Armies};
}

sub viewId {
	my $self = shift;
	if (@_) {
		$self->{ViewId} = shift;
	}
	return $self->{ViewId};
}

sub armySoldiers {
	my $self = shift;
	if (@_) {
		my ($i, $x) = @_;
		if (!defined($x)) {
			return ${$self->{ArmySoldiers}}[$i];
		}
		${$self->{ArmySoldiers}}[$i] = $x;
	}
	return $self->{ArmySoldiers};
}

sub lastDiffTime {
	my $self = shift;
	if (@_) {
		$self->{LastDiffTime} = shift;
	}
	return $self->{LastDiffTime};
}

sub userdir {
	my $self = shift;
	if (@_) {
		$self->{Userdir} = shift;
	}
	return $self->{Userdir};
}

# accessor ここまで

sub nextTerritoryId {
	my $self = shift;
	my $maxId = 0;
	for my $ter (@{$self->territories()}) {
		if ($ter->id() > $maxId) {
			$maxId = $ter->id();
		}
	}
	return ($maxId + 1);
}

sub addNewTerritory {
	my $self = shift;
	my $name = shift;
	my %config = NobOConfig->getConfig();

	my $ter = NobOTerritory->new();
	my $newId = $self->nextTerritoryId();
	if ($name eq '') {
		$name = 'new territory ' . $newId;
	}
	$ter->id($newId);
	$ter->name($name);
	my $area = 0.0;
	while (1) {
		my $noConflict = 1;
		
		$ter->x(rand($area * 2) - $area);
		$ter->y(rand($area * 2) - $area);
		for my $cter (@{$self->territories()}) {
			if ($cter->distanceTerritory($ter) < $config{territoryMinDistance}) {
				$noConflict = 0;
				last;
			}
		}
		if ($noConflict) {
			last;
		}
		$area += 0.5;
	}
	push @{$self->territories()}, $ter;
	
	return $newId;
}

sub conquer {
	my $self = shift;
	my $territoryId = shift;
	my $owner = shift;

	my @newOwners = ();
	for my $own (@{$self->owners()}) {
		if ($own->territoryId() eq $territoryId) {
			next;
		}
		push @newOwners, $own;
	}
	
	my $newOwner = NobOOwner->new();
	$newOwner->territoryId($territoryId);
	$newOwner->ownerName($owner);
	$newOwner->capital(0);
	push @newOwners, $newOwner;
	
	$self->{Owners} = \@newOwners;
}

sub addNewConquerdTerritory {
	my $self = shift;
	my $conquerName = shift;

	my $tid = $self->addNewTerritory('');
	$self->conquer($tid, $conquerName);
	
	return $tid;
}

sub getTerritoryById {
	my $self = shift;
	my $territoryId = shift;

	for my $ter (@{$self->territories()}) {
		if ($ter->id() == $territoryId) {
			return $ter;
		}
	}
	return undef;
}

sub getOwnerByTerId {
	my $self = shift;
	my $territoryId = shift;

	for my $own (@{$self->owners()}) {
		if ($own->territoryId() == $territoryId) {
			return $own;
		}
	}
	return undef;
}

sub getSoldiersByArmId {
	my $self = shift;
	my $armyId = shift;

	my @ret = ();
	for my $s (@{$self->armySoldiers()}) {
		if ($s->armyId() == $armyId) {
			push @ret, $s;
		}
	}
	return @ret;
}

sub nextArmyId {
	my $self = shift;
	my $maxId = 0;
	for my $arm (@{$self->armies()}) {
		if ($arm->id() > $maxId) {
			$maxId = $arm->id();
		}
	}
	return ($maxId + 1);
}

sub addNewArmy {
	my $self = shift;
	my $leaderName = shift;
	my $from = shift;
	my $to = shift;

	my $arm = NobOArmy->new();
	my $newId = $self->nextArmyId();
	$arm->id($newId);
	$arm->leaderName($leaderName);
	$arm->setPosition($self->getTerritoryById($from), $self->getTerritoryById($to));
	push @{$self->armies()}, $arm;
	
	return $newId;
}

sub newGame {
	my $self = shift;
	my $conquerName = shift;

	$self->renounceAll($conquerName);
	my $tid = $self->addNewConquerdTerritory($conquerName, 1);
	$self->setCapital($conquerName, $tid);
}

sub renounceAll {
	my $self = shift;
	my $conquerName = shift;

	my @newOwners = ();
	for my $own (@{$self->owners()}) {
		if ($own->ownerName() eq $conquerName) {
			next;
		}
		push @newOwners, $own;
	}
	
	$self->{Owners} = \@newOwners;
}

sub setCapital {
	my $self = shift;
	my $conquerName = shift;
	my $territoryId = shift;

	for my $ownI (0..$#{$self->owners()}) {
		if (${$self->owners()}[$ownI]->ownerName() eq $conquerName) {
			if (${$self->owners()}[$ownI]->territoryId() == $territoryId) {
				${$self->owners()}[$ownI]->capital(1);
			} else {
				${$self->owners()}[$ownI]->capital(0);
			}
		}
	}
}

sub isCapital {
	my $self = shift;
	my $territoryId = shift;

	for my $own (@{$self->owners()}) {
		if ($own->territoryId() == $territoryId) {
			return $own->capital();
		}
	}
	return 0;
}

sub deleteArmySoldiers {
	my $self = shift;
	my $army = shift;
	
	my @newArmySoldiers = ();
	for my $as (@{$self->armySoldiers()}) {
		if ($as->armyId() != $army->id()) {
			push @newArmySoldiers, $as;
		}
	}
	$self->{ArmySoldiers} = \@newArmySoldiers;
}

sub armySoldier {
	my $self = shift;
	my $armyId = shift;
	my $soldierAmount = shift;
	
	my $s = NobOArmySoldier->new();
	$s->armyId($armyId);
	$s->amount($soldierAmount);
	push @{$self->armySoldiers()}, $s;
}

sub populationIncrease {
	my $self = shift;
	my $territoryId = shift;
	my $amount = shift;
	
	for my $terI (0..$#{$self->territories()}) {
		if (${$self->territories()}[$terI]->id() == $territoryId) {
			${$self->territories()}[$terI]->addPopulation($amount);
		}
	}
}

sub civilizationAbsorption {
	my $self = shift;
	my $territoryId = shift;
	my $amount = shift;
	
	$amount |= 0;
	
	for my $terI (0..$#{$self->territories()}) {
		if (${$self->territories()}[$terI]->id() == $territoryId) {
			${$self->territories()}[$terI]->civilizationAbsorption($amount);
		}
	}
}

sub cultureIncrease {
	my $self = shift;
	my $territoryId = shift;
	my $amount = shift;
	
	for my $terI (0..$#{$self->territories()}) {
		if (${$self->territories()}[$terI]->id() == $territoryId) {
			my $terOwner = $self->getOwnerByTerId($territoryId);
			my $ownerName = (defined($terOwner)) ? $terOwner->ownerName() : '';
			${$self->territories()}[$terI]->addCulture($amount, $ownerName);
		}
	}
}

sub move {
	my $self = shift;
	my $conquerName = shift;
	my $from = shift;
	my $to = shift;
	my $amount = shift;
	my %config = NobOConfig->getConfig();
	
	my $fromOwner = $self->getOwnerByTerId($from);
	if (defined($fromOwner) && $fromOwner->ownerName() eq $conquerName) {
		my $fromTerritory = $self->getTerritoryById($from);
		my $soldierAmount = int($fromTerritory->population() * $amount / 100);
		if ($soldierAmount >= $config{minMove}) {
			my $armyId = $self->addNewArmy($conquerName, $from, $to);
			$self->armySoldier($armyId, $soldierAmount);
			$self->populationIncrease($from, -1 * $soldierAmount);
			return $armyId;
		}
	}
	return 0;
}

sub trade {
	my $self = shift;
	my $conquerName = shift;
	my $from = shift;
	my $to = shift;
	my %config = NobOConfig->getConfig();

	my $armyId = $self->move($conquerName, $from, $to, 10);
	
	my $targetOwner = $self->getOwnerByTerId($to);
	if (!defined($targetOwner) || $targetOwner->ownerName() ne $conquerName) {
		for my $arm (@{$self->armies()}) {
			if ($arm->id() == $armyId) {
				$arm->trade(1);
				if (rand($config{tradeCultureIncreaseDifficulty}) < 1) {
					$self->cultureIncrease($from, 1);
				}
			}
		}
	}
}

sub territoryNameSet {
	my $self = shift;
	my $conquerName = shift;
	my $at = shift;
	my $terName = shift;
	
	my $targetOwner = $self->getOwnerByTerId($at);
	if (defined($targetOwner) && $targetOwner->ownerName() eq $conquerName) {
		for my $terI (0..$#{$self->territories()}) {
			if (${$self->territories()}[$terI]->id() == $at) {
				${$self->territories()}[$terI]->name($terName);
			}
		}
	}
}

sub goal {
	my $self = shift;
	my $army = shift;
	
	my $targetOwner = $self->getOwnerByTerId($army->targetTerritoryId());
	if (defined($targetOwner) && $targetOwner->ownerName() eq $army->leaderName()) {
		$self->migrate($army);
	} elsif ($army->trade()) {
		$self->tradeComplete($army);
	} else {
		$self->attack($army);
	}
	$self->deleteArmySoldiers($army);
}

sub migrate {
	my $self = shift;
	my $army = shift;
	
	my $log = NobOLog->new();
	$log->toName($army->leaderName());
	$log->appendText('ほかの拠点に人を移動させました<br>');
	my @armySoldiers = $self->getSoldiersByArmId($army->id());
	for my $s (@armySoldiers) {
		$self->populationIncrease($army->targetTerritoryId(), $s->amount());
		$log->appendText('内訳:' . $s->amount() . '人');
		$log->appendText('<br>');
	}
	$log->sendMail();
}

sub tradeComplete {
	my $self = shift;
	my $army = shift;
	
	my $log = NobOLog->new();
	$log->toName($army->leaderName());
	$log->appendText('ほかの拠点と交易を行いました<br>');
	my @armySoldiers = $self->getSoldiersByArmId($army->id());
	for my $s (@armySoldiers) {
		$self->populationIncrease($army->targetTerritoryId(), $s->amount());
		$log->appendText('内訳:' . $s->amount() . '人');
		$log->appendText('<br>');
	}
	$log->sendMail();
}

sub attack {
	my $self = shift;
	my $army = shift;
	my %config = NobOConfig->getConfig();

	my $log = NobOLog->new();
	$log->toName($army->leaderName());
	$log->appendText('ほかの拠点を攻撃しました<br>');
	
	my $targetOwner = $self->getOwnerByTerId($army->targetTerritoryId());
	
	my $log2 = NobOLog->new();
	$log2->appendText('他のプレイヤーから攻撃を受けました<br>');
	
	my @armySoldiers = $self->getSoldiersByArmId($army->id());
	my $totalSoldiers = 0;
	for my $s (@armySoldiers) {
		$totalSoldiers += $s->amount();
	}
	my $tt = $self->getTerritoryById($army->targetTerritoryId());
	my $decrease;
	my $conquer = 0;
	my $diffenceMultiple = 1.0;
	my $attackRest = 0;
	for my $attackTry (1..$totalSoldiers) {
		$attackRest = $totalSoldiers - $attackTry;
		if (defined($targetOwner)) {
			if ($targetOwner->capital()) {
				$diffenceMultiple = $config{capitalDiffence};
			} else {
				$diffenceMultiple = $config{userDiffence};
			}
		} else {
			$diffenceMultiple = $config{noUserDiffence};
		}
		$decrease = int($attackTry * $diffenceMultiple);
		my $targetRest = $tt->population() - $decrease;
		if ($attackRest * $diffenceMultiple > $targetRest * $config{conquerNeedsMultiple}) {
			$conquer = 1;
			last;
		}
	}
	$log->appendText($totalSoldiers . '人の兵士を送り、双方に損害が出ました<br>');
	$log2->appendText($totalSoldiers . '人の兵士が送られ、' . $decrease . '人の損害が出ました<br>');
	$self->populationIncrease($army->targetTerritoryId(), $attackRest - $decrease);
	if ($conquer) {
		$self->conquer($army->targetTerritoryId(), $army->leaderName());
		$log->appendText('結果拠点の占領に成功しました！<br>');
		$log2->appendText('結果拠点を占領されてしまいました<br>');
	} else {
		$self->civilizationAbsorption($army->targetTerritoryId(), $army->civilization());
		$log->appendText('結果拠点の占領にまでは至りませんでした！<br>');
		$log2->appendText('結果拠点を防衛に成功しました<br>');
	}
	$log->sendMail();
	if (defined($targetOwner)) {
		$log2->toName($targetOwner->ownerName());
		$log2->sendMail();
	}
}

sub calcDiff {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	for my $ter (@{$self->territories()}) {
		my $terDiff = $diff;
		if ($self->isCapital($ter->id())) {
			$terDiff = int($config{capitalModify} * $diff);
		}
		my $terOwner = $self->getOwnerByTerId($ter->id());
		my $ownerName = (defined($terOwner)) ? $terOwner->ownerName() : '';
		$ter->calcDiff($terDiff, $ownerName);
	}
	my @reachedArmyIds = ();
	for my $arm (@{$self->armies()}) {
		if ($arm->move($diff, $self->getTerritoryById($arm->targetTerritoryId()))) {
			push @reachedArmyIds, $arm->id();
		}
	}
	for my $reachedId (@reachedArmyIds) {
		for my $armI (0..$#{$self->armies()}) {
			if (${$self->armies()}[$armI]->id() == $reachedId) {
				my $reachedArmy = splice @{$self->armies()}, $armI, 1;
				$self->goal($reachedArmy);
				last;
			}
		}
	}
}

sub progress {
	my $self = shift;
	
	my $now = time();
	my $diff = $now - $self->lastDiffTime();
	$self->calcDiff($diff);
	$self->lastDiffTime($now);
}

sub TO_JSON {
	my $self = shift;
	my %h_self = ();
	for my $key (keys(%$self)) {
		if ($self->viewId() ne '') {
			my $invisible = 0;
			if ($invisible) {
				next;
			}
		}
		$h_self{$key} = $self->{$key};
	}

	return { ref($self) => \%h_self };
}

sub FROM_JSON {
	my $self = shift;
	my $json = shift;
	
	my $data = decode_json($json);
	for my $key (keys(%$self)) {
		if ($key eq 'Territories') {
			my @newArr = ();
			for (@{${${$data}{NobO}}{$key}}) {
				my $ret = NobOTerritory->new();
				$ret->FROM_JSON(encode_json($_));
				push @newArr, $ret;
			}
			$self->{$key} = \@newArr;
		} elsif ($key eq 'Owners') {
			my @newArr = ();
			for (@{${${$data}{NobO}}{$key}}) {
				my $ret = NobOOwner->new();
				$ret->FROM_JSON(encode_json($_));
				push @newArr, $ret;
			}
			$self->{$key} = \@newArr;
		} elsif ($key eq 'Armies') {
			my @newArr = ();
			for (@{${${$data}{NobO}}{$key}}) {
				my $ret = NobOArmy->new();
				$ret->FROM_JSON(encode_json($_));
				push @newArr, $ret;
			}
			$self->{$key} = \@newArr;
		} elsif ($key eq 'ViewId') {
			$self->{$key} = '';
		} elsif ($key eq 'ArmySoldiers') {
			my @newArr = ();
			for (@{${${$data}{NobO}}{$key}}) {
				my $ret = NobOArmySoldier->new();
				$ret->FROM_JSON(encode_json($_));
				push @newArr, $ret;
			}
			$self->{$key} = \@newArr;
		} else {
			$self->{$key} = ${${$data}{NobO}}{$key};
		}
	}
}

1;