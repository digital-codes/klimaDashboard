import pandas as pd
import json


# Create a DataFrame
df = pd.read_csv("../public/data/karlsruhe/Kennzahlenwerte_zu_Maßnahme_mit.csv",sep=";",decimal=",")

# Define variables for the column names
"""
Maßnahmen_ID	Maßnahmen_Bez	Um was geht es?	Details	Kennzahl	Maßeinheit	Jahr	Wert
"""
col_l1 = 'Maßnahmen_ID'
col_l2 = 'Kennzahl'
col_unit = 'Maßeinheit'
col_date = 'Jahr'
col_value = 'Wert'
col_grpid = "Gruppe"

def isNum(x):
    return pd.to_numeric(x, errors='coerce')

def colId(x):
    if isinstance(x,str):
        return x.strip()
    else:
        return ""


# Convert date column to datetime using the variable
df[col_date] = pd.to_datetime(df[col_date])

# clean level columns
for c in [col_l1, col_l2,col_unit]:
    df[c] = df[c].map(colId)

# Create a new column with a unique identifier for each group based on l1, l2, and unit
df[col_grpid] = df[col_l1].astype(str) + '_' + df[col_l2].astype(str) + '_' + df[col_unit].astype(str)

# Display the DataFrame with the new group_id column
print(df)

# Group by new column
grouped = df.groupby(col_grpid)


# Initialize the result list
result = []

# Iterate over each group
for grpid, group in grouped:
    total_rows = len(group)
    valid_rows = group[col_value].map(isNum).count()  # Count rows where 'value' is not NaN
    
    # Extracting unique values of l1, l2, unit, date, value for the group
    columns_data = {
        col_l1: group[col_l1].unique().tolist()[0].strip(),
        col_l2: group[col_l2].unique().tolist()[0].strip(),
        col_unit: colId(group[col_unit].unique().tolist()[0])
    }
    # Append the result as a dictionary
    result.append({
        'grpid': grpid,
        'total_rows': int(total_rows),
        'valid_rows': int(valid_rows),
         'columns': columns_data
        })

# Convert the result to JSON format
json_result = json.dumps(result, indent=4)

# Print the JSON result
print(json_result)

rdf = pd.DataFrame(result)
# drop below 4 valid rows
rdf = rdf[rdf['valid_rows'] >= 4]

rdf.to_json("groupinfo.json",orient="records")

# second step
# Now, create a list where we group by l1 and unit, and collect distinct l2 values
l1_unit_l2_result = []

# Group by col_l1 and col_unit and collect distinct col_l2 values
l1_unit_grouped = df.groupby([col_l1, col_unit])

for (l1, unit), group in l1_unit_grouped:
    unique_l2 = group[col_l2].unique().tolist()
    
    # Append a dictionary with l1, unit, and list of unique l2 values
    l1_unit_l2_result.append({
        col_l1: l1,
        col_unit: unit,
        'unique_l2_values': unique_l2
    })

# Convert the results to JSON format
json_result = json.dumps(l1_unit_l2_result, indent=4)

# Print the JSON result
print(json_result)

rdf2 = pd.DataFrame(l1_unit_l2_result)
rdf2.to_json("group2info.json",orient="records")


# third step, find all massnahmen with multiple entries
l1_groups = rdf2.groupby(by=col_l1).groups
multi_groups = [z for z in l1_groups if len(l1_groups[z]) > 1]
print("Multi:",multi_groups)

for m in multi_groups:
    df = rdf2[rdf2[col_l1] == m]
    df.to_json(f"group_{m}.json",orient="records")
    print(f"Group {m}: {len(df)} items")
    
