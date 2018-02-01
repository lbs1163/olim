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
	$('button[skill="skill0"]').addClass("disabled");

	$("button#help").off("click touchstart");
	$("button#help").on("click touchstart", function(e) {
		e.preventDefault();
		buttonOff();
		$.ajax({
			method: "POST",
			url: "/finalbossbattle/",
			data: { type: "help" },
		}).done(function(data) {
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
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
		data: { type: "attack", skill: skill },
	}).done(function(data) {
		console.log("useSkill", data);
		if (data.type == "healthNotEnough") {
			dialog("그 기술을 쓰기엔 체력이 부족하다!", 1, function() {
				dialog("다음엔 무엇을 할까?", 1, function() {
					buttonOn();
				});
			});
		} else if (data.type == "frusted") {
			$("#dialog").html("좌절하고 있어 기술을 쓸 수 없다!");
		} else if (data.type == "time2help") {
			$("#dialog").html("친구들을 도와야 한다!");
		} else if (data.type == "attackSuccess") {
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
		} else if (data.type == "attackFailure") {
			$("#dialog").html("턴이 끝나기를 기다리는 중...");
		}
	});
}

var everyonesecond = function() {
	clearInterval(id);
	$.ajax({
		method: "POST",
		url: "/finalbossbattle/",
		data: { type: "everyonesecond" }
	}).done(function(data) {
		console.log("everyonesecond", data);
		$("#ally_health").css("width", data.ally_health + "%");
		if (data.state == "before") {
			id = setInterval(everyonesecond, 1000);
		} else if (data.state == "finalbattle") {
			$("#whole").removeClass("invisible");
			if (data.frusted) {
				buttonOff();
				dialog("좌절하고 있어 기술을 쓸 수 없다!", 1, function() {});
				frusted = true;
				id = setInterval(everyonesecond, 1000);
			} else if (data.ready && !data.frusted) {
				dialog("다음엔 무엇을 할까?", 1, function() {
					buttonOff();
					buttonOn();
					id = setInterval(everyonesecond, 1000);
				});
			} else {
				$("#dialog").html("턴이 끝나기를 기다리는 중...");
				buttonOff();
				id = setInterval(everyonesecond, 1000);
			}
		} else if (data.state == "allfrusted") {
			buttonOff();
			id = setInterval(everyonesecond, 1000);
		} else if (data.state == "helpeachother") {
			$("#help").parent().removeClass("invisible");
			if (data.frusted) {
				buttonOff();
				dialog("좌절하고 있어 기술을 쓸 수 없다!", 1, function() {});
				id = setInterval(everyonesecond, 1000);
			} else if (data.ready && !data.frusted) {
				if (frusted) {
					console.log("sasdfasdf");
					frusted = false;
					dialog(data.helper + "(이)가 도와줘서 좌절에서 벗어났다!", 1, function() {
						setTimeout(function() {
							dialog("다음엔 무엇을 할까?", 1, function() {
								buttonOff();
								buttonOn();
								$("#skills button").addClass("disabled");
								id = setInterval(everyonesecond, 1000);
							});
						}, 2000);
					});
				} else {
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOff();
						buttonOn();
						$("#skills button").addClass("disabled");
						id = setInterval(everyonesecond, 1000);
					});
				}
			} else {
				buttonOff();
				$("#dialog").html("턴이 끝나기를 기다리는 중...");
				id = setInterval(everyonesecond, 1000);
			}
		} else if (data.state == "helpphoenix") {
			if (data.ready) {
				buttonOff();
				buttonOn();
				$("#skills button").addClass("disabled");
				id = setInterval(everyonesecond, 1000);
			} else {
				buttonOff();
				$("#dialog").html("턴이 끝나기를 기다리는 중...");
				id = setInterval(everyonesecond, 1000);
			}
		} else if (data.state == "finalattack") {
			buttonOff();
			buttonOn();
			$("#help").addClass("disabled");
			id = setInterval(everyonesecond, 1000);
		} else if (data.state == "ending") {
			$("#whole").addClass("invisible");
		}
	});
}

if (state == "before") {
} else if (state == "finalbattle") {
	$("#whole").removeClass("invisible");
	buttonOff();
	buttonOn();
} else if (state == "allfrusted") {
	$("#whole").removeClass("invisible");
	buttonOff();
} else if (state == "helpeachother") {
	$("#whole").removeClass("invisible");
	buttonOff();
	buttonOn();
	$("#help").parent().removeClass("invisible");
	$("#skills button").addClass("disabled");
} else if (state == "helpphoenix") {
	$("#whole").removeClass("invisible");
	buttonOff();
	buttonOn();
	$("#help").parent().removeClass("invisible");
	$("#skills button").addClass("disabled");
} else if (state == "finalattack") {
	$("#whole").removeClass("invisible");
	buttonOff();
	buttonOn();
	$("#help").parent().removeClass("invisible");
	$("#help").addClass("disabled");
} else if (state == "ending") {
	$("#whole").addClass("invisible");
}

id = setInterval(everyonesecond, 1000);
