import logging
from pathlib import Path
import PyPDF2
import docx
import csv
import json
import zipfile
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)

# Mappings for file readers
FILE_READERS = {
    '.pdf': 'read_pdf_file',
    '.docx': 'read_docx_file',
    '.csv': 'read_csv_file',
    '.json': 'read_json_file',
    '.zip': 'read_zip_file',
    '.png': 'read_image_file',
    '.jpg': 'read_image_file',
    '.jpeg': 'read_image_file',
    '.tiff': 'read_image_file',
    '.txt': 'read_text_file',
    '.md': 'read_text_file'
}

def read_local_file(file_path: Path) -> str:
    """Read content from a file, determining the appropriate method based on the file type."""
    if not file_path.exists() or not file_path.is_file():
        logger.error(f"File {file_path} does not exist or is not a file.")
        return ""
    
    suffix = file_path.suffix.lower()
    reader_function = globals().get(FILE_READERS.get(suffix))
    
    if reader_function:
        return reader_function(file_path)
    else:
        logger.warning(f"Unsupported file type: {suffix}. Returning empty content.")
        return ""

def read_pdf_file(file_path: Path) -> str:
    """Extract text from a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = "".join(page.extract_text() for page in reader.pages)
        logger.info(f"Successfully extracted content from PDF {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read PDF file {file_path}: {e}")
        return ""

def read_docx_file(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        content = "\n".join(para.text for para in doc.paragraphs)
        logger.info(f"Successfully extracted content from DOCX {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read DOCX file {file_path}: {e}")
        return ""

def read_csv_file(file_path: Path) -> str:
    """Extract text from a CSV file."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            reader = csv.reader(file)
            content = "\n".join(", ".join(row) for row in reader)
        logger.info(f"Successfully extracted content from CSV {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read CSV file {file_path}: {e}")
        return ""

def read_json_file(file_path: Path) -> str:
    """Extract content from a JSON file."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            content = json.dumps(json.load(file), indent=4)
        logger.info(f"Successfully extracted content from JSON {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        return ""

def read_zip_file(file_path: Path) -> str:
    """Extract and concatenate text content from files within a ZIP archive."""
    try:
        content = []
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as file:
                    content.append(f"\nFile: {file_name}\n" + file.read().decode('utf-8'))
        logger.info(f"Successfully extracted content from ZIP {file_path}")
        return "".join(content)
    except Exception as e:
        logger.error(f"Failed to read ZIP file {file_path}: {e}")
        return ""

def read_image_file(file_path: Path) -> str:
    """Extract text from an image file using OCR."""
    try:
        image = Image.open(file_path)
        content = pytesseract.image_to_string(image)
        logger.info(f"Successfully extracted text from image {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read image file {file_path}: {e}")
        return ""

def read_text_file(file_path: Path) -> str:
    """Read content from a plain text or markdown file."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            content = file.read()
        logger.info(f"Successfully read content from text file {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to read text file {file_path}: {e}")
        return ""

def ensure_dir(directory: Path):
    """Ensure that a directory exists; create it if it doesn't."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    except Exception as e:
        logger.critical(f"Failed to create directory {directory}: {e}")
        raise
