#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbsd.cgi';
#=================================================
# 代表専用掲示板 Created by Merino
#=================================================
&get_data;
#&error("$cs{name}[0]の方は入れません") if $m{country} eq '0';
#&error("国の代表\者でないと入れません") unless &is_daihyo;

$this_title  = "各国代表\評議会";
$this_file   = "$logdir/bbs_daihyo";
$this_script = 'bbs_daihyo.cgi';
$this_violator_file = "$logdir/violator.cgi";

@violate = ('島流し', '斬首', '永久追放');

# 君主の議決によりﾌﾟﾚｲﾔｰ削除権限(0:なし,1:あり)
my $is_ceo_delete = 1;

# 削除権限ありの場合。必要経過日数
my $non_new_commer_date = 30;
my $is_delete = $config_test ? 1 : $m{start_time} + $non_new_commer_date * 24 * 3600 < $time;

# 削除権限ありの場合。必要票
my @need_vote_violator = (2, 4, 5);

#=================================================
&vote;
&run;
&print_vote;
&footer;
exit;

sub print_vote {
	return unless &is_ceo;

	print '<hr>流刑者ﾘｽﾄ<br>';
	open my $fh, "< $this_violator_file" or &error("$this_violator_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		
		unless ($name) {
			next;
		}
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$lv |= 0;
		
		print qq|<font color="$cs{color}[$country]">$cs{name}[$country]</font>の$e2j{ceo}$nameが『$violator』を$violate[$lv]すべきと思っています<br>|;
		print qq|理由：$message<br>|;
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="cmd" value="$no">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="answer" value="1"><input type="submit" value="賛成" class="button_s"> $yes_c票：$yess<br>|;
		print qq|</form>|;
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="cmd" value="$no">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="answer" value="1"><input type="submit" value="反対" class="button_s"> $no_c票：$nos<br>|;
		print qq|</form>|;
		print qq|<hr>|;
	}
	close $fh;
}

sub vote {
	return unless &is_ceo;

	unless ($is_delete) {
		return;
	}
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_violator_file" or &error("$this_violator_fileﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		$lv |= 0;
		
		if ($cmd eq $no) {
			# 申請したのが自分で反対なら申請を取消
			if ($m{name} eq $name && $in{answer} eq '2') {
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("自分の評議には投票することができません");
			}

			my $v_id = unpack 'H*', $violator;
			# 自動削除などで消えていた場合は除外
			if (!-f "$userdir/$v_id/user.cgi") {
				next;
			}

			# すでに自分がどちらかに入れていた場合のために、一回白紙にする
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{country} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{country} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($in{answer} eq '1') {
				$new_yess .= "$m{country},";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{country},";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_c = @yes_c;
			my $no_c  = @no_c;
			
			if ($yes_c >= $need_vote_violator[$lv]) {
				if($violator eq $admin_name){
					&write_world_news("<b>【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$datas{country}]の$violatorが$violate[$lv]になりました…と思ったか、バカめ</b>");
					for my $n (@yes_c) {
						&regist_you_data($cs{ceo}[$n],'shogo','★反逆者');
						&regist_you_data($cs{ceo}[$n],'shogo_t','★反逆者');
						&regist_you_data($cs{ceo}[$n],'trick_time',$time + 30*24*3600);
						&regist_you_data($cs{ceo}[$n], 'wt', 7 * 24 * 3600);
					}
				}else{
					if ($lv > 0) {
						my %datas = &get_you_datas($v_id, 1);
						if ($lv > 1) {
							# 違反者リストに追加
							open my $fh2, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgiﾌｧｲﾙが開けません");
							open my $afh, "< $userdir/$v_id/access_log.cgi" or &error("$userdir/$v_id/access_log.cgiﾌｧｲﾙが開けません");
							while ($aline = <$afh>) {
								my ($aaddr, $ahost, $aagent)  = split /<>/, $aline;
								print $fh2 $aagent =~ /DoCoMo/ || $aagent =~ /KDDI|UP\.Browser/
									|| $aagent =~ /J-PHONE|Vodafone|SoftBank/ ? "$aagent\n" : "$aaddr\n";
							}
							close $afh;
							print $fh2 $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
								|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
							close $fh2;
						}
						&move_player($violator, $datas{country}, 'trash');
					} else {
						my %datas = &get_you_datas($v_id, 1);
						&move_player($violator, $datas{country}, 0);
						&regist_you_data($datas{name}, 'wt', 7 * 24 * 3600);
						&regist_you_data($datas{name}, 'country', 0);
						&regist_you_data($datas{name}, 'lib', '');
						&regist_you_data($datas{name}, 'tp', 0);
						&regist_you_data($datas{name},'silent_time',$time+7*24*3600);
						&regist_you_data($datas{name},'silent_kind',0);
					}
					&write_world_news("<b>【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$datas{country}]の$violatorが$violate[$lv]になりました<br>理由：$message</b>");
				}
			}
			elsif ($no_c > $w{country} - $need_vote_violator[$lv]) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # 申請した人が消えていた場合
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("【議決】各国の$e2j{ceo}達の評議により、$cs{name}[$country]の$e2j{ceo}$nameが国外追放となりました</b>", 1, $name);
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>$lv<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}