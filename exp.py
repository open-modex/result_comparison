import pathlib
import json
import pandas as pd
import requests
import urllib3
import numpy as np
from assets.data.data_scalars import scalars

urllib3.disable_warnings()
print("hi")
null=0

from assets.data.data_scalars import scalars
from assets.data.data_in_scalars import scalars_in
scalar=scalars_in
from assets.data.data_timeseries import timeseries
from assets.data.data_in_timeseries import timeseries_in
from assets.data.help import data

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


for i in range(len(data)):
    print(i,data[i]['source'],data[i]['region'],data[i]['series'][0],data[i]['series'][1])

dff = pd.DataFrame(timeseries)#,columns=['parameter_name','technology','technology_type','input_energy_vector'])
#dff=dff['parameter_name'].unique()

