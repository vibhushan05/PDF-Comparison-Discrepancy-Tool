import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_path = "ComparePDFs/reference.pdf"

# -----------------------------
# Try pdfplumber first
# -----------------------------

extracted_text = ""

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text


# -----------------------------
# If text exists, use it
# -----------------------------

if extracted_text.strip():

    print("TEXT PDF DETECTED")
    print("\nEXTRACTED CONTENT:\n")
    print(extracted_text)

# -----------------------------
# Otherwise use OCR
# -----------------------------

else:

    print("IMAGE PDF DETECTED")
    print("RUNNING OCR...\n")

    pages = convert_from_path(
        pdf_path,
        poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
    )

    ocr_text = ""

    for page in pages:

        ocr_text += pytesseract.image_to_string(page)

    print("OCR EXTRACTED CONTENT:\n")
    print(ocr_text)