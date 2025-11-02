from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import re

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_repeat"
# initialize the app with the extension
db= SQLAlchemy(app)

# Define the BTS Lyrics model
class lyrics_v6(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<bts_lyric_repeat {self.song_name}>'

@app.route('/')
def index():
    songs = lyrics_v6.query.all()
    return render_template('index.html',songs=songs)

# @app.route('/form')
# def input_form():
#     return render_template('form.html')


stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_song = db.Column(db.Text)
    user_lyrics = db.Column(db.Text, nullable=False)

    # Create the database tables
db.create_all()


@app.route('/analyze', methods=['POST'])
def analyze():
    song_name = request.form.get('song_name')
    user_lyrics = request.form.get('user_lyrics')
    user_song = request.form.get('user_song')  # Retrieve the user's song name input

    if song_name:  # Check if a BTS song is selected
        # Query the database to retrieve lyrics entry for the selected BTS song
        lyrics_entry = lyrics_v6.query.filter_by(song_name=song_name).first()

        if lyrics_entry:
            # Analyze BTS song as you did before
            words = re.findall(r'\w+', lyrics_entry.lyrics.lower())
            final = [word for word in words if word not in stop_words]
            word_counts = Counter(final)
            most_common_word = word_counts.most_common(1)
            most_common_word = most_common_word[0][0] if most_common_word else "No words found"
        else:
            most_common_word = "Lyrics not found"
    else:
        lyrics_entry = None
        most_common_word = "No selection made"
        


    # Analyze user input lyrics
    if user_lyrics:
        # Create a new UserInput object and save it to the database
        user_input_entry = UserInput(user_song=user_song, user_lyrics=user_lyrics)
        db.session.add(user_input_entry)
        db.session.commit()

        # Now, you can analyze the user's input lyrics as needed
        user_words = re.findall(r'\w+', user_lyrics.lower())
        user_final = [word for word in user_words if word not in stop_words]
        user_word_counts = Counter(user_final)
        user_most_common_word = user_word_counts.most_common(1)
        user_most_common_word = user_most_common_word[0][0] if user_most_common_word else "No words found"
    else:
        user_most_common_word = "User Lyrics not provided"

    # Retrieve existing songs from the database
    songs = lyrics_v6.query.all()

    # Query user input data from the database
    user_input_data = UserInput.query.order_by(UserInput.id.desc()).first()
    return render_template('result.html', songs=songs, song_name=song_name, lyrics=lyrics_entry.lyrics if lyrics_entry else "", most_common_word=most_common_word if lyrics_entry else "", user_lyrics=user_lyrics, user_most_common_word=user_most_common_word, user_song=user_song,user_input_data=user_input_data)

if __name__ == '__main__':
    app.run()