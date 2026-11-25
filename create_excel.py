import pandas as pd

data = {
    "CPU Pin": ["DQ0", "DQ1", "DQ2"],
    "Memory Pin": ["DQ4", "DQ5", "DQ6"]
}

df = pd.DataFrame(data)

df.to_excel(
    "memory_connections.xlsx",
    index=False
)

print("Excel file created successfully!")