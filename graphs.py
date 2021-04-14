
from collections import ChainMap
from plotly import express as px

from settings import GRAPHS_DEFAULT_COLOR_MAP, GRAPHS_DEFAULT_LAYOUT, GRAPHS_DEFAULT_OPTIONS, GRAPHS_MAX_TS_PER_PLOT


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
    # Remove duplicate columns:
    data = data.loc[:, ~data.columns.duplicated()]
    fig_options = ChainMap(options, GRAPHS_DEFAULT_OPTIONS["timeseries"])
    fig_options["y"] = [column for column in data.columns[:GRAPHS_MAX_TS_PER_PLOT] if column != "index"]
    fig = px.line(
        data.reset_index(),
        color_discrete_map=GRAPHS_DEFAULT_COLOR_MAP,
        **fig_options
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector={
            "buttons": [
                {"count": 1, "label": "1d", "step": "day", "stepmode": "backward"},
                {"count": 7, "label": "1w", "step": "day", "stepmode": "backward"},
                {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
                {"count": 6, "label": "6m", "step": "month", "stepmode": "backward"},
                {"step": "all"}
            ]
        }
    )
    fig.update_layout(GRAPHS_DEFAULT_LAYOUT)
    return fig
