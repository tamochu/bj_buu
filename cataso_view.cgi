#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

sub header2 {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	
print << "HTML";
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<title>view</title>
<link rel="stylesheet" href="$htmldir/css/html5reset-1.6.1.css" />
<script src="$htmldir/js/view.js" charset="utf-8"></script>
<script src="$htmldir/js/enchant.min.js" charset="utf-8"></script>
<script src="$htmldir/cataso_view/Const.js" charset="utf-8"></script>
<script src="$htmldir/cataso_view/Game.js" charset="utf-8"></script>
<script>
    onLoad = function () {
        Game.onLoad();
    }
    onMessage = function (message) {
        if (Game.isOpen) { Game.onMessage(JSON.parse(message)); }
    }
</script>
</head>
<body>
HTML
}

sub run {
	print qq|<div id="enchant-stage"></div>|;
}

sub footer2 {
	print qq|</body></html>|;
}

&header2;
&run;
&footer2;
exit;
