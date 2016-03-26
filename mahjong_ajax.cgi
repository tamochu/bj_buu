#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use lib './lib';
use MahjongGame;
use JSON;

my @files = (
#	[0]番号		[1]ファイル名				[2]ログファイル名				[3]レート
	[0,			$logdir . '/mahjong1.cgi',	$logdir . '/chat_casino_m.cgi',	1000]
);

&decode;
&read_user;
&access_check;
&read_cs;

$in{no} ||= 0;
$in{no} = int($in{no});
if ($in{no} < 0 || $in{no} >= @files) {
	$in{no} = 0;
}
print "Content-type: applecation/json; charset=utf-8\n\n";
&run;

sub run {
	my $mahjong = MahjongGame->new();
	$mahjong->setObserver($id);
	my $md5 = $in{oldMd5} ? $in{oldMd5} : '';
	if (-f $files[$in{no}][1]) {
		$mahjong = getMahjongData();
		$mahjong->setObserver($id);
		if (!$md5) {
			$md5 = $mahjong->md5();
		}
	}
	if ($mahjong->isPlaying()) {
		if ($mahjong->points(0)->name() eq $id) {
			my %mes = $mahjong->play();
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
					if ($move_point != 0 && $point[$r]->name() !~ /dummy/) {
						&coin_move($move_point * $files[$in{no}][3], $pname);
					}
				}
			}
			saveMahjongData($mahjong);
		} else {
			if (-f $files[$in{no}][1]) {
				my $start_time = time;
				while ($mahjong->md5() eq $md5) {
					$mahjong = getMahjongData();
					$mahjong->setObserver($id);

					sleep 1;
					my $now = time;
					if ($now - $start_time > 10) {
						last;
					}
				}
			}
		}
	} else {
		if ($mahjong->isReady()) {
			$mahjong->startGame();
			saveMahjongData($mahjong);
			&system_comment('ゲームを開始します。');
		}
	}
	my $coder = JSON->new->utf8->convert_blessed;
	print $coder->encode($mahjong);
}


sub coin_move{
	my ($m_coin, $name) = @_;
	
	if($m_coin > 0){
		&system_comment("$name は $m_coin ｺｲﾝ得ました");
	}else{
		my $temp = -1 * $m_coin;
		&system_comment("$name は $temp ｺｲﾝ払いました");
	}
	if($name eq $m{name}){
		my $temp = $m{coin} + $m_coin;
		$temp = 0 if $temp < 0;
		$m{coin} = $temp;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $m_coin;
		$temp = 0 if $temp < 0;
		&regist_you_data($name, 'coin', $temp);
	}
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

sub system_comment{
	my $s_mes = shift;
	$s_mes =~ s/&/&amp/g;
	$s_mes =~ s/;/&#59;/g;
	$s_mes =~ s/&amp/&amp;/g;
	$s_mes =~ s/,/&#44;/g;
	$s_mes =~ s/</&lt;/g;
	$s_mes =~ s/>/&gt;/g;
	$s_mes =~ s/"/&quot;/g;#"
	$s_mes =~ s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]//g;
	$s_mes =~ s/\.\.\///g;
	$s_mes =~ s/【ダイス】/(ダイス)/g;
	my $file_name = $files[$in{no}][2];

	my @lines = ();
	open my $fh, "+< $file_name" or &error("$file_name ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	
	# ｵｰﾄﾘﾝｸ
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>system messge<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

sub getMahjongData {
	my $mahjong = MahjongGame->new();
	open my $fh, "< $files[$in{no}][1]" or &error("ゲームファイル読み込みエラー");
	my $str = '';
	while (my $line = <$fh>) {
		$str .= $line;
	}
	close $fh;
	$mahjong->readState($str);
	return $mahjong;
}

sub saveMahjongData {
	my $mahjong = shift;
	open my $fh, "+< $files[$in{no}][1]" or &error("$files[$in{no}][1]ゲームファイル読み込みエラー");
	eval { flock $fh, 2; };
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $mahjong->stateString();
	close $fh;
}
exit;
