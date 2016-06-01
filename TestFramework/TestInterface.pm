#################################################
# テストのインターフェース
#################################################

package TestInterface;

use Carp;
use File::Copy::Recursive qw(dircopy);

sub new{

	my $class = shift;
	my $self = {};

	#出力クラス
	$self->{TEST_RESULT} = shift;

	#テスト開始前後で退避させるフォルダ
	$self->{FOLDERS_TO_SAVE} = [ 'log', 'datas', 'user' ];
	$self->{ESCAPE_FOLDER} = "./escape";

	return bless ($self, $class);

}

#ゲームデータを保存
sub save_world{

	my $self = shift;
	my $num_folder = $self->{FOLDERS_TO_SAVE};
	--$num_folder;

	#退避先へコピー
	for my $i (0 .. $num_folder){

		my $orig = $self->{FOLDERS_TO_SAVE}[$i];
		my $dest = $self->{ESCAPE_FOLDER} . $self->{FOLDERS_TO_SAVE}[$i];

		dircopy($orig, $dest) or die @!;
			
	}

}

#ゲームデータを復元
sub recovery_world{

	my $self = shift;

	my $self = shift;
	my $num_folder = $self->{FOLDERS_TO_SAVE};
	--$num_folder;

	#元のフォルダを削除して退避先をコピー
	for my $i (0 .. $num_folder){

		my $orig = $self->{FOLDERS_TO_SAVE}[$i];
		my $dest = $self->{ESCAPE_FOLDER} . $self->{FOLDERS_TO_SAVE}[$i];

		rmdir $orig or die @!;
		dircopy($orig, $dest) or die @!;
			
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

	#エラーケースと成功ケースをそれぞれ別個に格納
	if($@){
		$self->{TEST_RESULT}->add_error($filename, $@);	
	}
	else{
		$self->{TEST_RESULT}->add_ok($filename);
	}
}

#指定されたフォルダの全てのテストを実行
sub run_all_tests{

	my $self = shift;
	my $folder = shift;

	#ディレクトリからファイル一覧を取得
	my $dh;
	opendir($dh, $folder)  
		or croak "couldn't find ", $folder, " folder\n";
	my @dir = readdir($dh);
	closedir($dh);

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
