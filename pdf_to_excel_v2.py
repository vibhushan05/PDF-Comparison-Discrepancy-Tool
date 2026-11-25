import pdfplumber
import pandas as pd
import re

def validate(cpu_pin, memory_pin):

    cpu_num = int(cpu_pin.replace("DQ", ""))
    mem_num = int(memory_pin.replace("DQ", ""))

    if abs(cpu_num - mem_num) <= 7:
        return "PASS"

    return "INVALID"


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

            status = validate(cpu, mem)

            records.append({
                "CPU Pin": cpu,
                "Memory Pin": mem,
                "Status": status
            })


df = pd.DataFrame(records)

df.to_excel(
    "memory_validation_report.xlsx",
    index=False
)

print("Validation report generated!")