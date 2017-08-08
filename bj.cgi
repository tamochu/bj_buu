#!/usr/local/bin/perl --
use Time::HiRes;
$load_time = Time::HiRes::time unless $load_time;
use CGI::Carp qw(fatalsToBrowser);
require 'config.cgi';
require 'config_game.cgi';
#================================================
# Ò²İCGI Created by Merino
#================================================
&get_data;
&error("Œ»İÒİÃÅİ½’†‚Å‚·B‚µ‚Î‚ç‚­‚¨‘Ò‚¿‚­‚¾‚³‚¢(–ñ $mente_min •ªŠÔ)") if ($mente_min);
&before_bj;
if ($m{wt} > 0) { # S‘©ŠÔ
	# S‘©’†‚É‚Å‚«‚és“®‚ÆÌ§²Ù‚Ì’è‹`
	my @menus = (
		['¤l‚Ì‚¨“X',	'shopping_akindo'],
		['µ°¸¼®İ‰ïê',	'shopping_auction'],
		['ÌŞ¯¸Ï°¹¯Ä',	'shopping_akindo_book'],
		['”ü‚Ì‰æ”ŒŠÙ',	'shopping_akindo_picture'],
	);

	# S‘©’†‚Ìs“®
	if ($m{lib_r} ne '' && -f "./lib/$m{lib_r}.cgi") { # lib_r ŒÄ‚Ño‚µ
		if ($m{tp_r} eq '1' && $cmd eq '0') { # beginÒÆ­°‚Å0(‚â‚ß‚é)‚ğ‘I‘ğ·¬İ¾Ù
			$m{lib_r} = $m{tp_r} = '';
		}
		else {
			if ($m{tp_r}) { # lib_r ˆ—
				require "./lib/$m{lib_r}.cgi";
				&{ 'tp_'.$m{tp_r} } if &is_satisfy; # is_satisfy‚ª1(true)‚È‚çˆ—‚·‚é
			}
			else { # begin ÒÆ­°
				&b_menu(@menus);
			}
		}
	}
	else {
		&b_menu(@menus) if defined($cmd);
	}

	# ƒeƒXƒgI—p‚ÌS‘©‰ğœ
	if ($config_test && $in{wt_refresh}) {
		$m{wt} = 0;
	}
	# ˆÈ‰º’Êí‚ÌS‘©’†‰æ–Ê
	elsif ($is_mobile && $m{lib_r} eq '') {
		my $next_time_mes = sprintf("Ÿ‚És“®‚Å‚«‚é‚Ü‚Å %d•ª%02d•b<br>", int($m{wt} / 60), int($m{wt} % 60) );
		$mes .= &disp_now();
		$mes .= $next_time_mes;
	}
	elsif($is_smart && $m{lib_r} eq '') {
		my $next_time_mes = sprintf("%d•ª%02d•b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("–ñ<b>%d</b><b>%02d</b>•ªŒã", $nokori_time / 3600, $nokori_time % 3600 / 60);
		$mes .= &disp_now();
		$mes .= qq|\nŸ‚És“®‚Å‚«‚é‚Ü‚Å <span id="nokori_time">$next_time_mes</span>\n|;
		$mes .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$mes .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$mes .= qq|“G‘[‘O‰ñF<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> ˜A‘±<b>$m{renzoku_c}</b>‰ñ]<br>| if $m{renzoku_c};
		$mes .= qq|Ÿ‚Ì‹‹—¿‚Ü‚Å $nokori_time_mes|;
	}
	elsif ($m{lib_r} eq '') {
		my $head_mes = '';
		if (-f "$userdir/$id/letter_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC66">è†‚ª“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
		}
		if (-f "$userdir/$id/depot_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC00">—a‚©‚èŠ‚É‰×•¨‚ª“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
		}
		if (-f "$userdir/$id/goods_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC99">Ï²Ù°Ñ‚É‰×•¨‚ª“Í‚¢‚Ä‚¢‚Ü‚·</font><br>|;
		}
		my $next_time_mes = sprintf("%d•ª%02d•b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("–ñ<b>%d</b><b>%02d</b>•ªŒã", $nokori_time / 3600, $nokori_time % 3600 / 60);

		$main_screen .= &disp_now();

		$main_screen .= qq|\nŸ‚És“®‚Å‚«‚é‚Ü‚Å <span id="nokori_time">$next_time_mes</span>\n|;
		$main_screen .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$main_screen .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$main_screen .= qq|“G‘[‘O‰ñF<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> ˜A‘±<b>$m{renzoku_c}</b>‰ñ]<br>| if $m{renzoku_c};
		$main_screen .= qq|Ÿ‚Ì‹‹—¿‚Ü‚Å $nokori_time_mes<br><br>|;

		require "$datadir/twitter_bots.cgi";
		$main_screen .= &{$twitter_bots[6]};
	}
#	$menu_cmd .= qq|<form method="$method" action="bj_rest_shop.cgi">|;
#	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="pass" value="$pass">|;
#	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="“X‚És‚­" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="“X‚És‚­" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

	# S‘©’†‚És“®‚µ‚Ä‚È‚¢
	unless ($m{lib_r}) {
		&n_menu;
		&menu( map { $_->[0] } @menus );
	}

	if ($config_test) {
		$menu_cmd .= qq|<form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="wt_refresh" value="1">|;
		$menu_cmd .= $is_mobile ? qq|<input type="submit" value="S‘©‰ğœ" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="S‘©‰ğœ" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}
}
else {
	if (-f "./lib/$m{lib}.cgi") { # lib ŒÄ‚Ño‚µ
		if ($m{tp} eq '1' && $cmd eq '0') { # beginÒÆ­°‚Å0(‚â‚ß‚é)‚ğ‘I‘ğ·¬İ¾Ù
			if ($m{lib} =~ /shopping_/) {
				require './lib/shopping.cgi';
				&refresh;
				$m{lib} = 'shopping';
			}
			else {
				$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
				require './lib/main.cgi';
				&refresh;
			}
		}
		else {
			require "./lib/$m{lib}.cgi";
		}
	}
	else { # ÃŞÌ«ÙÄlib ŒÄ‚Ño‚µ
		require './lib/main.cgi';
	}
	
	if ($m{tp}) { # lib ˆ—
		&{ 'tp_'.$m{tp} } if &is_satisfy; # is_satisfy‚ª1(true)‚È‚çˆ—‚·‚é
	}
	else { # begin ÒÆ­°
		$m{tp} = 1;
		&begin;
	}
}

&auto_heal unless $is_battle;
$is_mobile ? require './lib/template_mobile_base.cgi' :
	$is_smart ? require './lib/template_smart_base.cgi' :
	$is_appli ? require './lib/template_appli_base.cgi' : require './lib/template_pc_base.cgi';
&write_user;
&footer;
# ------------------
# ŠÔ‚É‚æ‚è‰ñ•œ
sub auto_heal {
	my $v = $time - $m{ltime}; 
	$v = &use_pet('heal_up', $v);
	$v = int( $v / $heal_time ); 
	$m{hp} += $v;
	$m{mp} += int($v * 0.8);
	$m{hp} = $m{max_hp} if $m{hp} > $m{max_hp};
	$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
}

sub disp_now {
	my $state = "‚»‚Ì‘¼";
	if($m{lib} eq 'domestic'){
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "”_‹Æ’†‚Å‚·";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "¤‹Æ’†‚Å‚·";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "’¥•º’†‚Å‚·";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "¬‹K–Í";
			}elsif($m{turn} eq '3'){
				$state = "‘å‹K–Í";
			}elsif($m{turn} eq '4'){
				$state = "’´‹K–Í";
			}else{
				$state = "’†‹K–Í";
			}
			$state .= "’·Šú“à­’†‚Å‚·";
		}
	}elsif($m{lib} eq 'military'){
		$state = "$cs{name}[$y{country}]‚ÖˆÚ“®’†‚Å‚·";
		if($m{tp} eq '110'){
			$state .= "(‹­’D)";
		}elsif($m{tp} eq '210'){
			$state .= "(’³•ñ)";
		}elsif($m{tp} eq '310'){
			$state .= "(ô”])";
		}elsif($m{tp} eq '410'){
			$state .= "(’ã@)";
		}elsif($m{tp} eq '510'){
			$state .= "(‹UŒv)";
		}elsif($m{tp} eq '610'){
			$state .= "(Ué)";
		}elsif($m{tp} eq '710'){
			if($m{value} eq 'military_ambush'){
				$state = "ŒR–";
			}else{
				$state = "iŒR";
			}
			$state .= "‘Ò‚¿•š‚¹’†‚Å‚·";
		}elsif($m{tp} eq '810'){
			$state .= "(’·Šú‹­’D)";
		}elsif($m{tp} eq '910'){
			$state .= "(’·Šú’³•ñ)";
		}elsif($m{tp} eq '1010'){
			$state .= "(’·Šúô”])";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{name}[$y{country}]‚Ì˜S–‚Å—H•Â’†‚Å‚·";
	}elsif($m{lib} eq 'promise'){
		$state = "$cs{name}[$y{country}]‚ÖˆÚ“®’†‚Å‚·";
		if($m{tp} eq '110'){
			$state .= "(—FD)";
		}elsif($m{tp} eq '210'){
			$state .= "(’âí)";
		}elsif($m{tp} eq '310'){
			$state .= "(éí•z)";
		}elsif($m{tp} eq '410'){
			$state .= "(“¯–¿ŒğÂ)";
		}elsif($m{tp} eq '510'){
			$state .= "(“¯–¿”jŠü)";
		}elsif($m{tp} eq '610'){
			$state = "“¯–¿‘‚ÖˆÚ“®’†‚Å‚·(H—¿—A‘—)";
		}elsif($m{tp} eq '710'){
			$state = "“¯–¿‘‚ÖˆÚ“®’†‚Å‚·(‘‹à—A‘—)";
		}elsif($m{tp} eq '810'){
			$state = "“¯–¿‘‚ÖˆÚ“®’†‚Å‚·(•ºm—A‘—)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "$cs{name}[$y{country}]‚ÖˆÚ“®’†‚Å‚·";
		if($m{value} eq '0.5'){
			$state .= "(­”iŒR)";
		}elsif($m{value} eq '1'){
			$state .= "(iŒR)";
		}elsif($m{value} eq '1.5'){
			$state .= "(’·Šú‰“ª)";
		}
	}
	return "$state<br>\n";
}

1; # íœ•s‰Â login.cgi‚Å bj.cgi‚ğrequire‚µ‚Ä‚¢‚é
