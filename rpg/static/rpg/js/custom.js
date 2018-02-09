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

var hair = $(".character img:nth-child(2)");
var clothes = $(".character img:nth-child(3)");
var eye = $(".character img:nth-child(4)");
var y;

var hairhaveid;
var clotheshaveid;
var eyehaveid;

$("img").on("click touchstart", function(e) {
	y = e.pageY;
});

$("#hair img").on("click touchend", function(e) {
	var newy = e.pageY;
	if (Math.abs(newy - y) < 5) {
		var src = $(this).attr("src");
		hair.attr("src", src);
		hairhaveid = $(this).attr("haveid");
	}
});

$("#clothes img").on("click touchend", function(e) {
	var newy = e.pageY;
	if (Math.abs(newy - y) < 5) {
		var src = $(this).attr("src");
		clothes.attr("src", src);
		clotheshaveid = $(this).attr("haveid");
	}
});

$("#eye img").on("click touchend", function(e) {
	var newy = e.pageY;
	if (Math.abs(newy - y) < 5) {
		var src = $(this).attr("src");
		eye.attr("src", src);
		eyehaveid = $(this).attr("haveid");
	}
});

$("#submit").on("click touchstart", function(e) {
	e.preventDefault();
	$.ajax({
		method: "POST",
		url: "/custom/",
		data: { hairhaveid: hairhaveid, clotheshaveid: clotheshaveid, eyehaveid: eyehaveid },
	}).done(function(data) {
		location.reload();
	});
});
