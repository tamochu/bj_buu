#================================================
# 自分の作品(絵) Created by Merino
#================================================

# 作品に使う自分のﾌｫﾙﾀﾞ(book,etc,music,picture)
$goods_dir = 'picture';

# 作品の種類(img,html,cgi)
$goods_type = 'img';

# 作品の名称
$goods_name = '絵';

# 所持できる最大数
$max_goods = $max_my_picture + $m{sedai} * 3;

# 宣伝費用
$need_ad_money = 500;

# 相手に送るときの手数料(同国)
$need_send_money = 500;

# 相手に送るときの手数料(他国)
$need_send_money_other = 3000;

# お店建設費用
$build_money = 100000;

# お店における最大数
$max_shop_item = 15;



#================================================
# 上で設定したものを処理CGIに渡す
require "./lib/_myself_goods.cgi";



1; # 削除不可
