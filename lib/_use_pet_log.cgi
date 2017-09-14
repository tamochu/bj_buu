#================================================
# 城壁システム Created by nanamie
#================================================

# require './lib/_use_pet_log.cgi';

# 23 ｱﾏﾂﾐ、ｾﾞｳｽ、ｸｯｷｰ、ﾏﾙｽ、ｴﾋﾞｽ、ﾉｱ、ﾒｼｱ、ｼｸﾞﾏ、ﾛﾌﾟﾄ、ﾕﾀﾞ、ﾌｪﾝﾘﾙ、
# ﾒﾃｵ、ﾍﾟｽﾄ、ﾍﾞﾙﾌｪ、ﾘｳﾞｧ、ﾍﾞﾙｾﾞ、ﾏﾓﾝ、ｱｽﾓ、ﾂｸﾖﾐ、ｱﾎﾟﾛﾝ、ｱﾙｶ、ｲｰｽﾀｰ、ﾛｽﾀｲﾑ
@country_pets = (61, 64..71, 134..145, 151..152);

#================================================
# ﾍﾟｯﾄの生け贄ﾛｸﾞを取得
#================================================
sub read_use_pet_log {
	my ($id, $pet) = @_;
	my $this_file = "$userdir/$id/use_pet_log.cgi";
	my %pet_logs;

	unless (-f "$this_file") {
		open my $fh1, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
		close $fh1;
	}

	open my $fh2, "< $this_file" or &error("ﾍﾟｯﾄの生け贄ﾛｸﾞﾌｧｲﾙが開けません");
	my $line = <$fh2>;
	close $fh2;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$pet_logs{$k} = $v if !defined($pet) || $pet && $pet == $k; # 何かバグ報告されて !defined 足した覚えはあるけど理由忘れた… 未定義である必要が我ながらよく分からない
	}

	return $pet ? $pet_logs{$pet} : %pet_logs;
}

#================================================
# ﾍﾟｯﾄの生け贄ﾛｸﾞを設定
#================================================
sub write_use_pet_log {
	my ($id, $pet) = @_;
	my $this_file = "$userdir/$id/use_pet_log.cgi";
	my %pet_logs;

	if (-f "$this_file") {
		open my $fh, "+< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		my $line = <$fh>;

		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$pet_logs{$k} = $v;
		}

		$pet_logs{$pet}++;

		$line = '';
		for my $k (keys(%pet_logs)) {
			$line .= "$k;$pet_logs{$k}<>";
		}

		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh $line;
		close $fh;
	}
	else {
		open my $fh, "> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
		print $fh "$pet;1<>";
		close $fh;
	}
}

#================================================
# ﾍﾟｯﾄの生け贄ﾛｸﾞを表示（ﾌﾟﾚｲﾔｰのﾌﾟﾛﾌｨｰﾙ用）
#================================================
sub show_use_pet_log {
	my $id = shift;
	my %pet_logs = &read_use_pet_log($id);

	for $pet (0 .. $#pets) {
		print qq|<li>$pets[$pet][1] $pet_logs{$pet}回</li><hr size="1">\n| if defined($pet_logs{$pet});
	}
}

1;
