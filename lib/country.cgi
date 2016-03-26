#================================================
# 国情報 Created by Merino
#================================================

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['やめる',			'main'],
	['各国の情報',		'country_info'],
	['仕官',			'country_move'],
	["$e2j{ceo}投票",	'country_leader'],
	['代表国民審査',	'country_review'],
	['代表\者の仕事',	'country_daihyo'], # 代表者のみ表示
	["$e2j{ceo}の仕事",	'country_config'], # 君主のみ表示
);


#================================================
sub begin {
	my $line = &get_countries_mes($m{country}) if $m{country};
	my($country_mes, $country_mark) = split /<>/, $line;
	my @lines = &get_country_members($m{country});
	
	$mes .= qq|<font color="$cs{color}[$m{country}]">$c_m</font>|;
	$mes .= qq|<br><img src="$icondir/$country_mark">| if $country_mark;
	$mes .= qq|<br>$country_mes| if $country_mes;
	$mes .= qq|<hr size="1">戦争：$cs{modify_war}[$m{country}] 内政：$cs{modify_dom}[$m{country}] 軍事：$cs{modify_mil}[$m{country}] 外交：$cs{modify_pro}[$m{country}]|;
	$mes .= qq|<hr size="1">所属者<br>@lines|;
	
	pop @menus unless $cs{ceo}[$m{country}] eq $m{name}; # 君主以外非表示
	pop @menus unless &is_daihyo; # 代表者以外非表示
	
	&menu(map{ $_->[0] }@menus);
}

sub tp_1 { &b_menu(@menus); }



1; # 削除不可
