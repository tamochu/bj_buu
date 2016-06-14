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
		$self->{HTML_PATH} = "./TestFramework/result.dat";
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

#出力用の中間HTML（body部のみ)を生成して保存
sub output_result{

	my $self = shift;

	#ＯＫメッセージ
	print qq|<b>OK</b><br>|;
	print qq|<div style = "background-color: lavender; border:#000000 solid 1px">|;
	for my $ok_filename (@{$self->{OK_MESSAGES}}){
		 print qq|<font color="blue">$ok_filename</font><br>|;
	}
	print qq|</div>|;

	print qq|<br>*************************************<br><br><b>Error</b><br>|;

	#ＥＲＲＯＲメッセージ
	for my $message (@{$self->{ERROR_MESSAGES}}){
		print qq|<div style = "background-color: lavender; border:#000000 solid 1px">|;
		print  qq|<font color="red"><b>$message->[0]<b></font><br>|;
		$message->[1] =~ s/\n/<br>/g;
		print  qq|$message->[1]|;
		print qq|</div><br>|;
	}
}

1;
