import jmespath
from functools import reduce
import pandas
import json
import numpy as np
from collections import ChainMap
from flask import flash
from units import unit, scaled_unit, NamedComposedUnit
from units.predefined import define_units
from units.registry import REGISTRY
from units.exception import IncompatibleUnitsError

from settings import (
    SC_COLUMNS,
    TS_COLUMNS,
    SC_FILTERS,
    TS_FILTERS,
    COLUMN_JOINER,
    GRAPHS_DEFAULT_COLOR_MAP,
    GRAPHS_DEFAULT_LABELS
)


def define_energy_model_units():
    scaled_unit("kW", "W", 1e3)
    scaled_unit("MW", "kW", 1e3)
    scaled_unit("GW", "MW", 1e3)
    scaled_unit("TW", "GW", 1e3)

    scaled_unit("a", "day", 365)

    scaled_unit("kt", "t", 1e3)
    scaled_unit("Mt", "kt", 1e3)
    scaled_unit("Gt", "Mt", 1e3)

    NamedComposedUnit("kWh", unit("kW") * unit("h"))
    NamedComposedUnit("MWh", unit("MW") * unit("h"))
    NamedComposedUnit("GWh", unit("GW") * unit("h"))
    NamedComposedUnit("TWh", unit("TW") * unit("h"))

    NamedComposedUnit("kW/h", unit("kW") / unit("h"))
    NamedComposedUnit("MW/h", unit("MW") / unit("h"))
    NamedComposedUnit("GW/h", unit("GW") / unit("h"))
    NamedComposedUnit("TW/h", unit("TW") / unit("h"))


define_units()
define_energy_model_units()


def convert_units(row, convert_to):
    if "unit" not in row or row["unit"] not in REGISTRY:
        return row
    if "value" in row:
        value = unit(row["unit"])(row["value"])
        try:
            row["value"] = unit(convert_to)(value).get_num()
        except IncompatibleUnitsError:
            return row
    elif "series" in row:
        try:
            mul = unit(convert_to)(unit(row["unit"])(1)).get_num()
        except IncompatibleUnitsError:
            return row
        row["series"] = row["series"] * mul
    else:
        return row
    row["unit"] = convert_to
    return row


class PreprocessingError(Exception):
    """Error is thrown if preprocessing goes wrong"""


def get_filter_options(scenario_data):
    filters = {}
    for filter_, filter_format in SC_FILTERS.items():
        jmespath_str = f"[].{filter_}"
        if filter_format["type"] == "list":
            jmespath_str += "[]"
        try:
            filters[filter_] = set(jmespath.search(jmespath_str, scenario_data))
        except TypeError:
            filters[filter_] = {
                ','.join(items)
                for items in jmespath.search(
                    jmespath_str, scenario_data
                )
            }

    output = (
        [
            {"label": filter_option, "value": filter_option}
            for filter_option in filter_options
        ]
        for _, filter_options in filters.items()
    )
    return list(output)


def extract_filters(type_, filter_div):
    filters = TS_FILTERS if type_ == "timeseries" else SC_FILTERS
    filter_kwargs = {}
    for item in filter_div:
        if item["type"] != "Dropdown":
            continue
        name = item["props"]["id"].split("-")[1]
        if name in filters and "value" in item["props"] and item["props"]["value"]:
            filter_kwargs[name] = item["props"]["value"]
    return filter_kwargs


def extract_graph_options(graph_div):
    options = {
        "type": graph_div[0]["props"]["value"],
        "options": {
            item["props"]["id"].split("-")[1]: None if (value := item["props"]["value"]) == "" else value
            for item in graph_div
            if item["type"] in ("Dropdown", "Input") and "id" in item["props"]
        },
    }
    return options


def extract_unit_options(units_div):
    return [
        unit_div["props"]["value"]
        for unit_div in units_div
        if unit_div["type"] == "Dropdown"
    ]


def extract_colors(str_colors):
    try:
        colors = json.loads(str_colors)
    except json.JSONDecodeError as je:
        colors = {}
        flash(f"Could not read color mapping. Input must be valid JSON. (Error: {je})", "warning")
    return ChainMap(colors, GRAPHS_DEFAULT_COLOR_MAP)


def extract_labels(str_labels):
    try:
        labels = json.loads(str_labels)
    except json.JSONDecodeError as je:
        labels = {}
        flash(f"Could not read color mapping. Input must be valid JSON. (Error: {je})", "warning")
    return ChainMap(labels, GRAPHS_DEFAULT_LABELS)


def sum_series(series):
    """
    Enables ndarray summing into one list
    """
    summed_series = sum(series)
    if isinstance(summed_series, np.ndarray):
        return summed_series.tolist()
    else:
        return summed_series


def prepare_data(data, group_by, aggregation_func, units, filters):
    if filters:
        conditions = []
        for filter_, filter_value in filters.items():
            if SC_FILTERS[filter_]["type"] == "list":
                # Build regex to filter for substrings:
                conditions.append(data[filter_].str.contains("|".join(filter_value)))
            else:
                conditions.append(data[filter_].isin(filter_value))
        data = data[reduce(np.logical_and, conditions)]
    # Check units:
    all_units = data["unit"].unique()
    for unit_ in all_units:
        if unit_ not in REGISTRY:
            flash(f"Unknown unit '{unit_}' found in data.", category="warning")
    for unit_ in units:
        data = data.apply(convert_units, axis=1, convert_to=unit_)
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        if "series" in data and len(lengths := data["series"].apply(len).unique()) > 1:
            flash(f"Timeseries of different lengths {lengths} can not be aggregated.", category="error")
            raise PreprocessingError("Different ts lengths at aggregation found.")
        data = data.groupby(group_by).aggregate(aggregation_func).reset_index()
        keep_columns = group_by + ["value", "series"]
        data = data[data.columns.intersection(keep_columns)]
    return data


def prepare_scalars(data, group_by, units, filters):
    df = pandas.DataFrame(data)
    df = df.loc[:, [column for column in SC_COLUMNS]]
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        group_by.append("unit")
    df = prepare_data(df, group_by, "sum", units, filters)
    return df


def prepare_timeseries(data, group_by, units, filters):
    df = pandas.DataFrame.from_dict(data)
    df = df.loc[:, [column for column in TS_COLUMNS]]
    df.series = df.series.apply(lambda x: np.array(x))
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        group_by = [
            "timeindex_start",
            "timeindex_stop",
            "timeindex_resolution",
            "unit"
        ] + group_by
    ts_series_grouped = prepare_data(df, group_by, sum_series, units, filters)
    timeseries, fixed_timeseries = concat_timeseries(ts_series_grouped)
    for name, (dates, entries) in fixed_timeseries.items():
        flash(
            f"Timeindex of timeseries '{name}' has different length than series elements "
            f"({dates}/{entries}). Timeindex has been guessed.",
            category="warning",
        )
    return timeseries


def concat_timeseries(ts):
    columns = [
        column for column in ts.columns
        if column not in ("timeindex_start", "timeindex_stop", "timeindex_resolution", "series")
    ]
    timeseries = []
    fixed_timeseries = {}
    for index, row in ts.iterrows():
        dates = pandas.date_range(
            start=row["timeindex_start"], end=row["timeindex_stop"], freq="H"
        )
        if len(dates) != len(row.series):
            name = COLUMN_JOINER.join(map(str, row[columns]))
            fixed_timeseries[name] = len(dates), len(row.series)
            dates = pandas.date_range(
                start=row["timeindex_start"], freq="H", periods=len(row.series)
            )
        mi = pandas.MultiIndex.from_tuples([tuple(row[columns])], names=columns)
        timeseries.append(pandas.DataFrame(index=dates, columns=mi, data=row.series))
    if timeseries:
        return pandas.concat(timeseries, axis=1), fixed_timeseries
    return pandas.DataFrame(), fixed_timeseries
