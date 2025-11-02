from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import re

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_repeat"
# Initialize the app with the extension
db = SQLAlchemy(app)

# Define the BTS Lyrics model
class lyrics_v6(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<bts_lyric_repeat {self.song_name}>'

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

@app.route('/')
def index():
    songs = lyrics_v6.query.all()
    return render_template('index.html', songs=songs)

@app.route('/analysis')
def analysis():
    songs = lyrics_v6.query.all()
    return render_template('analysis.html', songs=songs)

@app.route('/analyze', methods=['POST'])
def analyze():
    song_name = request.form.get('song_name')

    # Query the database to retrieve lyrics entry
    lyrics_entry = lyrics_v6.query.filter_by(song_name=song_name).first()

    if lyrics_entry:
        # Tokenize the lyrics into words (split by whitespace)
        words = re.findall(r'\w+', lyrics_entry.lyrics.lower())

        final = [word for word in words if word not in stop_words]

        # Count the frequency of each word
        word_counts = Counter(final)

        most_common_word = word_counts.most_common(1)
        if most_common_word:
            most_common_word = most_common_word[0][0]
        else:
            most_common_word = "No words found"
    else:
        most_common_word = "Lyrics not found"

    # Retrieve existing songs from the database
    songs = lyrics_v6.query.all()

    # Check if the user provided their own lyrics
    user_lyrics = request.form.get('user_lyrics')

    if user_lyrics:
        # Tokenize the user's lyrics into words (split by whitespace)
        user_words = re.findall(r'\w+', user_lyrics.lower())

        user_final = [word for word in user_words if word not in stop_words]

        # Count the frequency of each word
        user_word_counts = Counter(user_final)

        user_most_common_word = user_word_counts.most_common(1)
        if user_most_common_word:
            user_most_common_word = user_most_common_word[0][0]
        else:
            user_most_common_word = "No words found"
    else:
        user_most_common_word = "User Lyrics not provided"
       
    return render_template('result.html', songs=songs, song_name=song_name, lyrics=lyrics_entry.lyrics, most_common_word=most_common_word, user_lyrics=user_lyrics, user_most_common_word=user_most_common_word)

@app.route('/add_song_form')
def add_song_form():
    return render_template('add_song_form.html')

@app.route('/add_song', methods=['POST'])
def add_song():
    new_song_name = request.form.get('new_song_name')
    new_lyrics = request.form.get('new_lyrics')
    
    # Check if the song already exists in the database
    existing_song = lyrics_v6.query.filter_by(song_name=new_song_name).first()

    if existing_song:
        return "Song already exists in the database."
    
    # Create a new entry in the database for the user-submitted song
    new_song = lyrics_v6(song_name=new_song_name, lyrics=new_lyrics)
    db.session.add(new_song)
    db.session.commit()
    
    return f"Song '{new_song_name}' has been added to the database."

if __name__ == '__main__':
    app.run(debug=True)
