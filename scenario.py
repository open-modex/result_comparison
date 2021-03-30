import json
import requests
from itertools import chain

from frictionless import Resource, validate_resource

from settings import MODEX_OUTPUT_SCHEMA, DATA_PATH

OEP_URL = "https://openenergy-platform.org"
CONNECTOR_URL = "https://modex.rl-institut.de/scenario/id/"


class ScenarioError(Exception):
    """Raised if scenario data is invalid"""


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
        "order_by": [
            {
                "type": "column",
                "column": "id"
            }
        ]
    }
    response = requests.post(OEP_URL + "/api/v0/advanced/search", json={"query": query})
    data = response.json()["data"]
    return [dict(zip(fields, row)) for row in data]


def get_scenario_data(scenario_id):
    response = requests.get(
        CONNECTOR_URL + str(scenario_id),
        {"mapping": "regions", "source": "modex_output"},
        timeout=10000,
        verify=False,
    )
    data = json.loads(response.text)
    validate_scenario_data(data)
    return data


def validate_scenario_data(data):
    for table in ("scenario", "scalars", "timeseries"):
        resource = Resource(
            name=table, profile="tabular-data-resource", data=data[table], schema=MODEX_OUTPUT_SCHEMA[table]
        )
        report = validate_resource(resource)
        if report["stats"]["errors"] != 0:
            with open(f"{DATA_PATH}/error_{table}.json", "w") as error_file:
                error_file.write(report.to_json())
            raise ScenarioError("Invalid")


def merge_scenario_data(scenario_data):
    # Merge scalars and timeseries, throw away scenario infos:
    return {
        key: list(chain.from_iterable([items[key] for items in scenario_data]))
        for key in ("scalars", "timeseries")
    }
