
import os
import json
import warnings
from dataclasses import dataclass
from typing import Union, List, Dict, Optional
import pandas as pd

VERSION = "0.16.0"

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    warnings.warn("No secret key found - never run in production mode without a secret key!")
DEBUG = os.environ.get("DEBUG", "False") == "True"
MANAGE_DB = os.environ.get("MANAGE_DB", "False") == "True"

USE_DUMMY_DATA = os.environ.get("USE_DUMMY_DATA", "False") == "True"
SKIP_TS = os.environ.get("SKIP_TS", "False") == "True"

DB_URL = os.environ.get("DB_URL")
if not DB_URL:
    warnings.warn("No DB set up - runnning without DB support!")

CACHE_CONFIG = {
    "CACHE_TYPE": "filesystem" if DEBUG else "redis",
    "CACHE_REDIS_URL": os.environ.get("REDIS_URL"),
    "CACHE_DIR": "cache",
}

DATA_PATH = "data"
DATA_SCENARIO_PATH = "scenarios"
DATAPACKAGE = "datapackage.json"

COLUMN_JOINER = "-"

with open(f"{DATA_PATH}/{DATAPACKAGE}", 'r') as datapackage_file:
    datapackage = json.loads(datapackage_file.read())
    MODEX_OUTPUT_SCHEMA = {resource["name"]: resource["schema"] for resource in datapackage["resources"]}

with open("README.md", "r") as readme_file:
    doc_lines = []
    for i, line in enumerate(readme_file.readlines()):
        if i < 3:
            continue
        if line.startswith("## Setup"):
            break
        doc_lines.append(line)
DOCUMENTATION = "".join(doc_lines)


# FILTERS

SC_FILTERS = {
    "year": {"type": "int"},
    "region": {"type": "str"},
    "technology": {"type": "str"},
    "technology_type": {"type": "str"},
    "parameter_name": {"type": "str"},
    "input_energy_vector": {"type": "str"},
    "output_energy_vector": {"type": "str"},
    "source": {"type": "str"},
}
TS_FILTERS = {k: v for k, v in SC_FILTERS.items() if k != "year"}

SC_COLUMNS = list(SC_FILTERS) + ["value", "unit"]
TS_COLUMNS = list(TS_FILTERS) + ["series", "unit", "timeindex_start", "timeindex_stop", "timeindex_resolution"]


# GRAPHS

GRAPHS_MAX_TS_PER_PLOT = 20


@dataclass
class GraphOption:
    label: str
    default: Union[str, List[Dict[str, str]], bool]
    type: str = "dropdown"
    step: Optional[str] = None
    from_filter: bool = True
    clearable: bool = False
    plotly_option: bool = True
    category: str = "General"


class GraphOptions:
    def __init__(self, **kwargs):
        self.options = dict(**kwargs)

    def get_defaults(self, exclude_non_plotly_options=False):
        return {
            name: option.default if option.from_filter else option.default[0]["value"]
            for name, option in self.options.items() if not (exclude_non_plotly_options and not option.plotly_option)
        }

    def __getitem__(self, item):
        return self.options[item]


GRAPHS_DEFAULT_OPTIONS = {
    "scalars": {
        "bar": GraphOptions(
            x=GraphOption("X-Axis", "value"),
            y=GraphOption("Y-Axis", "source"),
            text=GraphOption("Text", "parameter_name", clearable=True),
            color=GraphOption("Color", "parameter_name"),
            hover_name=GraphOption("Hover", "region"),
            axis_type=GraphOption(
                label="Axis Type",
                default=[{"label": "linear", "value": "linear"}, {"label": "logarithmic", "value": "log"}],
                from_filter=False,
                plotly_option=False
            ),
            orientation=GraphOption(
                label="Orientation",
                default=[{"label": "horizontal", "value": "h"}, {"label": "vertical", "value": "v"}],
                from_filter=False,
            ),
            barmode=GraphOption(
                label="Mode",
                default=[{"label": mode, "value": mode} for mode in ('relative', 'group', 'overlay')],
                from_filter=False,
            ),
            facet_col=GraphOption("Subplots", "", clearable=True),
            facet_col_wrap=GraphOption("Subplots per row", "5", type="int"),
            height=GraphOption("Chart Height", "", type="int", category="Display"),
            xaxis_title=GraphOption("X-Axis Title", "", type="input", plotly_option=False, category="Display"),
            yaxis_title=GraphOption("Y-Axis Title", "", type="input", plotly_option=False, category="Display"),
            subplot_label=GraphOption("Subplot Title", "", type="input", plotly_option=False, category="Display"),
            showlegend=GraphOption(
                "Show Legend",
                default=[{"label": "Show Legend", "value": "showlegend"}],
                type="bool",
                from_filter=False,
                plotly_option=False,
                category="Display"
            ),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
            bargap=GraphOption("Bar Gap", "", type="float", plotly_option=False, category="Display"),
            margin_l=GraphOption("Margin Left", "", type="int", plotly_option=False, category="Display"),
            margin_r=GraphOption("Margin Right", "", type="int", plotly_option=False, category="Display"),
            margin_t=GraphOption("Margin Top", "", type="int", plotly_option=False, category="Display"),
            margin_b=GraphOption("Margin Bottom", "", type="int", plotly_option=False, category="Display"),
            facet_row_spacing=GraphOption("Subplot Spacing", "0.07", type="float", step="0.01", category="Display"),
        ),
        "radar": GraphOptions(
            r=GraphOption("Radius", "value"),
            theta=GraphOption("Theta", "technology"),
            color=GraphOption("Color", "source"),
            normalize_theta=GraphOption(
                "Normalize Theta",
                default=[{"label": "Normalize Theta", "value": "normalize"}],
                type="bool",
                from_filter=False,
                plotly_option=False,
            ),
            axis_title=GraphOption("Radar Axis Title", "", type="input", plotly_option=False, category="Display"),
            showlegend=GraphOption(
                "Show Legend",
                default=[{"label": "Show Legend", "value": "showlegend"}],
                type="bool",
                from_filter=False,
                plotly_option=False,
                category="Display"
            ),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
            height=GraphOption("Chart Height", "", type="int", category="Display"),
            margin_l=GraphOption("Margin Left", "", type="int", plotly_option=False, category="Display"),
            margin_r=GraphOption("Margin Right", "", type="int", plotly_option=False, category="Display"),
            margin_t=GraphOption("Margin Top", "", type="int", plotly_option=False, category="Display"),
            margin_b=GraphOption("Margin Bottom", "", type="int", plotly_option=False, category="Display"),
        ),
        "dot": GraphOptions(
            x=GraphOption("X-Axis", "value"),
            y=GraphOption("Y-Axis", "technology"),
            color=GraphOption("Color", "source"),
            xaxis_title=GraphOption("X-Axis Title", "", type="input", plotly_option=False, category="Display"),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
        ),
    },
    "timeseries": {
        "line": GraphOptions(
            xaxis_title=GraphOption("X-Axis Title", "", type="input", plotly_option=False, category="Display"),
            yaxis_title=GraphOption("Y-Axis Title", "", type="input", plotly_option=False, category="Display"),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
        ),
        "box": GraphOptions(
            color=GraphOption("Color", "source"),
            sample=GraphOption(
                label="Sample",
                default=[
                    {"label": "1 month", "value": "M"},
                    {"label": "6 months", "value": "6M"},
                    {"label": "1 year", "value": "Y"}
                ],
                from_filter=False,
                plotly_option=False
            ),
            facet_col=GraphOption("Subplots", "", clearable=True),
            xaxis_title=GraphOption("X-Axis Title", "", type="input", plotly_option=False, category="Display"),
            yaxis_title=GraphOption("Y-Axis Title", "", type="input", plotly_option=False, category="Display"),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
        ),
        "heat_map": GraphOptions(
            x=GraphOption(
                label="X-Axis",
                default=[
                    {"label": "Months", "value": "month"},
                    {"label": "Years", "value": "year"},
                ],
                from_filter=False,
                plotly_option=False
            ),
            y=GraphOption(
                label="Y-Axis",
                default=[
                    {"label": "Days", "value": "day"},
                    {"label": "Months", "value": "month"},
                    {"label": "Years", "value": "year"}
                ] + [{"label": filter_, "value": filter_} for filter_ in TS_FILTERS],
                from_filter=False,
                plotly_option=False
            ),
            xaxis_title=GraphOption("X-Axis Title", "", type="input", plotly_option=False, category="Display"),
            yaxis_title=GraphOption("Y-Axis Title", "", type="input", plotly_option=False, category="Display"),
            legend_title=GraphOption("Legend Title", "", type="input", plotly_option=False, category="Display"),
        ),
    }
}

GRAPHS_DEFAULT_COLOR_MAP = {
    "variable cost": "#407FB7",
    "fixed cost": "#00549F",
    "renewable generation": "#00549F",
}

GRAPHS_DEFAULT_LABELS = {}

GRID_COLOR = "lightgray"

GRAPHS_DEFAULT_TEMPLATE = "plotly_white"
GRAPHS_DEFAULT_LAYOUT = {
    "legend": {
        "font": {"size": 14},
    }
}
GRAPHS_DEFAULT_XAXES_LAYOUT = {
    "autorange": True,
    "title": {"font": {"size": 18}},
    "gridcolor": GRID_COLOR,
    "linecolor": GRID_COLOR,
    "linewidth": 2,
    "mirror": True,
    "showline": True,
    "ticks": "outside",
    "tickcolor": GRID_COLOR,
    "tickfont": {"size": 14},
}
GRAPHS_DEFAULT_YAXES_LAYOUT = {
    "autorange": True,
    "title": {"font": {"size": 18}},
    "gridcolor": GRID_COLOR,
    "linecolor": GRID_COLOR,
    "linewidth": 2,
    "mirror": True,
    "showline": True,
    "ticks": "outside",
    "tickcolor": GRID_COLOR,
    "tickfont": {"size": 14},
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

# UNITS

UNITS = {
    "Energy": {
        "units": ["kWh", "MWh", "GWh", "TWh"],
        "default": "GWh"
    },
    "Power": {
        "units": ["kW", "MW", "GW", "TW"],
        "default": "GW"
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


# ERRORS AND WARNINGS
MAX_WARNINGS = 10
MAX_INFOS = 10
