#================================================
# ｾﾘﾌ変更 Created by Merino
#================================================

my %e2j_serifu = (
	mes			=> 'ﾒｯｾｰｼﾞ',
	mes_win		=> '勝ちｾﾘﾌ',
	mes_lose	=> '負けｾﾘﾌ',
	mes_touitsu	=> '統一ｾﾘﾌ',
);


#=================================================
sub begin {
	$layout = 2;
	$mes .= qq|<form method="$method" action="$script">|;
	
	for my $k (qw/mes mes_win mes_lose mes_touitsu/) {
		$mes .= qq|$e2j_serifu{$k} [全角20(半角40)文字まで]：<br><input type="text" name="$k" value="$m{$k}" class="text_box_b"><br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="変更する" class="button1"></form>|;
	&n_menu;
}

sub tp_1 {
	&refresh;
	my $is_rewrite = 0;
	
	if ($in{mes} || $in{mes_win} || $in{mes_lose} || $in{mes_touitsu}) {
		for my $k (qw/mes mes_win mes_lose mes_touitsu/) {
			unless ($in{$k} eq $m{$k}) {
				&error("$e2j_serifu{$k}に不正な文字( ,;\"\'&<> )が含まれています") if $in{$k} =~ /[ ,;\"\'&<>]/;
				&error("$e2j_serifu{$k}は全角20(半角40)文字までです") if length $in{$k} > 40;
				$m{$k} = $in{$k};
				$mes .= "$e2j_serifu{$k}を$in{$k}に変更しました<br>";
				$is_rewrite = 1;
			}
		}
	}
	
	$mes .= 'やめました<br>' unless $is_rewrite;
	&n_menu;
}


1; # 削除不可
