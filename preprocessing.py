import jmespath
from functools import reduce
import pandas
import numpy as np

from settings import FILTERS


def get_filter_options(scenario_data):
    filters = {}
    for filter_, filter_format in FILTERS.items():
        jmespath_str = f"[oed_scalars, oed_timeseries][].{filter_}"
        if filter_format["type"] == "list":
            jmespath_str += "[]"
        filters[filter_] = set(jmespath.search(jmespath_str, scenario_data))
    output = (
        [{"label": filter_option, "value": filter_option} for filter_option in filter_options]
        for _, filter_options in filters.items()
    )
    return list(output)


def extract_filters(filters):
    return {filter_: filters[i] for i, filter_ in enumerate(FILTERS) if filters[i]}


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
