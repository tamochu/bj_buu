require "$datadir/seed_templates.cgi";
#================================================
# 新種族テンプレート選択
#================================================

#================================================
sub begin {
	$m{tp} = 100;
	&n_menu;
}
sub tp_1  {
	$m{tp} = 100;
	&n_menu;
}

sub tp_100  {
	$mes .= "テンプレートを選んでください。";
	$layout = 2;
	&show_templates;
	$m{tp} = 200;
	&n_menu;
}

sub tp_200 {
	if ($cmd ne '1') {
		&begin;
		return;
	}

	unless ($in{seed_name}) {
		$mes .= "種族名が設定されていません。";
		&begin;
		return;
	}
	
	my $pt = 0;
	my %sames = ();
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			$pt += $seed_templates[$i][3];
			my @seed_keys = keys(%{$seed_templates[$i][2]});
			for my $key (@seed_keys) {
				if ($sames{$key}++) {
					$mes .= "同系統のステータス($key)は同時に選べません。";
					&begin;
					return;
				}
			}
		}
	}

	if ($pt > $m{stock}) {
		$mes .= "選択したステータス値が大きすぎます。";
		&begin;
		return;
	}
	
	&create_seed;
	&refresh;
	&n_menu;
}

sub show_templates {
	$mes .= qq|振り分け可能\pt$m{stock}<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|種族名：<input type="text" name="seed_name"/><br>|;
	$mes .= qq|<table class="table1"><tr><th>選択</th><th>能\力名</th><th>ステータス値<br></th></tr>| unless $is_mobile;
	
	for my $i (0..$#seed_templates) {
		$mes .= $is_mobile ? qq|<input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/> / $seed_templates[$i][1] / $seed_templates[$i][3]<br>|
						 : qq|<tr><td><input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/></td><td>$seed_templates[$i][1]</td><td>$seed_templates[$i][3]<br></td></tr>|;
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>新種族の持つ能\力などの要望（実装するとは限らない）</p>|;
	$mes .= qq|<textarea name="free"></textarea>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="cmd" value="1">|;
	$mes .= qq|<p><input type="submit" value="決定" class="button1"></p></form>|;
	$mes .= qq|<h3>新種族作成の説明</h3>|;
	$mes .= qq|<p>新種族転生時には、まずﾎﾟｲﾝﾄを割り振って種族の大まかな能\力について決めてください。ﾎﾟｲﾝﾄの初期値は1～2のランダムですが、各能\力の合計値が初期値に収まれば問題ないのでマイナスのデメリット能\力と組み合わせることで高ﾎﾟｲﾝﾄの能\力を選択することができます。また、新種族特有の能\力など思い付くものがあればコメント欄に書いてください。</p>|;
}

sub create_seed {
	$new_seed = "new_seed_" . $time . $id;
	$fecundity = 10;
	$new_seed_name = $in{seed_name};
	$bonus_line = <<"EOM";
		'default' => sub {
			\$v = shift;
			return \$v;
		}
EOM
	my $pt = 0;
	my $seed_detail_line = '';
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			for my $key (keys(%{$seed_templates[$i][2]})) {
				if ($key eq 'fecundity') {
					$fecundity += $seed_templates[$i][2]->{$key};
				} else {
					$bonus_line .= $seed_templates[$i][2]->{$key};
				}
			}
			$pt += $seed_templates[$i][3];
			$seed_detail_line .= $seed_templates[$i][1];
		}
	}
	$blank_line = <<"EOM";
\@$new_seed = (
	'$seed_name',
	{
$bonus_line
	},
	$fecundity,
	'$seed_detail_line'
);

1;
EOM
	open my $fh, "> $add_seeds_dir/$new_seed.cgi";
	print $fh $blank_line;
	close $fh;
	chmod 0666, "$add_seeds_dir/$new_seed.cgi";
	$m{seed} = $new_seed;
	
	$in{comment} = qq|$m{name} さんが新種族$new_seed_nameになりました。至急対応をお願いします。<br>|;
	$in{comment} .= qq|キー : $m{seed}<br>|;
	$in{comment} .= qq|振り分けpt $pt / $m{stock}<br>|;
	if ($in{free}) {
		$in{comment} .= qq|自由入力<br>|;
		$in{comment} .= $in{free};
	}
	my $mname = $m{name};
	$m{name} = "システム";
	&send_letter($admin_name, 0);
	&send_letter($admin_sub_name, 0);
	$m{name} = $mname;
}

1; # 削除不可
