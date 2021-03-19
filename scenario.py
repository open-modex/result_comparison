import json
import requests
import jmespath
from itertools import chain

from settings import FILTERS

OEP_URL = "https://openenergy-platform.org"
CONNECTOR_URL = "https://modex.rl-institut.de/scenario/id/"


def get_scenarios():
    fields = ["scenario", "id", "source"]
    query = {
        "fields": fields,
        "distinct": True,
        "from": {
            "type": "table",
            "table": "oed_scenario_output",
            "schema": "model_draft",
        },
        # TODO: Order-by id
    }
    response = requests.post(OEP_URL + "/api/v0/advanced/search", json={"query": query})
    data = response.json()["data"]
    return [dict(zip(fields, row)) for row in data]


def get_scenario_data(scenario_id):
    response = requests.get(
        CONNECTOR_URL + str(scenario_id),
        {"mapping": "concrete", "source": "modex_output"},
        timeout=10000,
        verify=False,
    )
    return json.loads(response.text)


def merge_scenario_data(scenario_data):
    # Merge scalars and timeseries, throw away scenario infos:
    return {
        key: list(chain.from_iterable([items[key] for items in scenario_data]))
        for key in ("oed_scalars", "oed_timeseries")
    }


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
