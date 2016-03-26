window.onload = function () {
    (function () {
        try {
            (function(){
                Tkm.webAudioContext = new webkitAudioContext();

                Tkm.audio = Tkm.Audio.WEB_AUDIO_API;

                var i;
                var len1 = Tkm.soundUrlList.length;
                for (i = 0; i < len1; i++) {
                    var xhr = new XMLHttpRequest();

                    xhr.open('GET', Tkm.soundUrlList[i] + '.mp3', true);
                    xhr.responseType = 'arraybuffer';

                    xhr.onload = (function () {
                        var _i = i;

                        return function () {
                            Tkm.webAudioContext.decodeAudioData(this.response, function (buffer) {
                                Tkm.soundList[_i] = buffer;
                            });
                        }
                    })();

                    xhr.send();
                }
            })();
        } catch (e) {
            (function(){
                Tkm.audio = Tkm.Audio.CREATE_JS;

                var format = '.mp3';

                var userAgent = navigator.userAgent.toLowerCase();

                if(userAgent.match(/firefox/)) { format = '.ogg'; }

                var manifest = [];

                var i;
                var len1 = Tkm.soundUrlList.length;
                for (i = 0; i < len1; i++) {
                    manifest.push({ src: Tkm.soundUrlList[i] + format, id: i });
                }

                var queue = new createjs.LoadQueue(true);
                queue.installPlugin(createjs.Sound);
                queue.loadManifest(manifest, true);
            })();
        }

        Tkm.view = document.getElementById('play-view').contentWindow;

        document.getElementById('play-input-chat').onkeypress = function (event) {
            if (
                   this.value !== ''
                && (event.which === 13 || event.keyCode === 13)
            ) {
                Tkm.send('c' + this.value);
                this.value = '';
            }
        }

        document.getElementById('play-select-volume').selectedIndex = 2;

        document.getElementById('play-select-volume').onchange = function () {
            Tkm.volume = parseFloat(this.value);
        }
        
        Tkm.ws = new WebSocket(Tkm.wsurl);
    })();
    Tkm.ws.onopen = function () {
        Tkm.send('a');
    }
    Tkm.ws.onmessage = function (event) {
        if (Tkm.view.uid === null) {
            // フロント
            switch (event.data[0]) {
                case 'A':
                    (function () {
                        var param = Tkm.splitSyntaxType3(event.data);

                        if (param[0] === '') {
                            document.getElementById('login-error').innerHTML = 'ログイン中のユーザーはいません。';
                        } else {
                            Tkm.userList = param;
                            Tkm.updateUserList();
                        }
                        login();
                    })();
                    break;
                case 'B':
                    (function () {
                        var param = Tkm.splitSyntaxType1(event.data).split('%');

                        document.getElementById('login').style.display = 'none';
                        document.getElementById('play').style.display = 'block';
                        Tkm.view.uid = param[0];

                        Tkm.view.onLoad();
                    })();
                    break;
            }
        } else {
            // ログイン画面
            switch (event.data[0]) {
                case 'A':
                    // リフレッシュ
                    (function () {
                        var param = Tkm.splitSyntaxType3(event.data);

                        if (param[0] === '') {
                            Tkm.userList.length = 0;
                        } else {
                            Tkm.userList = param;
                        }

                        Tkm.updateUserList();
                    })();
                    break;
                case 'D':
                    // ユーザー追加
                    Tkm.userList.push(Tkm.splitSyntaxType1(event.data));
                    Tkm.updateUserList();
                    break;
                case 'E':
                    // ユーザー削除
                    (function () {
                        var param = Tkm.splitSyntaxType1(event.data);

                        var i;
                        var len1 = Tkm.userList.length;
                        for (i = 0; i < len1; i++) {
                            if (Tkm.userList[i] === param) {
                                Tkm.userList.splice(i, 1);
                                break;
                            }
                        }

                        Tkm.updateUserList();
                    })();
                    break;
                case 'F':
                    // 管理者設定
                    Tkm.view.cid = Tkm.splitSyntaxType1(event.data).split('%')[0];
                    Tkm.updateUserList();
                    break;
                case 'G':
                    // 管理者設定解除
                    Tkm.view.cid = '';
                    Tkm.updateUserList();
                    break;
                case 'H':
                    // ログ更新
                    (function () {
                        var param = Tkm.splitSyntaxType2(event.data);
                        var playLog = document.getElementById('play-log');

                        if (param[0] === '?') {
                            playLog.innerHTML += '<div class="chat"><span style="color:' + param[1]
                                                + ';">' + param[2] + '</span></div>';
                        } else {
                            playLog.innerHTML += '<div class="chat"><span class="uid">' + param[0]
                                                + '</span>:<span style="color:' + param[1] + ';">'
                                                + param[2] + '</span></div>';
                        }

                        playLog.scrollTop = playLog.scrollHeight;

                        Tkm.sound(Tkm.Sound.CHAT);
                    })();
                    break;
                case 'I':
                    // ゲームデータ
                    Tkm.view.onMessage(Tkm.splitSyntaxType1(event.data));
                    break;
                case 'J':
                    // ベル
                    if(!Tkm.isMuteBell) { Tkm._sound(Tkm.Sound.BELL); }
                    break;
                case 'K':
                    // 再ログイン要求
                    _login();
                    break;
            }
        }
    }
}

function login() {
	_login();
}

function _login() {
    var uid = document.getElementById('login-input-uid').value;
    var ratio = document.getElementById('login-input-ratio').value;

    if (uid !== '') { Tkm.send('b' + uid + ' ' + ratio); }
}

function play_button_se() {
    if (Tkm.isMuteSE) {
        Tkm.isMuteSE = false;
        document.getElementById('play-button-se').style.backgroundColor = 'orange';
    } else {
        Tkm.isMuteSE = true;
        document.getElementById('play-button-se').style.backgroundColor = 'gray';
    }
}

function play_button_bs() {
    // ミュート
    if (Tkm.isMuteBell) {
        Tkm.isMuteBell = false;
        document.getElementById('play-button-bs').style.backgroundColor = 'orange';
    } else {
        Tkm.isMuteBell = true;
        document.getElementById('play-button-bs').style.backgroundColor = 'gray';
    }
}

function play_button_dice() {
    Tkm.send('f');
}

function play_button_bell() {
    Tkm.send('e');
}

function popup_help() {
    var $d = $("<a href='cataso_help.cgi' rel='prettyPopin'></a>").prettyPopin({width: 550,followScroll:false});
    $d.click();
}

