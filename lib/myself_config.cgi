#================================================
# 設定変更
#================================================

#=================================================
sub begin {
	$layout = 2;
	if ($m{tp} > 1) {
		$mes .= '他に何かしますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '個人設定を変更します<br>';
	}

	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="1">|;
	$mes .= '混乱の時シャッフルされる？<br>';
	$mes .= $m{shuffle} ? qq|<input type="radio" name="shuffle" value="0">はい <input type="radio" name="shuffle" value="1" checked>いいえ <br>|:
						qq|<input type="radio" name="shuffle" value="0" checked>はい <input type="radio" name="shuffle" value="1">いいえ<br>|;

	$mes .= '対人ｶｼﾞﾉを表示する？<br>';
	$mes .= $m{disp_casino} ? qq|<input type="radio" name="disp_casino" value="1" checked>はい <input type="radio" name="disp_casino" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_casino" value="1">はい <input type="radio" name="disp_casino" value="0" checked>いいえ<br>|;

	$mes .= '交流広場をJAVA表示にする？<br>';
	$mes .= $m{chat_java} ? qq|<input type="radio" name="chat_java" value="1" checked>はい <input type="radio" name="chat_java" value="0">いいえ<br>|:
						qq|<input type="radio" name="chat_java" value="1">はい <input type="radio" name="chat_java" value="0" checked>いいえ<br>|;

	$mes .= 'TOPを表示する？<br>';
	$mes .= $m{disp_top} ? qq|<input type="radio" name="disp_top" value="1" checked>はい <input type="radio" name="disp_top" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_top" value="1">はい <input type="radio" name="disp_top" value="0" checked>いいえ<br>|;

	$mes .= '過去の栄光を表示する？<br>';
	$mes .= $m{disp_news} ? qq|<input type="radio" name="disp_news" value="1" checked>はい <input type="radio" name="disp_news" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_news" value="1">はい <input type="radio" name="disp_news" value="0" checked>いいえ<br>|;

	$mes .= '交流広場を表示する？<br>';
	$mes .= $m{disp_chat} ? qq|<input type="radio" name="disp_chat" value="1" checked>はい <input type="radio" name="disp_chat" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_chat" value="1">はい <input type="radio" name="disp_chat" value="0" checked>いいえ<br>|;

	$mes .= '宣伝言板を表示する？<br>';
	$mes .= $m{disp_ad} ? qq|<input type="radio" name="disp_ad" value="1" checked>はい <input type="radio" name="disp_ad" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_ad" value="1">はい <input type="radio" name="disp_ad" value="0" checked>いいえ<br>|;

	$mes .= '代表評議会を表示する？<br>';
	$mes .= $m{disp_daihyo} ? qq|<input type="radio" name="disp_daihyo" value="1" checked>はい <input type="radio" name="disp_daihyo" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_daihyo" value="1">はい <input type="radio" name="disp_daihyo" value="0" checked>いいえ<br>|;

	$mes .= '給料を自動で受け取る？<br>';
	$mes .= $m{salary_switch} ? qq|<input type="radio" name="salary_switch" value="0">はい <input type="radio" name="salary_switch" value="1" checked>いいえ<br>|:
						qq|<input type="radio" name="salary_switch" value="0" checked>はい <input type="radio" name="salary_switch" value="1">いいえ<br>|;

	$mes .= 'ボスを避ける？<br>';
	$mes .= $m{no_boss} ? qq|<input type="radio" name="no_boss" value="1" checked>はい <input type="radio" name="no_boss" value="0">いいえ<br>|:
						qq|<input type="radio" name="no_boss" value="1">はい <input type="radio" name="no_boss" value="0" checked>いいえ<br>|;

	$mes .= '孵化スイッチをつける？<br>';
	$mes .= $m{incubation_switch} ? qq|<input type="radio" name="incubation_switch" value="1" checked>はい <input type="radio" name="incubation_switch" value="0">いいえ<br>|:
						qq|<input type="radio" name="incubation_switch" value="1">はい <input type="radio" name="incubation_switch" value="0" checked>いいえ<br>|;

	$mes .= 'ガチャ等の残り時間を表示する？<br>';
	$mes .= $m{disp_gacha_time} ? qq|<input type="radio" name="disp_gacha_time" value="1" checked>はい <input type="radio" name="disp_gacha_time" value="0">いいえ<br>|:
						qq|<input type="radio" name="disp_gacha_time" value="1">はい <input type="radio" name="disp_gacha_time" value="0" checked>いいえ<br>|;

	$mes .= 'ブラックリストを有効にする？<br>';
	$mes .= $m{valid_blacklist} ? qq|<input type="radio" name="valid_blacklist" value="1" checked>はい <input type="radio" name="valid_blacklist" value="0">いいえ<br>|:
						qq|<input type="radio" name="valid_blacklist" value="1">はい <input type="radio" name="valid_blacklist" value="0" checked>いいえ<br>|;

	$mes .= '戦争で陣形を選ぶ？<br>';
	$mes .= $m{war_select_switch} ? qq|<input type="radio" name="war_select_switch" value="1" checked>はい <input type="radio" name="war_select_switch" value="0">いいえ<br>|:
						qq|<input type="radio" name="war_select_switch" value="1">はい <input type="radio" name="war_select_switch" value="0" checked>いいえ<br>|;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="変更" class="button1"></form>|;
		
	&menu('やめる');
}
sub tp_1 {
	return if &is_ng_cmd(1);
	
	$m{tp} = 100;
	&{ 'tp_' .$m{tp} };
}


#=================================================
# 変更
#=================================================
sub tp_100 {
	$m{shuffle} = $in{shuffle};	
	$m{disp_casino} = $in{disp_casino};
	$m{chat_java} = $in{chat_java};
	$m{disp_top} = $in{disp_top};
	$m{disp_news} = $in{disp_news};
	$m{disp_chat} = $in{disp_chat};
	$m{disp_ad} = $in{disp_ad};
	$m{disp_daihyo} = $in{disp_daihyo};
	$m{salary_switch} = $in{salary_switch};
	$m{no_boss} = $in{no_boss};
	$m{incubation_switch} = $in{incubation_switch};
	$m{disp_gacha_time} = $in{disp_gacha_time};
	$m{valid_blacklist} = $in{valid_blacklist};
	$m{war_select_switch} = $in{war_select_switch};

	&begin;
}

1; # 削除不可
