from flask import Flask, request, render_template, send_file, flash, redirect
import os
from werkzeug.utils import secure_filename
import tempfile
from docx import Document
from PyPDF2 import PdfReader
import ebooklib
from ebooklib import epub
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create uploads directory in the same directory as the script
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_docx_to_epub(input_path):
    # Read DOCX
    doc = Document(input_path)
    
    # Create EPUB book
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Converted Document')
    book.set_language('en')
    
    # Add default style
    style = '''
        body { font-family: Times, Times New Roman, serif; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Convert content
    chapters = []
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip():  # Skip empty paragraphs
            c = epub.EpubHtml(title=f'Para_{i}', file_name=f'chapter_{i}.xhtml', lang='en')
            c.content = f'<p>{para.text}</p>'
            book.add_item(c)
            chapters.append(c)
    
    # Create table of contents
    book.toc = chapters
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create spine
    book.spine = ['nav'] + chapters
    
    # Save EPUB
    output_path = os.path.splitext(input_path)[0] + '.epub'
    epub.write_epub(output_path, book, {})
    return output_path

def convert_pdf_to_epub(input_path):
    # Read PDF
    reader = PdfReader(input_path)
    
    # Create EPUB book
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Converted PDF')
    book.set_language('en')
    
    # Add default style
    style = '''
        body { font-family: Times, Times New Roman, serif; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Convert content
    chapters = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text.strip():  # Skip empty pages
            c = epub.EpubHtml(title=f'Page_{i+1}', file_name=f'page_{i+1}.xhtml', lang='en')
            c.content = f'<div>{text}</div>'
            book.add_item(c)
            chapters.append(c)
    
    # Create table of contents
    book.toc = chapters
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create spine
    book.spine = ['nav'] + chapters
    
    # Save EPUB
    output_path = os.path.splitext(input_path)[0] + '.epub'
    epub.write_epub(output_path, book, {})
    return output_path

def convert_txt_to_epub(input_path):
    # Read text file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create EPUB book
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Converted Text')
    book.set_language('en')
    
    # Add default style
    style = '''
        body { font-family: Times, Times New Roman, serif; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Convert content
    c = epub.EpubHtml(title='Content', file_name='content.xhtml', lang='en')
    c.content = f'<div>{content}</div>'
    book.add_item(c)
    
    # Create table of contents
    book.toc = [c]
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create spine
    book.spine = ['nav', c]
    
    # Save EPUB
    output_path = os.path.splitext(input_path)[0] + '.epub'
    epub.write_epub(output_path, book, {})
    return output_path

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
                # Convert based on file type
                file_ext = filename.rsplit('.', 1)[1].lower()
                if file_ext == 'docx':
                    output_path = convert_docx_to_epub(input_path)
                elif file_ext == 'pdf':
                    output_path = convert_pdf_to_epub(input_path)
                elif file_ext == 'txt':
                    output_path = convert_txt_to_epub(input_path)
                
                # Clean up input file
                os.remove(input_path)
                
                # Send the converted file
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=os.path.basename(output_path),
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
