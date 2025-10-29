import pandas as pd

# Path to your CSV file
csv_file = "C:\\Users\\Nimish\\Downloads\\train.csv"

# Path to your desired Excel file
excel_file = "C:\\Users\\Nimish\\Downloads\\train.xlsx"

# Read CSV
df = pd.read_csv(csv_file)

# Save as Excel
df.to_excel(excel_file, index=False, engine='openpyxl')

print("✅ Successfully converted CSV to Excel:", excel_file)
