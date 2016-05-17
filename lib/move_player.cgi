#================================================
# 移籍・ﾕｰｻﾞｰ削除・自作ｱｲｺﾝ削除 Created by Merino
#================================================
# admin.cgi、country_move.cgi、prison.cgi、login.cgi、war.cgiなどで使用
# ﾒﾝﾊﾞｰﾌｧｲﾙから移動。代表なら名前を取り除く
# ※国のﾘｽﾄを移動 or 削除するだけなので、移動する場合はﾌﾟﾚｲﾔｰﾃﾞｰﾀを変更する処理が必要
#   例：$m{country} = 国No; または &regist_you_data('名前', 'country', '国No');など


#================================================
# member.cgiを変更する
#================================================
sub move_player {
	my($name, $from_country, $to_country) = @_;

	# 国ﾒﾝﾊﾞｰﾘｽﾄから取り除き、移動先に追加
	my %sames = ();
	my @lines = ();
	my $is_find = 0;
	open my $fh, "+< $logdir/$from_country/member.cgi" or &error("$logdir/$from_country/member.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;

		# 同じ名前の人が複数いる場合
		next if ++$sames{$line} > 1;
		
		if ($line eq $name) {
			$is_find = 1;
			next;
		}
		push @lines, "$line\n";
	}
	if ($is_find) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		--$cs{member}[$from_country];
	}
	close $fh;
	
	my $p_id = unpack 'H*', $name;
	my %datas = ();
	%datas = &get_you_datas($p_id, 1) if -f "$userdir/$p_id/user.cgi";
	
	unless ($from_country eq '0') {
		# 投票しているのがあれば
		&check_vote(%datas) if $datas{vote};
	
		# 代表者系取り除く
		for my $key (qw/ceo war dom mil pro/) {
			if ($cs{$key}[$from_country] eq $name) {
				$cs{$key}[$from_country] = '';
				if($key ne 'ceo'){
					$m{$key.'_c'} = int($m{$key.'_c'} / 2);
					$cs{$key.'_c'}[$from_country] = 0;
				}
			}
		}
	}

	if ($to_country eq 'del') {
		&delete_user($p_id, %datas) if -d "$userdir/$p_id";
	
		&write_entry_news("$nameという者が去りました");
	}
	else {
		open my $fh9, ">> $logdir/$to_country/member.cgi" or &error("$logdir/$to_country/member.cgiﾌｧｲﾙが開けません");
		print $fh9 "$name\n";
		close $fh9;
		++$cs{member}[$to_country];
	}
#	&refresh_new_commer;
	&write_cs;
}


#================================================
# 投票していたらその票を除く
#================================================
sub check_vote {
	my %datas = @_;
	
	my @lines = ();
	open my $fh, "+< $logdir/$datas{country}/leader.cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($vname, $vote) = split /<>/, $line;
		next if $datas{name} eq $vname; # 立候補していた場合は消す

		if ($datas{vote} eq $vname) { # 一票削除
			--$vote;
			$line = "$vname<>$vote<>\n";
		}
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#================================================
# ﾕｰｻﾞｰﾃﾞｰﾀを削除
#================================================
sub delete_user {
	my($p_id, %datas) = @_;
	
	opendir my $dh, "$userdir/$p_id";
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		
		if (-d "$userdir/$p_id/$file_name") {
			opendir my $dh2, "$userdir/$p_id/$file_name";
			while (my $file_name2 = readdir $dh2) {
				next if $file_name2 =~ /^\./;
				unlink "$userdir/$p_id/$file_name/$file_name2";
			}
			closedir $dh2;
			
			rmdir "$userdir/$p_id/$file_name";
		}
		else {
			unlink "$userdir/$p_id/$file_name";
		}
	}
	closedir $dh;
	rmdir "$userdir/$p_id";
	--$w{player};
	
	# 自作ｱｲｺﾝ削除
	unlink "$icondir/$datas{icon}" if $datas{icon} ne $default_icon && -f "$icondir/$datas{icon}";
}


1; # 削除不可
