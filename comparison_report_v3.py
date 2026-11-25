import pdfplumber
import pandas as pd
import re


# ==========================================
# Extract Data From PDF
# ==========================================

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


# ==========================================
# Load PDFs
# ==========================================

reference_file = "ComparePDFs/reference.pdf"
test_file = "ComparePDFs/test.pdf"

reference_data = extract_connections(reference_file)
test_data = extract_connections(test_file)


# ==========================================
# Compare Data
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
# Summary Statistics
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


# ==========================================
# Create DataFrames
# ==========================================

detail_df = pd.DataFrame(results)

summary_df = pd.DataFrame({
    "Metric": [
        "Reference File",
        "Test File",
        "Total Records",
        "Matches",
        "Mismatches",
        "Match Rate (%)"
    ],
    "Value": [
        reference_file,
        test_file,
        total_records,
        matches,
        mismatches,
        round(match_rate, 2)
    ]
})


# ==========================================
# Export to Excel
# ==========================================

output_file = "PDF_Comparison_Report_v3.xlsx"

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


print("\n===================================")
print("Comparison Report Generated")
print("===================================")

print(f"Reference File : {reference_file}")
print(f"Test File      : {test_file}")
print(f"Total Records  : {total_records}")
print(f"Matches        : {matches}")
print(f"Mismatches     : {mismatches}")
print(f"Match Rate     : {match_rate:.2f}%")

print(f"\nSaved As: {output_file}")