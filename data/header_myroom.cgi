#=================================================
# ���̨�ِݒ� Created by Merino
#=================================================
# ���ǉ�/�폜/�ύX/���ёւ���
# ���̨�قŕ\��������́B���̉p���͓�������Ȃ���Ή��ł��ǂ�

my @files = (
	['�莆',	'letter'],
	['���L',	'blog'],
	['���G�`��','oekaki'],
	['�{�쐬',	'book'],
	['���G�`��(���߯��)','oekaki_spp'],
);


#=================================================
# ���̨��ͯ�ް
#=================================================
sub header_myroom {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;

	for my $i (0 .. $#files) {
		next if ($is_mobile || $is_smart) && $files[$i][1] eq 'oekaki';
		next if $is_mobile && $files[$i][1] eq 'oekaki_spp';
		print $in{no} eq $i ? qq| $files[$i][0] /| : qq| <a href="$files[$i][1].cgi?id=$id&pass=$pass&no=$i">$files[$i][0]</a> /|;
	}
	print qq| <a href="./../upbbs/imgboard.cgi?id=$id&pass=$pass">�摜�f����</a>|;
	print qq|<h1>$files[$in{no}][0]</h1>|;
}

1; # �폜�s��
