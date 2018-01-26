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

var bossbattle = new Audio('/static/rpg/sound/battle.mp3');
var select = new Audio('/static/rpg/sound/select.mp3');
var hit = new Audio('/static/rpg/sound/hit.mp3');
var destroy = new Audio('/static/rpg/sound/destroy.mp3');
var win = new Audio('/static/rpg/sound/win.mp3');
var lose = new Audio('/static/rpg/sound/lose.mp3');
var talk = new Audio('/static/rpg/sound/talk.mp3');

bossbattle.addEventListener('ended', function() {
	this.currentTime = 0;
	this.play();
}, false);

bossbattle.play();

var dialog = function(string, i, callback) {
	if (string.length == i - 1) {
		callback();
	} else {
		$("#dialog").html(string.substring(0, i));
		talk.play();
		setTimeout(function() { dialog(string, i+1, callback) }, 70);
	}
}

var buttonOn = function() {
	$("button.skill").off("click touchstart")
		$("button.skill").on("click touchstart", function(e) {
			var skill = $(this).attr("skill");
			useSkill(skill);
		});
	$("button.skill").on("touchend", function(e) {
		e.preventDefault();
	});

	$("button").removeClass("disabled");
}

var buttonOff = function() {
	$("button").unbind("click touchstart");
	$("button").addClass("disabled");
}

$("html").on("touchend", function(e) {
	e.preventDefault();
});

var turn = 0;
var turnseconds = 10;

var useSkill = function(skill) {
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
			turn = data.turn;
			console.log(data);
			if (data.type == "gameover") {
				data.enemy_health = 0;
				data.monster = monster;
			}
			$(".character").effect("shake", {times:1, distance:5, direction: "left"}, 1000);
			dialog("전원 총 공격!", 1, function() {
				setTimeout(function() {
					$("#ally_health").html("내 체력: " + data.ally_health);
					$("#enemy_health").html("체력: " + data.enemy_health);
					hit.play();
					$("#monster").effect("shake", {times:4, distance:10}, 500);
					var str = data.monster + "(은)는 " + (enemy_health - data.enemy_health) + "의 피해를 입었다.";
					monster = data.monster;
					enemy_health = data.enemy_health;

					if (enemy_health == 0) {
						dialog(str, 1, function() {
							setTimeout(function() {
								bossbattle.pause();
								win.play();
								dialog(data.monster + "을(를) 물리쳤다!", 1, function() {
									setTimeout(function() {
										window.location.replace("/");
									}, 1000);
								});
							}, 1000);
						});
					} else {
						dialog(str, 1, function() {
							setTimeout(function() {
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
										setTimeout(function() {
											dialog("다음엔 무엇을 할까?", 1, function() {
												buttonOn();
											});
										});
									});
								}
							}, 1000);
						});
					}
				}, 1000);
			});
		}
	});
}

	setInterval(everyonesecond, 1000);
	buttonOn();
