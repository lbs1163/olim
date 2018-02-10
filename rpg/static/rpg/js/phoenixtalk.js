var talk = new Audio('/static/rpg/sound/talk.mp3');
var music = new Audio('/static/rpg/sound/phoenixtalk.mp3');

var dialog = function(string, i, callback) {
	if (string.length == i - 1) {
		setTimeout(callback, 2300);
	} else {
		$("#dialog").html(string.substring(0, i));
		talk.currentTime = 0;
		talk.play();
		setTimeout(function() { dialog(string, i+1, callback) }, 70);
	}
}

var phoenixtalk = function(lines, i, callback) {
	if (lines.length <= i) {
		callback();
	} else {
		if (lines[i] == "gogo"
				|| lines[i] == "happy"
				|| lines[i] == "jumping"
				|| lines[i] == "normal"
				|| lines[i] == "studying"
				|| lines[i] == "teaching") {
			$("#phoenix img").attr("src", "/static/rpg/image/" + lines[i] + "_phoenix.png");
			phoenixtalk(lines, i+1, callback);
		} else {
			dialog(lines[i], 1, function() {
				phoenixtalk(lines, i+1, callback)
			});
		}
	}
}

var fade = function() {
	if (music.volume >= 0.1) {
		music.volume -= 0.1;
		setTimeout(fade, 200);
	} else {
		music.pause();
	}
}

phoenixtalk(lines, 0, function() {
	fade();
});

music.loop = true;
music.play();
