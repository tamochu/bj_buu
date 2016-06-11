#!/usr/local/bin/perl --

package test_browser;
use CGI::Carp;

#フレームワークのルート
my $framework_root = "./TestFramework";
#フレームワーク直下のテストフォルダ
my $test_root = "Tests";
#テストを実行するcgi
my $test_runner = "./test_runner.cgi";

my $in = {};

&decode;
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

	print qq|<form action="$test_runner" method="post">|;

	#チェックボックス作成
	print qq|<div id="treeList" style = "background-color: lavender">|;
	print qq|<label>テスト選択</label>|;
	print qq|<ul>|;
	_load_tests($framework_root,$test_root);
	print qq|</ul>|;
	print qq|</div>|;

	#設定用div作成
	print qq|<div id="settingWindow" style = "background-color: lavender">|;
	print qq|<label>設定選択</label>|;
	print qq|<ul>テスト前にTestFramework/saveに保存するディレクトリ|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./log" checked="checked">log</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./data" checked="checked">data</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./html" checked="checked">html</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./user" checked="checked">user</label></li>|;
	print qq|</ul>|;
	print qq|</div>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" name="submit" value="実行">|;
	print qq|</form>|;

	#メッセージウィンドウ
	print qq|<div id="messageWindow" style = "background-color: lavender; border:#ff0000 solid 1px;">|;
	print qq|<p>開発中。触るな危険</p>|;
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
			push(@file_list, $name);
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
<html>
  <head>
    <title>TestFramework</title>
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<script type='text/javascript' src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.js"></script>
	<script type='text/javascript' src="$framework_root/js/test_gui.js"></script>
      </head>
  <body>
  |;
}

#footer
sub print_footer{
	print qq|
</body>
</html>|;
}

#decode
sub decode{
	my ($k,$v,$buf);
	my $err_flag = 0;
	
	if ($ENV{REQUEST_METHOD} eq 'POST') {
		&error if $ENV{CONTENT_LENGTH} > 51200;
		read STDIN, $buf, $ENV{CONTENT_LENGTH};
	}
	else {
		&error if length $ENV{QUERY_STRING} > 51200;
		$buf = $ENV{QUERY_STRING};
	}
	
	for my $pair (split /&/, $buf) {

		($k,$v) = split /=/, $pair;
		$v =~ tr/+/ /;
		$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack 'H2', $1/eg;

		# 記号置換え
		$v =~ s/&/&amp/g;
		$v =~ s/;/&#59;/g;
		$v =~ s/&amp/&amp;/g;
		$v =~ s/,/&#44;/g;
		$v =~ s/</&lt;/g;
		$v =~ s/>/&gt;/g;
		$v =~ s/"/&quot;/g;#"
		$v =~ s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]//g;
		$v =~ s/\.\.\///g;
		$v =~ s/【ダイス】/(ダイス)/g;
		
		$in{$k} = $v;
		
		push @delfiles, $v if $k eq 'delete';
	}
	$cmd = $in{cmd};
}

#パスワードチェック
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	if($in{pass} ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
	
exit;

