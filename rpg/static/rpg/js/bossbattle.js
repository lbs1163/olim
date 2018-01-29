// using jQuery
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

var battle = new Audio('/static/rpg/sound/bossbattle.mp3');
var select = new Audio('/static/rpg/sound/select.mp3');
var hit = new Audio('/static/rpg/sound/hit.mp3');
var destroy = new Audio('/static/rpg/sound/destroy.mp3');
var win = new Audio('/static/rpg/sound/win.mp3');
var lose = new Audio('/static/rpg/sound/lose.mp3');
var talk = new Audio('/static/rpg/sound/talk.mp3');

function initAudio() {
	battle.volume = 0;
	select.volume = 0;
	hit.volume = 0;
	destroy.volume = 0;
	win.volume = 0;
	lose.volume = 0;
	talk.volume = 0;

	battle.play();
	battle.pause();
	select.play();
	select.pause();
	hit.play();
	hit.pause();
	destroy.play();
	destroy.pause();
	win.play();
	win.pause();
	lose.play();
	lose.pause();
	talk.play();
	talk.pause();

	battle.currentTime = 0;
	select.currentTime = 0;
	hit.currentTime = 0;
	destroy.currentTime = 0;
	win.currentTime = 0;
	lose.currentTime = 0;
	talk.currentTime = 0;

	battle.volume = 1;
	select.volume = 1;
	hit.volume = 1;
	destroy.volume = 1;
	win.volume = 1;
	lose.volume = 1;
	talk.volume = 1;

	battle.loop = true;
	battle.play();
}

var dialog = function(string, i, callback) {
	$("#dialog").html(string);
	setTimeout(function(){callback();}, 1000);
}

var buttonOn = function() {
	$("button.skill").off("click touchstart")
		$("button.skill").on("click touchstart", function(e) {
			var skill = $(this).attr("skill");
			var health = parseInt($(this).attr("health"));
			useSkill(skill, health);
		});
	$("button.skill").on("touchend", function(e) {
		e.preventDefault();
	});

	$("button").removeClass("disabled");
	$("button[type='" + bannedtype + "']").addClass("disabled");
	$("button[skill='skill0']").addClass("disabled");
}

var buttonOff = function() {
	$("button").unbind("click touchstart");
	$("button").addClass("disabled");
}

$("html").on("touchend", function(e) {
	e.preventDefault();
});

var turnseconds = 10;

var useSkill = function(skill, health) {
	buttonOff();
	select.play();
	$.ajax({
		method: "POST",
		url: "/bossbattle/",
		data: { type: "attack", skill: skill, turn: turn },
	}).done(function(data) {
		if (data.type == "healthNotEnough") {
			dialog("그 기술을 쓰기엔 체력이 부족하다!", 1, function() {
				setTimeout(function(e) {
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOn();
					});
				}, 500);
			});
		} else if (data.type == "typeBanned") {
			dialog("그 기술의 속성은 봉인당했다!", 1, function() {
				setTimeout(function(e) {
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOn();
					});
				}, 500);
			});
		} else if (data.type == "attackSuccess") {
			turn = data.turn;
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
			console.log(ally_health);
			console.log(health);
			ally_health -= health;
			console.log(ally_health);
		}
	});
}

var monster;

var everyonesecond = function() {
	$.ajax({
		method: "POST",
		url: "/bossbattle/",
		data: { type: "everyonesecond", turn: turn },
	}).done(function(data) {
		if (turn != data.turn) {
			buttonOff();

			if (data.type == "win" || data.type == "lose") {
				window.clearInterval(id);
			}

			turn = data.turn;
			console.log(data);
			if (data.type == "gameover") {
				data.enemy_health = 0;
				data.monster = monster;
			}
			$(".character").effect("shake", {times:1, distance:5, direction: "left"}, 1000);
			$("#ally_health").css("width", ally_health + "%");
			ally_health = data.ally_health;
			dialog("전원 총 공격!", 1, function() {
				if (data.enemy_health < 0) {
					$("#enemy_health").css("width", "0%");
				} else {
					$("#enemy_health").css("width", (data.enemy_health * 100 / data.monsterhealth) + "%");
				}
				hit.play();
				$("#monster").effect("shake", {times:4, distance:10}, 500);
				var str = data.monster + "(은)는 " + (enemy_health - data.enemy_health) + "의 피해를 입었다.";
				monster = data.monster;
				enemy_health = data.enemy_health;

				if (data.type == "win") {
					dialog(str, 1, function() {
						battle.pause();
						win.play();
						dialog(data.monster + "을(를) 물리쳤다!", 1, function() {
							dialog(data.givenskill + " 스킬을 획득했다!", 1, function() {
								setTimeout(function() {
									window.location.replace("/map/");
								}, 2000);
							});
						});
					});
				} else if (data.type == "lose") {
					dialog(str, 1, function() {
						battle.pause();
						lose.play();
						dialog(data.monster + "에게 패배했다...", 1, function() {
							setTimeout(function() {
								window.location.replace("/map/");
							}, 2000);
						});
					});
				} else {
					dialog(str, 1, function() {
						if (data.bossskill == 0) {
							if (data.bosstype == "math")
								type = "수학";
							else if (data.bosstype == "phys")
								type = "물리";
							else if (data.bosstype == "chem")
								type = "화학";
							else if (data.bosstype == "life")
								type = "생물";
							else if (data.bosstype == "prog")
								type = "프밍";
							$(".battleground").removeClass("math phys chem life prog");
							$(".battleground").addClass(data.bosstype);
							dialog(data.monster + "(은)는 자신의 속성을 " + type + "(으)로 변경했다!", 1, function() {
								dialog("다음엔 무엇을 할까?", 1, function() {
									buttonOn();
								});
							});
						} else if (data.bossskill == 1) {
							$("#monster").effect("shake", {times:1, distance:5, direction: "right"}, 1000);
							dialog(data.monster + "의 공격!", 1, function() {
								$("#ally_health").css("width", data.ally_health + "%");
								hit.play();
								$(".character").effect("shake", {times:4, distance:10}, 500);
								dialog("모두 " + data.bossdamage + "의 피해를 입었다.", 1, function() {
									dialog("다음엔 무엇을 할까?", 1, function() {
										buttonOn();
									});
								});
							});
						} else if (data.bossskill == 2) {
							bannedtype = data.bannedtype;
							if (data.bannedtype == "math")
								type = "수학";
							else if (data.bannedtype == "phys")
								type = "물리";
							else if (data.bannedtype == "chem")
								type = "화학";
							else if (data.bannedtype == "life")
								type = "생물";
							else if (data.bannedtype == "prog")
								type = "프밍";
							dialog(data.monster + "(은)는 " + type + " 속성의 스킬을 봉인했다!", 1, function() {
								dialog("이제 " + type + " 속성의 스킬은 사용할 수 없다!", 1, function() {
									dialog("다음엔 무엇을 할까?", 1, function() {
										buttonOn();
									});
								});
							});
						} else if (data.bossskill == 3) {
							$("#monster").effect("shake", {times:1, distance:5, direction: "right"}, 1000);
							dialog(data.monster + "의 필살기!", 1, function() {
								$("#ally_health").css("width", data.ally_health + "%");
								hit.play();
								$(".character").effect("shake", {times: 4, distance: 10}, 500);
								dialog("남은 인원 중 절반의 체력이 0이 되었다!", 1, function() {
									dialog("다음엔 무엇을 할까?", 1, function() {
										buttonOn();
									});
								});
							});
						}
					});
				}
			});
		}
	});
}

var id;

$("button#gamestart").on("click touchstart", function() {
	$("div#loading").remove();
	$(".invisible").removeClass("invisible");
	id = setInterval(everyonesecond, 1000);
	initAudio();
	buttonOn();
});
