import pathlib
import json
import pandas as pd
import requests
import urllib3
from assets.data.data_scalars import scalars
from qa import x
urllib3.disable_warnings()

'''print(scalars[0]['output_energy_vector'])

for i in range(len(scalars)):
    print(scalars[i]['output_energy_vector'])'''

'''URL='https://modex.rl-institut.de/scenario/id/6?source=modex&mapping=concrete'
response = requests.get(URL, verify=False)
json_data = json.loads(response.text)
scalar=json_data["oed_scalars"]'''
#print(scalar[0]['output_energy_vector'])


for i in range(len(x)):
    print(i,x[i]['input_energy_vector'])


