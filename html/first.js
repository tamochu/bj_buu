var ctrlr, view, Buu = function() { };

Buu.wsurl = 'ws://buu.pandora.nu/cgi-bin/bj/mahjang_js.cgi';
Buu.ws = null;
Buu.roomIdx = null;
Buu.userList = [];

Buu.send = function (msg) {
    Buu.ws.send(String.fromCharCode(Buu.roomIdx) + msg);
}

Buu.splitSyntax1 = function(src) {
    return src.substring(1);
 }

Buu.splitSyntax2 = function(src) {
    var result = /^([^ ]*) ([^ ]*) ?(.*)$/.exec(src.substring(1));
    result.shift();
    return result;
}

Buu.splitSyntax3 = function (src) {
    return (src.substring(1)).split(' ');
}

Buu.updateUserList = function () {
    var i, foo, bar;

    document.getElementById('user-list').innerHTML = '';

    for (i = 0; i < Buu.userList.length; i++) {
        foo = Buu.userList[i].split('%');
        switch (foo[0]) {
            case view.uid:
                if (foo[0] === view.cid)
                    bar = '$@';
                else
                    bar = '　@';
                break;
            case view.cid:
                bar = '$　';
                break
            default:
                bar = '　　';
                break;
        }
        bar = '<span style = "color: white;">' + bar + '</span>';
        bar += '<span class="uid">' + foo[0] + '</span>';
        if (foo.length > 1) bar += '◆' + '<span class="trip">' + foo[1] + '</span>';

        document.getElementById('user-list').innerHTML += '<li>' + bar + '</li>';
    }
}