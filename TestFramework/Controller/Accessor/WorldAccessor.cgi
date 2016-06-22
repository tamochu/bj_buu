####################################
# 世界データのアクセサ
####################################

use warnings;
#use strict;

package WorldAccessor;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::accessor_util;

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

		require $ControllerConst::bj_wrapper;
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
	my $more_switch = shift;

	my $sub_routine = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		
		_load_config();
		&read_cs;
		&disaster($more_switch);
		&write_cs;
	};

	Util::fork_sub($sub_routine);

}

1;
