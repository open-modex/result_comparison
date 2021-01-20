import json

#features = open("assets/features.txt", "r")
#content=features.read()
germany = json.load(open("assets/features.geojson", "r"))
print(type(germany))
from assets.data.data_karte import features
print(type(features))


