import pandas as pd
import json

df = pd.read_excel('techdata.xlsx')

# Convert the DataFrame back to JSON and save it
data = df.to_dict(orient='records')
data1 = {}
for i in data:
    for da in i.items():
        if "[" in str(da[1]):
            li = da[1][1:-1].split(",")
            li = [int(x) for x in li]
            i[da[0]] = li
    name = i["Name"]
    del i["Name"]
    data1[name] = i
print(data1)
with open('techdata.json', 'w', encoding='utf-8') as f:
    json.dump(data1, f, ensure_ascii=False)
