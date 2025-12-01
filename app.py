from flask import Flask, render_template, request, send_file, jsonify
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from helper_functions import encode, decode_image
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode_message():
    if 'image' not in request.files or 'message' not in request.form or 'password' not in request.form:
        return jsonify({'error': "Missing data"}), 400

    image = request.files['image']
    message = request.form['message']
    password = request.form['password']

    # Read image into memory
    image_bytes = BytesIO(image.read())
    image_pil = Image.open(image_bytes).convert("RGB")

    # Convert PIL image to OpenCV format
    img = np.array(image_pil)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Encode message
    encoded_img = encode(img, message, password)

    # Convert OpenCV image back to bytes
    _, encoded_buffer = cv2.imencode(".png", encoded_img)
    encoded_io = BytesIO(encoded_buffer)

    encoded_image_base64 = base64.b64encode(encoded_io.getvalue()).decode('utf-8')
    encoded_image_data_url = f"data:image/png;base64,{encoded_image_base64}"

    return jsonify({'encoded_image': encoded_image_data_url})

@app.route('/decode', methods=['POST'])
def decode_message():
    if 'image' not in request.files or 'password' not in request.form:
        return jsonify({'error': "Missing image or password"}), 400

    image = request.files['image']
    password = request.form['password']

    # Read image into memory
    image_bytes = BytesIO(image.read())
    image_pil = Image.open(image_bytes).convert("RGB")

    # Convert PIL image to OpenCV format
    img = np.array(image_pil)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Decode message
    decoded_message = decode_image(img, password)

    return jsonify({'decoded_message': decoded_message})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)