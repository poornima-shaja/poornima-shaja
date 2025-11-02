from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    name = request.form.get('name')
    text_color = request.form.get('text_color')

    

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        # Save the uploaded image
        uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(uploaded_image_path)

        # Open the uploaded image using Pillow
        img = Image.open(uploaded_image_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Overlay text on the image
        text = "BTS Album"
        name = name
        draw.text((10, 10), text, fill='white', font=font)

        # Calculate the coordinates to place the text at the bottom-middle of the image
        text_width, text_height = draw.textsize(name, font)
        x = (img.width - text_width) / 2
        y = img.height - text_height - 10  # Position the text above the very bottom with a small margin

        # Draw the user-provided album name on the image
        if name:
            # Draw the user-provided album name on the image at the calculated coordinates
            draw.text((x, y), name, fill=text_color, font=font)

        # Save the modified image as the album cover
        album_cover_path = os.path.join(app.config['UPLOAD_FOLDER'], 'album_cover.png')
        img.save(album_cover_path)

        return send_file(album_cover_path, mimetype='image/png')
    else:
        return "Invalid file format"


if __name__ == '__main__':
    app.run()
