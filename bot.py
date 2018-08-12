import os
from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from flask import jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import postgres

app = Flask(__name__)
port = int(os.getenv("PORT"))

english_bot = ChatBot("indiana_janos")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train('chatterbot.corpus.english.greetings')

#add table to html
#check columns before result

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/ask", methods=['POST'])
def ask():
	message = (request.form['messageText'])

	while True:
		if message == "":
			continue
		else:
			sql_data = postgres.query(message)
			#print(sql_data)
			#bot_response = str(english_bot.get_response(message))
			#print bot_response
			if sql_data == "no_columns":
				return jsonify({'status':'OK','type':'','answer':"Sorry, i didn't understand that. You can click the '?' icon for help."})
			else:
				return jsonify({'status':'OK','type':'table','answer':sql_data})


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=port,debug=False)
