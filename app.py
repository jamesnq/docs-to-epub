from flask import Flask, request, render_template, send_file, flash, redirect
import os
import pypandoc
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'html', 'epub', 'md'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)
            
            try:
                # Create a temporary directory for output
                with tempfile.TemporaryDirectory() as temp_dir:
                    output_filename = os.path.splitext(filename)[0] + '.epub'
                    output_path = os.path.join(temp_dir, output_filename)
                    
                    # Convert to epub using pypandoc
                    pypandoc.convert_file(
                        input_path,
                        'epub',
                        outputfile=output_path,
                        extra_args=['--epub-chapter-level=2']
                    )
                    
                    # Clean up input file
                    os.remove(input_path)
                    
                    # Send the converted file
                    return send_file(
                        output_path,
                        as_attachment=True,
                        download_name=output_filename,
                        mimetype='application/epub+zip'
                    )
            
            except Exception as e:
                flash(f'Error converting file: {str(e)}')
                if os.path.exists(input_path):
                    os.remove(input_path)
                return redirect(request.url)
        else:
            flash('Allowed file types are: ' + ', '.join(ALLOWED_EXTENSIONS))
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
