from ocr import extract_text
from database import save_document

image_path = "sample.jpeg"

text = extract_text(image_path)

print("Extracted Text:\n", text)

save_document("sample.jpeg", text)

print("\nSaved to database successfully!")