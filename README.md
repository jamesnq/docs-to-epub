# Document to EPUB Converter

A web application that converts various document formats (PDF, DOCX, TXT) to EPUB format, suitable for e-readers including Kindle devices.

## Online Version

Try it online at: [https://kindleconverter.onrender.com](https://kindleconverter.onrender.com)

Simply upload your document and get an EPUB file in return. The online version supports PDF, DOCX, and TXT files.

## Features

- Easy-to-use web interface
- Supports multiple input formats:
  * PDF (.pdf)
  * Microsoft Word (.docx)
  * Text files (.txt)
- Converts to EPUB format
- Preserves document structure:
  * Maintains paragraphs from DOCX files
  * Preserves page breaks from PDF files
  * Formats plain text for readability
- Clean, modern interface
- Instant download of converted files
- No installation required

## File Format Support

### Input Formats
- PDF (.pdf)
  * Extracts text content
  * Maintains page structure
  * Preserves basic formatting

- Microsoft Word (.docx)
  * Preserves paragraphs
  * Maintains text content
  * Converts basic formatting

- Text (.txt)
  * Converts plain text
  * Adds basic formatting
  * Creates readable e-book structure

### Output Format
- EPUB (.epub)
  * Universal e-book format
  * Compatible with most e-readers
  * Works with Kindle devices (through Amazon's conversion)
  * Maintains document structure
  * Includes table of contents

## Using with Kindle

While this tool outputs EPUB files, you can easily use them with your Kindle:

1. Send the EPUB file to your Kindle email address
2. Amazon will automatically convert it to Kindle format
3. The converted book will appear in your Kindle library

Alternatively, you can use Calibre on your local machine to convert EPUB to MOBI/AZW3 format.

## Local Development

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install via pip):
  ```
  pip install -r requirements.txt
  ```

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/jamesnq/docs-to-epub.git
   cd docs-to-epub
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and visit `http://localhost:5000`

## Contributing

Feel free to open issues or submit pull requests on [GitHub](https://github.com/jamesnq/docs-to-epub). Some areas for improvement:

- Add support for more input formats
- Improve conversion quality
- Enhance formatting preservation
- Add batch conversion capabilities
- Implement more styling options

## License

This project is open source and available under the MIT License.
