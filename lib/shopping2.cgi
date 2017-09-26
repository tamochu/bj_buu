#================================================
# ¼®¯Ëßİ¸Ş2 Created by Merino
#================================================

# ÒÆ­° ’Ç‰Á/•ÏX/íœ/•À‚×‘Ö‚¦‰Â”\
my @menus = (
	['–ß‚é', 		'main'],
	['‘O‚ÌÍß°¼Ş',	'shopping'],
	['ÊÛ°Ü°¸',	'shopping_job_change'],
	['’b–è‰®',		'shopping_smith'],
	['“ä‚Ì_“a',	'shopping_unit_exchange'],
	['ºİÃ½Ä‰ïê',	'shopping_contest'],
	['•ó‚­‚¶‰®',	'shopping_lot'],
	['æÎ‘K” ',	'shopping_offertory_box'],
	['Œ‹¥‘Š’kŠ',	'shopping_marriage'],
	['ˆÅ‹à—Z',		'shopping_finance'],
	['¯~‚è‚Ì‚Ù‚±‚ç',	'shopping_mix'],
	['“¹ê',	'shopping_master'],
);

#================================================
sub begin {
	$mes .= '‚Ç‚±‚És‚«‚Ü‚·‚©?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  {
	return if &is_ng_cmd(1..$#menus);
	&b_menu(@menus);
}

1; # íœ•s‰Â
