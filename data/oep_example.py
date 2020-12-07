
import json
import requests
import  pandas

CONNECTOR_URL = "https://modex.rl-institut.de/scenario/id/"


def get_scenario_data(scenario_id):
    response = requests.get(CONNECTOR_URL + str(scenario_id), {"source": "modex","mapping": "concrete"}, timeout=10000, verify=False)
    json_data = json.loads(response.text)
    data = {timeseries["output_energy_vector"]: timeseries["series"] for timeseries in json_data["oed_timeseries"]}
    data["hour"] = range(8784)
    return pandas.DataFrame(data)
