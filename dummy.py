import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.express as px
import json
import requests
import  pandas
from dash.dependencies import Input, Output
import urllib3

urllib3.disable_warnings()

URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
scalar=json_data['oed_scalars']
scalar1=scalar[1540:1556]
#mit dem unteren Slice wird das Framework Balmorel mitgenommen
#scalar1=scalar[1540:1561]
df=pandas.DataFrame(scalar1)
df=df[df["parameter_name"]=="cost system"]




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

# HEADER
# ======

header = dbc.NavbarSimple(
    brand='Optimized Costs by Respective Frameworks',
    brand_href='#',
    color='primary',
    dark=True,
)



fig = px.bar(
        df,
        x="source",
        y="value",
        hover_name="id",
        labels= {"value": "costs in trillion €'s",
                 "source":"Simulation Framework"},
        color='value'
    )
fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
#fig.update_traces(marker_color='green')
fig.update_xaxes(tickangle=10, tickfont=dict(family='Rockwell', color='black', size=14),showgrid=True)
fig.update_yaxes(showgrid=True)
fig.update_layout(transition_duration=500)

app.layout = html.Div([
    header,
    dcc.Graph(
        id='honeychu',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
