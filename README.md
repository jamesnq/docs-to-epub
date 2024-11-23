# Document to Kindle (.pub) Converter

A Python application that converts various document formats (PDF, DOCX, TXT, etc.) to Kindle-compatible .pub format.

## Online Version

Try it online at: [https://docs-to-pub.onrender.com](https://docs-to-pub.onrender.com)

Simply upload your document and get a Kindle-compatible .pub file in return. The online version supports all the same formats as the local version.

## Local Installation

### Prerequisites

- Python 3.7 or higher
- Pandoc (will be automatically installed if missing)
- Calibre (must be installed on your system)

### Installation

1. Install Calibre from: https://calibre-ebook.com/download
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

### Directory Structure

- `input_books/`: Place your source documents here
- `output_books/`: Converted .pub files will be saved here

### Usage

1. Place your documents in the `input_books` directory

2. Start the converter in one of these ways:

   a. Interactive Mode (recommended):
   ```bash
   python doc_converter.py
   ```
   or
   ```bash
   python doc_converter.py -i
   ```
   This will show a menu where you can:
   - Select a file by number to convert it
   - Press 'r' to refresh the file list
   - Press 'q' to quit

   b. List available files:
   ```bash
   python doc_converter.py list
   ```

   c. Convert a specific file:
   ```bash
   python doc_converter.py filename.pdf
   ```
   or
   ```bash
   python doc_converter.py filename.pdf output.pub
   ```

If no output filename is specified, the converter will generate one automatically with a timestamp.

## Supported Input Formats

- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Text files (.txt)
- HTML (.html, .htm)
- ePub (.epub)
- Markdown (.md, .markdown)
- And more (see Pandoc documentation for full list)

## Notes

- The output will be in .pub format, compatible with Kindle devices
- Images and formatting will be preserved where possible
- Large files may take longer to process
- Each conversion creates a unique file with a timestamp to prevent overwriting

## Self-Hosting

The application can be self-hosted on any platform that supports Python. The repository includes configuration for Render.com deployment.

## Contributing

Feel free to open issues or submit pull requests on GitHub.
