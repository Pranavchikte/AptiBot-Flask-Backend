import os
from PyPDF2 import PdfReader
import docx
from google.cloud import vision

# This code correctly looks for 'gcloud_credentials.json'
basedir = os.path.abspath(os.path.dirname(__file__))
credentials_path = os.path.join(basedir, '..', 'gcloud_credentials.json')

if os.path.exists(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    print("--- SUCCESS: Google credentials loaded successfully.")
else:
    print(f"--- CRITICAL FAILURE: Google credentials file not found at {credentials_path}")

def process_file(filepath: str) -> str:
    """Processes an uploaded file, extracts text based on extension."""
    _, extension = os.path.splitext(filepath)
    ext = extension.lower()

    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.docx':
        return extract_text_from_docx(filepath)
    elif ext in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(filepath)
    else:
        return f"Error: Unsupported file type '{ext}'."

def extract_text_from_pdf(filepath: str) -> str:
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(filepath)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return "Error: Could not read text from the PDF file."

def extract_text_from_docx(filepath: str) -> str:
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return "Error: Could not read text from the DOCX file."

def extract_text_from_image(filepath: str) -> str:
    """Detects document text in an image file using Google Cloud Vision."""
    try:
        client = vision.ImageAnnotatorClient()
        with open(filepath, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)
        return response.full_text_annotation.text
    except Exception as e:
        print(f"--- GOOGLE VISION API ERROR --- \n {e} \n -----------------------------")
        return "Error: Could not read text from the image file."