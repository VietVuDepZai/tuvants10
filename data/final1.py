import json

# Read the JSON file
with open('final.json', 'r', encoding='utf-8') as infile:
    schools = json.load(infile)

# Process the data
for school in schools:
    # Check if all nv fields are blank
    is_chuyen = (school.get('nv1', '') == "" and school.get('nv2', '') == "" and school.get('nv3', '') == "")
    school["isChuyen"] = is_chuyen

# Write the modified data to a new JSON file
with open('best.json', 'w', encoding='utf-8') as outfile:
    json.dump(schools, outfile, indent=4, ensure_ascii=False)

print("Data has been processed and saved to output.json")
