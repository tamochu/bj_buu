require 'lib/_write_tag.cgi';
#=================================================
# BBS,CHAT補助ｻﾌﾞﾙｰﾁﾝ Created by Merino
#=================================================

#=================================================
# 書き込み処理
#=================================================
sub write_comment {
	&error('本文に何も書かれていません') if $in{comment} eq '';
	&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;
	&error('書き込み権限がありません') if (!&writer_check);

	if ($this_file =~ /$userdir\/(.*?)\//) {
		my $wid = $1;
		if (-f "$userdir/$wid/blacklist.cgi") {
			open my $fh, "< $userdir/$wid/blacklist.cgi" or &error("$userdir/$wid/blacklist.cgiﾌｧｲﾙが開けません");
			while (my $line = <$fh>) {
				my($blackname) = split /<>/, $line;
				if ($blackname eq $m{name}) {
					&error('ﾌﾞﾗﾀﾓﾘ');
				}
			}
			close $fh;
		}
	}

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	return 0 if $in{comment} eq $hcomment;
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("連続投稿は禁止しています。<br>しばらく待ってから書き込んでください");
	}
	push @lines, $head_line;

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}

	# この位置で判断すると情勢を取得できるプログラムからの呼び出しと、
	# そうでないプログラムからの呼び出しで匿名が効いたり効かなかったり
	# 情勢を取得できるプログラムからの呼び出しだった場合には強制的に匿名になるため、
	# 手っ取り早い対処法として「<hr>【宣伝言板へのレス】」を含んでいるならば匿名にはしない
	if ( ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) && $in{comment} !~ "<hr>【宣伝言板へのレス】") {
		$mname = "名無し";
	}

	my %bbs_config = ();
	$bbs_config{shogo_limit} = 16;
	my $this_config = $this_file . '_config.cgi';
	if (-f $this_config) {
		open my $fhc, "< $this_config" or &error("$this_config ﾌｧｲﾙが開けません");
		my $config_line = <$fhc>;
		for my $config_hash (split /<>/, $config_line) {
			my($k, $v) = split /;/, $config_hash;
			$bbs_config{$k} = $v;
		}
	}
	my $mshogo = length($m{shogo}) > $bbs_config{shogo_limit} ? substr($m{shogo}, 0, $bbs_config{shogo_limit}) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('voice');
	}
	
	return 1;
}


#=================================================
# ﾒﾝﾊﾞｰ取得
#=================================================
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub writer_check {
	if (@writer_member > 0) {
		for my $member (@writer_member) {
			if ($m{name} eq $member) {
				return 1;
			}
		}
		return 0;
	}
	return 1;
}

1; # 削除不可
