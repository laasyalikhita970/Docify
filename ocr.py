import pytesseract
from PIL import Image
from docx import Document
import pdfplumber
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    # IMAGE FILES
    if ext in [".png", ".jpg", ".jpeg"]:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    # PDF FILES
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
        # DOCX FILES
    elif ext == ".docx":
        doc = Document(file_path)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    else:
        return "Unsupported file type"