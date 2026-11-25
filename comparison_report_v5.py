import pandas as pd
import re

from datetime import datetime

from openpyxl import load_workbook
from openpyxl.styles import PatternFill

from extract_text import extract_text_from_pdf


# ==========================================
# Extract Connections from PDF
# ==========================================

def extract_connections(pdf_file):

    connections = []

    text = extract_text_from_pdf(pdf_file)

    cpu_pins = re.findall(
        r"CPU Pin:\s*(DQ\d+)",
        text
    )

    memory_pins = re.findall(
        r"Memory Pin:\s*(DQ\d+)",
        text
    )

    for cpu, mem in zip(
        cpu_pins,
        memory_pins
    ):

        connections.append(
            (cpu, mem)
        )

    return connections


# ==========================================
# Input Files
# ==========================================

reference_file = "ComparePDFs/set 2_ref.pdf"
test_file = "ComparePDFs/set 2_test.pdf"


# ==========================================
# Extract Data
# ==========================================

reference_data = extract_connections(reference_file)
test_data = extract_connections(test_file)

reference_df = pd.DataFrame(
    reference_data,
    columns=[
        "CPU Pin",
        "Memory Pin"
    ]
)

test_df = pd.DataFrame(
    test_data,
    columns=[
        "CPU Pin",
        "Memory Pin"
    ]
)

with pd.ExcelWriter(
    "Structured_Dataset_Review.xlsx",
    engine="openpyxl"
) as writer:

    reference_df.to_excel(
        writer,
        sheet_name="Reference Dataset",
        index=False
    )

    test_df.to_excel(
        writer,
        sheet_name="Test Dataset",
        index=False
    )

print(
    "Structured Dataset Review File Generated:"
)

print(
    "Structured_Dataset_Review.xlsx"
)
# ==========================================
# Comparison Logic
# ==========================================

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


# ==========================================
# Statistics
# ==========================================

total_records = len(results)

matches = sum(
    1 for row in results
    if row["Status"] == "MATCH"
)

mismatches = sum(
    1 for row in results
    if row["Status"] == "MISMATCH"
)

if total_records > 0:
    match_rate = (matches / total_records) * 100
else:
    match_rate = 0

comparison_time = datetime.now().strftime(
    "%d-%b-%Y %H:%M:%S"
)


# ==========================================
# DataFrames
# ==========================================

detail_df = pd.DataFrame(results)

discrepancies_df = detail_df[
    detail_df["Status"] == "MISMATCH"
]

summary_df = pd.DataFrame({

    "Metric": [

        "Comparison Date",
        "Reference File",
        "Test File",
        "Total Records",
        "Matches",
        "Mismatches",
        "Match Rate (%)"

    ],

    "Value": [

        comparison_time,
        reference_file,
        test_file,
        total_records,
        matches,
        mismatches,
        round(match_rate, 2)

    ]

})


# ==========================================
# Export Workbook
# ==========================================

output_file = "PDF_Comparison_Report_v5.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    summary_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    detail_df.to_excel(
        writer,
        sheet_name="Detailed Results",
        index=False
    )

    discrepancies_df.to_excel(
        writer,
        sheet_name="Discrepancies Only",
        index=False
    )


# ==========================================
# Excel Formatting
# ==========================================

wb = load_workbook(output_file)

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

for sheet_name in [

    "Detailed Results",
    "Discrepancies Only"

]:

    ws = wb[sheet_name]

    for row in ws.iter_rows(min_row=2):

        status_cell = row[3]

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

        ws.column_dimensions[
            column_letter
        ].width = max_length + 2

    # Filters

    ws.auto_filter.ref = ws.dimensions


# ==========================================
# Summary Sheet Formatting
# ==========================================

summary_ws = wb["Summary"]

for column in summary_ws.columns:

    max_length = 0

    column_letter = column[0].column_letter

    for cell in column:

        if cell.value:

            max_length = max(
                max_length,
                len(str(cell.value))
            )

    summary_ws.column_dimensions[
        column_letter
    ].width = max_length + 4

summary_ws.auto_filter.ref = summary_ws.dimensions


wb.save(output_file)


# ==========================================
# Console Output
# ==========================================

print("\n========================================")
print("PDF COMPARISON REPORT V5 GENERATED")
print("========================================")

print(f"Reference File : {reference_file}")
print(f"Test File      : {test_file}")
print(f"Total Records  : {total_records}")
print(f"Matches        : {matches}")
print(f"Mismatches     : {mismatches}")
print(f"Match Rate     : {match_rate:.2f}%")

print(f"\nSaved As: {output_file}")