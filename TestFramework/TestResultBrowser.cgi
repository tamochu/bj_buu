#################################
# test_browser.cgiのテスト結果出力クラス
#################################
package TestResultBrowser;
use CGI::Carp;

sub new{

	my $class = shift;
	my $self = {};

	#出力時のHTMLのパス
	#コンストラクタで与えられなければデフォルト値
	$self->{HTML_PATH} = shift;	
	unless($self->{HTML_PATH}){
		$self->{HTML_PATH} = "./TestFramework/result.html";
	}

	#メッセージのプール
	$self->{OK_MESSAGES} = [];
	$self->{ERROR_MESSAGES} = [];

	return bless ($self, $class);

}

#プールにメッセージをプッシュ
sub add_error{

	my $self = shift;
	my ($filename, $message) = @_;

	my $set = [$filename, $message];

	push(@{$self->{ERROR_MESSAGES}}, $set);
}

sub add_ok{

	my $self = shift;
	my $filename = shift;

	push(@{$self->{OK_MESSAGES}}, $filename);

}

#出力用のHTMLを生成
sub output_result{

	my $self = shift;


	open(FH, "> $self->{HTML_PATH}") or croak("Can't open $self->{HTML_PATH}, $@");
	print FH qq|<html><head><title>Results></title></head><body>|;
	print FH qq|<b>OK</b><br>|;
	for my $ok_filename (@{$self->{OK_MESSAGES}}){
		 print FH qq|$ok_filename<br>|;
	}

	print FH qq|<br>*************************************<br><br><b>Error</b><br>|;
	for my $message (@{$self->{ERROR_MESSAGES}}){
		print FH qq|<font color="red">$message->[0]</font><br>|;
		print FH qq|$message->[1]<br><br><br>|;
	}

	print FH qq|</body></html>|;
	close FH;
}

1;
