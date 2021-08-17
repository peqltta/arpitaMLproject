from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from aiml import Kernel
import os
import numpy as np
import pandas as pd
import html
import sys
import speech_recognition as sr
import pyttsx3
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
nltk.download("punkt")
nltk.download("vader_lexicon")
sid = SentimentIntensityAnalyzer()
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
allcommands = 'hello'
kernel = Kernel()

if os.path.isfile("bot_brain.brn"):
	os.remove("bot_brain.brn")
	kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	kernel.saveBrain("bot_brain.brn")
else:
	kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	kernel.saveBrain("bot_brain.brn")

def speaks(audioString):
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say(audioString)
	engine.runAndWait()
	
def recordAudio():
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
 
	# Speech recognition using Google Speech Recognition
	data = ""
	voicecommand = ""
	try:
		voicecommand = r.recognize_google(audio)
		print("You said: " + voicecommand)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	print('Sentiment Score (For later use - NLP)')
	
	return voicecommand
	
def jarvis(data):
	s = kernel.respond(data)
	return s

@app.route("/voice", methods=['POST'])
def voice():
    global allcommands
    data = request.data.decode()
    allcommands = allcommands+' '+data
    sentiment = str(sid.polarity_scores(data))
    answer = kernel.respond(data) + '#' +sentiment
    return answer #jsonify({'status':'OK','answer':jarvis(data)})

@app.route("/")
def hello():
	return render_template('chat.html')

@app.route("/wordcloud", methods=['POST'])
def wordcloud():
	wordcloud = WordCloud(stopwords=STOPWORDS,background_color='black',max_words=300)
	wordcloud.generate(allcommands)
	wordcloud.to_file("static/wordcloud.png")
	return render_template('wordcloud.html')

@app.route("/ask", methods=['POST'])
def ask():
	global allcommands
	message = str(request.form['messageText'])
	allcommands += allcommands + ' ' + message
	# kernel now ready for use
	while True:
		if message == "quit":
			exit()
		elif message == "save":
			kernel.saveBrain("bot_brain.brn")
		else:
			bot_response = kernel.respond(message)
			# print bot_response
			return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
	app.run()
	app.run(host='192.168.0.11', port=5000)
