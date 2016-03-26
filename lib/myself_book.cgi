#================================================
# 自分の作品(本) Created by Merino
#================================================

# 作品に使う自分のﾌｫﾙﾀﾞ(book,etc,music,picture)
$goods_dir = 'book';

# 作品の種類(img,html,cgi)
$goods_type = 'html';

# 作品の名称
$goods_name = '本';

# 所持できる最大数
$max_goods = $max_my_book;

# 宣伝費用
$need_ad_money = 500;

# 相手に送るときの手数料(同国)
$need_send_money = 500;

# 相手に送るときの手数料(他国)
$need_send_money_other = 3000;

# お店建設費用
$build_money = 100000;

# お店における最大数
$max_shop_item = 30;


#================================================
# 上で設定したものを処理CGIに渡す
require "./lib/_myself_goods.cgi";



1; # 削除不可
