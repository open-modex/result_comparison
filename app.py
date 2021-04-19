import pathlib

import urllib3

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask_caching import Cache

from data import dev
import preprocessing
from layout import get_layout, create_warnings, get_graph_options
from settings import DEBUG, SKIP_TS, FILTERS, TS_FILTERS, GRAPHS_DEFAULT_OPTIONS, USE_DUMMY_DATA, CACHE_CONFIG
import scenario
import graphs

urllib3.disable_warnings()

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"},
    ],
)
app.layout = get_layout(app, scenarios=scenario.get_scenarios())
server = app.server

# Cache
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)


@cache.memoize()
def get_scenario_data(scenario_id):
    if USE_DUMMY_DATA:
        return dev.get_dummy_data()
    return scenario.get_scenario_data(scenario_id)


@cache.memoize()
def get_multiple_scenario_data(*scenario_ids):
    scenarios = [
        get_scenario_data(scenario_id) for scenario_id in scenario_ids
    ]
    return scenario.merge_scenario_data(scenarios)


@app.callback(
    [Output(component_id=f"filter_{filter_}", component_property="options") for filter_ in FILTERS],
    [Input(component_id="dd_scenario", component_property="value")],
)
def load_scenario(scenarios):
    if scenarios is None:
        raise PreventUpdate
    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    data = get_multiple_scenario_data(*scenarios)
    return preprocessing.get_filter_options(data)


@app.callback(
    [Output(component_id=f"graph_scalars_options", component_property="children")],
    [Input(component_id="graph_scalars_plot_switch", component_property="value")],
)
def toggle_scalar_graph_options(plot_type):
    return get_graph_options("scalars", plot_type),


@app.callback(
    [Output(component_id=f"graph_timeseries_options", component_property="children")],
    [Input(component_id="graph_timeseries_plot_switch", component_property="value")],
)
def toggle_timeseries_graph_options(plot_type):
    return get_graph_options("timeseries", plot_type),


# @app.callback(
#     [
#         Output(component_id='graph_scalars', component_property='figure'),
#         Output(component_id='graph_scalars_error', component_property='children'),
#         Output(component_id='graph_scalars_error', component_property='style'),
#     ],
#     [
#         Input(component_id="dd_scenario", component_property="value"),
#         Input(component_id="aggregation_group_by", component_property="value"),
#         Input(component_id="graph_scalars_plot_switch", component_property="value"),
#     ] +
#     [Input(component_id=f"filter_{filter_}", component_property='value') for filter_ in FILTERS] +
#     [
#         Input(component_id=f"graph_scalars_option_{option}", component_property='value')
#         for option in GRAPHS_DEFAULT_OPTIONS["scalars"]
#     ]
# )
# def scalar_graph(scenarios, agg_group_by, use_custom_graph_options, *filter_args):
#     if scenarios is None:
#         raise PreventUpdate
#     data = get_multiple_scenario_data(*scenarios)
#     filters, graph_options = preprocessing.extract_filters_and_options("scalars", filter_args, use_custom_graph_options)
#     preprocessed_data = preprocessing.prepare_scalars(data["scalars"], agg_group_by, filters)
#     try:
#         fig = graphs.get_scalar_plot(preprocessed_data, graph_options)
#     except ValueError as ve:
#         return graphs.get_empty_fig(), f"Error: {str(ve)}", {"color": "red"}
#     return fig, "", {}
#
#
# @app.callback(
#     [
#         Output(component_id='graph_timeseries', component_property='figure'),
#         Output(component_id='graph_timeseries_error', component_property='children'),
#         Output(component_id='graph_timeseries_error', component_property='style'),
#     ],
#     [
#         Input(component_id="dd_scenario", component_property="value"),
#         Input(component_id="aggregation_group_by", component_property="value"),
#         Input(component_id="graph_timeseries_options_switch", component_property="value"),
#     ] +
#     [Input(component_id=f"filter_{filter_}", component_property='value') for filter_ in TS_FILTERS] +
#     [
#         Input(component_id=f"graph_timeseries_option_{option}", component_property='value')
#         for option in GRAPHS_DEFAULT_OPTIONS["timeseries"]
#     ]
# )
# def timeseries_graph(scenarios, agg_group_by, use_custom_graph_options, *filter_args):
#     if scenarios is None or SKIP_TS:
#         raise PreventUpdate
#     data = get_multiple_scenario_data(*scenarios)
#     filters, graph_options = preprocessing.extract_filters_and_options(
#         "timeseries", filter_args, use_custom_graph_options
#     )
#     preprocessed_data = preprocessing.prepare_timeseries(data["timeseries"], agg_group_by, filters)
#     warnings = preprocessing.check_timeseries_data(preprocessed_data)
#     try:
#         fig = graphs.get_timeseries_plot(preprocessed_data, graph_options)
#     except ValueError as ve:
#         return graphs.get_empty_fig(), f"Error: {str(ve)}", {"color": "red"}
#     if warnings:
#         return fig, create_warnings(warnings), {"color": "orange"}
#     else:
#         return fig, "", {}


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
