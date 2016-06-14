#標準出力へのprintを抑制
package StopStdout;
sub TIEHANDLE { my $class = shift; my @lines; bless \@lines, $class; }
sub PRINT {}
1;
