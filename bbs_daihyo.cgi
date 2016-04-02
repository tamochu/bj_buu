#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbsd.cgi';
#=================================================
# ‘ã•\ê—pŒf¦”Â Created by Merino
#=================================================
&get_data;
#&error("$cs{name}[0]‚Ì•û‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{country} eq '0';
#&error("‘‚Ì‘ã•\\Ò‚Å‚È‚¢‚Æ“ü‚ê‚Ü‚¹‚ñ") unless &is_daihyo;

$this_title  = "Še‘‘ã•\\•]‹c‰ï";
$this_file   = "$logdir/bbs_daihyo";
$this_script = 'bbs_daihyo.cgi';
$this_violator_file = "$logdir/violator.cgi";

@violate = ('“‡—¬‚µ', 'añ', '‰i‹v’Ç•ú');

# ŒNå‚Ì‹cŒˆ‚É‚æ‚èÌßÚ²Ô°íœŒ ŒÀ(0:‚È‚µ,1:‚ ‚è)
my $is_ceo_delete = 1;

# íœŒ ŒÀ‚ ‚è‚Ìê‡B•K—vŒo‰ß“ú”
my $non_new_commer_date = 30;

# íœŒ ŒÀ‚ ‚è‚Ìê‡B•K—v•[
my @need_vote_violator = (2, 4, 6);

#=================================================
&vote;
&run;
&print_vote;
&footer;
exit;

sub print_vote {
	return unless &is_ceo;

	print '<hr>—¬ŒYÒØ½Ä<br>';
	open my $fh, "< $this_violator_file" or &error("$this_violator_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
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
		
		print qq|<font color="$cs{color}[$country]">$cs{name}[$country]</font>‚Ì$e2j{ceo}$name‚ªw$violatorx‚ğ$violate[$lv]‚·‚×‚«‚Æv‚Á‚Ä‚¢‚Ü‚·<br>|;
		print qq|——RF$message<br>|;
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="cmd" value="$no">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="answer" value="1"><input type="submit" value="^¬" class="button_s"> $yes_c•[F$yess<br>|;
		print qq|</form>|;
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="cmd" value="$no">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="hidden" name="answer" value="1"><input type="submit" value="”½‘Î" class="button_s"> $no_c•[F$nos<br>|;
		print qq|</form>|;
		print qq|<hr>|;
	}
	close $fh;
}

sub vote {
	return unless &is_ceo;

	if ($m{start_time} + $non_new_commer_date * 24 * 3600 > $time) {
		return;
	}
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_violator_file" or &error("$this_violator_fileÌ§²Ù‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		$lv |= 0;
		
		if ($cmd eq $no) {
			# \¿‚µ‚½‚Ì‚ª©•ª‚Å”½‘Î‚È‚ç\¿‚ğæÁ
			if ($m{name} eq $name && $in{answer} eq '2') {
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("©•ª‚Ì•]‹c‚É‚Í“Š•[‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ");
			}

			my $v_id = unpack 'H*', $violator;
			# ©“®íœ‚È‚Ç‚ÅÁ‚¦‚Ä‚¢‚½ê‡‚ÍœŠO
			if (!-f "$userdir/$v_id/user.cgi") {
				next;
			}

			# ‚·‚Å‚É©•ª‚ª‚Ç‚¿‚ç‚©‚É“ü‚ê‚Ä‚¢‚½ê‡‚Ì‚½‚ß‚ÉAˆê‰ñ”’†‚É‚·‚é
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
					&write_world_news("<b>y‹cŒˆzŠe‘‚Ì$e2j{ceo}’B‚Ì•]‹c‚É‚æ‚èA$cs{name}[$datas{country}]‚Ì$violator‚ª$violate[$lv]‚É‚È‚è‚Ü‚µ‚½c‚Æv‚Á‚½‚©AƒoƒJ‚ß</b>");
					for my $n (@yes_c) {
						&regist_you_data($cs{ceo}[$n],'shogo','š”½‹tÒ');
						&regist_you_data($cs{ceo}[$n],'shogo_t','š”½‹tÒ');
						&regist_you_data($cs{ceo}[$n],'trick_time',$time + 30*24*3600);
						&regist_you_data($cs{ceo}[$n], 'wt', 7 * 24 * 3600);
					}
				}else{
					if ($lv > 0) {
						my %datas = &get_you_datas($v_id, 1);
						if ($lv > 1) {
							# ˆá”½ÒƒŠƒXƒg‚É’Ç‰Á
							open my $fh2, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
							open my $afh, "< $userdir/$v_id/access_log.cgi" or &error("$userdir/$v_id/access_log.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
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
						&move_player($violator, $datas{country}, 'del');
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
					&write_world_news("<b>y‹cŒˆzŠe‘‚Ì$e2j{ceo}’B‚Ì•]‹c‚É‚æ‚èA$cs{name}[$datas{country}]‚Ì$violator‚ª$violate[$lv]‚É‚È‚è‚Ü‚µ‚½<br>——RF$message</b>");
				}
			}
			elsif ($no_c > $w{country} - $need_vote_violator[$lv]) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # \¿‚µ‚½l‚ªÁ‚¦‚Ä‚¢‚½ê‡
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("y‹cŒˆzŠe‘‚Ì$e2j{ceo}’B‚Ì•]‹c‚É‚æ‚èA$cs{name}[$country]‚Ì$e2j{ceo}$name‚ª‘ŠO’Ç•ú‚Æ‚È‚è‚Ü‚µ‚½</b>", 1, $name);
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