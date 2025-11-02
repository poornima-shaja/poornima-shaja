import string
from flask import Flask,render_template
from collections import Counter
import os
from nltk.corpus import stopwords

# import matplotlib.pyplot as plt
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_repeat"
# Initialize the app with the extension
# db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

from flask import request  # Add this import statement

@app.route('/analyze', methods=['POST'])
def analyze():
    user_lyrics = request.form.get('user_lyrics')

    if not user_lyrics:
        return render_template('error.html', message="No lyrics provided. Please enter some lyrics.")

    cleaned_text = user_lyrics.lower().translate(str.maketrans('', '', string.punctuation))
    tokenized_words = cleaned_text.split()

    stop_words = set(stopwords.words('english'))
    final_words = [word for word in tokenized_words if word not in stop_words]

    emotion_list = []
    with open('emotion.txt', 'r') as file:
        for line in file:
            if ':' in line:
                clear_line = line.strip().lower().replace(",", '').replace("'", '')
                word, emotion = clear_line.split(':')
                if word in final_words:
                    emotion_list.append(emotion)

    emotion_words = []
    for word in tokenized_words:
        if word in emotion_list:
            word = f"<u>{word}</u>"
        emotion_words.append(word)
    modified_lyrics = ' '.join(emotion_words)

    count_of_emo = Counter(emotion_list)

    return render_template('sentiment_result.html', user_lyrics=user_lyrics, emotion_list=emotion_list, modified_lyrics=modified_lyrics, emotion_counts=count_of_emo)


if __name__ == '__main__':
    app.run()