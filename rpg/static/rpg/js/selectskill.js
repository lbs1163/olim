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

var skill1 = false;
var skill2 = false;
var skill3 = false;
var skill4 = false;

var skillEventHandler = function(e) {
	if (skill1 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill1").children().remove();
		$("#skill1").append(temp);
		skill1 = true;
	} else if (skill2 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill2").children().remove();
		$("#skill2").append(temp);
		skill2 = true;
	} else if (skill3 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill3").children().remove();
		$("#skill3").append(temp);
		skill3 = true;
	} else if (skill4 == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill4").children().remove();
		$("#skill4").append(temp);
		skill4 = true;
	}
}

$("div#select button.skill").bind("click", skillEventHandler);

$("#skill1").bind("click", function(e) {
	if (skill1 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill1 = false;
	}
});

$("#skill2").bind("click", function(e) {
	if (skill2 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill2 = false;
	}
});

$("#skill3").bind("click", function(e) {
	if (skill3 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill3 = false;
	}
});

$("#skill4").bind("click", function(e) {
	if (skill4 == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", skillEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		skill4 = false;
	}
});

$("button#submit").bind("click", function(e) {
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
