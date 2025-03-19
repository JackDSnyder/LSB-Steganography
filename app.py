from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from textEncodingDecoding import encodeText, decodeText
from imageEncodingDecoding import encodeImage, decodeImage
from helper import padImage
import time
import glob

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['TEMP_FOLDER'] = 'static/temp'
app.config['MAX_AGE'] = 3600  # 1 hour in seconds

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

def cleanup_old_files():
    """Remove files older than MAX_AGE from both temp and upload folders"""
    current_time = time.time()
    
    # Clean temp folder
    temp_files = glob.glob(os.path.join(app.config['TEMP_FOLDER'], '*'))
    for file_path in temp_files:
        if os.path.getmtime(file_path) < current_time - app.config['MAX_AGE']:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temp file {file_path}: {e}")
    
    # Clean upload folder (except for the current output files)
    upload_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for file_path in upload_files:
        if os.path.getmtime(file_path) < current_time - app.config['MAX_AGE']:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting upload file {file_path}: {e}")

def save_temp_file(file, prefix=''):
    """Save a file to temp folder with unique name"""
    timestamp = int(time.time())
    filename = f"{prefix}_{timestamp}_{secure_filename(file.filename)}"
    filepath = os.path.join(app.config['TEMP_FOLDER'], filename)
    file.save(filepath)
    return filepath

def cleanup_output_file(filepath):
    """Schedule output file for cleanup"""
    try:
        # Set the file's modification time to MAX_AGE seconds ago
        # This will make it eligible for cleanup in the next cleanup cycle
        os.utime(filepath, (time.time() - app.config['MAX_AGE'], time.time() - app.config['MAX_AGE']))
    except Exception as e:
        print(f"Error scheduling cleanup for {filepath}: {e}")

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
        
        # Clean up old files
        cleanup_old_files()
        
        # Save the uploaded image temporarily
        image_path = save_temp_file(image, 'input')
        
        # Generate output filename
        output_filename = 'encoded_image.png'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Encode the text
        success = encodeText(image_path, text, output_path, password)
        
        # Clean up temp file
        try:
            os.remove(image_path)
        except:
            pass
        
        if success:
            # Schedule the output file for cleanup
            cleanup_output_file(output_path)
            return jsonify({
                'success': True,
                'output_file': output_filename
            })
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
        
        # Clean up old files
        cleanup_old_files()
        
        # Save the uploaded image temporarily
        image_path = save_temp_file(image, 'input')
        
        # Decode the text
        text = decodeText(image_path, password)
        
        # Clean up temp file
        try:
            os.remove(image_path)
        except:
            pass
        
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
        
        # Clean up old files
        cleanup_old_files()
        
        # Save the uploaded images temporarily
        original_path = save_temp_file(original, 'original')
        hidden_path = save_temp_file(hidden, 'hidden')
        
        # Generate output filename
        output_filename = 'encoded_image.png'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Encode the image
        success = encodeImage(original_path, hidden_path, output_path, password)
        
        # Clean up temp files
        try:
            os.remove(original_path)
            os.remove(hidden_path)
        except:
            pass
        
        if success:
            # Schedule the output file for cleanup
            cleanup_output_file(output_path)
            return jsonify({
                'success': True,
                'output_file': output_filename
            })
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
        
        # Clean up old files
        cleanup_old_files()
        
        # Save the uploaded image temporarily
        image_path = save_temp_file(image, 'input')
        
        # Generate output filename
        output_filename = 'decoded_image.png'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Decode the image
        success = decodeImage(image_path, output_path, password)
        
        # Clean up temp file
        try:
            os.remove(image_path)
        except:
            pass
        
        if success:
            # Schedule the output file for cleanup
            cleanup_output_file(output_path)
            return jsonify({
                'success': True,
                'output_file': output_filename
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to decode image'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 
    app.run(debug=True) 