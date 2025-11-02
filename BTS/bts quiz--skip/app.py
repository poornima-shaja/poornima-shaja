from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_quiz"
db = SQLAlchemy(app)

class ques_ans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80))
    answer = db.Column(db.String(20))
    wrong_option = db.Column(db.String(20))

# Set the maximum number of questions
MAX_QUESTIONS = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        session['user_input'] = user_input
        session['question_count'] = 0  # Initialize question count
        return redirect(url_for('quiz'))
    return render_template('first_page.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    user_input = session.get('user_input')
    
    # Retrieve the current question count from the session
    question_count = session.get('question_count', 0)
    
    if question_count >= MAX_QUESTIONS:
        # If the maximum number of questions has been reached, redirect to the result page
        return redirect(url_for('result'))
    
    # Retrieve a random question and its correct answer from the database
    quiz_item = ques_ans.query.order_by(func.rand()).first()

    # Increment the question count
    question_count += 1
    session['question_count'] = question_count

    return render_template('index.html', question=quiz_item.question if quiz_item else None, 
                           answer=quiz_item.answer if quiz_item else None, 
                           wrong_option=quiz_item.wrong_option if quiz_item else None, 
                           user_input=user_input, question_count=question_count)

@app.route('/result')
def result():
    # Retrieve the user's responses from the session
    user_responses = session.get('user_responses', [])

    # Calculate the score by comparing user responses to the correct answers
    score = 0
    for user_response in user_responses:
        # Assuming each user response is a dictionary with keys 'question' and 'response'
        question = user_response.get('question')
        response = user_response.get('response')

        # Query the database to check if the response is correct
        correct_answer = ques_ans.query.filter_by(question=question, answer=response).first()
        
        if correct_answer:
            score += 1  # Increment the score for correct responses

    return render_template('result.html', score=score)


if __name__ == '__main__':
    app.run()
