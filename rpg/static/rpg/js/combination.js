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

var left = false, right = false;

var itemEventHandler = function(e) {
	if (left == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill-left").children().remove();
		$("#skill-left").append(temp);
		left = true;
	}
	else if (right == false) {
		var temp = $(this);
		$(this).parent().remove();
		$("#skill-right").children().remove();
		$("#skill-right").append(temp);
		right = true;
	}
}

$("#skill-left").bind("click", function(e) {
	if (left == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn" id="skill-right">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", itemEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		left = false;
	}
});

$("#skill-right").bind("click", function(e) {
	if (right == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn" id="skill-right">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", itemEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		left = false;
	}
});

$("button.skill").bind("click", itemEventHandler);
