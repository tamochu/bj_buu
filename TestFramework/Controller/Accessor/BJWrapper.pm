#############################################
# bjのcgiに名前空間を付けて使うためのラッパー
#############################################
package BJWrapper;
use CGI::Carp;

#bj.cgiのbefore_bj
#decodeは行わない
sub _before_bj{

	my $user_name = shift;
	_load_config();
	_read_user($user_name);
	&read_cs;
}

#config.cgi等を名前空間付きで読み込む
sub _load_config{

	require "config.cgi";
	require "config_game.cgi";
	
	#config_test抑制
	$config_test = 0;

	#&twitter_botを上書きして抑制
	no warnings 'redefine';
    	*twitter_bot = sub {};	

	#&errorを上書きして例外でスローするようにする
	*error = sub{
		my($error_mes, $is_need_header) = @_;
		my $caller_filename = (caller 0)[1];
		my $caller_num_line = (caller 0)[2];
		my $error_info = "system_game.cgi::error was called at $caller_filename at line $caller_num_line\n";
		die("$error_info error message = $error_mes\n");
	};
}

#ユーザー名から%m,%yにデータ読み込み
sub _read_user{

	_load_config();
	my $user_name = shift;

	my $id = unpack ('H*', $user_name);

	#%m %yへユーザーデータ読み込み
	$in{id} = $id;
	$in{pass} = _get_pass($user_name);
	&read_user;
}

#pass検索
sub _get_pass{

	_load_config();
	my $user_name = shift;
	my $user_id = unpack('H*', $user_name);

	open my $fh, "< $userdir/$user_id/user.cgi" or die("couldn't open ", $userdir, "/", $user_id, "/user.cgi");
	my $line = <$fh>;	
	close $fh;

	my $pass;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if($k eq "pass") {
			$pass = $v;	
			last;
		}
	}

	return $pass;
}

#拘束判定
sub _is_bound{

	my $user_name = shift;
	_load_config();
	_read_user($user_name);

	#拘束中	
	if($m{wt} > 0){
		die "is bound : m{wt} > 0"; 
	}

	#lib処理中
	if($m{lib} ne ""){
		die "is processing lib $m{lib}";
	}

}

#bj.cgiの&decode部分で読み込む環境変数のid/passによる基礎部分の生成
sub _make_env_base{

	my $player_name = shift;

	my $player_id = unpack('H*', $player_name);
	#pass回収

	my $pass = _get_pass($player_name);

	#bj.cgiを開く時、decodeされるブラウザからの環境変数の偽装用変数
	my $env_base = "id=$player_id&pass=$pass";

	return $env_base;

}

1;
