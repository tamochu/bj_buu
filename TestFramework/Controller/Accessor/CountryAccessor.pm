####################################
# 国データのアクセサ
# 値を出来るだけ直接書き込まずに既存のCGIで国データを操作する
####################################

use warnings;
#use strict;
use CGI::Carp;
use File::Copy::Recursive qw( dircopy );
use File::Path qw(rmtree);

package CountryAccessor;

require './TestFramework/Controller/Accessor/Util.pm';

#BJWrapper.pmのファイル名
my $bj_wapper = './TestFramework/Controller/Accessor/BJWrapper.pm';

sub new{
	my $class = shift;
	my $self = {};
	return bless ($self, $class);
}
#./log/countries.cgiのデータに直接アクセスして取得/設定
sub access_data{

	my $self = shift;
	my $country_index = shift;
	my $data_name = shift;
	my $new_data = shift;
	
	#世界データ読み込み

	
	$sub_routine = sub{

		require $bj_wapper;
		package BJWrapper;

		#新しい値が設定されていれば設定、なければそのまま取得
		_load_config();
		&read_cs;
		if(defined($new_data)){
	
			$cs{$data_name}[$country_index] = $new_data;
			&write_cs;
			&read_cs;

		}
		return	$cs{$data_name}[$country_index];
	};

	return Util::fork_sub($sub_routine);
}

#国の数を取得
sub get_num_country{
	
	my $self = shift;

	my $sub_routine = sub{
	
		require $bj_wapper;
		package BJWrapper;

		_load_config();
		&read_cs;
		return $w{country};
	};

	return Util::fork_sub($sub_routine);

}

#国を追加(admin_country.cgi経由)
sub add_country{

	my $self = shift;
	my $add_name;
	my $add_color;

	if(@_) {
		$add_name = shift;
		$add_color = shift;
	}
	else{
		$add_name = "default";
		$add_color = "#000FFF";
	}

	my $sub_routine = sub{
	
		require $bj_wapper;
		package BJWrapper;

		_load_config();

		#環境変数を偽装しadmin_country.cgiを呼び出す
 		$ENV{QUERY_STRING} = "mode=add_country&pass=pass&add_name=$add_name&add_color=$add_color";
		require "admin_country.cgi";	
		&read_cs;
		return $w{country};

	};

	return Util::fork_sub($sub_routine);
	
}

#国を削除(system_game.cgi::delete_countryが壊れているようなので自作)
sub remove_country {
	
	carp ("CountryAccessor::remove_country() is experimental\n");

	my $self = shift;
	my $country_index_to_remove = shift;


	$sub_routine = sub{	

		require $bj_wapper;
		package BJWrapper;

		_load_config();

		#国データ読み込み
		&read_cs;
	
		#削除される国の国民はネバラン送り
		my @lines = &get_country_members($country_index_to_remove);
		for my $line (@lines) {
			$line =~ tr/\x0D\x0A//d;
			&move_player($line, $country_index_to_remove, 0);
			&regist_you_data($line, 'country', 0);
		}	
	
		#左シフトされる国の国民はuser/username/userのcountryを変更
		for my $i (($country_index_to_remove + 1) .. $w{country}){
			@lines = &get_country_members($i);
			for my $line (@lines){
				$line =~ tr/\x0D\x0A//d;
				&regist_you_data($line, 'country', ($i - 1));
			}
		}

		#国フォルダをテンプにコピーしてから削除
		my $temp_dir = "temp"; #tempフォルダ名
		for my $i ($country_index_to_remove .. $w{country}){
			
			#元のフォルダ名-1にリネームしてテンプフォルダにコピー
			my $orig = "$logdir/$i";
			die ("$orig:$!") unless (-d $orig);
			$i--;
			my $dest = "$logdir/$temp_dir/$i";
	
			dircopy($orig, $dest);

			#既存の国のフォルダを削除
			rmtree($orig);
		}
	
		#コピーしてリネームしたフォルダを元のlogdir直下へ戻す
		my $num_country = $w{country};
		$num_country--;

		for my $i ($country_index_to_remove .. $num_country){
	
			my $orig = "$logdir/$temp_dir/$i";
			my $dest = "$logdir/$i";
			dircopy($orig, $dest);

		}
	
		#テンプの国フォルダを消す
		rmtree ($temp_dir);
	
		#countries.cgi用に$csの国情報をずらす
		#@keysはsystem.cgiのwrite_cs()からコピー
		my @keys = (qw/
			name strong tax food money solcroakr state is_croak member capacity color
			win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
			modify_war modify_dom modify_mil modify_pro
			extra extra_limit disaster disaster_limit
			new_commer
		/);
	
		my $num_countries_to_move = $w{country} - $country_index_to_remove;
		for my $i (0 .. ($num_countries_to_move - 1)){
	
			for my $key (@keys){
				$cs{$key}[($country_index_to_remove + $i)] = $cs{$key}[($country_index_to_remove + $i + 1)];
			}
		}
		
		#重複した国情報の末尾をundef
		for my $key (@keys){
			undef ($cs{$key}[$w{country}]);
		}
	
	
		#世界設定の国数をデクリメント
		--$w{country};
	
		#国の設定の変更を書き込み
		&write_cs;
	
	};

	return Util::fork_sub($sub_routine);
}

1;
