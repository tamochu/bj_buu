####################################
# アイテム関連のアクセサ
####################################

use warnings;
use CGI::Carp;
#use strict;

package ItemAccessor;
use TestFramework::Controller::ControllerConst;
require $ControllerConst::accessor_util;

sub new{
	my $class = shift;
	my $self = {};
	return bless $self, $class;
}

#user/depot.cgiに直接アクセスしてアイテムを追加
sub give_item{

	my $self = shift;
	my ($player_name, $kind, $item_no, $item_c, $item_lv) = @_;
	
	my $user_id = unpack('H*', $player_name);

	my $sub_routine = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_load_config();

		#depot.cgi読み込み
		my @lines = ();
		open my $fh, "+< $userdir/$user_id/depot.cgi" or die("couldn't open ", $userdir, "/", $user_id, "/depot.cgi");
		while (my $line = <$fh>){
			push @lines, $line;
		}
	
		#追加
		my $new_line = "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		print "new_line = $new_line\n";
		push @lines, $new_line;

		#書き込み
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;
		close $fh;
	};

	Util::fork_sub($sub_routine);

}

#アイテムのインデックスを取得
sub get_item_index{

	my $self = shift;
	my ($player_name, $kind, $item_no, $item_c, $item_lv) = @_;
	my $user_id = unpack('H*', $player_name);

	my $sub_routine = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_load_config();
		
		#depot.cgiを読み込み検索
		my @lines = ();
		my $index = undef;
		my $current_index = 0;
	
		open my $fh, "+< $userdir/$user_id/depot.cgi" or die("couldn't open ", $userdir, "/", $user_id, "/depot.cgi");
	
		while (my $line = <$fh>){

			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			if(($rkind eq $kind) and ($ritem_no eq $item_no) and ($ritem_c eq $item_c) and ($ritem_lv eq $item_lv)){
				$index = $current_index;
				last;
			}
			$current_index++;
	
		}
		close $fh;
	
		#無ければ例外をスロー
		(defined $index) or die "no such a item ($kind, $item_no, $item_c, $item_lv) is in $player_name/depot.cgi\n"; 
		return $index;
	};

	return Util::fork_sub($sub_routine);

}

#アイテムを引き出す
sub action_draw_item{

	my $self = shift;
	my ($player_name, $item_index) = @_;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);

	
	#bj.cgiを開き預り所へ行く
	my $enter_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		_is_bound($player_name);

		$m{lib} = "depot";
		&write_user;

		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base;

		require "bj.cgi";

		_read_user($player_name);
		die ("failed to draw item : m{tp} expect 1:actual  $m{tp} :mes = $mes") if ($m{tp} ne 1);
	};

	#引き出すを選ぶ
	my $select_draw = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);

		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=1";

		require "bj.cgi";
		_read_user($player_name);
		die ("failed to draw item : m{tp} expect 110:actual  $m{tp} :mes = $mes") if ($m{tp} ne 110);

	};

	#一覧からアイテムを選び引き出す
	my $select_item = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$item_index++;
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=$item_index";

		require "bj.cgi";
		_read_user($player_name);
		die ("failed to draw item : m{tp} expect 1:actual  $m{tp} :mes = $mes") if ($m{tp} ne 1);


	};

	#やめるコマンドでm{tp}を1に
	my $break_depot= sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=0";

		require "bj.cgi";
		_read_user($player_name);
		die ("failed to draw item : m{tp} expect \"\": actual  $m{tp} :mes = $mes") if ($m{tp} ne "1");

	};

	#やめるでrefresh()を呼ぶ
	my $back_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=0";

		require "bj.cgi";
		_read_user($player_name);
		die ("failed to draw item : m{lib} expect \"\": actual  $m{lib} :mes = $mes") if ($m{lib} ne "");

	};


	
	Util::fork_sub($enter_bj);
	Util::fork_sub($select_draw);
	Util::fork_sub($select_item);
	Util::fork_sub($break_depot);
	Util::fork_sub($back_bj);

}

#ペットを使う
sub action_use_pet{

	my $self = shift;
	my $player_name = shift;

	#ブラウザから送られる環境変数の偽装の基礎部分
	my $make_env = sub{
		require $ControllerConst::bj_wrapper;
		package BJWrapper;
		_make_env_base($player_name);
	};
	my $env_base = Util::fork_sub($make_env);

	
	
	#bj.cgiを開きマイルームへ行く
	my $enter_bj = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);

		#拘束中またはlib処理中なら例外をスロー
		_is_bound($player_name);

		#ペットがなければ例外をスロー
		die ("$player_name has no pet") if ($m{pet} eq 0);

		#ペットがmyselfで使えないものなら例外をスロー
		die ("$pets[$m{pet}][1] cannot be activated in myroom") if ($pets[$m{pet}][2] ne 'myself' );


		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&cmd=4";

		require "bj.cgi";

		_read_user($player_name);
		die ("failed to draw item : m{tp} expect 1:actual  $m{tp} :mes = $mes") if ($m{tp} ne 1);
	};

	
	#ペットを使う
	my $use= sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);


		$ENV{REQUEST_METHOD} = "";
		$ENV{QUERY_STRING} = $env_base."&mode=use_pet";
		require "bj.cgi";
		

		_read_user($player_name);

		#通常のﾍﾟｯﾄ
		if(($m{pet} eq 0) and ($m{lib} eq "")){
			return 0;
		}
		#消費された後にlibの状態が変わるﾍﾟｯﾄ
		if(($m{pet} eq 0) and ($m{lib} ne "")){
			return 1;
		}
		#消費されずにlibの状態が変わるペット
		elsif(($m{pet} ne 1) and ($m{lib} ne "")){
			return 2;
		}
		else{
			die("unexpected pet was used : $pets[$m{pet}][1]"); 
		}
	};

	Util::fork_sub($enter_bj);
	return Util::fork_sub($use);
	
}

#マイルームでの使用後に処理が必要なペットの処理
sub action_step_pet{

	my $self = shift;
	my $player_name = shift;
	my @argvs = @_;

	#現在装備しているペットの外部ファイル化された処理を取得
	my $get_pet = sub{

		require $ControllerConst::bj_wrapper;
		package BJWrapper;

		_before_bj($player_name);
		return $m{pet};
	};
	my $my_pet = Util::fork_sub($get_pet);

	#ペット特有の処理をする
	print STDERR "do ./TestFramework/Controller/Accessor/ItemAccessorSpecific/pet$my_pet.pm\n";
	do "./TestFramework/Controller/Accessor/ItemAccessorSpecific/pet$my_pet.pm";
	enact($player_name, @argvs);
}

1;
