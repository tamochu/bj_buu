require './lib/tutorial.cgi';
#=================================================
# ½ÀİÌß’  Created by nanamie
#=================================================

sub begin {	
=pod
	if ($config_test && $m{name} eq '‚¢') {
		foreach my $k (keys(%tutorial_quests)) {
			$m{$k} = 0;
		}
		$m{tutorial_quest_stamp_c} = 0;
		&write_user;
	}
=cut
	&show_stamps;

	&refresh;
	&n_menu;
}

1; # íœ•s‰Â
