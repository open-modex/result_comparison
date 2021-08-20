
from collections import ChainMap

import pandas
from flask import flash
from plotly import express as px
from plotly import graph_objects as go

from settings import (
    COLUMN_JOINER, GRAPHS_DEFAULT_LAYOUT, GRAPHS_DEFAULT_XAXES_LAYOUT, GRAPHS_DEFAULT_YAXES_LAYOUT,
    GRAPHS_DEFAULT_TEMPLATE, GRAPHS_DEFAULT_OPTIONS, GRAPHS_MAX_TS_PER_PLOT
)


class PlottingError(Exception):
    """Thrown if plotting goes wrong"""


def get_empty_fig():
    empty_fig = px.bar()
    empty_fig.update_layout(
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    return empty_fig


def trim_timeseries(timeseries, max_entries=GRAPHS_MAX_TS_PER_PLOT):
    if len(timeseries.columns) > max_entries:
        flash(
            f"Too many timeseries to plot; only {max_entries} series are plotted.",
            category="warning",
        )
        timeseries = timeseries.loc[:, timeseries.columns[:max_entries]]
    return timeseries


def add_unit_to_label(label, data):
    if isinstance(data.columns, pandas.MultiIndex):
        units = data.columns.get_level_values("unit").unique()
    else:
        units = data["unit"].unique()
    if len(units) == 1:
        return f"{label} [{units[0]}]"
    return label


def get_scalar_plot(data, options):
    if options["type"] == "bar":
        return bar_plot(data, options["options"])
    elif options["type"] == "radar":
        return radar_plot(data, options["options"])
    elif options["type"] == "dot":
        return dot_plot(data, options["options"])


def bar_plot(data, options):
    xaxis_title = options.pop("xaxis_title")
    yaxis_title = options.pop("yaxis_title")
    layout = {
        "legend_title": options.pop("legend_title"),
        "bargap": options.pop("bargap"),
        "margin_l": options.pop("margin_l"),
        "margin_r": options.pop("margin_r"),
        "margin_t": options.pop("margin_t"),
        "margin_b": options.pop("margin_b"),
    }
    labels = options.pop("labels")
    subplot_label = options.pop("subplot_label")

    fig_options = ChainMap(
        options,
        GRAPHS_DEFAULT_OPTIONS["scalars"]["bar"].get_defaults(exclude_non_plotly_options=True)
    )
    try:
        fig = px.bar(
            data,
            **fig_options
        )
    except ValueError as ve:
        if str(ve) == "nan is not in list":
            flash(
                f"Scalar plot error: {ve} " +
                f"(This might occur due to 'nan' values in data. Please check data via 'Show data')",
                category="error"
            )
        else:
            flash(f"Scalar plot error: {ve}", category="error")
        raise PlottingError(f"Scalar plot error: {ve}")

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)
    if subplot_label:
        fig.for_each_annotation(lambda a: a.update(text=f"{subplot_label} {a.text.split('=')[-1]}"))
    else:
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Remove padding between stacked bars:
    fig.update_traces(
        marker={"line": {"width": 0}}
    )

    unit_axis = "x" if fig_options["orientation"] == "h" else "y"
    if unit_axis == "x" and not xaxis_title:
        layout["xaxis_title"] = add_unit_to_label(fig_options["x"], data)
    if unit_axis == "y" and not yaxis_title:
        layout["yaxis_title"] = add_unit_to_label(fig_options["y"], data)
    if xaxis_title:
        fig.update_xaxes(title=xaxis_title)
    if yaxis_title:
        fig.update_yaxes(row=1, col=1, title=yaxis_title)

    try:
        fig.update_layout(
            template=GRAPHS_DEFAULT_TEMPLATE,
            **layout,
            **GRAPHS_DEFAULT_LAYOUT
        )
    except ValueError as ve:
        flash(f"Scalar layout error: {ve}", category="error")
        raise PlottingError(f"Scalar layout error: {ve}")
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig


def radar_plot(data, options):
    axis_title = options.pop("axis_title") or add_unit_to_label(options["r"], data)
    labels = options.pop("labels")

    categories = data[options["theta"]].unique()

    fig = go.Figure()
    for ellipse in data[options["color"]].unique():
        fig.add_trace(
            go.Scatterpolar(
                r=data[data[options["color"]] == ellipse][options["r"]],
                theta=categories,
                fill='toself',
                name=ellipse
            )
        )

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)

    fig.update_layout(
        polar={
            "radialaxis": {
                "title": axis_title,
                "visible": True,
                "range": [data[options["r"]].min(), data[options["r"]].max()]
            }
        },
        showlegend=False,
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig


def dot_plot(data, options):
    y = data[options["y"]].unique()
    xaxis_title = options.pop("xaxis_title") or add_unit_to_label(options["x"], data)
    legend_title = options.pop("legend_title")
    labels = options.pop("labels")

    fig = go.Figure()

    for category in data[options["color"]].unique():
        cat_data = data[data[options["color"]] == category][options["x"]]
        fig.add_trace(go.Scatter(
            x=cat_data,
            y=y,
            name=category,
        ))

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)

    fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))
    fig.update_layout(
        xaxis_title=xaxis_title,
        legend_title=legend_title,
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig


def get_timeseries_plot(data, options):
    if options["type"] == "line":
        return line_plot(data, options["options"])
    elif options["type"] == "box":
        return box_plot(data, options["options"])
    elif options["type"] == "heat_map":
        return heat_map(data, options["options"])


def line_plot(data, options):
    xaxis_title = options.pop("xaxis_title") or "Timeindex"
    yaxis_title = options.pop("yaxis_title") or add_unit_to_label("", data)
    legend_title = options.pop("legend_title")
    labels = options.pop("labels")
    fig_options = ChainMap(
        options,
        GRAPHS_DEFAULT_OPTIONS["timeseries"]["line"].get_defaults(exclude_non_plotly_options=True)
    )
    data = trim_timeseries(data)
    data.columns = [COLUMN_JOINER.join(map(str, column)) for column in data.columns]
    fig_options["y"] = [column for column in data.columns]
    try:
        fig = px.line(
            data.reset_index(),
            x="index",
            **fig_options
        )
    except ValueError as ve:
        flash(f"Timeseries plot error: {ve}", category="error")
        raise PlottingError(f"Timeseries plot error: {ve}")
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

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)

    fig.update_layout(
        yaxis_title=yaxis_title,
        xaxis_title=xaxis_title,
        legend_title=legend_title,
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig


def box_plot(data, options):
    xaxis_title = options.pop("xaxis_title") or "Time"
    yaxis_title = options.pop("yaxis_title")
    legend_title = options.pop("legend_title")
    labels = options.pop("labels")
    sample = options.pop("sample")
    fig_options = ChainMap(
        options,
        GRAPHS_DEFAULT_OPTIONS["timeseries"]["box"].get_defaults(exclude_non_plotly_options=True)
    )
    fig_options["x"] = "time"
    fig_options["y"] = "value"

    ts_resampled = data.resample(sample).sum()
    ts_resampled.index.name = "time"
    ts_unstacked = ts_resampled.unstack()
    ts_unstacked.name = "value"
    ts_flattened = ts_unstacked.reset_index()

    try:
        fig = px.box(
            ts_flattened,
            points="outliers",
            **fig_options
        )
    except ValueError as ve:
        flash(f"Timeseries plot error: {ve}", category="error")
        raise PlottingError(f"Timeseries plot error: {ve}")

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title or add_unit_to_label(fig_options["y"], ts_flattened),
        legend_title=legend_title,
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig


def heat_map(data, options):
    x = options.pop("x")
    y = options.pop("y")
    xaxis_title = options.pop("xaxis_title") or x
    yaxis_title = options.pop("yaxis_title") or y
    legend_title = options.pop("legend_title") or add_unit_to_label("Value", data)
    labels = options.pop("labels")

    fig_options = ChainMap(
        options,
        GRAPHS_DEFAULT_OPTIONS["timeseries"]["heat_map"].get_defaults(exclude_non_plotly_options=True)
    )

    data.index.name = "time"
    ts_unstacked = data.unstack()
    ts_unstacked.name = "value"
    ts_flattened = ts_unstacked.reset_index()
    ts_flattened["day"] = ts_flattened["time"].apply(lambda time: time.day)
    ts_flattened["month"] = ts_flattened["time"].apply(lambda time: time.month)
    ts_flattened["year"] = ts_flattened["time"].apply(lambda time: time.year)
    ts_grouped = ts_flattened.groupby([x, y], as_index=False).sum()
    ts_pivot = ts_grouped.pivot(index=y, columns=x, values="value")

    try:
        fig = px.imshow(
            ts_pivot,
            labels={
                "x": xaxis_title,
                "y": yaxis_title,
                "color": legend_title
            },
            **fig_options
        )
    except ValueError as ve:
        flash(f"Timeseries plot error: {ve}", category="error")
        raise PlottingError(f"Timeseries plot error: {ve}")

    # Override labels:
    if labels:
        for trace in fig.data:
            trace.name = labels.get(trace.name, trace.name)

    fig.update_xaxes(side="top")
    fig.update_layout(
        template=GRAPHS_DEFAULT_TEMPLATE,
        **GRAPHS_DEFAULT_LAYOUT
    )
    fig.update_xaxes(GRAPHS_DEFAULT_XAXES_LAYOUT)
    fig.update_yaxes(GRAPHS_DEFAULT_YAXES_LAYOUT)
    return fig
