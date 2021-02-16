import pathlib
import json
import pandas as pd
import requests
import urllib3
from assets.data.data_scalars import scalars

urllib3.disable_warnings()

'''print(scalars[0]['output_energy_vector'])

for i in range(len(scalars)):
    print(scalars[i]['output_energy_vector'])'''
print("hi")
null=0
URL='https://modex.rl-institut.de/scenario/id/12?source=modex&mapping=concrete'
response = requests.get(URL, verify=False)
json_data = json.loads(response.text)
scalar=json_data["oed_scalars"]
timeseries=json_data["oed_timeseries"]

df = pd.DataFrame(scalar, columns=['input_energy_vector','parameter_name', 'technology','technology_type'])
#df = pd.DataFrame(scalar)
#dff = pd.DataFrame(timeseries)
#dff = pd.DataFrame(timeseries, columns=['input_energy_vector','region','output_energy_vector','parameter_name', 'technology','technology_type','timeindex_start'])
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)
print(df)
#print(dff)
'''for i in range(len(scalar)):
    print(i,scalar[i]['parameter_name'],scalar[i]['input_energy_vector'],scalar[i]['region'])'''


