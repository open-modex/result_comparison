import dash_core_components as dcc
import dash_html_components as html

from settings import REGIONS


def get_header(app):
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Img(
                        src=app.get_asset_url("open_Modex-logo.png"),
                        style={"height": "100px", "width": "auto"},
                    ),
                    html.H4(children="Energy Frameworks to Germany"),
                    html.P(
                        children="How to efficiently sustain Germany's energy "
                        "\n usage with efficient parameters based on regions.",
                    ),
                ],
            ),
        ],
    )


scenario = html.Div(
    children=[
        dcc.Tabs(
            value="base",
            children=[
                dcc.Tab(
                    label="Base-Scenario",
                    value="base",
                    style={"background-color": "#FFFFFF"},
                ),
                dcc.Tab(
                    label="Pathway",
                    value="var1",
                    style={"background-color": "#1B2129"},
                ),
                dcc.Tab(
                    label="Pathway + Heat",
                    value="var2",
                    style={"background-color": "#1B2129"},
                ),
            ],
        ),
    ],
)

# FILTER COLUMN

filter_column = html.Div(
    style={'width': '20%', 'display': 'inline-block', "vertical-align": "top"},
    children=[
        html.Div(
            id="selection",
            children=[
                html.Label("Select Year:"),
                dcc.Dropdown(
                    id="dd_year",
                    options=[
                        {"label": "2021", "value": "2021"},
                    ],
                    value=2021
                ),
                html.Label("Filter Regions:"),
                dcc.Dropdown(
                    id="dd_region",
                    options=REGIONS,
                    value=["BB"],
                    multi=True,
                    clearable=True,
                ),
                html.Label("Filter Technologies:"),
                dcc.Dropdown(id="dd_technology", multi=True, clearable=True),
                html.Label("Filter Technology Type:"),
                dcc.Dropdown(id="dd_technology_type", multi=True, clearable=True),
                html.Label("Filter Parameters:"),
                dcc.Dropdown(id="dd_parameter", multi=True, clearable=True),
                html.Label("Filter Input:"),
                dcc.Dropdown(id="dd_input_energy_vector", multi=True, clearable=True),
                html.Label("Filter Output:"),
                dcc.Dropdown(id="dd_output_energy_vector", multi=True, clearable=True),
                html.Label("Filter Sources:"),
                dcc.Checklist(
                    id="cl_source",
                    options=[
                        {"label": "Urbs", "value": "Urbs"},
                        {"label": "Oemof", "value": "Oemof"},
                        {"label": "GENESYS-2", "value": "GENESYS-2"},
                        {"label": "Balmorel", "value": "Balmorel"},
                        {"label": "Genesys-mod", "value": "Genesys-mod"},
                    ],
                    value=["Urbs", "Oemof", "GENESYS-2", "Balmorel", "Genesys-mod"],
                    labelStyle={"display": "inline-block", "size": "50px"},
                ),
                html.Button(id="refresh_filters", value="Refresh")
            ],
        ),
    ],
)

graph_column = html.Div(
    style={'width': '80%', 'display': 'inline-block'},
    children=[
        html.Label("Scalars:"),
        dcc.Graph(id="graph_scalar", figure={}, style={}),
        html.Label("Timeseries:"),
        dcc.Graph(id="graph_timeseries", figure={}, style={}),
    ]
)


def get_layout(app):
    return html.Div(
        children=[
            get_header(app),
            html.Div(
                children=[scenario, html.Div(children=[filter_column, graph_column])],
            ),
        ],
    )
