#================================================
# 麻雀js
#================================================
require "$datadir/casino_bonus.cgi";
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

use lib './lib';
use MahjongGame;

my @files = (
#	[0]番号		[1]ファイル名				[2]ログファイル名				[3]レート
	[0,			$logdir . '/mahjong1.cgi',	$logdir . '/chat_casino_m.cgi',	1000]
);

$enchant_game .= qq|<script type="text/javascript" src="$htmldir/Box2dWeb-2.1.a.3.js?$jstime"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/PhySprite.enchant.js?$jstime"></script>\n|;

$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongPai.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongPhyPai.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongDispPai.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongTehai.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongHo.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongYama.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongPlayerInfo.js?$jstime" charset="cp932"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/MahjongGame.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/mahjong.js?$jstime" charset="cp932"></script>\n|;

sub run {
	if ($in{mode} eq "drop") {
		&drop_pai;
	}
	elsif ($in{mode} eq "eat") {
		$in{comment} = &eat;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "cancel") {
		&cancel;
	}
	elsif ($in{mode} eq "kan") {
		$in{comment} = &kan;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "reach") {
		$in{comment} = &reach;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "hora") {
		&hora;
	}
	elsif ($in{mode} eq "noHuro") {
		&no_huro;
	}
	elsif ($in{mode} eq "tedumi") {
		&tedumi;
	}
	elsif ($in{mode} eq "tsumikomi") {
		&tsumikomiSet;
	}
	elsif ($in{mode} eq "force_start") {
		$in{comment} = &start_game_f;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "start") {
		$in{comment} = &start_game;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "participate") {
		$in{comment} = &participate;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
		$in{comment} = &exit_game;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "kill") {
		$in{comment} = &kill_game;
		&write_comment if $in{comment};
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;


	print qq|<table><tr>|;
	print qq|<td>|;
	print qq|<div id="enchant-stage"></div>|;
	print qq|<input type="hidden" id="no" name="no" value="0"><input type="hidden" id="name" name="name" value="$m{name}">|;
	if ($is_smart) {
		print qq|<input type="hidden" id="smart" name="smart" value="1">|;
	}
	print qq|</td>|;

	print qq|<td>|;
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id" id="id"><input type="hidden" name="pass" value="$pass" id="pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="mode" value="kill">|;
	print qq|<input type="submit" value="ちゃぶ台返し" class="button1"></form>|;
	print qq|<form method="$method" action="mahjong_ajax.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="no" value="0">|;
	print qq|<input type="hidden" name="md5" value="status">|;
	print qq|<input type="checkbox" name="noPlay" value="1">|;
	print qq|<input type="submit" value="ajax" class="button1"></form>|;
	if (!&isPlaying) {
		if (&isParty) {
			print qq|<form method="$method" action="$this_script">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="hidden" name="mode" value="exit">|;
			print qq|<input type="submit" value="退席" class="button1"></form>|;
			if (&isReady) {
				print qq|<form method="$method" action="$this_script">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="hidden" name="mode" value="start">|;
				print qq|<input type="submit" value="開始" class="button1"></form>|;
			} else {
				print qq|<form method="$method" action="$this_script">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="hidden" name="mode" value="force_start">|;
				print qq|<input type="submit" value="NPC開始" class="button1"></form>|;
			}
		} else {
			print qq|<form method="$method" action="$this_script">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="submit" value="着席" class="button1"></form>|;
		}
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|自動ﾘﾛｰﾄﾞ<select name="reload_time" class="select1"><option value="0">なし|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]秒| : qq|<option value="$i">$reload_times[$i]秒|;
		}
		print qq|</select>|;
	}
	print qq|</form>|;
	print qq|<div id="body_mes"><font size="2">$member_c人:$member</font><br>|;
	
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	my $i = 0;
	while (my $line = <$fh>) {
		$i++;
		if ($i > 7) {
			last;
		}
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment = &comment_change($bcomment, 1);
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
	print qq|</div>|;
	print qq|</td>|;
	print qq|</tr></table>|;
}
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub isParty {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	return defined($mahjong->nameToPosition($id));
}

sub isReady {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	return $mahjong->isReady();
}

sub isPlaying {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	return $mahjong->isPlaying();
}

sub drop_pai {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->dropPai($mahjong->nameToPosition($id), $in{arg});
	saveMahjongData($mahjong);
}

sub cancel {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->noEat($mahjong->nameToPosition($id));
	saveMahjongData($mahjong);
}

sub eat {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->eat($mahjong->nameToPosition($id), $in{arg});
	saveMahjongData($mahjong);
	
	return $in{arg} == 3 ? 'カン':
			$in{arg} == 2 ? 'ポン':
							'チー';
}

sub kan {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->kan($mahjong->nameToPosition($id), $in{arg});
	saveMahjongData($mahjong);
	
	return 'カン';
}

sub reach {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->reach($mahjong->nameToPosition($id));
	saveMahjongData($mahjong);
	
	return 'リーチ';
}

sub hora {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	my %mes = $mahjong->hora($mahjong->nameToPosition($id));
	if ($mes{Mes}) {
		&system_comment($mes{Mes});
	}
	if ($mes{Mes2}) {
		&system_comment($mes{Mes2});
	}
	if (defined($mes{Finish})) {
		my $fname;
		if ($mes{Finish}->name() =~ /dummy/) {
			$fname = $mes{Finish}->name();
		} else {
			$fname = pack 'H*', $mes{Finish}->name();
		}
		if (defined($mes{Drop})) {
			my $dname;
			if ($mes{Drop}->name() =~ /dummy/) {
				$dname = $mes{Drop}->name();
			} else {
				$dname = pack 'H*', $mes{Drop}->name();
			}
			&system_comment($fname . "ロン" . $dname . "放銃");
		} else {
			&system_comment($fname . "ツモ");
		}
	}
	if ($mes{Yakuman}) {
		&yakuman_bonus($mes{Yakuman});
	}
	if ($mes{EndMes}) {
		&system_comment($mes{EndMes});
		my @point = ($mes{Pos0}, $mes{Pos1}, $mes{Pos2}, $mes{Pos3});
		@point = sort {$a->point() <=> $b->point() || $b->position() <=> $a->position()} @point;
		my $top_point = 0;
		for my $r (0..3) {
			my $move_point = $point[$r]->point() - 30000;
			if ($move_point % 1000 > 0) {
				$move_point += 1000;
			}
			$move_point = int($move_point / 1000);
			if ($r == 0) {
				$move_point -= 30;
			} elsif ($r == 1) {
				$move_point -= 10;
			} elsif ($r == 2) {
				$move_point += 10;
			}
			my $pname;
			if ($point[$r]->name() =~ /dummy/) {
				$pname = $point[$r]->name();
				$move_point = 0;
			} else {
				$pname = pack 'H*', $point[$r]->name();
			}
			if ($r == 3) {
				$move_point = $top_point;
			} else {
				$top_point -= $move_point;
			
			}
			my $rank = $r == 0 ? 'ラス': (4 - $r) . '位';
			my $point_str = $move_point > 0 ? '+' . $move_point:
							$move_point < 0 ? $move_point:
												'+-0';
			&system_comment($rank . $pname . '(' . $point_str . ')');
			if ($move_point != 0) {
				&coin_move($move_point * $files[$fileno][3], $pname);
			}
		}
	}
	saveMahjongData($mahjong);
}

sub no_huro {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->noHuro($mahjong->nameToPosition($id));
	saveMahjongData($mahjong);
}

sub tedumi {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	my %mes = $mahjong->sipaiTedumi($mahjong->nameToPosition($id), $in{arg});
	if ($mes{startDice}) {
		&system_comment($mes{startDice});
	}
	saveMahjongData($mahjong);
}

sub tsumikomiSet {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->tsumikomiSet($mahjong->nameToPosition($id), $in{arg});
	saveMahjongData($mahjong);
}

sub start_game {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->startGame();
	saveMahjongData($mahjong);
	
	return 'ゲームを開始します。';
}

sub start_game_f {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->participate('dummy1');
	$mahjong->participate('dummy2');
	$mahjong->participate('dummy3');
	$mahjong->participate('dummy4');
	$mahjong->startGame();
	saveMahjongData($mahjong);
	
	return 'ゲームを開始します。';
}

sub participate {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->participate($id);
	saveMahjongData($mahjong);
	
	return '着席しました。';
}

sub exit_game {
	my $mahjong = MahjongGame->new();
	if (-f $files[$fileno][1]) {
		$mahjong = getMahjongData();
	}
	$mahjong->cancelParticipate($id);
	saveMahjongData($mahjong);
	
	return '退席しました。';
}

sub kill_game {
	open my $fh, "> $files[$fileno][1]" or &error("ゲームファイル読み込みエラー");
	close $fh;
	
	return 'ゲームを強制終了しました。（罰金-10000ｺｲﾝ）';
}

sub yakuman_bonus{
	my $name = shift;
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	&system_comment("$name は役満祝儀として $prize を獲得しました");
	&write_send_news(qq|<font color="#FF0000">$name が役満を上がりました</font>|);

}

sub getMahjongData {
	my $mahjong = MahjongGame->new();
	open my $fh, "< $files[$fileno][1]" or &error("ゲームファイル読み込みエラー");
	my $str = '';
	while (my $line = <$fh>) {
		$str .= $line;
	}
	$mahjong->readState($str);
	return $mahjong;
}

sub saveMahjongData {
	my $mahjong = shift;
	open my $fh, "+< $files[$fileno][1]" or &error("ゲームファイル読み込みエラー");
	eval { flock $fh, 2; };
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $mahjong->stateString();
	close $fh;
}
1;