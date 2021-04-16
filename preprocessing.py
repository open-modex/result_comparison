import jmespath
from functools import reduce
import pandas
import numpy as np
from flask import flash

from settings import FILTERS, TS_FILTERS, GRAPHS_DEFAULT_OPTIONS, GRAPHS_MAX_TS_PER_PLOT


class PreprocessingError(Exception):
    """Error is thrown if preprocessing goes wrong"""


def get_filter_options(scenario_data):
    filters = {}
    for filter_, filter_format in FILTERS.items():
        jmespath_str = f"[scalars, timeseries][].{filter_}"
        if filter_format["type"] == "list":
            jmespath_str += "[]"
        filters[filter_] = set(jmespath.search(jmespath_str, scenario_data))
    output = (
        [{"label": filter_option, "value": filter_option} for filter_option in filter_options]
        for _, filter_options in filters.items()
    )
    return list(output)


def extract_filters_and_options(type_, filters, use_graph_options):
    if type_ == "timeseries":
        filter_kwargs = {filter_: filters[i] for i, filter_ in enumerate(TS_FILTERS) if filters[i]}
    else:
        filter_kwargs = {filter_: filters[i] for i, filter_ in enumerate(FILTERS) if filters[i]}
    if use_graph_options == "default":
        graph_options = {}
    else:
        graph_options = {
            option: filters[len(FILTERS) + i]
            for i, option in enumerate(GRAPHS_DEFAULT_OPTIONS[type_])
            if filters[len(FILTERS) + i]
        }
    return filter_kwargs, graph_options


def prepare_data(data, group_by, aggregation_func, filters):
    if filters:
        conditions = [data[filter_].isin(filter_value) for filter_, filter_value in filters.items()]
        data = data[reduce(np.logical_and, conditions)]
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        data = data.groupby(group_by).aggregate(aggregation_func)
    return data


def prepare_scalars(data, group_by, filters):
    df = pandas.DataFrame(data)
    return prepare_data(df, group_by, "sum", filters).reset_index()


def prepare_timeseries(data, group_by, filters):
    def sum_series(series):
        """
        Enables ndarray summing into one ndarray

        If len == 1 check wasn't there pandas gets confused and neglects series column in agg
        """
        if len(series) == 1:
            return series
        return sum(series)

    df = pandas.DataFrame.from_dict(data)
    df.series = df.series.apply(lambda x: np.array(x))
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        group_by = ["timeindex_start", "timeindex_stop", "timeindex_resolution"] + group_by
    ts_series_grouped = prepare_data(df, group_by, sum_series, filters)
    timeseries = []
    for index, row in ts_series_grouped.iterrows():
        # TODO: Freq should be read from index[2]!
        if group_by:
            dates = pandas.date_range(start=index[0], end=index[1], freq="H")
            name = "_".join(index[3 + i] for i in range(group_by))
        else:
            dates = pandas.date_range(start=row["timeindex_start"], end=row["timeindex_stop"], freq="H")
            name = "_".join(row[filter_] for filter_ in TS_FILTERS)
        try:
            series = pandas.Series(name=name, data=row.series, index=dates)
        except ValueError as ve:
            flash(f"Timeseries '{name}' entries and date range don't fit: {ve}", category="error")
            raise PreprocessingError(f"Timeseries entries and date range don't fit: {ve}")
        timeseries.append(series)
    return pandas.concat(timeseries, axis=1)


def check_timeseries_data(data):
    duplicate_columns = sum(data.columns.duplicated())
    if duplicate_columns > 0:
        flash("Found duplicate timeseries; duplicates will be neglected", category="warning")
    if len(data.columns) - duplicate_columns > GRAPHS_MAX_TS_PER_PLOT:
        flash(f"Too many timeseries to plot; only {GRAPHS_MAX_TS_PER_PLOT} series are plotted.", category="warning")
