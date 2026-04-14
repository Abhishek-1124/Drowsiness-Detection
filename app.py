import streamlit as st
import tensorflow as tf
import cv2
import numpy as np

# Load the trained model
model = tf.keras.models.load_model("drowsiness_model.keras")
class_names = ['Awake', 'Drowsy']  # Adjust if needed

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to preprocess the face ROI and detect eyes
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return None, frame, False  # No face detected

    # Choose the largest face
    x, y, w, h = max(faces, key=lambda b: b[2]*b[3])
    face_roi = frame[y:y+h, x:x+w]
    gray_face = gray[y:y+h, x:x+w]

    # Eye detection within the face ROI
    eyes = eye_cascade.detectMultiScale(gray_face)
    eyes_open = len(eyes) >= 1  # At least one eye is open

    # Draw face bounding box
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Preprocess face for model
    img = cv2.resize(face_roi, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    return img, frame, eyes_open

# Streamlit App
st.title("🛑 Real-Time Drowsiness Detection (Eye-Aware)")
run = st.checkbox("Start Webcam")

FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to capture frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        processed_img, output_frame, eyes_open = preprocess_frame(frame_rgb)

        if processed_img is not None:
            prediction = model.predict(processed_img)[0]
            label = class_names[np.argmax(prediction)]

            # If eyes are detected open, override label to 'Awake'
            if eyes_open:
                label = "Awake"
        else:
            label = "No Face Detected"

        # Display the final label
        cv2.putText(output_frame, f'Status: {label}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        FRAME_WINDOW.image(output_frame)

    cap.release()
else:
    st.write("Click the checkbox to start webcam.")
