import os
import pdfplumber
import pandas as pd
import re

records = []

pdf_folder = "PDFs"

for filename in os.listdir(pdf_folder):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(pdf_folder, filename)

        with pdfplumber.open(pdf_path) as pdf:

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

                    records.append({
                        "Source File": filename,
                        "CPU Pin": cpu,
                        "Memory Pin": mem
                    })

df = pd.DataFrame(records)

df.to_excel(
    "combined_report.xlsx",
    index=False
)

print("Combined report generated!")