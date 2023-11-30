import json
from copy import deepcopy

"""
Some fields have a value of a list of two elements, the first being the stock and the second being the readiness.
This script converts those fields to two fields, one for the stock and one for the readiness.

"""
data = None
with open('data/raw.json') as f:
	data = json.load(f)

copy = deepcopy(data)
for country, info in copy.items():
	for title, value in info.items():	
		if type(value) == list:
			data[country][title] = value[0]
			data[country][title + " Ready"] = value[1]