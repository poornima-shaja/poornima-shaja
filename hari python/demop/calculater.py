from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/' )
def index():
    return render_template('index.html')
    
        
@app.route('/result' , methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        Symbols = request.form.get('Symbols')
        
        if Symbols == "+":
            calculate = int(fname) + int(lname)
        elif Symbols == "-":
            calculate = int(fname) - int(lname)
        elif Symbols == "*":
            calculate = int(fname) * int(lname)
        
    return render_template('result.html', calculate=calculate)
    
if __name__ == '__main__':
    app.run()