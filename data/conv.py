import pandas as pd
import json

# Load the Excel file
file_path = 'diem.xlsx'
df = pd.read_excel(file_path)

# Select only the desired columns
selected_columns = df[['      ỦY BAN NHÂN DÂN QUẬN 11','Unnamed: 2','Unnamed: 6', 'Unnamed: 10', 'Unnamed: 14']]

# Drop rows where all selected columns are NaN
selected_columns = selected_columns.dropna(how='all')

# Convert the selected data to JSON format
json_data = selected_columns.to_dict(orient='records')

# Save the JSON data to a file
json_output_path = 'output.json'
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print(f"Data has been successfully converted to JSON and saved to {json_output_path}")
