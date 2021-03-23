import pandas as pd


# GRAPHS

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
    "region": {"type": "list"},
    "technology": {"type": "str"},
    "technology_type": {"type": "str"},
    "parameter_name": {"type": "str"},
    "input_energy_vector": {"type": "str"},
    "output_energy_vector": {"type": "str"},
    "source": {"type": "str"},
}
