import os
from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Enable template auto-reloading
app.template_folder = "templates"  # Set the folder where templates are located

# Function to get a list of songs from the "audio" folder
def get_songs():
    audio_folder = "static/audio"
    songs = []

    # List all files in the audio folder
    for filename in os.listdir(audio_folder):
        if filename.endswith(".mp3"):  # Adjust the file extension as needed
            songs.append({"title": filename[:-4]})  # Remove the file extension for the title

    return songs

@app.route("/")
def index():
    songs = get_songs()
    return render_template("index.html", songs=songs)

if __name__ == "__main__":
    app.run()
