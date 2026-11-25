from extract_text import extract_text_from_pdf

text = extract_text_from_pdf(
    "ComparePDFs/reference.pdf"
)

print("\nEXTRACTED CONTENT:\n")

print(text)