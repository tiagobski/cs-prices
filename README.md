# Intro

This project aims to collect skin prices from multiple sources.

Sources implemented:

- [x] CSFloat
- [x] GamerPay
- [x] Waxpeer
- [x] ShadowPay

# Getting started

1. Populate file `.env`
2. Execute `py csgo-api/_downloader.py`
3. Execute `py csgo-api/_gen_list_skin_names.py`
4. Configure `config.py`
5. Execute `py script.py`

# State of development

- `script2` - Fetches prices using "price list" endpoints, which returns a list of all items and their min prices
- `script` - Fetches prices item by item, which was deemed unfeasible due to rate limits (csfloat limits to 200 requests / hour)

# Assessing purchases

We are looking to buy items at a price below what they are actually worth.

To assess fair value, implement the following procedure:

1. Liquidity:
   1. Value provided by ShadowPay - Should be 70+
   2. Last sales on CSFloat - There should be multiple per day
2. Price:
   1. Last sales on CSFloat - We should be buying at the best price registered recently
   2. Buy orders on CSFloat - We should be buying at a price equal or better than the highest

Filters:

- A - item - does not contain 'StatTrak' + 'Sticker'
- G - pct - < 1.51
- I - max_on - = csfloat
- J - liquidity - remove 'ND' and blanks

# Ideas

- [ ] Implement automatically fetching CSFloat sales history

  ```
  curl 'https://csfloat.com/api/v1/history/AWP%20%7C%20Safari%20Mesh%20(Field-Tested)/sales?paint_index=72' \
    -H 'sec-ch-ua-platform: "Windows"' \
    -H 'Referer: https://csfloat.com/item/911380888590355521' \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36' \
    -H 'Accept: application/json, text/plain, */*' \
    -H 'sec-ch-ua: "Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"' \
    -H 'sec-ch-ua-mobile: ?0'
  ```

- [ ] Implement automatically fetching CSFloat buy orders