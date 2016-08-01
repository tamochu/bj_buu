#=================================================
# ｺﾚｸｼｮﾝ追加 Created by Merino
#=================================================
# 使い方: require './lib/add_collection.cgi'; して &add_collection;
# collction.cgi,depot.cgiで使用

#================================================
# ｺﾚｸｼｮﾝﾃﾞｰﾀ取得 + 今装備中のﾓﾉがｺﾚｸｼｮﾝにないなら追加
#=================================================
sub add_collection {
	my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
	my $kind = 1;
	my $is_rewrite = 0;
	my @lines = ();
	
	my %temp = ();
	$temp{wea} = $m{wea};
	$temp{egg} = $m{egg};
	if ($temp{egg} == 53) {
		$temp{egg} = 42;
	}
	$temp{pet} = $m{pet} < 0 ? 0 : $m{pet};
	if ($temp{pet} == 180) {
		$temp{pet} = 76;
	}
	if ($temp{pet} == 181) {
		$temp{pet} = 77;
	}
	if ($temp{pet} == 195) {
		$temp{pet} = 194;
	}
	$temp{gua} = $m{gua};
	
	open my $fh, "+< $userdir/$id/collection.cgi" or &error("ｺﾚｸｼｮﾝﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d; # \n改行削除
		# 追加
		if ($temp{ $kinds[$kind] } && $line !~ /,$temp{ $kinds[$kind] },/) {
			$is_rewrite = 1;
			$line .= "$temp{ $kinds[$kind] },";
			$mes .= $kind eq '1' ? $weas[$temp{wea}][1]
				  : $kind eq '2' ? $eggs[$temp{egg}][1]
				  : $kind eq '3' ? $pets[$temp{pet}][1]
				  :                $guas[$temp{gua}][1]
				  ;
			$mes .= 'が新しく図鑑に追加されました<br>';
			
			# sort
			$line  = join ",", sort { $a <=> $b } split /,/, $line;
			$line .= ",";
		}
		
		push @lines, "$line\n";
		++$kind;
	}
	while($kind < @kinds){
		push @lines, ",\n";
		$kind++;
		$is_rewrite = 1;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	return @lines;
}


1; # 削除不可
