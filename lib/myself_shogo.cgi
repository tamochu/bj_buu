#================================================
# 称号切り替え Created by Merino
#================================================

# 自由称号が使用可能な世代
my $free_shogo_sedai = 15;

# @shogos以外の特別な称号 ※『★』を付けないと自由称号でなることが可能
my @special_shogos = (
	# 称号名,		ﾌﾟﾚｲﾔｰ名
#	['★管理人★',	'管理者名'],
#	['★副管理人',	'副ちゃん'],
	['★鯖管代行殿',	'変態糞娘'],
);


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0] は称号を変更することができません<br>";
		$mes .= "闇金融でお金を払ってください<br>";
		&refresh;
		&n_menu;
		return 0;
	}elsif ($m{shogo_t} ne ''){
		$mes .= "それを変えるなんてとんでもない<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	
	return 1;
}

#================================================
sub begin {
	&n_menu;
	$layout = 2;
	my $count = 0;
	my $sub_mes = qq|<input type="radio" name="no" value="0">なし<br>|;
	#-----------------------------------
	# 標準称号
	for my $i (1 .. $#shogos) {
		my($k, $v) = each %{ $shogos[$i][1] };
		if ($m{$k} >= $v) {
			$sub_mes .= $m{shogo} eq $shogos[$i][0]
				? qq|<input type="radio" name="no" value="$i" checked>$shogos[$i][0]<br>|
				: qq|<input type="radio" name="no" value="$i">$shogos[$i][0]<br>|
				;
			++$count;
		}
	}
	#-----------------------------------
	# マスター
	if (-f "$userdir/$id/shogo_master_flag.cgi") {
		$sub_mes .= $m{shogo} eq $shogos[2][0]
			? qq|<input type="radio" name="no" value="2" checked>$shogos[2][0]<br>|
			: qq|<input type="radio" name="no" value="2">$shogos[2][0]<br>|
			;
	}
	elsif ($count == $#shogos - 2) {
		&write_comp_legend;
	}
	#-----------------------------------
	# 特別な称号
	for my $i (0 .. $#special_shogos) {
		$i+=1000;
		if ($m{name} eq $special_shogos[$i-1000][1]) {
			$sub_mes .= $m{shogo} eq $special_shogos[$i-1000][0]
				? qq|<input type="radio" name="no" value="$i" checked>$special_shogos[$i-1000][0]<br>|
				: qq|<input type="radio" name="no" value="$i">$special_shogos[$i-1000][0]<br>|
				;
		}
	}

	#-----------------------------------
	# フリー称号
	$sub_mes .= qq|<p>自由称号：全角5(半角10)文字まで<br><input type="text" name="free_shogo" class="text_box_s"></p>| if $m{sedai} >= $free_shogo_sedai;

	my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
	$comp_par = 100 if $comp_par > 100;
	
	$mes .= qq|【$m{name}の取得称号一覧】《ｺﾝﾌﾟ率 <b>$comp_par</b>%》<hr>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="変更する" class="button1"></form>|;
}

#================================================
sub tp_1 {
	#-----------------------------------
	# フリー称号
	if ($in{free_shogo} && $m{sedai} >= $free_shogo_sedai) {
		&error("自由称号に不正な文字( ,;\"\'&<> )が含まれています") if $in{free_shogo} =~ /[,;\"\'&<>]/;
		&error("自由称号に半角数字のみは使えません") if $in{free_shogo} =~ /^\d+$/;
		&error("自由称号が長すぎます全角5(半角10)文字までです") if length $in{free_shogo} > 10;
		
		$in{free_shogo} =~ s/★/☆/g;
		$m{shogo} = $in{free_shogo};
		$mes .= "$m{shogo}に変更しました<br>";
	}
	#-----------------------------------
	# 特別な称号
	elsif ($in{no} >= 1000 && $m{name} eq $special_shogos[$in{no}-1000][1]) {
		$m{shogo} = $special_shogos[$in{no}-1000][0];
		$mes .= "$m{shogo}に変更しました<br>";
	}
	elsif (defined $in{no} && defined $shogos[$in{no}] && $shogos[$in{no}][0] ne $m{shogo}) {
		my($k, $v) = each %{ $shogos[$in{no}][1] };
		#-----------------------------------
		# マスター
		if ($in{no} eq '2' && -f "$userdir/$id/shogo_master_flag.cgi") {
			$m{shogo} = $shogos[$in{no}][0];
			$mes .= "$m{shogo}に変更しました<br>";
		}
		#-----------------------------------
		# 標準称号
		elsif ($m{$k} >= $v) {
			$m{shogo} = $shogos[$in{no}][0];
			if ($m{shogo}) {
				$mes .= "$m{shogo}に変更しました<br>";
			}
			else {
				$mes .= "称号を外しました<br>";
			}
		}
		else {
			$mes .= 'やめました<br>';
		}
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&refresh;
	&n_menu;
}

#=================================================
# ｺﾝﾌﾟﾘｰﾄ処理ﾌﾗｸﾞﾌｧｲﾙ作成
#=================================================
sub write_comp_legend {
	&write_legend('comp_shogo', "$c_mの$m{name}が全ての称号を手に入れる", 1);
	&mes_and_world_news("<i>全ての称号をｺﾝﾌﾟﾘｰﾄしました。$m{name}に$shogos[2][0]の称号があたえられました</i>");

	open my $fh, "> $userdir/$id/shogo_master_flag.cgi" or &error("$userdir/$id/shogo_master_flag.cgiﾌｧｲﾙが開けません");
	close $fh;
}


1; # 削除不可
