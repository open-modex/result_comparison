import os
import pathlib

import urllib3

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask_caching import Cache

import filters
from layout import get_layout
from settings import FILTERS
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

CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    "CACHE_TYPE": "filesystem",
    "CACHE_REDIS_URL": os.environ.get("REDIS_URL"),
    "CACHE_DIR": "cache-directory",
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)


@cache.memoize()
def get_scenario_data(scenario_id):
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
    return filters.get_filter_options(data)


@app.callback(
    Output(component_id='graph_scalar', component_property='figure'),
    [Input(component_id="dd_scenario", component_property="value")] +
    [Input(component_id=f"filter_{filter_}", component_property='value') for filter_ in FILTERS]
)
def scalar_graph(scenarios, *filter_args):
    if scenarios is None:
        raise PreventUpdate
    data = get_multiple_scenario_data(*scenarios)
    filter_kwargs = filters.extract_filters(filter_args)
    return graphs.get_scalar_plot(data["oed_scalars"], filter_kwargs)


if __name__ == "__main__":
    app.run_server(debug=True)
