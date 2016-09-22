sub comment_change {
	my ($bcomment, $chat_flag) = @_;
	if ($chat_flag){
		$pic_size = q|width="25px" height="25px"|;
	}else{
		$pic_size = $mobile_icon_size;
	}
	my $pai_size = q|width="12px" height="16px"|;
	$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;

	# 正規表現を使った置換連打をなるべく走らせない
	# 正規表現でパフォーマンスが落ちるのはマッチする対象が存在しなかった場合らすい（本当にマッチしないのか一生懸命探索するため）
	# 「&big(hoge)」が書かれた文章では&bigの置換操作よりもそれにマッチしない small,color,chikuwa... の各正規表現操作がネックになってそう
	# if index で振り分けてからのが速いかどうかは分からん
	if (index($bcomment, '&amp;') > -1) {
		$bcomment =~ s|&amp;big\((.*?)\)|<font size="+1">\1</font>|g;
		$bcomment =~ s|&amp;big(\d+)\((.*?)\)|<font size="+\1">\2</font>|g;
		$bcomment =~ s|&amp;small\((.*?)\)|<font size="-1">\1</font>|g;
		$bcomment =~ s|&amp;small(\d+)\((.*?)\)|<font size="-\1">\2</font>|g;
		$bcomment =~ s|&amp;color([0-9A-Fa-f]{6})\((.*?)\)|<font color="#\1">\2</font>|g;
		$bcomment =~ s|&amp;chikuwa\(\)|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|g;
		$bcomment =~ s|&amp;homashinchiw\(\)|<img src="$icondir/homashinchiw.jpg" style="vertical-align:middle;" $pic_size>|g;
		$bcomment =~ s|&amp;kappa\(\)|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>|g;
		$bcomment =~ s|&amp;homo\(\)|┌(┌^o^)┐ホモォ|g;
		$bcomment =~ s|&amp;italic\((.*?)\)|<i>\1</i>|g;
		$bcomment =~ s|&amp;bold\((.*?)\)|<b>\1</b>|g;
		$bcomment =~ s|&amp;underline\((.*?)\)|<u>\1</u>|g;
		while ($bcomment =~ /&amp;mahjong\(([mspz][1-9])(.*?)\)/) {
			$bcomment =~ s|&amp;mahjong\(([mspz][1-9])(.*?)\)|<img src="$icondir/mahjongpai/\1.gif" style="vertical-align:middle;" $pai_size>&amp;mahjong(\2)|g;
		}
		$bcomment =~ s|&amp;mahjong\((.*?)\)|\1|g;
	
		# 正規表現とかない言語ずっと使っててよく分からんし力技
		if (!$is_mobile) {
			if ($chat_flag) {
				$bcomment =~ s!&amp;img\(([^&]*?)(jpg|png)\)!<a href="./../upbbs/img-box/\1\2"><img src="./../upbbs/img-box/\1\2" $pic_size></a>!g;
			}
			else {
				$bcomment =~ s!&amp;img\(([^&]*?)(jpg|png)\)!<p class="img"><a href="./../upbbs/img-box/\1\2"><img src="./../upbbs/img-box/\1\2"></a></p>!g;
			}
			$bcomment =~ s|&amp;img\((.*?)\)|<a href="./../upbbs/img-box/\1">\1</a>|g;
		}
		else {
			$bcomment =~ s|&amp;img\((.*?)\)|<a href="./../upbbs/img-box/\1">\1</a>|g;
		}
	}

	return $bcomment;
}


1; # 削除不可
