#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ﾌﾟﾚｲﾔｰﾘｾｯﾄ処理 Created by Merino
#================================================

&decode;
&header;
&run;
&footer;
exit;


#================================================
sub run {
	&refresh_player if defined $in{login_name} && defined $in{pass};

	print <<"EOM";
<form action="$script_index">
	<input type="submit" value="ＴＯＰ" class="button1">
</form>

<h2>ﾌﾟﾚｲﾔｰﾘｾｯﾄ処理</h2>

<div class="mes">
	<ul>
		<li>画面に何も表\示されなくなってしまった
		<li>変な無限ﾙｰﾌﾟに陥ってしまったなどの緊急処理
		<li>この処理は本当にどうしようもなくなった時以外使用しないように!
		<li>まずは、二次被害三次被害にならないように掲示板などに報告すること
		<li>何をしていて、どのﾀｲﾐﾝｸﾞでそうなってしまったのかバグった内容を詳しく報告すること
		<li><font color="#FF0000">使用ﾍﾟﾅﾙﾃｨ：ｽﾃｰﾀｽﾀﾞｳﾝ、$shogos[1][0]の称号、$GWT分拘束</font>
		<li>牢獄での救助や拘束状態を解除するものではないので注意!
	</ul>
</div>
<br>
<form method="$method" action="reset_player.cgi">
<table class="table1">
	<tr><th><tt>ﾌﾟﾚｲﾔｰ名:</tt></th><td><input type="text" name="login_name" class="text_box1"></td></tr>
	<tr><th><tt> ﾊﾟｽﾜｰﾄﾞ:</tt></th><td><input type="password" name="pass" class="text_box1"></td></tr>
</table>
<p><input type="submit" value="ﾘｾｯﾄ" class="button_s"></p>
</form>
EOM
}

# =========================================================
# 画面が表示されない、ハマった場合に使用(何かしらの異常ｴﾗｰの時)
# 管理画面のﾘｾｯﾄにﾍﾟﾅﾙﾃｨがついただけ
sub refresh_player {
	&read_user;
	
	if ($m{lib}) {
		$m{lib} = $m{tp} = '';
		for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
			$m{$k} = int($m{$k} * 0.9) if $m{$k} > 5;
		}
		&wait;
		$m{shogo} = $shogos[1][0];
		
		&write_user;
		
		&error("$m{name}にﾘｾｯﾄ処理をしました<br>");
	}
	else {
		&error('すでにﾘｾｯﾄ処理がされています');
	}
}

