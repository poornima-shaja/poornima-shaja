from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Create a chatbot instance
chatbot = ChatBot('BTSChatbot')

# Create a new instance of a ChatterBotCorpusTrainer
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on BTS-related data from the corpus
trainer.train('chatterbot.corpus.english')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['GET'])
def get_response():
    user_message = request.args.get('msg')
    response = chatbot.get_response(user_message).text
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
