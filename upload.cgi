#!/usr/local/bin/perl --

require './config.cgi';
require './config_game.cgi';

# 読み込み容量をオーバーした状態で cgi-lib.pl をロードするとそちらのエラーに巻き込まれて落ちる
# エラーに巻き込まれるようであれば自分でエラー処理をする
my $maxdata    = 131072;
my $len  = $ENV{'CONTENT_LENGTH'};
my $is_error = $len > $maxdata;
if ($is_error) {
	&decode;
}
else {
	require './cgi-lib.pl';
}

my $size = 15 * 1024;

&header;
&ReadParse unless $is_error; # cgi-lib.pl のエラーに巻き込まれるようでなければ
if($in{back} eq '1'){
	&read_user;
	&read_cs;
	$m{lib} = 'shopping_upload';
	$m{tp} = 100;
	&write_user;
	&error("イリーガルなアクセスです");
	&footer;
} else {
	my $_time = $time;
	my $newfile = ''; # なぜか add_picture 内で判別できないので外で
	&up_read_user;
	unless ($is_error) { # cgi-lib.pl のエラーに巻き込まれるようでなければ
		if (-f "$userdir/$id/upload_token.cgi") {
			if($ENV{REQUEST_METHOD} eq 'POST'){
				$newfile = &add_picture($_time); # add_picture 内で判別できないので外に出す
			}
		}

		if (!-f $newfile) { # なぜか add_picture 外なら判別できる
			$m{lib} = 'shopping_upload';
			$m{tp} = 100;
			&write_user;
			&error("イメージファイルの作成に失敗しました");
		}
		else {
			# ﾍﾟｲﾝﾀｰが効いた時にだけ upload_token.cgi を削除
			# shopping_upload.cgi $m{tp} == 400 の時にこのﾌｧｲﾙが残っているなら失敗してると判断できる
			unlink "$userdir/$id/upload_token.cgi";
			&show_picture;
			&footer;
		}
	}
}
exit;

sub add_picture {
	my $time2 = shift;
	my $ext = '';
	my $path = "$userdir/$id/picture";

	for my $tmp (@in) {
		if ($tmp =~ /(.*)Content-type:(.*)/i) {
			if ($2 =~ /image\/jpeg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /image\/pjpeg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /image\/gif/i) { $ext = '.gif'; }
			elsif ($2 =~ /image\/png/i) { $ext = '.png'; }
			else { $ext = 'NO'; }
		}
		elsif ($tmp =~ /(.*)filename=(.*)/i) {
			if ($2 =~ /\.jpg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /\.gif/i) { $ext = '.gif'; }
			elsif ($2 =~ /\.png/i) { $ext = '.png'; }
			else { $ext = 'NO'; }
		}
	}

	my $newfile = "$path/_$time2$ext";

	if (($ext eq 'NO') || ($ext eq '') || !defined($ext)) {
		$m{lib} = 'shopping_upload';
		$m{tp} = 100;
		&write_user;
		&error('不正な拡張子です');
	} else {
		open my $nfh,">$newfile" or &error("イメージファイルを作れません");
		binmode $nfh;
		print $nfh $in{'upfile'};
		close $nfh;

		if(-s $newfile > $size){
			unlink $newfile;
			$m{lib} = 'shopping_upload';
			$m{tp} = 100;
			&write_user;
			&error("サイズ超過です(15KBまで)");
		}
	}
	return $newfile;
}

sub show_picture{
	$layout = 2;
	my $count = 0;
	opendir my $dh, "$userdir/$id/picture" or &error("ﾏｲﾋﾟｸﾁｬが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<hr><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;"> $file_title |;
		++$count;
	}
	closedir $dh;
	print qq|$sub_mes<hr>|;
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}

sub up_read_user {
 # Get %m %y
	%m = ();
	%y = ();
	$id   = $in{id};
	$pass = $in{pass};
	open my $fh, "< $userdir/$id/user.cgi" or &error("プレイヤーデータが読み込めません");
	my $line = <$fh>;
	close $fh;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if ($k =~ /^y_(.+)$/) {
			$y{$1} = $v;
		}else {
			$m{$k} = $v;
		}
	}
	&error('パスワードが違います') unless $m{pass} eq $pass;
	# 拘束時間がある場合、経過時間分減らす
	$m{wt} -= ($time - $m{ltime}) if $m{wt} > 0;
}
