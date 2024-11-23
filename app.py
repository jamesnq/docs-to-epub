import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from doc_converter import DocumentConverter, INPUT_DIR, OUTPUT_DIR

app = Flask(__name__)
app.secret_key = os.urandom(24)  # for flash messages

# Ensure upload folders exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'html', 'epub', 'md', 'markdown'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(INPUT_DIR, filename)
            file.save(input_path)
            
            try:
                converter = DocumentConverter()
                output_file = converter.convert_to_pub(input_path)
                
                # Get the filename from the full path
                output_filename = os.path.basename(output_file)
                
                flash(f'Successfully converted {filename} to {output_filename}')
                return redirect(url_for('download_file', filename=output_filename))
            except Exception as e:
                flash(f'Error converting file: {str(e)}')
                return redirect(request.url)
                
        else:
            flash('Allowed file types are: ' + ', '.join(ALLOWED_EXTENSIONS))
            return redirect(request.url)
            
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(OUTPUT_DIR, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
