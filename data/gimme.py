import json

# Load data from the JSON file
with open('merged.json', 'r', encoding='utf-8') as f:
    schools_info = json.load(f)

# Initialize the new list for the desired output format
expanded_schools_info = []

# Iterate over each school and its specialized subjects
for school in schools_info:
    school_name = school['ten_truong']
    dia_chi = school['dia_chi']
    quan_huyen = school['quan_huyen']
    ghichu = school['ghichu']

    # For each specialized subject, create a new entry in the expanded list
    for mon in school['mon_chuyen']:
        expanded_schools_info.append({
            "name": school_name,
            "dia_chi": dia_chi,
            "quan_huyen": quan_huyen,
            "ghichu": ghichu,
            "monchuyen": mon['mon_chuyen'],
            "nv1": mon['nv1'],
            "nv2": mon['nv2'],
            "nv3": mon['nv3'],
            "isChuyen" : True
        })

# Save the expanded data to a new JSON file
with open('expanded_schools_info.json', 'w', encoding='utf-8') as f_out:
    json.dump(expanded_schools_info, f_out, ensure_ascii=False, indent=4)

print("Expansion completed. Check 'expanded_schools_info.json' for the result.")
