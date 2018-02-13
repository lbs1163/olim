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

var battle = new Audio('/static/rpg/sound/finalbossbattle.mp3');
var hit = new Audio('/static/rpg/sound/hit.mp3');
var normaltalk = new Audio('/static/rpg/sound/talk.mp3');
var eviltalk = new Audio('/static/rpg/sound/eviltalk.wav');
var burn = new Audio('/static/rpg/sound/burning.wav');
var hope = new Audio('/static/rpg/sound/hope.mp3');
var ending = new Audio('/static/rpg/sound/ending.mp3');
var talk = normaltalk;

var beforedialog = $("#dialog1");
var afterdialog = $("#dialog2");
var dialognow = beforedialog;

var dialog = function(string, i, callback) {
	if (string.length == i - 1) {
		setTimeout(callback, 2000);
	} else {
		dialognow.html(string.substring(0, i));
		talk.currentTime = 0;
		talk.play();
		setTimeout(function() { dialog(string, i+1, callback) }, 70);
	}
}

var multiDialog = function(lines, i, callback) {
	if (lines.length <= i) {
		callback();
	} else {
		dialog(lines[i], 1, function() {
			multiDialog(lines, i+1, callback)
		});
	}
}

var beforelines = [
	"드디어 시상식이 다 끝났어!",
	"다들 새터는 잘 즐겼길 바라",
	"자 이제 시상식도 다 끝났으니...",
];

var changelines = [
	'"아직... 끝나지 않았다..."',
	'"강력한 숙주를 구하기 위해 돌아다녔지만..."',
	'"모두 하나같이 약해 빠졌더군..."',
	'"몬스터로 안된다면..."',
	'"이 세계의 관리자..."',
	'"네 녀석의 몸을 차지하겠다!"',
];

var enemy_line_num = 0;

var enemy_lines = [
	'"너희는 날 이길 수 없다..."',
	'"끝 없이 좌절해라..."',
	'"소용 없다..."',
	'"나는 절대 죽지 않는다..."',
];

var hope_line_num = 0;

var hope_lines = [
	'"무의미한 발버둥이다..."',
	'"그래봤자 시간만 끌 뿐..."',
	'"왜 좌절하지 않는 것인가..."',
	'"그만....."',
	'"이럴 리가 없다..."',
]

var attack_lines = [
	"포닉스가 불꽃을 내뿜는다!",
	"사람들이 좌절에 빠지고 있다...",
	"다음엔 무엇을 할까?",
];

var giveup_lines = [
	'"이제 단 한 명만 남았다..."',
	'"그만 포기해라..."',
];

var dontgiveup_lines = [
	'"아직 아니야....!"',
	'"간신히 잠깐 정신을 차릴 수 있었어"',
	'"마지막으로 너희들에게 스킬을 줄께...!"',
];

var finish_lines = [
	'"덕분에 빠져나올 수 있었어!"',
	'"이제 저 녀석을 끝장낼 시간이야!"',
	'"내 능력으로 턴과 체력을 무제한으로 할테니"',
	'"전부 한꺼번에 공격해!"',
	'"자 간다!"',
];

var ending_lines = [
	'"도와줘서 고마워!"',
	'"너희들 덕분에 바이러스를 완전히 물리칠 수 있었어"',
	'"모두들 이번처럼 서로 도와주기만 한다면"',
	'"앞으로도 어떤 일이든 해낼 수 있을꺼야"',
	'"나는 새터가 끝나면 더이상 볼 수 없을지도 모르지만"',
	'"너희에게 좋은 추억을 만들어줄 수 있어서 기뻤어"',
	'"다들 나와 함께 모험해줘서 고마워"',
	'"다들 안녕! 다음에 봐!"',
];

var beforeafter = function() {
	$("body").addClass("black");
	$("div#before").addClass("invisible");
	$("div#after").removeClass("invisible");
	battle.loop = true;
	battle.play();
	talk = normaltalk;
	dialognow = afterdialog;
}

var afterbefore = function() {
	$("body").removeClass("black");
	$("div#before").removeClass("invisible");
	$("div#after").addClass("invisible");
	dialognow = beforedialog;
}

var stateUpdate = function() {
	$.ajax({
		method: "POST",
		url: "/finalbossbattle/",
	}).done(function(data) {
		console.log(data);
		if (data.state == "before") {
			multiDialog(beforelines, 0, function() {
				talk = eviltalk;
				dialog('"크흐흐흐흐...."', 1, function() {
					talk = normaltalk;
					dialog('무...무슨 일이지!?', 1, function() {
						talk = eviltalk;
						multiDialog(changelines, 0, function() {
							$("div#before").addClass("invisible");
							$("body").addClass("black");
							$("div#change").removeClass("invisible");
							burn.play();
							setTimeout(function(){
								$("div#change").addClass("invisible");
								$.ajax({
									method: "POST",
									url: "/finalbossbattle/",
									data: {type: "ready"},
								}).done(function(data) {
									$("div#after").removeClass("invisible");
									battle.loop = true;
									battle.play();
									talk = normaltalk;
									dialognow = afterdialog;
									dialog("포닉스가 몬스터로 변했다!", 1, function() {
										dialog("다들 휴대폰을 꺼내자!", 1, function() {
											dialog("우리는 무엇을 할까?", 1, function() {
												$.ajax({
													method: "POST",
													url: "/finalbossbattle/",
													data: {type: "finalbattle"}
												}).done(function(data) {
													$.ajax({
														method: "POST",
														url: "/finalbossbattle/",
														data: {type: "ready"}
													}).done(function(data) {
														setTimeout(function(){
															stateUpdate();
														}, 5000);
													});
												});				
											});
										});
									});
								});
							}, 7000);
						});
					});
				});
			});
		} else if (data.state == "finalbattle") {
			$.ajax({
				method: "POST",
				url: "/finalbossbattle/",
				data: {type: "calculate"},
			}).done(function(data) {
				console.log(data);
				if (data.type == "ongoing" || data.type == "allfrusted") {
					talk = normaltalk;
					dialog("전원 총 공격!", 1, function() {
						$("#enemy_health").css("width", (data.enemy_health * 100 / data.monsterhealth) + "%");
						hit.play();
						$("#monster").effect("shake", {times: 4, distance: 10}, 500);
						var str = "포닉스는 " + (enemy_health - data.enemy_health) + "의 피해를 입었다.";
						dialog(str, 1, function(){
							enemy_health = data.enemy_health;
							talk = eviltalk;
							dialog(enemy_lines[enemy_line_num], 1, function(){
								enemy_line_num += 1;
								if (enemy_line_num >= enemy_lines.length) {
									enemy_line_num = 0;
								}
								talk = normaltalk;
								$("#monster").effect("shake", {times:1, distance:100, direction: "right"}, 1000);
								attack_lines[1] = data.frustednumber + "명이 좌절에 빠져 아무것도 못하고 있다...";
								if (data.type == "allfrusted") {
									dialog(attack_lines[0], 1, function() {
										dialog(attack_lines[1], 1, function() {
											stateUpdate();
										});
									});
								} else {
									multiDialog(attack_lines, 0, function() {
										$.ajax({
											method: "POST",
											url: "/finalbossbattle/",
											data: {type: "ready"},
										}).done(function(data) {
											setTimeout(function(){
												stateUpdate();
											}, 5000);
										});
									});
								}
							});
						});
					});
				}
			});
		} else if (data.state == "allfrusted") {
			battle.pause();
			talk = eviltalk;
			multiDialog(giveup_lines, 0, function() {
				talk = normaltalk;
				$("#monster img").attr("src", "/static/rpg/image/normal_phoenix.png");
				$("#monster").css("padding-top", "80px");
				$("#monster img").addClass("non-pixel");
				multiDialog(dontgiveup_lines, 0, function() {
					$.ajax({
						method: "POST",
						url: "/finalbossbattle/",
						data: {type: "helpeachother"},
					}).done(function(data) {
							hope.loop = true;
							hope.play();
							dialog("도와주기 스킬을 얻었다!", 1, function() {
								dialog("반격할 차례다.", 1, function() {
									$("#monster").css("padding-top", "0");
									$("#monster img").attr("src", "/static/rpg/image/phoenix.gif");
									$("#monster img").removeClass("non-pixel");
									$.ajax({
										method: 'POST',
										url: '/finalbossbattle/',
										data: {type: 'ready'},
									}).done(function(data) {
										setTimeout(function() {
										stateUpdate();
									}, 5000);
								});
							});
						});
					});
				});
			});
		} else if (data.state == "helpeachother") {
			$.ajax({
				method: "POST",
				url: "/finalbossbattle/",
				data: {type: "calculate"},
			}).done(function(data) {
				if (data.type == "ongoing" || data.type == "helpphoenix") {
					talk = normaltalk;
					dialog("서로가 서로를 돕고 있다!", 1, function() {
						talk = eviltalk;
						dialog(hope_lines[hope_line_num], 1, function(){
							hope_line_num += 1;
							if (hope_line_num >= hope_lines.length) {
								hope_line_num = 0;
							}
							talk = normaltalk;
							if (data.frustednumber == undefined) {
								data.frustednumber = 0;
							}
							var str2 = "도와줄 사람이 " + data.frustednumber + "명 남았다!";

							if (data.type == "helpphoenix") {
								dialog(str2, 1, function() {
									stateUpdate();
								});
							} else {
								dialog(str2, 1, function() {
									dialog("다음엔 무엇을 할까?", 1, function() {
										$.ajax({
											method: "POST",
											url: "/finalbossbattle/",
											data: {type: "ready"},
										}).done(function(data) {
											setTimeout(function(){
												stateUpdate();
											}, 5000);
										});
									});
								});
							}
						});
					});
				}
			});
		} else if (data.state == "helpphoenix") {
			talk = eviltalk;
			dialog("큭....크윽......", 1, function() {
				talk = normaltalk;
				dialog("지금이다! 약해졌을 때 포닉스를 도와야 한다!", 1, function() {
					dialog("다들 도와주기를 사용하자!", 1, function() {
						$.ajax({
							method: "POST",
							url: "/finalbossbattle/",
							data: {type: "ready"},
						}).done(function(data) {
							setTimeout(function() {
								$("#monster img").attr("src", "/static/rpg/image/normal_phoenix.png");
								$("#monster").css("padding-top", "80px");
								$("#monster img").addClass("non-pixel");
								dialog("포닉스가 몬스터와 분리되었다!", 1, function() {
									multiDialog(finish_lines, 0, function() {
										$("#monster img").attr("src", "/static/rpg/image/phoenix.gif");
										$("#monster").css("padding-top", "0");
										$("#monster img").removeClass("non-pixel");
										$.ajax({
											method: "POST",
											url: "/finalbossbattle/",
											data: {type: "finalattack"},
										}).done(function(data) {
											$.ajax({
												method: "POST",
												url: "/finalbossbattle/",
												data: {type: "ready"},
											}).done(function(data) {
												stateUpdate();
											});
										});	
									});
								});
							}, 10000);
						});
					});
				});
			});
		} else if (data.state == "finalattack") {
			id = setInterval(getDamage, 100);
		} else if (data.state == "ending") {
			multiDialog(ending_lines, 0, function() {
				$("html").fadeOut(5000, function() {
					window.location.replace("/ending/");
				});
			});
		}
	});
}

var id;

var getDamage = function() {
	clearInterval(id);
	$.ajax({
		method: "POST",
		url: "/finalbossbattle/",
		data: {type: "getDamage"},
	}).done(function(data) {
		if (enemy_health > data.enemy_health) {
			hit.currentTime = 0;
			hit.play();
			$("#enemy_health").css("width", (data.enemy_health * 100 / data.monsterhealth) + "%");
			dialognow.html("포닉스의 잔재는 " + (enemy_health - data.enemy_health) + "만큼의 데미지를 입었다!");
			enemy_health = data.enemy_health;
		}
		if (enemy_health <= 0) {
			hope.pause();
			$("html").fadeOut(10000, function() {
				$.ajax({
					method: "POST",
					url: "/finalbossbattle/",
					data: {type: "ending"},
				}).done(function(data) {
					afterbefore();
					$("html").fadeIn(1, function() {
						ending.play();
						stateUpdate();
					});
				});
			});
		} else {
			id = setInterval(getDamage, 100);
		}
	});
}

if (state == "before") {
	stateUpdate();
} else if (state == "finalbattle") {
	beforeafter();
	stateUpdate();
} else if (state == "allfrusted") {
	beforeafter();
	stateUpdate();
} else if (state == "helpeachother") {
	beforeafter();
	battle.pause();
	hope.loop = true;
	hope.play();
	stateUpdate();
} else if (state == "helpphoenix") {
	beforeafter();
	battle.pause();
	hope.loop = true;
	hope.play();
	stateUpdate();
} else if (state == "finalattack") {
	beforeafter();
	battle.pause();
	hope.loop = true;
	hope.play();
	stateUpdate();
} else if (state == "ending") {
	afterbefore();
	$("html").fadeIn(1, function() {
		ending.play();
		stateUpdate();
	});
}
