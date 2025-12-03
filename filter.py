import pandas as pd

import api
from search import Search; search = Search()

"""
item = 'Patch | Shattered Web'
#price_history = search.csfloat_price_history(item)
#print(price_history)
buy_orders = search.csfloat_buy_orders(item)
print(buy_orders)
exit()

# Buy orders
item = 'Patch | Shattered Web'
listings = api.csfloat(item, 1)
listing_id = listings['data'][0]['id']
buy_orders = api.csfloat_buy_orders(listing_id)
print(buy_orders)
exit()

# Avg sale price
item = 'Patch | Shattered Web'
data = api.csfloat_price_history(item)
avg_avg_price  = sum(item["avg_price"] for item in data) / len(data)
print(avg_avg_price)
exit()
"""

# Load data
df = pd.read_csv('data/output.csv')
print(df)

# Calculate new values
df['notional'] = df['max'] - df['min']
df['liquidity'] = pd.to_numeric(df['liquidity'], errors='coerce')

# Filter
filter = df
filter = filter[~filter['item'].str.contains('StatTrak|Sticker|Capsule|Patch|Music Kit|Charm', case=False, na=False)]
filter = filter[('ND' not in df['liquidity']) & ('' not in filter['liquidity']) & (filter['liquidity'] >= 70)]
filter = filter[filter['max_on'] == 'csfloat']
filter = filter[filter['notional'] >= 0.2]

# Fetch CSFloat data
filter = filter.reset_index(drop=True)

for i in range(len(filter)):
    # Avg sale price
    price_history = api.csfloat_price_history(filter.iloc[i]['item'])
    price_history = search.csfloat_price_history(filter.iloc[i]['item'])
    avg_avg_price  = sum(item["avg_price"] for item in price_history) / len(price_history)
    filter.loc[i, "avg_price_history"] = avg_avg_price

    # Buy orders
    buy_orders = search.csfloat_buy_orders(filter.iloc[i]['item'])
    best_buy_order_price = 0 if len(buy_orders) == 0 else buy_orders[0]['price']
    filter.loc[i, "best_buy_order_price"] = best_buy_order_price

    break

# Output
filter.to_csv('data/output-filter.csv')
print(f"Initial length: {len(df)}")
print(f"Final length: {len(filter)}")
print('Done')