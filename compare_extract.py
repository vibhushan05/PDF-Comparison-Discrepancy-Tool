import pdfplumber

files = [
    "ComparePDFs/reference.pdf",
    "ComparePDFs/test.pdf"
]

for file in files:

    print("\n================================")
    print(f"FILE: {file}")
    print("================================\n")

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            print(text)