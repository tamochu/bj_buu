#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# Ò²İCGI Created by Merino
#================================================
&get_data;
&error("Œ»İÒİÃÅİ½’†‚Å‚·B‚µ‚Î‚ç‚­‚¨‘Ò‚¿‚­‚¾‚³‚¢(–ñ $mente_min •ªŠÔ)") if $mente_min;

if ($m{wt} > 0) { # S‘©ŠÔ
	require './lib/shopping_akindo_r.cgi';
	if ($m{tp_r} eq '1' && $cmd eq '0' || $m{tp_r} > 610) { # beginÒÆ­°‚Å0(‚â‚ß‚é)‚ğ‘I‘ğ·¬İ¾Ù
			$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
			$m{tp_r} = 0;
	}
	
	if ($m{tp_r}) { # lib ˆ—
		&{ 'tp_'.$m{tp_r} } if &is_satisfy; # is_satisfy‚ª1(true)‚È‚çˆ—‚·‚é
	}
	else { # begin ÒÆ­°
		$m{tp_r} = 1;
		&begin;
	}
}
$menu_cmd .= qq|<form method="$method" action="$script">|;
$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
$menu_cmd .= $is_mobile || $is_smart ? qq|<input type="submit" value="‚â‚ß‚é" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="‚â‚ß‚é" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

&auto_heal unless $is_battle;
$is_mobile || $is_smart ? require './lib/template_mobile_base.cgi' : require './lib/template_pc_base.cgi';
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


1; # íœ•s‰Â login.cgi‚Å bj.cgi‚ğrequire‚µ‚Ä‚¢‚é
