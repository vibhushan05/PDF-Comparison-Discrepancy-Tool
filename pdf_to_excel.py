import pdfplumber
import pandas as pd
import re

records = []

with pdfplumber.open("sample.pdf") as pdf:

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
                "CPU Pin": cpu,
                "Memory Pin": mem
            })

df = pd.DataFrame(records)

df.to_excel(
    "pin_connections.xlsx",
    index=False
)

print("Report generated successfully!")