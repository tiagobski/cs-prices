import os
from dotenv import load_dotenv

load_dotenv()
API_KEY_WAXPEER = os.getenv('API_KEY_WAXPEER')
API_KEY_CSFLOAT = os.getenv('API_KEY_CSFLOAT')
API_KEY_SHADOWPAY = os.getenv('API_KEY_SHADOWPAY')
COOKIE_CSFLOAT = os.getenv('COOKIE_CSFLOAT')
FILTER_MAX_REQUESTS = int(os.getenv('FILTER_MAX_REQUESTS'))
FILTER_FILE_INPUT = os.getenv('FILTER_FILE_INPUT')
FILTER_FILE_OUTPUT = os.getenv('FILTER_FILE_OUTPUT')

search = {
    "stat_trak": False,     # Bool
    "conditions": ['Field-Tested', 'Well-Worn', 'Battle-Scarred'],  # List all conditions you want to search
    "sources": ['waxpeer', 'csfloat', 'gamerpay', 'shadowpay'],     # List all sources you want to search
    "rate_limit": 0,                                                # Searches per minute (0 to disable)
}

item_conditions = [
    {
        "name": 'Factory New',
        "range": [0, 0.07]
    },
    {
        "name": 'Minimal Wear',
        "range": [0.08, 0.15]
    },
    {
        "name": 'Field-Tested',
        "range": [0.16, 0.37]
    },
    {
        "name": 'Well-Worn',
        "range": [0.37, 0.44]
    },
    {
        "name": 'Battle-Scarred',
        "range": [0.44, 1]
    }
]