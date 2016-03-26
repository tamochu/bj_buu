window.onload = function () {
    var queue = new createjs.LoadQueue(true);
    queue.installPlugin(createjs.Sound);
    queue.loadManifest(Buu.manifest, true);

    view = document.getElementById('view').contentWindow;

    Buu.ws = new WebSocket(Buu.wsurl);

    Buu.ws.onopen = function () {
        Buu.send('a');
    }

    Buu.ws.onmessage = function (evnt) {
        var i, foo, bar, optn;

        if (view.uid === null) {
            switch (evnt.data[0]) {
                case 'A':
                    optn = Buu.splitSyntax3(evnt.data);
                    if (optn[0] === '')
                        Buu.userList.length = 0;
                    else
                        Buu.userList = optn;
                    if (Buu.userList.length > 0) {
                        document.getElementById('login-users').innerHTML = '';
                        for (i = 0; i < Buu.userList.length; i++) {
                            foo = Buu.userList[i].split('%');
                            bar = '<span class="uid">' + foo[0] + '</span>';
                            if (foo.length > 1) bar += '◆' + '<span class="trip">' + foo[1] + '</span>';
                            document.getElementById('login-users').innerHTML += '<li>' + bar + '</li>';
                        }
                    } else {
                        document.getElementById('login-users').innerHTML = '<li>ログイン中のユーザーはいません。</li>';
                    }
                    break;
                case 'B':
                    document.getElementById('login').style.display = 'none';
                    document.getElementById('play').style.display = 'block';
                    view.onLoad();
                    foo = (Buu.splitSyntax1(evnt.data)).split('%');
                    view.uid = foo[0];
                    document.getElementById('chat-text').onkeypress = function (e) {
                        if (this.value !== '' && (e.which === 13 || e.keyCode === 13)) {
                            Buu.send('c' + this.value);
                            this.value = '';
                        }
                    }
                    document.getElementById('chat-silent-btn').onclick = function () {
                        if (this.alt === 'on') {
                            this.src = '../img/chat-off.png';
                            this.alt = 'off';
                        } else {
                            this.src = '../img/chat-on.png';
                            this.alt = 'on';
                        }
                    }
                    document.getElementById('se-silent-btn').onclick = function () {
                        if (this.alt === 'on') {
                            this.src = '../img/se-off.png';
                            this.alt = 'off';
                        } else {
                            this.src = '../img/se-on.png';
                            this.alt = 'on';
                        }
                    }
                    Buu.updateUserList();
                    break;
                case 'C':
                    document.getElementById('err-msg').style.display = 'block';
                    break;
            }
        } else {
            switch (evnt.data[0]) {
                case 'A':
                    optn = Buu.splitSyntax3(evnt.data);
                    if (optn[0] === '')
                        Buu.userList.length = 0;
                    else
                        Buu.userList = optn;
                    Buu.updateUserList();
                    break;
                case 'D':
                    optn = Buu.splitSyntax1(evnt.data);
                    Buu.userList.push(optn);
                    Buu.updateUserList();
                    break;
                case 'E':
                    optn = Buu.splitSyntax1(evnt.data);
                    for (i = 0; i < Buu.userList.length; i++) {
                        if (Buu.userList[i] === optn) {
                            Buu.userList.splice(i, 1);
                            break;
                        }
                    }
                    Buu.updateUserList();
                    break;
                case 'F':
                    foo = (Buu.splitSyntax1(evnt.data)).split('%');
                    view.cid = foo[0];
                    Buu.updateUserList();
                    break;
                case 'G':
                    view.cid = '';
                    Buu.updateUserList();
                    break;
                case 'H':
                    if (document.getElementById('chat-silent-btn').alt === 'on') Buu.sound('chat');
                    optn = Buu.splitSyntax2(evnt.data);
                    if (optn[0] === '?') {
                        document.getElementById('log').innerHTML
                            += '<span style="color: ' + optn[1] + ';">' + optn[2] + '</span></br>';
                    } else {
                        document.getElementById('log').innerHTML
                            += '<span class="uid">' + optn[0]
                            + '</span>:<span style="color: ' + optn[1] + ';">'
                            + optn[2] + '</span></br>';
                    }
                    document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight;
                    break;
                case 'I':
                    view.onMessage(Buu.splitSyntax1(evnt.data));
                    break;
            }
        }

        document.getElementById('login-btn').onclick = function () {
            var login_uid = document.getElementById('login-uid');

            if (login_uid.value !== '') {
                Buu.send('b' + login_uid.value);
                login_uid.value = '';
            }
        }
    }
}