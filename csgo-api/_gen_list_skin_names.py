"""
Generates a list of item names in format "{item_name} ({wear})" e.g. 'MP5-SD | Savannah Halftone (Field-Tested)'
"""

import json
from rich import print_json

print('🏃‍♂️ Starting')

# Load list of skins
data = None
with open("skins_not_grouped.json") as fd: data = json.load(fd)

# Gen list of item names
#output = [{k: d[k] for k in ("name") if k in d} for d in data]  # Select only key 'name'

output = []
for d in data:
    output.append(d['name'])

"""
output = []
#i = 0
for k,v in enumerate(data):
    for w in v['wears']:
        item_name = f"{v['name']} ({w['name']})"
        output.append(item_name)
        #print(f"{k} - {item_name}")

    #i+=1
    #if i > 4: break
"""

# Write list to file
with open('_list_skin_names.json', 'w') as f:
    json.dump(output, f, indent=4)

print('✅ Done')

#print_json(data=data[0])