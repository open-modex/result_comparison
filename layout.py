import uuid
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from graphs import get_empty_fig
from settings import FILTERS, TS_FILTERS, GRAPHS_DEFAULT_OPTIONS


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
            html.Button("Reload", id="scenario_reload")
        ],
    )


def get_graph_options(data_type, graph_type):
    options = GRAPHS_DEFAULT_OPTIONS[data_type][graph_type]
    if data_type == "scalars":
        dd_options = [{"label": "value", "value": "value"}] + [
            {"label": filter_, "value": filter_} for filter_ in FILTERS
        ]
    else:
        dd_options = [{"label": "series", "value": "series"}] + [
            {"label": filter_, "value": filter_} for filter_ in TS_FILTERS
        ]

    # sum concatenates lists:
    return sum(
        [
            [
                html.Label(option),
                dcc.Dropdown(
                    id=f"{data_type}-{option}",
                    options=dd_options,
                    value=value,
                    clearable=False
                )
            ]
            for option, value in options.items()
        ],
        [dcc.Input(type="hidden", name="graph_type", value=graph_type)]
    )


aggregation_column = html.Div(
    children=[
        html.Label("Aggregation"),
        html.Label("Group-By:"),
        dcc.Dropdown(
            id="aggregation_group_by",
            multi=True,
            clearable=True,
            options=[{"label": filter_, "value": filter_} for filter_ in FILTERS],
        )
    ]
)

filter_column = html.Div(
    style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
    children=[
        html.Div(
            # sum concatenates lists:
            children=sum(
                [
                    [
                        html.Label(f"Filter {filter_.capitalize()}"),
                        dcc.Dropdown(id=f"filter_{filter_}", multi=True, clearable=True)
                    ]
                    for filter_ in FILTERS
                ],
                []
            ) + [aggregation_column]
        ),
    ],
)

graph_column = html.Div(
    style={"width": "68%", "display": "inline-block"},
    children=[
        html.Div(
            children=[
                html.Div(
                    style={"width": "85%", "display": "inline-block", "vertical-align": "top"},
                    children=[
                        html.Label(f"{graph.capitalize()}:"),
                        dcc.Loading(
                            style={"padding-bottom": "30px"},
                            type="default",
                            children=html.P(id=f"graph_{graph}_error", children="")
                        ),
                        dcc.Graph(id=f"graph_{graph}", figure=get_empty_fig(), style={}),
                        dash_table.DataTable(
                            id=f"table_{graph}",
                            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            },
                        )
                    ]
                ),
                html.Div(
                    style={"width": "15%", "display": "inline-block"},
                    children=[
                        dcc.RadioItems(
                            id=f"graph_{graph}_plot_switch",
                            options=[
                                {"label": graph_type.capitalize(), "value": graph_type}
                                for graph_type in GRAPHS_DEFAULT_OPTIONS[graph].keys()
                            ],
                            value=list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0]
                        ),
                        html.Div(
                            id=f"graph_{graph}_options",
                            children=get_graph_options(graph, list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0])
                        )
                    ]
                ),
            ]
        )
        for graph in ("scalars", "timeseries")
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


def get_error_and_warnings_div(errors, warnings, infos):
    return html.Div(
        children=(
            [html.P(error, style={"color": "red"}) for error in errors] +
            [html.P(warning, style={"color": "orange"}) for warning in warnings] +
            [html.P(info) for info in infos]
        )
    )
