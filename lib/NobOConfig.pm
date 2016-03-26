#!/usr/local/bin/perl --
package NobOConfig;
use strict;
use warnings;

sub new {
	my $clazz = shift;
	my $self = {
		Dummy => 0
	};
	return bless $self, $clazz;
}

sub getConfig {
	my %config = (
		'baseDiffSec' => 1,
		'minPopulation' => 10,
		'minEnvironment' => 0,
		'maxEnvironment' => 100,
		'minHungry' => 0,
		'maxHungry' => 100,
		'populationAddRand' => 120,
		'populationAddBase' => -20,
		'populationAddHungryBorder' => 50,
		'hungryMax' => 100,
		'civilizationUpDifficulty' => 1,
		'cultureAddCivilizationBottom' => 100,
		'civilizationAddNobleBottom' => 1,
		'cultureUpDifficulty' => 10000,
		'environmentAddRand' => 100,
		'environmentAddBase' => 0,
		'environmentAddCivilizationBase' => 50,
		'environmentPopulationLimit' => 1000,
		'environmentChangeDifficulty' => 10,
		'hungryAddEnvironmentBorder' => 70,
		'hungryAddCivilizationBase' => 100,
		'hungryUpDifficulty' => 10,
		'territoryMinDistance' => 1.0,
		'conquerNeedsMultiple' => 3.0,
		'capitalModify' => 3.0,
		'capitalDiffence' => 0.01,
		'userDiffence' => 1.0,
		'noUserDiffence' => 3.0,
		'tradeCultureIncreaseDifficulty' => 2,
		'minMove' => 10,
		'userdir' => './user'
	);
	return %config;
}


sub getNobles {
	my %nobles = (
		'culture_1' => [1, 1, 'Å‰‚Ì•¶‰»l'],
	);
	return %nobles;
}

1;