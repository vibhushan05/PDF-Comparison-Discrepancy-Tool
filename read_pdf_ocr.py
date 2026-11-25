from pdf2image import convert_from_path
import pytesseract

# Tell Python exactly where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_path = "ComparePDFs/reference.pdf"

pages = convert_from_path(
    pdf_path,
    poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
)

for page_num, page in enumerate(pages, start=1):

    text = pytesseract.image_to_string(page)

    print(f"\n--- PAGE {page_num} ---\n")

    print(text)