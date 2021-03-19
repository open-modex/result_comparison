import json
import requests
from itertools import chain

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
