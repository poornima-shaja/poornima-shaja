import base64
from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user

app=Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/cover_repo?connect_timeout=120"
# Initialize the app with the extension
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Set the login view route

# Define a User model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Function to load a user by ID
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class Accounts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(20))
    password= db.Column(db.String(80))
    re_password= db.Column(db.String(80))
    date = db.Column(db.String(12)) 

@app.route('/')
def firstpage():
    user_name = session.get('user_name')  # Get the user's name from the session
    return render_template('firstpage.html', user_name=user_name)

@app.route('/logout')
def logout():
    session.clear()  # Clear the user's session
    return redirect(url_for("firstpage"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["passw"]

        login = Accounts.query.filter_by(email=email, password=password).first()
        if login is not None:
            # Authenticate the user using Flask-Login
            user = User(login.sno)  # Pass the user's ID to User constructor
            login_user(user)  # Log in the user
            session['user_name'] = login.name  # Set the user's name in the session
            flash('Login successful!', 'success')
            return redirect(url_for("firstpage"))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')




 
@app.route('/register',methods=["GET","POST"])
def register():
     if request.method == "POST":
        uname = request.form.get('name')
        email = request.form.get('email')
        passw  = request.form.get('passw')
        re_passw  = request.form.get('re_password')

        register = Accounts(name = uname, email = email, password = passw,re_password =re_passw ,date=datetime.now())
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
     return render_template('register.html')    

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(12),nullable=False) 
    file_data = db.Column(db.LargeBinary, nullable=False)
    textarea = db.Column(db.String(255), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='upload', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.sno'), nullable=False)
    date = db.Column(db.String(12))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic



@app.route('/upload', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        textarea = request.form.get('textarea')
        if file:
            filename = file.filename  # Get the original filename
            file_data = file.read()  # Read the file data
            data = file_data  # Set data to file_data (if needed)
            render_file = render_picture(data)

            new_file = Upload(filename=filename, file_data=file_data, data=data, rendered_data=render_file, user_id=current_user.id,textarea=textarea)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('feed', file_id=new_file.id))

    return render_template('index.html')


@app.route('/success/<int:file_id>')
def success(file_id):
    user_name = session.get('user_name')
    upload = Upload.query.get(file_id)
    if upload:
        return render_template('success.html', upload=upload,user_name=user_name)
    return "File not found."

@app.route('/like/<int:file_id>', methods=['POST'])
def like(file_id):
    upload = Upload.query.get(file_id)
    if upload:
        # Increment the likes count
        upload.likes += 1
        db.session.commit()
    return redirect(url_for('feed', file_id=file_id))



@app.route('/comment/<int:file_id>', methods=['POST'])
def comment(file_id):
    text = request.form.get('comment_text')
    upload = Upload.query.get(file_id)

    if text and upload:
        new_comment = Comment(text=text, upload_id=file_id)
        db.session.add(new_comment)
        db.session.commit()

    return redirect(url_for('feed', file_id=file_id))




@app.route('/profile')
@login_required
def profile():
    # Get the current logged-in user
    user_name = session.get('user_name')
    if user_name:
        # Fetch user data from the database (adjust the User model and database structure as needed)
        user = Accounts.query.filter_by(name=user_name).first()
        if user:
            user_email = user.email
            # You can add more user-related information here

            # Fetch only the files uploaded by the current user, ordered by date in descending order
            user_files = Upload.query.filter_by(user_id=user.sno).order_by(Upload.date.desc()).all()

            return render_template('profile.html', user_name=user_name, user_email=user_email, user_files=user_files)
    
    flash('Please log in to access your profile.', 'info')
    return redirect(url_for('login'))

@app.route('/feed')
@login_required
def feed():
    # Fetch all user files from the database
    users = Upload.query.order_by(Upload.date.desc()).all()
    return render_template('feed.html', users=users)

@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    # Check if the current user owns the file (you should implement this logic)
    upload = Upload.query.get(file_id)
    if upload and upload.user_id == current_user.id:
        # Delete the file from the database
        db.session.delete(upload)
        db.session.commit()
        flash('File deleted successfully.', 'success')
    else:
        flash('You do not have permission to delete this file.', 'danger')
    return redirect(url_for('profile'))  # Redirect to the profile page


if __name__== '__main__':
    app.run()