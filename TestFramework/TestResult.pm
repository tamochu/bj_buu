package TestResult;

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
	my $message = shift;

	push($self->{ERROR_MESSAGES}, $message);
}

sub add_ok{

	my $self = shift;
	my $message = shift;

	push($self->{OK_MESSAGES}, $message);

}

sub output_result{

	my $self = shift;

	#再初期化
	$self->{OK_MESSAGES} = undef;
	$self->{ERROR_MESSAGES} = undef;
}
