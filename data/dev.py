import os
import json

from scenario import get_scenario_data
from settings import DATA_PATH, DATA_SCENARIO_PATH, SKIP_TS


def get_dummy_data(scenario_id, table):
    with open(f"{DATA_PATH}/{DATA_SCENARIO_PATH}/{scenario_id}_{table}.json", 'r') as dummy_data_file:
        data = json.load(dummy_data_file)
    return data


def create_dummy_data(scenario_id):
    tables = ["oed_scalars"] if SKIP_TS else ["oed_scalars", "oed_timeseries"]
    for table in tables:
        data = get_scenario_data(scenario_id, table)
        with open(f"{DATA_PATH}/{DATA_SCENARIO_PATH}/{scenario_id}_{table}.json", "w") as dummy_file:
            json.dump(data, dummy_file)


def get_dummy_filters(scenario_id):
    with open(f"{DATA_PATH}/{DATA_SCENARIO_PATH}/{scenario_id}_oed_scalars.json", 'r') as dummy_data_file:
        data = json.load(dummy_data_file)
    return data


if __name__ == "__main__":
    IDS = [346, 311, 305, 339, 362]
    for i, id_ in enumerate(IDS):
        print(f"Getting {i + 1}/{len(IDS)}: ID #{id_}")
        create_dummy_data(id_)
