#=================================================
# BBS,CHAT自動更新用ルーチン
#=================================================

#=================================================
# 書き込み処理
#=================================================
sub auto_loader {
	my ($file_name, $ten_limit) = @_;
	
	my $head_str = '';
	$head_str .= "<script>\n";
	$head_str .= "\$(document).ready(function(){\n";
	$head_str .= "setInterval(function(){auto_load();}, 5000);\n";
	$head_str .= "});\n";
	$head_str .= "function auto_load() {\n";
	$head_str .= "\$.get(\"chat_ajax.cgi\",\n";
	$head_str .= "{id: \"$in{id}\", pass: \"$in{pass}\", file: \"$file_name\", ten_limit: \"$ten_limit\"},\n";
	$head_str .= "function(html){\n\$(\"#body_mes\").html(html);\n});\n";
	$head_str .= "}\n";
	$head_str .= "</script>\n";
	return $head_str;
}

1; # 削除不可
