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


#data = {timeseries["output_energy_vector"]: timeseries["series"] for timeseries in json_data["oed_timeseries"]}
#data["hour"] = range(201)


URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
scalar=json_data['oed_scalars']
scalar=scalar[0:1540]
scalar={timeseries["region"]=='BB' for timeseries in scalar}
df=pd.DataFrame(scalar)
#df = df[df["parameter_name"] == 'generation']
print(df)

# Server definition

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"}
    ],
)
server = app.server

'''fig = px.bar(
        df,
        x="value",
        y="source",
        hover_name="region",
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
])'''





if __name__ == '__main__':
    app.run_server(debug=True)
