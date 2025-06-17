import requests
import pdfplumber
import pandas as pd
import os

# Step 1: Download the PDF file from a URL
pdf_url = "https://taggs.hhs.gov/Content/Data/HHS_Grants_Terminated.pdf"
local_pdf_path = "data.pdf"  # This will be saved in your current working directory

# Download and save the file
response = requests.get(pdf_url)
with open(local_pdf_path, "wb") as f:
    f.write(response.content)

# Step 2: Extract tables using pdfplumber in "lattice" mode
# Extract tables
all_tables = []


with pdfplumber.open(local_pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        table = page.extract_table({
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines"
        })

        if table:
            if i == 0:
              headers = table[0]
              data = table[1:]
            else:
              data = table
             # Normalize row lengths
            data = [row[:len(headers)] + [""] * (len(headers) - len(row)) if len(row) < len(headers) else row[:len(headers)] for row in data]

            # Convert to DataFrame
            df = pd.DataFrame(data, columns=headers)
            print(f"Page {i +1} → {len(df.columns)} columns: {df.columns.tolist()}")
            df["page"] = i + 1
            all_tables.append(df)


combined_df = pd.concat(all_tables, ignore_index= True)

combined_df.to_csv("hhs_grants.csv", index = False)

print("Current working directory:", os.getcwd())
