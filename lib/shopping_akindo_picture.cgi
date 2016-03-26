#================================================
# 作品のお店(絵) Created by Merino
#================================================

# 作品に使う自分のﾌｫﾙﾀﾞ(book,etc,music,picture)
$goods_dir = 'picture';

# 作品の種類(img,html,cgi)
$goods_type = 'img';

# 作品の名称
$goods_name = '絵';


#================================================
# 上で設定したものを処理CGIに渡す
require "./lib/_shopping_akindo_goods.cgi";



1; # 削除不可
