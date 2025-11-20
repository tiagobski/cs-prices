import api
import translate
import config

import time
import json

class Search:
    def __init__(self):
        self.searches = {
            'waxpeer': [],
            'csfloat': [],
            'gamerpay': [],
            'shadowpay': [],
        }

    def handle_rate_limit(self, source):
        # Get number of searches in the last minute
        timestamps = self.searches[source]
        now = round(time.time())
        count = sum(1 for t in timestamps if now - t <= 60)

        # If hit rate limit, wait until it's clear
        if count >= config.search['rate_limit'] and config.search['rate_limit'] != 0:
            first_search_ts = self.searches[source][0]
            next_req = first_search_ts + 61 # TODO: Maybe 61?
            seconds_to_wait = next_req - now

            if seconds_to_wait > 0:
                print(f"⏳ [{source}] Waiting {seconds_to_wait}s")
                time.sleep(seconds_to_wait)

        # Save a search happening in current ts
        now = round(time.time())
        self.searches[source].append(now)
        self.searches[source] = self.searches[source][-20:] # Filter to last 20 elements

        # Debug
        with open('debug/rate-limit.json', 'w') as f: json.dump(self.searches, f, indent=4)

    def waxpeer(self, item_name):
        self.handle_rate_limit('waxpeer')
        data = api.waxpeer(item_name)
        output = []
        for i in data['items']:
            output.append(translate.waxpeer(i))
        return output

    def csfloat(self, item_name):
        self.handle_rate_limit('csfloat')
        data = api.csfloat(item_name)
        output = []
        for i in data['data']:
            output.append(translate.csfloat(i))
        return output

    def gamerpay(self, item_name):
        self.handle_rate_limit('gamerpay')
        data = api.gamerpay(item_name)
        output = []
        for i in data['items']:
            output.append(translate.gamerpay(i))
        return output

    def shadowpay(self, item_name):
        self.handle_rate_limit('shadowpay')
        data = api.shadowpay(item_name)
        output = []
        for i in data['data']:
            output.append(translate.shadowpay(i))
        return output