import json

from scenario import get_scenario_data
from settings import DATA_PATH


def get_dummy_data():
    with open(f"{DATA_PATH}/dummy_data.json", 'r') as dummy_data_file:
        data = json.load(dummy_data_file)
    return data


def create_dummy_data(scenario_id):
    data = get_scenario_data(scenario_id)
    with open(f"{DATA_PATH}/dummy_data.json", "w") as dummy_file:
        json.dump(data, dummy_file)
