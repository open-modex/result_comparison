from .app import server as application

if __name__ == '__main__':
    application.run()

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
scalar=scalar[1540:1561]
#scalar=scalar[1540:1556]
df=pandas.DataFrame(scalar)
#df=df[df["parameter_name"]=="cost system"]
available_parameter = df['parameter_name'].unique()




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


app.layout = html.Div([
    html.Div([
        header,
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_parameter],
                value='emissions'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='results'),
])



@app.callback(
    Output('results', 'figure'),
    [Input(component_id='yaxis-column', component_property='value')])

def update_graph(yaxis_column_name):
    dff=df[df['parameter_name'] == yaxis_column_name]
    fig = px.bar(x='source',
                 y=dff[dff["parameter_name"] == yaxis_column_name]['value'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0},transition_duration=500)
    fig.update_xaxes(title='source')
    fig.update_yaxes(title=yaxis_column_name)

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
