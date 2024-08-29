import json

# Function to load JSON data from a file
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Function to merge or create new data
def merge_data(provided_data, default_data):
    merged_list = []

    for default_item in default_data:
        for provided_item in provided_data:
            if provided_item['name'] == default_item['ten_truong']:
                # Merge data
                new_entry = {
                    'ten_truong': provided_item['name'],
                    'dia_chi': default_item['dia_chi'],
                    'quan_huyen': default_item['quan_huyen'],
                    'ghichu': default_item['ghichu'],
                    'nv1': provided_item['nv1'],
                    'nv2': provided_item['nv2'],
                    'nv3': provided_item['nv3'],
                    'isChuyen': default_item['isChuyen'],
                    'monchuyen': 'Tích hợp'
                }
                merged_list.append(new_entry)
                break
        

    return merged_list

# Load the provided data from tichhop.json and the default data from best.json
provided_data = load_json('tichhop.json')
default_data = load_json('best.json')

# Merging the data
merged_result = merge_data(provided_data, default_data)

# Output the merged result to the console
print(json.dumps(merged_result, ensure_ascii=False, indent=4))

# Optionally, save the merged result to a new file
save_json('mergedtichhop.json', merged_result)
