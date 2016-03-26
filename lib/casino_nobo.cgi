#================================================
# nobojs
#================================================
require './lib/_comment_tag.cgi';
require './lib/_nobo_common.cgi';

use lib './lib';
use NobO;
use JSON;

my $game_file = $logdir . '/nobo.cgi';
my $this_log_file = $userdir . '/' . $id . '/nobo_letter.cgi';

$enchant_game .= qq|<script type="text/javascript" src="$htmldir/ui.enchant.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/widget.enchant.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/jquery.periodicalupdater.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/md5.js?$jstime" charset="cp932"></script>\n|;

$enchant_game .= qq|<script type="text/javascript" src="$htmldir/NobOGame.js?$jstime" charset="utf-8"></script>\n|;
$enchant_game .= qq|<script type="text/javascript" src="$htmldir/nobo.js?$jstime" charset="cp932"></script>\n|;

sub run {
	if ($in{mode} eq "new_game") {
		$in{comment} = &new_game;
		&write_comment;
	} elsif ($in{mode} eq "move") {
		&move;
	} elsif ($in{mode} eq "trade") {
		&trade;
	} elsif ($in{mode} eq "territory_name_set") {
		&territory_name_set;
	} elsif ($in{mode} eq "write" && $in{comment}) {
		&write_comment;
	}
	my ($member_c, $member) = &get_member;


	print qq|<table><tr>|;
	print qq|<td>|;
	print qq|<div id="enchant-stage"></div>|;
	print qq|<input type="hidden" id="name" name="name" value="$m{name}">|;
	if ($is_smart) {
		print qq|<input type="hidden" id="smart" name="smart" value="1">|;
	}
	print qq|</td>|;

	print qq|<td>|;
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id" id="id"><input type="hidden" name="pass" value="$pass" id="pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form><br>|;
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="button" id="new_game" value="領地放棄" class="button1">|;
	print qq|</form>|;
	print qq|<h2>$this_title</h2>|;
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

	print qq|<td>|;
	print qq|<div id="logDiv">|;
	if (-f $this_log_file) {
		open my $fh, "< $this_log_file" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
		my $i = 0;
		while (my $line = <$fh>) {
			$i++;
			if ($i > 5) {
				last;
			}
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
			print qq|$bcomment <font size="1">($bdate)</font><hr size="1">\n|;
		}
		close $fh;
	}
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

sub new_game {
	my $nobo = &getNobO($id);
	$nobo->newGame($id);
	&saveNobO($nobo);
	
	return "$m{name}は新しい領地を得ました。";
}

sub move {
	my $nobo = &getNobO($id);
	$nobo->move($id, $in{from}, $in{to}, $in{amount});
	&saveNobO($nobo);
}

sub trade {
	my $nobo = &getNobO($id);
	$nobo->trade($id, $in{from}, $in{to});
	&saveNobO($nobo);
}

sub territory_name_set {
	my $nobo = &getNobO($id);
	$nobo->territoryNameSet($id, $in{at}, $in{territory_name});
	&saveNobO($nobo);
}

1;