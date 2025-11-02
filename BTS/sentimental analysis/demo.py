import string
from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import os
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_repeat"
# Initialize the app with the extension
db = SQLAlchemy(app)

@app.route('/')
def index():
    songs = lyrics_v6.query.all()
    return render_template('index.html', songs=songs)

# Define the BTS Lyrics model
class lyrics_v6(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)