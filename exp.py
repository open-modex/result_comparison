import xml.etree.ElementTree as ET
import pathlib
import json
import pandas as pd
import requests
import urllib3
import numpy as np

import os
import ast

urllib3.disable_warnings()
print("hi")
null=0
nan=0



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)
#df=df['parameter_name'].unique()

'''dfx = pd.read_csv(os.path.join(os.path.dirname(__file__),
                               "Balmorel/oed_timeseries_output.csv"),sep=';')

timeseries=dfx.to_dict('records')

for i in range(len(timeseries)):
    timeseries[i]['region']=ast.literal_eval(timeseries[i]['region'])
    timeseries[i]['series'] = ast.literal_eval(timeseries[i]['series'])

with open("timeseries.py","w") as f:
    f.write('timeseries={}'.format(timeseries))
    f.close()
'''

from assets.data.ergebnisse import scalars,BY_PV_rooftop,BY_chp_gas_cc
from assets.data.data_in_scalars import scalars_in
from assets.data.data_in_timeseries import timeseries_in
from timeseries import timeseries
from assets.data.help import serie
honeychu=scalars

print(len(BY_chp_gas_cc['series']))


#df=pd.DataFrame(timeseries,columns=['parameter_name','region','timeindex_start'])
#df=df['parameter_name'].unique()
#df=df[df['parameter_name']=='demand']#.unique()
#df=df[df['timeindex_start']=='2016-01-01T00:00:00']

print(len(serie))

please=np.array(serie)/1000

#print(list(please)[0:8736])

ltb=[1, 5, 7, 8, 10, 12, 13, 22, 23, 26, 28, 31, 32, 34, 35, 37, 39, 40, 41, 43, 45, 46, 48, 50, 51, 52, 54, 55, 56, 58, 59, 61, 62, 64, 65, 66, 69, 72, 73, 74, 76, 77, 78, 79, 82, 85, 86, 89, 90, 93, 95, 96, 97, 98, 99]
print(ltb)
ltb_have=[4,75,79,89,98,99,100,110,105,108,1,2, 74, 75, 81, 55, 111, 56, 21, 16,20,23,24,51,18]


fiftyeuro=[5,7,8,11,17,22,27,36,42,46,53,54,55,69,71,72,74,75,77,79,83,84,86,87,89,91,94,95,99]
must_get=[]
duplicates=[1, 23, 51, 55, 56, 74, 79, 89, 98, 99]
new_ltb=[5, 7, 8, 10, 12, 13, 22, 26, 28, 31, 32, 34, 35, 37, 39, 40, 41, 43, 45, 46, 48, 50, 52, 54, 58, 59, 61, 62, 64, 65, 66, 69, 72, 73, 76, 77, 78, 82, 85, 86, 90, 93, 95, 96, 97,50, 54, 98, 48, 90, 40, 73, 34, 76, 54, 52, 46]
print(len(ltb))


for j in fiftyeuro:
    if j in new_ltb:
        new_ltb.remove(j)
print('ltb is',new_ltb)
print(len(new_ltb))
must_get_2=[]
for i in duplicates:
    if i not in ltb:
        must_get_2.append(i)

print(must_get_2)

print(must_get)

#print(list(please)[0:8736])

#print(len(BE_chp_CC['series']))
#print(HE_PV_R['series'][8736])

#df=df['technology_type'].unique()



















'''#root = ET.parse('test.xml').getroot()
root = ET.parse(os.path.join(os.path.dirname(__file__), "test.xml")).getroot()
tags = {"tags":[]}

for elem in root.iter():
    for elem in root.find('.//region'):
        print(elem.tab, elem.attrib)
    tag = {}
    tag["Id"] = elem.attrib['Id']
    tag["TagName"] = elem.attrib['TagName']
    tag["Countt"] = elem.attrib['Count']
    tag["ExcerptPostId"] = elem.attrib['ExcerptPostId']
    tag["WikiPostId"] = elem.attrib['WikiPostId']
    tags["tags"]. append(tag)

#df_users = pd.DataFrame(tags["tags"])
#df_users.head()
#print(df_users)

root = ET.parse(os.path.join(os.path.dirname(__file__), "test_2.xml")).getroot()
tags = {"tags": []}

for elem in root:
    tag = {}
    tag["scenario"] = elem.attrib['scenario']
    #tag["software_compile_data"] = elem.attrib['software_compile_date']

    tags["tags"]. append(tag)

df_userss = pd.DataFrame(tags["tags"])
#df_users.head()
print(df_userss)'''