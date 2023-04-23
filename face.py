from flask import Flask, request, jsonify
import cv2

app = Flask(__name__)


@app.route('/')
def detect_face():
    # Get the uploaded image from the request
    file = request.files['image']
    image = cv2.imdecode(np.fromstring(
        file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Perform face detection using OpenCV or face_recognition library
    # Extract the bounding box coordinates of the detected faces

    # Define the frame boundaries
    frame_left = 100
    frame_top = 100
    frame_right = 500
    frame_bottom = 500

    # Check if any face has left the frame
    for (x, y, w, h) in detected_faces:
        if x < frame_left or x + w > frame_right or y < frame_top or y + h > frame_bottom:
            # Face has left the frame, trigger appropriate action
            # For example, return a JSON response with status and message
            return jsonify({'status': 'face_left', 'message': 'Face has left the frame'})

    # If no face has left the frame, return a JSON response with status and message
    return jsonify({'status': 'face_detected', 'message': 'Face detected within frame'})


app.run(host='127.0.0.1', port=3030, debug=True)
