//手動タブのメニューのホバー・クリックイベントハンドラ


/* インプットフォームテンプレート */

//テキストの説明
function make_description(description){
	var ret = "<p class=\"menu_input_description\">";
	ret += description;
	ret += "</p>";
	return ret;
};

//ファイルの指定
function make_input_file(file_name){
	var ret = "<input type=\"hidden\" name=\"file\" value=\"";
	ret += file_name;
	ret += "\">";
	return ret;
};

//テキストボックスの作成
function make_textbox(name, opt_default_value){
	var ret = opt_default_value === undefined ?
		"<input class=\"menu_input_text\" type=\"text\" name=\""
		:"<input class=\"menu_input_text\" type=\"text\" value=" + opt_default_value + " name=\"";
	ret += name;
	ret += "\">";
	return ret;
};

//セレクトボックスの作成
function make_selectbox(name, array_option, first_value){

	var ret = "<select name=\"" + name + "\">";
	var value = first_value;
	var key;
	for (key in array_option){
		ret += "<option value = \"" + value + "\">";
		ret += array_option[key];
		ret += "</option>";
		value ++;
	}
	ret += "</select>";
	return ret;
};

//メニューのヘッダーフッター
var menu_header = "<div id=\"menu_input_form\" class=\"menu_form_class\">";
var menu_footer = "</div>";


//PlayerController
$(function(){
    $("#player_controller").hover(function(){ 
            $("#msg_window").find("p").text("プレイヤーの生成や士官、削除");
        });
});

//PlayerController::access_data
$(function(){
    $("#access_data", "#player_controller").on({
	"click": function(e){ 
		$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("データ名")
			   +make_textbox("value2")
			   +make_description("新しい値")
			   +make_textbox("value3")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("プレイヤーのuser.cgiに直接アクセスして値の設定/取得を行う");
		$("#msg_window").find("p").append("<br>$m{data_name}を操作する動作");
		$("#msg_window").find("p").append("<br>ブラウザ版では新しい値にget_valueを設定すると現在の値を取得してエラーとして出力する");
	}
   });
});

//PlayerController::create_player
$(function(){
    $("#create_player", "#player_controller").on({
	"click": function(){ 

		var sex = ["男性", "女性"];
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("パスワード")
			   +make_textbox("value2")
			   +make_description("性別")
			   +make_selectbox("value3", sex, 1)
			   +make_description("ＩＰアドレス(ブラウザ版は調整中。デフォルト値のまま使って)")
			   +make_textbox("value4", "1.1.1.1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/create_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("login.cgiから新規プレイヤーを作成");

	}
   });
});


//PlayerController::action_shikan_player
$(function(){
    $("#action_shikan_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("士官する国のインデックス")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/action_shikan_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("メイン画面→国情報→士官から士官する");
		$("#msg_window").find("p").append("放浪の場合は士官する国に国の総数+1を指定する");

	}
   });
});

//PlayerController::remove_player
$(function(){
    $("#remove_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/remove_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("プレイヤーを削除する");

	}
   });
});

//PlayerController::refresh_player
$(function(){
    $("#refresh_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/refresh_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("プレイヤーのtp,lib,turnを空にする(&refresh相当)");
	}
   });
});

//CountryController
$(function(){
    $("#country_controller").hover(function(){ 
            $("#msg_window").find("p").text("国に関するコントローラー");
        });
});

//CountryController::access_data
$(function(){
    $("#access_data", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("国のインデックス")
			   +make_textbox("value1")
			   +make_description("データ名")
			   +make_textbox("value2")
			   +make_description("新しい値")
			   +make_textbox("value3")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("countries.cgiに直接アクセスして国の値を設定/取得する");
		$("#msg_window").find("p").append("<br>新しい値にget_valueを設定すると現在の値を取得してエラーとして出力する");

	}
   });
});

//CountryController::admin_reset_countries
$(function(){
    $("#admin_reset_countries", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("スタートする年度")
			   +make_textbox("value1", "1")
			   +make_description("世界情勢")
			   +make_textbox("value2", "1")
			   +make_description("国の数")
			   +make_textbox("value3", "6")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/admin_reset_countries.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("admin.cgiのおまかせ国作成を呼び世界をリセットする");

	}
   });
});

//CountryController::admin_add_country
$(function(){
    $("#admin_add_country", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("新しい国名")
			   +make_textbox("value1")
			   +make_description("新しい国の色")
			   +make_textbox("value2", "#ff0000")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/admin_add_country.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("admin.cgi経由で新しい国を追加する");

	}
   });
});

//CountryController::action_stand_candidate
$(function(){
    $("#action_stand_candidate", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/action_stand_candidate.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("国情報→君主投票→立候補から立候補する");

	}
   });
});

//CountryController::action_vote
$(function(){
    $("#action_vote", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("候補者名")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/action_vote.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("国情報→君主投票→投票から投票する");

	}
   });
});

//WorldController
$(function(){
    $("#world_controller").hover(function(){ 
            $("#msg_window").find("p").text("世界設定のコントローラー");
        });
});

//WorldController::access_data
$(function(){
    $("#access_data", "#world_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("データ名")
			   +make_textbox("value1")
			   +make_description("新しい値")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WorldController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("countries.cgiに直接アクセスして値を設定/取得する");
		$("#msg_window").find("p").append("<br>$w{data_name}を操作するのと同じ");
		$("#msg_window").find("p").append("<br>新しい値にget_valueを設定すると現在の値を取得してエラーとして出力する");

	}
   });
});

//WorldController::evoke_disaster
$(function(){
    $("#evoke_disaster", "#world_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("moreスイッチ")
			   +make_textbox("value1", 0)
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WorldController/evoke_disaster.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("災害を起こす。");

	}
   });
});

//WarController
$(function(){
    $("#war_controller").hover(function(){ 
            $("#msg_window").find("p").text("戦争関連のコントローラー");
        });
});

//WarController::action_set_war
$(function(){
    $("#action_set_war", "#war_controller").on({
	"click": function(){ 

		var array = ["少数", "通常", "長期"];
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("対象国インデックス")
			   +make_textbox("value2")
			   +make_description("規模")
			   +make_selectbox("value3", array, 1)
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_set_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("メニューの戦争→規模選択→国選択で出発するプレイヤー操作をエミュレートする");
		$("#msg_window").find("p").append("<br>成功すれば$m{lib}はwarになり、$m{wt}に待機時間が設定される。");

	}
   });
});

//WarController::action_encount
$(function(){
    $("#action_encount", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_encount.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("action_set_warで出発した状態から着弾する。");
		$("#msg_window").find("p").append("<br>待機時間中には着弾出来ない。（$m{wt}が0でないなら失敗する)");
		$("#msg_window").find("p").append("<br>対戦相手は着弾後に決定し、$y{}から参照できる。");

	}
   });
});

//WarController::action_step_war
$(function(){
    $("#action_step_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_step_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("戦争で戦闘を行う");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});


//WarController::action_win_war
$(function(){
    $("#action_win_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_win_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("相手の兵力を０に、自分の兵力を１万にして戦闘を行い勝利する");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});

//WarController::action_win_war
$(function(){
    $("#action_lose_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_lose_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("自分の兵力を０に、相手の兵力を１万にして戦闘を行い敗北する");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});

//WarController::action_draw_war_turn
$(function(){
    $("#action_draw_war_turn", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_draw_war_turn.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("turnを０に設定してから戦闘を行い引き分けにする");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});

//WarController::action_draw_war_kaimetu
$(function(){
    $("#action_draw_war_kaimetu", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_draw_war_kaimetu.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("お互いの兵力を０に設定してから戦闘を行い引き分けにする");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});

//WarController::action_complete_war
$(function(){
    $("#action_complete_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_complete_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("じゃんけんを固定して決着するまで戦闘する");
		$("#msg_window").find("p").append("<br>着弾前に呼べば失敗する");

	}
   });
});

//WarController::action_after_war
$(function(){
    $("#action_after_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("プレイヤー名")
			   +make_textbox("value1")
			   +make_description("選択肢")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_after_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("統一後に選択肢を処理する");

	}
   });
});


