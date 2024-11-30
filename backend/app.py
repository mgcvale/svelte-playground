import string
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS, cross_origin
import random
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
IMAGE_PREFIX_SIZE = 16
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_PREFIX_SIZE'] = IMAGE_PREFIX_SIZE

def generate_random_string(n: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@cross_origin
@app.route('/images/upload', methods = ["POST"])
def upload_image():

    files = request.files
    if "image" not in files:
        return jsonify({"error": "no file provided"}), 400
    image = files['image']

    if not image.filename:
        return jsonify({"error": "Invalid file provided"}), 400

    filename = generate_random_string(app.config['IMAGE_PREFIX_SIZE']) + "_" + image.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    return jsonify({"message": "succes", "filename": filename}), 200

@cross_origin
@app.route('/images/<image_name>', methods=["GET"])
def serve_image(image_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_name, mimetype="image/jpeg")

@cross_origin
@app.route('/images/preview/<image_name>', methods=["GET"])
def serve_preview(image_name):
    image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
    max_size = (360, 360)
    image.thumbnail(max_size)
    image = image.convert('RGB')

    img_io = BytesIO()
    image.save(img_io, format="JPEG", quality=40, optimize=True)
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype="image/jpeg",
    )



@cross_origin
@app.route('/images/delete/<image_name>', methods=["DELETE"])
def delete_image(image_name):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': 'success'}), 200
    else:
        return jsonify({'message': 'File not found'}), 404

@cross_origin
@app.route("/images/all", methods=["GET"])
def get_all_images():
    return jsonify({"images": [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]}), 200
