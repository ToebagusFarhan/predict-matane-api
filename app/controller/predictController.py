import os
from flask import Blueprint, request, jsonify
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array, load_img
from google.cloud import storage
import tempfile

from app.utils.apiauth import amIAllowed

# Flask Blueprint for predict-related routes
predict_controller = Blueprint("predict_controller", __name__)

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

model_path = "app\model\Matane_Model.h5"
model = load_model(filepath=model_path)
print("Model Exist:", os.path.exists(model_path))

def predict():
    if not amIAllowed():
        return jsonify({"error": "You are not allowed to access this route"}), 401
    
    if "image" not in request.files:
        return jsonify({"error": "There's no file here boi, don't eat it swiper!"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            img = load_img(temp_file.name, target_size=(224, 224))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array)
            hasil_index = np.argmax(predictions)
            hasil = hasil_mapping.get(hasil_index, "invalid")

            return jsonify({"result": hasil})
    except Exception as e:
        return jsonify({"error": str(e)}), 500