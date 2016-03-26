#!/usr/local/bin/perl --
use lib './lib';
use NobO;
use JSON;

my $game_file = $logdir . '/nobo.cgi';

sub getNobO {
	my $mid = shift;
	my $nobo = NobO->new();
	
	open my $fh, "< $game_file" or &error("ゲームファイル読み込みエラー");
	my $str = '';
	while (my $line = <$fh>) {
		$str .= $line;
	}
	close $fh;
	
	$nobo->FROM_JSON($str);
	$nobo->viewId($mid);
	$nobo->userdir($userdir);
	$nobo->progress();
	
	&saveNobO($nobo);
	
	return $nobo;
}

sub saveNobO {
	my $nobo = shift;
	
	my $coder = JSON->new->utf8->convert_blessed;
	
	open my $fh, "+< $game_file" or &error("ゲームファイル読み込みエラー");
	eval { flock $fh, 2; };
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $coder->encode($nobo);
	close $fh;
}

1;