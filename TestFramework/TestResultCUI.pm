#################################
# TestCUI用のテスト結果出力クラス
#################################
package TestResultCUI;

sub new{

	my $class = shift;
	my $self = {};

	#メッセージのプール
	$self->{OK_MESSAGES} = [];
	$self->{ERROR_MESSAGES} = [];

	return bless ($self, $class);

}

#プールにメッセージをプッシュ
sub add_error{

	my $self = shift;
	my ($filename, $message) = @_;

	my %set = (where=>$filename, message=> $message);
	push($self->{ERROR_MESSAGES}, \%set);
}

sub add_ok{

	my $self = shift;
	my $filename = shift;

	push($self->{OK_MESSAGES}, $filename);

}

sub output_result{

	my $self = shift;

	print "\n\n***ok results***\n\n";

	for my $ok_filename (@{$self->{OK_MESSAGES}}){
		print qq/ok : $ok_filename\n/;
	}

	print "\n\n***error results***\n\n";
	for my $message (@{$self->{ERROR_MESSAGES}}){
		print qq/error: at $message->{where}\n$message->{message}\n\n/;
	}


	#再初期化
	$self->{OK_MESSAGES} = undef;
	$self->{ERROR_MESSAGES} = undef;
	print "\n***results reinitalized***\n";
}

1;
