import json
import pathlib

import urllib3

import dash
from dash.dependencies import Input, Output, State, ALL, ClientsideFunction
from dash.exceptions import PreventUpdate
from dash.dash import no_update
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import flash, get_flashed_messages
from flask_caching import Cache

from data import dev
import preprocessing
from settings import (
    SECRET_KEY,
    DB_URL,
    DEBUG,
    MANAGE_DB,
    SKIP_TS,
    SC_FILTERS,
    USE_DUMMY_DATA,
    CACHE_CONFIG,
    MAX_WARNINGS,
    MAX_INFOS,
)
import scenario
import graphs
from models import db, get_model_options, Filter, Colors, Labels, Scenarios

urllib3.disable_warnings()

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"},
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
server.secret_key = SECRET_KEY

# Database
server.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(server)

# Cache
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)

# Layout
if not MANAGE_DB:
    from layout.main import (
        DEFAULT_LAYOUT,
        get_layout,
        get_graph_options,
        get_error_and_warnings_div,
    )
    from layout.imprint import get_imprint_layout
    from layout.privacy import get_privacy_layout
    from layout.results import get_results_layout
    from layout.docs import get_docs_layout

    app.layout = DEFAULT_LAYOUT
    app.validation_layout = html.Div(
        [
            DEFAULT_LAYOUT,
            get_layout(app, scenarios=scenario.get_scenarios()),
            get_imprint_layout(app),
            get_privacy_layout(app),
            get_results_layout(app),
            get_docs_layout(app)
        ]
    )


# Multiple pages
@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/imprint":
        return get_imprint_layout(app)
    elif pathname == "/privacy":
        return get_privacy_layout(app)
    elif pathname == "/documentation":
        return get_docs_layout(app)
    elif pathname == "/results":
        return get_results_layout(app)
    else:
        return get_layout(app, scenarios=scenario.get_scenarios())


@cache.memoize()
def get_scenario_data(scenario_id, table):
    app.logger.info(f"Loading scenario data #{scenario_id} (not cached)...")
    if USE_DUMMY_DATA:
        return dev.get_dummy_data(scenario_id, table)
    return scenario.get_scenario_data(scenario_id, table)


@cache.memoize()
def get_multiple_scenario_data(*scenario_ids, table):
    app.logger.info("Merging scenario data (not cached)...")
    scenarios = [get_scenario_data(scenario_id, table) for scenario_id in scenario_ids]
    merged = scenario.merge_scenario_data(scenarios)
    app.logger.info("Merged scenario data")
    return merged


@cache.memoize()
def get_scenario_filters(scenario_id):
    app.logger.info(f"Loading scenario data #{scenario_id} (not cached)...")
    if USE_DUMMY_DATA:
        return dev.get_dummy_filters(scenario_id)
    return scenario.get_scenario_filters(scenario_id)


@cache.memoize()
def get_multiple_scenario_filters(*scenario_ids):
    app.logger.info("Merging scenario data (not cached)...")
    scenarios = [
        get_scenario_filters(scenario_id) for scenario_id in scenario_ids
    ]
    merged = scenario.merge_scenario_data(scenarios)
    app.logger.info("Merged scenario data")
    return merged


@app.callback(
    Output(component_id="dd_scenario", component_property="options"),
    Input("scenario_reload", "n_clicks"),
)
def reload_scenarios(_):
    scenarios = scenario.get_scenarios()
    return [
        {"label": f"{sc['id']}, {sc['scenario']}, {sc['source']}", "value": sc["id"]}
        for sc in scenarios
    ]


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_refresh_elements"),
    Output(component_id="refresh_scalars", component_property="className"),
    Output(component_id="refresh_timeseries", component_property="className"),
    [
        Input("dd_scenario", "value"),
        Input(component_id="order_by", component_property="value"),
        Input(component_id="aggregation_group_by", component_property="value"),
        Input({"name": ALL, "type": "filters"}, "value"),
        Input({"name": ALL, "type": "unit-dropdown"}, "value"),
        Input({"name": ALL, "type": "graph_scalars_option"}, "value"),
        Input({"name": ALL, "type": "graph_timeseries_option"}, "value"),
        Input("load_filters", "value"),
        Input("load_colors", "value"),
        Input("load_labels", "value"),
    ],
    prevent_initial_call=True,
)


@app.callback(
    [
        Output(component_id="load_filters", component_property="options"),
        Output(component_id="save_filters_name", component_property="value"),
    ],
    Input("save_filters", "n_clicks"),
    [
        State(component_id="save_filters_name", component_property="value"),
        State(component_id="graph_scalars_options", component_property="children"),
        State(component_id="graph_timeseries_options", component_property="children"),
        State(component_id="order_by", component_property="value"),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id="normalize", component_property="value"),
        State(component_id="filters", component_property="children"),
    ],
)
def save_filters(
    _,
    name,
    graph_scalars_options,
    graph_timeseries_options,
    order_by,
    agg_group_by,
    normalize,
    filter_div,
):
    if not name:
        raise PreventUpdate

    filters = preprocessing.extract_filters("scalars", filter_div)
    filters["order_by"] = order_by
    filters["agg_group_by"] = agg_group_by
    filters["normalize"] = normalize
    scalar_graph_options = preprocessing.extract_graph_options("scalars", graph_scalars_options)
    ts_graph_options = preprocessing.extract_graph_options("timeseries", graph_timeseries_options)

    db_filter = Filter(
        name=name,
        filters=filters,
        scalar_graph_options=scalar_graph_options,
        ts_graph_options=ts_graph_options,
    )
    db.session.add(db_filter)
    db.session.commit()

    return get_model_options(Filter), ""


@app.callback(
    [
        Output(component_id="load_colors", component_property="options"),
        Output(component_id="save_colors_name", component_property="value"),
        Output(component_id="colors_error", component_property="children"),
    ],
    Input("save_colors", "n_clicks"),
    [
        State(component_id="save_colors_name", component_property="value"),
        State(component_id="colors", component_property="value"),
    ],
)
def save_colors(_, name, str_colors):
    if not name:
        raise PreventUpdate

    try:
        colors = json.loads(str_colors)
    except json.JSONDecodeError as je:
        flash(
            f"Could not read color mapping. Input must be valid JSON. (Error: {je})",
            "error",
        )
        return get_model_options(Colors), "", show_logs()[0]

    db_colors = Colors(name=name, colors=colors,)
    db.session.add(db_colors)
    db.session.commit()

    return get_model_options(Colors), "", show_logs()[0]


@app.callback(
    [
        Output(component_id="load_labels", component_property="options"),
        Output(component_id="save_labels_name", component_property="value"),
        Output(component_id="labels_error", component_property="children"),
    ],
    Input("save_labels", "n_clicks"),
    [
        State(component_id="save_labels_name", component_property="value"),
        State(component_id="labels", component_property="value"),
    ],
)
def save_labels(_, name, str_labels):
    if not name:
        raise PreventUpdate

    try:
        labels = json.loads(str_labels)
    except json.JSONDecodeError as je:
        flash(
            f"Could not read labels. Input must be valid JSON. (Error: {je})", "error"
        )
        return get_model_options(Labels), "", show_logs()[0]

    db_labels = Labels(name=name, labels=labels,)
    db.session.add(db_labels)
    db.session.commit()

    return get_model_options(Labels), "", show_logs()[0]


@app.callback(
    [
        Output(component_id="load_scenarios", component_property="options"),
        Output(component_id="save_scenarios_name", component_property="value"),
        Output(component_id="scenarios_error", component_property="children"),
    ],
    Input("save_scenarios", "n_clicks"),
    [
        State(component_id="save_scenarios_name", component_property="value"),
        State(component_id="dd_scenario", component_property="value"),
    ],
)
def save_scenarios(_, name, scenario_ids):
    if not name or not scenario_ids:
        raise PreventUpdate

    db_scenarios = Scenarios(name=name, ids=scenario_ids,)
    db.session.add(db_scenarios)
    db.session.commit()

    return get_model_options(Scenarios), "", show_logs()[0]


# TODO: Fixed arg number can possibly fixed with Dash 2.0 allowing for keyword args,
#  but Dash 2.0 breaks CSS styles
@app.callback(
    [
        Output(component_id="graph_scalars_plot_switch", component_property="value"),
        Output(component_id="graph_timeseries_plot_switch", component_property="value"),
        Output(component_id="order_by", component_property="value"),
        Output(component_id="aggregation_group_by", component_property="value"),
        Output(component_id="normalize", component_property="value"),
    ]
    + [
        Output(
            component_id={"name": filter_, "type": "filter-dropdown"},
            component_property="value",
        )
        for filter_ in SC_FILTERS
    ]
    + [Output(component_id="save_load_errors", component_property="children")],
    [
        Input("load_filters", "value"),
    ] +
    [Input(f"all_{filter_}", "n_clicks") for filter_ in SC_FILTERS],
    State(component_id="dd_scenario", component_property="value"),
    prevent_initial_call=True,
)
def load_filters(name, _, __, ___, ____, _____, ______, _______, ________, scenarios):
    if not scenarios:
        flash("No scenario selected - cannot load filters without scenario", "error")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            *([no_update] * len(SC_FILTERS)),
            show_logs()[0],
        )

    ctx = dash.callback_context

    # All Button clicked:
    if ctx.triggered[0]["prop_id"].endswith("n_clicks"):
        current_filter = ctx.triggered[0]["prop_id"][4:-9]
        raw_filter_values = get_multiple_scenario_filters(*scenarios)
        scan_filters = {current_filter: SC_FILTERS[current_filter]}
        current_filter_options = preprocessing.get_filter_options(
            raw_filter_values,
            filter_list=scan_filters,
            as_options=False
        )
        filter_options = [no_update] * len(SC_FILTERS)
        current_filter_index = list(SC_FILTERS.keys()).index(current_filter)
        filter_options[current_filter_index] = list(current_filter_options[current_filter])
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            *filter_options,
            show_logs()[0],
        )

    # Load filters:
    if not name:
        raise PreventUpdate
    db_filter = Filter.query.filter_by(name=name).first()
    filters = [db_filter.filters.get(filter_, None) for filter_ in SC_FILTERS]
    flash("Successfully loaded filters", "info")
    return (
        db_filter.scalar_graph_options["type"],
        db_filter.ts_graph_options["type"],
        db_filter.filters.get("order_by", []),
        db_filter.filters["agg_group_by"],
        db_filter.filters["normalize"] if "normalize" in db_filter.filters else no_update,
        *filters,
        show_logs()[0],
    )


@app.callback(
    Output(component_id="colors", component_property="value"),
    Input("load_colors", "value"),
    prevent_initial_call=True,
)
def load_colors(name):
    if not name:
        raise PreventUpdate

    db_colors = Colors.query.filter_by(name=name).first()
    return json.dumps(db_colors.colors)


@app.callback(
    Output(component_id="labels", component_property="value"),
    Input("load_labels", "value"),
    prevent_initial_call=True,
)
def load_labels(name):
    if not name:
        raise PreventUpdate

    db_labels = Labels.query.filter_by(name=name).first()
    return json.dumps(db_labels.labels)


@app.callback(
    Output(component_id="dd_scenario", component_property="value"),
    Input("load_scenarios", "value"),
    prevent_initial_call=True,
)
def load_scenarios(name):
    if not name:
        raise PreventUpdate

    db_scenarios = Scenarios.query.filter_by(name=name).first()
    return db_scenarios.ids


@app.callback(
    [
        Output(
            component_id={"name": filter_, "type": "filter-dropdown"},
            component_property="options",
        )
        for filter_ in SC_FILTERS
    ],
    [Input(component_id="dd_scenario", component_property="value")],
)
def load_scenario(scenarios):
    if scenarios is None:
        raise PreventUpdate
    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    filters = get_multiple_scenario_filters(*scenarios)
    app.logger.info("Data successfully loaded")
    return preprocessing.get_filter_options(filters)


@app.callback(
    [Output(component_id="graph_scalars_options", component_property="children")],
    [
        Input(component_id="graph_scalars_plot_switch", component_property="value"),
        Input("load_filters", "value"),
    ],
    prevent_initial_call=True,
)
def toggle_scalar_graph_options(plot_type, name):
    # Have to use "callback_context" as every component can only have one output callback
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] == "graph_scalars_plot_switch.value":
        graph_scalar_options = get_graph_options("scalars", plot_type)
    else:
        if not name:
            raise PreventUpdate
        db_filter = Filter.query.filter_by(name=name).first()
        graph_scalar_options = get_graph_options(
            "scalars",
            db_filter.scalar_graph_options["type"],
            db_filter.scalar_graph_options["options"],
        )
    return (graph_scalar_options,)


@app.callback(
    [Output(component_id="graph_timeseries_options", component_property="children")],
    [
        Input(component_id="graph_timeseries_plot_switch", component_property="value"),
        Input("load_filters", "value"),
    ],
    prevent_initial_call=True,
)
def toggle_timeseries_graph_options(plot_type, name):
    # Have to use "callback_context" as every component can only have one output callback
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] == "graph_timeseries_plot_switch.value":
        graph_timeseries_options = get_graph_options("timeseries", plot_type)
    else:
        if not name:
            raise PreventUpdate
        db_filter = Filter.query.filter_by(name=name).first()
        graph_timeseries_options = get_graph_options(
            "timeseries",
            db_filter.ts_graph_options["type"],
            db_filter.ts_graph_options["options"],
        )
    return (graph_timeseries_options,)


@app.callback(
    [
        Output(component_id="graph_scalars", component_property="figure"),
        Output(component_id="table_scalars", component_property="data"),
        Output(component_id="table_scalars", component_property="columns"),
        Output(component_id="graph_scalars_error", component_property="children"),
        Output(component_id="tab_scalars_error", component_property="labelClassName"),
        Output(component_id="view-dashboard_scalars", component_property="className"),
        Output(component_id="view-dashboard-data_scalars", component_property="className"),
        Output(component_id="table_div_scalars", component_property="style"),
    ],
    [
        Input(component_id="refresh_scalars", component_property="n_clicks"),
        Input(component_id="view-dashboard_scalars", component_property="n_clicks"),
        Input(component_id="view-dashboard-data_scalars", component_property="n_clicks"),
    ],
    [
        State(component_id="view-dashboard-data_scalars", component_property="className"),
        State(component_id="units", component_property="children"),
        State(component_id="graph_scalars_options", component_property="children"),
        State(component_id="filters", component_property="children"),
        State(component_id="colors", component_property="value"),
        State(component_id="labels", component_property="value"),
        State(component_id="order_by", component_property="value"),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id="normalize", component_property="value"),
        State(component_id="dd_scenario", component_property="value"),
    ],
    prevent_initial_call=True,
)
def scalar_graph(
    _,
    __,
    ___,
    show_data_cls,
    units_div,
    graph_scalars_options,
    filter_div,
    colors,
    labels,
    order_by,
    agg_group_by,
    normalize,
    scenarios,
):
    if scenarios is None:
        raise PreventUpdate

    # Check if data shall be shown:
    show_data = show_data_cls and "active" in show_data_cls
    data_div_cls = no_update, no_update, no_update
    ctx = dash.callback_context
    if "view-dashboard-data" in ctx.triggered[0]["prop_id"]:
        if show_data:
            raise PreventUpdate
        show_data = True
        data_div_cls = "view view--dashboard", "view view--dashboard-data active", {}
    elif "view-dashboard" in ctx.triggered[0]["prop_id"]:
        if not show_data:
            raise PreventUpdate
        show_data = False
        data_div_cls = "view view--dashboard active", "view view--dashboard-data", {"display": "none"}

    data = get_multiple_scenario_data(*scenarios, table="oed_scalars")
    filters = preprocessing.extract_filters("scalars", filter_div)
    units = preprocessing.extract_unit_options(units_div)
    graph_options = preprocessing.extract_graph_options("scalars", graph_scalars_options)
    colors = preprocessing.extract_colors(colors)
    graph_options["options"]["color_discrete_map"] = colors
    labels = preprocessing.extract_labels(labels)
    try:
        preprocessed_data = preprocessing.prepare_scalars(
            data, order_by, agg_group_by, units, filters, labels
        )
    except preprocessing.PreprocessingError:
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls
    if preprocessed_data.empty:
        flash("No data for current filter settings", "warning")
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls
    if normalize:
        preprocessed_data = preprocessing.normalize_data(preprocessed_data, graph_options)
    try:
        fig = graphs.get_scalar_plot(preprocessed_data, graph_options)
    except graphs.PlottingError:
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls

    if show_data:
        columns = [{"name": i, "id": i} for i in preprocessed_data.columns]
        data_table = preprocessed_data.applymap(str).to_dict("records")
    else:
        columns = []
        data_table = []

    log_div, log_level = show_logs()
    return fig, data_table, columns, log_div, log_level, *data_div_cls


@app.callback(
    [
        Output(component_id="graph_timeseries", component_property="figure"),
        Output(component_id="table_timeseries", component_property="data"),
        Output(component_id="table_timeseries", component_property="columns"),
        Output(component_id="graph_timeseries_error", component_property="children"),
        Output(component_id="tab_timeseries_error", component_property="labelClassName"),
        Output(component_id="view-dashboard_timeseries", component_property="className"),
        Output(component_id="view-dashboard-data_timeseries", component_property="className"),
        Output(component_id="table_div_timeseries", component_property="style"),
    ],
    [
        Input(component_id="refresh_timeseries", component_property="n_clicks"),
        Input(component_id="view-dashboard_timeseries", component_property="n_clicks"),
        Input(component_id="view-dashboard-data_timeseries", component_property="n_clicks"),
    ],
    [
        State(component_id="view-dashboard-data_timeseries", component_property="className"),
        State(component_id="units", component_property="children"),
        State(component_id="graph_timeseries_options", component_property="children"),
        State(component_id="filters", component_property="children"),
        State(component_id="colors", component_property="value"),
        State(component_id="labels", component_property="value"),
        State(component_id="order_by", component_property="value"),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id="dd_scenario", component_property="value"),
    ],
    prevent_initial_call=True,
)
def timeseries_graph(
    _,
    __,
    ___,
    show_data_cls,
    units_div,
    graph_timeseries_options,
    filter_div,
    colors,
    labels,
    order_by,
    agg_group_by,
    scenarios,
):
    if scenarios is None or SKIP_TS:
        raise PreventUpdate

    # Check if data shall be shown:
    show_data = show_data_cls and "active" in show_data_cls
    data_div_cls = no_update, no_update, no_update
    ctx = dash.callback_context
    if "view-dashboard-data" in ctx.triggered[0]["prop_id"]:
        if show_data:
            raise PreventUpdate
        data_div_cls = "view view--dashboard", "view view--dashboard-data active", {}
    elif "view-dashboard" in ctx.triggered[0]["prop_id"]:
        if not show_data:
            raise PreventUpdate
        show_data = False
        data_div_cls = "view view--dashboard active", "view view--dashboard-data", {"display": "none"}

    data = get_multiple_scenario_data(*scenarios, table="oed_timeseries")
    filters = preprocessing.extract_filters("timeseries", filter_div)
    units = preprocessing.extract_unit_options(units_div)
    graph_options = preprocessing.extract_graph_options("timeseries", graph_timeseries_options)
    colors = preprocessing.extract_colors(colors)
    graph_options["options"]["color_discrete_map"] = colors
    labels = preprocessing.extract_labels(labels)
    try:
        preprocessed_data = preprocessing.prepare_timeseries(
            data, order_by, agg_group_by, units, filters, labels
        )
    except preprocessing.PreprocessingError:
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls
    if preprocessed_data.empty:
        flash("No data for current filter settings", "warning")
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls
    try:
        fig = graphs.get_timeseries_plot(preprocessed_data, graph_options)
    except graphs.PlottingError:
        log_div, log_level = show_logs()
        return graphs.get_empty_fig(), [], [], log_div, log_level, *data_div_cls

    if show_data:
        columns = [{"name": i, "id": i} for i in preprocessed_data.columns]
        data_table = preprocessed_data.applymap(str).to_dict("records")
    else:
        columns = []
        data_table = []

    log_div, log_level = show_logs()
    return fig, data_table, columns, log_div, log_level, *data_div_cls


def show_logs():
    errors = get_flashed_messages(category_filter=["error"])
    warnings = get_flashed_messages(category_filter=["warning"])
    if len(warnings) > MAX_WARNINGS:
        warnings = warnings[:MAX_WARNINGS]
        warnings.append(
            f"Too many warnings (>{MAX_WARNINGS}) - Skipping further warnings..."
        )
    infos = get_flashed_messages(category_filter=["info"])
    if len(infos) > MAX_INFOS:
        infos = infos[:MAX_INFOS]
        infos.append(f"Too many infos (>{MAX_INFOS}) - Skipping further infos...")
    level = "infos"
    if errors:
        level = "errors"
    elif warnings:
        level = "warnings"
    return get_error_and_warnings_div(errors, warnings, infos), level


if __name__ == "__main__":
    app.run_server(
        debug=DEBUG, use_debugger=False, use_reloader=False, passthrough_errors=True
    )
