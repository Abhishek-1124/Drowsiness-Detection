import streamlit as st
import tensorflow as tf
import cv2
import numpy as np

# Load the trained model
model = tf.keras.models.load_model("drowsiness_model.keras")

# Define class names used during training
class_names = ['Awake', 'Drowsy']  # Update if needed

# Load OpenCV's Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to extract face ROI and preprocess
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return None, frame  # No face found

    # Select the largest detected face (most prominent)
    x, y, w, h = max(faces, key=lambda b: b[2]*b[3])
    face = frame[y:y+h, x:x+w]

    # Draw bounding box for visual feedback
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Resize and normalize
    img = cv2.resize(face, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    return img, frame

# Streamlit UI
st.title("🛑 Real-Time Drowsiness Detection")
run = st.checkbox("Start Webcam")

FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to capture frame.")
            break

        # Convert BGR (OpenCV default) to RGB (required by TensorFlow & Streamlit)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get face ROI and preprocessed image
        processed_img, output_frame = preprocess_frame(frame_rgb)

        if processed_img is not None:
            # Predict with model
            prediction = model.predict(processed_img)[0]
            label = class_names[np.argmax(prediction)]
        else:
            label = "No Face Detected"

        # Show prediction on screen
        cv2.putText(output_frame, f'Status: {label}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Show the frame in Streamlit
        FRAME_WINDOW.image(output_frame)

    cap.release()
else:
    st.write("Click the checkbox to start webcam.")
