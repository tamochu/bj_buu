####################################
# 世界データのアクセサ
####################################

use warnings;
#use strict;

package WorldAccessor;
require './TestFramework/Adapter/Accessor/Util.pm';


sub new{
	my $class = shift;
	my $self = {};

	return bless $self, $class;
}

#./log/countries.cgiに直接アクセスしてデータを取得/設定
#new_dataにzeroで空
sub access_data{

	my $self = shift;
	my $data_name = shift;
	my $new_data = shift;

	my $sub_routine = sub{

		_load_config();
		&read_cs;
		
		#新しい値が設定されていれば設定、なければ取得
		if($new_data){
			if($new_data eq "zero"){
				$new_data = 0;
			}
			$w{$data_name} = $new_data;
			&write_cs;
			&read_cs;
		}
	
		return  $w{$data_name};
	};

	return Util::fork_sub($sub_routine);
}

#災害を起こす(system_game.cgi::disaster()にバイパス)
sub evoke_disaster{

	my $self = shift;

	my $sub_routine = sub{
		
		_load_config();
		&disaster(@_);
	};

	Util::fork_sub($sub_routine);

}


#forkしたプロセスからbjのCGIをrequireする
sub _load_config{

	require "config.cgi";
	require "config_game.cgi";
}

#ユーザー名から%m,%yにデータ読み込み
sub _read_user{

	my $user_name = shift;

	my $id = unpack ('H*',$user_name);

	open my $fh, "< $userdir/$id/user.cgi" or croak("couldn't open ", $userdir, "/", $id, "/user.cgi");
	my $line = <$fh>;	
	close $fh;

	#pass検索
	my $pass;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if($k eq "pass") {
			$pass = $v;	
			last;
		}
	}

	#%m %yへユーザーデータ読み込み
	$in{id} = $id;
	$in{pass} = $pass; 
	&read_user;
}


