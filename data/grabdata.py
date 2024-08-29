from bs4 import BeautifulSoup
import requests
import json
import re

# Function to format the address string
def format_address(address):
    # Replace multiple spaces with a single space
    address = re.sub(r'\s+', ' ', address)
    # Ensure space between numbers and text, but avoid space around slashes and commas
    address = re.sub(r'(\d)([^\d\s/,\d])', r'\1 \2', address)  # Number followed by non-digit, non-slash, non-comma
    address = re.sub(r'([^\d\s/,\d])(\d)', r'\1 \2', address)  # Non-digit, non-slash, non-comma followed by number
    return address.strip()

# Function to format district names
def format_district(district):
    # Capitalize "quận" to "Quận", ensuring consistency in district names
    district = re.sub(r'\bquận\b', 'Quận', district, flags=re.IGNORECASE)
    return district

# Fetch the webpage content
url = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_trung_h%E1%BB%8Dc_ph%E1%BB%95_th%C3%B4ng_t%E1%BA%A1i_Th%C3%A0nh_ph%E1%BB%91_H%E1%BB%93_Ch%C3%AD_Minh"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Initialize list to hold all school data
school_data = []

# Parse the table data
tables = soup.find_all("table", {"class": "wikitable"})

for table in tables:
    # Extract header text for use as fallback district value from <th colspan="6"> and <th colspan="5">
    headers_6 = table.find_all("th", {"colspan": "6"})
    headers_5 = table.find_all("th", {"colspan": "5"})
    header_text = ""

    # Use the header text as a fallback for district if no specific district is found
    if headers_6:
        header_text = headers_6[0].get_text(strip=True)  # Extract text from <th colspan="6">
    elif headers_5:
        header_text = headers_5[0].get_text(strip=True)  # Extract text from <th colspan="5">

    # Skip the header row and process each subsequent row in the table
    rows = table.find_all("tr")[1:]
    for row in rows:
        columns = row.find_all("td")
        # Check if the row has at least 3 columns (ensures valid data)
        if len(columns) >= 3:
            school_name = columns[0].get_text(strip=True)  # School name from the first column
            address = format_address(columns[2].get_text(strip=True))  # Address from the third column
            school_name.replace("Thể dục Thể thao", "TDTT")
            school_name.replace("TP.HCM", "")
            # Extract district information starting from the word "Quận" or "TP. Thủ Đức"
            district_match = re.search(r"quận.*|Quận.*|TP\.\s*Thủ\s*Đức", address, re.IGNORECASE)
            district = district_match.group() if district_match else header_text  # Use header as fallback if needed
            district = format_district(district)  # Format district name
            # Store the school information in a dictionary
            if len(columns) > 4: 
                school_info = {
                    "ten_truong": school_name,
                    "dia_chi": address,
                    "quan_huyen": district,
                    "ghichu": columns[4].get_text(strip=True),
                    "nv1": "",
                    "nv2": "",
                    "nv3": "",
                }
                school_data.append(school_info)  # Append the dictionary to the list
            else:
                school_info = {
                    "ten_truong": school_name,
                    "dia_chi": address,
                    "quan_huyen": district,
                    "ghichu": "",
                    "nv1": "",
                    "nv2": "",
                    "nv3": "",
                }
                school_data.append(school_info)  # Append the dictionary to the list

# Convert the list of dictionaries to JSON format and save it to a file
with open("ho_chi_minh_high_schools.json", "w", encoding="utf-8") as f:
    json.dump(school_data, f, ensure_ascii=False, indent=4)

print("Data has been saved to ho_chi_minh_high_schools.json")
