import json
from rich import print_json
import pandas as pd

from search import Search; search = Search()

pricelist = { 'shadowpay': {} }
with open('data/shadowpay.json') as fd: pricelist['shadowpay'] = json.load(fd)
pricelist['shadowpay'] = search.shadowpay_pricelist(pricelist['shadowpay'])
#print_json(data=[item.__dict__ for item in pricelist['shadowpay']])

output = {}
for e in pricelist['shadowpay']:
    output[e.name] = e.liquidity

print_json(data=output)

#df = pd.DataFrame(output)
#df.to_csv('data/liquidity.csv', index=False)

