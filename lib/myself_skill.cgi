require "$datadir/skill.cgi";
my $this_file = "$userdir/$id/skill.cgi";
#================================================
# ｽｷﾙ継承 Created by Merino
#================================================

#=================================================
sub begin {
	my @m_skills = split /,/, $m{skills};
	my @m_skills_s = split /,/, $m{skills_sub};
	my @m_skills_s2 = split /,/, $m{skills_sub2};
	my @m_skills_s3 = split /,/, $m{skills_sub3};
	$layout = 2;
	if ($m{tp} > 1) {
		$mes .= '他に何かしますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '習得済みの技を学んだり、今覚えている技を忘れることができます<br>';
	}

	$mes .= '<hr>覚えている技<br>';
	for my $no (@m_skills) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>セットしている技1<br>';
	for my $no (@m_skills_s) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>セットしている技2<br>';
	for my $no (@m_skills_s2) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>セットしている技3<br>';
	for my $no (@m_skills_s3) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>';
	
	open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	
	my $count = 0;
	my $sub_mes = '';
	for my $no (split /,/, $line) {
		next if $no eq ''; # 先頭の空
		
		$sub_mes .= "[$skills[$no][2]]$skills[$no][1] 消費$e2j{mp}$skills[$no][3]<br>" if $no;
		++$count;
	}
	my $comp_par = $count <= 0 ? 0 : int($count / $#skills * 100);
	$comp_par = 100 if $comp_par > 100;
	&write_comp_legend if $count eq $#skills;
	
	$mes .= "習得済みの技《ｺﾝﾌﾟ率 <b>$comp_par</b>%》<hr>";
	$mes .= $sub_mes;
	
	&menu('やめる','覚える','忘れる','セットする','セット技に変更');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_' .$m{tp} };
}


#=================================================
# 覚える
#=================================================
sub tp_100 {
	$layout = 2;
	$m{tp} += 10;
	$mes .= "どの技を覚えますか?<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked> やめる<br>|;
	
	open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	for my $no (split /,/, $line) {
		next unless $no;
		$mes .= qq|<input type="radio" name="cmd" value="$no">[$skills[$no][2]]$skills[$no][1]<br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<input type="submit" value="覚える" class="button1" accesskey="0"></form>|:
		qq|<input type="submit" value="覚える" class="button1"></form>|;
	&n_menu;
}
sub tp_110 {
	my @m_skills = split /,/, $m{skills};
	if ($cmd) {
		if (@m_skills >= 5) {
			$mes .= '5個までしか覚えることができません<br>';
		}
		else {
			open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
			my $line = <$fh>;
			close $fh;
			$line =~ tr/\x0D\x0A//d;

			for my $no (split /,/, $line) {
				next unless $no;
				if ($no eq $cmd) {
					$mes .= "[$skills[$no][2]]$skills[$no][1]を覚えました!<br>";
					$m{skills} .= "$no,";
					last;
				}
			}
		}
	}
	&begin;
}

#=================================================
# 忘れる
#=================================================
sub tp_200 {
	$m{tp} += 10;
	$mes .= "どの技を忘れますか?<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	my $count = 0;
	for my $skill (split /,/, $m{skills}) {
		++$count;
		$mes .= qq|<input type="checkbox" id="no_$count" name="$count" value="1">|;
		$mes .= qq|<label for="no_$count">| unless $is_mobile;
		$mes .= qq|[$skills[$skill][2]]$skills[$skill][1]|;
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|<br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<input type="submit" value="忘れる" class="button1" accesskey="0"></form>|:
		qq|<input type="submit" value="忘れる" class="button1"></form>|;
	&n_menu;

}
sub tp_210 {
	my @m_skills = split /,/, $m{skills};
	my $line = '';
	for my $count (0 .. $#m_skills) {
		if ($in{$count+1}) {
			$mes .= "[$skills[ $m_skills[$count] ][2]]$skills[ $m_skills[$count] ][1]を忘れました<br>";
		}
		else {
			$line .= "$m_skills[$count],";
		}
	}
	$m{skills} = $line;
	&begin;
}

sub tp_300{
	$mes .= "何番にセットしますか？";
	$m{tp} += 10;
	&menu('やめる','1','2','3');
}

sub tp_310{
	if($cmd eq '1'){
		$m{skills_sub} = $m{skills};
		$mes .= "今覚えている技をセットしました";
	}elsif($cmd eq '2'){
		$m{skills_sub2} = $m{skills};
		$mes .= "今覚えている技をセットしました";
	}elsif($cmd eq '3'){
		$m{skills_sub3} = $m{skills};
		$mes .= "今覚えている技をセットしました";
	}else{
		$mes .= "やめました";
	}
    &begin;
}


sub tp_400{
	$mes .= "何番をセットしますか？";
	$m{tp} += 10;
	&menu('やめる','1','2','3');
}

sub tp_410{
	if($cmd eq '1'){
		$m{skills} = $m{skills_sub};
		$mes .= "セットしている技に変えました";
	}elsif($cmd eq '2'){
		$m{skills} = $m{skills_sub2};
		$mes .= "セットしている技に変えました";
	}elsif($cmd eq '3'){
		$m{skills} = $m{skills_sub3};
		$mes .= "セットしている技に変えました";
	}else{
		$mes .= "やめました";
	}
	&begin;
}

#=================================================
# ｺﾝﾌﾟﾘｰﾄ処理
#=================================================
sub write_comp_legend {
	&write_legend('comp_skill', "$c_mの$m{name}が全ての技を極める", 1);
	&mes_and_world_news("<i>全ての技をｺﾝﾌﾟﾘｰﾄしました。$m{name}に★奥義師範の称号があたえられました</i>");

	# 一時的な称号
	$m{shogo} = '★奥義師範';

	# 0 を追加することで ｺﾝﾌﾟflagとして0を追加100%を超えた数字になる
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d; # \n改行削除
	$line .= '0,';
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
}


1; # 削除不可
