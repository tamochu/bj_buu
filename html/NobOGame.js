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
		NobOGame = definition();
	}

})(function(){// 実際の定義を行う関数
	'use strict';

	var NobOGame= {};
	
	NobOGame.sizeX = 550;
	NobOGame.sizeY = 550;
	NobOGame.scale = 100;
	NobOGame.fps = 24;
	NobOGame.image_ = ['./html/chara1.png', './html/bar.png', './icon0.png', './html/catsle.png'];
	NobOGame.game_ = null;
	NobOGame.stage = null;
	NobOGame.baseX = 0;
	NobOGame.baseY = 0;
	NobOGame.resetX = 0;
	NobOGame.resetY = 0;
	NobOGame.infoLabelWidth = 200;
	NobOGame.infoLabelHeight = 60;
	NobOGame.worldTop = 0;
	NobOGame.worldBottom = NobOGame.sizeX;
	NobOGame.worldLeft = 0;
	NobOGame.worldRight = NobOGame.sizeY;
	NobOGame.barWidth = 100;
	NobOGame.barHeight = 10;
	NobOGame.setGame = function(game) {
		NobOGame.game_ = game;
		NobOGame.game_._touchEventTarget = [];
	};
	
	// ゲームのクラス本体
	NobOGame.Game = Class.create({
		initialize: function() {
			var that = this;
			NobOGame.game_.fps = NobOGame.fps;
			NobOGame.game_.preload(NobOGame.image_);
			NobOGame.id = $("#id").val();
			NobOGame.salt = Math.floor($.now() / 1000);
			NobOGame.sid = CybozuLabs.MD5.calc(NobOGame.salt + NobOGame.id);
			NobOGame.game_.onload = function() {
				NobOGame.game_.keybind('R'.charCodeAt(0), 'a');
				NobOGame.game_.rootScene.backgroundColor = 'white';
				
				var pad = new Pad();
				pad.x = 0;
				pad.y = 0;
				NobOGame.game_.rootScene.addChild(pad);
				
				var resetButton = new enchant.ui.Button('位置リセット');
				resetButton.x = 0;
				resetButton.y = 100;
				resetButton.ontouchstart = function() {
					that.resetPosition();
				};
				NobOGame.game_.rootScene.addChild(resetButton);
				
				var zoomInButton = new enchant.ui.Button('+');
				zoomInButton.x = 0;
				zoomInButton.y = 130;
				zoomInButton.ontouchstart = function() {
					that.zoomIn();
				};
				NobOGame.game_.rootScene.addChild(zoomInButton);
				
				var zoomOutButton = new enchant.ui.Button('-');
				zoomOutButton.x = 0;
				zoomOutButton.y = 160;
				zoomOutButton.ontouchstart = function() {
					that.zoomOut();
				};
				NobOGame.game_.rootScene.addChild(zoomOutButton);
				
				NobOGame.moveButton = new enchant.ui.Button('兵士移動');
				NobOGame.moveButton.x = 0;
				NobOGame.moveButton.y = 190;
				NobOGame.moveButton.buttonMode = 0;
				NobOGame.moveButton.ontouchstart = function() {
					if (NobOGame.moveButton.buttonMode == 1) {
						that.trade();
					} else {
						that.move();
					}
				};
				NobOGame.game_.rootScene.addChild(NobOGame.moveButton);
				
				NobOGame.changeButton = new enchant.ui.Button('モード変更');
				NobOGame.changeButton.x = 0;
				NobOGame.changeButton.y = 220;
				NobOGame.changeButton.ontouchstart = function() {
					if (NobOGame.moveButton.buttonMode == 1) {
						NobOGame.moveButton.buttonMode = 0;
						NobOGame.moveButton.text = '兵士移動';
					} else {
						NobOGame.moveButton.buttonMode = 1;
						NobOGame.moveButton.text = '交易';
					}
				};
				NobOGame.game_.rootScene.addChild(NobOGame.changeButton);
				
				var barLabel = new Label('');
				barLabel.x = 20;
				barLabel.y = 250;
				barLabel.width = 30;
				barLabel.height = NobOGame.barHeight;
				NobOGame.bar = new Bar(NobOGame.barWidth, NobOGame.barHeight);
				NobOGame.bar.x = 50;
				NobOGame.bar.y = 250;
				NobOGame.bar.image = NobOGame.game_.assets[NobOGame.image_[1]];
				NobOGame.bar.maxvalue = 100;
				NobOGame.bar.value = 10;
				NobOGame.bar.touchV = -10;
				NobOGame.bar.ontouchstart = function() {
					this.value += this.touchV;
					if (this.value <= 10 && this.touchV < 0) {
						this.touchV = 10;
						this.value = 10;
					} else if (this.value >= 100 && this.touchV > 0) {
						this.touchV = -10;
						this.value = 100;
					}
					barLabel.text = NobOGame.bar.value + '%';
				};
				barLabel.text = NobOGame.bar.value + '%';
				NobOGame.game_.rootScene.addChild(NobOGame.bar);
				
				NobOGame.barDown = new Sprite(16, 16);
				NobOGame.barDown.image = NobOGame.game_.assets[NobOGame.image_[2]];
				NobOGame.barDown.x = 0;
				NobOGame.barDown.y = 250;
				NobOGame.barDown.frame = 43;
				NobOGame.barDown.rotation = 180;
				NobOGame.barDown.ontouchstart = function() {
					NobOGame.bar.value -= 10;
					if (NobOGame.bar.value <= 10) {
						NobOGame.bar.value = 10;
					}
					barLabel.text = NobOGame.bar.value + '%';
				}
				NobOGame.game_.rootScene.addChild(NobOGame.barDown);
				
				NobOGame.barUp = new Sprite(16, 16);
				NobOGame.barUp.image = NobOGame.game_.assets[NobOGame.image_[2]];
				NobOGame.barUp.x = 50 + NobOGame.barWidth;
				NobOGame.barUp.y = 250;
				NobOGame.barUp.frame = 43;
				NobOGame.barUp.ontouchstart = function() {
					NobOGame.bar.value += 10;
					if (NobOGame.bar.value >= 100) {
						NobOGame.bar.value = 100;
					}
					barLabel.text = NobOGame.bar.value + '%';
				}
				NobOGame.game_.rootScene.addChild(NobOGame.barUp);
				NobOGame.game_.rootScene.addChild(barLabel);
				
				NobOGame.nameInput = new InputTextBox();
				NobOGame.nameInput.x = 0;
				NobOGame.nameInput.y = 280;
				NobOGame.nameInput.width = 100;
				NobOGame.nameInput.placeholder = '領地に名前を付けます';
				NobOGame.game_.rootScene.addChild(NobOGame.nameInput);
				
				var nameSetButton = new enchant.ui.Button('変更');
				nameSetButton.x = 100;
				nameSetButton.y = 280;
				nameSetButton.ontouchstart = function() {
					that.territoryNameSet();
				};
				NobOGame.game_.rootScene.addChild(nameSetButton);
				
				
				NobOGame.infoLabel1 = new Label();
				NobOGame.infoLabel1.x = NobOGame.sizeX - NobOGame.infoLabelWidth;
				NobOGame.infoLabel1.y = 0;
				NobOGame.infoLabel1.width = NobOGame.infoLabelWidth;
				NobOGame.infoLabel1.height = NobOGame.infoLabelHeight;
				NobOGame.infoLabel1.backgroundColor = 'gray';
				NobOGame.infoLabel1.ontouchstart = function() {
					if (this.info) {
						that.movePos(this.info.moveX, this.info.moveY);
					}
				};
				NobOGame.game_.rootScene.addChild(NobOGame.infoLabel1);

				NobOGame.infoLabel2 = new Label();
				NobOGame.infoLabel2.x = NobOGame.sizeX - NobOGame.infoLabelWidth;
				NobOGame.infoLabel2.y = NobOGame.infoLabelHeight;
				NobOGame.infoLabel2.width = NobOGame.infoLabelWidth;
				NobOGame.infoLabel2.height = NobOGame.infoLabelHeight;
				NobOGame.infoLabel2.backgroundColor = 'gray';
				NobOGame.infoLabel2.ontouchstart = function() {
					if (this.info) {
						that.movePos(this.info.moveX, this.info.moveY);
					}
				};
				NobOGame.game_.rootScene.addChild(NobOGame.infoLabel2);
				
				that.readData();
			};
			
			NobOGame.game_.onabuttondown = function() {
				that.resetPosition();
			};
		},
		
		start: function() {
			NobOGame.game_.start();
		},
		
		movePos: function(x, y) {
			NobOGame.stage.x = (NobOGame.sizeX / 2) - x * NobOGame.stage.scaleX;
			NobOGame.stage.y = (NobOGame.sizeY / 2) - y * NobOGame.stage.scaleY;
		},
		
		resetPosition: function() {
			if (NobOGame.resetX == 0 && NobOGame.resetY == 0) {
				this.movePos(NobOGame.baseX, NobOGame.baseY);
			} else {
				this.movePos(NobOGame.resetX, NobOGame.resetY);
			}
		},
		
		zoomIn: function() {
			var x = ((NobOGame.sizeX / 2) - NobOGame.stage.x) / NobOGame.stage.scaleX;
			var y = ((NobOGame.sizeY / 2) - NobOGame.stage.y) / NobOGame.stage.scaleY;
			NobOGame.stage.scaleX /= 0.8;
			NobOGame.stage.scaleY /= 0.8;
			this.movePos(x, y);
		},
		
		zoomOut: function() {
			var x = ((NobOGame.sizeX / 2) - NobOGame.stage.x) / NobOGame.stage.scaleX;
			var y = ((NobOGame.sizeY / 2) - NobOGame.stage.y) / NobOGame.stage.scaleY;
			NobOGame.stage.scaleX *= 0.8;
			NobOGame.stage.scaleY *= 0.8;
			this.movePos(x, y);
		},
		
		setInfo: function(info) {
			if (NobOGame.infoLabel1.info && NobOGame.infoLabel1.info.terId == info.terId) {
				NobOGame.infoLabel2.text = NobOGame.infoLabel1.detailText;
			} else {
				NobOGame.infoLabel2.text = NobOGame.infoLabel1.text;
			}
			NobOGame.infoLabel2.backgroundColor = NobOGame.infoLabel1.backgroundColor;
			NobOGame.infoLabel2.info = NobOGame.infoLabel1.info;
			
			NobOGame.infoLabel1.backgroundColor = info.backgroundColor;
			var infoText = info.name;
			if (info.capital) {
				infoText += '(首都)'
			}
			infoText += "<br>所有者コード:" + info.owner.substr(0, 6) + "<br>座標X" + info.x + "<br>座標Y" + info.y;
			NobOGame.infoLabel1.text = infoText;
			NobOGame.infoLabel1.detailText = "人口:" + info.population
											+ "  環境:" + info.environment
											+ "<br>文明:" + info.civilization
											+ "  分化:" + info.culture;
			NobOGame.infoLabel1.info = info;

			var start = null;
			var goal = null;
			for (var nodeI = 0; nodeI < NobOGame.stage.childNodes.length; nodeI++) {
				var node = NobOGame.stage.childNodes[nodeI];
				if (node.terId) {
					if (NobOGame.infoLabel2.info && node.terId == NobOGame.infoLabel2.info.terId) {
						start = node;
					} else if (NobOGame.infoLabel1.info && node.terId == NobOGame.infoLabel1.info.terId) {
						goal = node;
					}
				}
			}
			NobOGame.arrow.context.clearRect(0, 0, NobOGame.worldRight - NobOGame.worldLeft, NobOGame.worldBottom - NobOGame.worldTop);
			if (start && goal) {
				NobOGame.arrow.context.beginPath();
				NobOGame.arrow.context.moveTo(start.x + 16 - NobOGame.worldLeft, start.y + 16 - NobOGame.worldTop);
				NobOGame.arrow.context.lineTo(goal.x + 16 - NobOGame.worldLeft, goal.y + 16 - NobOGame.worldTop);
				NobOGame.arrow.context.closePath();
				NobOGame.arrow.context.stroke();
				
				NobOGame.arrow.context.beginPath();
				NobOGame.arrow.context.arc(goal.x + 16 - NobOGame.worldLeft, goal.y + 16 - NobOGame.worldTop, 10, 0, Math.PI*2, false);
				NobOGame.arrow.context.fill();
			}
		},
		
		move: function() {
			var that = this;
			if (NobOGame.infoLabel1.info && NobOGame.infoLabel2.info && NobOGame.bar) {
				$.ajax({
					type: 'POST',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'move',
						from: NobOGame.infoLabel2.info.terId,
						to: NobOGame.infoLabel1.info.terId,
						amount: NobOGame.bar.value
					},
					success: function(data) {
						that.reload();
					}
				});
			}
		},
		
		trade: function() {
			var that = this;
			if (NobOGame.infoLabel1.info && NobOGame.infoLabel2.info && NobOGame.bar) {
				$.ajax({
					type: 'POST',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'trade',
						from: NobOGame.infoLabel2.info.terId,
						to: NobOGame.infoLabel1.info.terId,
					},
					success: function(data) {
						that.reload();
					}
				});
			}
		},
		
		territoryNameSet: function() {
			var that = this;
			if (NobOGame.infoLabel1.info && NobOGame.nameInput.value) {
				$.ajax({
					type: 'POST',
					data: {
						id: $("#id").val(),
						pass: $("#pass").val(),
						mode: 'territory_name_set',
						at: NobOGame.infoLabel1.info.terId,
						territory_name: NobOGame.nameInput.value
					},
					success: function(data) {
						that.reload();
						that.infoLabelReset();
					}
				});
			}
		},
		
		readData: function() {
			var that = this;
			$.ajax({
				type: 'POST',
				url: 'nobo_ajax.cgi',
				dataType: 'JSON',
				data: {
					id: $("#id").val(),
					pass: $("#pass").val()
				},
				success: function(data) {
					that.preReload();
					var territories = [];
					for (var terI = 0; terI < data.NobO.Territories.length; terI++) {
						var ter = new Sprite(56, 50);
						ter.image = NobOGame.game_.assets[NobOGame.image_[3]];
						ter.terId = data.NobO.Territories[terI].NobOTerritory.ID;
						ter.orgX = data.NobO.Territories[terI].NobOTerritory.X;
						ter.orgY = data.NobO.Territories[terI].NobOTerritory.Y;
						ter.x = ter.orgX * NobOGame.scale;
						if (NobOGame.worldLeft > ter.x) {
							NobOGame.worldLeft = ter.x;
						}
						if (NobOGame.worldRight < ter.x) {
							NobOGame.worldRight = ter.x;
						}
						ter.y = ter.orgY * NobOGame.scale;
						if (NobOGame.worldTop > ter.y) {
							NobOGame.worldTop = ter.y;
						}
						if (NobOGame.worldBottom < ter.y) {
							NobOGame.worldBottom = ter.y;
						}
						ter.name = data.NobO.Territories[terI].NobOTerritory.Name;
						ter.owner = '';
						for (var ownI = 0; ownI < data.NobO.Owners.length; ownI++) {
							if (data.NobO.Owners[ownI].NobOOwner.TerritoryID == data.NobO.Territories[terI].NobOTerritory.ID) {
								if (data.NobO.Owners[ownI].NobOOwner.OwnerName == NobOGame.id && data.NobO.Owners[ownI].NobOOwner.Capital) {
									NobOGame.baseX = ter.x;
									NobOGame.baseY = ter.y;
								}
								ter.owner = data.NobO.Owners[ownI].NobOOwner.OwnerName;
								ter.capital = data.NobO.Owners[ownI].NobOOwner.Capital;
							}
						}
						if (ter.owner == NobOGame.id) {
							ter.ownerKbn  = 1;
							ter.frame = 0;
						} else if (ter.owner == '') {
							ter.ownerKbn  = 0;
							ter.frame = 2;
						} else {
							ter.ownerKbn  = -1;
							ter.frame = 4;
						}
						if (ter.capital) {
							ter.frame += 1;
						}
						ter.population = data.NobO.Territories[terI].NobOTerritory.Population;
						ter.environment = data.NobO.Territories[terI].NobOTerritory.Environment;
						ter.civilization = data.NobO.Territories[terI].NobOTerritory.Civilization;
						ter.culture = data.NobO.Territories[terI].NobOTerritory.Culture;
						
						ter.ontouchstart = function() {
							var info = new Object();
							info.terId = this.terId;
							info.name = this.name;
							info.owner = '';
							if (this.owner) {
								info.owner = CybozuLabs.MD5.calc(NobOGame.salt + this.owner);
							}
							if (this.ownerKbn == 1) {
								info.backgroundColor = '#FFFFFF';
							} else if (this.ownerKbn == 0) {
								info.backgroundColor = '#AAFFAA';
							} else {
								info.backgroundColor = '#AAAAFF';
							}
							info.x = this.orgX;
							info.y = this.orgY;
							info.moveX = this.x;
							info.moveY = this.y;
							
							info.population = this.population;
							info.environment = this.environment;
							info.civilization = this.civilization;
							info.culture = this.culture;
							info.capital = this.capital;
							
							that.setInfo(info);
						};
						territories.push(ter);
					}
					var armies = [];
					for (var armI = 0; armI < data.NobO.Armies.length; armI++) {
						var arm = new Sprite(32, 32);
						arm.image = NobOGame.game_.assets[NobOGame.image_[0]];
						arm.armId = data.NobO.Armies[armI].NobOArmy.ID;
						arm.orgX = data.NobO.Armies[armI].NobOArmy.X;
						arm.orgY = data.NobO.Armies[armI].NobOArmy.Y;
						arm.x = arm.orgX * NobOGame.scale;
						arm.y = arm.orgY * NobOGame.scale;
						arm.startX = arm.x;
						arm.startY = arm.y;
						arm.leaderName = data.NobO.Armies[armI].NobOArmy.LeaderName;
						arm.speed = data.NobO.Armies[armI].NobOArmy.Speed;
						arm.targetTerritoryId = data.NobO.Armies[armI].NobOArmy.TargetTerritoryID;
						for (var terI = 0; terI < territories.length; terI++) {
							if (territories[terI].terId == arm.targetTerritoryId) {
								arm.targetX = territories[terI].x;
								arm.targetY = territories[terI].y;
								arm.afterStartTime = 0;
								arm.onenterframe = function() {
									if (NobOGame.game_.frame % NobOGame.game_.fps == 0) {
										this.afterStartTime++;
										var distance = Math.sqrt(Math.pow((this.targetX - this.startX), 2) + Math.pow((this.targetY - this.startY), 2));
										var p = this.speed * NobOGame.scale * this.afterStartTime / distance;
										if (p > 1.0) {
											that.reload();
										}
										this.moveTo((this.targetX * p + this.startX * (1 - p)), (this.targetY * p + this.startY * (1 - p)));
									}
								};
								break;
							}
						}
						arm.targetToMyTerritory = false;
						for (var ownI = 0; ownI < data.NobO.Owners.length; ownI++) {
							if (data.NobO.Owners[ownI].NobOOwner.TerritoryID == arm.targetTerritoryId && data.NobO.Owners[ownI].NobOOwner.OwnerName == NobOGame.id) {
								arm.targetToMyTerritory = true;
							}
						}
						
						arm.frame = 0;
						if (arm.leaderName != NobOGame.id) {
							arm.frame = 5;
							if (arm.targetToMyTerritory) {
								arm.frame = 10;
							}
						}
						armies.push(arm);
					}
					that.postReload();
					for (var terI = 0; terI < territories.length; terI++) {
						NobOGame.stage.addChild(territories[terI]);
					}
					for (var armI = 0; armI < armies.length; armI++) {
						NobOGame.stage.addChild(armies[armI]);
					}
					NobOGame.game_.rootScene.addChild(NobOGame.barDown);
					NobOGame.game_.rootScene.addChild(NobOGame.barUp);
					that.resetPosition();
				}
			});
		},
		
		reload: function() {
			NobOGame.resetX = ((NobOGame.sizeX / 2) - NobOGame.stage.x) / NobOGame.stage.scaleX;
			NobOGame.resetY = ((NobOGame.sizeY / 2) - NobOGame.stage.y) / NobOGame.stage.scaleY;
			this.readData();
		},
		
		preReload: function() {
			NobOGame.game_.rootScene.removeChild(NobOGame.stage);
			NobOGame.game_.rootScene.removeChild(NobOGame.bar);
			NobOGame.game_.rootScene.removeChild(NobOGame.barDown);
			NobOGame.game_.rootScene.removeChild(NobOGame.barUp);

			NobOGame.stage = new Group();
		},
		
		postReload: function() {
			var w = Math.ceil(NobOGame.worldRight - NobOGame.worldLeft);
			var h = Math.ceil(NobOGame.worldBottom - NobOGame.worldTop);
			NobOGame.arrow = new Sprite(w, h);
			var surface = new Surface(w, h);
			NobOGame.arrow.image = surface;
			NobOGame.arrow.context = surface.context;
			NobOGame.arrow.x = NobOGame.worldLeft;
			NobOGame.arrow.y = NobOGame.worldTop;
			NobOGame.stage.addChild(NobOGame.arrow);
			
			NobOGame.stage.addEventListener(Event.ENTER_FRAME, function(e) {
				if (NobOGame.game_.input.right) {
					NobOGame.stage.x -= 5;
				} else if (NobOGame.game_.input.left) {
					NobOGame.stage.x += 5;
				}
				if (NobOGame.game_.input.up) {
					NobOGame.stage.y += 5;
				} else if (NobOGame.game_.input.down) {
					NobOGame.stage.y -= 5;
				}
			});
			
			NobOGame.game_.rootScene.addChild(NobOGame.stage);
			NobOGame.game_.rootScene.addChild(NobOGame.bar);
		},
		
		infoLabelReset: function() {
			NobOGame.infoLabel1.text = '';
			NobOGame.infoLabel1.backgroundColor = 'gray';
			NobOGame.infoLabel1.info = null;

			NobOGame.infoLabel2.text = '';
			NobOGame.infoLabel2.backgroundColor = 'gray';
			NobOGame.infoLabel2.info = null;
			
			NobOGame.arrow.context.clearRect(0, 0, NobOGame.worldRight - NobOGame.worldLeft, NobOGame.worldBottom - NobOGame.worldTop);
		}
	});
	
	return NobOGame;
});