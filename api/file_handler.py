from flask import Blueprint, request, jsonify
import os

from werkzeug.utils import secure_filename

file_api = Blueprint("file_api", __name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'json'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check valid file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to handle file upload
@file_api.route('/upload', methods=['POST'])
def upload_file():
    from api.analyzer import analyze_file  # 🔥 Import inside function to prevent circular import

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"No selected file"}), 400


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Call analysis function
        analysis_result = analyze_file(filepath)

        return jsonify({'message': 'File uploaded successfully', 'analysis': analysis_result}), 200

    return jsonify({'error': 'Invalid file type'}), 400
