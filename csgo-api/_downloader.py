"""
@ref https://github.com/ByMykel/CSGO-API
"""

import requests
import json
import time

parts = [
    'skins',
    'skins_not_grouped',
    'stickers',
    'stickers_slab',
    'keychains',
    'collections',
    'crates',
    'keys',
    'collectibles',
    'agents',
    'patches',
    'graffiti',
    'music_kits',
    'base_weapons',
    'highlights',
]

for p in parts:
    print(f"🔷 Downloading '{p}'")
    url = f"https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/{p}.json"

    res = requests.request("GET", url)
    res = json.loads(res.text)
    with open(f"{p}.json", 'w') as f:
        json.dump(res, f, indent=4)
    print('   🔹 Done')
    time.sleep(2)