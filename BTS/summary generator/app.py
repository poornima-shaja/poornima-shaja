from transformers import pipeline
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyrics_summary"
# initialize the app with the extension
db= SQLAlchemy(app)


# Load a pre-trained model for summarization (e.g., T5)

summarizer = pipeline("summarization", model="t5-small", revision="d769bba")


# Define the BTS Lyrics model
class lyrics_summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<bts_lyric_repeat {self.song_name}>'

@app.route('/')
def index():
    songs = lyrics_summary.query.all()
    return render_template('index.html',songs=songs)

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_song = db.Column(db.Text)
    user_lyrics = db.Column(db.Text, nullable=False)

@app.route('/analyze', methods=['POST'])
def analyze():
    song_name = request.form.get('song_name')
    user_lyrics = request.form.get('user_lyrics')
    user_song = request.form.get('user_song')  # Retrieve the user's song name input

    # Initialize summary variables
    summary_1 = "Summary not available"
    summary_2 = "Summary not available"

    if song_name:
        # Query the database to retrieve lyrics entry for the selected BTS song
        lyrics_entry = lyrics_summary.query.filter_by(song_name=song_name).first()

        if lyrics_entry:
            # Get lyrics for the selected song
            lyrics_1 = lyrics_entry.song_lyrics
            # Truncate the lyrics if it's longer than the model's limit (512 tokens)
            if len(lyrics_1.split()) > 512:
                lyrics_1 = " ".join(lyrics_1.split()[:512])

            try:
                summary_1 = summarizer(lyrics_1, max_length=200, min_length=30, do_sample=False)
            except Exception as e:
                summary_1 = f"Error: Unable to generate a summary. {str(e)}"

    if user_lyrics:
        # Create a new UserInput object and save it to the database
        user_input_entry = UserInput(user_song=user_song, user_lyrics=user_lyrics)
        db.session.add(user_input_entry)
        db.session.commit()

        # Get user input lyrics
        lyrics_2 = user_lyrics
        # Use the summarization model to generate a summary for user input lyrics
        try:
            summary_2 = summarizer(lyrics_2, max_length=200, min_length=30, do_sample=False)
        except Exception as e:
            summary_2 = f"Error: Unable to generate a summary. {str(e)}"

    # Retrieve existing songs from the database
    songs = lyrics_summary.query.all()

    # Query user input data from the database
    user_input_data = UserInput.query.order_by(UserInput.id.desc()).first()

    return render_template('result.html', songs=songs, song_name=song_name, user_lyrics=user_lyrics, user_song=user_song, summary_1=summary_1, summary_2=summary_2, user_input_data=user_input_data)

if __name__ == '__main__':
    db.create_all()
    app.run()






# # Your song database with lyrics
# song_database = {
#     "Song 1 Title": '''BTS (Korean:y Scouts), also'''
# }

# # User selects two songs
# selected_song_1 = "Song 1 Title"


# # Get lyrics for the selected songs
# lyrics_1 = song_database.get(selected_song_1, "Lyrics not found for this song.")
# # Use the summarization model to generate summaries for the songs
# summary_1 = summarizer(lyrics_1, max_length=200, min_length=30, do_sample=False)



# # Print the summaries
# print("Summary of", selected_song_1 + ":")
# print(summary_1[0]['summary_text'])
