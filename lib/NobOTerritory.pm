#!/usr/local/bin/perl --
package NobOTerritory;
use strict;
use warnings;
use JSON qw/decode_json/;
use NobOLog;
use NobOConfig;

sub new {
	my $clazz = shift;
	my $self = {
		ID => 0,
		Name => 'default territory',
		X => 0.0,
		Y => 0.0,
		Population => 100,
		Civilization => 0,
		Culture => 0,
		Environment => 100,
		Hungry => 100,
		Noble => 0
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

sub name {
	my $self = shift;
	if (@_) {
		$self->{Name} = shift;
	}
	return $self->{Name};
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

sub population {
	my $self = shift;
	if (@_) {
		$self->{Population} = shift;
	}
	return $self->{Population};
}

sub civilization {
	my $self = shift;
	if (@_) {
		$self->{Civilization} = shift;
	}
	return $self->{Civilization};
}

sub culture {
	my $self = shift;
	if (@_) {
		$self->{Culture} = shift;
	}
	return $self->{Culture};
}

sub environment {
	my $self = shift;
	if (@_) {
		$self->{Environment} = shift;
	}
	return $self->{Environment};
}

sub hungry {
	my $self = shift;
	if (@_) {
		$self->{Hungry} = shift;
	}
	return $self->{Hungry};
}

sub noble {
	my $self = shift;
	if (@_) {
		$self->{Noble} = shift;
	}
	return $self->{Noble};
}

# accessor‚±‚±‚Ü‚Å

sub addPopulation {
	my $self = shift;
	my $add = shift;
	my %config = NobOConfig->getConfig();
	
	my $v = $self->population() + $add;
	if ($config{minPopulation} > $v) {
		$v = int($config{minPopulation} / 2 + rand($config{minPopulation} / 2));
	}
	
	$self->population($v);
}

sub addCivilization {
	my $self = shift;
	my $add = shift;
	my $owner = shift;
	
	$self->civilization($self->civilization() + $add);
}

sub addCulture {
	my $self = shift;
	my $add = shift;
	my $owner = shift;
	my %nobles = NobOConfig->getNobles();

	my @newNoble = ();
	
	my $before = $self->culture() + 1;
	$self->culture($self->culture() + $add);
	my $after = $self->culture();
	if ($before <= $after) {
		for my $cul ($before..$after) {
			if (defined($nobles{'culture_' . $cul})) {
				$self->addNoble($nobles{'culture_' . $cul}[1]);
				my $log = NobOLog->new();
				$log->toName($owner);
				$log->appendText($self->name());
				$log->appendText('‚Ì•¶‰»‚ª¬’·‚µ');
				$log->appendText($nobles{'culture_' . $cul}[2]);
				$log->appendText('‚ª“oê‚µ‚Ü‚µ‚½');
				$log->sendMail();
			}
		}
	}
}

sub addEnvironment {
	my $self = shift;
	my $add = shift;
	my %config = NobOConfig->getConfig();
	
	my $v = $self->environment() + $add;
	if ($config{minEnvironment} > $v) {
		$v = $config{minEnvironment};
	} elsif ($config{maxEnvironment} < $v) {
		$v = $config{maxEnvironment};
	}
	
	$self->environment($v);
}

sub addHungry {
	my $self = shift;
	my $add = shift;
	my %config = NobOConfig->getConfig();
	
	my $v = $self->hungry() + $add;
	if ($config{minHungry} > $v) {
		$v = $config{minHungry};
	} elsif ($config{maxHungry} < $v) {
		$v = $config{maxHungry};
	}
	
	$self->hungry($v);
}

sub addNoble {
	my $self = shift;
	my $add = shift;
	
	$self->noble($self->noble() + $add);
}

sub civilizationAbsorption {
	my $self = shift;
	my $absorption = shift;
	my $v = $absorption - $self->civilization();
	if ($v < 2) {
		$v = 2;
	}
	if (rand($v) > 1) {
		$self->addCivilization(1);
	}
}

sub calcDiffPopulation {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	return int($self->population()
				* $diff
				* (rand($config{populationAddRand}) + $config{populationAddBase})
				* ($self->hungry() - $config{populationAddHungryBorder})
				/ ($config{minPopulation} * $config{baseDiffSec} * 100 * $config{hungryMax}));
}

sub calcDiffCivilization {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	return int(rand($diff
				* ($self->noble() + $config{civilizationAddNobleBottom})
				/ ($config{baseDiffSec} * $config{civilizationAddNobleBottom} * $config{civilizationUpDifficulty})));
}

sub calcDiffCulture {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	return int(rand($diff
				* ($self->civilization() + $config{cultureAddCivilizationBottom})
				* $self->population()
				/ ($config{baseDiffSec} * $config{cultureAddCivilizationBottom} * $config{minPopulation} * $config{cultureUpDifficulty})));
}

sub calcDiffEnvironment {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	return int($self->population()
				* $diff
				* (rand($config{environmentAddRand}) + $config{environmentAddBase})
				* ($self->noble() - $self->civilization() - $config{environmentAddCivilizationBase})
				* ($self->population() - $config{environmentPopulationLimit})
				/ ($config{minPopulation} * $config{baseDiffSec} * $config{environmentAddCivilizationBase} * $config{environmentPopulationLimit} * $config{environmentChangeDifficulty}));
}

sub calcDiffHungry {
	my $self = shift;
	my $diff = shift;
	my %config = NobOConfig->getConfig();
	
	return int(rand($diff
				* ($self->environment() - $config{hungryAddEnvironmentBorder})
				* ($self->civilization() + $self->noble() + $config{hungryAddCivilizationBase})
				/ ($config{baseDiffSec} * $config{hungryAddEnvironmentBorder} * $config{hungryUpDifficulty})));
}

sub calcDiff {
	my $self = shift;
	my $diff = shift;
	my $owner = shift;
	
	my $diffPop = $self->calcDiffPopulation($diff);
	my $diffCiv = $self->calcDiffCivilization($diff);
	my $diffCul = $self->calcDiffCulture($diff);
	my $diffEnv = $self->calcDiffEnvironment($diff);
	my $diffHun = $self->calcDiffHungry($diff);
	
	$self->addPopulation($diffPop);
	if ($owner ne '') {
		$self->addCivilization($diffCiv, $owner);
		$self->addCulture($diffCul, $owner);
	}
	$self->addEnvironment($diffEnv);
	$self->addHungry($diffHun);
}

sub distanceTerritory {
	my $self = shift;
	my $compare = shift;
	
	return sqrt((($self->x() - $compare->x()) ** 2) + (($self->y() - $compare->y()) ** 2));
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
		$self->{$key} = ${${$data}{NobOTerritory}}{$key};
	}
	
	return $self;
}

1;