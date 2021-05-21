import os
import json

from scenario import get_scenario_data
from settings import DATA_PATH, DATA_SCENARIO_PATH


def get_dummy_data(scenario_id):
    with open(f"{DATA_PATH}/{DATA_SCENARIO_PATH}/{scenario_id}.json", 'r') as dummy_data_file:
        data = json.load(dummy_data_file)
    return data


def create_dummy_data(scenario_id):
    data = get_scenario_data(scenario_id, as_text=True)
    with open(f"{DATA_PATH}/{DATA_SCENARIO_PATH}/{scenario_id}.json", "w") as dummy_file:
        dummy_file.write(data)


if __name__ == "__main__":
    sc_id = os.environ["SCENARIO_ID"]
    create_dummy_data(sc_id)
