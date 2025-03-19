from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from textEncodingDecoding import encodeText, decodeText
from imageEncodingDecoding import encodeImage, decodeImage
from helper import padImage
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode-text', methods=['POST'])
def encode_text():
    try:
        if 'image' not in request.files or 'text' not in request.form:
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        image = request.files['image']
        text = request.form['text']
        password = request.form.get('password', '')
        
        if image.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        if not image.filename.lower().endswith('.png'):
            return jsonify({'success': False, 'error': 'Only PNG images are supported'})
        
        # Process image in memory
        image_data = image.read()
        image_io = BytesIO(image_data)
        
        # Create output buffer
        output_io = BytesIO()
        
        # Encode the text
        success = encodeText(image_io, text, output_io, password)
        
        if success:
            output_io.seek(0)
            return send_file(
                output_io,
                mimetype='image/png',
                as_attachment=True,
                download_name='encoded_image.png'
            )
        else:
            return jsonify({'success': False, 'error': 'Failed to encode text'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decode-text', methods=['POST'])
def decode_text():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        image = request.files['image']
        password = request.form.get('password', '')
        
        if image.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        if not image.filename.lower().endswith('.png'):
            return jsonify({'success': False, 'error': 'Only PNG images are supported'})
        
        # Process image in memory
        image_data = image.read()
        image_io = BytesIO(image_data)
        
        # Decode the text
        text = decodeText(image_io, password)
        
        if text is not None:
            return jsonify({
                'success': True,
                'text': text
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to decode text'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/encode-image', methods=['POST'])
def encode_image():
    try:
        if 'original' not in request.files or 'hidden' not in request.files:
            return jsonify({'success': False, 'error': 'Missing required images'})
        
        original = request.files['original']
        hidden = request.files['hidden']
        password = request.form.get('password', '')
        
        if original.filename == '' or hidden.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        if not original.filename.lower().endswith('.png') or not hidden.filename.lower().endswith('.png'):
            return jsonify({'success': False, 'error': 'Only PNG images are supported'})
        
        # Process images in memory
        original_data = original.read()
        hidden_data = hidden.read()
        original_io = BytesIO(original_data)
        hidden_io = BytesIO(hidden_data)
        
        # Create output buffer
        output_io = BytesIO()
        
        # Encode the image
        success = encodeImage(original_io, hidden_io, output_io, password)
        
        if success:
            output_io.seek(0)
            return send_file(
                output_io,
                mimetype='image/png',
                as_attachment=True,
                download_name='encoded_image.png'
            )
        else:
            return jsonify({'success': False, 'error': 'Failed to encode image'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decode-image', methods=['POST'])
def decode_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        image = request.files['image']
        password = request.form.get('password', '')
        
        if image.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        if not image.filename.lower().endswith('.png'):
            return jsonify({'success': False, 'error': 'Only PNG images are supported'})
        
        # Process image in memory
        image_data = image.read()
        image_io = BytesIO(image_data)
        
        # Create output buffer
        output_io = BytesIO()
        
        # Decode the image
        success = decodeImage(image_io, output_io, password)
        
        if success:
            output_io.seek(0)
            return send_file(
                output_io,
                mimetype='image/png',
                as_attachment=True,
                download_name='decoded_image.png'
            )
        else:
            return jsonify({'success': False, 'error': 'Failed to decode image'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 