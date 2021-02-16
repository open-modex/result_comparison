import pathlib
import json
import pandas as pd
import requests
import urllib3
from assets.data.data_scalars import scalars

urllib3.disable_warnings()

from assets.data.data_in_scalars import scalars_in
from assets.data.data_in_timeseries import timeseries_in
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"
map=pd.read_csv("assets/states_list.csv", engine="python", index_col=False, delimiter='\;', dtype={"abbrev": str})

region_options = [{"label": str(region), "value": str(region)}
                    for region in map['abbrev']]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)

df=pd.DataFrame(timeseries_in,columns=['technology','technology_type','input_energy_vector','region','parameter_name'])
print(df)

