package FlockWrapper;
#########################################################
# flock Wrapper
# (C)2004 PANDORA C4 script by ZeRo
# http://pandora.nu admin@pandora.nu
#########################################################
#
# 説明
# 	flockの使え無い環境で無理矢理flockを上書きして、
# 	mkdir symlik を使ったロックを実行するモジュール
#
#	このモジュールは自己責任で使って下さい。このモジュールを使い
#	いかなる支障、損害が発生してもモジュール作成者は責任をおいません。
#
# 注意
#	無理矢理flockとcloseを上書きしてるので、完璧ではありません。
#	localなどで極小化してあるGLOB(handle)と極小化していないGLOBの
#	識別ができないため、GLOB(handle)名が同じものを何度も利用している
#	ようなスクリプトには適していません。その場合は、ソースコードを
#	修正した方が早いでしょう。
#
# 使い方
#	use FlockWrapper ( 
#		flock   => ロックのモード(flock mkdir symlink)か
#		           任意のコードリファレンス,
#
#		dir     => mkdir symlinkを使ったロックを動作させる
#				   ためのデレクトリ（パーミッションは777にすること),
#				   デフォルトは "." カレントデレクトリ
#
#		try     => mkdir symlink を使ったロックでロックの取得
#                  を試みる回数指定する。
#				   デフォルトは 5 回
#
#		timeout => mkdir symlink を使ったロックで作成したロック
#				   を強制的に解除するまでの時間（秒）
#				   デフォルトは 60 秒
#
#		close   => mkdir symlink を使ったロックでflockの呼び出しと対に
#				   なるcloseを上書きするかどうか（する:1, しない:0）
#				   デフォルトは 1
#
#       clean   => スクリプト終了時にロックを解除する（する:1、しない:0）
#                  デフォルトは 1
#
#		debug   => デバック情報の出力（する:1、しない:0）
#	);
#
# DEBUG
#	use strict;
#	use lib q(.);
#	use FlockWrapper (flock => 'mkdir', dir => './lock', clean => 0, debug => 1);
#	# ↑上のように引数を指定する。
#
#	local(*IN);
#	print "handle ref: ". \*IN. "\n";
#   open(IN, "+<./lockfile") or die $!;
#	flock(IN, 2);
#	# ↑ここでスクリプトを終了すると、dirで指定したデレクトリにmkdirで
#	# 作成したデレクトリが存在する事がわかる。
#
#	close(IN);
#	# ↑ここでmkdirで作成したデレクトリが削除されてればok
#
#
# 例
#	use strict;
#	use lib q(.);
#	use FlockWrapper(flock => 'mkdir', dir => './lock');
#
#	# 元ソース
#	local(*LOCK);
#	open(LOCK, "+<lockfile") or die $!;
#	flock(LOCK, 2);
#	#↑ここを上書きして強制的にmkdirロックを実行
#
#	・・・省略・・・
#
#	close(LOCK);
#	# ↑ここも上書きしてあるので内部でロック解除する。
#
######################################################

my %args = ();
my %handle = ();

my %lock = ();
$lock{mkdir}   = \&lock_mkdir;
$lock{symlink} = \&lock_symlink;

BEGIN { sub import
{
	my $pkg = shift;
	%args = @_;

	# パラメータの初期化
	$args{dir}       = "." if !defined($args{dir});
	$args{dir}       =~ s/\/$//;
	$args{fname}     = $args{dir}. "/lockfile";
	$args{try}     ||= 10;
	$args{timeout} ||= 60;
	$args{unlocked}  = 0;
	$args{clean}     = 1 if !defined($args{clean});
	$args{close}     = 1 if !defined($args{close});
	$args{debug}   ||= 0;

	# flock と close のラッパ作成
	my $code = undef;
	if (!defined($args{flock})) {
		return;
	} elsif ($args{flock} eq 'flock') {
		return;
	} elsif (ref($args{flock}) eq 'CODE') {
		$code = $args{flock};
	} elsif (defined($lock{$args{flock}})) {
		$code = $lock{$args{flock}};
	} else {
		die "undefined lock mode.";
	}
	*CORE::GLOBAL::flock = undef;
	*CORE::GLOBAL::close = undef;
	*CORE::GLOBAL::flock = sub(*$) {
		no strict q/refs/;
		my $call = caller(0);
		my $ref = $_[0];
		$ref = \*{"${caller}::$ref"} if ref($ref) ne 'GLOB';
		print STDERR "flock:$ref\n" if $args{debug};
		$handle{$ref} = 1;
		$code->();
	};
	if ($args{close}) {
		*CORE::GLOBAL::close = sub(*) {
			no strict q/refs/;
			my $call = caller(0);
			my $ref = $_[0];
			$ref = \*{"${call}::$ref"} if ref($ref) ne 'GLOB';
			print STDERR "close:$ref\n" if $args{debug};
			if ($handle{$ref}) {
				print STDERR "unlock:$ref\n" if $args{debug};
				FlockWrapper::unlock();
				delete($handle{$ref});
			}
			return close($ref);
		};
	}
}}
END { unlock() if $args{clean}; }



sub lock_mkdir
{
	if (-e $args{fname}) {
		my $mtime = (stat($args{fname}))[9];
		unlock() if $mtime < time() - $args{timeout};
	}

	my $try = $args{try};
	while (!mkdir($args{fname}, 0755)) {
		return 0 if --$try <= 0;
		sleep(1);
	}
	return 1;
}



sub lock_symlink
{
	if (-e $args{fname}) {
		my $mtime = (stat($args{fname}))[9];
		unlock() if $mtime < time() - $args{timeout};
	}

	my $try = $args{try};
	while (!symlink(".", $args{fname})) {
		return 0 if --$try <= 0;
		sleep(1);
	}
	return 1;
}



sub unlock
{
	if ($args{flock} eq 'symlink') {
		unlink($args{fname});
		$args{unlocked} = 1;
	} elsif ($args{flock} eq 'mkdir') {
		rmdir($args{fname});
		$args{unlocked} = 1;
	}
}



1;
