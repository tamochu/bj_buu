#################################################
# テストのインターフェース
#################################################

package TestInterface;

use Carp;
use File::Path;
require "./TestFramework/Controller/Accessor/SystemAccessor.pm";

sub new{

	my $class = shift;
	my $self = {};
	#出力クラス
	$self->{TEST_RESULT} = shift;

	#テスト開始前後で退避させるディレクトリ
	$self->{FOLDERS_TO_BE_SAVED} = []; 

	#ファイルを退避させておくディレクトリ
	$self->{FOLDER_TO_SAVE} = "./TestFramework/save";

	$self->{SYSTEM_ACCESSOR} = SystemAccessor->new();

	bless $self, $class;

	return $self;

}


#退避するディレクトリを追加
sub add_save_dir{

	my $self = shift;
	my $dir = shift;
	
	if(-d $dir){
		push(@{$self->{FOLDERS_TO_BE_SAVED}}, $dir);
	}
	else{
		croak "Couldn't locate $dir";
	}
}

#ゲームデータを保存
sub save_data{

	my $self = shift;

	#セーブフォルダ作成
	mkpath($self->{FOLDER_TO_SAVE});

	#コピーして退避
	for my $dir (@{$self->{FOLDERS_TO_BE_SAVED}}){
		unless (-d $dir){
			croak("Couldn't identfy $dir as an existing directory");
		}

		my $saved_dir = $dir;
		$saved_dir =~ s/^\.//;
		$saved_dir = $self->{FOLDER_TO_SAVE}.$saved_dir;
		$self->{SYSTEM_ACCESSOR}->copy_data($dir, $saved_dir);
	}

}

#退避していたデータを復元
sub restore_data{

	my $self = shift;

	#退避していたディレクトリを復元

	for my $dir (@{$self->{FOLDERS_TO_BE_SAVED}}){

		unless (-d $dir){
			croak("Couldn't find $dir in DESTROY");
		}	

		my $saved_dir = $dir;
		$saved_dir =~ s/^\.//;
		$saved_dir = $self->{FOLDER_TO_SAVE}.$saved_dir;
		$self->{SYSTEM_ACCESSOR}->move_data($saved_dir, $dir);

	}
}
#テストを指定して実行
sub run_test{

	my $self = shift;
	my $filename = shift;
	
	#テスト実行
	eval{
		require "$filename";
	};

	#失敗したファイル名と成功したファイル名をそれぞれ別個に格納
	if($@){
		$self->{TEST_RESULT}->add_error($filename, $@);	
	}
	else{
		$self->{TEST_RESULT}->add_ok($filename);
	}
}

#指定されたディレクトリの全てのテストを実行
sub run_all_tests{

	my $self = shift;
	my @dir = shift;

	#全てのテストを実行
	foreach my $filename (@dir){

		#テスト実行
		eval{
			require "$filename";
		};

		#エラーケースと成功ケースをそれぞれ別個に格納
		if($@){
			$self->{TEST_RESULT}->add_error($filename, $@);	
		}
		else{
			$self->{TEST_RESULT}->add_ok($filename);
		}
	}

}

#テスト結果を表示
sub output_result{

	my $self = shift;
	$self->{TEST_RESULT}->output_result();

}

1;
