import uuid
import dash_core_components as dcc
import dash_html_components as html

from graphs import get_empty_fig
from settings import FILTERS


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


def get_scenario_column(scenarios):
    return html.Div(
        style={"padding-bottom": "50px"},
        children=[
            html.Label("Select scenario:"),
            dcc.Dropdown(
                id="dd_scenario",
                multi=True,
                options=[
                    {
                        "label": f"{scenario['id']}, {scenario['scenario']}, {scenario['source']}",
                        "value": scenario["id"],
                    }
                    for scenario in scenarios
                ],
            ),
        ],
    )


aggregation_column = html.Div(
    children=[
        html.Label("Aggregation"),
        html.Label("Group-By:"),
        dcc.Dropdown(
            id="aggregation_group_by",
            multi=True,
            clearable=True,
            options=[{"label": filter_, "value": filter_} for filter_ in FILTERS if filter_ != "source"],
        ),
        html.Label("Aggregation Function:"),
        dcc.Dropdown(
            id="aggregation_func",
            clearable=True,
            options=[
                {"label": "Sum", "value": "sum"},
                {"label": "Mean", "value": "mean"},
            ],
            value="sum"
        ),
    ]
)

filter_column = html.Div(
    style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
    children=[
        html.Div(
            children=[
                html.Label("Select Year:"),
                dcc.Dropdown(id="filter_year"),
                html.Label("Filter Regions:"),
                dcc.Dropdown(id="filter_region", multi=True, clearable=True,),
                html.Label("Filter Technologies:"),
                dcc.Dropdown(id="filter_technology", multi=True, clearable=True),
                html.Label("Filter Technology Type:"),
                dcc.Dropdown(id="filter_technology_type", multi=True, clearable=True),
                html.Label("Filter Parameters:"),
                dcc.Dropdown(id="filter_parameter_name", multi=True, clearable=True),
                html.Label("Filter Input:"),
                dcc.Dropdown(
                    id="filter_input_energy_vector", multi=True, clearable=True
                ),
                html.Label("Filter Output:"),
                dcc.Dropdown(
                    id="filter_output_energy_vector", multi=True, clearable=True
                ),
                html.Label("Filter Sources:"),
                dcc.Checklist(
                    id="filter_source",
                    labelStyle={"display": "inline-block", "size": "50px"},
                ),
                aggregation_column,
            ],
        ),
    ],
)

graph_column = html.Div(
    style={"width": "68%", "display": "inline-block"},
    children=[
        html.Label("Scalars:"),
        html.P(id="graph_scalar_error", children=""),
        dcc.Graph(id="graph_scalar", figure=get_empty_fig(), style={}),
        html.Label("Timeseries:"),
        dcc.Graph(id="graph_timeseries", figure=get_empty_fig(), style={}),
    ],
)


def get_layout(app, scenarios):
    session_id = str(uuid.uuid4())

    return html.Div(
        children=[
            html.Div(session_id, id="session-id", style={"display": "none"}),
            get_header(app),
            html.Div(
                children=[
                    get_scenario_column(scenarios),
                    html.Div(children=[filter_column, graph_column]),
                ],
            ),
        ],
    )
