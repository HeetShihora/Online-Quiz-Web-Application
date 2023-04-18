import os
import cv2
import csv
import openpyxl


def detect_face_in_frame(frame, frame_region):
    # Load the face detection classifier
    face_cascade = cv2.CascadeClassifier(
        'C:/Users/HEET/Desktop/psc/haarcascade_frontalface_default.xml')

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.1, minNeighbors=5)

    # Draw a rectangle in the specified frame region
    x, y, w, h = frame_region
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Check if any detected face falls within the specified frame region
    face_in_frame = False
    for (x, y, w, h) in faces:
        if x > frame_region[0] and y > frame_region[1] and x + w < frame_region[2] and y + h < frame_region[3]:
            face_in_frame = True
            break

    # Display a message if the detected face is not within the specified frame region
    if not face_in_frame:
        cv2.putText(frame, 'Please keep your face within the frame', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Face detection', frame)


# Open the video stream from the user's camera
cap = cv2.VideoCapture(0)

# Set the frame region in which the face should be detected
frame_region = (100, 100, 500, 500)


def start_detection():
    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Detect faces in the frame and check if the detected face falls within the specified region
        detect_face_in_frame(frame, frame_region)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
