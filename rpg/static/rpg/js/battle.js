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

var battle = new Audio('/static/rpg/sound/battle.mp3');
var select = new Audio('/static/rpg/sound/select.mp3');
var hit = new Audio('/static/rpg/sound/hit.mp3');
var destroy = new Audio('/static/rpg/sound/destroy.mp3');
var win = new Audio('/static/rpg/sound/win.mp3');
var lose = new Audio('/static/rpg/sound/lose.mp3');
var talk = new Audio('/static/rpg/sound/talk.mp3');

battle.addEventListener('ended', function() {
	this.currentTime = 0;
	this.play();
}, false);

battle.play();

var dialog = function(string, i, callback) {
	if (string.length == i - 1) {
		callback();
	} else {
		$("#dialog").html(string.substring(0, i));
		talk.load();
		talk.play();
		setTimeout(function() { dialog(string, i+1, callback) }, 70);
	}
}

var buttonOn = function() {
	$("button.skill").on("click touchstart", function(e) {
		var skillid = $(this).attr("skillid");
		useSkill(skillid);
	});
	$("button.skill").on("touchend", function(e) {
		e.preventDefault();
	});

	$("button#runaway").on("click touchstart", function(e) {
		$.ajax({
			method: "POST",
			url: "/battle/",
			data: {"type": "runaway"}
		}).done(function(data){
			if (data.type == "runawaySuccess") {
				buttonOff();
				battle.pause();
				lose.play();
				dialog("무사히 도망쳤다!", 1, function() {
					$("html").on("click touchstart", function(e) {
						window.location.replace("/map/");
					});
				});
			} else {
				location.reload();
			}
		});
	});
	$("button#runaway").on("touchend", function(e) {
		e.preventDefault();
	});

	$("button").removeClass("disabled");
}

var buttonOff = function() {
	$("button").unbind("click touchstart");
	$("button").addClass("disabled");
}

var dialogStart = function(data) {
	var str1 = "체력 " + data.health_used + "(을)를 사용하여 " + data.skill + " 공격!";
	if (data.health_used < 0) {
		$("#ally_health").html("체력: " + data.ally_health);
		str1 = "체력을 " + (-data.health_used) + "만큼 회복!";
		dialog(str1, 1, function() {
			$("html").on("click touchstart", function(e) {
				$("html").off("click touchstart");
				var str2 = "다음엔 무엇을 할까?";
				dialog(str2, 1, function() {
					buttonOn();
				});
			});
		});
		return;
	}
	$("#ally_health").html("체력: " + data.ally_health);
	$(".character").effect("shake", {times:1, distance: 10, direction: "left"}, 1000);
	dialog(str1, 1, function() {
		$("html").on("click touchstart", function(e) {
			$("html").off("click touchstart");
			var str2 = data.monster + "(은)는 " + data.damage + "의 피해를 입었다.";
			if (data.double) {
				str2 = "효과가 굉장했다! " + str2;
			}
			hit.play();
			$("#enemy_health").html("체력: " + data.enemy_health);
			$("#monster").effect("shake", {times:4, distance: 10}, 500);
			dialog(str2, 1, function() {
				$("html").on("click touchstart", function(e) {
					$("html").off("click touchstart");
					dialog(data.dialog, 1, function() {
						$("html").on("click touchstart", function(e) {
							$("html").off("click touchstart");
							if(data.type == "battleWin") {
								$("p#enemy_health").remove();
								$("#monster").effect("puff");
								battle.pause();
								win.play();
								dialog(data.monster + "(을)를 이해했다!", 1, function() {
									$("html").on("click touchstart", function(e){
										$("html").off("click touchstart");
										dialog(data.exp_type + " 지식을 " + data.exp + " 만큼 획득했다!", 1, function() {
											$("html").on("click touchstart", function(e) {
												$("html").off("click touchstart");
												if (data.skillname != false) {
													dialog(data.skillname + " 스킬을 획득했다!", 1, function() {
														$("html").on("click touchstart", function(e){
															$("html").off("click touchstart");
															window.location.replace("/map/");
														});
													});
												} else {
													$("html").on("click touchstart", function(e){
														$("html").off("click touchstart");
														window.location.replace("/map/");
													});
												}
											});
										});
									});
								});
							} else {
								dialog("다음엔 무엇을 할까?", 1, function() {
									buttonOn();
								});
							}
						});
					});
				});
			});
		});
	});
}

$("html").on("touchend", function(e) {
	e.preventDefault();
});

var useSkill = function(skillid) {
	buttonOff();
	select.play();
	$.ajax({
		method: "POST",
		url: "/battle/",
		data: { skillid: skillid },
	}).done(function(data) {
		if (data.type && data.type == "healthNotEnough") {
			dialog("그 기술을 쓰기엔 체력이 부족하다!", 1, function() {
				$("html").on("click touchstart", function(e) {
					$("html").off("click touchstart");
					dialog("다음엔 무엇을 할까?", 1, function() {
						buttonOn();
					});
				});
			});
		} else {
			dialogStart(data);
		}
	});
}

buttonOn();
