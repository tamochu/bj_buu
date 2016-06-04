####################################
# 世界データのアクセサ
####################################

use warnings;
#use strict;

package WorldAccessor;
require './TestFramework/Controller/Accessor/Util.pm';

#BJWrapper.pmのファイル名
my $bj_wapper = './TestFramework/Controller/Accessor/BJWrapper.pm';

sub new{
	my $class = shift;
	my $self = {};

	return bless $self, $class;
}

#./log/countries.cgiに直接アクセスしてデータを取得/設定
sub access_data{

	my $self = shift;
	my $data_name = shift;
	my $new_data = shift;

	my $sub_routine = sub{

		require $bj_wapper;
		package BJWrapper;

		_load_config();
		&read_cs;
		
		#新しい値が設定されていれば設定、なければ取得
		if(defined $new_data){
			$w{$data_name} = $new_data;
			&write_cs;
		}
	
		return  $w{$data_name};
	};

	return Util::fork_sub($sub_routine);
}

#災害を起こす(system_game.cgi::disaster()にバイパス)
sub evoke_disaster{

	my $self = shift;
	my $disaster_type = shift;

	my $sub_routine = sub{

		require $bj_wapper;
		package BJWrapper;
		
		_load_config();
		&disaster($disaster_type);
	};

	Util::fork_sub($sub_routine);

}

1;
