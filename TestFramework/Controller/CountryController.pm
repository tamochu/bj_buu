#use strict;
use warnings;

package CountryController;
require "./TestFramework/Controller/CountryAccessor.pm";

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
	my ($country_index, $data_name) = @_;
	return $self->{COUNTRY_ACCESSOR}->access_data($country_index, $data_name);

}

#国の数を取得
sub get_num_country{

	my $self = shift;
	#世界データ読み込み
	return $self->{COUNTRY_ACCESSOR}->get_num_country();

}


#新しい国を生成
sub add_country{

	my $self = shift;

	#国の名前と色のデフォルト
	my $add_name = "default";
	my $add_color = "#000FFF";

	#引数があれば設定
	if(@_){
		$add_name = shift;
		$add_color = shift;
	}

	$self->{COUNTRY_ACCESSOR}->add_country($add_name, $add_color);
}

#国を削除
sub remove_country{

	my $self = shift;

	#引数が無ければエラー
	unless (@_) { die ("CountryAccessController::remove_country() needs arguments : the ndex of the target country"); };

	my $country_to_remove = shift;
	$self->{COUNTRY_ACCESSOR}->remove_country($country_to_remove);

}



1;
