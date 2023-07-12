import pandas as pd
import json

# Load the JSON data
with open('techdata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Write the DataFrame to an Excel file
df.to_excel('techdata.xlsx', index_label='Name')
