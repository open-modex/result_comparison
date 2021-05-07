import jmespath
from functools import reduce
import pandas
import numpy as np
from flask import flash
from units import unit, scaled_unit, NamedComposedUnit
from units.predefined import define_units
from units.registry import REGISTRY
from units.exception import IncompatibleUnitsError

from settings import FILTERS, TS_FILTERS, GRAPHS_MAX_TS_PER_PLOT


def define_energy_model_units():
    scaled_unit("kW", "W", 1e3)
    scaled_unit("MW", "kW", 1e3)
    scaled_unit("GW", "MW", 1e3)
    scaled_unit("TW", "GW", 1e3)

    scaled_unit('a', 'day', 365)

    scaled_unit('kt', 't', 1e3)
    scaled_unit('Mt', 'kt', 1e3)
    scaled_unit('Gt', 'Mt', 1e3)

    NamedComposedUnit("kt/a", unit("kt") / unit("a"))
    NamedComposedUnit("Mt/a", unit("Mt") / unit("a"))
    NamedComposedUnit("Gt/a", unit("Gt") / unit("a"))

    NamedComposedUnit("kWh", unit("kW") * unit("h"))
    NamedComposedUnit("MWh", unit("MW") * unit("h"))
    NamedComposedUnit("GWh", unit("GW") * unit("h"))
    NamedComposedUnit("TWh", unit("TW") * unit("h"))

    NamedComposedUnit("kWh/a", unit("kWh") / unit("a"))
    NamedComposedUnit("MWh/a", unit("MWh") / unit("a"))
    NamedComposedUnit("GWh/a", unit("GWh") / unit("a"))
    NamedComposedUnit("TWh/a", unit("TWh") / unit("a"))

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
    for filter_, filter_format in FILTERS.items():
        jmespath_str = f"[oed_scalars, od_timeseries][].{filter_}"
        if filter_format["type"] == "list":
            jmespath_str += "[]"
        filters[filter_] = set(jmespath.search(jmespath_str, scenario_data))
    output = (
        [{"label": filter_option, "value": filter_option} for filter_option in filter_options]
        for _, filter_options in filters.items()
    )
    return list(output)


def extract_filters(type_, filter_div):
    if type_ == "timeseries":
        filters = TS_FILTERS
    else:
        filters = FILTERS
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
            item["props"]["id"].split("-")[1]: item["props"]["value"]
            for item in graph_div if item["type"] == "Dropdown"
        }
    }
    return options


def extract_unit_options(units_div):
    return [unit_div["props"]["value"] for unit_div in units_div if unit_div["type"] == "Dropdown"]


def sum_series(series):
    """
    Enables ndarray summing into one ndarray

    If len == 1 check wasn't there pandas gets confused and neglects series column in agg
    """
    if len(series) == 1:
        return series.tolist()
    summed_series = sum(series)
    if isinstance(summed_series, np.ndarray):
        return summed_series.tolist()
    else:
        return summed_series


def prepare_data(data, group_by, aggregation_func, units, filters):
    if filters:
        conditions = []
        for filter_, filter_value in filters.items():
            if FILTERS[filter_]["type"] == "list":
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
        data = data.groupby(group_by).aggregate(aggregation_func)
    return data


def prepare_scalars(data, group_by, units, filters):
    df = pandas.DataFrame(data)
    df = prepare_data(df, group_by, "sum", units, filters).reset_index()
    return df


def prepare_timeseries(data, group_by, units, filters):
    df = pandas.DataFrame.from_dict(data)
    df.series = df.series.apply(lambda x: np.array(x))
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        group_by = ["timeindex_start", "timeindex_stop", "timeindex_resolution"] + group_by
    ts_series_grouped = prepare_data(df, group_by, sum_series, units, filters)
    timeseries, fixed_timeseries = concat_timeseries(group_by, ts_series_grouped)
    reduced_timeseries = remove_duplicates_and_trim_timeseries(timeseries)
    for name, (dates, entries) in fixed_timeseries.items():
        if name not in reduced_timeseries.columns:
            continue
        flash(
            f"Timeindex of timeseries '{name}' has different length than series elements "
            f"({dates}/{entries}). Timeindex has been guessed.",
            category="warning"
        )
    return reduced_timeseries


def remove_duplicates_and_trim_timeseries(timeseries):
    duplicate_columns = sum(timeseries.columns.duplicated())
    if duplicate_columns > 0:
        flash("Found duplicate timeseries; duplicates will be neglected", category="warning")
    # Remove duplicate columns:
    timeseries = timeseries.loc[:, ~timeseries.columns.duplicated()]
    if len(timeseries.columns) > GRAPHS_MAX_TS_PER_PLOT:
        flash(f"Too many timeseries to plot; only {GRAPHS_MAX_TS_PER_PLOT} series are plotted.", category="warning")
        timeseries = timeseries.loc[:, timeseries.columns[:GRAPHS_MAX_TS_PER_PLOT]]
    return timeseries


def concat_timeseries(group_by, ts_series_grouped):
    timeseries = []
    fixed_timeseries = {}
    for index, row in ts_series_grouped.iterrows():
        # TODO: Freq should be read from index[2]!
        if group_by:
            dates = pandas.date_range(start=index[0], end=index[1], freq="H")
            name = "_".join(index[3 + i] for i in range(len(group_by) - 3))
        else:
            dates = pandas.date_range(start=row["timeindex_start"], end=row["timeindex_stop"], freq="H")
            name = "_".join(str(row[filter_]) for filter_ in TS_FILTERS)
        if len(dates) != len(row.series):
            fixed_timeseries[name] = len(dates), len(row.series)
            dates = pandas.date_range(start=row["timeindex_start"], freq="H", periods=len(row.series))
        series = pandas.Series(name=name, data=row.series, index=dates)
        timeseries.append(series)
    return pandas.concat(timeseries, axis=1), fixed_timeseries
