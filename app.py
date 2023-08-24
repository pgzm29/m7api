from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import subprocess

app = Flask(__name__, static_folder='./dist', static_url_path="/")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if not os.path.isfile('model.keras'):
    subprocess.run(
        ['curl --output model.keras --location "https://github.com/pgzm29/m7api/raw/ba52b73aedd7e284a129472cc74da59f77c22432/pneumonia_model.keras"'], shell=True)


@app.route('/api/healthcheck')
def healthcheck():
    return jsonify({'status': 'healthy'})


@app.route('/api/predict', methods=['POST'])
def predict():
    # Load the trained model
    model_path = './model.keras'
    model = tf.keras.models.load_model(model_path, compile=False)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Load and preprocess the image
    img = Image.open(file)  # type: ignore
    img = img.convert('RGB')  # Convert to RGB color mode
    # Resize to match the input size of your model
    img = img.resize((128, 128))
    img_array = np.array(img) / 255.0   # Normalize

    # Make a prediction
    pred = model.predict(np.expand_dims(img_array, axis=0))  # type: ignore

    # Interpret prediction
    prediction = 'Pneumonia' if pred[0][0] >= 0.5 else 'Normal'

    return jsonify({'prediction': prediction})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
