import json
from rich import print_json
import pandas as pd

import api
import translate
from search import Search; search = Search()

def pctdiff(v1,v2):
    return (v2-v1)/v1

def data_to_csv(data, csv_path='data/results.csv'):    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return df

pricelist = {
    'waxpeer': None,
    'csfloat': None,
    'shadowpay': None,
}

# Download price lists
if 1==1:
    print('Fetching price list from waxpeer')
    pricelist['waxpeer'] = api.waxpeer_prices()
    json.dump(pricelist['waxpeer'], open("data/waxpeer.json", "w"), indent=4)

    print('Fetching price list from csfloat')
    pricelist['csfloat'] = api.csfloat_prices()
    json.dump(pricelist['csfloat'], open("data/csfloat.json", "w"), indent=4)

    print('Fetching price list from shadowpay')
    pricelist['shadowpay'] = api.shadowpay_prices()
    json.dump(pricelist['shadowpay'], open("data/shadowpay.json", "w"), indent=4)

# Parse existing price lists
print('Parsing data')
with open('data/waxpeer.json') as fd: pricelist['waxpeer'] = json.load(fd)
pricelist['waxpeer'] = search.waxpeer_pricelist(pricelist['waxpeer'])
with open('data/csfloat.json') as fd: pricelist['csfloat'] = json.load(fd)
pricelist['csfloat'] = search.csfloat_pricelist(pricelist['csfloat'])
with open('data/shadowpay.json') as fd: pricelist['shadowpay'] = json.load(fd)
pricelist['shadowpay'] = search.shadowpay_pricelist(pricelist['shadowpay'])

"""
# Store pricelist organized by site
for k in pricelist.keys():
    pricelist[k] = [obj.__dict__ for obj in pricelist[k]]
    
json.dump(pricelist, open("data/pricelist.json", "w"), indent=4)
"""

# Organize pricelist by item name
pricelist_by_item = {}
for source in pricelist.keys():
    for e in pricelist[source]:
        if not e.name in pricelist_by_item: pricelist_by_item[e.name] = {}  # Create key for item if not exists
        pricelist_by_item[e.name][source] = e.price_min # Store price_min for this source

# Get liquidity data
print('Getting liquidity')
liquidity = {}  # liquidity[item_name] = float(0-100)|None
for e in pricelist['shadowpay']:
    liquidity[e.name] = e.liquidity

# Get min and max values
print('Calculating min, max values')
for item in pricelist_by_item:
    min_on = min(pricelist_by_item[item], key=pricelist_by_item[item].get)
    max_on = max(pricelist_by_item[item], key=pricelist_by_item[item].get)
    pricelist_by_item[item]['min'] = pricelist_by_item[item][min_on] #min(pricelist_by_item[item].values())
    pricelist_by_item[item]['max'] = pricelist_by_item[item][max_on] #max(pricelist_by_item[item].values())
    pricelist_by_item[item]['pct'] = pctdiff(pricelist_by_item[item]['min'], pricelist_by_item[item]['max'])
    pricelist_by_item[item]['min_on'] = min_on
    pricelist_by_item[item]['max_on'] = max_on
    pricelist_by_item[item]['liquidity'] = liquidity[item] if item in liquidity else "ND"   # No data

print('Writing output')
json.dump(pricelist_by_item, open("data/pricelist_by_item.json", "w"), indent=4)
#data_to_csv(pricelist_by_item)
df = pd.DataFrame.from_dict(pricelist_by_item, orient="index")
df.index.name = "item"
df.reset_index(inplace=True)
df.to_csv("data/output.csv", index=False)