enchant();

(function(definition){// 定義する関数を引数にとる
    // ロードされた文脈に応じてエクスポート方法を変える

    // CommonJS
    if (typeof exports === "object") {
        module.exports = definition();

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
        define(definition);

    // <script>
    } else {
        MahjongTehai = definition();
    }

})(function(){// 実際の定義を行う関数
    'use strict';
    
    var MahjongTehai = {};
    
    MahjongTehai.game_ = null;
    MahjongTehai.setGame = function(game) {
        MahjongTehai.game_ = game;
    };
    // 鳴き牌・面子を表すインナークラス
    MahjongTehai.Naki = Class.create({
        // コンストラクタ
        initialize: function() {
            this.paiNaki = MahjongPai.Pai();
            this.pai1 = MahjongPai.Pai();
            this.pai2 = MahjongPai.Pai();
            this.kanFlag = 0;// 0:ポン・チー 1:明槓 2:暗槓 -1:面前面子
            this.nakiFrom = 3;// 3:上家 2:対面 1:下家
        },
        
        // 鳴き牌を文字列から設定する関数。public
        setNaki: function(str) {
            var split_str = str.split('');
            if (split_str[0] == '-') {
                if (split_str[split_str.length - 1] == '-') {
                    // 対面ポン
                    this.pai1.setFrame(split_str[1] + split_str[2]);
                    this.paiNaki.setFrame(split_str[3] + split_str[4]);
                    this.pai2.setFrame(split_str[5] + split_str[6]);
                    if (split_str.length === 10) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 2;
                } else {
                    // 上家ポンチー
                    this.paiNaki.setFrame(split_str[1] + split_str[2]);
                    this.pai1.setFrame(split_str[3] + split_str[4]);
                    this.pai2.setFrame(split_str[5] + split_str[6]);
                    if (split_str.length === 9) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 3;
                }
            } else {
                if (split_str[split_str.length - 1] === '-') {
                    // 下家ポン
                    this.pai1.setFrame(split_str[0] + split_str[1]);
                    this.pai2.setFrame(split_str[2] + split_str[3]);
                    this.paiNaki.setFrame(split_str[4] + split_str[5]);
                    if (split_str.length === 9) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 1;
                } else {
                    // 暗槓
                    this.paiNaki.setFrame(split_str[0] + split_str[1]);
                    this.pai1.setFrame(split_str[2] + split_str[3]);
                    this.pai2.setFrame(split_str[4] + split_str[5]);
                    this.kanFlag = 2;
                    this.nakiFrom = 0;
                }
            }
        },
        
        // 面子を文字列から設定する関数。public
        setMentsu: function(str) {
            var split_str = str.split('');
            this.paiNaki.setFrame(split_str[0] + split_str[1]);
            this.pai1.setFrame(split_str[2] + split_str[3]);
            this.pai2.setFrame(split_str[4] + split_str[5]);
            this.kanFlag = -1;
        },
        
        // 読み込み可能な文字列に変換する関数。public
        toString: function() {
            var retStr = "";
            if (this.kanFlag === 2) {
                for (var i = 0; i < 4; i++) {
                    retStr += this.paiNaki.str;
                }
            } else {
                if (this.kanFlag !== -1) {
                    if (this.nakiFrom === 2 || this.nakiFrom === 3) {
                        retStr += "-";
                    }
                }
                retStr += this.paiNaki.str + this.pai1.str + this.pai2.str;
                if (this.kanFlag === 1) {
                    retStr += this.paiNaki.str;
                }
                if (this.kanFlag !== -1) {
                    if (this.nakiFrom === 1 || this.nakiFrom === 2) {
                        retStr += "-";
                    }
                }
            }
            return retStr;
        },
        
        // 利便性のため色々判定する関数。順子。public
        isShuntsu: function() {
            return (this.pai1.str !== this.pai2.str);
        },
        
        // 利便性のため色々判定する関数。刻子。public
        isKotsu: function() {
            return (this.pai1.str === this.pai2.str);
        },
        
        // 利便性のため色々判定する関数。ポン。public
        isPon: function() {
            return (this.isKotsu() && this.kanFlag === 0);
        },
        
        // 利便性のため色々判定する関数。暗刻。public
        isAnko: function() {
            return (this.isKotsu() && this.kanFlag === -1);
        },
        
        // 利便性のため色々判定する関数。明槓。public
        isMinkan: function() {
            return (this.isKotsu() && this.kanFlag === 1);
        },
        
        // 利便性のため色々判定する関数。暗槓。public
        isAnkan: function() {
            return (this.isKotsu() && this.kanFlag === 2);
        },
        
        // 利便性のため色々判定する関数。一九牌を含むか。public
        isIku: function() {
            if (this.pai1.isIku()) {
                return true;
            }
            if (this.pai2.isIku()) {
                return true;
            }
            if (this.paiNaki.isIku()) {
                return true;
            }
            
            return false;
        },
        
        // 利便性のため色々判定する関数。字牌か。public
        isTsu: function() {
            var type = this.pai1.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            type = this.pai2.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            type = this.paiNaki.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            
            return false;
        },
        
        // 利便性のため色々判定する関数。一九字牌を含むか。public
        isYaochu: function() {
            return (this.isIku() || this.isTsu());
        }
    });
    // 手牌を面子ごとに分けて保持する点数などの計算用インナークラス。
    MahjongTehai.MentsuSeparatedTehai = Class.create({
        // コンストラクタ
        initialize: function() {
            this.mentsu = [];
            this.janto = MahjongPai.Pai();
            this.finishShape = 0;// 0:両面 1:シャボ 2:嵌張 3:辺張 4:単騎
            this.tehai = null;// 天和等のフラグを保存するために手牌クラスも持つ
        },
        
        // 手牌を設定する関数。public
        setTehai: function(tehai) {
            this.tehai = tehai;
            for (var i = 0; i < this.tehai.naki.length; i++) {
                this.addMentsu(this.tehai.naki[i]);
            }
        },
        
        // 面子を追加する関数。public
        addMentsu: function(naki) {
            this.mentsu.push(naki);
        },
        
        // 雀頭を設定する関数。public
        setJanto: function(str) {
            this.janto.setFrame(str);
        },
        
        // 上がりが他を設定する関数。public
        setFinishShape: function(shape) {
            this.finishShape = shape;
        }, 
        
        // 面子のゲッター。public
        getMentsu: function(index) {
            if (index >= 0 && index < this.mentsu.length) {
                return this.mentsu[index];
            }
            return null;
        },
        
        // 順子を数える関数。public
        countShuntsu: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isShuntsu()) {
                    count++;
                }
            }
            return count;
        },
        
        // 刻子を数える関数。public
        countKotsu: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isKotsu()) {
                    count++;
                }
            }
            return count;
        },
        
        // 面子が4つあるか調べる関数。public
        is4Mentsu: function() {
            return ((this.countShuntsu() + this.countKotsu()) === 4);
        },
        
        // 暗刻の数を数える関数。public
        countAnko: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isAnko() || this.mentsu[i].isAnkan()) {
                    count++;
                }
            }
            return count;
        },
        
        // 槓子の数を数える関数。public
        countKan: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isMinkan() || this.mentsu[i].isAnkan()) {
                    count++;
                }
            }
            return count;
        },
        
        // 面前か判定する関数。public
        isMenzen: function() {
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].kanFlag !== -1 && this.mentsu[i].kanFlag !== 2) {
                    return false;
                }
            }
            return true;
        },
        
        // 符の計算をする関数。public
        calcHu: function(ba, kaze) {
            // 符計算
            var hu = 20;
            if (this.janto.str === ba) {
                hu += 2;
            }
            if (this.janto.str === kaze) {
                hu += 2;
            }
            if (this.finishShape === 2 || this.finishShape === 3 || this.finishShape === 4) {
                hu += 2;
            }
            for (var i = 0; i < this.mentsu.length; i++) {
                var addHu = 0;
                if (this.mentsu[i].isPon()) {
                    addHu = 2;
                } else if (this.mentsu[i].isAnko()) {
                    if (this.finishShape === 1 && this.mentsu[i].pai1.str === this.tehai.lastAddPai.str) {
                        addHu = 2;
                    } else {
                        addHu = 4;
                    }
                } else if (this.mentsu[i].isMinkan()) {
                    addHu = 8;
                } else if (this.mentsu[i].isAnkan()) {
                    addHu = 16;
                }
                if (this.mentsu[i].isYaochu()) {
                    addHu *= 2;
                }
                hu += addHu;
            }

            if (hu % 10 > 0) {
                hu += 10 - (hu % 10);
            }
            return hu;
        },
        
        // 飜数を計算する関数。public
        calcFan: function(ba, kaze) {
            // 飜計算
            var fan = 0;
            var yaku = '';
            var yakuList = [];
            for (var ruleI = 0; ruleI < MahjongTehai.Rule.ruleSize(); ruleI++) {
                var rule = MahjongTehai.Rule.getRule(ruleI);
                var result = rule(this, ba, kaze);
                if (result[0] > 0) {
                    yakuList.push(result);
                }
            }
            var isYakuman = false;
            for (var yakuI = 0; yakuI < yakuList.length; yakuI++) {
                if (yakuList[yakuI][0] >= 13) {
                    isYakuman = true;
                }
            }
            for (var yakumanI = 0; yakumanI < yakuList.length; yakumanI++) {
                if (!isYakuman || yakuList[yakumanI][0] >= 13) {
                    fan += yakuList[yakumanI][0];
                    yaku += yakuList[yakumanI][1] + ',';
                }
            }
            // ドラ加算
            if (fan > 0) {
                var doraNum = 0;
                var hist = this.tehai.toHistogramAll();
                var doras = this.tehai.getDoras();
                for (var doraI = 0; doraI < doras.length; doraI++) {
                    var doraHyouji = doras[doraI];
                    var doraStr = MahjongPai.getDoraNextStr(doraHyouji);
                    doraNum += hist[MahjongPai.strToNum(doraStr)];
                }
                if (doraNum > 0) {
                    fan += doraNum;
                    yaku += 'ドラ' + doraNum + ',';
                }
            }
            return [fan, yaku];
        },
        
        // 点数を計算する関数。public
        calcPoint: function(ba, kaze) {
            var hu = this.calcHu(ba, kaze);
            var fan = this.calcFan(ba, kaze);
            return MahjongTehai.calcPointFromHuAndFan(hu, fan, this.tehai.isTsumo(), kaze === 'z1');
        },
        
        // 自分と同じインスタンスを返す関数。public
        clone: function() {
            var ret = MahjongTehai.MentsuSeparatedTehai();
            ret.setTehai(this.tehai);
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].kanFlag === -1) {
                    var mentsu = MahjongTehai.Naki();
                    mentsu.setMentsu(this.mentsu[i].toString());
                    ret.mentsu.push(mentsu);
                }
            }
            ret.janto.setFrame(this.janto.str);
            ret.finishShape = this.finishShape;            
            return ret;
        }
    });
    // 手牌のクラス本体
    MahjongTehai.Tehai = Class.create({
        // コンストラクタ
        initialize: function() {
            this.tehai = [];
            this.naki = [];
            this.position = 0;// 0:下 1:右 2:上 3:左
            this.mine = 1;
            this.tsumoFlag = false;
            this.chankanFlag = false;
            this.tenhoFlag = false;
            this.chihoFlag = false;
            this.reachFlag = false;
            this.doubleReachFlag = false;
            this.ippatsuFlag = false;
            this.rinshanFlag = false;
            this.haiteiFlag = false;
            this.doras = [];
            this.agariHai = null;
            this.lastAddPai = null;
            this.selected = null;
        },
        
        // 自分と同じインスタンスを返す関数。public
        clone: function() {
            var ret = MahjongTehai.Tehai();
            ret.setAll(this.toString());
            ret.position = this.position;
            ret.mine = this.mine;
            ret.tsumoFlag = this.tsumoFlag;
            ret.chankanFlag = this.chankanFlag;
            ret.tenhoFlag = this.tenhoFlag;
            ret.chihoFlag = this.chihoFlag;
            ret.reachFlag = this.reachFlag;
            ret.doubleReachFlag = this.doubleReachFlag;
            ret.ippatsuFlag = this.ippatsuFlag;
            ret.rinshanFlag = this.rinshanFlag;
            ret.haiteiFlag = this.haiteiFlag;
            ret.doras = this.doras;
            ret.lastAddPai = this.lastAddPai;
            ret.selected = this.selected;
            
            return ret;
        },
        
        // 位置を設定する関数。public
        setPosition: function(position) {
            this.position = position;
        },
        
        // 対戦用自分の手牌かどうかを設定する関数。public
        setMine: function(mine) {
            this.mine = mine;
        },
        
        // 手牌を読み込む関数。
        setTehai: function(str) {
            var split_str = str.split('');
            this.tehai = [];
            var i = 0;
            while (i < split_str.length) {
                if (split_str[i] === ' ') {
                    break;
                }
                var pai = MahjongPai.Pai();
                pai.setFrame(split_str[i] + split_str[i + 1]);
                this.tehai.push(pai);
                i += 2;
            }
        },
        
        setSelected: function(selecting) {
            this.selected = selecting;
        },
        
        // 鳴き牌を含め手牌を読み込む関数。public
        setAll: function(str) {
            this.naki = [];
            var split_str = str.split(' ');
            for (var i = 0; i < split_str.length; i++) {
                if (i === 0) {
                    this.setTehai(split_str[i]);
                } else {
                    var huro = MahjongTehai.Naki();
                    huro.setNaki(split_str[i]);
                    this.naki.push(huro);
                }
            }
        },
        
        // 手牌に追加する関数。引数はMahjongPai.Pai。public
        add: function(pai) {
            this.tehai.push(pai);
            if (this.lastAddPai === null) {
                this.lastAddPai = MahjongPai.Pai();
            }
            this.lastAddPai.setFrame(pai.str);
            this.setIds();
            this.refresh();
        },
        
        // チーしたときに呼ぶ関数。引数はチーした牌とチーした形。public
        chi: function(pai, type) {
            var pai1Str = pai.getType() + (pai.getNum() - 1);
            var pai2Str = pai.getType() + (pai.getNum() + 1);
            if (type === -1) {
                pai1Str = pai.getType() + (pai.getNum() - 2);
                pai2Str = pai.getType() + (pai.getNum() - 1);
            } else if (type === 1) {
                pai1Str = pai.getType() + (pai.getNum() + 1);
                pai2Str = pai.getType() + (pai.getNum() + 2);
            }
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai1Str)] > 0 && hist[MahjongPai.strToNum(pai2Str)] > 0) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai1Str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai2Str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                naki.setNaki('-' + pai.str + pai1Str + pai2Str);
                this.naki.push(naki);
                this.refresh();
                return true;
            }
            return false;
        },
        
        // ポンしたときに呼ぶ関数。引数はポンした牌とポンした方向。public
        pon: function(pai, from) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] >= 2) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str;
                if (from === 3) {
                    nakiStr = '-' + nakiStr;
                } else if (from === 2) {
                    nakiStr = '-' + nakiStr + '-';
                } else if (from === 1) {
                    nakiStr = nakiStr + '-';
                }
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                this.refresh();
                return true;
            }
            return false;
        },
        
        // 明槓したときに呼ぶ関数。引数は明槓した牌と明槓した方向。public
        minkan: function(pai, from) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] >= 3) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                for (var i3 = 0; i3 < this.tehai.length; i3++) {
                    if (this.tehai[i3].str === pai.str) {
                        this.tehai.splice(i3, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str + pai.str;
                if (from === 3) {
                    nakiStr = '-' + nakiStr;
                } else if (from === 2) {
                    nakiStr = '-' + nakiStr + '-';
                } else if (from === 1) {
                    nakiStr = nakiStr + '-';
                }
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                return true;
            }
            return false;
        },
        
        // 暗槓したときに呼ぶ関数。引数は暗槓した牌。public
        ankan: function(pai) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] === 4) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                for (var i3 = 0; i3 < this.tehai.length; i3++) {
                    if (this.tehai[i3].str === pai.str) {
                        this.tehai.splice(i3, 1);
                        break;
                    }
                }
                for (var i4 = 0; i4 < this.tehai.length; i4++) {
                    if (this.tehai[i4].str === pai.str) {
                        this.tehai.splice(i4, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str + pai.str;
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                return true;
            }
            return false;
        },
        
        // 加槓したときに呼ぶ関数。引数は加槓した牌。public
        kakan: function(pai) {
            var nakiIndex = -1;
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                if (this.naki[nakiI].pai1.str === pai.str && this.naki[nakiI].isPon()) {
                    nakiIndex = nakiI;
                    break;
                }
            }
            var tehaiIndex = -1;
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                if (this.tehai[tehaiI].str === pai.str) {
                    tehaiIndex = tehaiI;
                    break;
                }
            }
            if (nakiIndex !== -1 && tehaiIndex !== -1) {
                this.tehai.splice(tehaiIndex, 1);
                this.naki[nakiIndex].kanFlag = 1;
                return true;
            }
            return false;
        },
        
        // 暗槓もしくは加槓できるかどうか返す関数。public
        getKanable: function() {
            var kanable = [];
            var hist = this.toHistogram();
            for (var ankanI = 0; ankanI < 34; ankanI++) {
                if (hist[ankanI] === 4) {
                    var ankanPai = MahjongPai.Pai();
                    ankanPai.setFrame(MahjongPai.numToStr(ankanI));
                    kanable.push(ankanPai);
                }
            }
            for (var kakanI = 0; kakanI < this.naki.length; kakanI++) {
                var naki = this.naki[kakanI];
                if (naki.isPon() && hist[MahjongPai.strToNum(naki.pai1.str)] === 1) {
                    var kakanPai = MahjongPai.Pai();
                    kakanPai.setFrame(naki.pai1.str);
                    kanable.push(kakanPai);
                }
            }
            return kanable;
        },
        
        // 牌を切る関数。引数は手牌のインデックス。public
        drop: function(index) {
            if (this.tehai.length % 3 !== 2) {
                return null;
            }
            if (index >= 0 && index < this.tehai.length) {
                var pai = this.tehai[index];
                this.tehai.splice(index, 1);
                
                this.sort();
                this.refresh();

                return pai;
            }
            return null;
        },
        
        // 手牌を読み込み可能な文字列に変換する関数。public
        toString: function(forceShow) {
            var retStr = "";
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                if (forceShow || this.mine === 1) {
                    retStr += this.tehai[tehaiI].str;
                }
            }
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                retStr += " ";
                retStr += this.naki[nakiI].toString();
            }
            
            return retStr;
        },
        
        // 手牌をヒストグラムに変換する関数。public
        toHistogram: function() {
            var hist = [];
            for (var initI = 0; initI < 34; initI++) {
                hist.push(0);
            }
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var str = this.tehai[tehaiI].str;
                hist[MahjongPai.strToNum(str)]++;
            }
            return hist;
        },
        
        // 鳴き牌を含め手牌をヒストグラムに変換する関数。public
        toHistogramAll: function() {
            var hist = [];
            for (var initI = 0; initI < 34; initI++) {
                hist.push(0);
            }
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var str = this.tehai[tehaiI].str;
                hist[MahjongPai.strToNum(str)]++;
            }
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                var naki = this.naki[nakiI];
                hist[MahjongPai.strToNum(naki.pai1.str)]++;
                hist[MahjongPai.strToNum(naki.pai2.str)]++;
                hist[MahjongPai.strToNum(naki.paiNaki.str)]++;
                if (naki.kanFlag > 0) {
                    hist[MahjongPai.strToNum(naki.paiNaki.str)]++;
                }
            }
            return hist;
        },
        
        // 理牌する関数。public
        sort: function() {
            this.tehai.sort(
                function(a, b) {
                    var aType = a.str.substr(0, 1); 
                    var aNum = parseInt(a.str.substr(1, 1), 10);
                    if (aType == 'm') {
                        aNum += 10;
                    } else if(aType === 's') {
                        aNum += 20;
                    } else if(aType === 'p') {
                        aNum += 30;
                    } else if(aType === 'z') {
                        aNum += 40;
                    }
                    var bType = b.str.substr(0, 1); 
                    var bNum = parseInt(b.str.substr(1, 1), 10);
                    if (bType == 'm') {
                        bNum += 10;
                    } else if(bType === 's') {
                        bNum += 20;
                    } else if(bType === 'p') {
                        bNum += 30;
                    } else if(bType === 'z') {
                        bNum += 40;
                    }
                    if (aNum < bNum) {
                        return -1;
                    } else if(aNum > bNum) {
                        return 1;
                    } else {
                        return 0;
                    }
                }
            );
            
            this.setIds();
        },
        
        // 手牌すべてにタッチしたときのリスナーを設定する関数。public
        setIds: function() {
            for (var i = 0; i < this.tehai.length; i++) {
                var pai = this.tehai[i];
                pai.setId(i);
            }
        },
        
        // 手牌の再描画フラグを立てる関数。
        refresh: function() {
            var e = new enchant.Event("refreshRequire");
            MahjongTehai.game_.dispatchEvent(e);
        },
        
        // 手牌を表示する関数。public
        show: function() {
            this.showCore(MahjongTehai.game_.rootScene, this.mine);
        },
        
        // 結果表示時に手牌を表示する関数。public
        showResult: function(scene, tenpai) {
            this.showCore(scene, tenpai);
        },
        
        // 手牌の表示用内部関数。
        showCore: function(scene, showFlag) {
            var beginPosX = 0.11 * MahjongTehai.game_.width;
            var beginPosY = 0.87 * MahjongTehai.game_.height;
            var beginPosNakiX = MahjongTehai.game_.width - MahjongPai.sizeX;
            var beginPosNakiY = 0.87 * MahjongTehai.game_.height;
            var directXX = 1;
            var directXY = 0;
            var directYX = 0;
            var directYY = 1;
            var rotate = 0;
            if (this.position === 1) {
                beginPosX = 0.89 * MahjongTehai.game_.width;
                beginPosY = 0.78 * MahjongTehai.game_.height;
                beginPosNakiX = 0.89 * MahjongTehai.game_.width;
                beginPosNakiY = 0;
                directXX = 0;
                directXY = -1;
                directYX = 1;
                directYY = 0;
                rotate = 270;
            } else if (this.position === 2) {
                beginPosX = 0.78 * MahjongTehai.game_.width;
                beginPosY = 0;
                beginPosNakiX = 0;
                beginPosNakiY = 0;
                directXX = -1;
                directXY = 0;
                directYX = 0;
                directYY = -1;
                rotate = 180;
            } else if (this.position === 3) {
                beginPosX = 0;
                beginPosY = 0.11 * MahjongTehai.game_.height;
                beginPosNakiX = 0;
                beginPosNakiY = MahjongTehai.game_.height - MahjongPai.sizeY;
                directXX = 0;
                directXY = 1;
                directYX = -1;
                directYY = 0;
                rotate = 90;
            }
            var posX = beginPosX;
            var posY = beginPosY;
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var paiTehai = this.tehai[tehaiI];
                paiTehai.x = posX;
                paiTehai.y = posY;
                if (this.position == 0 && tehaiI === this.selected) {
                    paiTehai.y -= MahjongPai.sizeY * 0.1;
                }
                paiTehai.rotation = rotate;
                if (!showFlag) {
                    paiTehai.setUra(true);
                }
                scene.addChild(paiTehai);
                posX += directXX * MahjongPai.sizeX;
                posY += directXY * MahjongPai.sizeX;
            }
            posX = beginPosNakiX;
            posY = beginPosNakiY;
            for (var nakiI = this.naki.length - 1; nakiI >= 0; nakiI--) {
                var huro = this.naki[nakiI];
                if (huro.kanFlag !== 2) {
                    if (huro.nakiFrom === 1) {
                        var paiNaki1 = huro.paiNaki;
                        paiNaki1.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki1.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki1.rotation = rotate - 90;
                        scene.addChild(paiNaki1);
                        if (huro.kanFlag === 1) {
                            var paiKan1 = MahjongPai.Pai();
                            paiKan1.setFrame(huro.paiNaki.str);
                            paiKan1.x = posX +
                                        directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                        directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan1.y = posY+
                                        directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                        directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan1.rotation = rotate - 90;
                            scene.addChild(paiKan1);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                        
                        var pai11 = huro.pai1;
                        pai11.x = posX;
                        pai11.y = posY;
                        pai11.rotation = rotate;
                        scene.addChild(pai11);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var pai21 = huro.pai2;
                        pai21.x = posX;
                        pai21.y = posY;
                        pai21.rotation = rotate;
                        scene.addChild(pai21);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
                    } else if (huro.nakiFrom === 2) {
                        var pai12 = huro.pai1;
                        pai12.x = posX;
                        pai12.y = posY;
                        pai12.rotation = rotate;
                        scene.addChild(pai12);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var paiNaki2 = huro.paiNaki;
                        paiNaki2.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki2.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki2.rotation = rotate - 90;
                        scene.addChild(paiNaki2);
                        if (huro.kanFlag === 1) {
                            var paiKan2 = MahjongPai.Pai();
                            paiKan2.setFrame(huro.paiNaki.str);
                            paiKan2.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan2.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan2.rotation = rotate - 90;
                            scene.addChild(paiKan2);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                        
                        var pai22 = huro.pai2;
                        pai22.x = posX;
                        pai22.y = posY;
                        pai22.rotation = rotate;
                        scene.addChild(pai22);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                    } else {
                        var pai13 = huro.pai1;
                        pai13.x = posX;
                        pai13.y = posY;
                        pai13.rotation = rotate;
                        scene.addChild(pai13);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var pai23 = huro.pai2;
                        pai23.x = posX;
                        pai23.y = posY;
                        pai23.rotation = rotate;
                        scene.addChild(pai23);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var paiNaki3 = huro.paiNaki;
                        paiNaki3.x = posX +
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki3.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki3.rotation = rotate - 90;
                        scene.addChild(paiNaki3);
                        if (huro.kanFlag === 1) {
                            var paiKan3 = MahjongPai.Pai();
                            paiKan3.setFrame(huro.paiNaki.str);
                            paiKan3.x = posX +
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan3.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan3.rotation = rotate - 90;
                            scene.addChild(paiKan3);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                    }
                } else {
                    var minimize = 0.75;
                    // 暗槓
                    var pai1an = MahjongPai.Pai();
                    pai1an.setFrame("u0");
                    pai1an.x = posX;
                    pai1an.y = posY;
                    pai1an.rotation = rotate;
                    pai1an.scaleX = MahjongPai.scale * minimize;
                    pai1an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai1an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai2an = MahjongPai.Pai();
                    pai2an.setFrame(huro.paiNaki.str);
                    pai2an.x = posX;
                    pai2an.y = posY;
                    pai2an.rotation = rotate;
                    pai2an.scaleX = MahjongPai.scale * minimize;
                    pai2an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai2an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai3an = MahjongPai.Pai();
                    pai3an.setFrame(huro.paiNaki.str);
                    pai3an.x = posX;
                    pai3an.y = posY;
                    pai3an.rotation = rotate;
                    pai3an.scaleX = MahjongPai.scale * minimize;
                    pai3an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai3an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai4an = MahjongPai.Pai();
                    pai4an.setFrame("u0");
                    pai4an.x = posX;
                    pai4an.y = posY;
                    pai4an.rotation = rotate;
                    pai4an.scaleX = MahjongPai.scale * minimize;
                    pai4an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai4an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                }
            }
        },
        
        // 手牌のシャンテン数を計算する関数。public
        calcShanten: function() {
            var c = this.calcChitoitsuShanten();
            var k = this.calcKokushiShanten();
            var b = this.calcBaseShanten();
            var min = 13;
            if (c < min) {
                min = c;
            }
            if (k < min) {
                min = k;
            }
            if (b < min) {
                min = b;
            }
            
            return min;
        },
        
        // 七対子まで何シャンテンか計算する関数。public
        calcChitoitsuShanten: function() {
            if (this.naki.length > 0) {
                return 13;
            }
            var hist = this.toHistogram();
            var toitsu = 0;
            var seed = 0;
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    seed++;
                }
                if (hist[i] >= 2) {
                    toitsu++;
                }
            }
            if (seed > 7) {
                seed = 7;
            }
            hist = null;
            return (13 - toitsu - seed);
        },
        
        // 国士無双まで何シャンテンか計算する関数。public
        calcKokushiShanten: function() {
            if (this.naki.length > 0) {
                return 13;
            }
            var hist = this.toHistogram();
            var yaochu = 0;
            var janto = 0;
            var yaochuIndex = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33];
            for (var i = 0; i < yaochuIndex.length; i++) {
                var num = hist[yaochuIndex[i]];
                if (num > 0) {
                    yaochu++;
                }
                if (janto === 0 && num >= 2) {
                    janto++;
                }
            }
            hist = null;
            yaochuIndex = null;
            return (13 - yaochu - janto);
        },
        
        
        // 4面子1雀頭１まで何シャンテンか計算する関数。public
        calcBaseShanten: function() {
            var hist = this.toHistogram();
            
            // 孤立牌除去
            for (var aloneI = 0; aloneI < hist.length; aloneI++) {
                if (hist[aloneI] == 1) {
                    if (aloneI >= 27) {
                            hist[aloneI] = 0;
                    } else {
                        var num = (aloneI % 9) + 1;
                        if (num === 1) {
                            if (hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 9) {
                            if (hist[aloneI - 2] + hist[aloneI - 1] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 2) {
                            if (hist[aloneI - 1] + hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 8) {
                            if (hist[aloneI - 2] + hist[aloneI - 1] + hist[aloneI + 1] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else {
                            if (hist[aloneI - 2] + hist[aloneI - 1] + hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        }
                    }
                }
            }
            
            var tatsuCalc = function (h, index) {
                while (h[index] === 0) {
                    index++;
                }
                if (index >= h.length) {
                    return 0;
                }
                // 対子
                if (h[index] >= 2) {
                    h[index] -= 2;
                    return (tatsuCalc(h, index) + 1);
                }
                
                // 字牌は順子の塔子は取れない
                if (index >= 27) {
                    return tatsuCalc(h, index + 1);
                }
                var num = (index % 9) + 1;
                // 辺張、両面
                if (num < 9) {
                    if (h[index + 1] > 0) {
                        h[index]--;
                        h[index + 1]--;
                        return (tatsuCalc(h, index) + 1);
                    }
                }
                
                // 嵌張
                if (num < 8) {
                    if (h[index + 2] > 0) {
                        h[index]--;
                        h[index + 2]--;
                        return (tatsuCalc(h, index) + 1);
                    }
                }
                return tatsuCalc(h, index + 1);
            };
            
            var mentsuCalc = function(h, index, mentsu) {
                while (h[index] === 0) {
                    index++;
                }
                if (index >= h.length) {
                    var tatsu = tatsuCalc(h, 0);
                    if (mentsu + tatsu > 4) {
                        tatsu = 4 - mentsu;
                    }
                    return (8 - mentsu * 2 - tatsu);
                }
                if (index >= 27) {
                    // 字牌は刻子のみ
                    if(h[index] >= 3) {
                        h[index] -= 3;
                        return mentsuCalc(h, index + 1, mentsu + 1);
                    }
                } else {
                    // 数牌は順子と刻子を考慮
                    var num = (index % 9) + 1;
                    var skipClone = h.concat();
                    var shanten = mentsuCalc(skipClone, index + 1, mentsu);
                    skipClone = null;
                    if (num < 8 && h[index + 1] > 0 && h[index + 2] > 0) {
                        // 順子が取れる場合
                        if (h[index] >= 3) {
                            // 順子も刻子もとれる場合
                            var shuntsuClone = h.concat();
                            shuntsuClone[index]--;
                            shuntsuClone[index + 1]--;
                            shuntsuClone[index + 2]--;
                            var shuntsuShanten2 = mentsuCalc(shuntsuClone, index, mentsu + 1);
                            var kotsuClone = h.concat();
                            kotsuClone[index] -= 3;
                            var kotsuShanten2 = mentsuCalc(kotsuClone, index, mentsu + 1);
                            if (shanten === undefined || shuntsuShanten2 < shanten) {
                                shanten = shuntsuShanten2;
                            }
                            if (shanten === undefined || kotsuShanten2 < shanten) {
                                shanten = kotsuShanten2;
                            }
                            shuntsuClone = null;
                            kotsuClone = null;
                        } else {
                            // 順子のみ取れる場合
                            h[index]--;
                            h[index + 1]--;
                            h[index + 2]--;
                            var shuntsuShanten1 = mentsuCalc(h, index, mentsu + 1);
                            if (shanten === undefined || shuntsuShanten1 < shanten) {
                                shanten = shuntsuShanten1;
                            }
                        }
                    } else {
                        if (h[index] >= 3) {
                            // 刻子のみ取れる場合
                            h[index] -= 3;
                            var kotsuShanten1 = mentsuCalc(h, index, mentsu + 1);
                            if (shanten === undefined || kotsuShanten1 < shanten) {
                                shanten = kotsuShanten1;
                            }
                        }
                    }
                    return shanten;
                }
                return mentsuCalc(h, index + 1, mentsu);
            };
            
            var cloneHist = hist.concat();
            var min = mentsuCalc(cloneHist, 0, this.naki.length);
            for (var histI = 0; histI < 34; histI++) {
                if (hist[histI] >= 2) {
                    cloneHist = hist.concat();
                    cloneHist[histI] -= 2;
                    var shanten = mentsuCalc(cloneHist, 0, this.naki.length) - 1;
                    if (min > shanten) {
                        min = shanten;
                    }
                }
            }
            cloneHist = null;
            hist = null;
            tatsuCalc = null;
            mentsuCalc = null;
            return min;
        },
        
        // 聴牌時の待ち牌を計算する関数。public
        getMachi: function() {
            if (this.calcShanten() === 0) {
                return this.getYuko();
            }
            return null;
        },
        
        // 有効牌を返す関数。public
        getYuko: function() {
            if (this.isTsumoban()) {
                var yukohais = [];
                var nowShanten = this.calcShanten();
                for (var i = 0; i < 34; i++) {
                    var pai = MahjongPai.Pai();
                    pai.setFrame(MahjongPai.numToStr(i));
                    var cloneTehai = this.clone();
                    cloneTehai.add(pai);
                    if (cloneTehai.calcShanten() === nowShanten - 1) {
                        yukohais.push(pai);
                    }
                    cloneTehai = null;
                    pai = null;
                }
                return yukohais;
            }
            return null;
        },
        
        // ツモ番か判定する関数。public
        isTsumoban: function() {
            return (this.tehai.length % 3 === 1);
        },
        
        // 切り番か判定する関数。public
        isKiriban: function() {
            return (this.tehai.length % 3 === 2);
        },
        
        // 少牌か判定する関数。public
        isShoupai: function() {
            return (this.tehai.length % 3 === 0);
        },
        
        //ツモフラグを立てる関数。public
        setTsumo: function(flag) {
            this.tsumoFlag = flag;
        },
        
        //ツモフラのゲッター。public
        isTsumo: function() {
            return this.tsumoFlag;
        },
        
        // 槍槓フラグを立てる関数。public
        setChankan: function(flag) {
            this.chankanFlag = flag;
        },
        
        // 槍槓フラグのゲッター。public
        isChankan: function() {
            return this.chankanFlag;
        },
        
        // 天和フラグを立てる関数。public
        setTenho: function(flag) {
            this.tenhoFlag = flag;
        },
        
        // 天和フラグのゲッター。public
        isTenho: function() {
            return this.tenhoFlag;
        },
        
        // 地和フラグを立てる関数。public
        setChiho: function(flag) {
            this.chihoFlag = flag;
        },
        
        // 地和フラグのゲッター。public
        isChiho: function() {
            return this.chihoFlag;
        },
        
        // 立直フラグを立てる関数。public
        setReach: function(flag) {
            this.reachFlag = flag;
        },
        
        // 立直フラグのゲッター。public
        isReach: function() {
            return this.reachFlag;
        },
        
        // ダブル立直フラグを立てる関数。public
        setDoubleReach: function(flag) {
            this.doubleReachFlag = flag;
            if (flag) {
                this.reachFlag = true;
            }
        },
        
        // ダブル立直フラグのゲッター。public
        isDoubleReach: function() {
            return this.doubleReachFlag;
        },
        
        // 一発フラグを立てる関数。public
        setIppatsu: function(flag) {
            this.ippatsuFlag = flag;
        },
        
        // 一発フラグのゲッター。public
        isIppatsu: function() {
            return this.ippatsuFlag;
        },
        
        // 嶺上フラグを立てる関数。public
        setRinshan: function(flag) {
            this.rinshanFlag = flag;
        },
        
        // 嶺上フラグのゲッター。public
        isRinshan: function() {
            return this.rinshanFlag;
        },
        
        // 海底フラグを立てる関数。public
        setHaitei: function(flag) {
            this.haiteiFlag = flag;
        },
        
        // 海底フラグのゲッター。public
        isHaitei: function() {
            return this.haiteiFlag;
        },
        
        // ドラを設定する関数。public
        setDoras: function(doras) {
            this.doras = doras;
        },
        
        // ドラのゲッター。public
        getDoras: function() {
            return this.doras;
        },
        
        // 点数を計算する関数。public
        calcPoint: function(ba, kaze) {
            this.sort();
            if (this.calcShanten() === -1) {
                if (this.calcChitoitsuShanten() === -1 && !this.isRyanpeikou()) {
                    var splitMentsu = MahjongTehai.MentsuSeparatedTehai();
                    splitMentsu.setTehai(this);
                    var fan = splitMentsu.calcFan(ba, kaze);
                    return MahjongTehai.calcPointFromHuAndFan(25, [2 + fan[0], '七対子,' + fan[1]], this.isTsumo(), kaze === 'z1');
                } else if (this.calcKokushiShanten() === -1) {
                    return MahjongTehai.calcPointFromHuAndFan(20, [13, '国士無双'], this.isTsumo(), kaze === 'z1');
                } else {
                    var maxPoint = [0, 0, 'チョンボ', ''];
                    var splitMentsuList = this.splitMentsu();
                    for (var i = 0; i < splitMentsuList.length; i++) {
                        var point = splitMentsuList[i].calcPoint(ba, kaze, this.isTsumo(), kaze === 'z1');
                        if (maxPoint[1] < point[1]) {
                            maxPoint = point;
                        }
                    }
                    return maxPoint;
                }
            }
            return [0, 0, 'チョンボ', ''];
        },
        
        // 手牌を面子ごとに分ける関数。
        splitMentsu: function() {
            var list = [];
            var hist = this.toHistogram();
            var splitTehai = MahjongTehai.MentsuSeparatedTehai();
            splitTehai.setTehai(this);
            var cloneHist = null;
            
            var removeMentsu = function(l, h, s) {
                var restFind = false;
                for (var i = 0; i < 34; i++) {
                    var removed = false;
                    if (h[i] > 0) {
                        restFind = true;
                        var num = (i % 9) + 1;
                        if (i < 27) {
                            // 数牌の場合順子が取れる
                            if (num <= 7) {
                                if (h[i] > 0 && h[i + 1] > 0 && h[i + 2] > 0) {
                                    var shuntsuHist = h.concat();
                                    var shuntsuSplitTehai = s.clone();
                                    shuntsuHist[i]--;
                                    shuntsuHist[i + 1]--;
                                    shuntsuHist[i + 2]--;
                                    var shuntsu = MahjongTehai.Naki();
                                    shuntsu.setMentsu(MahjongPai.numToStr(i) + MahjongPai.numToStr(i + 1) + MahjongPai.numToStr(i + 2));
                                    shuntsuSplitTehai.addMentsu(shuntsu);
                                    removeMentsu(l, shuntsuHist, shuntsuSplitTehai);
                                    
                                    shuntsuHist = null;
                                    shuntsuSplitTehai = null;
                                    shuntsu = null;
                                    
                                    removed = true;
                                }
                            }
                        }
                        if (h[i] >= 3) {
                            var kotsuHist = h.concat();
                            var kotsuSplitTehai = s.clone();
                            kotsuHist[i] -= 3;
                            var kotsu = MahjongTehai.Naki();
                            kotsu.setMentsu(MahjongPai.numToStr(i) + MahjongPai.numToStr(i) + MahjongPai.numToStr(i));
                            kotsuSplitTehai.addMentsu(kotsu);
                            removeMentsu(l, kotsuHist, kotsuSplitTehai);
                            
                            kotsuHist = null;
                            kotsuSplitTehai = null;
                            kotsu = null;
                            
                            removed = true;
                        }
                    }
                    if (removed) {
                        break;
                    }
                }
                if (!restFind) {
                    l.push(s);
                }
            };
            
            var machiSet = function(list, finishPai) {
                var machiList = [];
                for (var i = 0; i < list.length; i++) {
                    var s = list[i];
                    for (var ryanmenJ = 0; ryanmenJ < s.mentsu.length; ryanmenJ++) {
                        var mentsuRyanmen = s.getMentsu(ryanmenJ);
                        if (mentsuRyanmen.kanFlag === -1 && mentsuRyanmen.isShuntsu()) {
                            if (mentsuRyanmen.paiNaki.str === finishPai.str && finishPai.getNum() !== 7) {
                                var sRyanmen7 = s.clone();
                                sRyanmen7.setFinishShape(0);
                                machiList.push(sRyanmen7);
                                break;
                            } else if (mentsuRyanmen.pai2.str === finishPai.str && finishPai.getNum() !== 3) {
                                var sRyanmen3 = s.clone();
                                sRyanmen3.setFinishShape(0);
                                machiList.push(sRyanmen3);
                                break;
                            }
                        }
                    }
                    for (var shaboJ = 0; shaboJ < s.mentsu.length; shaboJ++) {
                        var mentsuShabo = s.getMentsu(shaboJ);
                        if (mentsuShabo.kanFlag === -1 && mentsuShabo.isKotsu()) {
                            if (mentsuShabo.paiNaki.str === finishPai.str) {
                                var sShabo = s.clone();
                                sShabo.setFinishShape(1);
                                machiList.push(sShabo);
                                break;
                            }
                        }
                    }
                    for (var kanchanJ = 0; kanchanJ < s.mentsu.length; kanchanJ++) {
                        var mentsuKanchan = s.getMentsu(kanchanJ);
                        if (mentsuKanchan.kanFlag === -1 && mentsuKanchan.isShuntsu()) {
                            if (mentsuKanchan.pai1.str === finishPai.str) {
                                var sKanchan = s.clone();
                                sKanchan.setFinishShape(2);
                                machiList.push(sKanchan);
                                break;
                            }
                        }
                    }
                    for (var penchanJ = 0; penchanJ < s.mentsu.length; penchanJ++) {
                        var mentsuPenchan = s.getMentsu(penchanJ);
                        if (mentsuPenchan.kanFlag === -1 && mentsuPenchan.isShuntsu()) {
                            if (mentsuPenchan.paiNaki.str === finishPai.str && finishPai.getNum() === 7) {
                                var sPenchan7 = s.clone();
                                sPenchan7.setFinishShape(3);
                                machiList.push(sPenchan7);
                                break;
                            } else if (mentsuPenchan.pai2.str === finishPai.str && finishPai.getNum() === 3) {
                                var sPenchan3 = s.clone();
                                sPenchan3.setFinishShape(3);
                                machiList.push(sPenchan3);
                                break;
                            }
                        }
                    }
                    if (s.janto.str === finishPai.str) {
                        var sTanki = s.clone();
                        sTanki.setFinishShape(4);
                        machiList.push(sTanki);
                    }
                }
                return machiList;
            };
            
            for (var i = 0; i < 34; i++) {
                if (hist[i] >= 2) {
                    cloneHist = hist.concat();
                    cloneHist[i] -= 2;
                    splitTehai.setJanto(MahjongPai.numToStr(i));
                    removeMentsu(list, cloneHist, splitTehai);
                }
            }
            list = machiSet(list, this.lastAddPai);
            
            hist = null;
            cloneHist = null;
            return list;
        },
        
        // 二盃口かどうか判定する関数。public
        isRyanpeikou: function() {
            // 二盃口だけは七対子と重なるので特別に判定
            if (this.calcChitoitsuShanten() === -1 || (this.calcBaseShanten() === -1)) {
                var hist = this.toHistogram();
                var peikou = 0;
                for (var manzuI = 0; manzuI < 7; manzuI++) {
                    if (hist[manzuI] >= 2 && hist[manzuI + 1] >= 2 && hist[manzuI + 2] >= 2) {
                        hist[manzuI] -= 2;
                        hist[manzuI + 1] -= 2;
                        hist[manzuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[manzuI] >= 2 && hist[manzuI + 1] >= 2 && hist[manzuI + 2] >= 2) {
                        hist[manzuI] -= 2;
                        hist[manzuI + 1] -= 2;
                        hist[manzuI + 2] -= 2;
                        peikou++;
                    }
                }
                for (var sozuI = 9; sozuI < 16; sozuI++) {
                    if (hist[sozuI] >= 2 && hist[sozuI + 1] >= 2 && hist[sozuI + 2] >= 2) {
                        hist[sozuI] -= 2;
                        hist[sozuI + 1] -= 2;
                        hist[sozuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[sozuI] >= 2 && hist[sozuI + 1] >= 2 && hist[sozuI + 2] >= 2) {
                        hist[sozuI] -= 2;
                        hist[sozuI + 1] -= 2;
                        hist[sozuI + 2] -= 2;
                        peikou++;
                    }
                }
                for (var pinzuI = 18; pinzuI < 15; pinzuI++) {
                    if (hist[pinzuI] >= 2 && hist[pinzuI + 1] >= 2 && hist[pinzuI + 2] >= 2) {
                        hist[pinzuI] -= 2;
                        hist[pinzuI + 1] -= 2;
                        hist[pinzuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[pinzuI] >= 2 && hist[pinzuI + 1] >= 2 && hist[pinzuI + 2] >= 2) {
                        hist[pinzuI] -= 2;
                        hist[pinzuI + 1] -= 2;
                        hist[pinzuI + 2] -= 2;
                        peikou++;
                    }
                }
                hist = null;
                if (peikou >= 2) {
                    return true;
                }
            }
            return false;
        }
    });
    
    // 役のクラス
    MahjongTehai.Rule = {};
    
    // 既定の役
    MahjongTehai.Rule.rules = [
        // 翻数の多い順に判定
        // 役満
        // 天和
        function(tehai, ba, kaze) {
            if (tehai.tehai.isTenho()) {
                return [13, '天和'];
            }
            return [0, ''];
        },
        // 地和
        function(tehai, ba, kaze) {
            if (tehai.tehai.isChiho()) {
                return [13, '地和'];
            }
            return [0, ''];
        },
        // 四暗刻
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countAnko() == 4) {
                    if (tehai.finishShape === 1 && tehai.tehai.isTsumo()) {
                        return [13, '四暗刻'];
                    } else if (tehai.finishShape === 4) {
                        return [26, '四暗刻単騎'];
                    }
                }
            }
            return [0, ''];
        },
        // 大三元
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var sangenCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z5') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z6') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z7') {
                        sangenCount++;
                    }
                    mentsu = null;
                }
                if (sangenCount == 3) {
                    return [13, '大三元'];
                }
            }
            return [0, ''];
        },
        // 字一色
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < hist.length; i++) {
                if (i < 27 && hist[i] > 0) {
                    return [0, ''];
                }
            }
            return [13, '字一色'];
        },
        // 小四喜
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kazeCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z1') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z2') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z3') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z4') {
                        kazeCount++;
                    }
                    mentsu = null;
                }
                if (kazeCount == 3 && (tehai.janto.str === 'z1' || tehai.janto.str === 'z2' || tehai.janto.str === 'z3' || tehai.janto.str === 'z4')) {
                    return [13, '小四喜'];
                }
            }
            return [0, ''];
        },
        // 大四喜
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kazeCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z1') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z2') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z3') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z4') {
                        kazeCount++;
                    }
                    mentsu = null;
                }
                if (kazeCount == 4) {
                    return [26, '大四喜'];
                }
            }
            return [0, ''];
        },
        // 緑一色
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < hist.length; i++) {
                if (hist[i] > 0) {
                    if (!(i === 10 || i === 11 || i === 12 || i === 14 || i === 16 || i === 32)) {
                        return [0, ''];
                    }
                }
            }
            return [13, '緑一色'];
        },
        // 清老頭
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var onlyIku = true;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.isShuntsu()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    if (!mentsu.isIku()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                if (jantoType === 'z') {
                    return [0, ''];
                }
                if (jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                return [13, '清老頭'];
            }
            return [0, ''];
        },
        // 四槓子
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKan() === 4) {
                    return [13, '四槓子'];
                }
            }
            return [0, ''];
        },
        // 九蓮宝燈
        function(tehai, ba, kaze) {
            if (tehai.isMenzen()) {
                var hist = tehai.tehai.toHistogramAll();
                for (var i = 0; i < 3; i++) {
                    if (hist[i * 9] >= 3 &&
                        hist[i * 9 + 1] >= 1 &&
                        hist[i * 9 + 2] >= 1 &&
                        hist[i * 9 + 3] >= 1 &&
                        hist[i * 9 + 4] >= 1 &&
                        hist[i * 9 + 5] >= 1 &&
                        hist[i * 9 + 6] >= 1 &&
                        hist[i * 9 + 7] >= 1 &&
                        hist[i * 9 + 8] >= 3) {
                        return [13, '九蓮宝燈'];
                    }
                }
            }
            return [0, ''];
        },
        
        // 六飜
        // 清一色
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            var mHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var sHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var pHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var zHist = [0, 0, 0, 0, 0, 0, 0];
            for (var histSplitI = 0; histSplitI < 34; histSplitI++) {
                if (histSplitI < 9) {
                    mHist[histSplitI] = hist[histSplitI];
                } else if (histSplitI < 18) {
                    sHist[histSplitI - 9] = hist[histSplitI];
                } else if (histSplitI < 27) {
                    pHist[histSplitI - 18] = hist[histSplitI];
                } else if (histSplitI < 34) {
                    zHist[histSplitI - 27] = hist[histSplitI];
                }
            }
            var suColors = 0;
            for (var manzuI = 0; manzuI < 9; manzuI++) {
                if(mHist[manzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var sozuI = 0; sozuI < 9; sozuI++) {
                if(sHist[sozuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var pinzuI = 0; pinzuI < 9; pinzuI++) {
                if(pHist[pinzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            var hasTsu = false;
            for (var tsuI = 0; tsuI < 7; tsuI++) {
                if(zHist[tsuI] > 0) {
                    hasTsu = true;
                    break;
                }
            }
            if (suColors === 1 && !hasTsu) {
                if (tehai.isMenzen()) {
                    return [6, '清一色'];
                } else {
                    return [5, '清一色'];
                }
            }
            return [0, ''];
        },
        
        // 三飜
        // 混一色
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            var mHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var sHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var pHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var zHist = [0, 0, 0, 0, 0, 0, 0];
            for (var histSplitI = 0; histSplitI < 34; histSplitI++) {
                if (histSplitI < 9) {
                    mHist[histSplitI] = hist[histSplitI];
                } else if (histSplitI < 18) {
                    sHist[histSplitI - 9] = hist[histSplitI];
                } else if (histSplitI < 27) {
                    pHist[histSplitI - 18] = hist[histSplitI];
                } else if (histSplitI < 34) {
                    zHist[histSplitI - 27] = hist[histSplitI];
                }
            }
            var suColors = 0;
            for (var manzuI = 0; manzuI < 9; manzuI++) {
                if(mHist[manzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var sozuI = 0; sozuI < 9; sozuI++) {
                if(sHist[sozuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var pinzuI = 0; pinzuI < 9; pinzuI++) {
                if(pHist[pinzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            var hasTsu = false;
            for (var tsuI = 0; tsuI < 7; tsuI++) {
                if(zHist[tsuI] > 0) {
                    hasTsu = true;
                    break;
                }
            }
            if (suColors === 1 && hasTsu) {
                if (tehai.isMenzen()) {
                    return [3, '混一色'];
                } else {
                    return [2, '混一色'];
                }
            }
            return [0, ''];
        },
        // 純全帯?九
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (!mentsu.isIku()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                if (jantoType === 'z') {
                    return [0, ''];
                }
                if (jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                if (tehai.isMenzen()) {
                    return [3, '純全帯?九'];
                } else {
                    return [2, '純全帯?九'];
                }
            }
            return [0, ''];
        },
        // 二盃口
        function(tehai, ba, kaze) {
            if(tehai.tehai.isRyanpeikou()){
                return [3, '二盃口'];
            }
            return [0, ''];
        },
        
        // 二飜
        // 三色同順
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 9; countI++) {
                    if (shuntsuMinPaiHist[countI] > 0 &&
                        shuntsuMinPaiHist[countI + 9] > 0 &&
                        shuntsuMinPaiHist[countI + 18] > 0) {
                        if (tehai.isMenzen()) {
                            return [2, '三色同順'];
                        } else {
                            return [1, '三色同順'];
                        }
                    }
                }
            }
            return [0, ''];
        },
        // 一気通貫
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 3; countI++) {
                    if (shuntsuMinPaiHist[countI * 9] > 0 &&
                        shuntsuMinPaiHist[countI * 9 + 3] > 0 &&
                        shuntsuMinPaiHist[countI * 9 + 6] > 0) {
                        if (tehai.isMenzen()) {
                            return [2, '一気通貫'];
                        } else {
                            return [1, '一気通貫'];
                        }
                    }
                }
            }
            return [0, ''];
        },
        // 混全帯?九
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var hasTsu = false;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (!mentsu.isYaochu()) {
                        mentsu = null;
                        return [0, ''];
                    } else if (mentsu.isTsu()) {
                        hasTsu = true;
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                
                if (jantoType !== 'z' && jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                if (tehai.countKotsu() === 4) {
                    return [0, ''];
                }
                
                
                if (hasTsu || jantoType === 'z') {
                    if (tehai.isMenzen()) {
                        return [2, '混全帯?九'];
                    } else {
                        return [1, '混全帯?九'];
                    }
                }
            }
            return [0, ''];
        },
        // 対々和
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKotsu() === 4) {
                    return [2, '対々和'];
                }
            }
            return [0, ''];
        },
        // 三暗刻
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countAnko() == 3) {
                    if (tehai.finishShape === 1) {
                        if (tehai.tehai.isTsumo()) {
                            return [2, '三暗刻'];
                        }
                    } else {
                        return [2, '三暗刻'];
                    }
                }
            }
            return [0, ''];
        },
        // 混老頭
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    if (i > 0 && i < 8) {
                        return [0, ''];
                    }
                    if (i > 9 && i < 17) {
                        return [0, ''];
                    }
                    if (i > 18 && i < 26) {
                        return [0, ''];
                    }
                }
            }
            return [2, '混老頭'];
        },
        // 三色同刻
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kotsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    kotsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isKotsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        
                        kotsuMinPaiHist[pai1Num]++;
                    }
                }
                for (var countI = 0; countI < 9; countI++) {
                    if (kotsuMinPaiHist[countI] > 0 &&
                        kotsuMinPaiHist[countI + 9] > 0 &&
                        kotsuMinPaiHist[countI + 18] > 0) {
                        return [2, '三色同刻'];
                    }
                }
            }
            return [0, ''];
        },
        // 三槓子
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKan() === 3) {
                    return [2, '三槓子'];
                }
            }
            return [0, ''];
        },
        // 小三元
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var sangenCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z5') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z6') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z7') {
                        sangenCount++;
                    }
                    mentsu = null;
                }
                if (sangenCount == 2 && MahjongPai.strToNum(tehai.janto.str) >= 31) {
                    return [2, '小三元'];
                }
            }
            return [0, ''];
        },
        // ダブル立直
        function(tehai, ba, kaze) {
            if (tehai.tehai.isDoubleReach()) {
                return [2, 'ダブル立直'];
            }
            return [0, ''];
        },
        
        // 一飜
        // 立直
        function(tehai, ba, kaze) {
            if (tehai.tehai.isReach() && !tehai.tehai.isDoubleReach()) {
                return [1, '立直'];
            }
            return [0, ''];
        },
        // 一発
        function(tehai, ba, kaze) {
            if (tehai.tehai.isIppatsu()) {
                return [1, '一発'];
            }
            return [0, ''];
        },
        // 門前清自摸和
        function(tehai, ba, kaze) {
            if (tehai.isMenzen() && tehai.tehai.isTsumo()) {
                return [1, '門前清自摸和'];
            }
            return [0, ''];
        },
        // 断?九
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    if (i === 0 || i === 8) {
                        return [0, ''];
                    }
                    if (i === 9 || i === 17) {
                        return [0, ''];
                    }
                    if (i === 18 || i === 26) {
                        return [0, ''];
                    }
                    if (i >= 27) {
                        return [0, ''];
                    }
                }
            }
            return [1, '断?九'];
        },
        // 平和
        function(tehai, ba, kaze) {
            if (!tehai.is4Mentsu()) {
                return [0, ''];
            }
            for (var i = 0; i < 4; i++) {
                var mentsu = tehai.getMentsu(i);
                if (!mentsu.isShuntsu()) {
                    return [0, ''];
                }
                mentsu = null;
            }
            var jantoType = tehai.janto.str.substr(0, 1);
            var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
            if (jantoType === 'z') {
                if (jantoNum >= 5) {
                    return [0, ''];
                } else {
                    if (tehai.janto.str === ba || tehai.janto.str === kaze) {
                        return [0, ''];
                    }
                }
            }
            if (tehai.finishShape !== 0) {
                return [0, ''];
            }
            return [1, '平和'];
        },
        // 一盃口
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu() && !tehai.tehai.isRyanpeikou()) {
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 34; countI++) {
                    if (shuntsuMinPaiHist[countI] >= 2) {
                        if (tehai.isMenzen()) {
                            return [1, '一盃口'];
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 圏風牌
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === ba) {
                            return [1, '場風'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 門風牌
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === kaze) {
                            return [1, '自風'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 白
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z5') {
                            return [1, '白'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 發
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z6') {
                            return [1, '發'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 中
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z7') {
                            return [1, '中'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // 嶺上開花
        function(tehai, ba, kaze) {
            if (tehai.tehai.isRinshan() && tehai.tehai.isTsumo()) {
                return [1, '嶺上開花'];
            }
            return [0, ''];
        },
        // 槍槓
        function(tehai, ba, kaze) {
            if (tehai.tehai.isChankan()) {
                return [1, '槍槓'];
            }
            return [0, ''];
        },
        // 海底摸月
        function(tehai, ba, kaze) {
            if (tehai.tehai.isHaitei() && tehai.tehai.isTsumo()) {
                return [1, '海底摸月'];
            }
            return [0, ''];
        },
        // 河底撈魚
        function(tehai, ba, kaze) {
            if (tehai.tehai.isHaitei() && !tehai.tehai.isTsumo()) {
                return [1, '河底撈魚'];
            }
            return [0, ''];
        },
    ];
    
    MahjongTehai.Rule.ruleSize = function() {
        return MahjongTehai.Rule.rules.length;
    };
    
    // 役のゲッター 。public
    MahjongTehai.Rule.getRule = function(index) {
        if (index < 0 || index >= MahjongTehai.Rule.rules.length) {
            var voidFunc = function(tehai) {
                return [0, ''];
            };
            return voidFunc;
        }
        return MahjongTehai.Rule.rules[index];
    };
    
    // 独自役を追加する際に使う関数。public
    MahjongTehai.Rule.addRule = function(rule) {
        MahjongTehai.Rule.rules.push(rule);
    };
    
    // 得点計算をするサブ関数。
    MahjongTehai.calcPointFromHuAndFan = function(hu, fan, tsumoFlag, oyaFlag) {
        var huFanStr = hu + '符' + fan[0] + '飜';
        if (fan[0] === 0) {
            return [0, 0, '役無し', ''];
        }
        var basePoint = hu * 2 * 2;
        for (var i = 0; i < fan[0]; i++) {
            basePoint *= 2;
        }
        if (basePoint >= 2000) {
            if (fan[0] >= 13) {
                var yakumanDoubled = parseInt(fan[0] / 13);
                basePoint = 8000 * yakumanDoubled;
                if (yakumanDoubled == 1) {
                    huFanStr = '役満';
                } else if (yakumanDoubled == 2) {
                    huFanStr = 'ダブル役満';
                } else if (yakumanDoubled == 3) {
                    huFanStr = 'トリプル役満';
                } else {
                    huFanStr = yakumanDoubled + '倍役満';
                }
            } else if (fan[0] >= 11) {
                basePoint = 6000;
                huFanStr += '三倍満';
            } else if (fan[0] >= 8) {
                basePoint = 4000;
                huFanStr += '倍満';
            } else if (fan[0] >= 6) {
                basePoint = 3000;
                huFanStr += '跳満';
            } else {
                basePoint = 2000;
                huFanStr += '満貫';
            }
        }
        if (tsumoFlag) {
            var oyaPoint = basePoint * 2;
            if (oyaPoint % 100 > 0) {
                oyaPoint = oyaPoint + 100 - (oyaPoint % 100);
            }
            var koPoint = basePoint;
            if (koPoint % 100 > 0) {
                koPoint = koPoint + 100 - (koPoint % 100);
            }
            if (oyaFlag) {
                return [oyaPoint, oyaPoint, fan[1], huFanStr];
            }
            return [koPoint, oyaPoint, fan[1], huFanStr];
        } else {
            var ronPoint = basePoint;
            if (oyaFlag) {
                ronPoint *= 6;
            } else {
                ronPoint *= 4;
            }
            if (ronPoint % 100 > 0) {
                ronPoint = ronPoint + 100 - (ronPoint % 100);
            }
            return [0, ronPoint, fan[1], huFanStr];
        }
    };
    
    return MahjongTehai;
});