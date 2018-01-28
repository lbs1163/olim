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

var skillEventHandler = function(e) {
	e.preventDefault();

	if (skill1 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill1").children().remove();
		$("#skill1").append(temp);
		$("#skill1").children().first().bind("click touchstart", skill1handler);
		skill1 = true;
	} else if (skill2 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill2").children().remove();
		$("#skill2").append(temp);
		$("#skill2").children().first().bind("click touchstart", skill2handler);
		skill2 = true;
	} else if (skill3 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill3").children().remove();
		$("#skill3").children().first().bind("click touchstart", skill3handler);
		$("#skill3").append(temp);
		skill3 = true;
	} else if (skill4 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill4").children().remove();
		$("#skill4").children().first().bind("click touchstart", skill4handler);
		$("#skill4").append(temp);
		skill4 = true;
	}
}

$("div#select button.skill").bind("click touchstart", skillEventHandler);
$("div#select button.skill.cannot").unbind("click touchstart");
$("div#select button.skill.cannot").bind("click touchstart", function(e) {
	e.preventDefault();
	skilllimit = $(this).attr("skilllimit");
	stat = $(this).attr("stat");
	type = $(this).attr("koreantype");
	alert(type + " 스탯이 부족합니다! 필요 스탯: " + skilllimit + " , 현재 스탯: " + stat);
});

var skill1handler = function(e) {
	e.preventDefault();
	if (skill1 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).clone());
		$(this).parent().append('<button class="skill btn"></button>');
		$(this).remove();
		temp.children().first().bind("click touchstart", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill1 = false;
	}
}

var skill2handler = function(e) {
	e.preventDefault();
	if (skill2 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).clone());
		$(this).parent().append('<button class="skill btn"></button>');
		$(this).remove();
		temp.children().first().bind("click touchstart", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill2 = false;
	}
}

var skill3handler = function(e) {
	e.preventDefault();
	if (skill3 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).clone());
		$(this).parent().append('<button class="skill btn"></button>');
		$(this).remove();
		temp.children().first().bind("click touchstart", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill3 = false;
	}
}

var skill4handler = function(e) {
	e.preventDefault();
	if (skill4 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).clone());
		$(this).parent().append('<button class="skill btn"></button>');
		$(this).remove();
		temp.children().first().bind("click touchstart", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill4 = false;
	}
}

$("#skill1").children().first().bind("click touchstart", skill1handler);
$("#skill2").children().first().bind("click touchstart", skill2handler);
$("#skill3").children().first().bind("click touchstart", skill3handler);
$("#skill4").children().first().bind("click touchstart", skill4handler);

$("button#submit").bind("click touchstart", function(e) {
	e.preventDefault();
	var skill1 = $("#skill1").children().first().attr("skillid");
	var skill2 = $("#skill2").children().first().attr("skillid");
	var skill3 = $("#skill3").children().first().attr("skillid");
	var skill4 = $("#skill4").children().first().attr("skillid");

	$.ajax({
		method: "POST",
		url: "/selectskill/",
		data: { skill1: skill1, skill2: skill2, skill3: skill3, skill4: skill4 },
	}).done(function(data) {
		location.reload();
	});
});
