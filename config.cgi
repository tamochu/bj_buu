require './lib/system.cgi';
#================================================
$VERSION = '2.71';
# 基本設定 Created by Merino
#================================================
# 国設定管理室のURL
# http://自分のURL/bj/admin_country.cgi?pass=管理者ﾊﾟｽﾜｰﾄﾞ
#
# ﾌﾟﾚｲﾔｰ管理室のURL
# http://自分のURL/bj/admin.cgi?pass=管理者ﾊﾟｽﾜｰﾄﾞ
# 
# ※「自分のURL」とはこのCGIを設置した場所までのｱﾄﾞﾚｽ
#================================================

# ﾒﾝﾃﾅﾝｽ表示(分) 通常稼動時は「0」
$mente_min = 0;

# 管理ﾊﾟｽﾜｰﾄﾞ(適当な半角英数字に必ず変更してください)
require './admin_password.cgi';

# 管理人ﾌﾟﾚｲﾔｰ名
$admin_name = '黒豚';

# gzip圧縮転送(わからない・使わない場合は空欄 '' )
$gzip = '';

# 携帯機種によりPNGが非表示なので
# 強制JPEG出力設定(0:PNG or JPEG, 1:JPEGのみ) 
$is_force_jpeg = 0;

# ----------------------------
# ﾀｲﾄﾙ
$title = 'Blind Justice';

# ﾀｲﾄﾙ画像(必要ない場合は「''」)
$title_img = './html/title.jpg';

# 戻り先URL
$home = 'http://buu.pandora.nu/';

# 大陸の名前
$world_name = 'ﾕｸﾞﾄﾞﾗﾙ';

# ----------------------------
# 最大登録人数
$max_entry = 400;

# 最大ﾛｸﾞｲﾝ人数
$max_login = 300;

# 最大ﾌﾟﾚｲ人数
$max_playing = 250;

# Topのﾛｸﾞｲﾝﾘｽﾄに表示する時間(分)
$login_min = 20;

# ----------------------------
# 機種判別によりﾍﾟｰｼﾞの切り替え(0:PC携帯判別、1:PCでも携帯画面)
# 携帯専用ﾍﾟｰｼﾞにする場合や携帯画面を確認する場合などに「1」
$is_mobile = 0;
$is_smart = 0;

# 携帯用bodyﾀｸﾞ
$body = 'bgcolor="#000000" text="#CCCCCC" link="#3366FF" vlink="#CC00FF" alink="#663333"';

# ----------------------------
# ﾃﾞﾌｫﾙﾄのｱｲｺﾝ画像(iconﾌｫﾙﾀﾞの中のﾌｧｲﾙ名 例> '000.gif' )
# ｱｲｺﾝを使わない場合は空欄('')
$default_icon = '000.gif';

# 自動削除期間(日)。この日にちを超えてもﾛｸﾞｲﾝしないﾕｰｻﾞｰは削除
$auto_delete_day = 30;

# 売上ﾗﾝｷﾝｸﾞ更新周期(日)。このﾀｲﾐﾝｸﾞで売上 0 Gのお店は削除
$sales_ranking_cycle_day = 15;

# 基本拘束時間(分) Game Standard Wait Time
$GWT = 20;

# 給与をもらえる間隔(時)
$salary_hour = 6;

# 君主任期周期(ｹﾞｰﾑ内での年)
$reset_ceo_cycle_year = 3;

# 代表任期周期(ｹﾞｰﾑ内での年)
$reset_daihyo_cycle_year = 5;

# ----------------------------
# 右下に表示される著作表示。HTMLﾀｸﾞ使用可能(「$copyright = <<"EOM";」～「EOM」の間に記述)
$copyright = <<"EOM";
<!-- ここから -->



<!-- ここまで -->
EOM

# ----------------------------
# 過去の栄光、物流情報、手紙やBBSなどの基本設定(※設定変更がない場合は以下がﾍﾞｰｽとなる)
# ----------------------------
# 最大ﾛｸﾞ保存件数
$max_log = 50;

# ----------------------------
# 手紙やBBSなどの基本設定(※設定変更がない場合は以下がﾍﾞｰｽとなる)
# ----------------------------
# 連続書き込み禁止時間(秒)
$bad_time    = 30;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 2000;

# ※個別に設定変更をする場合は、処理される前に変数の値を変えれば良い(blog.cgiなど参照)


# ----------------------------
# ﾀｲﾄﾙがない場合(日記)
$non_title = '無題';

# 絵の最大所持数
$max_my_picture = 15;

# 本の最大所持数
$max_my_book = 30;


#================================================
# ｽﾊﾟﾑ/荒らし対策設定
#================================================
# ｱｸｾｽ拒否者へのメッセージ
$deny_message = 'あなたのIPｱﾄﾞﾚｽはｱｸｾｽ制限がかかっています';

# ｱｸｾｽ拒否ﾘｽﾄ「 '禁止IPｱﾄﾞﾚｽまたはﾎｽﾄ名', 」
# ｱｽﾀﾘｽｸ(*)で前方一致(例> '*.proxy',)、後方一致(例> '127.0.0.*',)
@deny_lists = (
	'*.anonymizer.com',
	'p*-ipngn100105matuyama.ehime.ocn.ne.jp',
	'',
);


#================================================
# 各ファイル設定
#================================================
$userdir  = './user';
$icondir  = './icon';
$logdir   = './log';
$datadir  = './data';
$htmldir  = './html';

$script       = 'bj.cgi';
$script_index = 'index.cgi';

$method = 'POST';
$chmod  = 0666;


#================================================
# 携帯端末判別処理
#================================================
$agent = $ENV{HTTP_USER_AGENT};
if ($is_mobile
	|| $agent =~ /DoCoMo/  # DoCoMo
	|| $agent =~ /KDDI|UP\.Browser/  # Ez
	|| $agent =~ /J-PHONE|Vodafone|SoftBank/  # SoftBank
#	|| $agent =~ /DDIPOCKET|WILLCOM/  # AIR-HDGE PHONE
#	|| $agent =~ /ASTEL/  # ドットi端末
	|| $ENV{HTTP_X_JPHONE_MSNAME}) {
		$is_mobile = 1;
		$method  = 'GET';

		if ($ENV{HTTP_X_DCMGUID}) {
			$agent = '固体識別番号'.$ENV{HTTP_X_DCMGUID}.'　'.$agent;
		}
		elsif ($ENV{HTTP_X_UP_SUBNO}) {
			$agent = '固体識別番号'.$ENV{HTTP_X_UP_SUBNO}.'　'.$agent;
		}
		
		# ----------------------------
		# 携帯時の戻り先URL
		$home = 'http://buu.pandora.nu';
	
		# 顔ｱｲｺﾝを使用している場合のｱｲｺﾝｻｲｽﾞ調整
		$mobile_icon_size = q|width="25px" height="25px"|;
}

if ($is_smart
	|| $agent =~ /iPhone/i  # iPhone
	|| $agent =~ /Android/i  # Android
	) {
		$is_smart = 1;
		
		# 顔ｱｲｺﾝを使用している場合のｱｲｺﾝｻｲｽﾞ調整
		$mobile_icon_size = q|width="25px" height="25px"|;
}


#================================================
# javascriptファイル更新変数
#================================================
$jstime = '201510311654';
1; # 削除不可
