
import uuid
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


# FILTER COLUMN

filter_column = html.Div(
    style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
    children=[
        html.Div(
            style={"padding-bottom": "50px"},
            children=[
                html.Label("Select scenario:"),
                dcc.Dropdown(id="dd_scenario"),
            ],
        ),
        html.Div(
            children=[
                html.Label("Select Year:"),
                dcc.Dropdown(id="dd_year"),
                html.Label("Filter Regions:"),
                dcc.Dropdown(id="dd_region", multi=True, clearable=True,),
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
                    labelStyle={"display": "inline-block", "size": "50px"},
                ),
                html.Button("Refresh", id="refresh_filters"),
            ],
        ),
    ],
)

graph_column = html.Div(
    style={"width": "70%", "display": "inline-block"},
    children=[
        html.Label("Scalars:"),
        dcc.Graph(id="graph_scalar", figure={}, style={}),
        html.Label("Timeseries:"),
        dcc.Graph(id="graph_timeseries", figure={}, style={}),
    ],
)


def get_layout(app):
    session_id = str(uuid.uuid4())

    return html.Div(
        children=[
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            get_header(app),
            html.Div(
                children=[filter_column, graph_column],
            ),
        ],
    )
