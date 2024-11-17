import os
from flask import Blueprint, request, jsonify
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.utils import img_to_array, load_img
from google.cloud import storage
import numpy as np
import tempfile

# Flask Blueprint for predict-related routes
predict_controller = Blueprint("predict_controller", __name__)

# Load model function
def load_model_from_source(local_path=None, gcs_bucket=None, gcs_blob=None):
    """
    Load the model from a local file or Google Cloud Storage.
    """
    if local_path and os.path.exists(local_path):
        # Load from local path
        return load_model(local_path)
    elif gcs_bucket and gcs_blob:
        # Download from GCS and load
        client = storage.Client()
        bucket = client.get_bucket(gcs_bucket)
        blob = bucket.blob(gcs_blob)

        # Temporarily store the model file locally
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=True) as temp_model_file:
            blob.download_to_filename(temp_model_file.name)
            return load_model(temp_model_file.name)
    else:
        raise ValueError("Invalid model source. Provide either a local_path or GCS bucket/blob.")

# Predict function
def predict(image_path, model):
    """
    Perform prediction on a given image using the loaded model.
    """
    # Preprocess the image
    img = load_img(image_path, target_size=(224, 224))  # Adjust target_size to match your model
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict
    predictions = model.predict(img_array)
    return predictions

# Route to handle prediction requests
def handle_predict_request():
    """
    Receive an image from the user, process it, and return the prediction.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    # Get the file from the request
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as temp_image_file:
            file.save(temp_image_file.name)

            # Load the model (adjust path/bucket/blob as needed)
            model = load_model_from_source(
                local_path="model.h5",  # Replace with your actual local model path
                gcs_bucket="your-gcs-bucket-name",
                gcs_blob="your-gcs-model-file.h5",
            )

            # Perform prediction
            predictions = predict(temp_image_file.name, model)

        # Construct the response
        return jsonify({
            "predictions": predictions.tolist(),  # Convert numpy array to list
            "message": "Prediction successful"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
