#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ﾒｲﾝCGI Created by Merino
#================================================
&get_data;
&error("現在ﾒﾝﾃﾅﾝｽ中です。しばらくお待ちください(約 $mente_min 分間)") if $mente_min;

if ($m{wt} > 0) { # 拘束時間
	require './lib/shopping_akindo_r.cgi';
	if ($m{tp_r} eq '1' && $cmd eq '0' || $m{tp_r} > 610) { # beginﾒﾆｭｰで0(やめる)を選択時ｷｬﾝｾﾙ
			$mes .= 'やめました<br>';
			$m{tp_r} = 0;
	}
	
	if ($m{tp_r}) { # lib 処理
		&{ 'tp_'.$m{tp_r} } if &is_satisfy; # is_satisfyが1(true)なら処理する
	}
	else { # begin ﾒﾆｭｰ
		$m{tp_r} = 1;
		&begin;
	}
}
$menu_cmd .= qq|<form method="$method" action="$script">|;
$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
$menu_cmd .= $is_mobile || $is_smart ? qq|<input type="submit" value="やめる" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="やめる" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

&auto_heal unless $is_battle;
$is_mobile || $is_smart ? require './lib/template_mobile_base.cgi' : require './lib/template_pc_base.cgi';
&write_user;
&footer;

# ------------------
# 時間により回復
sub auto_heal {
	my $v = $time - $m{ltime}; 
	$v = &use_pet('heal_up', $v);
	$v = int( $v / $heal_time ); 
	$m{hp} += $v;
	$m{mp} += int($v * 0.8);
	$m{hp} = $m{max_hp} if $m{hp} > $m{max_hp};
	$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
}


1; # 削除不可 login.cgiで bj.cgiをrequireしている
