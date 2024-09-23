import pandas as pd
import json
from difflib import SequenceMatcher


file_path = '/home/kugel/temp/js/klimaDashboard/public/data/karlsruhe/Kennzahlenwerte_zu_Maßnahme_mit.csv'
data = pd.read_csv(file_path, delimiter=';', on_bad_lines="warn")

# Selecting relevant columns and cleaning the data
data_clean = data[['Maßnahmen_ID', 'Kennzahl', 'Maßeinheit', 'Jahr', 'Wert']].copy()

# Drop rows with missing values in key columns
data_clean.dropna(subset=['Maßnahmen_ID', 'Kennzahl', 'Maßeinheit', 'Jahr', 'Wert'], inplace=True)

# Convert 'Jahr' and 'Wert' columns to appropriate types
data_clean['Jahr'] = pd.to_numeric(data_clean['Jahr'], errors='coerce')
data_clean['Wert'] = pd.to_numeric(data_clean['Wert'], errors='coerce')

# Drop any rows where Jahr or Wert couldn't be converted
data_clean.dropna(subset=['Jahr', 'Wert'], inplace=True)

# Now we will group the data by 'Maßnahmen_ID', 'Kennzahl', and 'Maßeinheit'
grouped = data_clean.groupby(['Maßnahmen_ID', 'Kennzahl', 'Maßeinheit'])

# Filter for groups that have at least 5 valid year-value pairs
valid_groups = grouped.filter(lambda x: len(x) >= 5)

# Create a JSON-like structure for grouping information
grouping_info = {
    group_name: {
        'Maßnahmen_ID': group_name[0],
        'Kennzahl': group_name[1],
        'Maßeinheit': group_name[2],
        'count': len(group)
    }
    for group_name, group in valid_groups.groupby(['Maßnahmen_ID', 'Kennzahl', 'Maßeinheit'])
}

# Convert tuple keys to strings for JSON compatibility
grouping_info_str_keys = {
    f"{group_name[0]}_{group_name[1]}_{group_name[2]}": group_data
    for group_name, group_data in grouping_info.items()
}

# Output grouping information in JSON format
grouping_info_json = json.dumps(grouping_info_str_keys, indent=4)

# Saving the JSON data to a file
json_file_path = './grouping_info.json'
with open(json_file_path, 'w') as json_file:
    json_file.write(grouping_info_json)

# Provide the path for download
print(json_file_path)

################ 
# Function to calculate similarity between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to check similarity by both title and context (same Maßnahmen_ID)
def is_contextually_similar(kennzahl_1, kennzahl_2, maßnahmen_id_1, maßnahmen_id_2):
    if maßnahmen_id_1 != maßnahmen_id_2:
        return False
    return similar(kennzahl_1, kennzahl_2) > 0.7 or ('Ökostrom' in kennzahl_1 and 'Ökostrom' in kennzahl_2)


# Grouping data by Maßnahmen_ID and Kennzahl for comparison
grouped_data = data_clean.groupby(['Maßnahmen_ID', 'Kennzahl', 'Maßeinheit']).size().reset_index()

# Threshold for similarity, set high to catch similar but not identical Kennzahlen
similarity_threshold = .8 #0.8


# Identifying related datasets based on both title similarity and context (same Maßnahmen_ID)
related_datasets = {}
for i, row_i in grouped_data.iterrows():
    for j, row_j in grouped_data.iterrows():
        if i != j and ((similar(row_i['Maßnahmen_ID'],row_j['Maßnahmen_ID']) >= similarity_threshold) or is_contextually_similar(row_i['Kennzahl'], row_j['Kennzahl'], row_i['Maßnahmen_ID'], row_j['Maßnahmen_ID'])):
            key = f"{row_i['Maßnahmen_ID']}_{row_i['Kennzahl']}"
            if key not in related_datasets:
                related_datasets[key] = {
                    'Maßnahmen_ID': row_i['Maßnahmen_ID'],
                    'Kennzahl_1': row_i['Kennzahl'],
                    'Maßeinheit_1': row_i['Maßeinheit'],
                    'Kennzahl_2': row_j['Kennzahl'],
                    'Maßeinheit_2': row_j['Maßeinheit'],
                }


# Removing duplicate pairs such as (a, b) and (b, a)
unique_related_datasets = {}

for key, value in related_datasets.items():
    # Create a sorted tuple of the two Kennzahl and Maßeinheit combinations to identify duplicates
    items = tuple(sorted([f"{value['Kennzahl_1']}|{value['Maßeinheit_1']}", f"{value['Kennzahl_2']}|{value['Maßeinheit_2']}"]))
    if items not in unique_related_datasets:
        unique_related_datasets[items] = value

# Adding the missing 'Maßnahmen_ID' back into the values for each related dataset
filtered_related_datasets_with_ids = {}
for key, value in unique_related_datasets.items():
    # Retrieve the Maßnahmen_ID from the grouped data (based on Kennzahl_1 and Maßeinheit_1)
    matching_row = grouped_data[
        (grouped_data['Kennzahl'] == value['Kennzahl_1']) &
        (grouped_data['Maßeinheit'] == value['Maßeinheit_1'])
    ]
    if not matching_row.empty:
        maßnahmen_id = matching_row.iloc[0]['Maßnahmen_ID']
        # Create the new key starting with Maßnahmen_ID
        new_key = f"{maßnahmen_id}_{value['Kennzahl_1']}_{value['Maßeinheit_1']}_{value['Kennzahl_2']}_{value['Maßeinheit_2']}"
        value['Maßnahmen_ID'] = maßnahmen_id
        filtered_related_datasets_with_ids[new_key] = value

# Export the modified related datasets into JSON format
related_datasets_with_ids_json = json.dumps(filtered_related_datasets_with_ids, indent=4)

# Save the modified JSON data to a file
#json_file_path_with_ids = '/mnt/data/related_datasets_with_ids.json'
json_file_path_with_ids = './related_datasets_with_ids.json'
with open(json_file_path_with_ids, 'w') as json_file:
    json_file.write(related_datasets_with_ids_json)

# Provide the path for download
print(json_file_path_with_ids)
