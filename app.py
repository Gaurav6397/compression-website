from flask import Flask, request, send_file, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dummy image compression function (replace with your algorithm)
def compress_image(input_image_path, output_image_path):
    # Open an image file
    with Image.open(input_image_path) as img:
        # Perform the compression (for demonstration, we'll just save it as is)
        img.save(output_image_path, 'JPEG', quality=20)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)
        file.save(input_path)
        
        # Call your compression function here
        compress_image(input_path, output_path)
        
        # Redirect to the download page
        return redirect(url_for('download_file', filename='compressed_' + filename))

@app.route('/download/<filename>')
def download_file(filename):
    return render_template('download.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
