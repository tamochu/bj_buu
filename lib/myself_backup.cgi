#================================================
# バックアップファイルダウンロード
#================================================
use File::Copy;
use Archive::Zip;
use Digest::MD5;

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "バックアップファイルをダウンロードします<br>";
		$mes .= "データが異常なときにはバックアップファイル<br>";
		$mes .= "をそのまま管理人に渡してください<br>";
	}
	&menu('やめる', 'ﾊﾞｯｸｱｯﾌﾟ');
}

sub tp_1 {
	return if &is_ng_cmd(1);
	
	$m{tp} = $cmd * 100;
	&tp_100;
}

#=================================================
# バックアップファイル作成
#=================================================
sub tp_100 {
	my $dir = "$userdir/$id";
	
	if($is_mobile){
		my $txtfile = "backup.txt";
		open my $bfh, "> $dir/$txtfile";
		
		print $bfh "=====user.cgi=====\n";
		open my $ufh, "<:encoding(shiftjis)","$dir/user.cgi";
		while (my $line = <$ufh>){
			print $bfh $line;
		}
		close $ufh;
		print $bfh "==================\n";
		
		print $bfh "====depot.cgi=====\n";
		open my $dfh, "< $dir/depot.cgi";
		while (my $line = <$dfh>){
			print $bfh $line;
		}
		close $dfh;
		print $bfh "==================\n";
		
		print $bfh "====skill.cgi=====\n";
		open my $sfh, "< $dir/skill.cgi";
		while (my $line = <$sfh>){
			print $bfh $line;
		}
		close $ufh;
		print $bfh "\n==================\n";
		
		print $bfh "==collection.cgi==\n";
		open my $cfh, "< $dir/collection.cgi";
		while (my $line = <$ufh>){
			print $bfh $line;
		}
		close $ufh;
		print $bfh "==================\n";
		
		close $bfh;
		
		my $md5 = Digest::MD5->new;
		
		open my $fh, "< $dir/$txtfile";
		$md5->addfile($fh);
		my $hexmd5 = $md5->hexdigest;
		
		open my $fh2, ">> $logdir/backup.cgi";
		print $fh2 "$time $m{name}:$hexmd5\n";
		close $fh2;
		$mes .= "<a href=\"link.cgi?$dir/$txtfile\" target=\"_blank\">バックアップファイル<\/a>";
	}else{
		my $zipfile = "backup.zip";
		
		unless (-d "$dir/backup"){
			mkdir "$dir/backup", 0755 or die "$!:$dirname";
		}
		
		copy("$dir/user.cgi", "$dir/backup/user.cgi");
		copy("$dir/depot.cgi", "$dir/backup/depot.cgi");
		copy("$dir/skill.cgi", "$dir/backup/skill.cgi");
		copy("$dir/collection.cgi", "$dir/backup/collection.cgi");
	
		my @lines = ();
		open my $dfh, "+< $dir/backup/depot.cgi";
		eval { flock $dfh, 2; };
		while (my $line = <$dfh>){
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if($kind == 2 && $item_no == 53){
				$line = "2<>42<>$item_c<>$item_lv<>\n";
				$n_egg++;
			}
			if($kind == 3 && $item_no == 180){
				$line = "3<>76<>$item_c<>$item_lv<>\n";
			}
			if($kind == 3 && $item_no == 181){
				$line = "3<>77<>$item_c<>$item_lv<>\n";
			}
			push @lines, $line;
		}
		seek  $dfh, 0, 0;
		truncate $dfh, 0;
		print $dfh @lines;
		close $dfh;
		
		my $zip = Archive::Zip->new();
	
		$zip->addTree("$dir/backup", $dir);
		
		$zip->writeToFileNamed("$dir/$zipfile");
		
		chmod 0666, "$dir/$zipfile";
		
		my $md5 = Digest::MD5->new;
		
		open my $fh, "< $dir/$zipfile";
		$md5->addfile($fh);
		my $hexmd5 = $md5->hexdigest;
		
		open my $fh2, ">> $logdir/backup.cgi";
		print $fh2 "$time $m{name}:$hexmd5\n";
		close $fh2;
		
		close $fh;
		$mes .= "<a href=\"link.cgi?$dir/$zipfile\" target=\"_blank\">バックアップファイル<\/a>";
	}

	$m{tp} = 110;
	&n_menu;
}



#=================================================
# バックアップファイル消去
#=================================================
sub tp_110 {
	my $dir = "$userdir/$id";
	
	if($is_mobile){
		my $txtfile = "backup.txt";
		unlink "$dir/$txtfile";
	}else{
		my $zipfile = "backup.zip";
	
		if (-d "$dir/backup"){
			unlink "$dir/backup/user.cgi";
			unlink "$dir/backup/depot.cgi";
			unlink "$dir/backup/skill.cgi";
			unlink "$dir/backup/collection.cgi";
			rmdir "$dir/backup";
		}
	
		unlink "$dir/$zipfile";
	}
	$mes .= "バックアップファイルを削除しました";
	
	$m{tp} = 1;
	&n_menu;
}
1; # 削除不可
