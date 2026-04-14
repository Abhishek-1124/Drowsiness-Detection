# Real-Time Drowsiness Detection

This project is a Streamlit-based real-time drowsiness detection app that uses:
- A trained TensorFlow/Keras model (`drowsiness_model.keras`)
- OpenCV webcam capture
- Haar cascade face (and optional eye) detection

It predicts whether a person is **Awake** or **Drowsy** from live webcam frames.

## Project Files

- `app.py`: Main app with face + eye-aware logic.
  - Detects face and eyes.
  - If eyes are detected open, it can override prediction to `Awake`.
- `app1.py`: Simpler version using face detection + model prediction only.
- `drowsiness_model.keras`: Trained model used by both apps.

## Requirements

- Python 3.9+ (recommended)
- Webcam access
- Linux/macOS/Windows

Python packages:
- `streamlit`
- `tensorflow`
- `opencv-python`
- `numpy`

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install streamlit tensorflow opencv-python numpy
```

## Run the App

Run the eye-aware version:

```bash
streamlit run app.py
```

Or run the basic version:

```bash
streamlit run app1.py
```

Then open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How It Works (High Level)

1. Capture frame from webcam.
2. Detect face using Haar cascade.
3. Crop and preprocess face image to `224x224`.
4. Normalize and pass to the Keras model.
5. Show predicted status (`Awake` / `Drowsy`) on-screen.
6. In `app.py`, eye detection is also used to improve practical behavior.

## Notes

- Ensure `drowsiness_model.keras` stays in the project root next to the app files.
- If webcam does not open, check camera permissions and if another app is using it.
- Performance and accuracy depend on lighting, camera quality, and model training quality.
