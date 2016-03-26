#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
# 連続書き込み禁止時間(秒)
$bad_time    = 10;
# 最大ﾛｸﾞ保存件数
$max_log     = 50;
# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 10000;
# ﾒﾝﾊﾞｰに表示される時間(秒)
$limit_member_time = 60 * 4;
# 最大過去ﾛｸﾞ保存件数
$max_bbs_past_log = 5;

#=================================================
# 共通掲示板 Created by Merino
#=================================================
&get_data;
&error("商人でない方は入れません") unless $m{akindo_guild};
&error("ただ今ギルド閉鎖中です");

$m{guild_number} = 1 unless $m{guild_number};

$this_title  = "商人のギルド";
$this_file   = "$logdir/bbs_akindo_$m{guild_number}";
$this_subfile   = $this_file . '_sub';
$this_script = 'bbs_akindo.cgi';
$member_list = $this_file . "_allmember";
$min_value = $this_file . "_value";
$log_back = 'bbs_akindo';
$shop_file = $logdir . '/guild_shop' . $m{guild_number} . '.cgi';
$sale_file = $logdir . '/guild_shop' . $m{guild_number} . '_sale.cgi';

$flag_share = 0;
$flag_value = 0;

#=================================================
sub write_list{
	my $list;
	my @item_list = ();
	open my $sfh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$sfh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display) = split /<>/, $line;
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";
		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_nameの商品が読み込めません");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>\n";
			}
			close $ifh;
		}
	}
	close $sfh;

	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;

	my $pre_kind = -1;
	my $pre_no = -1;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name) = split /<>/, $line;
		if($kind == $pre_kind && $item_no == $pre_no){
			next;
		}
		$list .= $kind eq '1' ? "|$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
			  : $kind eq '2' ? "|$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
			  : 			   "|$pets[$item_no][1]"
			  ;
		$list .= "|$price G|$name|<br>";
		$pre_kind = $kind;
		$pre_no = $item_no;
	}
	
	
	my @lines = ();
	my $this_log = $this_file . "_log";
	open my $fh, "+< $this_log.cgi" or &error("$this_log.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_bbs_past_log-1;
	}
	unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$list<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	@lines = ();
	open my $fh2, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh2, 2; };
	while (my $line = <$fh2>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	$out_mes = '価格一覧を出力しました';
	unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$out_mes<>$m{icon}<>\n";
	seek  $fh2, 0, 0;
	truncate $fh2, 0;
	print $fh2 @lines;
	close $fh2;
	$mes .= "書き込みをﾛｸﾞ保存しました<br>";
}

sub shop_check{
	my $shop_comment = '';
	my @lines = ();
	my @sub_lines = ();
	
	open my $fh2, "< $sale_file" or &error("$sale_fileが読み込めません");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money, $update_t) = split /<>/, $line;
	$shop_comment .= "ギルド積立金：$sale_money G 売上個数：$sale_c 個<br>";
	
	
	open my $fhv, "+< $min_value.cgi" or &error('価格ﾘｽﾄﾌｧｲﾙが開けません');
	my $w_line = <$fhv>;
	my @v_weapon = split /<>/, $w_line;
	my $e_line = <$fhv>;
	my @v_egg = split /<>/, $e_line;
	my $p_line = <$fhv>;
	my @v_pet = split /<>/, $p_line;
	
	open my $fhs, "+< $shop_file" or &error("$shop_fileが開けません");
	eval { flock $fhs, 2; };
	
	while (my $line = <$fhs>){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$item_no = 42.5 if($kind == 2 && $item_no == 53);
		$item_no = 76.5 if($kind == 3 && $item_no == 180);
		$item_no = 77.5 if($kind == 3 && $item_no == 181);
		$item_no = 194.5 if ($kind == 3 && $item_no == 195);
		$price = $kind == 1 ? $v_weapon[$item_no]:
				$kind == 2 ? $v_egg[$item_no]:
							$v_pet[$item_no];
		$line = "$no<>$kind<>$item_no<>$item_c<>$item_lv<>$price<>\n";
		push @lines, $line;
	}
	@lines = map { $_->[0] }
				sort { $a->[2] <=> $b->[2] || $a->[3] <=> $b->[3] }
					map { [$_, split /<>/ ] } @lines;
	my $i = 1;
	my $pre_kind = 0;
	my $pre_no = 0;
	my $count_i = 0;
	for my $line (@lines){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		if($kind == 2 && $item_no == 42.5){
			$line = "$i<>2<>53<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 76.5){
			$line = "$i<>3<>180<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 77.5){
			$line = "$i<>3<>181<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 194.5){
			$line = "$i<>3<>195<>$item_c<>$item_lv<>$price<>\n";
		}else {
			$line = "$i<>$kind<>$item_no<>$item_c<>$item_lv<>$price<>\n";
		}
		push @sub_lines, $line;
		if($kind == $pre_kind && $item_no == $pre_no){
			$count_i++;
		}else{
			if($count_i){
				$shop_comment .= "$count_i 個|<br>";
			}
			$shop_comment .= $kind == 1 ? "|$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])":
							$kind == 2 ? "|$eggs[$item_no][1]($item_c/$eggs[$item_no][2])":
							"|$pets[$item_no][1]";
			$shop_comment .= "|$price|";
			$count_i = 1;
		}
		$i++;
		$pre_kind = $kind;
		$pre_no = $item_no;
	}
	$shop_comment .= "$count_i 個|<br>";
	
	seek  $fhs, 0, 0;
	truncate $fhs, 0;
	print $fhs @sub_lines;
	close $fhs;
	
	$in{comment} = $shop_comment;
	&write_comment;
	$mes .= "店頭商品一覧出力しました<br>";
}

sub value_change{
	open my $fhv, "+< $min_value.cgi" or &error('価格ﾘｽﾄﾌｧｲﾙが開けません');
	my $w_line = <$fhv>;
	my @v_weapon = split /<>/, $w_line;
	my $e_line = <$fhv>;
	my @v_egg = split /<>/, $e_line;
	my $p_line = <$fhv>;
	my @v_pet = split /<>/, $p_line;
	my $w_n_line = '';
	my $e_n_line = '';
	my $p_n_line = '';
	
	for my $i (0..$#weas){
		my $value = $v_weapon[$i];
		if($in{ch_mat} eq "w$i"){
			$value = $in{value};
		}
		if($value =~ /[^0-9]/ || !$value){
			$value = 9999999;
		}
		$w_n_line .= "$value<>"
	}
	$w_n_line .= "\n";
	for my $i (0..$#eggs){
		my $value = $v_egg[$i];
		if($in{ch_mat} eq "e$i"){
			$value = $in{value};
		}
		if($value =~ /[^0-9]/ || !$value){
			$value = 9999999;
		}
		$e_n_line .= "$value<>"
	}
	$e_n_line .= "\n";
	for my $i (0..$#pets){
		my $value = $v_pet[$i];
		if($in{ch_mat} eq "p$i"){
			$value = $in{value};
		}
		if($value =~ /[^0-9]/ || !$value){
			$value = 9999999;
		}
		$p_n_line .= "$value<>"
	}
	$p_n_line .= "\n";
	seek  $fhv, 0, 0;
	truncate $fhv, 0;
	print $fhv $w_n_line;
	print $fhv $e_n_line;
	print $fhv $p_n_line;
	close $fhv;
}

sub share_sale{
	my @for_vote = @_;
	my $member_n = @for_vote;
	my $shop_comment = '';
	
	
	open my $fha, "< $member_list.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	my $headline = <$fha>;
	my($gname, $gcolor) = split /<>/, $headline;
	close $fha;
	
	open my $fh2, "< $sale_file" or &error("$sale_fileが読み込めません");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money, $update_t) = split /<>/, $line;
	if($in{share} * $member_n < $sale_money && $in{share} !~ /[^0-9]/ && $in{share} > 0){
		$sale_money -= int($in{share} * $member_n);
		for my $s_name (@for_vote){
			&send_money($s_name, "【$gname】$m{name}", int($in{share}));
		}
	}
	open my $fh2, "> $sale_file" or &error("$sale_fileが読み込めません");
	print $fh2 "$sale_c<>$sale_money<>$update_t<>";
	close $fh2;
	$shop_comment .= "分配金を$in{share} $member_n 人に払いました<br>ギルド積立金：$sale_money G<br>";
	
	$in{comment} = $shop_comment;
	&write_comment;
}

sub sub_vote{
	my @lines = ();
	open my $sfh, "+< $this_subfile.cgi" or &error("$this_subfile.cgi ﾌｧｲﾙが開けません");
	eval { flock $sfh, 2; };
	while (my $line = <$sfh>) {
		my($no, $kind, $itemno, $value, $member_yes, $member_no) = split /<>/, $line;
		my @ymem = split /,/, $member_yes;
		my $num_y = @ymem;
		my @nmem = split /,/, $member_no;
		my $num_n = @nmem;
		if($in{vote_no} == $no){
			if($in{vote_yn} eq 'no'){
				if($num_n > 0){
					$member_no .= ",$m{name}";
				}else{
					$member_no = "$m{name}";
				}
				$num_n++;
			}else{
				$member_yes .= ",$m{name}";
				$num_y++;
			}
		}
		next if $num_n > 3;
		if($num_y > 3){
			if($kind eq 'share'){
				$flag_share = 1;
				$in{share} = $value;
			}elsif($kind eq 'weapon'){
				$flag_value = 1;
				$in{ch_mat} = "w$itemno";
				$in{value} = $value;
			}elsif($kind eq 'egg'){
				$flag_value = 1;
				$in{ch_mat} = "e$itemno";
				$in{value} = $value;
			}elsif($kind eq 'pet'){
				$flag_value = 1;
				$in{ch_mat} = "p$itemno";
				$in{value} = $value;
			}
			next;
		}
		push @lines, "$no<>$kind<>$itemno<>$value<>$member_yes<>$member_no<>\n";
	}
	seek  $sfh, 0, 0;
	truncate $sfh, 0;
	print $sfh @lines;
	close $sfh;
}

sub add_share{
	my @lines = ();
	my $last_no = 1;
	open my $sfh, "+< $this_subfile.cgi" or &error("$this_subfile.cgi ﾌｧｲﾙが開けません");
	eval { flock $sfh, 2; };
	while (my $line = <$sfh>) {
		my($no, $kind, $itemno, $value, $member_yes, $member_no) = split /<>/, $line;
		push @lines, "$no<>$kind<>$itemno<>$value<>$member_yes<>$member_no<>\n";
		$last_no = $no;
	}
	$last_no++;
	push @lines, "$last_no<>share<>0<>$in{share}<>$m{name}<><>\n";
	seek  $sfh, 0, 0;
	truncate $sfh, 0;
	print $sfh @lines;
	close $sfh;
}

sub add_value{
	my @lines = ();
	my $last_no = 1;
	open my $sfh, "+< $this_subfile.cgi" or &error("$this_subfile.cgi ﾌｧｲﾙが開けません");
	eval { flock $sfh, 2; };
	while (my $line = <$sfh>) {
		my($no, $kind, $itemno, $value, $member_yes, $member_no) = split /<>/, $line;
		push @lines, "$no<>$kind<>$itemno<>$value<>$member_yes<>$member_no<>\n";
		$last_no = $no;
	}
	my $t_kind;
	my $t_no;
	my $t_find = 0;
	for my $i (0..$#weas){
		if($in{ch_mat} eq "w$i"){
			$t_kind = 'weapon';
			$t_no = $i;
			$t_find = 1;
		}
	}
	for my $i (0..$#eggs){
		last if $t_find;
		if($in{ch_mat} eq "e$i"){
			$t_kind = 'egg';
			$t_no = $i;
			$t_find = 1;
		}
	}
	for my $i (0..$#pets){
		last if $t_find;
		if($in{ch_mat} eq "p$i"){
			$t_kind = 'pet';
			$t_no = $i;
			$t_find = 1;
		}
	}
	$last_no++;
	push @lines, "$last_no<>$t_kind<>$t_no<>$in{value}<>$m{name}<><>\n";
	seek  $sfh, 0, 0;
	truncate $sfh, 0;
	print $sfh @lines;
	close $sfh;
}

#=================================================

if ($in{mode} eq "write" && $in{comment}) {
	&write_comment;

	# 保存ﾛｸﾞ用
	if ($in{is_save_log}) {
		if (&is_daihyo) {
			my $sub_this_file = $this_file;
			$this_file .= "_log";
			$max_log = $max_bbs_past_log;
			&write_comment;
			$this_file = $sub_this_file;
			$mes .= "書き込みをﾛｸﾞ保存しました<br>";
		}
		else {
			$mes .= "国の代表\者以外はﾛｸﾞ保存はできません<br>";
		}
	}
}

if ($in{mode} eq "list") {
	&write_list;
}

if ($in{mode} eq "shop_check") {
	&shop_check;
}

if ($in{mode} eq "sub_vote") {
	&sub_vote;
}

if ($in{mode} eq "confiscate") {
	&confiscate_shop($m{guild_number}, 1);
}

my($member_c, $member) = &get_member;

my $is_find_a = 0;
my $member_a  = '';
my @members_a = ();
my %sames_a = ();
my %voted = ();
my $guild_master = '';
my $max_voted = 1;
my @for_vote = ();
my $pre_vote = '';
my $m_vote = $m{name};

open my $fha, "+< $member_list.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
eval { flock $fha, 2; };
my $headline = <$fha>;
my($gname, $gcolor) = split /<>/, $headline;
$this_title = $gname if $gname;
while (my $line = <$fha>) {
	my($mname, $vote, $master) = split /<>/, $line;
	next if $sames_a{$mname}++; # 同じ人なら次
	next unless $mname;
	
	if($in{mode} eq "m_refresh"){
		my $shop_id = unpack 'H*', $mname;
		if(-f "$userdir/$shop_id/shop.cgi"){
			my %datas1 = &get_you_datas($mname);
			if($datas1{guild_number} != $m{guild_number}){
				if($mname eq $guild_master){
					$guild_master = '';
					$max_voted = 0;
				}
				next;
			}
		}else{
			if($mname eq $guild_master){
				$guild_master = '';
				$max_voted = 0;
			}
			next;
		}
	}
	
	$voted{$vote}++;

	if ($mname eq $m{name}) {
		$is_find_a = 1;
		$m_vote = $vote;
		if ($in{mode} eq "vote_ch") {
			$pre_vote = $vote;
			$vote = $in{v_name};
			$m_vote = $in{v_name};
		}
	}
	if ($master) {
		$guild_master = $mname;
		$max_voted = $master;
	}else {
		push @members_a, "$mname<>$vote<><>\n";
	}
	push @for_vote, $mname;
	$member_a .= "$mname,";
}
$max_voted-- if($pre_vote eq $guild_master && $in{v_name} ne $guild_master);
unshift @members_a, "$guild_master<>$guild_master<>$max_voted<>\n";
if($in{mode} eq "master_ch" && $m{name} eq $guild_master){
	my $is_rewrite = 0;
	if ($in{gname} || $in{gcolor}) {
		unless ($gname eq $in{gname}) {
			&error("ギルド名を記入してください") if $in{gname} eq '';
			&error("ギルド名に不正な文字( ,;\"\'&<>\\\/ )が含まれています") if $in{gname} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("ギルド名に不正な空白が含まれています") if $in{gname} =~ /　/ || $in{gname} =~ /\s/;
			&error("ギルド名は全角7(半角14)文字までです") if length $in{gname} > 14;
			
			$gname = $in{gname};
		}
		unless ($gcolor eq $in{gcolor}) {
			&error('色を半角英数字で記入してください') if $in{gcolor} eq '' || $in{gcolor} =~ /[^0-9a-zA-Z#]/;
			&error('色を#から始まる16進数の色で記入してください') if $in{gcolor} !~ /#.{6}/;
			$gcolor = $in{gcolor};
		}
	}
}
unshift @members_a, "$gname<>$gcolor<>\n";

unless ($is_find_a) {
	push @members_a, "$m{name}<>$m{name}<><>\n";
	$member_a .= "$m{name},";
}
my $member_ca = @members_a - 1;
my $is_changed = 0;

if($in{mode} eq "m_refresh"){
	$max_voted = 0;
}
while (my($name, $v_num) = each(%voted)){
	next unless ($sames_a{$name});
	if ($v_num > $max_voted){
		$max_voted = $v_num;
		$guild_master = $name;
		$is_changed = 1;
	}
}
if ($is_changed) {
	my @c_mem = ();
	for my $line (@members_a) {
		my($mname, $vote, $master) = split /<>/, $line;
		if ($mname eq $guild_master) {
			push @c_mem, "$mname<>$vote<>$max_voted<>\n";
		}else {
			push @c_mem, "$mname<>$vote<><>\n";
		}
	}
	@members_a = @c_mem;
}
seek  $fha, 0, 0;
truncate $fha, 0;
print $fha @members_a;
close $fha;
if($in{mode} eq "value_ch" && $m{name} eq $guild_master){
	&add_value;
}
if($in{mode} eq "share" && $m{name} eq $guild_master){
	&add_share;
}
if($flag_value){
	&value_change;
}
if($flag_share){
	&share_sale(@for_vote);
}

$this_title = $gname if $gname;
print qq|<form method="$method" action="$script">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<input type="submit" value="戻る" class="button1"></form>|;
print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
print qq|<p>$mes</p>| if $mes;

print qq|<form method="$method" action="past_log.cgi"><input type="hidden" name="this_title" value="$this_title">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<input type="hidden" name="this_file" value="$this_file"><input type="hidden" name="this_script" value="$log_back">|;
print qq|<input type="submit" value="過去ﾛｸﾞ" class="button_s"></form>|;

my $rows = $is_mobile ? 2 : 5;
print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
print qq|<input type="submit" value="書き込む" class="button_s">|;
print qq|　 <input type="checkbox" name="is_save_log" value="1">ﾛｸﾞ保存</form><br>|;


print qq|あなたは$m_voteに投票しています<br>|;
print qq|投票<form method="$method" action="$this_script"><input type="hidden" name="mode" value="vote_ch"><select name="v_name" class="menu1">|;
for my $i (@for_vote) {
	next if $i eq '';
	if($i eq $m_vote){
		print qq|<option value="$i" selected>$i</option>|;
	}else {
		print qq|<option value="$i">$i</option>|;
	}
}
print qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
print qq|<input type="submit" value="決 定" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="shop_check">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<input type="submit" value="直営店販売物一覧" class="button_s"></form>|;

if($m{name} eq $guild_master){
	print qq|貴方がギルドマスターです<br>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="master_ch">|;
	print qq|ギルド名：<input type="text" name="gname" value="$gname" class="text_box1"><br>|;
	print qq|色：<input type="text" name="gcolor" value="$gcolor" class="text_box1"><br>|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<p><input type="submit" value="変更する" class="button1"></p></form>|;
	
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="list">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="最安値一覧出力" class="button_s"></form>|;
	
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="share">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="text" name="share" value="10000" class="text_box1">G<input type="submit" value="積立金分配" class="button_s"></form>|;
}

print qq|<font size="2">$member_c人:$member</font><hr>|;

print qq|<font size="2">ギルドマスター:$guild_master  所属$member_ca人:$member_a</font><hr>|;

open my $sfh, "< $this_subfile.cgi" or &error("$this_subfile.cgi ﾌｧｲﾙが開けません");
while (my $line = <$sfh>) {
	my($no, $kind, $itemno, $value, $member_yes, $member_no) = split /<>/, $line;
	my @ymem = split /,/, $member_yes;
	my $num_y = @ymem;
	my @nmem = split /,/, $member_no;
	my $num_n = @nmem;
	my $gc = $gcolor ? $gcolor:$cs{color}[$bcountry];
	my $bmes;
	my $voted_yn = 0;
	for my $i (@ymem){
		if($m{name} eq $i){
			$voted_yn = 1;
		}
	}
	for my $i (@nmem){
		if($m{name} eq $i){
			$voted_yn = 1;
		}
	}
	my $buttons;
	unless($voted_yn){
		$buttons = qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="sub_vote"><input type="hidden" name="vote_no" value="$no"><input type="hidden" name="vote_yn" value="yes"><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON"><input type="submit" value="賛成" class="button_s"></form><br>|;
		$buttons .= qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="sub_vote"><input type="hidden" name="vote_no" value="$no"><input type="hidden" name="vote_yn" value="no"><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON"><input type="submit" value="反対" class="button_s"></form>|;
	}
	if($kind eq 'share'){
		$bmes = "$value Gの売上金分配案が出ています賛成者 $num_y 人,反対者 $num_n 人";
	}elsif($kind eq 'weapon'){
		$bmes = "$weas[$itemno][1] の $value Gへの基準値変更案が出ています賛成者 $num_y 人,反対者 $num_n 人";
	}elsif($kind eq 'egg'){
		$bmes = "$eggs[$itemno][1] の $value Gへの基準値変更案が出ています賛成者 $num_y 人,反対者 $num_n 人";
	}elsif($kind eq 'pet'){
		$bmes = "$pets[$itemno][1] の $value Gへの基準値変更案が出ています賛成者 $num_y 人,反対者 $num_n 人";
	}
	if ($is_mobile) {
		print qq|<div><font color="$gc">$bmes</font>$buttons</div><hr size="1">\n|;
	}
	else {
		print qq|<table border="0"><tr><td valign="top"><font color="$gc">$bmes</font><br></td><td>$buttons</td></tr></table><hr size="1">\n|;
	}
}
close $sfh;

open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
while (my $line = <$fh>) {
	my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	my $gc = $gcolor ? $gcolor:$cs{color}[$bcountry];
	$bname .= "[$bshogo]" if $bshogo;
	$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
	$bcomment = &comment_change($bcomment, 1);
	if ($is_mobile) {
		print qq|<div>$bicon<font color="$gc">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font></div><hr size="1">\n|;
	}
	else {
		print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon<br><font color="$gc">$bname</font></td><td valign="top"><font color="$gc">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br></td></tr></table><hr size="1">\n|;
	}
}
close $fh;

print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="m_refresh">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<input type="submit" value="メンバー一覧修正" class="button_s"></form>|;

print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="confiscate">|;
print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
print qq|<input type="submit" value="廉売品没収" class="button_s"></form>|;

open my $fhv, "< $min_value.cgi" or &error('価格ﾘｽﾄﾌｧｲﾙが開けません');
my $w_line = <$fhv>;
my @v_weapon = split /<>/, $w_line;
my $e_line = <$fhv>;
my @v_egg = split /<>/, $e_line;
my $p_line = <$fhv>;
my @v_pet = split /<>/, $p_line;
close $fhv;
unless($is_mobile){
print qq|最低価格一覧<br>|;
	if($m{name} eq $guild_master){
		print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="value_ch"><select name="ch_mat" class="menu1">|;
		my $selected = 1;
		for my $i (1..$#weas) {
			if($selected){
				print qq|<option value="w$i" selected>$weas[$i][1]</option>|;
				$selected = 0;
			}else{
				print qq|<option value="w$i">$weas[$i][1]</option>|;
			}
		}
		for my $i (1..$#eggs) {
			next if($i == 53);
			print qq|<option value="e$i">$eggs[$i][1]</option>|;
		}
#		for my $i (1..$#pets){
#			next if($i == 180 || $i == 181 || $i == 195);
#			print qq|<option value="p$i">$pets[$i][1]</option>|;
#		}
		print qq|<input type="text" name="value" value="0" class="text_box1">G<br>|;
		print qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|<input type="submit" value="変更する" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}
	for my $i (1..$#weas){
		next if $v_weapon[$i] >= 9999999;
		print qq|$weas[$i][1]：$v_weapon[$i]G<br>|;
	}
	for my $i (1..$#eggs){
		next if($i == 53);
		next if $v_egg[$i] >= 9999999;
		print qq|$eggs[$i][1]：$v_egg[$i]G<br>|;
	}
#	for my $i (1..$#pets){
#		next if($i == 180 || $i == 181 || $i == 195);
#		next if $v_pet[$i] >= 9999999;
#		print qq|$pets[$i][1]：$v_pet[$i]G<br>|;
#	}
}
&footer;
exit;
