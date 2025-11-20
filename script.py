"""
TODO: ✅ Handle non-200 res.status_code
TODO: ✅ Handle rate limits
TODO: ✅ Gamerpay returning StatTrak items mixed with non-st, as well as items without std name format "{name} {condition}"
TODO: Search for StatTrak items (all api sources)
"""

from rich import print_json
import json
from datetime import datetime
import pandas as pd
import os

import config
import api
import translate
from search import Search; search = Search()

def data_to_csv(data, csv_path='results.csv'):    
    df = pd.DataFrame([obj.__dict__ for obj in data])
    df.to_csv(csv_path, index=False)
    return df

# Load list of skins
skins = None
with open('csgo-api/_list_skin_names.json') as fd: skins = json.load(fd)
len_initial = len(skins)

# Filter list of skins
skins_to_search = []
for skin in skins:
    # Exclude StatTrak skins
    if config.search['stat_trak'] is False and 'StatTrak' in skin:
        #print(f"Excluding {skin}")
        continue

    # Exclude skins not in the conditions we are looking for
    if not any(s in skin for s in config.search['conditions']):
        #print(f"Excluding {skin}")
        continue

    skins_to_search.append(skin)

len_final = len(skins_to_search)
print(f"Searching {len_final} / {len_initial} skins")

# TEST
#skins_to_search = skins_to_search[300:350]

# Fetch all items from all sources
results = []
unique_searches = 0

try:
    for skin in skins_to_search:
        unique_searches += 1
        for s in config.search['sources']:
            print(f"[{unique_searches+1}/{len_final}] [{s}] Searching - {skin}")
            data = getattr(search, s)(skin) # call search[s](skin)
            print(f"[{unique_searches+1}/{len_final}] [{s}] {len(data)} found")
            results.extend(data)
            #print(data)
except Exception as e:
    print(f"🟥 Error: {e}")

# Store results
print(f"Total of {len(results)} skins found ({unique_searches} uniques)")

if (len(results) > 0):
    print('Saving results to CSV and JSON')
    data_to_csv(results)
    data = [obj.__dict__ for obj in results]
    json.dump(data, open("results.json", "w"), indent=4)

"""
# Fetch item info

item = 'MP5-SD | Savannah Halftone (Field-Tested)'  #'USP-S | 27 (Field-Tested)'  #StatTrak™ XM1014 | Seasons

data = api.waxpeer(item)
item = data['items'][0]
item = translate.waxpeer(item)
print_json(data=item.__dict__)

data = api.csfloat(item)
item = data['data'][0]
item = translate.csfloat(item)
print_json(data=item.__dict__)

data = api.gamerpay(item)
item = data['items'][2]
item = translate.gamerpay(item)
print_json(data=item.__dict__)

data = api.shadowpay(item)
item = data['data'][0]
item = translate.shadowpay(item)
print_json(data=item.__dict__)
"""
