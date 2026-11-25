import pdfplumber
import pandas as pd
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

                connections.append((cpu, mem))

    return connections


reference_data = extract_connections(
    "ComparePDFs/reference.pdf"
)

test_data = extract_connections(
    "ComparePDFs/test.pdf"
)

results = []

for ref, test in zip(reference_data, test_data):

    ref_cpu, ref_mem = ref
    test_cpu, test_mem = test

    if ref == test:
        status = "MATCH"
    else:
        status = "MISMATCH"

    results.append({
        "CPU Pin": ref_cpu,
        "Reference Pin": ref_mem,
        "Test Pin": test_mem,
        "Status": status
    })

df = pd.DataFrame(results)

df.to_excel(
    "PDF_Comparison_Report.xlsx",
    index=False
)

print("Comparison report generated successfully!")