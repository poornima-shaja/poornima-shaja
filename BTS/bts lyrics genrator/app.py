from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bts_lyric_generator'  
db = SQLAlchemy(app)

class Btslyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.String(500))
    # Add other columns as needed

@app.route('/', methods=['GET', 'POST'])
def search_lyrics():
    if request.method == 'POST':
        keyword = request.form['keyword']
        
        # Retrieve rows where the keyword matches
        matching_results = Btslyrics.query.filter(Btslyrics.lyrics.like(f"%{keyword}%")).all()
        
        # Randomly select 8 lines from each matching result
        formatted_results = []
        for result in matching_results:
            lines = result.lyrics.split('\n')
            random.shuffle(lines)
            selected_lines = lines[:8]
            formatted_results.append("\n".join(selected_lines))
        
        return render_template('results.html', keyword=keyword,selected_lines=selected_lines)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
