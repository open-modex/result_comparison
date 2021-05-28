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


def get_scenario_filters(scenario_id):
    query = {
        "from": {
            "type": "join",
            "left": {
                "type": "table",
                "table": "oed_scenario_output",
                "schema": "model_draft",
                "alias": "s",
            },
            "right": {
                "type": "table",
                "table": "oed_data_output",
                "schema": "model_draft",
                "alias": "d",
            },
            "on": {
                "operands": [
                    {"type": "column", "column": "id", "table": "s"},
                    {"type": "column", "column": "scenario_id", "table": "d"}
                ],
                "operator": "=",
                "type": "operator"
            }
        },
        "where": {
            "operands": [
                {
                    "type": "column",
                    "table": "s",
                    "column": "id"
                },
                31
            ],
            "operator": "=",
            "type": "operator"
        }
    }
    response = requests.post(OEP_URL + "/api/v0/advanced/search", json={"query": query})
    response_json = response.json()
    fields = [field[0] for field in response_json["description"]]
    return [dict(zip(fields, row)) for row in response_json["data"]]


def get_scenario_data(scenario_id, table):
    # TODO: Logging instead of print (could not find corresponding dash logger - "app.access"?)
    print(f"Requesting data for scenario #{scenario_id}...")
    response = requests.get(
        CONNECTOR_URL + str(scenario_id),
        {
            "mapping": json.dumps({
                "base_mapping": "concrete",
                "mapping": {
                    table: f"map(&set(@, 'region', join(',', @.region)), {table})",
                }
            }),
            "source": "modex_output"
        },
        timeout=10000,
        verify=False,
    )
    print(f"Loading {table} for scenario #{scenario_id}...")
    data = json.loads(response.text)
    print(f"Validating {table} for scenario #{scenario_id}...")
    validate_scenario_data(data, table)
    print(f"Successfully loaded {table} for scenario #{scenario_id}.")
    return data[table]


def validate_scenario_data(data, table):
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
    return list(chain.from_iterable([items for items in scenario_data]))
