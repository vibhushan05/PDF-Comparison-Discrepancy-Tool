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

from openpyxl import load_workbook
from openpyxl.styles import PatternFill

wb = load_workbook("PDF_Comparison_Report.xlsx")
ws = wb.active

green_fill = PatternFill(
    start_color="90EE90",
    end_color="90EE90",
    fill_type="solid"
)

red_fill = PatternFill(
    start_color="FF9999",
    end_color="FF9999",
    fill_type="solid"
)

for row in ws.iter_rows(min_row=2):

    status_cell = row[3]  # Status column

    if status_cell.value == "MATCH":
        status_cell.fill = green_fill

    elif status_cell.value == "MISMATCH":
        status_cell.fill = red_fill

# Auto-fit columns
for column in ws.columns:

    max_length = 0
    column_letter = column[0].column_letter

    for cell in column:

        if cell.value:

            max_length = max(
                max_length,
                len(str(cell.value))
            )

    ws.column_dimensions[column_letter].width = max_length + 2

# Add filters
ws.auto_filter.ref = ws.dimensions

wb.save("PDF_Comparison_Report.xlsx")