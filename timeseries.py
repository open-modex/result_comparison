import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import requests
import pandas as pd
import flask
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import urllib3
urllib3.disable_warnings()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)

URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
data = {timeseries["output_energy_vector"]: timeseries["series"] for timeseries in json_data["oed_timeseries"]}
data["hour"] = range(201)
#scalar=json_data['oed_timeseries']
#scalar=scalar[0:1540]
df=pd.DataFrame(data)
print(df)


scalar=json_data['oed_timeseries']
dff=pd.DataFrame(scalar)
dff = dff[dff["output_energy_vector"] == 'CO2']
print(dff)

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
]
external_scripts = [
    'https://code.jquery.com/jquery-3.2.1.slim.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
]

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    server=server,
)

fig = px.bar(
        df,
        x="hour",
        y="CO2",
        hover_name="CO2",
        #hover_data=["id"],
    )

body = html.Div(
    [
        html.Div(id='scenario_id_selected'),
        dcc.Graph(id='results',figure=fig)
    ],
)

# APP LAYOUT
# ==========

app.layout = html.Div([
    body,
])





if __name__ == '__main__':
    app.run_server(debug=True)
