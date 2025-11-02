from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import cv2
import clip
import torch
from PIL import Image
import numpy as np

app = Flask(__name__)

# Check if GPU is available and use it for both YOLO and CLIP
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load YOLO model on GPU
model = YOLO('yolov8s.pt').to(device)  # Ensure YOLO uses GPU

# Load CLIP model
clip_model, preprocess = clip.load("ViT-B/32", device)

# Global variables to store the latest frame and caption
latest_frame = None
latest_caption = "No caption available yet."

# Function to generate caption using YOLO and CLIP
def generate_caption(frame, detected_objects):
    object_description = ", ".join(detected_objects) if detected_objects else "No objects detected"

    # Preprocess the image and the object description for CLIP
    image = Image.fromarray(frame)
    text_inputs = clip.tokenize([object_description]).to(device)
    image_input = preprocess(image).unsqueeze(0).to(device)

    # Get image and text features from CLIP
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        text_features = clip_model.encode_text(text_inputs)

    # Calculate similarity between image and text
    similarity = (image_features @ text_features.T).squeeze(0)
    caption = object_description if similarity.item() > 0 else "No relevant caption found."

    return caption

# Webcam video stream
def generate_frames():
    global latest_frame, latest_caption
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return  # Exit if camera is not available

    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Failed to capture frame.")
            break  # Exit loop if frame capture fails

        if frame is None or frame.size == 0:
            print("Error: Invalid frame captured.")
            continue  # Skip to next frame if the current frame is invalid

        # Downscale frame for faster processing (e.g., 320x240)
        frame_resized = cv2.resize(frame, (320, 240))

        # Perform object detection every frame
        results = model(frame_resized)

        # Get detected objects (e.g., bottles, people, etc.)
        detected_objects = []
        for result in results[0].boxes.data:  # Get object boxes
            class_id = int(result[5])  # Class ID (category)
            confidence = result[4].item()  # Confidence score
            label = results[0].names[class_id]  # Object name
            detected_objects.append(label)

        # Generate caption using YOLO and CLIP
        if frame_count % 5 == 0:
            latest_caption = generate_caption(frame_resized, detected_objects)

        # Annotate the frame with detected objects
        object_description = ", ".join(detected_objects)
        cv2.putText(frame, f"Objects: {object_description}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        latest_frame = frame  # Store the latest frame

        # Resize frame to 640x480 before encoding for streaming
        frame_resized = cv2.resize(frame, (640, 480))
        ret, buffer = cv2.imencode('.jpg', frame_resized)
        if ret:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_count += 1

    cap.release()  # Release the camera when done

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/caption')
def get_caption():
    global latest_caption
    return jsonify({'caption': latest_caption})

if __name__ == '__main__':
    app.run(debug=True)

