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

var display = function(data) {
	if (data.numOfGroup == data.numOfReady && data.numOfGoup >= 5) {
		location.reload();
	}
	$("span#numOfGroup").html(data.numOfGroup);
	$("span#numOfReady").html(data.numOfReady);
};

var refresh = function() {
	$.ajax({
		url: "/bossbattle/",
		method: "POST",
		data: { "type": "refresh" },
	}).done(function(data) {
		display(data);
	});
};

var ready = function(e) {
	e.preventDefault();
	
	$.ajax({
		url: "/bossbattle/",
		method: "POST",
		data: { "type": "ready" },
	}).done(function(data) {
		display(data);
		$("button#ready").off("click touchstart");
		$("button#ready").on("click touchstart", unready);
		$("button#ready").html("준비 해제");
	});
};

var unready = function(e) {
	e.preventDefault();

	$.ajax({
		url: "/bossbattle/",
		method: "POST",
		data: { "type": "unready" },
	}).done(function(data) {
		display(data);
		$("button#ready").off("click touchstart");
		$("button#ready").on("click touchstart", ready);
		$("button#ready").html("준비 완료");
	});
};

var first = $("button#ready").html();

if (first == "준비 완료") {
	$("button#ready").on("click touchstart", ready);
} else if (first == "준비 해제") {
	$("button#ready").on("click touchstart", unready);
}

refresh();
setInterval(refresh, 1000);
