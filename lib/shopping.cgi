#================================================
# ｼｮｯﾋﾟﾝｸﾞ Created by Merino
#================================================

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['戻る', 		'main'],
	['次のﾍﾟｰｼﾞ',	'shopping2'],
	['商人のお店',	'shopping_akindo'],
	['美の画伯館',	'shopping_akindo_picture'],
	['ﾌﾞｯｸﾏｰｹｯﾄ',	'shopping_akindo_book'],
	['商人の銀行',	'shopping_akindo_bank'],
	['違法ｶｼﾞﾉ',	'shopping_akindo_casino'],
	['ｵｰｸｼｮﾝ会場',	'shopping_auction'],
	['ｼﾞｬﾝｸｼｮｯﾌﾟ',	'shopping_junk_shop'],
	['育て屋',	'shopping_breeder'],
	['ｶｼﾞﾉﾍﾞｶﾞｽ',	'shopping_casino'],
	['ｶｼﾞﾉ交換所',	'shopping_casino_exchange'],
	['闘技場',		'shopping_colosseum'],
	['黒十字病院',	'shopping_hospital'],
);

if (&on_december) {
	push @menus, ['年末売出', 'shopping_december'];
}
#================================================
sub begin {
	$mes .= 'どこに行きますか?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  { &b_menu(@menus); }



1; # 削除不可
