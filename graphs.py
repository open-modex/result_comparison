
from functools import reduce
import pandas
import numpy as np
import plotly.express as px

from settings import FILTERS


def get_scalar_plot(data, filters):
    df = pandas.DataFrame(data)
    if filters:
        conditions = [df[filter_].isin(filter_value) for filter_, filter_value in filters.items()]
        df = df[reduce(np.logical_and, conditions)]
    fig = px.bar(
        df,
        orientation="h",
        x="value",
        y="source",
        text="parameter_name",
        color_discrete_map={
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
        },
        hover_name="region",
        hover_data=["technology", "parameter_name", "unit"],
        labels={"source": "Simulation Framework"},
    )

    fig_layout = fig["layout"]
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#ffffff"
    fig_layout["legend_bgcolor"] = "#1f2630"
    fig_layout["title"]["font"]["color"] = "#3391CF"
    fig_layout["xaxis"]["tickfont"]["color"] = "#ffffff"
    fig_layout["yaxis"]["tickfont"]["color"] = "#ffffff"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["margin"]["t"] = 50
    fig_layout["margin"]["r"] = 50
    fig_layout["margin"]["b"] = 50
    fig_layout["margin"]["l"] = 50

    return fig
