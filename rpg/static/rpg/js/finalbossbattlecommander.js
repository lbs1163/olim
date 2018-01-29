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

var dialog = function(string, i, callback) {
	$("#dialog").html(string);
	setTimeout(function(){callback();}, 1000);
}

var buttonOn = function() {
	$("button.skill").on("click touchstart", function(e) {
		e.preventDefault();
		var skill = $(this).attr("skill");
		useSkill(skill);
	});

	$("button").removeClass("disabled");

	$("button#help").off("click touchstart");
	$("button#help").on("click touchstart", function(e) {
		e.preventDefault();
		buttonOff();
		$.ajax({
			method: "POST",
			url: "/finalbossbattle/",
			data: { type: "help" },
		}).done(function(data) {
			console.log("help", data);
			if (data.type == "helpSuccess") {
				turn = data.turn;
				$("#dialog").html("턴이 끝나기를 기다리는 중...");
				id = setInterval(everyonesecond, 1000);
			} else if (data.type == "noFrusted") {
				dialog("좌절한 사람이 더 이상 없다!", 1, function() {
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOn();
					});
				});
			}
		});
	});
}

var buttonOff = function() {
	$("button").unbind("click touchstart");
	$("button").addClass("disabled");
}

var useSkill = function(skill) {
	buttonOff();
	$.ajax({
		method: "POST",
		url: "/finalbossbattle/",
		data: { type: "attack", skill: skill, turn: turn },
	}).done(function(data) {
		console.log("useSkill", data);
		if (data.type == "healthNotEnough") {
			dialog("그 기술을 쓰기엔 체력이 부족하다!", 1, function() {
				dialog("다음엔 무엇을 할까?", 1, function() {
					buttonOn();
				});
			});
		} else if (data.type == "frusted") {
			dialog("좌절하고 있어 기술을 쓸 수 없다!", 1, function() {
			});
			id = setInterval(everyonesecond, 1000);
		} else if (data.type == "attackSuccess") {
			turn = data.turn;
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
			id = setInterval(everyonesecond, 1000);
		} else if (data.type == "attackFailure") {
			turn = data.turn;
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
			id = setInterval(everyonesecond, 1000);
		}
	});
}

var frusted = false;

var everyonesecond = function() {
	$.ajax({
		method: "POST",
		url: "/finalbossbattle/",
		data: { type: "everyonesecond" }
	}).done(function(data) {
		console.log("everyonesecond", data);
		clearInterval(id);
		if (data.hope) {
			$(".invisible").removeClass("invisible");
		}
		if (data.frusted) {
			buttonOff();
			dialog("좌절하고 있어 기술을 쓸 수 없다!", 1, function() {});
			frusted = true;
			id = setInterval(everyonesecond, 1000);
		} else if (!data.frusted && frusted) {
			frusted = false;
			dialog(data.helper + "(이)가 도와줘서 좌절에서 벗어났다!", 1, function() {
				setTimeout(function() {
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOn();
					});
				}, 1000);
			});
		} else if (turn == data.turn || data.finalattack) {
			$("#ally_health").css("width", data.ally_health + "%");
			dialog("다음엔 무엇을 할까?", 1, function() {
				buttonOn();
			});
		}
		else {
			id = setInterval(everyonesecond, 1000);
		}
	});
}

buttonOn();
