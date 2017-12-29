#=================================================
# 討伐ﾌｨｰﾙﾄﾞ設定 Created by Merino
#=================================================
# ◎追加/削除/変更/並び替え可
# ※No10以上増やす場合は./log/monster/にﾌｧｲﾙを追加してね

# *その数値以上のﾓﾝｽﾀｰが生息：例> 森なら300以上600未満の強さの魔物が生息
@places = (
#[0]No,[1]*強さ,[2]名前,			[3]拾えるﾀﾏｺﾞ
	['beginner',	0,		'新兵訓練場',		[51],	],
	[0,	30,		'ﾎﾟｶﾎﾟｶ平原',		[4..24,42,43,50,51],	],
	[1,	300,	'ﾓﾘﾓﾘ森',			[1,4..24,43,50],		],
	[2,	600,	'ﾃﾞﾛﾃﾞﾛ沼',			[1,4..31,33,43,48,50],	],
	[3,	1000,	'ｿｰﾀﾞｰ海',			[1,4..31,33,43..46,48],	],
	[4,	1500,	'ｶｯｻﾘ砂漠',			[1..33,43..50],			],
	[5,	2500,	'ｺﾞﾂｺﾞﾂ山',			[1..50],				], # 1..36,38,39,41..50
	[6,	4000,	'空白の跡地',		[2..41],				],
	[7,	6000,	'封印されし魔界',	[2..41],				],
	['boss',	999999,	'君の銀の庭',	[2,3,38,40,41],				],
);
# 君の銀の庭でｴﾝｼﾞｪﾙ拾えるから山のｴﾝｼﾞｪﾙ削除された？ ｺﾞｯﾄﾞは空白・封印
# ボスや君の銀の庭の使い勝手によってはまた変更されるかも

1; # 削除不可
