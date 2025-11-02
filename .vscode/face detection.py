import base64
import cv2
from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/bts_lyric_repeat"
# initialize the app with the extension
db= SQLAlchemy(app)

# Define the user upload model
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_image = db.Column(db.String(100), unique=True, nullable=False)
    filename = db.Column(db.String(12),nullable=False) 
    file_data = db.Column(db.LargeBinary, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)


def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

# Specify the directory containing the dataset
dataset_directory = (r'C:\Users\veathavalli\Desktop\.vscode\BTS facial recogonization\images')

# List all image files in the directory
image_files = [f for f in os.listdir(dataset_directory) if f.endswith('.jpg')]

# Loop through the image files and display them
for image_file in image_files:
    image_path = os.path.join(dataset_directory, image_file)
    image = cv2.imread(image_path)

    # Display the image using Matplotlib
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(image_file)  # Set the title to the image file name
    plt.axis('off')  # Turn off axis labels
    plt.show()


@app.route('/upload', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename  # Get the original filename
            file_data = file.read()  # Read the file data
            data = file_data  # Set data to file_data (if needed)
            render_file = render_picture(data)

            new_file = Upload(filename=filename, file_data=file_data, data=data, rendered_data=render_file)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('result', file_id=new_file.id))

    return render_template('index.html')

