var ending = new Audio('/static/rpg/sound/credit.mp3');

$("#title").hide();
$("#video").hide();
$("#design").hide();
$("#stage").hide();
$("#insol").hide();
$("#specialthanksto").hide();
$("#insolja1").hide();
$("#insolja2").hide();
$("#insolja3").hide();
$("#new").hide();
$("#missiontour").hide();
$("#theme").hide();
$("#heads").hide();
$("#end").hide();

var start = function() {
	ending.play();
	$("#title").show("fade", 2600, function() {
		$("#title").hide();
		$("#video").effect("slide", {direction: "left", mode: 'show'}, 1000, function() {
			setTimeout(function() {
				$("#video").effect("slide", {direction: "right", mode: "hide"}, 1000, function() {
					$("#design").effect("slide", {direction: "up", mode: "show"}, 1000, function() {
						setTimeout(function() {
							$("#design").effect("slide", {direction: "down", mode: "hide"}, 1000, function() {
								$("#stage").effect("slide", {direction: "right", mode: "show"}, 1000, function() {
									setTimeout(function() {
										$("#stage").effect("slide", {direction: "left", mode: "hide"}, 1000, function() {
											$("#insol").effect("slide", {direction: "down", mode: "show"}, 1000, function() {
												setTimeout(function() {
													$("#insol").effect("slide", {direction: "up", mode: "hide"}, 1000, function() {
														specialthanksto();
													});
												}, 8707);
											});
										});
									}, 8707);
								});
							});
						}, 8707);
					});
				});
			}, 8707);
		});
	});
}

var specialthanksto = function() {
	$("#specialthanksto").effect("fade", {mode: "show"}, 1000, function() {
		setTimeout(function() {
			$("#specialthanksto").effect("fade", {mode: "hide"}, 1000, function() {
				$("#insolja1").effect("fade", {mode: "show"}, 1000, function() {
					setTimeout(function() {
						$("#insolja1").effect("fade", {mode: "hide"}, 1000, function() {
							$("#insolja2").effect("fade", {mode: "show"}, 1000, function() {
								setTimeout(function() {
									$("#insolja2").effect("fade", {mode: "hide"}, 1000, function() {
										$("#insolja3").effect("fade", {mode: "show"}, 1000, function() {
											setTimeout(function() {
												$("#insolja3").effect("fade", {mode: "hide"}, 1000, function() {
													buildup();
												});
											}, 3662);
										});
									});
								}, 3662);
							});
						});
					}, 3662);
				});
			});
		}, 3662);
	});
};

var buildup = function() {
	$("#new").effect("slide", {direction: "left", mode: "show"}, 1000, function() {
		setTimeout(function() {
			$("#new").effect("slide", {direction: "right", mode: "hide"}, 1000, function() {
				$("#missiontour").effect("slide", {direction: "up", mode: "show"}, 1000, function() {
					setTimeout(function() {
						$("#missiontour").effect("slide", {direction: "down", mode: "hide"}, 1000, function() {
							$("#theme").effect("slide", {direction: "right", mode: "show"}, 1000, function(){
								setTimeout(function() {
									$("#theme").effect("slide", {direction: "left", mode: "hide"}, 1000, function() {
										$("#heads").effect("slide", {direction: "down", mode: "show"}, 1000, function() {
											setTimeout(function() {
												$("#heads").effect("slide", {direction: "up", mode: "hide"}, 1000, function() {
													setTimeout(function() {
														$("#end").effect("slide", {direction: "down", mode: "show"}, 10000, function() {
														});
													}, 3380);
												});
											}, 8707);
										});
									});
								}, 8707);
							});
						});
					}, 8707);
				});
			});
		}, 8707);
	});
};

ending.addEventListener('canplaythrough', start);
