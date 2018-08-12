window.onload = function () {

	var name = "User";
	var recognition;

	//speech function
	speak = function (text, callback) {
		var utterThis = new SpeechSynthesisUtterance();
		utterThis.text = text;
		utterThis.lang = 'en-UK';
		utterThis.rate = '0.6'; //1 is default

		utterThis.onend = function () {
			if (callback) {
				callback();
			}
		};

		utterThis.onerror = function (e) {
			if (callback) {
				callback(e);
			}
		};

		speechSynthesis.speak(utterThis);
	};
	//

	//speech recognition
	startDictation = function () {
		recognition = new webkitSpeechRecognition();
		recognition.continuous = true;
		recognition.interimResults = true;
		recognition.lang = "en-US";

		recognition.onresult = function (e) {
			for (var i = e.resultIndex; i < e.results.length; ++i) {
				//console.log(e.results)
				if (e.results[i].isFinal) {
					document.getElementById('messageText').value
						 = e.results[i][0].transcript;

					recognition.stop();
					$("#overlay").hide();
					document.getElementById('chatbot-form-btn').click();
					// recognition.start();
				}
			}
		};

		recognition.start();

		recognition.onerror = function (e) {
			recognition.stop();
			$("#overlay").hide();
		}
	};

	stopDictation = function () {
		recognition.stop();
	};
	//

	//overlay logic
	$("#talk").click(function () {
		startDictation();
		$("#overlay").show();

	});

	$("#overlay").click(function () {
		stopDictation();
		$("#overlay").hide();
	});
	//

	//toast logic
	$("#info").click(function () {
		var toastElement = document.querySelector('.toast');
		if (toastElement) {
			var toastInstance = M.Toast.getInstance(toastElement);
			toastInstance.dismiss();
		} else {
			M.toast({
				html: info_text,
				displayLength: 10000
			})
		}
	});
	//

	//chat logic
	bot_message = '<li class="collection-item avatar"><i class="large material-icons circle blue darken-4">adb</i><span class="title">Bot</span><p>: '
		user_message = '<li class="collection-item avatar"><i class="large material-icons circle orange">account_circle</i><span class="title">User</span><p>: '
		message_end = '</p></li>'

		$('#chatbot-form-btn').click(function (e) {
			e.preventDefault();
			$('#chatbot-form').submit();
		});

	$('#chatbot-form').submit(function (e) {
		e.preventDefault();
		var message = $('#messageText').val();
		$('#messageText').val('');
		if (message.toLowerCase().includes("name")) {
			$("#chatList").append(user_message + message + message_end);

			var n = message.split(" ");
			name = n[n.length - 1];
			user_message = '<li class="collection-item avatar"><i class="large material-icons circle orange">account_circle</i><span class="title">' + name + '</span><p>: '
				name_text = "Hi!, " + name + " how may i help you?"
				$("#chatList").append(bot_message + name_text + message_end);
			$('#chatList').animate({
				scrollTop: $('#chatList').prop("scrollHeight")
			}, 500);
			speak(name_text, () => M.toast({
					html: 'For sample questions click "?"'
				}));
			info_text = 'You can ask qustions like:' +
				'<br>"Women married before age 18 in anantapur andhra pradesh"' +
				'<br>"Houses in rural areas with mobile phones"' +
				'<br>"Districts where female literates are more than male literates"' +
				'<br>"Net enrolment rate of education"' +
				'<br>"percentage houses in rural areas of Anantapur with mobile phones"' +
				'<br>"Total working population in Anantpur"' +
				'<br>"Districts where female literates are more than male literates"' +
				'<br>"Districts where sex ratio more than 200"';
		} else if (message != "") {
			$("#chatList").append(user_message + message + message_end);
			$('#chatList').animate({
				scrollTop: $('#chatList').prop("scrollHeight")
			}, 500);
			$.ajax({
				type: "POST",
				url: "/ask",
				//data: $(this).serialize(),
				data: {
					"messageText": message
				},
				success: function (response) {

					$('#messageText').val('');
					if (response.type == 'table') {
						//console.log(response.answer);
						var data = JSON.parse(response.answer);
						//$("#tablediv").show();
						//console.log($("#table")); //use this

						$("#table > thead > tr").remove();
						$("#table > tbody > tr").remove();
						for (var i = 0; i < data.length; i++) {
							var items = [];
							for (var j = 0; j < data[i].length; j++) {
								if (i == 0) {
									items += "<th>" + data[i][j] + "</th>"
								} else {
									items += "<td>" + data[i][j] + "</td>"
								}
							}
							if (i == 0) {
								$("#table > thead").append("<tr>" + items + "</tr>");
							} else {
								$("#table > tbody").append("<tr>" + items + "</tr>");
							}

						}

						var answer = "This is what i found.";
						speak(answer);
						$("#chatList").append(bot_message + answer + message_end);
						$('#chatList').animate({
							scrollTop: $('#chatList').prop("scrollHeight")
						}, 500);

						$('html, body').animate({
							scrollTop: $("#chatBoxDiv").offset().top
						}, 2000);
					} else {
						var answer = response.answer;
						speak(answer);
						$("#chatList").append(bot_message + answer + message_end);
						$('#chatList').animate({
							scrollTop: $('#chatList').prop("scrollHeight")
						}, 500);
					}

				},
				error: function (error) {
					console.log(error);
				}
			});

		}
	});
	//

	//onload
	$("#overlay").hide();
	//$("#tablediv").hide();
	welcome_text = "Hi! I am the Jaano India bot. May i know your name please?";
	speak(welcome_text, () => M.toast({
			html: 'For help click "?"'
		}));
	info_text = 'You may say "My name is Bob."'
		$("#chatList").append(bot_message + welcome_text + message_end);
	//

};
