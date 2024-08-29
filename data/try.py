import pandas as pd
import json

# Load the Excel file
file_path = 'chuyen.xlsx'
sheet_name = 'CHUYÊN'  # Adjust if your sheet has a different name

# Read the data starting from row 6
df = pd.read_excel(file_path, sheet_name=sheet_name, header=5)

# Create a dictionary to store the JSON data
data = []
print("Column names:", df.columns)
i = 0
# Iterate through the dataframe
for index, row in df.iterrows():
    print(row)
    school_name = row.iloc[0]  # First column for the school name
    monchuyen = row.iloc[1]  # Second column for "monchuyen"
    nv1 = row.iloc[3]  # Fourth column for nv1
    nv2 = row.iloc[5]  # Sixth column for nv2
    nv3 = row.iloc[7]  # Eighth column for nv3
    data.append({
        'name' : school_name,
        'monchuyen': monchuyen,
        'nv1': nv1,
        'nv2': nv2,
        'nv3': nv3
    })

# Save the data to a JSON file with UTF-8 encoding
with open('chuyenbest.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
