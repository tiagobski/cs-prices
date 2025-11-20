import api
import translate

def waxpeer(item_name):
    data = api.waxpeer(item_name)
    output = []
    for i in data['items']:
        output.append(translate.waxpeer(i))
    return output

def csfloat(item_name):
    data = api.csfloat(item_name)
    output = []
    for i in data['data']:
        output.append(translate.csfloat(i))
    return output

def gamerpay(item_name):
    data = api.gamerpay(item_name)
    output = []
    for i in data['items']:
        output.append(translate.gamerpay(i))
    return output

def shadowpay(item_name):
    data = api.shadowpay(item_name)
    output = []
    for i in data['data']:
        output.append(translate.shadowpay(i))
    return output