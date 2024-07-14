# Face Analysis Service

This project provides an API service for face analysis, including face detection, face recognition, face similarity check, gender detection, and emotion detection. The project utilizes TensorFlow, UltraFace model, and DeepFace.

## Features

- **Face Detection**: Detects faces in an image using the UltraFace model.
- **Face Recognition**: Detects faces, creates feature vectors, and checks similarity against enrolled images.
- **Face Similarity Check**: Detects faces from two different images and checks their similarity.
- **Gender Detection**: Identifies the gender of detected faces.
- **Emotion Detection**: Detects emotions on detected faces.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/marofES/faceAnalysisService.git
    cd faceAnalysisService
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run Project:
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 80
    ```
