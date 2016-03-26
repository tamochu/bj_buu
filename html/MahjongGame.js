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
		MahjongGame = definition();
	}

})(function(){// 実際の定義を行う関数
	'use strict';

	var MahjongGame = {};
	
	MahjongGame.sizeX = 550;
	MahjongGame.sizeY = 550;
	MahjongGame.game_ = null;
	MahjongGame.setGame = function(game) {
		MahjongGame.game_ = game;
		MahjongGame.game_._touchEventTarget = [];
	};
	MahjongGame.refreshWait = false;
	MahjongGame.labelX = MahjongGame.sizeX * 0.47;
	MahjongGame.labelY = MahjongGame.sizeY * 0.45;
	MahjongGame.labelWidth = MahjongGame.sizeX * 0.07;
	MahjongGame.labelHeight = MahjongGame.sizeY * 0.03;
	
	MahjongGame.buttonLabelWidth = MahjongGame.sizeX * 0.05;
	MahjongGame.buttonLabelHeight = MahjongGame.sizeY * 0.03;
	
	MahjongGame.buttonHoraLabelX = MahjongGame.sizeX * 0.7;
	MahjongGame.buttonHoraLabelY = MahjongGame.sizeY * 0.75;
	
	MahjongGame.buttonCancelLabelX = MahjongGame.sizeX * 0.77;
	MahjongGame.buttonCancelLabelY = MahjongGame.sizeY * 0.75;
	
	MahjongGame.buttonHuroLabelX = MahjongGame.sizeX * 0.7;
	MahjongGame.buttonHuroLabelY = MahjongGame.sizeY * 0.8;
	
	MahjongGame.buttonReachLabelX = MahjongGame.sizeX * 0.77;
	MahjongGame.buttonReachLabelY = MahjongGame.sizeY * 0.8;
	
	MahjongGame.buttonNoHuroLabelX = MahjongGame.sizeX * 0.7;
	MahjongGame.buttonNoHuroLabelY = MahjongGame.sizeY * 0.85;
	
	MahjongGame.buttonKanLabelX = MahjongGame.sizeX * 0.77;
	MahjongGame.buttonKanLabelY = MahjongGame.sizeY * 0.85;
	
	MahjongGame.nakiSelectX = MahjongGame.sizeX * 0.6;
	MahjongGame.nakiSelectY = MahjongGame.sizeY * 0.78;
	
	// 麻雀ゲームのクラス本体
	MahjongGame.Game = Class.create({
		initialize: function() {
			this.autoPlayMode = 1;// 0:対戦モード 1:プレイヤー一人 2:観戦モード
			this.infoLabel = new Label();
			this.infoLabel.x = MahjongGame.labelX;
			this.infoLabel.y = MahjongGame.labelY;
			this.infoLabel.width = MahjongGame.labelWidth;
			this.infoLabel.height = MahjongGame.labelHeight;
			this.infoLabel.backgroundColor = 'white';
			this.directLabels = [];
			this.md5 = '';
			this.tempClear();
			
			this.buttonHora = new Label('和了');
			this.buttonHora.x = MahjongGame.buttonHoraLabelX;
			this.buttonHora.y = MahjongGame.buttonHoraLabelY;
			this.buttonHora.width = MahjongGame.buttonLabelWidth;
			this.buttonHora.height = MahjongGame.buttonLabelHeight;
			this.buttonHora.backgroundColor = 'yellow';
			this.buttonHora.ontouchstart = function() {
				var e = new enchant.Event('hora');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonHora.visible = false;
			this.buttonHuro = new Label('副露');
			this.buttonHuro.x = MahjongGame.buttonHuroLabelX;
			this.buttonHuro.y = MahjongGame.buttonHuroLabelY;
			this.buttonHuro.width = MahjongGame.buttonLabelWidth;
			this.buttonHuro.height = MahjongGame.buttonLabelHeight;
			this.buttonHuro.backgroundColor = 'yellow';
			this.buttonHuro.ontouchstart = function() {
				var e = new enchant.Event('huro');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonHuro.visible = false;
			this.buttonCancel = new Label('パス');
			this.buttonCancel.x = MahjongGame.buttonCancelLabelX;
			this.buttonCancel.y = MahjongGame.buttonCancelLabelY;
			this.buttonCancel.width = MahjongGame.buttonLabelWidth;
			this.buttonCancel.height = MahjongGame.buttonLabelHeight;
			this.buttonCancel.backgroundColor = 'yellow';
			this.buttonCancel.ontouchstart = function() {
				var e = new enchant.Event('cancel');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonCancel.visible = false;
			this.buttonReach = new Label('立直');
			this.buttonReach.x = MahjongGame.buttonReachLabelX;
			this.buttonReach.y = MahjongGame.buttonReachLabelY;
			this.buttonReach.width = MahjongGame.buttonLabelWidth;
			this.buttonReach.height = MahjongGame.buttonLabelHeight;
			this.buttonReach.backgroundColor = 'yellow';
			this.buttonReach.ontouchstart = function() {
				var e = new enchant.Event('reach');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonReach.visible = true;
			this.buttonNoHuro = new Label('有鳴');
			this.buttonNoHuro.x = MahjongGame.buttonNoHuroLabelX;
			this.buttonNoHuro.y = MahjongGame.buttonNoHuroLabelY;
			this.buttonNoHuro.width = MahjongGame.buttonLabelWidth;
			this.buttonNoHuro.height = MahjongGame.buttonLabelHeight;
			this.buttonNoHuro.backgroundColor = 'yellow';
			this.buttonNoHuro.ontouchstart = function() {
				var e = new enchant.Event('noHuro');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonNoHuro.visible = true;
			this.buttonKan = new Label('カン');
			this.buttonKan.x = MahjongGame.buttonKanLabelX;
			this.buttonKan.y = MahjongGame.buttonKanLabelY;
			this.buttonKan.width = MahjongGame.buttonLabelWidth;
			this.buttonKan.height = MahjongGame.buttonLabelHeight;
			this.buttonKan.backgroundColor = 'yellow';
			this.buttonKan.ontouchstart = function() {
				var e = new enchant.Event('kan');
				MahjongGame.game_.dispatchEvent(e);
			};
			this.buttonKan.visible = false;
			
			this.sipaiWorld = null;
			
			this.fr = 0;
			this.smart = 0;
			if ($("#smart")[0] && $("#smart").val() == 1) {
				this.smart = 1;
			}
			this.selectMode = 0;
			this.swipeStartX = 0;
			this.swipeStartY = 0;
			this.swipeEndX = 0;
			this.swipeEndY = 0;
			this.selectingPos = 0;
			this.ajaxStatus = 0;
			this.shuffleFlag = 0;
			this.tsumikomiSelectable = 0;
			
			MahjongGame.game_.fps = 4;
			MahjongGame.game_.preload([MahjongPai.image_, MahjongPhyPai.image_]);
			MahjongPai.setGame(MahjongGame.game_);
			MahjongPhyPai.setGame(MahjongGame.game_);
			MahjongDispPai.setGame(MahjongGame.game_);
			MahjongTehai.setGame(MahjongGame.game_);
			MahjongHo.setGame(MahjongGame.game_);
			MahjongYama.setGame(MahjongGame.game_);
			MahjongPlayerInfo.setGame(MahjongGame.game_);
			
			var that = this;
			MahjongGame.game_.onload = function() {
				MahjongGame.game_.keybind('H'.charCodeAt(0), 'down');
				MahjongGame.game_.keybind('G'.charCodeAt(0), 'a');
				MahjongGame.game_.keybind('B'.charCodeAt(0), 'b');
				MahjongGame.game_.rootScene.backgroundColor = 'green';
			};
			MahjongGame.game_.onparticipate = function() {
				that.sendAjax('participate', 0);
			};
			MahjongGame.game_.onkan = function() {
				var kan0Event = function() {
					var e = new enchant.Event('kan0');
					MhjongGame.game_.dispatchEvent(e);
				};
				var kan1Event = function() {
					var e = new enchant.Event('kan1');
					MhjongGame.game_.dispatchEvent(e);
				};
				var kan2Event = function() {
					var e = new enchant.Event('kan2');
					MhjongGame.game_.dispatchEvent(e);
				};
				var kanable = that.tehais[0].getKanable();
				if (kanable.length > 1) {
					var posX = MahjongGame.nakiSelectX;
					var posY = MahjongGame.nakiSelectY;
					for (var i = 0; i < kanable.length; i++) {
						var pai = kanable[i];
						pai.x = posX;
						pai.y = posY;
						if (i == 0) {
							pai.addEventListener('touchstart', kan0Event);
						} else if (i == 1) {
							pai.addEventListener('touchstart', kan1Event);
						} else {
							pai.addEventListener('touchstart', kan2Event);
						}
						MahjongGame.game_.rootScene.addChild(pai);
						
						posX -= mahjongPai.sizeX * 1.3;
					}
				} else {
					that.sendAjax('kan', 0);
				}
			};
			MahjongGame.game_.onkan0 = function() {
				that.sendAjax('kan', 0);
			};
			MahjongGame.game_.onkan1 = function() {
				that.sendAjax('kan', 1);
			};
			MahjongGame.game_.onkan2 = function() {
				that.sendAjax('kan', 2);
			};
			MahjongGame.game_.onselectm1 = function() {
				that.eatFlag = false;
				alert('eat', -1);
			};
			MahjongGame.game_.onselect0 = function() {
				var key = 'drop';
				if (that.eatFlag) {
					key = 'eat';
					that.eatFlag = false;
				}
				that.sendAjax(key, 0);
			};
			MahjongGame.game_.onselect1 = function() {
				var key = 'drop';
				if (that.eatFlag) {
					key = 'eat';
					that.eatFlag = false;
				}
				that.sendAjax(key, 1);
			};
			MahjongGame.game_.onselect2 = function() {
				var key = 'drop';
				if (that.eatFlag) {
					key = 'eat';
					that.eatFlag = false;
				}
				that.sendAjax(key, 2);
			};
			MahjongGame.game_.onselect3 = function() {
				var key = 'drop';
				if (that.eatFlag) {
					key = 'eat';
					that.eatFlag = false;
				}
				that.sendAjax(key, 3);
			};
			MahjongGame.game_.onselect4 = function() {
				that.sendAjax('drop', 4);
			};
			MahjongGame.game_.onselect5 = function() {
				that.sendAjax('drop', 5);
			};
			MahjongGame.game_.onselect6 = function() {
				that.sendAjax('drop', 6);
			};
			MahjongGame.game_.onselect7 = function() {
				that.sendAjax('drop', 7);
			};
			MahjongGame.game_.onselect8 = function() {
				that.sendAjax('drop', 8);
			};
			MahjongGame.game_.onselect9 = function() {
				that.sendAjax('drop', 9);
			};
			MahjongGame.game_.onselect10 = function() {
				that.sendAjax('drop', 10);
			};
			MahjongGame.game_.onselect11 = function() {
				that.sendAjax('drop', 11);
			};
			MahjongGame.game_.onselect12 = function() {
				that.sendAjax('drop', 12);
			};
			MahjongGame.game_.onselect13 = function() {
				that.sendAjax('drop', 13);
			};
			MahjongGame.game_.onhora = function() {
				that.sendAjax('hora', 0);
			};
			MahjongGame.game_.onhuro = function() {
				that.eatFlag = true;
				var hist = that.tehais[0].toHistogram();
				var eatable = [];
				if (that.turn !== 1 && that.latestDrop.getType() !== 'z') {
					var num = that.latestDrop.getNum();
					if (num >= 3) {
						if (hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() - 2))] > 0 &&
							hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() - 1))] > 0
						) {
							eatable.push(-1);
						}
					}
					if (num >= 2 && num <= 8) {
						if (hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() - 1))] > 0 &&
							hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() + 1))] > 0
						) {
							eatable.push(0);
						}
					}
					if (num <= 7) {
						if (hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() + 1))] > 0 &&
							hist[MahjongPai.strToNum(that.latestDrop.getType() + (that.latestDrop.getNum() + 2))] > 0
						) {
							eatable.push(1);
						}
					}
				}
				if (hist[MahjongPai.strToNum(that.latestDrop.str)] >= 2) {
					eatable.push(2);
				}
				if (hist[MahjongPai.strToNum(that.latestDrop.str)] == 3) {
					eatable.push(3);
				}
				if (eatable.length === 1) {
					that.sendAjax('eat', eatable[0]);
					return;
				} else if (eatable.length > 1) {
					var posX = MahjongGame.nakiSelectX;
					var posY = MahjongGame.nakiSelectY;
					for (var i = eatable.length - 1; i >= 0; i--) {
						var id = eatable[i];
						if (id === -1) {
							id = 'm1';
						}
						var pai1 = MahjongPai.Pai();
						pai1.setId(id);
						pai1.x = posX;
						pai1.y = posY;
						posX -= MahjongPai.sizeX;
						var pai2 = MahjongPai.Pai();
						pai2.setId(id);
						pai2.x = posX;
						pai2.y = posY;
						posX -= MahjongPai.sizeX;
						var pai3 = MahjongPai.Pai();
						pai3.setId(id);
						pai3.x = posX;
						pai3.y = posY;
						posX -= MahjongPai.sizeX;
						var paiKan = MahjongPai.Pai();
						paiKan.setId(id);
						paiKan.x = posX;
						paiKan.y = posY;
						if (eatable[i] === -1) {
							pai1.setFrame(that.latestDrop.str);
							pai2.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() - 1));
							pai3.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() - 2));
						} else if (eatable[i] === 0) {
							pai1.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() + 1));
							pai2.setFrame(that.latestDrop.str);
							pai3.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() - 1));
						} else if (eatable[i] === 1) {
							pai1.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() + 2));
							pai2.setFrame(that.latestDrop.getType() + (that.latestDrop.getNum() + 1));
							pai3.setFrame(that.latestDrop.str);
						} else if (eatable[i] >= 2) {
							pai1.setFrame(that.latestDrop.str);
							pai2.setFrame(that.latestDrop.str);
							pai3.setFrame(that.latestDrop.str);
						}
						MahjongGame.game_.rootScene.addChild(pai1);
						MahjongGame.game_.rootScene.addChild(pai2);
						MahjongGame.game_.rootScene.addChild(pai3);
						
						if (eatable[i] === 3) {
							paiKan.setFrame(that.latestDrop.str);
							MahjongGame.game_.rootScene.addChild(paiKan);
							posX -= MahjongPai.sizeX * 1.3;
						} else {
							posX -= MahjongPai.sizeX * 0.3;
						}
					}
				}
			};
			MahjongGame.game_.oncancel = function() {
				if (!that.buttonCancel.visible) {
					return;
				}
				that.sendAjax('cancel', 0);
			};
			MahjongGame.game_.onreach = function() {
				that.sendAjax('reach', 0);
			};
			MahjongGame.game_.onnoHuro = function() {
				that.sendAjax('noHuro', 0);
			};
			MahjongGame.game_.onenterframe = function() {
				if (that.shuffleFlag == 0) {
					if (that.ajaxStatus == 0) {
						that.ajaxStatus = 1;
						that.refresh();
					}
				} else {
					if (that.ajaxStatus == 0) {
						that.ajaxStatus = 1;
						that.sipaiRefresh();
					}
					var children = MahjongGame.game_.rootScene.childNodes;
					for (var ci = 0; ci < children.length; ci++) {
						if (!children[ci].dispPai && children[ci].body.m_body.GetType() == DYNAMIC_SPRITE) {
							if (children[ci].x < 50 ||
									children[ci].x > MahjongGame.game_.width - 50 ||
									children[ci].y < 50 ||
									children[ci].y > MahjongGame.game_.height - 50) {
								children[ci].position = {x: Math.floor(Math.random()* (MahjongGame.game_.height) - 100) + 50 , y:Math.floor(Math.random()* (MahjongGame.game_.width - 100)) + 50};
							}
							if (Math.random() * 100 < 5) {
								children[ci].reverse();
							}
						}
					}
					if (MahjongGame.game_.frame % MahjongGame.game_.fps == MahjongGame.game_.fps - 1) {
						$.ajax({
							type: 'POST',
							url: 'chat_casino.cgi',
							data: {
								id: $("#id").val(),
								pass: $("#pass").val(),
								mode: 'tedumi',
								arg: 'u0'
							}
						});
					}
					that.sipaiWorld.step(MahjongGame.game_.fps);
				}
			};
			if (that.smart == 1) {
				MahjongGame.game_.rootScene.ontouchstart = function(e) {
					that.swipeStartX = e.x;
					that.swipeStartY = e.y;
				};
				MahjongGame.game_.rootScene.ontouchend = function(e) {
					that.swipeEndX = e.x;
					that.swipeEndY = e.y;
					var difX = that.swipeEndX - that.swipeStartX;
					var difY = that.swipeEndY - that.swipeStartY;
					if (difX < -50 || difX > 50) {
						if (that.selectMode == 1) {
							if (difX < 0) {
								that.selectingPos--;
							} else {
								that.selectingPos++;
							}
							if (that.selectingPos < 0) {
								that.selectingPos = that.tehais[0].tehai.length - 1;
							} else if (that.selectingPos >= that.tehais[0].tehai.length) {
								that.selectingPos = 0;
							}
							that.refresh();
						} else if (that.selectMode == 2) {
							if (difX < 0) {
								var e = new enchant.Event('huro');
								MahjongGame.game_.dispatchEvent(e);
							} else {
								var e = new enchant.Event('hora');
								MahjongGame.game_.dispatchEvent(e);
							}
						}
					} else if (difY < -50) {
						if (that.selectMode == 1) {
							var e = new enchant.Event('select' + that.selectingPos);
							MahjongGame.game_.dispatchEvent(e);
						}
					} else if (difY > 50) {
						var e = new enchant.Event('cancel');
						MahjongGame.game_.dispatchEvent(e);
					}
				};
			}
			MahjongGame.game_.ondownbuttondown = function() {
				$.ajax({
					type: 'POST',
					url: 'chat_casino.cgi',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'tsumikomi',
						arg: 1
					}
				});
			};
			MahjongGame.game_.onabuttondown = function() {
				$.ajax({
					type: 'POST',
					url: 'chat_casino.cgi',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'tsumikomi',
						arg: 2
					}
				});
			};
			MahjongGame.game_.onbbuttondown = function() {
				$.ajax({
					type: 'POST',
					url: 'chat_casino.cgi',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'tsumikomi',
						arg: 3
					}
				});
			};
		},
		
		refresh: function() {
			var that = this;
			$.ajax({
				type: 'POST',
				url: 'mahjong_ajax.cgi',
				data: {
					id: $("#id").val(),
					pass: $("#pass").val(),
					no: $("#no").val()
				},
				dataType: 'json',
				success: function(data) {
					that.tempClear();
					var child = MahjongGame.game_.rootScene.firstChild;
					while (child !== undefined && child !== null) {
						child.clearEventListener('touchstart');
						MahjongGame.game_.rootScene.removeChild(child);
						child = MahjongGame.game_.rootScene.firstChild;
					}
					for (var pi = 0; pi < data.PlayerNames.length; pi++) {
						that.playerNames.push(data.PlayerNames[pi]);
					}
					if (data.Round != -1) {
						if (data.Phase != -1) {
							for (var i = 0; i < data.Tehais.length; i++) {
								var tehai = MahjongTehai.Tehai();
								tehai.setPosition(i);
								tehai.setAll(data.Tehais[i].Tehai);
								that.tehais.push(tehai);
								if (i == 0) {
									that.tehais[0].setIds();
									if (that.smart == 1) {
										that.tehais[0].setSelected(that.selectingPos);
									}
								}
								that.tehais[i].show();

								var ho = MahjongHo.Ho();
								ho.setPosition(i);
								ho.setAll(data.Hos[i].Ho);
								that.hos.push(ho);
								that.hos[i].show();

								var point = MahjongPlayerInfo.PlayerInfo();
								point.setPosition(i);
								point.setPlayerName(data.Points[i].PName);
								point.setPoint(data.Points[i].Point);
								that.point.push(point);
								that.point[i].show();
								
								that.playerNoHuro.push(data.PlayerNoHuro[i]);
								that.playerHuroType.push(data.PlayerHuroType[i]);
								that.playerAutoFinish.push(data.PlayerAutoFinish[i]);
								that.playerIsFinish.push(data.PlayerIsFinish[i]);
								that.waitPlayer.push(data.WaitPlayer[i]);
							}
							
							that.yama = MahjongYama.Yama();
							that.yama.setJson(data.Yama);
							that.yama.show();
							
							that.round = data.Round;
							that.continuous = data.Continuous;
							that.turn = data.Turn;
							that.phase = data.Phase;
							that.roundSets = data.RoundSets;
							if (data.LatestDrop) {
								that.latestDrop = MahjongPai.Pai();
								that.latestDrop.setFrame(data.LatestDrop.Str);
							}
							that.dropPos = data.DropPos;
							that.kyotaku = data.Kyotaku;
							
							if (data.PlayerNoHuro[0] && data.PlayerNoHuro[0] > 1) {
								that.buttonNoHuro.text = '無鳴';
							} else {
								that.buttonNoHuro.text = '有鳴';
							}
							that.selectMode = 0;
							if (data.WaitPlayer[0] && data.WaitPlayer[0] > 0) {
								that.buttonCancel.visible = false;
								if (data.WaitPlayer[0] >= 2) {
									that.buttonHora.visible = true;
									that.buttonCancel.visible = true;
								} else {
									that.buttonHora.visible = false;
								}
								if (!data.PlayerNoHuro[0] || data.PlayerNoHuro[0] == 0) {
									that.buttonHuro.visible = true;
									that.buttonCancel.visible = true;
								} else {
									that.buttonHuro.visible = false;
								}
								that.selectMode = 2;
							} else {
								that.buttonHora.visible = false;
								that.buttonHuro.visible = false;
								that.buttonCancel.visible = false;
							}
							
							that.buttonKan.visible = false;
							if (that.tehais[0].isKiriban()) {
								if (that.tehais[0].calcShanten() == -1) {
									that.buttonHora.visible = true;
								} else {
									that.buttonHora.visible = false;
								}
								if (that.tehais[0].getKanable().length > 0) {
									that.buttonKan.visible = true;
								}
								that.selectMode = 1;
							}
							
							MahjongGame.game_.rootScene.addChild(that.infoLabel);
							MahjongGame.game_.rootScene.addChild(that.buttonHora);
							MahjongGame.game_.rootScene.addChild(that.buttonHuro);
							MahjongGame.game_.rootScene.addChild(that.buttonCancel);
							MahjongGame.game_.rootScene.addChild(that.buttonReach);
							MahjongGame.game_.rootScene.addChild(that.buttonNoHuro);
							MahjongGame.game_.rootScene.addChild(that.buttonKan);
							
							for (var di = 0; di < that.directLabels.length; d++) {
								MahjongGame.game_.rootScene.addChild(that.directLabels[i]);
							}
						} else {
							// 洗牌
							that.shuffleFlag = 1;

							that.sipaiWorld = new PhysicsWorld(0, 0);
							
							var paiInit = [];
							
							for (var ppi = 0; ppi < 34; ppi++) {
								for (var no = 0; no < 4; no++) {
									var pai = new MahjongPhyPai.PhyPai();
									
									pai.setId(MahjongPai.numToStr(ppi), no);
									
									if (Math.random() * 100 < 50) {
										pai.setUra(true);
									}
									
									paiInit.push(pai);
								}
							}
							
							// 初期配置ランダム
							var pii = paiInit.length;
							while (pii) {
								var pij = Math.floor(Math.random()*pii);
								var t = paiInit[--pii];
								paiInit[pii] = paiInit[pij];
								paiInit[pij] = t;
							}
							
							for (var pip = 0; pip < paiInit.length; pip++) {
								var posX = MahjongPhyPai.sizeX * 2.5 * (pip % 17);
								var posY = MahjongPhyPai.sizeY * 2.5 * parseInt(pip / 17, 10);
								paiInit[pip].position = { x: posX, y: posY };
								paiInit[pip].angle = Math.floor(Math.random()*360);
								MahjongGame.game_.rootScene.addChild(paiInit[pip]);
							}
							
							var rollBar = new PhyBoxSprite(MahjongGame.game_.width * 1.5, 5, KINEMATIC_SPRITE, 1.0, 0.5, 0.1, true);
							rollBar.position = {x: MahjongGame.game_.width * 0.5, y: MahjongGame.game_.height * 0.5};
							rollBar.angularVelocity = 10;
							rollBar.color = 'green';
							MahjongGame.game_.rootScene.addChild(rollBar);

							var up = new PhyBoxSprite(MahjongGame.game_.width, 100, STATIC_SPRITE, 1.0, 0.5, 0.1, true);
							up.position = {x: MahjongGame.game_.width * 0.5, y: 0};
							MahjongGame.game_.rootScene.addChild(up);
							
							var down = new PhyBoxSprite(MahjongGame.game_.width, 100, STATIC_SPRITE, 1.0, 0.5, 0.1, true);
							down.position = {x: MahjongGame.game_.width * 0.5, y: MahjongGame.game_.height};
							MahjongGame.game_.rootScene.addChild(down);
							
							var left = new PhyBoxSprite(100, MahjongGame.game_.height, STATIC_SPRITE, 1.0, 0.5, 0.1, true);
							left.position = {x: 0, y: MahjongGame.game_.height * 0.5};
							MahjongGame.game_.rootScene.addChild(left);
							
							var right = new PhyBoxSprite(100, MahjongGame.game_.height, STATIC_SPRITE, 1.0, 0.5, 0.1, true);
							right.position = {x: MahjongGame.game_.width, y: MahjongGame.game_.height * 0.5};
							MahjongGame.game_.rootScene.addChild(right);
						}
					} else {
						var sitInfo = new Label();
						sitInfo.font = "28px cursive";
						sitInfo.x = MahjongGame.game_.width * 0.4;
						sitInfo.y = MahjongGame.game_.height * 0.4;
						sitInfo.width = MahjongGame.game_.width * 0.2;
						sitInfo.height = MahjongGame.game_.height * 0.2;
						sitInfo.backgroundColor = 'white';
						var infoText = '';
						var direct = ['東', '南', '西', '北'];
						for (var i = 0; i < data.PlayerNames.length; i++) {
							infoText += direct[i] + ':';
							if (data.PlayerNames[i] !== null) {
								infoText += '着席';
							}
							infoText += "<br>";
						}
						sitInfo.text = infoText;
						MahjongGame.game_.rootScene.addChild(sitInfo);
					}
					that.ajaxStatus = 0;
				}
			});
		},
		
		sipaiRefresh: function() {
			var that = this;
			$.ajax({
				type: 'POST',
				url: 'mahjong_ajax.cgi',
				data: {
					id: $("#id").val(),
					pass: $("#pass").val(),
					no: $("#no").val()
				},
				dataType: 'json',
				success: function(data) {
					var children = MahjongGame.game_.rootScene.childNodes;
					for (var ci = 0; ci < children.length; ci++) {
						if (children[ci].dispPai
							|| (children[ci].body != null
								&& children[ci].body.m_body.GetType() == DYNAMIC_SPRITE
								&& $.inArray(children[ci].id, data.Yama.TedumiRest) == -1)) {
							children[ci].clearEventListener('touchstart');
							MahjongGame.game_.rootScene.removeChild(children[ci]);
						}
					}
					
					var noYama = true;
					if (data.Yama.TedumiYamas[0]) {
						for (var dp = 0; dp < data.Yama.TedumiYamas[0].length; dp++) {
							var dpStr = data.Yama.TedumiYamas[0][dp].substr(0, 2);
							if (dpStr == "u0") {
								continue;
							}
							var dPai = new MahjongDispPai.DispPai();
							dPai.setFrame(dpStr);
							dPai.x = MahjongGame.game_.width - MahjongDispPai.sizeX * parseInt((dp / 2 + 3), 10);
							dPai.y = MahjongGame.game_.height + MahjongDispPai.sizeY * (parseInt(dp % 2, 10) - 3);
							MahjongGame.game_.rootScene.addChild(dPai);
							noYama = false;
						}
					}
					if (noYama) {
						if (data.Yama.Tsumikomi[0] == 0) {
							this.tsumikomiSelectable = 1;
							var selectLabel = new Label();
							selectLabel.text = "平積み：H<br>元禄積み：G<br>爆弾積み：B<br>";
							selectLabel.dispPai = true;
							MahjongGame.game_.rootScene.addChild(selectLabel);
						}
					}
					if (data.Yama.TedumiRest.length <= 0) {
						that.shuffleFlag = 0;
					}
					that.ajaxStatus = 0;
				}
			});
		},
		
		tempClear: function() {
			this.tehais = [];
			this.hos = [];
			this.playerNames = [];
			this.point = [];
			this.yama = null;
			this.round = 0;
			this.continuous = 0;
			this.turn = 0;
			this.phase = -1;
			this.roundSets = 2;
			this.latestDrop = null;
			this.dropPos = null;
			this.kyotaku = 0;
			this.playerNoHuro = [];
			this.playerHuroType = [];
			this.playerAutoFinish = [];
			this.playerIsFinish = [];
			this.waitPlayer = [];
			this.eatFlag = false;
			this.tsumikomiSelectable = 0;
		},
		
		start: function() {
			MahjongGame.game_.start();
		},
		
		sendAjax: function(mode, arg) {
			$.ajax({
				type: 'POST',
				url: 'chat_casino.cgi',
				data: {
					id: $("#id").val(),
					pass: $("#pass").val(),
					mode: mode,
					arg: arg
				}
			});
		}
	});
	
	return MahjongGame;
});