#!/usr/local/bin/perl --
################################################
# test_browser.cgiから呼び出されるテスト実行部分
################################################
use CGI;
$CGI::LIST_CONTEXT_WARN = 0;
use CGI::Carp;
require "./TestFramework/TestInterface.cgi";
require "./TestFramework/TestResultBrowser.cgi";

#フレームワークのルート
my $framework_root ="./TestFramework";
#結果出力用のHTML
my $output_html = "./TestFramework/result.html";
#戻り先
my $back_to = "test_browser.cgi";

my $q = new CGI;

&init;
&run;
&end;

#初期化
sub init{


	#ヘッダ
	print qq|
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja-JP" xml:lang="ja-JP">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>結果</title>
<link rel="stylesheet" href="$framework_root/HTML/test_browser.css">
</head>
<body>|;

	#認証
	unless(&_is_valid_passward){
		print qq|<div id="msg_window"><p class="msg_class">invalid pass</p></div><br>|;
		print $q->end_html;
		exit;
	}
}

#モード別に処理実行
sub run{

	my $mode = $q->param('mode');
	
	if($mode eq "save"){
		&_run_save;
	}
	elsif($mode eq "load"){
		&_run_load;
	}
	elsif($mode eq "script"){
		&_run_script;
	}
	elsif($mode eq "manual"){
		&_run_manual;
	}
}

#セーブモード
sub _run_save{

	#設定回収
	my $dir_to_save = $q->param('dir_to_save');
	unless($dir_to_save){
		print qq|dir_to_saveが与えられていない<br>|;
		return;
	}

	#テストインターフェースクラス生成
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);

	#セーブ
	$test_interface->add_save_dir("./data");
	$test_interface->add_save_dir("./log");
	$test_interface->add_save_dir("./html");
	$test_interface->add_save_dir("./user");
	$test_interface->save_data($dir_to_save);
	print qq|<div id="msg_window"><p class="msg_class">data, log, html, userディレクトリを$dir_to_saveにセーブした</p></div><br>|;
}

#ロードモード
sub _run_load{

	#設定回収
	my $dir_to_save = $q->param('dir_to_save');
	unless($dir_to_save){
		print qq|dir_to_saveが与えられていない<br>|;
		return;
	}

	#テストインターフェースクラス生成
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);

	#ロード
	$test_interface->add_save_dir("./data");
	$test_interface->add_save_dir("./log");
	$test_interface->add_save_dir("./html");
	$test_interface->add_save_dir("./user");
	$test_interface->restore_data($dir_to_save);
	print qq|<div id="msg_window"><p class="msg_class">data, log, html, userディレクトリを$dir_to_saveにロードした</p></div><br>|;
}

#スクリプトモード
sub _run_script{

	#設定回収
	my @files = $q->param('file');
	unless(@files){
		print qq|<div id="msg_window"><p class="msg_class">スクリプトが選択されていない</p></div><br>|;
		return;
	}
	my @settings_save= $q->param('setting_save');

	#テストインターフェースクラス生成
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);
	
	#退避ディレクトリ設定
	for my $setting_save (@settings_save){
		$test_interface->add_save_dir($setting_save);
	}
	
	#テスト実行
	$test_interface->run_all_tests(@files);
	
	#テスト結果を出力
	$test_interface->output_result();
	
	#復元
	$test_interface->restore_data();

}

#マニュアルモード
sub _run_manual{
	print qq|<div id="msg_window"><p class="msg_class">開発中</p></div><br>|;
}

#終了処理
sub end{

	#戻るボタン生成
	print qq|<form action="$back_to" method="post">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="戻る">|;
	print qq|</form>|;

	#終了
	print $q->end_html();
	exit;

}

#パスワードチェック
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	if($q->param('pass') ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
