#!/usr/local/bin/perl --

package test_browser;
use CGI::Carp;
use CGI;

#フレームワークのルート
my $framework_root = "./TestFramework";
#フレームワーク直下のテストフォルダ
my $test_root = "Tests";
#テストを実行するcgi
my $test_runner = "test_runner.cgi";
#セーブ＆ロードのディレクトリ
my $dir_to_save = "$framework_root/save";


my $q = CGI->new();
&print_header;
&init;
&print_footer;




#初期化
sub init{

	#パスチェック
	unless(&_is_valid_passward){
		print qq|<p>invalid passward</p>|;
		return 1;
	}

	#メッセージウィンドウ
	print qq|<div id="msg_window">|;
	print qq|<p class="msg_class">開発中</p>|;
	print qq|</div>|;

	#タブ生成
 	print qq|
<div id="tabs">
	<ul>
        <li><a href="#tab_saveload">セーブ＆ロード</a></li>
        <li><a href="#tab_script">スクリプト</a></li>
        <li><a href="#tab_manual">手動</a></li>
   	</ul>|;
	&generate_saveload_tab;
	&generate_script_tab;
	&generate_manual_tab;
	print qq|</div>|;


}

#セーブ＆ロード用のtab生成
sub generate_saveload_tab{

	print qq|<div id="tab_saveload">|;

	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="save">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="セーブ">|;
	print qq|</form>|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="load">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="ロード">|;
	print qq|</form>|;

	print qq|</div>|;
}

#スクリプト用のtab生成
sub generate_script_tab{

	print qq|<div id="tab_script">|;
	print qq|<form action="$test_runner" method="post">|;

	#チェックボックス作成
	print qq|<div id="treeList" class="content_box">|;
	print qq|<label>スクリプト選択</label>|;
	print qq|<ul>|;
	_load_tests($framework_root,$test_root);
	print qq|</ul>|;
	print qq|</div>|;

	#設定用div作成
	print qq|<div id="settingWindow" class="content_box">|;
	print qq|<label>設定選択</label>|;
	print qq|<ul>それぞれのテスト前でTestFramework/saveに退避させてそれぞれのテスト後に復元するディレクトリ|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./log" checked="checked">log</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./data" checked="checked">data</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./html" checked="checked">html</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./user" checked="checked">user</label></li>|;
	print qq|</ul>|;
	print qq|</div>|;
	print qq|<input type="hidden" name="mode" value="script">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="実行">|;
	print qq|</form>|;
	print qq|</div>|;

}

#手動でコントロールするタブ
sub generate_manual_tab{

	print qq|<div id="tab_manual">|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="manual">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="実行">|;
	print qq|</form>|;
	print qq|</div>|;
}

#再帰的にディレクトリを探索しチェックボックスを作る
sub _load_tests{

	my $parent_path = shift;
	my $this_dirname = shift;

	
	my $dir_name = $parent_path."/".$this_dirname;
	opendir(DIRHANDLE,$dir_name) or die ("$dir_name : $!");
	my @list = readdir DIRHANDLE;
	closedir(DIRHANDLE);
	my @dir_list;
	my @file_list;
	for my $name (@list){
		if(-f $parent_path."/".$this_dirname."/".$name){
			
			#cgi, pm, t拡張子のみ表示
			if($name =~ /\.cgi$|\.pm$|\.t$/){
				push(@file_list, $name);
			}
		}
		elsif(-d $parent_path."/".$this_dirname."/".$name){
			#親のパスは無視
			unless($name =~ /\.$/){
				push(@dir_list, $name);
			}
		}
	}
	

	print qq|<li>|;
	#自身のチェックボックス
	print qq|<label><input type="checkbox"><font color="red">$this_dirname</font></label>|;
	print qq|<ul>|;
	#ファイルのチェックボックス
	for my $file(@file_list){
		print qq|<li>|;
		print qq|<label><input type="checkbox" name="file" value="$dir_name/$file">$file</label>|;
		print qq|</li>|;
	}

	#子ディレクトリへ
	for my $dir (@dir_list){
		_load_tests($dir_name, $dir);
	}
	print qq|</ul>|;
	print qq|</li>|;
	
}

#header
sub print_header{
	print qq|
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja-JP" xml:lang="ja-JP">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>Blind Justice テストフレームワーク</title>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/jquery-ui.min.js"></script>
<script src="$framework_root/HTML/js/test_gui.js"></script>
<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/themes/redmond/jquery-ui.css">
<link rel="stylesheet" href="$framework_root/HTML/test_browser.css">
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/i18n/jquery-ui-i18n.min.js"></script>
    <script>
        \$(function(){
	    \$( '#tabs' ) . tabs();
        });
    </script>
</head>
<body>|;
}

#footer
sub print_footer{

	print $q->end_html();

}


#パスワードチェック
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	
	if($q->param("pass") ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
	
exit;
