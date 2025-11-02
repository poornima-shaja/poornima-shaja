from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_guess"
# initialize the app with the extension
db= SQLAlchemy(app)

# Define the BTS Lyrics model
class Bts_lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    random_lyric = Bts_lyrics.query.order_by(func.rand()).first()
    # Split the lyrics into lines
    lines = random_lyric.song_lyrics.split('\n')
        # Select the first 2-3 lines from the lyrics
    selected_lines = lines[:3]

    # Join the selected lines back into a single string
    selected_lyrics = '\n'.join(selected_lines)
    song_name = random_lyric.song_name
    return render_template("index.html",selected_lyrics=selected_lyrics,song_name=song_name)

@app.route('/next')
def next_lyric():
    # Redirect to the homepage ("/") to generate a new random lyric
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
