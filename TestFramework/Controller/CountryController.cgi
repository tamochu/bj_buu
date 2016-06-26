#use strict;
use warnings;

package CountryController;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::country_accessor;

sub new{
	my $class = shift;
	my $self = {};
	#国データのアクセサ
	$self->{COUNTRY_ACCESSOR} = CountryAccessor->new(); 

	$self->{DATA_TO_BE_SAVED} = [];
	bless ($self, $class);


	return $self;
}


#######################################
# テストから呼び出される関数
#######################################

#countries.cgiのデータに直接アクセスして値を設定
sub access_data{

	my $self = shift;
	my ($country_index, $data_name, $new_data) = @_;
	return $self->{COUNTRY_ACCESSOR}->access_data($country_index, $data_name, $new_data);

}


#新しい国を生成
#戻り値は現在の$w{country}
sub admin_add_country{

	my $self = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	#国の名前と色のデフォルト
	my $add_name = "default";
	my $add_color = "#000FFF";

	#引数があれば設定
	if(@_){
		$add_name = shift;
		$add_color = shift;
	}

	my $num_country = undef;
	eval{
		$num_country = $self->{COUNTRY_ACCESSOR}->add_country($add_name, $add_color);
	};
	if($@){
		die ("$error_info: failed to add countries\n", $@);
	}
}

#国をリセット
sub admin_reset_countries{
	
	my $self = shift;
	my $setting = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	#設定
	my $default_setting = { year => 1, world => 1, country => 6};
	if(defined $setting->{year}){
		$default_setting->{year} = $setting->{year};
	}
	if(defined $setting->{world}){
		$default_setting->{world} = $setting->{world};
	}
	if(defined $setting->{country}){
		$default_setting->{country} = $setting->{country};
	}

	eval{
		$self->{COUNTRY_ACCESSOR}->reset_countries($default_setting);
	};
	if($@){
		die ("$error_info: failed to reset countries\n", $@);
	}

}

#立候補する
sub action_stand_candidate{
	
	my $self = shift;
	my $player_name = shift;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	

	eval{
		$self->{COUNTRY_ACCESSOR}->action_stand_candidate($player_name);
	};
	if($@){
		die ("$error_info: action_stand_candidate failed\n", $@);
	}

}


#投票する
sub action_vote{
	
	my $self = shift;
	my ($player_name, $candidate_name) = @_;

	my $caller_filename = (caller 1)[1];
	my $caller_num_line = (caller 1)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	

	eval{
		$self->{COUNTRY_ACCESSOR}->action_vote($player_name, $candidate_name);
	};
	if($@){
		die ("$error_info: action_vote failed\n", $@);
	}

}

#国を削除
#sub remove_country{
#
#	my $self = shift;
#
#	#引数が無ければエラー
#	unless (@_) { die ("CountryAccessController::remove_country() needs arguments : the ndex of the target country"); };
#
#	my $country_to_remove = shift;
#	$self->{COUNTRY_ACCESSOR}->remove_country($country_to_remove);
#}



1;
