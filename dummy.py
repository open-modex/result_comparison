import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.express as px
import json
import requests
import  pandas
from dash.dependencies import Input, Output, State
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
available_parameter=df['parameter_name'].unique()




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

body = html.Div([
            dcc.Dropdown(
                id='parameter',
                options=[{'label': i, 'value': i} for i in available_parameter],
                value='emissions'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )],style={'width': '48%', 'display': 'inline-block'})

app.layout = html.Div([
    header,
    body,
    dcc.Graph(id='honeychu', figure={}, style={})
])

@app.callback(
    Output(component_id='honeychu', component_property='figure'),
    [Input(component_id='parameter', component_property='value'),
     Input(component_id='yaxis-type', component_property='value')])
def update_graph(parameter,yaxis_type):
    dff=df[df["parameter_name"] == parameter]
    #avg=(dff['value']).sum()/4
    #print(avg)
    unit=dff["unit"].tolist()
    fig = px.bar(
            dff,
            x="source",
            y="value",
            hover_name='region',
            labels={"source":"Simulation Framework"},
    )
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0})
    fig.update_traces(marker_color = "orange")
    fig.update_yaxes(title=parameter + "in" + unit[0],
                     type='linear' if yaxis_type == 'Linear' else 'log')

    #print(fig)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)