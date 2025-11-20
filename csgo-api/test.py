import json

with open('agents.json', 'r') as f:
    data = json.load(f)

print(data)