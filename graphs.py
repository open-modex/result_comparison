
from collections import ChainMap
from plotly import express as px

from settings import GRAPHS_DEFAULT_COLOR_MAP, GRAPHS_DEFAULT_LAYOUT, GRAPHS_DEFAULT_OPTIONS


def get_empty_fig():
    empty_fig = px.bar()
    empty_fig.update_layout(GRAPHS_DEFAULT_LAYOUT)
    return empty_fig


def get_scalar_plot(data, options):
    fig_options = ChainMap(options, GRAPHS_DEFAULT_OPTIONS["scalars"])
    fig = px.bar(
        data,
        orientation="h",
        color_discrete_map=GRAPHS_DEFAULT_COLOR_MAP,
        labels={"source": "Simulation Framework"},
        **fig_options
    )
    fig.update_layout(GRAPHS_DEFAULT_LAYOUT)
    return fig


def get_timeseries_plot(data, options):
    fig_options = ChainMap(options, GRAPHS_DEFAULT_OPTIONS["timeseries"])
    fig = px.bar(
        data,
        orientation="h",
        color_discrete_map=GRAPHS_DEFAULT_COLOR_MAP,
        labels={"source": "Simulation Framework"},
        **fig_options
    )
    fig.update_layout(GRAPHS_DEFAULT_LAYOUT)
    return fig
