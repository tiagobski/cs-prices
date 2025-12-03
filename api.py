import requests
import urllib
import json

import config

def waxpeer(item_name):
    """
    @ref https://docs.waxpeer.com/?method=v2-search-items-by-name-get
    """
    item_name_list = []

    # item_name already contains the condition
    if " (" in item_name:
        item_name_list.append(item_name)
    # item_name doesn't contain condition, add all
    else:
        for condition in config.item_conditions:
            item_name_list.append(f"{item_name} ({condition['name']})")

    # URL encode item names
    url_item_names = []
    for i in item_name_list:
        url_item_names.append(urllib.parse.quote_plus(i))

    # Join all possible item names
    url_item_names = "&".join(url_item_names)

    # Assemble final URL
    url = f"https://api.waxpeer.com/v1/search-items-by-name?api={config.API_KEY_WAXPEER}&minified=0&order=price&sort=ASC&names[]={url_item_names}"
    
    # Send req, parse json, output
    try:
        res = requests.request("GET", url)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[waxpeer] Request failed", e)

def csfloat(item_name, limit=50):
    """
    @ref https://docs.csfloat.com/#get-all-listings
    """
    # Prep req
    url_item_name = urllib.parse.quote_plus(item_name)
    url = f"https://csfloat.com/api/v1/listings?limit={limit}&sort_by=lowest_price&type=buy_now&market_hash_name={url_item_name}"
    payload = {}
    headers = {
        'Authorization': config.API_KEY_CSFLOAT
    }

    # Send req, parse json, output
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[csfloat] Request failed", e)

def gamerpay(item_name):
    # Prep req
    url_item_name = urllib.parse.quote_plus(item_name)
    is_st = int('StatTrak' in item_name)
    url = f"https://api.gamerpay.gg/feed?page=1&sortBy=price&ascending=true&market=steam&statTrak={is_st}&query={url_item_name}"
    
    print(url)
    exit()
    payload = {}
    headers = { 
        'accept': '*/*', 
        'accept-language': 'pt-PT', 
        'authorization': '5908d0c7-441e-4880-bdd0-2c2d1c03e5d3', 
        'cache-control': 'no-cache', 
        'content-type': 'application/json', 
        'origin': 'https://gamerpay.gg', 
        'pragma': 'no-cache', 
        'priority': 'u=1, i', 
        'referer': 'https://gamerpay.gg/', 
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"', 
        'sec-ch-ua-mobile': '?0', 
        'sec-ch-ua-platform': '"Windows"', 
        'sec-fetch-dest': 'empty', 
        'sec-fetch-mode': 'cors', 
        'sec-fetch-site': 'same-site', 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    # Send req, parse json, output
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[gamerpay] Request failed", e)

def shadowpay(item_name):
    """
    To get an API key go to Profile > Edit and in the modal there it is
    @ref https://shadowpay.com/profile
    @ref https://doc.shadowpay.com/docs/shadowpay/cfec7d5173741-get-items
    """

    # Prep req
    url_item_name = urllib.parse.quote_plus(item_name)
    url = f"https://api.shadowpay.com/api/v2/user/items?price_to=150354.61&sort_column=price&sort_dir=asc&stack=false&offset=0&limit=50&sort=asc&game=csgo&steam_market_hash_name={url_item_name}"
    payload = {}
    headers = {
        'Authorization': f"Bearer {config.API_KEY_SHADOWPAY}"
    }

    # Send req, parse json, output
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[shadowpay] Request failed", e)

def waxpeer_prices():
    """
    @ref https://docs.waxpeer.com/?method=v1-prices-get
    """

    url = f"https://api.waxpeer.com/v1/prices?api={config.API_KEY_WAXPEER}"
    try:
        res = requests.request("GET", url)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[waxpeer] Request failed", e)
    
def csfloat_prices():
    """
    @ref https://docs.csfloat.com/#get-all-listings
    """

    url = "https://csfloat.com/api/v1/listings/price-list"
    payload = {}
    headers = {
        'Authorization': config.API_KEY_CSFLOAT
    }
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[csfloat] Request failed", e)
    
def shadowpay_prices():
    """
    @ref https://doc.shadowpay.com/docs/shadowpay/6d63adddb51eb-get-item-prices
    """

    url = "https://api.shadowpay.com/api/v2/user/items/prices"
    payload = {}
    headers = {
        'Authorization': f"Bearer {config.API_KEY_SHADOWPAY}"
    }
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[shadowpay] Request failed", e)

def csfloat_price_history(item_name):
    # Prep req
    url_item_name = urllib.parse.quote_plus(item_name)
    url = f"https://csfloat.com/api/v1/history/{url_item_name}/graph"
    payload = {}
    headers = {}
    
    # Send req, parse json, output
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[csfloat] Request failed", e)

def csfloat_buy_orders(listing_id):
    # Prep req
    url = f"https://csfloat.com/api/v1/listings/{listing_id}/buy-orders?limit=10"
    payload = {}
    headers = {
        'Cookie': f"session={config.COOKIE_CSFLOAT}"
    }

    # Send req, parse json, output
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
        res.raise_for_status()
        res = json.loads(res.text)
        return res
    except Exception as e:   # catch-all
        raise Exception("[csfloat] Request failed", e)