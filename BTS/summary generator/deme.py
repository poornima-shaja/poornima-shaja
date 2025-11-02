from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from events import FileSystemEventHandler

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyrics_summary"
# Initialize the app with the extension
db = SQLAlchemy(app)

# Load a pre-trained model for summarization (e.g., T5)
summarizer = pipeline("summarization", model="t5-small", revision="d769bba")

# Define the BTS Lyrics model
class lyrics_summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<bts_lyrics_summary {self.song_name}>'
    

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_song = db.Column(db.Text)
    user_lyrics = db.Column(db.Text, nullable=False)    




# Routes for selecting songs and inputting lyrics
@app.route('/')
def index():
    songs = lyrics_summary.query.all()
    return render_template('index.html', songs=songs)

@app.route('/input_lyrics')
def input_lyrics():
    return render_template('input_lyrics.html')

# Route for analyzing lyrics and displaying summaries
@app.route('/analyze', methods=['POST'])
def analyze():
    song_name = request.form.get('song_name')
    user_lyrics = request.form.get('user_lyrics')
    user_song = request.form.get('user_song')

    # Initialize summary variables
    summary_1 = summary_2 = ""

    if song_name:
        lyrics_entry = lyrics_summary.query.filter_by(song_name=song_name).first()
        if lyrics_entry:
            lyrics_1 = lyrics_entry.song_lyrics
            try:
                summary_1 = summarizer(lyrics_1, max_length=200, min_length=30, do_sample=False)
            except Exception as e:
                logging.error(f"Error generating summary for {song_name}: {str(e)}")
                summary_1 = "Error: Unable to generate a summary."

    if user_lyrics:
        # Save user input to the database
        user_input_entry = UserInput(user_song=user_song, user_lyrics=user_lyrics)
        db.session.add(user_input_entry)
        db.session.commit()

        # Get user input lyrics
        lyrics_2 = user_lyrics
        try:
            summary_2 = summarizer(lyrics_2, max_length=200, min_length=30, do_sample=False)
        except Exception as e:
            logging.error(f"Error generating summary for user input: {str(e)}")
            summary_2 = "Error: Unable to generate a summary."

    # Retrieve existing songs from the database
    songs = lyrics_summary.query.all()

    # Query user input data from the database
    user_input_data = UserInput.query.order_by(UserInput.id.desc()).first()

    return render_template('result.html', songs=songs, song_name=song_name, user_lyrics=user_lyrics,
                           user_song=user_song, summary_1=summary_1, summary_2=summary_2,
                           user_input_data=user_input_data)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
