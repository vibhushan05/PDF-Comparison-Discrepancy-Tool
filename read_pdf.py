import pdfplumber

with pdfplumber.open("sample.pdf") as pdf:

    for page_num, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        print(f"\n--- PAGE {page_num} ---\n")
        print(text)