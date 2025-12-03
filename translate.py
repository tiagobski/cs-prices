import re

from models.item import Item
from models.item_pricelist import ItemPricelist

def waxpeer_gen_url(item_api):
    # Handle characters
    url_item_name = (
        re.sub(r'[^\w\s]', ' ', item_api['name'].lower())   # replace non-alphanumeric with space
    )
    url_item_name = (
        re.sub(r'\s+', ' ', url_item_name)          # collapse multiple spaces
        .strip()                                   # trim ends
        .split(' ')                                # split on spaces
    )
    url_item_name = '-'.join(url_item_name)

    url = f"https://waxpeer.com/{url_item_name}/item/{item_api['item_id']}"
    return url

def waxpeer(item_api):
    translated = {
        "site": 'waxpeer',
        "id": item_api['item_id'],
        "name": item_api['name'],
        "float": item_api['float'],
        "price": item_api['price'] / 1000,
        "tradable": True,                       # TODO
        "tradelock_expires_at": 0,              # TODO
        "url": waxpeer_gen_url(item_api)
    }

    item = Item(**translated)
    return item

def csfloat(item_api):
    translated = {
        "site": 'csfloat',
        "id": item_api['id'],
        "name": item_api['item']['market_hash_name'],
        "float": item_api['item']['float_value'],
        "price": item_api['price'] / 100,
        "tradable": item_api['item']['tradable'],
        "tradelock_expires_at": 0,              # TODO
        "url": f"https://csfloat.com/item/{item_api['id']}"
    }

    item = Item(**translated)
    return item

def gamerpay(item_api):
    translated = {
        "site": 'gamerpay',
        "id": item_api['id'],
        "name": item_api['marketHashName'],
        "float": item_api['floatValue'],
        "price": item_api['price'] / 100,
        "tradable": item_api['tradeLockExpiresAt'] == None,
        "tradelock_expires_at": item_api['tradeLockExpiresAt'],
        "url": f"https://gamerpay.gg/item/{item_api['id']}"
    }

    item = Item(**translated)
    return item

def shadowpay(item_api):
    translated = {
        "site": 'shadowpay',
        "id": item_api['id'],
        "name": item_api['steam_item']['steam_market_hash_name'],
        "float": item_api['floatvalue'],
        "price": item_api['price'],
        "tradable": True,               # TODO
        "tradelock_expires_at": 0,      # TODO
        "url": f"https://shadowpay.com/item/{item_api['id']}"
    }

    item = Item(**translated)
    return item

def waxpeer_pricelist(item_api):
    translated = {
        "name": item_api['name'],
        "qty": item_api['count'],
        "price_min": item_api['min'] / 1000,
        "price_steam": item_api['steam_price'] / 1000 if item_api['steam_price'] not in [None, 0] else 0,
    }

    item = ItemPricelist(**translated)
    return item

def csfloat_pricelist(item_api):
    translated = {
        "name": item_api['market_hash_name'],
        "qty": item_api['qty'],
        "price_min": item_api['min_price'] / 100,
    }

    item = ItemPricelist(**translated)
    return item

def shadowpay_pricelist(item_api):
    translated = {
        "name": item_api['steam_market_hash_name'],
        "qty": item_api['volume'],
        "price_min": item_api['price'],
        "liquidity": item_api['liquidity'],
    }

    item = ItemPricelist(**translated)
    return item

def csfloat_price_history(data):
    for i in range(len(data)):
        data[i]['avg_price'] /= 100

    return data

def csfloat_buy_orders(data):
    for i in range(len(data)):
        data[i]['price'] /= 100

    return data
