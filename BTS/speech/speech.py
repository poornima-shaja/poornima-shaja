from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio_data = request.files['audio']
    # Process the live audio data using your voice recognition model
    # Replace this with your actual voice recognition code
    # Example: 
    # result = your_voice_recognition_model.recognize_audio(audio_data)
    # return result
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
