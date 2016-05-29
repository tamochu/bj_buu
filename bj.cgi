#!/usr/local/bin/perl --
use CGI::Carp qw(fatalsToBrowser);
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ﾒｲﾝCGI Created by Merino
#================================================
&get_data;
&error("現在ﾒﾝﾃﾅﾝｽ中です。しばらくお待ちください(約 $mente_min 分間)") if ($mente_min);
&before_bj;
if ($m{wt} > 0) { # 拘束時間
	if ($is_mobile) {
		my $next_time_mes = sprintf("次に行動できるまで %d分%02d秒<br>", int($m{wt} / 60), int($m{wt} % 60) );
		$mes .= &disp_now();
		$mes .= $next_time_mes;
	}
	elsif($is_smart) {
		my $next_time_mes = sprintf("%d分%02d秒", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("約<b>%d</b>時<b>%02d</b>分後", $nokori_time / 3600, $nokori_time % 3600 / 60);
		$mes .= &disp_now();
		$mes .= qq|\n次に行動できるまで <span id="nokori_time">$next_time_mes</span>\n|;
		$mes .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$mes .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$mes .= qq|敵国[前回：<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> 連続<b>$m{renzoku_c}</b>回]<br>| if $m{renzoku_c};
		$mes .= qq|次の給料まで $nokori_time_mes|;
	}
	else{
		my $head_mes = '';
		if (-f "$userdir/$id/letter_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC66">手紙が届いています</font><br>|;
		}
		if (-f "$userdir/$id/depot_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC00">預かり所に荷物が届いています</font><br>|;
		}
		if (-f "$userdir/$id/goods_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC99">ﾏｲﾙｰﾑに荷物が届いています</font><br>|;
		}
		my $next_time_mes = sprintf("%d分%02d秒", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("約<b>%d</b>時<b>%02d</b>分後", $nokori_time / 3600, $nokori_time % 3600 / 60);

		$main_screen .= &disp_now();

		$main_screen .= qq|\n次に行動できるまで <span id="nokori_time">$next_time_mes</span>\n|;
		$main_screen .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$main_screen .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$main_screen .= qq|敵国[前回：<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> 連続<b>$m{renzoku_c}</b>回]<br>| if $m{renzoku_c};
		$main_screen .= qq|次の給料まで $nokori_time_mes<br><br>|;

		require "$datadir/twitter_bots.cgi";
		$main_screen .= &{$twitter_bots[6]};
	}
	&n_menu;
	$menu_cmd .= qq|<form method="$method" action="bj_rest_shop.cgi">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="店に行く" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="店に行く" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

}
else {
	if (-f "./lib/$m{lib}.cgi") { # lib 呼び出し
		if ($m{tp} eq '1' && $cmd eq '0') { # beginﾒﾆｭｰで0(やめる)を選択時ｷｬﾝｾﾙ
			if ($m{lib} =~ /shopping_/) {
				require './lib/shopping.cgi';
				&refresh;
				$m{lib} = 'shopping';
			}
			else {
				$mes .= 'やめました<br>';
				require './lib/main.cgi';
				&refresh;
			}
		}
		else {
			require "./lib/$m{lib}.cgi";
		}
	}
	else { # ﾃﾞﾌｫﾙﾄlib 呼び出し
		require './lib/main.cgi';
	}
	
	if ($m{tp}) { # lib 処理
		&{ 'tp_'.$m{tp} } if &is_satisfy; # is_satisfyが1(true)なら処理する
	}
	else { # begin ﾒﾆｭｰ
		$m{tp} = 1;
		&begin;
	}
}

&auto_heal unless $is_battle;
$is_mobile ? require './lib/template_mobile_base.cgi' :
	$is_smart ? require './lib/template_smart_base.cgi' : require './lib/template_pc_base.cgi';
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

sub disp_now {
	my $state = "その他";
	if($m{lib} eq 'domestic'){
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "農業中です";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "商業中です";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "徴兵中です";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}elsif($m{turn} eq '5'){
				$state = "超規模";
			}else{
				$state = "中規模";
			}
			$state .= "長期内政中です";
		}
	}elsif($m{lib} eq 'military'){
		$state = "$cs{name}[$y{country}]へ移動中です";
		if($m{tp} eq '110'){
			$state .= "(強奪)";
		}elsif($m{tp} eq '210'){
			$state .= "(諜報)";
		}elsif($m{tp} eq '310'){
			$state .= "(洗脳)";
		}elsif($m{tp} eq '410'){
			$state .= "(偵察)";
		}elsif($m{tp} eq '510'){
			$state .= "(偽計)";
		}elsif($m{tp} eq '610'){
			if($m{value} eq 'military_ambush'){
				$state = "軍事";
			}else{
				$state = "進軍";
			}
			$state .= "待ち伏せ中です";
		}elsif($m{tp} eq '710'){
			$state .= "(長期強奪)";
		}elsif($m{tp} eq '810'){
			$state .= "(長期諜報)";
		}elsif($m{tp} eq '910'){
			$state .= "(長期洗脳)";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{name}[$y{country}]の牢獄で幽閉中です";
	}elsif($m{lib} eq 'promise'){
		$state = "$cs{name}[$y{country}]へ移動中です";
		if($m{tp} eq '110'){
			$state .= "(友好)";
		}elsif($m{tp} eq '210'){
			$state .= "(停戦)";
		}elsif($m{tp} eq '310'){
			$state .= "(宣戦布告)";
		}elsif($m{tp} eq '410'){
			$state .= "(同盟交渉)";
		}elsif($m{tp} eq '510'){
			$state .= "(同盟破棄)";
		}elsif($m{tp} eq '610'){
			$state = "同盟国へ移動中です(食料輸送)";
		}elsif($m{tp} eq '710'){
			$state = "同盟国へ移動中です(資金輸送)";
		}elsif($m{tp} eq '810'){
			$state = "同盟国へ移動中です(兵士輸送)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "$cs{name}[$y{country}]へ移動中です";
		if($m{value} eq '0.5'){
			$state .= "(少数進軍)";
		}elsif($m{value} eq '1'){
			$state .= "(進軍)";
		}elsif($m{value} eq '1.5'){
			$state .= "(長期遠征)";
		}
	}
	return "$state<br>\n";
}

1; # 削除不可 login.cgiで bj.cgiをrequireしている
