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

var buttonOn = function() {
	$("button.skill").on("click", function() {
		var skillid = $(this).attr("skillid");
		useSkill(skillid);
	});

	$("button#runaway").on("click", function() {
		$.ajax({
			method: "POST",
			url: "/battle/",
			data: {"type": "runaway"}
		}).done(function(data){
			if (data.type == "runawaySuccess") {
				buttonOff();
				$("#dialog").html("무사히 도망쳤다!");
				$("html").on("click", function() {
					window.location.replace("/");
				});
			} else {
				location.reload();
			}
		});
	});

	$("button").removeClass("disabled");
}

var buttonOff = function() {
	$("button").unbind("click");
	$("button").addClass("disabled");
}

var dialogStart = function(data) {
	var str1 = "체력 " + data.health_used + "(을)를 사용하여 " + data.skill + " 공격!"
	$("#dialog").html(str1);
	$("#ally_health").html("체력: " + data.ally_health);
	$("html").on("click", function() {
		var str2 = data.monster + "(은)는 " + data.damage + "의 피해를 입었다.";
		$("#dialog").html(str2);
		$("#enemy_health").html("체력: " + data.enemy_health);
		$("html").off();
		$("html").on("click", function() {
			$("#dialog").html(data.dialog);
			$("html").off();
			$("html").on("click", function() {
				if(data.battle_win) {
					$("#dialog").html(data.monster + "(을)를 이해했다!");
					$("html").off();
					$("html").on("click", function(){
						$("#dialog").html(data.skillname + " 스킬을 획득했다!");
						$("html").off();
						$("html").on("click", function(){ window.location.replace("/"); });
					});
				} else {
					$("#dialog").html("다음엔 무엇을 할까?");
					$("html").off();
					buttonOn();
				}
			});
		})
	})
}

var useSkill = function(skillid) {
	buttonOff();
	$.ajax({
		method: "POST",
		url: "/battle/",
		data: { skillid: skillid },
	}).done(function(data) {
		if (data.type && data.type == "healthNotEnough") {
			$("#dialog").html("그 기술을 쓰기엔 체력이 부족하다!");
			$("html").on("click", function(e) {
				$("#dialog").html("다음엔 무엇을 할까?");
				$("html").off();
				buttonOn();
			});
		} else {
			dialogStart(data);
		}
	});
}

buttonOn();
