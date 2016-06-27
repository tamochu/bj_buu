package Situation1;


#プレイヤーの設定
our $situation1_players;

sub refresh{

	#コントローラーで使う定数
	use TestFramework::Controller::ControllerConst;

	#コントローラー
	require $ControllerConst::PlayerController;
	require $ControllerConst::CountryController;
	my $pc = PlayerController->new();
	my $cc = CountryController->new();

	#国をデフォルトでリセット（6ヵ国、１年目、平和）
	$cc->admin_reset_countries();

	#プレイヤーキャラクタ
	my $common_passward = "situation1";
	#名前はsituation1country1male
	$situation1_players=  [
		{ name=>"s1c1m", sex=>1, passward=>$common_passward,  country=>1},
		{ name=>"s1c1f", sex=>2, passward=>$common_passward,  country=>1},
		{ name=>"s1c2m", sex=>1, passward=>$common_passward,  country=>2},
		{ name=>"s1c2f", sex=>2, passward=>$common_passward,  country=>2},
		{ name=>"s1c3m", sex=>1, passward=>$common_passward,  country=>3},
		{ name=>"s1c3f", sex=>2, passward=>$common_passward,  country=>3},
		{ name=>"s1c4m", sex=>1, passward=>$common_passward,  country=>4},
		{ name=>"s1c4f", sex=>2, passward=>$common_passward,  country=>4},
		{ name=>"s1c5m", sex=>1, passward=>$common_passward,  country=>5},
		{ name=>"s1c5f", sex=>2, passward=>$common_passward,  country=>5},
		{ name=>"s1c6m", sex=>1, passward=>$common_passward,  country=>6},
		{ name=>"s1c6f", sex=>2, passward=>$common_passward,  country=>6}
	];


	#キャラクタ生成
	for my $player (@$situation1_players){
		$pc->create_player($player->{name}, $player->{passward}, $player->{sex});
	}

	#国設定
	for my $i (1 .. 6){
		$cc->access_data($i, "capacity", 2);
		$cc->access_data($i, "food", 999999);
		$cc->access_data($i, "money", 999999);
		$cc->access_data($i, "soldier", 999999);
	}

	#士官
	for my $player (@$situation1_players){
		$pc->action_shikan_player($player->{name}, $player->{country});
	}

	#セーブ
	require $ControllerConst::SituationLoader;
	SituationLoader::save_situation("situation1");
}


1;
