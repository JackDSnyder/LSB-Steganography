from flask import Blueprint, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from app.utils import textEncodingDecoding, imageEncodingDecoding
from app.utils.constants import defaultPassword
from io import BytesIO

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/encode-text', methods=['POST'])
def encode_text():
    try:
        # Get form data
        image = request.files['image']
        text = request.form['text']
        password = request.form.get('password', '')

        # Read image data into memory
        image_data = BytesIO(image.read())
        output_data = BytesIO()

        # Encode text in image
        textEncodingDecoding.encodeText(image_data, text, output_data, password)
        output_data.seek(0)

        # Send the encoded image directly
        return send_file(
            output_data,
            mimetype='image/png',
            as_attachment=True,
            download_name='encoded_image.png'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/decode-text', methods=['POST'])
def decode_text():
    try:
        print("Received decode-text request")
        print("Files:", request.files)
        print("Form data:", request.form)
        
        # Get form data
        if 'image' not in request.files:
            print("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
            
        image = request.files['image']
        if image.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400
            
        password = request.form.get('password', '')
        print(f"Processing image: {image.filename}, password: {password}")

        # Read image data into memory
        image_data = BytesIO(image.read())

        # Decode text from image
        text = textEncodingDecoding.decodeText(image_data, password)
        
        if text == "Incorrect passcode.":
            return jsonify({'error': 'Incorrect password. Please try again.'}), 400
        elif text == '':
            return jsonify({'error': 'No text found in the image.'}), 400
        else:
            return jsonify({'text': text})

    except Exception as e:
        print(f"Decoding error: {str(e)}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 400

@bp.route('/encode-image', methods=['POST'])
def encode_image():
    try:
        # Get form data
        original_image = request.files['original']
        hidden_image = request.files['hidden']
        password = request.form.get('password', '')

        # Read image data into memory
        original_data = BytesIO(original_image.read())
        hidden_data = BytesIO(hidden_image.read())
        output_data = BytesIO()

        # Encode hidden image in original image
        imageEncodingDecoding.encodeImage(original_data, hidden_data, output_data, password)
        output_data.seek(0)

        # Send the encoded image directly
        return send_file(
            output_data,
            mimetype='image/png',
            as_attachment=True,
            download_name='encoded_image.png'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/decode-image', methods=['POST'])
def decode_image():
    try:
        # Get form data
        encoded_image = request.files['image']
        password = request.form.get('password', '')

        # Read image data into memory
        encoded_data = BytesIO(encoded_image.read())
        output_data = BytesIO()

        # Decode hidden image
        imageEncodingDecoding.decodeImage(encoded_data, output_data, password)
        output_data.seek(0)

        # Send the decoded image directly
        return send_file(
            output_data,
            mimetype='image/png',
            as_attachment=True,
            download_name='decoded_image.png'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 400 