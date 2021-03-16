import pandas as pd

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
MAPBOX_STYLE = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"
STATES = pd.read_csv(
    "assets/states_list.csv",
    engine="python",
    index_col=False,
    delimiter="\;",
    dtype={"abbrev": str},
)
REGIONS = [
    {"label": str(region), "value": str(region)} for region in STATES["abbrev"]
]
