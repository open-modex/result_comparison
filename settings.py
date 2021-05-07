
import os
import json
from dataclasses import dataclass
from typing import Union, List, Dict
import pandas as pd

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False") == "True"
MANAGE_DB = os.environ.get("MANAGE_DB", "False") == "True"

USE_DUMMY_DATA = os.environ.get("USE_DUMMY_DATA", "False") == "True"
SKIP_TS = os.environ.get("SKIP_TS", "False") == "True"

DB_URL = os.environ["DB_URL"]

CACHE_CONFIG = {
    "CACHE_TYPE": "filesystem" if DEBUG else "redis",
    "CACHE_REDIS_URL": os.environ.get("REDIS_URL"),
    "CACHE_DIR": "cache",
}

DATA_PATH = "data"
DATAPACKAGE = "datapackage.json"

with open(f"{DATA_PATH}/{DATAPACKAGE}", 'r') as datapackage_file:
    datapackage = json.loads(datapackage_file.read())
    MODEX_OUTPUT_SCHEMA = {resource["name"]: resource["schema"] for resource in datapackage["resources"]}

# GRAPHS

GRAPHS_MAX_TS_PER_PLOT = 20


@dataclass
class GraphOption:
    value: Union[str, List[Dict[str, str]]]
    from_filter: bool = True


class GraphOptions:
    def __init__(self, **kwargs):
        self.options = dict(**kwargs)

    def get_defaults(self):
        return {
            name: option.value if option.from_filter else option.value[0]["value"]
            for name, option in self.options.items()
        }

    def __getitem__(self, item):
        return self.options[item]


GRAPHS_DEFAULT_OPTIONS = {
    "scalars": {
        "bar": GraphOptions(
            x=GraphOption("value"),
            y=GraphOption("source"),
            text=GraphOption("parameter_name"),
            color=GraphOption("parameter_name"),
            hover_name=GraphOption("region"),
            orientation=GraphOption(
                [{"label": "horizontal", "value": "h"}, {"label": "vertical", "value": "v"}], False)
        ),
        "radar": GraphOptions(
            r=GraphOption("value"),
            theta=GraphOption("technology"),
            color=GraphOption("source")
        ),
        "dot": GraphOptions(
            x=GraphOption("value"),
            y=GraphOption("technology"),
            color=GraphOption("source")
        ),
    },
    "timeseries": {
        "line": GraphOptions(),
    }
}

GRAPHS_DEFAULT_COLOR_MAP = {
    "BB": "#5E5D5F",
    "BE": "#5E5D5F",
    "BW": "#5E5D5F",
    "BY": "#5E5D5F",
    "HB": "#5E5D5F",
    "HE": "#5E5D5F",
    "HH": "#5E5D5F",
    "MV": "#5E5D5F",
    "NI": "#00549F",
    "NW": "#5E5D5F",
    "RP": "#5E5D5F",
    "SH": "#5E5D5F",
    "SL": "#5E5D5F",
    "SN": "#5E5D5F",
    "ST": "#5E5D5F",
    "TH": "#5E5D5F",
    "variable cost": "#407FB7",
    "fixed cost": "#00549F",
    "renewable generation": "#00549F",
}

GRAPHS_DEFAULT_LAYOUT = {
    "paper_bgcolor": "#1f2630",
    "plot_bgcolor": "#1f2630",
    "font": {"color": "#ffffff"},
    "legend_bgcolor": "#1f2630",
    "title": {"font": {"color": "#3391CF"}},
    "xaxis": {
        "gridcolor": "#5b5b5b",
        "tickfont": {"color": "#ffffff"}},
    "yaxis": {
        "gridcolor": "#5b5b5b",
        "tickfont": {"color": "#ffffff"}
    },
    "margin": {
        "t": 50,
        "r": 50,
        "b": 50,
        "l": 50,
    }
}

# MAP

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
MAPBOX_STYLE = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


# REGIONS

STATES = pd.read_csv(
    "assets/states_list.csv",
    engine="python",
    index_col=False,
    delimiter=";",
    dtype={"abbrev": str},
)
REGIONS = {state["abbrev"]: state["Bundesland"] for _, state in STATES.iterrows()}

# FILTERS

FILTERS = {
    "year": {"type": "int"},
    "region": {"type": "str"},
    "technology": {"type": "str"},
    "technology_type": {"type": "str"},
    "parameter_name": {"type": "str"},
    "input_energy_vector": {"type": "str"},
    "output_energy_vector": {"type": "str"},
    "source": {"type": "str"},
}
TS_FILTERS = {k: v for k, v in FILTERS.items() if k != "year"}

# UNITS

UNITS = {
    "Energy": {
        "units": ["kWh", "MWh", "GWh", "TWh"],
        "default": "GWh"
    },
    "Energy per Year": {
        "units": ["kWh/a", "MWh/a", "GWh/a", "TWh/a"],
        "default": "GWh/a"
    },
    "Power per Hour": {
        "units": ["kW/h", "MW/h", "GW/h", "TW/h"],
        "default": "MW/h"
    },
    "Mass": {
        "units": ["Mt", "Gt"],
        "default": "Gt"
    },
    "Mass per year": {
        "units": ["Mt/a", "Gt/a"],
        "default": "Gt/a"
    }
}
