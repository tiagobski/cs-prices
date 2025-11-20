import re

from models.item import Item

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
        "name": item_api['name'],
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
