import json
import pathlib

import urllib3
from functools import partial

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dash import no_update
import dash_bootstrap_components as dbc
from flask import flash, get_flashed_messages
from flask_caching import Cache

from data import dev
import preprocessing
from settings import (
    SECRET_KEY, DB_URL, DEBUG, MANAGE_DB, SKIP_TS, SC_FILTERS, USE_DUMMY_DATA, CACHE_CONFIG, MAX_WARNINGS, MAX_INFOS)
import scenario
import graphs
from models import db, get_model_options, Filter, Colors, Labels

urllib3.disable_warnings()

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"},
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
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
    from layout import get_layout, get_graph_options, get_error_and_warnings_div
    app.layout = partial(get_layout, app, scenarios=scenario.get_scenarios())


@cache.memoize()
def get_scenario_data(scenario_id, table):
    app.logger.info(f"Loading scenario data #{scenario_id} (not cached)...")
    if USE_DUMMY_DATA:
        return dev.get_dummy_data(scenario_id, table)
    return scenario.get_scenario_data(scenario_id, table)


@cache.memoize()
def get_multiple_scenario_data(*scenario_ids, table):
    app.logger.info("Merging scenario data (not cached)...")
    scenarios = [
        get_scenario_data(scenario_id, table) for scenario_id in scenario_ids
    ]
    merged = scenario.merge_scenario_data(scenarios)
    app.logger.info("Merged scenario data")
    return merged


@cache.memoize()
def get_multiple_scenario_filters(*scenario_ids):
    app.logger.info("Merging scenario data (not cached)...")
    scenarios = [
        scenario.get_scenario_filters(scenario_id) for scenario_id in scenario_ids
    ]
    merged = scenario.merge_scenario_data(scenarios)
    app.logger.info("Merged scenario data")
    return merged


@app.callback(
    Output(component_id="dd_scenario", component_property="options"),
    Input('scenario_reload', 'n_clicks'),
)
def reload_scenarios(_):
    scenarios = scenario.get_scenarios()
    return [
        {
            "label": f"{sc['id']}, {sc['scenario']}, {sc['source']}",
            "value": sc["id"],
        }
        for sc in scenarios
    ]


@app.callback(
    [
        Output(component_id="load_filters", component_property="options"),
        Output(component_id="save_filters_name", component_property="value"),
    ],
    Input('save_filters', 'n_clicks'),
    [
        State(component_id="save_filters_name", component_property="value"),
        State(component_id=f"graph_scalars_options", component_property='children'),
        State(component_id=f"graph_timeseries_options", component_property='children'),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id=f"filters", component_property='children')
    ]
)
def save_filters(_, name, graph_scalars_options, graph_timeseries_options, agg_group_by, filter_div):
    if not name:
        raise PreventUpdate

    filters = preprocessing.extract_filters("scalars", filter_div)
    filters["agg_group_by"] = agg_group_by
    scalar_graph_options = preprocessing.extract_graph_options(graph_scalars_options)
    ts_graph_options = preprocessing.extract_graph_options(graph_timeseries_options)

    db_filter = Filter(
        name=name,
        filters=filters,
        scalar_graph_options=scalar_graph_options,
        ts_graph_options=ts_graph_options
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
    Input('save_colors', 'n_clicks'),
    [
        State(component_id="save_colors_name", component_property="value"),
        State(component_id="colors", component_property='value')
    ]
)
def save_colors(_, name, str_colors):
    if not name:
        raise PreventUpdate

    try:
        colors = json.loads(str_colors)
    except json.JSONDecodeError as je:
        flash(f"Could not read color mapping. Input must be valid JSON. (Error: {je})", "error")
        return get_model_options(Colors), "", show_logs()

    db_colors = Colors(
        name=name,
        colors=colors,
    )
    db.session.add(db_colors)
    db.session.commit()

    return get_model_options(Colors), "", show_logs()


@app.callback(
    [
        Output(component_id="load_labels", component_property="options"),
        Output(component_id="save_labels_name", component_property="value"),
        Output(component_id="labels_error", component_property="children"),
    ],
    Input('save_labels', 'n_clicks'),
    [
        State(component_id="save_labels_name", component_property="value"),
        State(component_id="labels", component_property='value')
    ]
)
def save_labels(_, name, str_labels):
    if not name:
        raise PreventUpdate

    try:
        labels = json.loads(str_labels)
    except json.JSONDecodeError as je:
        flash(f"Could not read labels. Input must be valid JSON. (Error: {je})", "error")
        return get_model_options(Labels), "", show_logs()

    db_labels = Labels(
        name=name,
        labels=labels,
    )
    db.session.add(db_labels)
    db.session.commit()

    return get_model_options(Labels), "", show_logs()


@app.callback(
    [
        Output(component_id="graph_scalars_plot_switch", component_property="value"),
        Output(component_id="graph_timeseries_plot_switch", component_property="value"),
        Output(component_id="aggregation_group_by", component_property="value")
    ] +
    [Output(component_id=f"filter-{filter_}", component_property='value') for filter_ in SC_FILTERS] +
    [Output(component_id="save_load_errors", component_property="children")],
    Input('load_filters', "value"),
    State(component_id="dd_scenario", component_property="value"),
    prevent_initial_call=True
)
def load_filters(name, scenarios):
    if not name:
        raise PreventUpdate
    if not scenarios:
        flash("No scenario selected - cannot load filters without scenario", "error")
        return (
            no_update,
            no_update,
            no_update,
            *([no_update] * len(SC_FILTERS)),
            show_logs(),
        )
    db_filter = Filter.query.filter_by(name=name).first()
    filters = [db_filter.filters.get(filter_, None) for filter_ in SC_FILTERS]
    flash("Successfully loaded filters", "info")
    return (
        db_filter.scalar_graph_options["type"],
        db_filter.ts_graph_options["type"],
        db_filter.filters["agg_group_by"],
        *filters,
        show_logs(),
    )


@app.callback(
    Output(component_id="colors", component_property="value"),
    Input('load_colors', "value"),
    prevent_initial_call=True
)
def load_colors(name):
    if not name:
        raise PreventUpdate

    db_colors = Colors.query.filter_by(name=name).first()
    return json.dumps(db_colors.colors)


@app.callback(
    Output(component_id="labels", component_property="value"),
    Input('load_labels', "value"),
    prevent_initial_call=True
)
def load_labels(name):
    if not name:
        raise PreventUpdate

    db_labels = Labels.query.filter_by(name=name).first()
    return json.dumps(db_labels.labels)


@app.callback(
    [Output(component_id=f"filter-{filter_}", component_property="options") for filter_ in SC_FILTERS],
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
    [Output(component_id=f"graph_scalars_options", component_property="children")],
    [
        Input(component_id="graph_scalars_plot_switch", component_property="value"),
        Input('load_filters', "value"),
    ],
    prevent_initial_call=True
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
            "scalars", db_filter.scalar_graph_options["type"], db_filter.scalar_graph_options["options"])
    return graph_scalar_options,


@app.callback(
    [Output(component_id=f"graph_timeseries_options", component_property="children")],
    [
        Input(component_id="graph_timeseries_plot_switch", component_property="value"),
        Input('load_filters', "value"),
    ],
    prevent_initial_call=True
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
            "timeseries", db_filter.ts_graph_options["type"], db_filter.ts_graph_options["options"])
    return graph_timeseries_options,


@app.callback(
    [
        Output(component_id='graph_scalars', component_property='figure'),
        Output(component_id='table_scalars', component_property='data'),
        Output(component_id='table_scalars', component_property='columns'),
        Output(component_id='graph_scalars_error', component_property='children'),
    ],
    [
        Input(component_id="refresh_scalars", component_property="n_clicks"),
        Input(component_id="show_scalars_data", component_property='value'),
    ],
    [
        State(component_id="units", component_property='children'),
        State(component_id=f"graph_scalars_options", component_property='children'),
        State(component_id=f"filters", component_property='children'),
        State(component_id="colors", component_property="value"),
        State(component_id="labels", component_property="value"),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id="dd_scenario", component_property="value"),
    ],
    prevent_initial_call=True
)
def scalar_graph(_, show_data, units_div, graph_scalars_options, filter_div, colors, labels, agg_group_by, scenarios):
    if scenarios is None:
        raise PreventUpdate
    data = get_multiple_scenario_data(*scenarios, table="oed_scalars")
    filters = preprocessing.extract_filters("scalars", filter_div)
    units = preprocessing.extract_unit_options(units_div)
    graph_options = preprocessing.extract_graph_options(graph_scalars_options)
    colors = preprocessing.extract_colors(colors)
    graph_options["options"]["color_discrete_map"] = colors
    labels = preprocessing.extract_labels(labels)
    graph_options["options"]["labels"] = labels
    try:
        preprocessed_data = preprocessing.prepare_scalars(data, agg_group_by, units, filters)
    except preprocessing.PreprocessingError:
        return graphs.get_empty_fig(), [], [], show_logs()
    if preprocessed_data.empty:
        flash("No data for current filter settings", "warning")
        return graphs.get_empty_fig(), [], [], show_logs()
    try:
        fig = graphs.get_scalar_plot(preprocessed_data, graph_options)
    except graphs.PlottingError:
        return graphs.get_empty_fig(), [], [], show_logs()

    if show_data and "True" in show_data:
        columns = [{"name": i, "id": i} for i in preprocessed_data.columns]
        data_table = preprocessed_data.applymap(str).to_dict("records")
    else:
        columns = []
        data_table = []
    return fig, data_table, columns, show_logs()


@app.callback(
    [
        Output(component_id='graph_timeseries', component_property='figure'),
        Output(component_id='table_timeseries', component_property='data'),
        Output(component_id='table_timeseries', component_property='columns'),
        Output(component_id='graph_timeseries_error', component_property='children'),
    ],
    [
        Input(component_id="refresh_timeseries", component_property="n_clicks"),
        Input(component_id="show_timeseries_data", component_property='value'),
    ],
    [
        State(component_id="units", component_property='children'),
        State(component_id="graph_timeseries_options", component_property='children'),
        State(component_id=f"filters", component_property='children'),
        State(component_id="colors", component_property="value"),
        State(component_id="labels", component_property="value"),
        State(component_id="aggregation_group_by", component_property="value"),
        State(component_id="dd_scenario", component_property="value"),
    ],
    prevent_initial_call=True
)
def timeseries_graph(
        _, show_data, units_div, graph_timeseries_options, filter_div, colors, labels, agg_group_by, scenarios
):
    if scenarios is None or SKIP_TS:
        raise PreventUpdate
    data = get_multiple_scenario_data(*scenarios, table="oed_timeseries")
    filters = preprocessing.extract_filters(
        "timeseries", filter_div
    )
    units = preprocessing.extract_unit_options(units_div)
    graph_options = preprocessing.extract_graph_options(graph_timeseries_options)
    colors = preprocessing.extract_colors(colors)
    graph_options["options"]["color_discrete_map"] = colors
    labels = preprocessing.extract_labels(labels)
    graph_options["options"]["labels"] = labels
    try:
        preprocessed_data = preprocessing.prepare_timeseries(data, agg_group_by, units, filters)
    except preprocessing.PreprocessingError:
        return graphs.get_empty_fig(), [], [], show_logs()
    if preprocessed_data.empty:
        flash("No data for current filter settings", "warning")
        return graphs.get_empty_fig(), [], [], show_logs()
    try:
        fig = graphs.get_timeseries_plot(preprocessed_data, graph_options)
    except graphs.PlottingError:
        return graphs.get_empty_fig(), [], [], show_logs()

    if show_data and "True" in show_data:
        columns = [{"name": i, "id": i} for i in preprocessed_data.columns]
        data_table = preprocessed_data.applymap(str).to_dict("records")
    else:
        columns = []
        data_table = []

    return fig, data_table, columns, show_logs()


def show_logs():
    errors = get_flashed_messages(category_filter=["error"])
    warnings = get_flashed_messages(category_filter=["warning"])
    if len(warnings) > MAX_WARNINGS:
        warnings = warnings[:MAX_WARNINGS]
        warnings.append(f"Too many warnings (>{MAX_WARNINGS}) - Skipping further warnings...")
    infos = get_flashed_messages(category_filter=["info"])
    if len(infos) > MAX_INFOS:
        infos = infos[:MAX_INFOS]
        infos.append(f"Too many infos (>{MAX_INFOS}) - Skipping further infos...")
    return get_error_and_warnings_div(errors, warnings, infos)


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
