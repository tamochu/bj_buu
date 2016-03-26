#================================================
# 作品のお店(本) Created by Merino
#================================================

# 作品に使う自分のﾌｫﾙﾀﾞ(book,etc,music,picture)
$goods_dir = 'book';

# 作品の種類(img,html,cgi)
$goods_type = 'html';

# 作品の名称
$goods_name = '本';


#================================================
# 上で設定したものを処理CGIに渡す
require "./lib/_shopping_akindo_goods.cgi";



1; # 削除不可
