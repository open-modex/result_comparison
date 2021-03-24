import jmespath
from functools import reduce
import pandas
import numpy as np

from settings import FILTERS, GRAPHS_DEFAULT_OPTIONS


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


def extract_filters_and_options(graph, filters, use_graph_options):
    filter_kwargs = {filter_: filters[i] for i, filter_ in enumerate(FILTERS) if filters[i]}
    if use_graph_options == "default":
        graph_options = {}
    else:
        graph_options = {
            option: filters[len(FILTERS) + i]
            for i, option in enumerate(GRAPHS_DEFAULT_OPTIONS[graph])
            if filters[len(FILTERS) + i]
        }
    return filter_kwargs, graph_options


def prepare_data(data, group_by, aggregation_func, filters):
    df = pandas.DataFrame(data)
    if filters:
        conditions = [df[filter_].isin(filter_value) for filter_, filter_value in filters.items()]
        df = df[reduce(np.logical_and, conditions)]
    if group_by:
        group_by = group_by if isinstance(group_by, list) else [group_by]
        # Always add "source" to group_by:
        group_by.append("source")
        df = df.groupby(group_by).aggregate(aggregation_func).reset_index()
    return df
