from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bts_quotes'
db = SQLAlchemy(app)

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(44), nullable=False)

@app.route('/')
def index():
    all_quotes = Quotes.query.all()
    
    if all_quotes:
        # Extract the 'quote' attribute from each Quote object and store in a list
        quote_texts = [quote.quote for quote in all_quotes]
          
        # Select a random quote from the list
        rand_quote = random.choice(quote_texts)
    return render_template('index.html', rand_quote=rand_quote)

if __name__ == '__main__':
    db.create_all()
    app.run()
