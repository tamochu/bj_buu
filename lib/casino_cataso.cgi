#================================================
# nobojs
#================================================
require './lib/_comment_tag.cgi';

$enchant_game .= qq|<link rel="stylesheet" href="$htmldir/css/html5reset-1.6.1.css?$jstime" />\n|;
$enchant_game .= qq|<link rel="stylesheet" href="$htmldir/css/room.css?$jstime" />\n|;
$enchant_game .= qq|<link rel="stylesheet" href="$htmldir/css/prettyPopin.css?$jstime" />\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/js/preloadjs-0.4.1.min.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/js/soundjs-0.5.2.min.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/js/jquery.prettyPopin.js?$jstime" charset="utf-8"></script>\n|;

sub run {
	if (!$m{cataso_ratio}) {
		$m{cataso_ratio} = 1500;
		&write_user;
	}
	print <<"HTML";
<form method="$method" action="$script">
<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">
<input type="submit" value="戻る" class="button1"></form>
<div id="wrapper">
	<div id="login">
		<div id="login-left">
			<input id="login-input-uid" type="hidden" value="$m{name}" />
			<input id="login-input-ratio" type="hidden" value="$m{cataso_ratio}" />
			<input id="login-button" type="button" onclick="login();"/>
			<div style="clear:both;"></div>
			<div id="login-error"></div>
			<div id="login-user-list"></div>
		</div>
		<div id="login-eye-catch"></div>
	</div>

	<div id="play">
		<input id="play-button-se" type="button" class="button" onclick="play_button_se();" value="効果音"/>
		<input id="play-button-bs" type="button" class="button" onclick="play_button_bs();" value="ベル音"/>
		<select id="play-select-volume">
			<option value="0.01">1%</option>
			<option value="0.03">3%</option>
			<option value="0.05">5%</option>
			<option value="0.1">10%</option>
			<option value="0.15">15%</option>
			<option value="0.2">20%</option>
			<option value="0.3">30%</option>
			<option value="0.4">40%</option>
			<option value="0.5">50%</option>
			<option value="0.6">60%</option>
			<option value="0.7">70%</option>
			<option value="0.8">80%</option>
			<option value="0.9">90%</option>
			<option value="1">100%</option>
		</select>
		<div style="clear:both;"></div>
		<div id="play-left">
			<div id="play-user-list"></div>
			<div id="play-log"></div>
		</div>
		<iframe id="play-view" src="cataso_view.cgi?id=$id&pass=$pass"></iframe>
		<div style="clear:both;"></div>
		<input id="play-input-chat" type="text" />
		<input id="play-button-dice" type="button" class="button" onclick="play_button_dice()" value="ダイス"/>
		<input id="play-button-bell" type="button" class="button" onclick="play_button_bell()" value="ベル"/>
		<input id="play-button-help" type="button" class="button" onclick="popup_help()" value="HELP"/>
	</div>
</div>

<div id="footer">
	<div id="support-browser">対応ブラウザ:&nbsp;Chrome&nbsp;16&nbsp;以降,&nbsp;Firefox&nbsp;11&nbsp;以降,&nbsp;Safari&nbsp;6&nbsp;以降,&nbsp;IE&nbsp;10&nbsp;以降</div>
	<div>powered by TkmOnline</div>
</div>

<script src="$htmldir/js/tkm-initialize.js?$jstime" charset="utf-8"></script>
<script>Tkm.roomIndex = 0;</script>
<script src="$htmldir/js/tkm-onload.js?$jstime" charset="utf-8"></script>
HTML
}

1;