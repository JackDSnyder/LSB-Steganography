from flask import Blueprint, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from app.utils import textEncodingDecoding, imageEncodingDecoding
from app.utils.constants import defaultPassword

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
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Missing required fields'}), 400
    
    file = request.files['image']
    text = request.form['text']
    password = request.form.get('password', defaultPassword)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, f'encoded_{filename}')
        
        file.save(input_path)
        textEncodingDecoding.encodeText(input_path, output_path, text, password)
        
        return jsonify({'success': True, 'output_file': f'encoded_{filename}'})
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/decode-text', methods=['POST'])
def decode_text():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image file'}), 400
    
    file = request.files['image']
    password = request.form.get('password', defaultPassword)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        decoded_text = textEncodingDecoding.decodeText(file_path, password)
        return jsonify({'success': True, 'text': decoded_text})
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/encode-image', methods=['POST'])
def encode_image():
    if 'original' not in request.files or 'hidden' not in request.files:
        return jsonify({'error': 'Missing required files'}), 400
    
    original = request.files['original']
    hidden = request.files['hidden']
    password = request.form.get('password', defaultPassword)
    
    if original.filename == '' or hidden.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if original and hidden and allowed_file(original.filename) and allowed_file(hidden.filename):
        original_filename = secure_filename(original.filename)
        hidden_filename = secure_filename(hidden.filename)
        
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        hidden_path = os.path.join(UPLOAD_FOLDER, hidden_filename)
        output_path = os.path.join(UPLOAD_FOLDER, f'encoded_{original_filename}')
        
        original.save(original_path)
        hidden.save(hidden_path)
        
        imageEncodingDecoding.encodeImage(original_path, hidden_path, output_path, password)
        
        return jsonify({'success': True, 'output_file': f'encoded_{original_filename}'})
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/decode-image', methods=['POST'])
def decode_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image file'}), 400
    
    file = request.files['image']
    password = request.form.get('password', defaultPassword)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, f'decoded_{filename}')
        
        file.save(input_path)
        imageEncodingDecoding.decodeImage(input_path, output_path, password)
        
        return jsonify({'success': True, 'output_file': f'decoded_{filename}'})
    
    return jsonify({'error': 'Invalid file type'}), 400 