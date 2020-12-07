import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.express as px
from dash.dependencies import Input, Output

from data.oep_example import get_scenario_data

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
]
#hallo welt

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
    children=[
        dbc.NavItem(dbc.NavLink('Page 1', href='#')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('More pages', header=True),
                dbc.DropdownMenuItem('Page 2', href='#'),
                dbc.DropdownMenuItem('Page 3', href='#'),
            ],
            nav=True,
            in_navbar=True,
            label='More',
        ),
    ],
    brand='OpenModex Visualization Julian',
    brand_href='#',
    color='primary',
    dark=True,
)

body = html.Div(
    [
        dbc.Label('Select Scenario'),
        dbc.Select(
            id='scenario_id',
            options=[
                {'label': 'Scenario #6', 'value': 6},
                {'label': 'Scenario #7', 'value': 7},
            ],
            value=6,
        ),
        html.Div(id='scenario_id_selected'),
        dcc.Graph(id='results')
    ],
)

# APP LAYOUT
# ==========

app.layout = html.Div([
    header,
    body,
])


@app.callback(
    Output(component_id='scenario_id_selected', component_property='children'),
    [Input(component_id='scenario_id', component_property='value')],
)
def update_scenario(input_value):
    return f'Selected scenario: #{input_value}'


@app.callback(
    Output(component_id='results', component_property='figure'),
    [Input(component_id='scenario_id', component_property='value')],
)
def update_figure(scenario_id):
    df = get_scenario_data(scenario_id)

    fig = px.bar(
        df,
        x="hour",
        y="electricity",
        hover_name="electricity",
    )
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
