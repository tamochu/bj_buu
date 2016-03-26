sub run {
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|$member_c 人が閲覧中|;
	print qq|<CENTER>\n|;
	print qq|<TABLE cellspacing="4" border="1">\n|;
	print qq|  <TBODY>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD colspan="2" align="center"><FONT size="+3">「汝は人狼なりや？」</FONT></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD colspan="2" height="5" bgcolor="#333333"></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD align="center" rowspan="2" valign="top">\n|;
	print qq|      <TABLE cellpadding="4" cellspacing="1" bgcolor="#333333">\n|;
	print qq|        <TBODY>\n|;
	print qq|          <TR>\n|;
	print qq|            <TD align="center"><B>menu</B></TD>\n|;
	print qq|          </TR>\n|;
	print qq|          <TR>\n|;
	print qq|            <TD bgcolor="#ffffff" align="center"><A href="rule.htm"><B>ルールを見る</B></A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=entry&id=$id&pass=$pass" target="_top"><B>村民登録</B><BR>\n|;
	print qq|            （プレイヤー登録）</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=room&id=$id&pass=$pass"><B>村に行く</B><BR>\n|;
	print qq|            （ログイン）</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=log&id=$id&pass=$pass"><B>過去の記録</B><BR>\n|;
	print qq|            （ログ参照）</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="log_buu.cgi?id=$id&pass=$pass"><B>過去の記録</B><BR>\n|;
	print qq|            （削除参照）</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=master&id=$id&pass=$pass">村の作成/削除<BR>\n|;
	print qq|            </A></TD>\n|;
	print qq|          </TR>\n|;
	print qq|        </TBODY>\n|;
	print qq|      </TABLE>\n|;
	print qq|      </TD>\n|;
	print qq|      <TD><B>○ゲームの開始方法</B></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD valign="top">１．左のメニューから「村民登録」を選んで登録画面にいき各項目を入力して登録を押してください。<BR>\n|;
	print qq|      ※すでにゲームが開始されている場合、村民が22名いる場合は登録できません。<BR>\n|;
	print qq|      ２．左のメニューから「村に行く」を選択します。<BR>\n|;
	print qq|      ３．村に入ります。<BR>\n|;
	print qq|      ４．人数があるていど集ったと管理者が判断するとゲームを開始します<BR>\n|;
	print qq|      　　それまでは適当に雑談していてください<BR>\n|;
	print qq|      ５．管理者がゲーム開始を宣言します。<BR>\n|;
	print qq|      　　ゲームが開始されると自動的に各自に役目が割り振られます。<BR>\n|;
	print qq|      <BR>\n|;
	print qq|      </TD>\n|;
	print qq|    </TR>\n|;
	print qq|  </TBODY>\n|;
	print qq|</TABLE>\n|;
	print qq|</CENTER>\n|;
	print qq|</BODY>\n|;
	print qq|</HTML>\n|;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @members, "<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members - 1;

	return ($member_c, $member);
}

1;