#use strict;
use warnings;

package ItemController;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::item_accessor;

sub new{
	my $class = shift;
	my $self = PlayerAccessor->new();

	#アイテムのアクセサ
	$self->{ITEM_ACCESSOR_INTERFACE} = ItemAccessor->new(); 

	bless ($self, $class);

	return $self;
}

#アイテムをdepotに追加する
#引数はプレイヤー名、アイテムの無名ハッシュリファレンス{type, no, c, lv}
sub give_item{

	my $self = shift;
	my ($player_name, $href_item) = @_;
	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $player_name) and (defined $href_item)){
		die ("$error_info : ItemAccessor::get_item_index needs player_name and item hash reference\n");
	}

	eval{
		$self->{ITEM_ACCESSOR_INTERFACE}->give_item($player_name, $href_item->{type}, $href_item->{no}, $href_item->{c}, $href_item->{lv});
	};
	if($@){
		die "$error_info : failed to give [$kind, $item_no, $item_c, $item_lv] to $player_name\n$@";
	}
}

#depotの中からアイテムのindexを取得する
#引数はプレイヤー名、アイテムの無名ハッシュリファレンス{type, no, c, lv}
sub get_item_index{

	my $self = shift;
	my ($player_name, $href_item) = @_;
	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $player_name) and (defined $href_item)){
		die ("$error_info : ItemAccessor::get_item_index needs player_name and item hash reference\n");
	}

	my $index;
	eval{
		$index = $self->{ITEM_ACCESSOR_INTERFACE}->get_item_index($player_name, $href_item->{type}, $href_item->{no}, $href_item->{c}, $href_item->{lv});
		
	};
	if($@){
		die "$error_info : failed to get index of [$href_item->{type}, $href_item->{no}, $href_item->{c}, $href_item->{lv}] in $player_name's depot\n$@";
	}

	return $index;
}

#預り所→引き出すでアイテムを装備する
#引数はプレイヤー名、アイテムのdepot内のインデックス
sub action_draw_item{

	my $self = shift;
	my ($player_name, $item_index) = @_;
	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless ((defined $player_name) and (defined $item_index)) {
		die ("$error_info : ItemAccessor::action_draw_item needs player_name and item_index\n");
	}

	eval{
		$self->{ITEM_ACCESSOR_INTERFACE}->action_draw_item($player_name, $item_index); 
		
	};
	if($@){
		die "$error_info : failed draw item:index$item_index in $player_name's depot\n$@";
	}
}

#ﾏｲﾙｰﾑ→ペットを使用で装備しているペットを使用する
#引数：プレイヤー名
#戻り値：その後の処理が必要なら１、使い切りなら０
sub action_use_pet{

	my $self = shift;
	my $player_name = shift;
	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	unless (defined $player_name) {
		die ("$error_info : ItemAccessor::action_ues_pet needs player_name\n");
	}

	eval{
		my $ret = $self->{ITEM_ACCESSOR_INTERFACE}->action_use_pet($player_name); 
		
	};
	if($@){
		die "$error_info : failed use pet :$player_name\n$@";
	}

	return $ret;
}

#ペット使用後にユーザー入力が必要なペットを処理する（いたずら系など）
#事前に対象のペットをaction_use_petしていないと例外
#それぞれの引数は./TestFramework/Controller/Accessor/ItemAccessorSpecificのペットno.pmを参照
sub action_step_pet{

	my $self = shift;
	my $player_name = shift;
	my $caller_filename = (caller 0)[1];
	my $caller_num_line = (caller 0)[2];
	my $error_info = "Error: $caller_filename at line $caller_num_line";

	eval{
		my $ret = $self->{ITEM_ACCESSOR_INTERFACE}->action_step_pet($player_name, @_); 
		
	};
	if($@){
		die "$error_info : action_step_ pet failed\n$@";
	}

}
