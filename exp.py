import json
import requests
import pandas as pd
from data_timeseries import timeseries
from data_scalars import scalars
import urllib3
urllib3.disable_warnings()

'''URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
scalar=json_data['oed_scalars']'''
df=pd.DataFrame(scalars)
print(df)


