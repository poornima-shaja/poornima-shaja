from flask import Flask, render_template, Response, jsonify, request
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Load YOLO model
model = YOLO('yolov8s.pt')  # Load YOLOv8 small model

# Open webcam
cap = cv2.VideoCapture(0)

# A function to detect objects and generate scene description
def generate_scene_description(frame):
    results = model(frame)
    
    # Initialize variables
    detected_objects = []
    colors = []

    # Process the results
    for result in results[0].boxes.data:  # Each detected object
        class_id = int(result[5])  # Class ID (category)
        label = results[0].names[class_id]  # Object name
        confidence = result[4].item()  # Confidence score

        if confidence > 0.5:  # Only consider detections with a confidence higher than 50%
            detected_objects.append(label)
            # Example for car color, could be refined later
            if 'car' in label:
                colors.append("red")  # Replace with actual detection logic if needed
    
    # Generate scene description
    scene_description = "Surroundings: "
    
    # Describe detected objects
    if len(detected_objects) > 0:
        scene_description += f"There are {len(detected_objects)} objects detected: {', '.join(detected_objects)}."
        if 'car' in detected_objects:
            scene_description += f" There is a {colors[0]} car detected."  # Example for car color (could be refined)
        if 'person' in detected_objects:
            scene_description += " A person is walking nearby."
    else:
        scene_description += "No objects detected."
    
    return detected_objects, colors, scene_description

# A function to answer questions about detected objects
def answer_question(question, detected_objects, colors):
    if "how many cars" in question.lower():
        car_count = detected_objects.count("car")  # Count how many cars are detected
        return f"There are {car_count} cars detected."
    
    if "color of the car" in question.lower():
        car_colors = [color for obj, color in zip(detected_objects, colors) if obj == "car"]
        if car_colors:
            return f"The color of the car is {car_colors[0]}."
        else:
            return "No car detected."
    
    if "how many people" in question.lower():
        person_count = detected_objects.count("person")  # Count how many people are detected
        return f"There are {person_count} people detected."
    
    return "I'm sorry, I couldn't understand that question."

# Video streaming and answering questions
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Generate scene description
        detected_objects, colors, description = generate_scene_description(frame)
        
        # Resize frame to 640x480 before encoding for streaming
        frame_resized = cv2.resize(frame, (640, 480))
        ret, buffer = cv2.imencode('.jpg', frame_resized)
        if ret:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to serve video stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to handle user questions (e.g., "How many cars?")
@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question', default="", type=str)
    
    # Use the last frame and detected objects to generate an answer
    detected_objects, colors, _ = generate_scene_description(cap.read()[1])  # Use current frame
    answer = answer_question(question, detected_objects, colors)

    return jsonify({'answer': answer})

# Route to get scene description
@app.route('/get_description', methods=['GET'])
def get_description():
    # Generate description based on the latest camera frame
    detected_objects, colors, description = generate_scene_description(cap.read()[1])
    return jsonify({'description': description})

@app.route('/')
def index():
    return render_template('inde.html')

if __name__ == '__main__':
    app.run(debug=True)
