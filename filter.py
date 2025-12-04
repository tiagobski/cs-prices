"""
This productivity script is multi purpose:
 - Filters the output file to reduce the number of entries to check manually
 - Adds extra stats - notional
 - Adds data from CSFloat: avg_price_history, best_buy_order_price
"""

import pandas as pd
import time

import config
from search import Search; search = Search()

print("🟩 Starting")

# Load data
print("🟦 Loading data")
df = pd.read_csv(config.FILTER_FILE_INPUT)

# Calculate new values
df['notional'] = df['max'] - df['min']
df['liquidity'] = pd.to_numeric(df['liquidity'], errors='coerce')

# Filter
print("🟦 Filtering data")
filter = df
filter = filter[~filter['item'].str.contains('StatTrak|Sticker|Capsule|Patch|Music Kit|Charm', case=False, na=False)]
filter = filter[('ND' not in df['liquidity']) & ('' not in filter['liquidity']) & (filter['liquidity'] >= 70)]
filter = filter[filter['max_on'] == 'csfloat']
filter = filter[filter['notional'] >= 0.2]

# Fetch CSFloat data
print(f" 🔹 Initial count: {len(df)}")
print(f" 🔹 Final count: {len(filter)}")
print(f"🟦 Fetching price history + buy order data")

filter = filter.reset_index(drop=True)
requests = 0

try:
    for i in range(len(filter)):
        print(f" 🔹 {filter.iloc[i]['item']}")

        # Avg sale price
        price_history = search.csfloat_price_history(filter.iloc[i]['item'])
        avg_avg_price  = sum(item["avg_price"] for item in price_history) / len(price_history)
        filter.loc[i, 'avg_price_history'] = avg_avg_price
        time.sleep(2)

        # Buy orders
        buy_orders = search.csfloat_buy_orders(filter.iloc[i]['item'])
        best_buy_order_price = 0 if len(buy_orders) == 0 else buy_orders[0]['price']
        filter.loc[i, 'best_buy_order_price'] = best_buy_order_price
        time.sleep(2)

        # Handle rate limit
        requests += 2
        if requests % config.FILTER_MAX_REQUESTS == 0:
            print('Waiting 60s')
            time.sleep(60)
        
except Exception as e:   # catch-all
    print('🟥 Fatal error - writing output before exiting')
    print(e)
    filter.to_csv(config.FILTER_FILE_OUTPUT)

# Output
filter.to_csv(config.FILTER_FILE_OUTPUT)
print('🟩 Finished')
