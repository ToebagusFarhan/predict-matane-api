import os
from flask import Blueprint, request, jsonify, render_template
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array, load_img
from google.cloud import storage
import tempfile

from app.utils.apiauth import amIAllowed

# Flask Blueprint for predict-related routes
predict_controller = Blueprint("predict_controller", __name__)

# little test for /
def home():
    if not amIAllowed():
        return render_template("error/401.html"), 401
    return jsonify({"message": "Hello, World!"})

hasil_mapping = {
    0: "Katarak: Dengan Tingkat Immature",
    1: "Mata Anda Sehat, Tidak Mengalami Katarak, dan Infeksi Mata Kering",
    2: "Katarak: Dengan Tingkat Mature",
    3: "Diabetic Retinopathy: Dengan Tingkat Mild",
    4: "Diabetic Retinopathy: Dengan Tingkat Moderate",
    5: "Diabetic Retinopathy: Dengan Tingkat Normal",
    6: "Diabetic Retinopathy: Dengan Tingkat Proliferate",
    7: "Diabetic Retinopathy: Dengan Tingkat Severe",
    8: "Infeksi Mata Kering"
}

if os.environ.get("Environment") == "production":
    model_path = "/mnt/bucket/models/model.h5"
    model = load_model(model_path)
else:
    model_path = "app/model-local/model.h5"
    model = load_model(model_path)

def predict():
    if not amIAllowed():
        return render_template("error/401.html"), 401
    
    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)

            # Validate image type
            import imghdr
            file_type = imghdr.what(temp_file.name)
            if file_type not in ["jpeg", "png", "bmp"]:
                return jsonify({"error": "Unsupported file format"}), 400

            # Preprocess image
            img = load_img(temp_file.name, target_size=(224, 224))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            predictions = model.predict(img_array)
            hasil_index = np.argmax(predictions)
            hasil = hasil_mapping.get(hasil_index, "Error,  Invalid result")

            return jsonify({"result": hasil})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure temp file cleanup
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
