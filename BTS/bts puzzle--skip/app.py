from flask import Flask, render_template
import random

app = Flask(__name__)

# List of album covers (you can add more)
album_covers = [
    "jhope0.png",
      "jhope1.png",
        "jhope3.png",  # Replace with the actual file path of the album cover
]

@app.route('/')
def index():
    # Randomly select an album cover
    selected_cover = random.choice(album_covers)
    
    # Shuffle the pieces (a simple 2x2 grid)
    pieces = ["piece1", "piece2", "piece3", "piece4"]
    random.shuffle(pieces)
    
    return render_template('index.html', album_cover=selected_cover, pieces=pieces)

if __name__ == '__main__':
    app.run(debug=True)
