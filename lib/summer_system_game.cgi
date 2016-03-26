#================================================
# 夏関数
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
# 夏イベ
#================================================
sub on_summer {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 7) {
		return 1;
	}
	return 0;
}
#================================================
# 年末イベ
#================================================
sub on_december {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 11) {
		return 1;
	}
	return 0;
}
#================================================
# 新春イベ
#================================================
sub on_new_year {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 0) {
		return 1;
	}
	return 0;
}
1; # 削除不可
