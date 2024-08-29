import json

# Load the JSON data from the input file
with open('best.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Filter the data to include only schools with isChuyen set to true
filtered_data = [
    {**school, "mon_chuyen": ""}
    for school in data
    if school.get("isChuyen", False)
]

# Save the filtered data to the output file
with open('chuyen.json', 'w', encoding='utf-8') as output_file:
    json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

print("Filtered data saved to output.json")
