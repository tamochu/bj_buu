@default_seeds = (
	[0, 'human',
		['Ë­°Ïİ',
		(
			'nou' => sub {
				$v = shift;
				print $v;
				return $v;
			}
		),
		100]
	]
);

1;
