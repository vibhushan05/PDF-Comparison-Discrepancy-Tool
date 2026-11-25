import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler location
POPPLER_PATH = (
    r"C:\poppler\poppler-26.02.0\Library\bin"
)


def extract_text_from_pdf(pdf_path):

    extracted_text = ""

    # Try pdfplumber first
    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text

    # Text PDF detected
    if extracted_text.strip():

        print(f"{pdf_path} -> TEXT PDF")

        return extracted_text

    # OCR fallback
    print(f"{pdf_path} -> IMAGE PDF (OCR)")

    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    ocr_text = ""

    for page in pages:

        ocr_text += pytesseract.image_to_string(page)

    return ocr_text