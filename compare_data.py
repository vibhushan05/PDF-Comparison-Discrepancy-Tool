import pdfplumber
import re

def extract_connections(pdf_file):

    connections = []

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            cpu_pins = re.findall(
                r"CPU Pin:\s*(DQ\d+)",
                text
            )

            memory_pins = re.findall(
                r"Memory Pin:\s*(DQ\d+)",
                text
            )

            for cpu, mem in zip(cpu_pins, memory_pins):

                connections.append(
                    (cpu, mem)
                )

    return connections


reference_data = extract_connections(
    "ComparePDFs/reference.pdf"
)

test_data = extract_connections(
    "ComparePDFs/test.pdf"
)

print("REFERENCE DATA")
print(reference_data)

print("\nTEST DATA")
print(test_data)