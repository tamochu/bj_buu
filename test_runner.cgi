#!/usr/local/bin/perl --
################################################
# test_browser.cgiから呼び出されるテスト実行部分
################################################

use CGI;
$CGI::LIST_CONTEXT_WARN = 0;
use CGI::Carp;
require "./TestFramework/TestInterface.pm";
require "./TestFramework/TestResultBrowser.pm";

#結果出力用のHTML
my $output_html = "./TestFramework/result.html";

my $q = new CGI;
#テスト開始
print $q->header;

#認証
#my $in = {};
#&decode;
unless(&_is_valid_passward){
	print qq|<p>invalid pass</p><br>|;
	print $q->end_html;
	exit;
}
print qq|<p>valid pass</p><br>|;
print $q->end_html;
exit;





#設定回収
my @files = $q->param('file');
unless(@files){
	print "no file is given";
}
my @settings_save= $q->param('setting_save');

#テストインターフェースクラス生成
my $result = TestResultBrowser->new($output_html);
my $test_interface = TestInterface->new($result);

#退避
for my $setting_save (@settings_save){
	$test_interface->add_save_dir($setting_save);
}
$test_interface->save_data();

#テスト実行
$test_interface->run_all_tests(@files);
$test_interface->output_result();

#復元
$test_interface->restore_data();

#テスト結果にリダイレクト
$output_html =~ s/^\.\///;
print $q->redirect("http://localhost/bj_buu/TestFramework/result.html");
print $q->end_html;


#パスワードチェック
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	if($q->param('pass') ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
