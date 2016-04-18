#================================================
# 祭り情勢の開始・終了で使われるモジュール
#================================================

#================================================
# 主な呼び出し元
# ./lib/_world_reset.cgi
# 自動的に呼ばれるので意識してロードする必要なし
#================================================

# 祭り情勢の開始と終了に紐づくので 1 ずつ空ける
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# 祭り情勢時に追加される国の数・国力・国名・国色の定義
use constant FESTIVAL_COUNTRY_PROPERTY => {
	'kouhaku' => [2, 75000, ["きのこの山", "たけのこの里"], ["#ffffff", "#ff0000"]],
	'sangokusi' => [3, 50000, ["魏", "呉", "蜀"], ["#4444ff", "#ff4444", "#44ff44"]]
};

# 不倶戴天国名
my $country_name_hug_1 = "たけのこの里";
my $country_name_hug_2 = "きのこの山";

# 三国志国名
my $country_name_san_1 = "魏";
my $country_name_san_2 = "呉";
my $country_name_san_3 = "蜀";


# 祭り情勢の名称と、開始時なら 1 終了時 なら 0 を指定する
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

# 指定された祭り情勢用の国を追加しその情勢の開始フラグを返す
# 追加される国の情報は FESTIVAL_COUNTRY_PROPERTY で定義しておく
sub add_festival_country {
	my $festival_name = shift;

	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	$w{country} += $country_num;
	my $max_c = int($w{player} / $country_num) + 3;
	for my $i ($w{country}-($country_num-1)..$w{country}){
		mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
			close $fh;
			chmod $chmod, $output_file;
		}
		for my $file_name (qw/leader member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
			close $fh;
			chmod $chmod, $output_file;
		}
		&add_npc_data($i);
		# create union file
		for my $j (1 .. $i-1) {
			my $file_name = "$logdir/union/${j}_${i}";
			$w{ "f_${j}_${i}" } = -99;
			$w{ "p_${j}_${i}" } = 2;
			next if -f "$file_name.cgi";
			open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
			close $fh;
			chmod $chmod, "$file_name.cgi";
			open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
			close $fh2;
			chmod $chmod, "${file_name}_log.cgi";
			open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
			close $fh3;
			chmod $chmod, "${file_name}_member.cgi";
		}
		unless (-f "$htmldir/$i.html") {
			open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
			close $fh_h;
		}

		my $num = $i-($w{country}+1-$country_num);
		$cs{name}[$i]     = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[2][$num];
		$cs{color}[$i]    = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[3][$num];
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 999;
		$cs{tax}[$i]      = 99;
		$cs{strong}[$i]   = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[1];
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = $max_c;
		$cs{is_die}[$i]   = 0;
		my @lines = &get_countries_mes();
		if ($w{country} > @lines - $country_num) {
			open my $fh9, ">> $logdir/countries_mes.cgi";
			print $fh9 "<>$default_icon<>\n";
			print $fh9 "<>$default_icon<>\n";
			close $fh9;
		}
	}

	for my $i (1 .. $w{country}-$country_num) {
		$cs{strong}[$i]   = 0;
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = 0;
		$cs{is_die}[$i]   = 1;

		for my $j ($i+1 .. $w{country}-$country_num) {
			$w{ "f_${i}_${j}" } = -99;
			$w{ "p_${i}_${j}" } = 2;
		}

		$cs{old_ceo}[$i] = $cs{ceo}[$i];
		$cs{ceo}[$i] = '';
		
		open my $fh, "> $logdir/$i/leader.cgi";
		close $fh;
	}

	return &festival_type($festival_name, 1);
}

1;