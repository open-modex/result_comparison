import uuid
import json
from collections import ChainMap, defaultdict

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from graphs import get_empty_fig
from settings import (
    VERSION, SC_FILTERS, TS_FILTERS, UNITS, GRAPHS_DEFAULT_OPTIONS, GRAPHS_DEFAULT_COLOR_MAP, GRAPHS_DEFAULT_LABELS
)
from models import get_model_options, Filter, Colors, Labels, Scenarios


DEFAULT_LAYOUT = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def get_header(app):
    return html.Section(
        className="header",
        children=[
            html.Div(
                className="header__content",
                children=[
                    html.Div(
                        className="header__logo",
                        children=[
                            dcc.Link(html.Img(src=app.get_asset_url("open_Modex-logo.png")), href="/")
                        ],
                    ),
                    html.Div(
                        className="header__heading",
                        children=[
                            html.P(
                                children=f"Version v{VERSION}",
                                className="version"
                                ),
                            html.H1(
                                children="Open Energy Dashboard",
                                className="title"
                                ),
                            html.P(
                                children="Comparison and analysis of multiple energysystem modelling results",
                                className="subtitle"
                            ),
                        ],
                    ),
                ]
            ),
            dbc.NavbarSimple(
                className="header__nav",
                children=[
                    dbc.NavItem(dcc.Link("Documentation", href="/documentation")),
                    dbc.NavItem(dcc.Link("Imprint", href="/imprint")),
                    dbc.NavItem(dcc.Link("Privacy", href="/privacy")),
                ],
                dark=False,
                expand="xl"
            )
        ],
    )


def get_scenario_column(app, scenarios):
    with app.server.app_context():
        options = get_model_options(Scenarios)
    return html.Div(
        className="scenarios",
        style={"padding-bottom": "50px"},
        children=[
            html.Label("Scenario"),
            dcc.Dropdown(
                id="dd_scenario",
                className="scenarios__dropdown",
                multi=True,
                options=[
                    {
                        "label": f"{scenario['id']}, {scenario['scenario']}, {scenario['source']}",
                        "value": scenario["id"],
                    }
                    for scenario in scenarios
                ],
            ),
            dbc.Button(
                "Reload",
                id="scenario_reload",
                className="scenarios__btn btn btn--refresh"
            ),
            html.Label("Save scenarios as:"),
            html.Div(
                className="save-filters",
                children=[
                    dcc.Input(id="save_scenarios_name", type="text"),
                    html.Button("Save", className="btn btn--small", id="save_scenarios")
                ]
            ),
            html.Label("Load Scenarios"),
            dcc.Dropdown(
                id="load_scenarios",
                options=options,
                clearable=True
            ),
            html.P(id="scenarios_error", children="")
        ],
    )


def get_graph_options(data_type, graph_type, preset_options=None):
    preset_options = preset_options or {}
    chosen_options = ChainMap(preset_options, GRAPHS_DEFAULT_OPTIONS[data_type][graph_type].get_defaults())
    if data_type == "scalars":
        dd_options = [{"label": "value", "value": "value"}] + [
            {"label": filter_, "value": filter_} for filter_ in SC_FILTERS
        ]
    else:
        dd_options = [{"label": "series", "value": "series"}] + [
            {"label": filter_, "value": filter_} for filter_ in TS_FILTERS
        ]

    tabs = defaultdict(list)
    for option, value in chosen_options.items():
        if GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].from_filter:
            options = dd_options
        else:
            options = GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].default
        component_type = GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].type
        if component_type == "dropdown":
            component = dcc.Dropdown(
                id={"name": option, "type": f"graph_{data_type}_option"},
                options=options,
                value=value,
                clearable=GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].clearable
            )
        elif component_type in ("input", "int", "float"):
            component = dcc.Input(
                id={"name": option, "type": f"graph_{data_type}_option"},
                value=value,
                type="text" if component_type == "input" else "number",
                step=GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].step
            )
        elif component_type == "bool":
            component = dcc.Checklist(
                id={"name": option, "type": f"graph_{data_type}_option"},
                options=options,
                value=value if isinstance(value, list) else [value],
            )
        else:
            raise ValueError("Unknown dcc component")
        tabs[GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].category] += [
            html.Label(GRAPHS_DEFAULT_OPTIONS[data_type][graph_type][option].label),
            component
        ]
    tabs[next(iter(tabs.keys()))].insert(0, dcc.Input(type="hidden", name="graph_type", value=graph_type))
    return dbc.Tabs(
        [dbc.Tab(tab, label=label) for label, tab in tabs.items()]
    )


def get_save_load_column(app):
    with app.server.app_context():
        options = get_model_options(Filter)
    return html.Div(
        children=[
            html.P(id="save_load_errors", children=""),
            html.Label("Save filters as:"),
            html.Div(
                className="save-filters",
                children=[
                    dcc.Input(id="save_filters_name", type="text"),
                    html.Button("Save", className="btn btn--small", id="save_filters")
                ]
            ),
            html.Label("Load filters"),
            dcc.Dropdown(
                id="load_filters",
                options=options,
                clearable=True
            )
        ]
    )


def get_aggregation_order_column():
    return html.Div(
        className="filter-section",
        children=[
            html.P("Order/Aggregation"),
            html.Label("Order-By:"),
            dcc.Dropdown(
                id="order_by",
                multi=True,
                clearable=True,
                options=[{"label": filter_, "value": filter_} for filter_ in SC_FILTERS],
            ),
            html.Label("Group-By:"),
            dcc.Dropdown(
                id="aggregation_group_by",
                multi=True,
                clearable=True,
                options=[{"label": filter_, "value": filter_} for filter_ in SC_FILTERS],
            ),
            html.Label("Normalize Data:"),
            dcc.Checklist(
                id="normalize",
                options=[{"label": "Normalize", "value": "normalize"}],
                value=[],
            )
        ]
    )


def get_units_column():
    return html.Div(
        id="units",
        className="filter-section",
        children=sum(
            (
                [
                    html.Label(unit_name),
                    dcc.Dropdown(
                        id={"name": unit_name, "type": "unit-dropdown"},
                        options=[
                            {"label": unit, "value": unit}
                            for unit in unit_data["units"]
                        ],
                        value=unit_data["default"],
                        clearable=False,
                    ),
                ]
                for unit_name, unit_data in UNITS.items()
            ),
            [html.P("Units")],
        ),
    )


def get_filter_column():
    return html.Div(
        id="filters",
        className="filter-section",
        children=sum(
            (
                [
                    html.Label(f"Filter {filter_.capitalize()}"),
                    dcc.Dropdown(
                        id={"name": filter_, "type": "filter-dropdown"}, multi=True, clearable=True
                    ),
                    html.Button("Select All", className="btn btn--no-border filter--select-all", id=f"all_{filter_}")
                ]
                for filter_ in SC_FILTERS
            ),
            [html.P("General")],
        ),
    )


def get_color_column(app):
    with app.server.app_context():
        options = get_model_options(Colors)
    return html.Div(
        className="filter__colors",
        children=[
            html.Label("Color Map"),
            dcc.Textarea(
                id="colors", value=json.dumps(GRAPHS_DEFAULT_COLOR_MAP), style={"width": "100%", "height": "50px"}
            ),
            html.Label("Save colors as:"),
            html.Div(
                className="save",
                children=[
                    dcc.Input(id="save_colors_name", type="text"),
                    html.Button("Save", id="save_colors"),
                ]
            ),
            html.Label("Load colors"),
            dcc.Dropdown(
                id="load_colors",
                options=options,
                clearable=True
            ),
            html.P(id="colors_error", children="")
        ]
    )


def get_label_column(app):
    with app.server.app_context():
        options = get_model_options(Labels)
    return html.Div(
        className="filter__labels",
        children=[
            html.Label("Labels"),
            dcc.Textarea(
                id="labels", value=json.dumps(GRAPHS_DEFAULT_LABELS), style={"width": "100%", "height": "50px"}
            ),
            html.Label("Save labels as:"),
            html.Div(
                className="save",
                children=[
                    dcc.Input(id="save_labels_name", type="text"),
                    html.Button("Save", id="save_labels"),
                ]
            ),
            html.Label("Load labels"),
            dcc.Dropdown(
                id="load_labels",
                options=options,
                clearable=True
            ),
            html.P(id="labels_error", children="")
        ]
    )


def get_graph_column():
    return html.Div(
        className="charts",
        children=[
            html.Div(
                className="charts__item",
                children=[
                    html.Div(
                        className="graph",
                        children=[
                            html.Div(
                                className="graph__view",
                                children=[
                                    html.Div(
                                        className="scenarios__views",
                                        children=[
                                            html.Div(
                                                id=f"view-dashboard_{graph}",
                                                className="view view--dashboard active"
                                            ),
                                            html.Div(
                                                id=f"view-dashboard-data_{graph}",
                                                className="view view--dashboard-data"
                                            )
                                        ]
                                    ),
                                    dcc.RadioItems(
                                        id=f"graph_{graph}_plot_switch",
                                        options=[
                                            {"label": graph_type.capitalize(), "value": graph_type}
                                            for graph_type in GRAPHS_DEFAULT_OPTIONS[graph].keys()
                                        ],
                                        value=list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0]
                                    ),
                                    html.Button("Refresh", id=f"refresh_{graph}", className="btn btn--refresh")
                                ]
                            ),
                            dcc.Loading(
                                style={"padding-bottom": "30px"},
                                type="default",
                                children=dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            dcc.Graph(
                                                id=f"graph_{graph}",
                                                figure=get_empty_fig(),
                                                style={},
                                                config={
                                                    'responsive': True,
                                                    'toImageButtonOptions': {
                                                        'format': 'svg',
                                                    }
                                                }
                                            ),
                                            label="Chart"
                                        ),
                                        dbc.Tab(
                                            html.P(id=f"graph_{graph}_error", children=""),
                                            id=f"tab_{graph}_error",
                                            label="Errors",
                                        ),
                                    ]
                                )
                            ),
                            html.Div(
                                id=f"table_div_{graph}",
                                style={"display": "none"},
                                children=dash_table.DataTable(
                                    id=f"table_{graph}",
                                    export_format="csv",
                                    style_table={'overflowX': 'auto'},
                                    style_header={
                                        'backgroundColor': 'rgb(246, 248, 250)',
                                        'textAlign': 'center'
                                        }, 
                                    style_cell={
                                        'backgroundColor': 'rgb(255, 255, 255)',
                                        'color': 'rgb(50, 50, 50)',
                                        'textAlign': 'left'
                                    },
                                )
                            )
                        ]
                    ),
                    html.Div(
                        className="chart-settings",
                        children=[
                            html.Div(
                                className="chart-settings__title",
                                children="Chart settings"
                            ),
                            html.Div(
                                className="chart-settings__form",
                                id=f"graph_{graph}_options",
                                children=get_graph_options(graph, list(GRAPHS_DEFAULT_OPTIONS[graph].keys())[0])
                            )
                        ]

                    )
                ]
            )
            for graph in ("scalars", "timeseries")
        ],
    )


def get_footer():
    return html.Div(
        className="footer",
        children=[
            html.A("Imprint", href="/imprint", className="nav-link"),
            html.A("Privacy", href="/privacy", className="nav-link")
        ]
    )


def get_layout(app, scenarios):
    session_id = str(uuid.uuid4())

    return html.Div(
        children=[
            html.Div(session_id, id="session-id", style={"display": "none"}),
            get_header(app),
            html.Main(
                className="dashboard",
                children=[
                    get_scenario_column(app, scenarios),
                    html.Div(
                        className="content",
                        children=[
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        [
                                            get_filter_column(),
                                            get_aggregation_order_column(),
                                            get_save_load_column(app),
                                            get_units_column(),
                                        ],
                                        className="test",
                                        label="Filters"
                                    ),
                                    dbc.Tab(
                                        [
                                            get_color_column(app),
                                            get_label_column(app),
                                        ],
                                        label="Presentation"
                                    )
                                ],
                            ),
                            get_graph_column()
                        ]
                    ),
                    get_footer()
                ],
            ),
        ],
    )


def get_error_and_warnings_div(errors=None, warnings=None, infos=None):
    errors = errors or []
    warnings = warnings or []
    infos = infos or []
    return html.Div(
        children=(
            [html.P(error, style={"color": "red"}) for error in errors] +
            [html.P(warning, style={"color": "orange"}) for warning in warnings] +
            [html.P(info) for info in infos]
        )
    )
