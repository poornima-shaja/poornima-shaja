from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define the questions and options
questions = [
    {
        "question": "What is your favorite color?",
        "options": {
            "Yellow": "RM",
            "Pink": "Jin",
            "Black": "Suga",
            "Blue": "J-Hope",
            "Orange": "Jimin",
            "Purple": "V",
            "Green": "Jungkook"
        }
    },
    {
        "question": "What is your favorite animal?",
        "options": {
            "Koala": "RM",
            "Cat": "Jin",
            "Horse": "Suga",
            "Tiger": "J-Hope",
            "Lion": "Jimin",
            "Dog": "V",
            "Cheetah": "Jungkook"
        }
    },
    {
        "question": "What is your favorite cartoon?",
        "options": {
            "Dala": "RM",
            "Mala": "Jin",
            "Dora": "Suga",
            "Chottabheem": "J-Hope",
            "Doremon": "Jimin",
            "Shinshan": "V",
            "Flower": "Jungkook"
        }
    }
]

@app.route('/')
def index():
    return render_template('quiz.html', questions=questions)

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        user_responses = request.form.to_dict()
        member_counts = {member: 0 for member in set(option for option in questions[0]['options'].values())}

        for question in questions:
            selected_option = user_responses.get(question['question'])
            if selected_option:
                selected_member = question['options'].get(selected_option)
                if selected_member:
                    member_counts[selected_member] += 1

        most_selected_member = max(member_counts, key=member_counts.get)
        return render_template("result.html",most_selected_member=most_selected_member)

if __name__ == '__main__':
    app.run()
