var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent
var grammar = '#JSGF V1.0; grammar = ' + (' | ') + ' ;'
var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;
var diagnostic = document.querySelector('.output');
var bg = document.querySelector('html');
var hints = document.querySelector('.hints');
recognition.onresult = function(event) {
    var voicecommand = event.results[0][0].transcript;
    $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div //class="media-body">' + voicecommand + '<hr/></div></div></div></li>');
    var http = new XMLHttpRequest();
    var url = '/voice';
    var params = voicecommand;
	var xhr = new XMLHttpRequest(); //make xhr
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			answer = xhr.responseText;
			$(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div //class="media-body">' + answer + '<hr/></div></div></div></li>');
			speechSynthesis.speak(new SpeechSynthesisUtterance(answer));
		}
	}
	xhr.open('POST', url, true);
	xhr.setRequestHeader('Content-Type', 'x-www-form-urlencoded');
	xhr.send(voicecommand);
    console.log(voicecommand)
    console.log('Confidence: ' + event.results[0][0].confidence);
}
recognition.onspeechend = function() {
    recognition.stop();
}

recognition.addEventListener('end', function() {
    setTimeout(() => { recognition.start(); }, 1000);
});
recognition.onnomatch = function(event) {
    diagnostic.textContent = 'huh';
}
recognition.start();