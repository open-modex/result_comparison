import pathlib
import json
import pandas as pd
import requests
import urllib3
from assets.data.data_scalars import scalars

urllib3.disable_warnings()
print("hi")
null=0

from assets.data.data_scalars import scalars
from assets.data.data_in_scalars import scalars_in
scalar=scalars_in
from assets.data.data_timeseries import timeseries
from assets.data.data_in_timeseries import timeseries_in
from assets.data.help import help


#df = pd.DataFrame(scalar, columns=['input_energy_vector','parameter_name', 'technology','technology_type'])

dff = pd.DataFrame(scalars)#,columns=['parameter_name','technology','technology_type','input_energy_vector'])
dff=dff[dff['technology']=='transmission']
dff=dff['parameter_name'].unique()

#dff = pd.DataFrame(timeseries, columns=['input_energy_vector','region','output_energy_vector','parameter_name', 'technology','technology_type','timeindex_start'])
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)
print(dff)

'''x=['energy flow','input energy','output energy','electricity generation','storage level']
r='generation'
if type(x) is list and r in x:
    print('supii')
else:
    print('nop')'''