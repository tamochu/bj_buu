# 祭り情勢の開始と終了に紐づくので 1 ずつ空ける
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sanngokushi' => 3,
	'konnrann' => 5,
	'sessoku' => 7,
	'dokuritsu' => 9
};

# 祭り情勢の名称と、開始時なら 1 終了時 なら 0を指定する
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

1;
