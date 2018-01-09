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
	$("button").on("click", function() {
		var skillid = $(this).attr("skillid");
		useSkill(skillid);
	});
}

var buttonOff = function() {
	$("button").off();
}

var dialogStart = function(data) {
	var str1 = "체력 " + data.health_used + "(을)를 사용하여 " + data.skill + " 공격!"
	$("#dialog").html(str1);
	$("#ally_health").html("체력: " + data.ally_health);
	$("#dialog").on("click", function() {
		var str2 = data.monster + "(은)는 " + data.damage + "만큼 이해당했다.";
		$("#dialog").html(str2);
		$("#enemy_health").html("이해도: " + data.enemy_health);
		$("#dialog").off();
		$("#dialog").on("click", function() {
			if(data.battle_win) {
				$("#dialog").html(data.monster + "(을)를 이해했다!");
				$("#dialog").off();
				$("#dialog").on("click", function(){ window.location.replace("/"); });
			} else {
				$("#dialog").html(data.dialog);
				$("#dialog").off();
				buttonOn();
			}
		})
	})
}

var useSkill = function(skillid) {
	$.ajax({
		method: "POST",
		url: "/battle/",
		data: { skillid: skillid },
	}).done(function(data) {
		buttonOff();
		dialogStart(data);
	});
}

buttonOn();
