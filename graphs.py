
import plotly.express as px

from settings import GRAPHS_DEFAULT_COLOR_MAP, GRAPHS_DEFAULT_LAYOUT


def get_scalar_plot(data):
    fig_kwargs = {
        "x": "value",
        "y": "source",
        "text": "parameter_name",
        "color": "parameter_name",
        "hover_name": "region",
        "hover_data": ["technology", "parameter_name", "unit"],
    }
    fig = px.bar(
        data,
        orientation="h",
        color_discrete_map=GRAPHS_DEFAULT_COLOR_MAP,
        labels={"source": "Simulation Framework"},
        **fig_kwargs
    )
    fig.update_layout(GRAPHS_DEFAULT_LAYOUT)
    return fig
