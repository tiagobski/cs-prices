"""
This script should be used when filter.py stops mid-execution due to external API rate limits.
It finds rows for which the CSFloat data is not available and completes them.
"""

import pandas as pd
import time
import math 

import config
from search import Search; search = Search()

print("🟦 Loading data")
df = pd.read_csv(config.FILTER_FILE_OUTPUT)

"""
x = float('nan')
print(df.iloc[80])
print( math.isnan(df.iloc[80]['avg_price_history']) )
exit()
"""

print(f"🟦 Fetching price history + buy order data")

filter = df
filter = filter.reset_index(drop=True)
requests = 0

try:
    for i in range(len(filter)):
        altered = math.isnan(filter.iloc[i]['avg_price_history']) or math.isnan(filter.iloc[i]['best_buy_order_price'])
        icon = '💬' if altered else '✅'
        print(f" 🔹 {filter.iloc[i]['item']} {icon}")

        # Avg sale price
        if math.isnan(filter.iloc[i]['avg_price_history']):
            price_history = search.csfloat_price_history(filter.iloc[i]['item'])
            avg_avg_price  = sum(item["avg_price"] for item in price_history) / len(price_history)
            filter.loc[i, 'avg_price_history'] = avg_avg_price
            time.sleep(2)

        # Buy orders
        if math.isnan(filter.iloc[i]['best_buy_order_price']):
            buy_orders = search.csfloat_buy_orders(filter.iloc[i]['item'])
            best_buy_order_price = 0 if len(buy_orders) == 0 else buy_orders[0]['price']
            filter.loc[i, 'best_buy_order_price'] = best_buy_order_price
            time.sleep(2)

        # Handle rate limit
        if altered: requests += 2
        if requests != 0 and requests % config.FILTER_MAX_REQUESTS == 0:  # Stop every X requests
            print('Waiting 60s')
            time.sleep(60)
        

except Exception as e:   # catch-all
    print('🟥 Fatal error - writing output before exiting')
    filter.to_csv(config.FILTER_FILE_OUTPUT)

# Output
filter.to_csv(config.FILTER_FILE_OUTPUT)
print('🟩 Finished')
