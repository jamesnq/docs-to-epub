#!/usr/bin/env python3
import os
import sys
import mimetypes
import pypandoc
import ebooklib
from ebooklib import epub
from PIL import Image
import argparse
from pathlib import Path
import subprocess
import shutil
import datetime

# Define constants for directories
INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_books')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_books')

def ensure_directories():
    """Ensure input and output directories exist"""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_calibre():
    """Find Calibre's ebook-convert tool"""
    # Common installation paths
    possible_paths = [
        r"C:\Program Files\Calibre2\ebook-convert.exe",
        r"C:\Program Files (x86)\Calibre2\ebook-convert.exe",
        os.path.expanduser("~\\AppData\\Local\\Programs\\Calibre2\\ebook-convert.exe"),
        shutil.which('ebook-convert')
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            return path
    return None

def ensure_pandoc():
    """Ensure Pandoc is available, download if necessary"""
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("Pandoc not found. Downloading and installing...")
        pypandoc.download_pandoc()
        print("Pandoc installation complete!")

class DocumentConverter:
    def __init__(self):
        self.supported_formats = {
            'application/pdf': 'pdf',
            'application/msword': 'doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'text/plain': 'txt',
            'text/html': 'html',
            'application/epub+zip': 'epub',
            'text/markdown': 'md'
        }
        mimetypes.init()
        # Add markdown mime type if not registered
        mimetypes.add_type('text/markdown', '.md')
        mimetypes.add_type('text/markdown', '.markdown')
        
        # Ensure directories exist
        ensure_directories()
        
        # Ensure pandoc is available
        ensure_pandoc()
        
        # Find Calibre
        self.calibre_path = find_calibre()
        if not self.calibre_path:
            print("Warning: Calibre's ebook-convert tool not found. Please make sure Calibre is installed and try again.")
            print("Download Calibre from: https://calibre-ebook.com/download")
            print("After installation, you may need to restart your computer.")
            sys.exit(1)

    def detect_format(self, input_file):
        """Detect the input file format using mimetypes"""
        mime_type, _ = mimetypes.guess_type(input_file)
        if mime_type:
            return self.supported_formats.get(mime_type)
        # Fallback to extension-based detection
        ext = os.path.splitext(input_file)[1].lower().lstrip('.')
        return ext if ext in ['pdf', 'doc', 'docx', 'txt', 'html', 'epub', 'md', 'markdown'] else None

    def generate_output_filename(self, input_file):
        """Generate unique output filename with timestamp"""
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.pub"

    def convert_to_epub(self, input_file, output_file):
        """Convert input document to EPUB format"""
        input_format = self.detect_format(input_file)
        if not input_format:
            raise ValueError(f"Unsupported input format for file: {input_file}")

        # Convert to EPUB using pypandoc
        output_epub = output_file.replace('.pub', '.epub')
        pypandoc.convert_file(
            input_file,
            'epub',
            outputfile=output_epub,
            extra_args=['--extract-media=.']
        )
        return output_epub

    def convert_to_pub(self, input_file, output_file=None):
        """Main conversion method"""
        # Ensure input file exists
        if not os.path.exists(input_file):
            # Check if file exists in input directory
            input_path = os.path.join(INPUT_DIR, os.path.basename(input_file))
            if os.path.exists(input_path):
                input_file = input_path
            else:
                raise FileNotFoundError(f"Input file not found: {input_file}")

        # Generate output filename if not provided
        if not output_file:
            output_file = os.path.join(OUTPUT_DIR, self.generate_output_filename(input_file))

        try:
            # First convert to EPUB
            epub_file = self.convert_to_epub(input_file, output_file)
            
            # Convert EPUB to MOBI using Calibre's ebook-convert
            print("Converting to .pub format using Calibre...")
            mobi_file = epub_file.replace('.epub', '.mobi')
            
            # Run ebook-convert command
            result = subprocess.run([
                self.calibre_path,
                epub_file,
                mobi_file,
                '--output-profile=kindle'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Rename .mobi to .pub
                pub_file = mobi_file.replace('.mobi', '.pub')
                os.rename(mobi_file, pub_file)
                os.remove(epub_file)  # Clean up intermediate EPUB file
                print(f"Successfully converted {input_file} to {pub_file}")
            else:
                raise Exception(f"Conversion failed: {result.stderr}")

        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            raise

def list_input_files():
    """List all files in the input directory"""
    files = []
    for file in os.listdir(INPUT_DIR):
        if os.path.isfile(os.path.join(INPUT_DIR, file)) and not file.startswith('.'):
            files.append(file)
    return files

def interactive_mode():
    """Interactive mode for selecting files to convert"""
    while True:
        files = list_input_files()
        if not files:
            print("\nNo files found in input_books directory.")
            return

        print("\nAvailable files in input_books directory:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        
        print("\nOptions:")
        print("Enter a number to convert a file")
        print("'r' to refresh the list")
        print("'q' to quit")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == 'r':
            continue
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(files):
                    selected_file = files[index]
                    print(f"\nConverting: {selected_file}")
                    try:
                        converter = DocumentConverter()
                        converter.convert_to_pub(os.path.join(INPUT_DIR, selected_file))
                        input("\nPress Enter to continue...")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        input("\nPress Enter to continue...")
                else:
                    print("\nInvalid number. Please try again.")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter a number, 'r', or 'q'.")
                input("Press Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description='Convert documents to Kindle .pub format')
    parser.add_argument('input_file', nargs='?', help='Input document file (or "list" to show available files)')
    parser.add_argument('output_file', nargs='?', help='Output .pub file (optional)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Start in interactive mode')
    
    args = parser.parse_args()
    
    try:
        if args.interactive:
            interactive_mode()
            return
            
        if not args.input_file:
            interactive_mode()
            return
            
        if args.input_file.lower() == 'list':
            files = list_input_files()
            if files:
                print("\nAvailable files in input_books directory:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
            else:
                print("\nNo files found in input_books directory.")
            return

        converter = DocumentConverter()
        converter.convert_to_pub(args.input_file, args.output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
