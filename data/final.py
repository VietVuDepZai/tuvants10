import json

# Paths to the input files
started_json_path = 'ho_chi_minh_high_schools.json'
another_json_path = 'output.json'

# Load the started JSON data from the file
with open(started_json_path, 'r', encoding='utf-8') as file:
    started_json = json.load(file)

# Load the another JSON data from the file
with open(another_json_path, 'r', encoding='utf-8') as file:
    another_json = json.load(file)

# Function to merge data based on the school name (ten_truong and Unnamed: 2)
for started_entry in started_json:
    for another_entry in another_json:
        if started_entry['ten_truong'].replace('Trường', '').strip().lower() == another_entry['Unnamed: 2'].strip().lower():
            started_entry['nv1'] = another_entry.get('Unnamed: 6', "")
            started_entry['nv2'] = another_entry.get('Unnamed: 10', "")
            started_entry['nv3'] = another_entry.get('Unnamed: 14', "")

# Output the merged result
merged_json_output_path = 'final.json'
with open(merged_json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(started_json, json_file, ensure_ascii=False, indent=4)

print(f"Merged JSON data has been saved to {merged_json_output_path}")
