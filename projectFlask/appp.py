import cv2
import numpy as np
import pyaudio
import wave
import librosa
import librosa.display
import tensorflow as tf
from keras.models import load_model
import sounddevice as sd

# Load the emotion detection model for images
model = load_model(r'C:\Users\veathavalli\Downloads\model (2).h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
label_map = ['Anger', 'Neutral', 'Happy', 'Sad', 'Surprise']

# Load the emotion detection model for voice
voice_model = load_model("voice_emotion_model.h5")  # Pre-trained voice emotion model
voice_emotions = ['Angry', 'Neutral', 'Happy', 'Sad', 'Fear']

def detect_face_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48, 48))
        roi = roi / 255.0
        roi = np.reshape(roi, (1, 48, 48, 1))
        prediction = face_model.predict(roi)
        emotion = label_map[np.argmax(prediction)]
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        return emotion
    return "No Face Detected"

def record_audio(duration=3, fs=44100):
    print("Recording... Speak now!")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording finished!")
    return audio_data

def detect_voice_emotion(audio_data, fs=44100):
    mfccs = librosa.feature.mfcc(y=audio_data[:, 0], sr=fs, n_mfcc=40)
    mfccs = np.mean(mfccs.T, axis=0)
    mfccs = np.reshape(mfccs, (1, 40))
    prediction = voice_model.predict(mfccs)
    return voice_emotions[np.argmax(prediction)]

def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        face_emotion = detect_face_emotion(frame)
        
        cv2.imshow('Real-Time Emotion Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('v'):
            audio_data = record_audio()
            voice_emotion = detect_voice_emotion(audio_data)
            print(f"Voice Emotion: {voice_emotion}")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
