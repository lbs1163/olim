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

var input = $("input").first();

$("button#submit").on("click touchstart", function(e) {
	e.preventDefault();
	var value = input.val();
	
	$.ajax({
		method: "POST",
		url: "/code/",
		data: { code: value },
	}).done(function(data) {
		if (data.type == "doesNotExist") {
			alert("없는 코드입니다 ㅠㅠ");
			location.reload();
		} else if (data.type == "success") {
			$("#box").fadeOut(3000, function() {
				$("#box").attr("src", data.img);
				$("#box").fadeIn(1, function(){});
				setInterval(function() {
					alert("축하합니다! " + data.name + "을(를) 얻었습니다!");
					location.reload();
				}, 1000);
			});
		} else if (data.type == "alreadyHave") {
			alert(data.name + "(은)는 이미 있는 의상입니다");
			location.reload();
		}
	});
});
