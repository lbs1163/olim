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

	if (left && right) {
		var left_skill = $("#skill-left").children().first().attr("skillid");
		var right_skill = $("#skill-right").children().first().attr("skillid");

		$.ajax({
			method: "POST",
			url: "/combination/",
			data: { real: false, left: left_skill, right: right_skill },
		}).done(function(data) {
			if (data.type == "combinationAlreadyFailed") {
				$("#skill-combined").children().first().html("조합 결과 없음");
			} else if (data.type == "combinationNotDiscoveredYet") {
				$("#skill-combined").children().first().html("조합 해보지 않음");
			} else if (data.type == "combinationPreview") {
				$("#skill-combined").children().first().html(data.newSkill.name);
			}
		});
	}
}

$("#skill-left").bind("click", function(e) {
	if (left == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", itemEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		left = false;
		$("#skill-combined").children().first().html("?????");
	}
});

$("#skill-right").bind("click", function(e) {
	if (right == true) {
		var temp = $("<div class='col s12 m6 l4 xl3'>").append($(this).children().first());
		$(this).children().first().remove();
		$(this).append('<button class="skill btn">스킬을 넣어주세요</button>');
		temp.children().first().bind("click", itemEventHandler)
		$("#" + temp.children().first().attr("type")).prepend(temp);
		right = false;
		$("#skill-combined").children().first().html("?????");
	}
});

$("button#submit").bind("click", function(e) {
	var combined = $("#skill-combined").children().first().attr("combined");
	var left_skill = $("#skill-left").children().first().attr("skillid");
	var right_skill = $("#skill-right").children().first().attr("skillid");

	if (combined) {
		$.ajax({
			method: "POST",
			url: "/combination/",
			data: { real: true, left: left_skill, right: right_skill },
		}).done(function(data) {
			if (data.type == "combinationAlreadyFailed") {
				alert("이미 실패한 조합입니다!");
			} else if (data.type == "combinationDoesNotExist") {
				$("#skill-combined").children().first().animate({
					opacity: 100
				}, 1000, function() {
					alert("조합에 실패하였습니다 ㅠㅠ");
					location.reload();
				});
			} else if (data.type == "combinationSuccess") {
				if (data.firstDiscovery) {
					$("#skill-combined").children().first().animate({
						opacity: 100
					}, 1000, function() {
						alert(data.newSkill.name + " 발견! 조합에 성공하였습니다!");
						location.reload();
					});
				}
				else {
					location.reload();
				}
			}
		});
	}
});

$("div#select button.skill").bind("click", itemEventHandler);
