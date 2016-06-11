//設定ボタンが押された時のオンクリックハンドラ
function OnSettingButtonClick(){
	
	var log = document.getElementById('log');

	//APIテスト
	if (!window.File) {
		log.innerHTML = "ブラウザがfile APIを扱えない。テスト出来ない。";
		return 0;
	}

	//中間ファイルへの出力
	var output;

	//選択されたテストを書き込み準備
	var checks = document.getElementsByName('file');
	document.getElementById('log').innerHTML = "選択されたテスト<br>";
	for(var i=0; i < checks.length; i++){
		if(checks[i].checked){
			log.innerHTML += checks[i].value + "<br>";
			output += "test_name<>";
			output += checks[i].value + "\n";
		}
	}

	//選択されたセッティングを書き込み準備
	log.innerHTML += "<br>保存するディレクトリ<br>";

	var settings_before = document.getElementsByName('setting_before');
	for(var i=0; i < settings_before.length; i++){
		if(settings_before[i].checked){
			log.innerHTML += settings_before[i].value + ": ON<br>";
			output += "save_before<>";
			output += settings_before[i].value + "\n";
		}
	}

	log.innerHTML += "<br>復元するディレクトリ<br>";
	var settings_after  = document.getElementsByName('setting_after');
	for(var i=0; i < settings_after.length; i++){
		if(settings_after[i].checked){
			log.innerHTML += settings_after[i].value + ": ON<br>";
			output += "save_after<>";
			output += settings_after[i].value + "\n";
		}
	}

	//中間ファイルに出力
}


//階層的なチェックボックスのクリックハンドラ
$(function() {
       	$("#treeList input[type=checkbox]").click(function(event) {
                   var $element = $(event.target);    
                   var checked = $element.attr('checked');
           
                   $element.closest("li").find('ul li input[type=checkbox]').each(function() {
                       if (checked) {
                           $(this).attr("checked", checked);
                       }
                       else {
                           $(this).removeAttr('checked');
                       }
                   });
               });
	});
